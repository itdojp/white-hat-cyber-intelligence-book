#!/usr/bin/env ruby
# frozen_string_literal: true

# Private exact-renderer backend for scripts/publication_projection.py.
# This file has no chapter, artifact, or Content Safety Policy knowledge.

require "json"
require "cgi"
require "uri"
require "jekyll"
require "kramdown"
require "kramdown-parser-gfm"

PROTOCOL_VERSION = "1"
PROJECTION_VERSION = "1.0.0"
SUPPORTED_BLOCKS = %i[p codeblock ul ol blockquote table dl hr blank header].freeze
MAX_FIELDS_PER_DOCUMENT = 5_000
MAX_PROJECTED_TEXT_BYTES = 2_000_000
MAX_RENDERED_HTML_BYTES = 4_000_000
MAX_PRE_RENDER_AST_BYTES = 8_000_000
MAX_DIAGNOSTICS_PER_DOCUMENT = 1_000
MAX_BATCH_FIELDS = 10_000
MAX_BATCH_PROJECTED_TEXT_BYTES = 4_000_000
MAX_BATCH_RENDERED_HTML_BYTES = 8_000_000
MAX_BATCH_DIAGNOSTICS = 2_000
SUPPORTED_DIRECT_ATTRIBUTE_ENTITIES = %w[Tab NewLine amp lt gt quot apos].freeze
DIRECT_NAMED_ENTITY = /&([A-Za-z][A-Za-z0-9]+);/
REPOSITORY_ROOT = File.expand_path("..", __dir__)
payload = JSON.parse($stdin.read)
production_config = payload.fetch("production_config")
unless production_config.is_a?(String) && production_config.bytesize <= 100_000
  raise "production publication configuration is malformed"
end
raw_config = SafeYAML.load(production_config)
unless raw_config.is_a?(Hash)
  raise "production publication configuration root must be a mapping"
end
JEKYLL_CONFIG = Jekyll.configuration(raw_config.merge(
  "skip_config_files" => true,
  "source" => File.join(REPOSITORY_ROOT, "docs"),
  "destination" => File.join(REPOSITORY_ROOT, ".work", "publication-projection-site"),
  "quiet" => true,
  "safe" => true,
)).validate.freeze
MARKDOWN_CONVERTER = Jekyll::Converters::Markdown.new(JEKYLL_CONFIG)
MARKDOWN_CONVERTER.setup
KRAMDOWN_OPTIONS = JEKYLL_CONFIG.fetch("kramdown").freeze

class PublicationProjector
  def initialize(document_id, source)
    @document_id = document_id
    @source = source
    @fields = []
    @field_keys = {}
    @unsupported = []
    @document = nil
    @front_matter = {}
    @line_offset = 0
    @projected_text_bytes = 0
  end

  def project
    body = extract_front_matter(@source)
    if @source.include?("{{") || @source.include?("{%")
      reject("liquid", 1, "Liquid source is outside the frozen projection contract")
      return rejected_projection
    end
    # Use the exact Jekyll-normalized Kramdown options from the tracked
    # production configuration generator.
    # Constructing the matching JekyllDocument exposes the same AST that the
    # production Markdown converter turns into HTML without loading a Site or
    # executing configured plugins.
    @document = Kramdown::JekyllDocument.new(body, KRAMDOWN_OPTIONS)
    interpreted_source = false
    cdata_token = "<![CDATA["
    if body.scan(cdata_token).length > ast_literal_token_count(@document.root, cdata_token)
      reject(
        "cdata",
        body_token_line(body, cdata_token),
        "interpreted CDATA source is outside the frozen projection contract",
      )
      interpreted_source = true
    end
    if body.scan("{::").length > ast_literal_token_count(@document.root, "{::")
      reject(
        "kramdown-extension",
        first_body_line,
        "interpreted Kramdown extension source is outside the frozen projection contract",
      )
      interpreted_source = true
    end
    return rejected_projection if interpreted_source

    if pre_render_ast_bytes(@document.root) > MAX_PRE_RENDER_AST_BYTES
      raise "publication pre-render AST expansion budget exceeded"
    end
    ast_html = @document.to_html
    production_html = MARKDOWN_CONVERTER.convert(body)
    unless ast_html == production_html
      raise "Jekyll converter and projection AST HTML diverged"
    end
    if production_html.bytesize > MAX_RENDERED_HTML_BYTES
      raise "publication rendered HTML budget exceeded"
    end
    @document.warnings.each do |warning|
      reject("renderer-warning", first_body_line, warning)
    end
    emit_front_matter
    inspect_tree(@document.root)
    emit_blocks(@document.root.children)

    {
      "document_id" => @document_id,
      "fields" => @fields.each_with_index.map { |field, index| field.merge("ordinal" => index) },
      "unsupported" => @unsupported.uniq,
      "rendered_html" => production_html,
    }
  rescue StandardError => error
    @unsupported = [{
      "kind" => "renderer-error",
      "line" => first_body_line,
      "reason" => "#{error.class}: #{error.message}",
    }]
    {
      "document_id" => @document_id,
      "fields" => [],
      "unsupported" => @unsupported.uniq,
      "rendered_html" => "",
    }
  end

  private

  def rejected_projection
    {
      "document_id" => @document_id,
      "fields" => [],
      "unsupported" => @unsupported.uniq,
      "rendered_html" => "",
    }
  end

  def body_token_line(body, token)
    index = body.index(token)
    index ? @line_offset + body[0...index].count("\n") + 1 : first_body_line
  end

  def ast_literal_token_count(node, token, seen = {})
    return 0 if seen[node.object_id]

    seen[node.object_id] = true
    # Only literal reader text/code can prove that a source opener survived
    # Kramdown interpretation. Attributes are deliberately excluded: reference
    # titles/alt values are expanded into every use site and therefore do not
    # retain one-to-one source identity.
    count = if %i[text codespan codeblock].include?(node.type) && node.value.is_a?(String)
      node.value.scan(token).length
    else
      0
    end
    count += node.children.sum { |child| ast_literal_token_count(child, token, seen) }
    if node.type == :footnote && node.value.respond_to?(:type)
      count += ast_literal_token_count(node.value, token, seen)
    end
    count
  end

  def pre_render_ast_bytes(root)
    total = 0
    stack = [root]
    abbreviation_definitions = root.options.fetch(:abbrev_defs, {})
    abbreviation_attributes = root.options.fetch(:abbrev_attr, {})
    until stack.empty?
      node = stack.pop
      # Include fixed structural overhead so a very large tree of tiny nodes is
      # bounded as well as reference-expanded values and attributes.
      total += 64
      total += node.value.bytesize if node.value.is_a?(String)
      node.attr.each do |key, value|
        total += key.to_s.bytesize + value.to_s.bytesize
      end
      if node.type == :abbreviation
        total += abbreviation_definitions[node.value].to_s.bytesize
        abbreviation_attributes.fetch(node.value, {}).each do |key, value|
          total += key.to_s.bytesize + value.to_s.bytesize
        end
      end
      return total if total > MAX_PRE_RENDER_AST_BYTES

      stack.concat(node.children)
      if node.type == :footnote && node.value.respond_to?(:type)
        # Do not identity-deduplicate here: repeated references can expand a
        # shared definition during rendering, so the conservative cost belongs
        # to every use site.
        stack << node.value
      end
    end
    total
  end

  def extract_front_matter(source)
    match = Jekyll::Document::YAML_FRONT_MATTER_REGEXP.match(source)
    return source unless match

    loaded = SafeYAML.load(match[1], safe: true)
    raise Jekyll::Errors::InvalidYAMLFrontMatterError, "front matter must be a mapping" unless loaded.is_a?(Hash)

    @front_matter = loaded
    @line_offset = match[0].count("\n")
    match.post_match
  rescue Psych::SyntaxError => error
    reject("front-matter", 1, "invalid YAML front matter: #{error.message.lines.first.to_s.strip}")
    ""
  end

  def emit_front_matter
    @front_matter.each do |key, value|
      if %w[title description].include?(key.to_s) &&
          !(value.nil? || value.is_a?(String) || value.is_a?(Numeric) || value == true || value == false)
        reject(
          "front-matter-visible-value",
          front_matter_key_line(key.to_s),
          "reader-visible front matter must be a scalar or null",
        )
        next
      end
      next unless value.is_a?(String) || value.is_a?(Numeric) || value == true || value == false

      type = %w[title description].include?(key.to_s) ? "reader_visible_attribute" : "hidden_metadata"
      add_field(
        type: type,
        text: value.to_s,
        line: front_matter_key_line(key.to_s),
        element_kind: "front_matter",
        attribute: key.to_s,
      )
    end
  end

  def front_matter_key_line(key)
    pattern = /^#{Regexp.escape(key)}\s*:/
    index = @source.lines.take(@line_offset).find_index { |line| pattern.match?(line) }
    index ? index + 1 : 1
  end

  def first_body_line
    @line_offset + 1
  end

  def source_line(node, fallback = 1)
    (node.options[:location] || fallback) + @line_offset
  end

  def reject(kind, line, reason)
    if @unsupported.length >= MAX_DIAGNOSTICS_PER_DOCUMENT
      raise "publication projection diagnostic budget exceeded"
    end
    @unsupported << {
      "kind" => kind,
      "line" => line || 1,
      "reason" => reason,
    }
  end

  def inert_checkbox?(node)
    node.type == :html_element && node.value == "input" &&
      node.options[:is_closed] == true &&
      node.attr["type"] == "checkbox" &&
      node.attr["class"] == "task-list-item-checkbox" &&
      node.attr["disabled"] == "disabled" &&
      (node.attr.keys - %w[type class disabled checked]).empty?
  end

  def safe_raw_break?(node)
    node.type == :html_element && node.value.casecmp("br").zero? && node.attr.empty?
  end

  def inspect_tree(node)
    if node.options[:ial]
      reject(
        "kramdown-ial",
        source_line(node),
        "Kramdown inline attribute lists are outside the frozen projection contract",
      )
    end

    case node.type
    when :html_element
      unless inert_checkbox?(node) || safe_raw_break?(node)
        reject("raw-html", source_line(node), "raw HTML is outside the frozen projection contract")
      end
    when :xml_comment
      reject(
        "raw-html-comment",
        source_line(node),
        "raw HTML comments are outside the frozen projection contract",
      )
    when :math
      reject("kramdown-math", source_line(node), "Kramdown math is outside the frozen projection contract")
    end

    node.children.each { |child| inspect_tree(child) }
    inspect_tree(node.value) if node.type == :footnote && node.value.respond_to?(:type)
  end

  def entity_character(value)
    entity = value.respond_to?(:char) ? value : Kramdown::Utils::Entities.entity(value.to_s)
    entity ? entity.char : value.to_s
  end

  def inline_text(node)
    case node.type
    when :text, :codespan, :codeblock
      node.value.to_s.gsub(/[\t\r\n\f\v]+/, " ")
    when :entity, :typographic_sym, :smart_quote
      entity_character(node.value)
    when :br
      # DOM textContent contributes no character for <br>. Keeping the fragments
      # contiguous also prevents a hard break from splitting one safety token.
      ""
    when :html_element
      inert_checkbox?(node) || safe_raw_break?(node) ? "" : ""
    when :a
      [inline_children(node), visible_attribute_text(node.attr["title"])].compact.join(" ")
    when :em, :strong, :del, :p, :header, :td, :dt, :dd
      inline_children(node)
    when :tr, :li, :ul, :ol, :blockquote, :dl, :thead, :tbody, :root
      block_children_text(node)
    when :abbreviation
      definition = @document.root.options.fetch(:abbrev_defs, {})[node.value]
      [node.value.to_s, visible_attribute_text(definition)].compact.join(" ")
    when :img
      [
        visible_attribute_text(node.attr["alt"]),
        visible_attribute_text(node.attr["title"]),
      ].compact.join(" ")
    when :footnote
      node.value.respond_to?(:type) ? " #{inline_text(node.value)}" : ""
    when :blank, :hr
      " "
    else
      node.children.map { |child| inline_text(child) }.join
    end
  end

  def inline_children(node)
    value = +""
    hard_break = false
    node.children.each do |child|
      if child.type == :br || safe_raw_break?(child)
        value.rstrip!
        hard_break = true
        next
      end
      child_text = inline_text(child)
      child_text = child_text.lstrip if hard_break
      value << child_text
      hard_break = false
    end
    value
  end

  def block_children_text(node)
    node.children
      .map { |child| inline_text(child).strip }
      .reject(&:empty?)
      .join(" ")
  end

  def visible_attribute_text(value)
    return nil if value.nil?

    browser_attribute_value(value).gsub(/[\t\r\n\f\v ]+/, " ").strip
  end

  def browser_attribute_value(value)
    direct_whitespace = value.to_s
      .gsub("&Tab;", "\t")
      .gsub("&NewLine;", "\n")
    CGI.unescapeHTML(direct_whitespace)
  end

  def reject_unsupported_attribute_entities(value, line)
    value.to_s.scan(DIRECT_NAMED_ENTITY).flatten.each do |name|
      next if SUPPORTED_DIRECT_ATTRIBUTE_ENTITIES.include?(name)

      reject(
        "html5-named-attribute-entity",
        line,
        "HTML5 named attribute entity &#{name}; is outside the frozen projection contract",
      )
    end
  end

  def add_field(type:, text:, line:, element_kind:, attribute: nil, metadata: {})
    value = if type == "destination"
      text.to_s
    else
      text.to_s.gsub(/[\t\r\n\f\v ]+/, " ").strip
    end
    return if value.empty?

    field = {
      "type" => type,
      "text" => value,
      "line" => line || 1,
      "element_kind" => element_kind,
      "attribute" => attribute,
      "metadata" => metadata,
    }
    key = [field["type"], field["text"], field["line"], field["element_kind"], field["attribute"], field["metadata"]]
    return if @field_keys.key?(key)

    @projected_text_bytes += value.bytesize
    if @fields.length >= MAX_FIELDS_PER_DOCUMENT ||
        @projected_text_bytes > MAX_PROJECTED_TEXT_BYTES
      raise "publication projection field budget exceeded"
    end

    @field_keys[key] = true
    @fields << field
  end

  def emit_attributes(node, fallback_line)
    line = source_line(node, fallback_line - @line_offset)
    node.attr.each_value { |value| reject_unsupported_attribute_entities(value, line) }
    case node.type
    when :a
      add_field(type: "destination", text: browser_attribute_value(node.attr["href"]), line: line, element_kind: "link", attribute: "href") if node.attr["href"]
      if node.attr["title"]
        add_field(
          type: "reader_visible_attribute",
          text: visible_attribute_text(node.attr["title"]),
          line: line,
          element_kind: "link",
          attribute: "title",
          metadata: {"scan_owner" => "inline_parent"},
        )
      end
    when :img
      add_field(type: "destination", text: browser_attribute_value(node.attr["src"]), line: line, element_kind: "image", attribute: "src") if node.attr["src"]
      add_field(
        type: "reader_visible_attribute",
        text: visible_attribute_text(node.attr["alt"]),
        line: line,
        element_kind: "image",
        attribute: "alt",
        metadata: {"scan_owner" => "inline_parent"},
      ) if node.attr["alt"]
      if node.attr["title"]
        add_field(
          type: "reader_visible_attribute",
          text: visible_attribute_text(node.attr["title"]),
          line: line,
          element_kind: "image",
          attribute: "title",
          metadata: {"scan_owner" => "inline_parent"},
        )
      end
    when :abbreviation
      title = @document.root.options.fetch(:abbrev_defs, {})[node.value]
      reject_unsupported_attribute_entities(title, line) if title
      if title
        add_field(
          type: "reader_visible_attribute",
          text: visible_attribute_text(title),
          line: line,
          element_kind: "abbreviation",
          attribute: "title",
          metadata: {"scan_owner" => "inline_parent"},
        )
      end
    when :header
      add_field(type: "hidden_metadata", text: node.attr["id"], line: line, element_kind: "heading", attribute: "id") if node.attr["id"]
    when :html_element
      if inert_checkbox?(node)
        add_field(
          type: "reader_visible_attribute",
          text: node.attr.key?("checked") ? "checked" : "unchecked",
          line: line,
          element_kind: "task_checkbox",
          attribute: "state",
        )
      end
    end

    node.children.each { |child| emit_attributes(child, line) }
    emit_attributes(node.value, line) if node.type == :footnote && node.value.respond_to?(:type)
  end

  def emit_unit(node, heading_context = nil)
    line = source_line(node)
    value = inline_text(node)
    value = "#{heading_context} #{value}" if heading_context && !heading_context.empty?
    add_field(type: "reader_visible_text", text: value, line: line, element_kind: node.type.to_s)
    emit_attributes(node, line)
  end

  def direct_list_item_blocks(item)
    item.children.reject { |child| %i[ul ol blank].include?(child.type) }
  end

  def nested_lists(item)
    item.children.select { |child| %i[ul ol].include?(child.type) }
  end

  def emit_list_item_paths(item, inherited_context = nil, heading_context = nil)
    own_blocks = direct_list_item_blocks(item)
    own_text = own_blocks.map { |block| inline_text(block) }.join(" ")
    context = [heading_context, inherited_context, own_text]
      .compact
      .reject(&:empty?)
      .join(" ")

    emitted = false
    nested_lists(item).each do |list|
      list.children.select { |child| child.type == :li }.each do |child_item|
        emit_list_item_paths(child_item, context, nil)
        emitted = true
      end
    end

    unless emitted
      add_field(
        type: "reader_visible_text",
        text: context,
        line: source_line(item),
        element_kind: "list_path",
      )
    end
    emit_attributes(item, source_line(item))
  end

  def emit_table_rows(node, heading_context)
    head = node.children.find { |child| child.type == :thead }
    body = node.children.find { |child| child.type == :tbody }
    header_text = head ? inline_text(head) : ""
    rows = body ? body.children.select { |child| child.type == :tr } : []

    if rows.empty?
      emit_unit(node, heading_context)
      return
    end

    emit_attributes(head, source_line(node)) if head

    rows.each do |row|
      text = [heading_context, header_text, inline_text(row)].compact.join(" ")
      add_field(
        type: "reader_visible_text",
        text: text,
        line: source_line(node),
        element_kind: "table_row",
      )
      emit_attributes(row, source_line(node))
    end
  end

  def emit_definition_pairs(node, heading_context)
    term = nil
    emitted_for_term = false
    node.children.each do |child|
      case child.type
      when :dt
        if term && !emitted_for_term
          reject(
            "definition-list",
            source_line(child),
            "definition term without a definition is outside the frozen projection contract",
          )
        end
        term = inline_text(child).strip
        emitted_for_term = false
        emit_attributes(child, source_line(child))
      when :dd
        unless term
          reject(
            "definition-list",
            source_line(child),
            "definition without a term is outside the frozen projection contract",
          )
          next
        end
        text = [heading_context, term, inline_text(child)].compact.join(" ")
        add_field(
          type: "reader_visible_text",
          text: text,
          line: source_line(child),
          element_kind: "definition_pair",
        )
        emit_attributes(child, source_line(child))
        emitted_for_term = true
      else
        reject(
          "definition-list",
          source_line(child),
          "unsupported definition-list child #{child.type}",
        )
      end
    end
    if term && !emitted_for_term
      reject(
        "definition-list",
        source_line(node),
        "definition term without a definition is outside the frozen projection contract",
      )
    end
  end

  def emit_heading(node, text, associated:)
    metadata = {"level" => node.options[:level]}
    metadata["scan_owner"] = "following_body" if associated
    add_field(
      type: "reader_visible_text",
      text: text,
      line: source_line(node),
      element_kind: "heading",
      metadata: metadata,
    )
    emit_attributes(node, source_line(node))
  end

  def emit_blocks(nodes)
    pending_heading = nil
    nodes.each do |node|
      next if %i[blank hr].include?(node.type)

      unless SUPPORTED_BLOCKS.include?(node.type)
        reject("unsupported-block", source_line(node), "unsupported renderer block type #{node.type}")
      end

      if node.type == :header
        if pending_heading
          emit_heading(
            pending_heading.fetch(:node),
            pending_heading.fetch(:text),
            associated: false,
          )
        end
        pending_heading = {node: node, text: inline_text(node).strip}
        next
      end

      heading_context = pending_heading&.fetch(:text)
      if pending_heading
        emit_heading(
          pending_heading.fetch(:node),
          heading_context,
          associated: true,
        )
      end

      case node.type
      when :ul, :ol
        items = node.children.select { |child| child.type == :li }
        items.each do |item|
          emit_list_item_paths(item, nil, heading_context)
        end
      when :table
        emit_table_rows(node, heading_context)
      when :dl
        emit_definition_pairs(node, heading_context)
      else
        emit_unit(node, heading_context)
      end
      pending_heading = nil
    end
    if pending_heading
      emit_heading(
        pending_heading.fetch(:node),
        pending_heading.fetch(:text),
        associated: false,
      )
    end
  end
end

documents = payload.fetch("documents")
projected_documents = []
batch_fields = 0
batch_projected_text_bytes = 0
batch_rendered_html_bytes = 0
batch_diagnostics = 0
documents.each do |item|
  projected = PublicationProjector.new(item.fetch("document_id"), item.fetch("source")).project
  batch_fields += projected.fetch("fields").length
  batch_projected_text_bytes += projected.fetch("fields").sum { |field| field.fetch("text").bytesize }
  batch_rendered_html_bytes += projected.fetch("rendered_html").bytesize
  batch_diagnostics += projected.fetch("unsupported").length
  projected_documents << projected
  next if batch_fields <= MAX_BATCH_FIELDS &&
    batch_projected_text_bytes <= MAX_BATCH_PROJECTED_TEXT_BYTES &&
    batch_rendered_html_bytes <= MAX_BATCH_RENDERED_HTML_BYTES &&
    batch_diagnostics <= MAX_BATCH_DIAGNOSTICS

  projected_documents = documents.map do |document|
    {
      "document_id" => document.fetch("document_id"),
      "fields" => [],
      "unsupported" => [{
        "kind" => "batch-budget",
        "line" => 1,
        "reason" => "publication projection batch budget exceeded",
      }],
      "rendered_html" => "",
    }
  end
  break
end
result = {
  "protocol_version" => PROTOCOL_VERSION,
  "projection_version" => PROJECTION_VERSION,
  "runtime" => {
    "ruby" => RUBY_VERSION,
    "jekyll" => Jekyll::VERSION,
    "kramdown" => Kramdown::VERSION,
    "kramdown_parser" => Kramdown::Parser::GFM.name,
    "kramdown_parser_gfm" => Gem.loaded_specs.fetch("kramdown-parser-gfm").version.to_s,
    "kramdown_hard_wrap" => KRAMDOWN_OPTIONS.fetch("hard_wrap").to_s,
    "liquid" => Liquid::VERSION,
    "production_base_scheme" => URI.parse(JEKYLL_CONFIG.fetch("url")).scheme,
    "syntax_highlighter" => KRAMDOWN_OPTIONS.fetch("syntax_highlighter"),
  },
  "documents" => projected_documents,
}
$stdout.write(JSON.generate(result))
$stdout.write("\n")

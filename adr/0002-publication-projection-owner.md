# ADR 0002: Publication Projectionの単一所有者

- Status: Accepted
- Date: 2026-08-25
- Decision owners: Issue #101 / PR #100
- Related: #17, #65, #67, #101

## Context

公開前Content Safety検査には、Markdown sourceではなく、固定された出版stackが読者へ提示するtext、title / accessibility attribute、link / image destinationを渡す必要がある。PR #100の初期実装は、この境界を第2章checker内のregexと手続きで再現した。その結果、第2章checkerへMarkdown/Kramdown/HTMLのblock、inline、list、table、code、link、raw HTML precedenceが集まり、review counterexampleごとの分岐が約3,000行へ拡大した。

責務は次の三層へ分ける。

1. Layer A: chapter固有のdocument/surface選択、finite section inventory、意味、Authority / Source / Artifact / Traceability。
2. Layer B: chapterに依存しないPublication Projection。
3. Layer C: shared Content Safety Policy。本PRでは`1.2.0`のまま変更しない。

## Decision

Layer Bの唯一のpublic ownerを`scripts/publication_projection.py`、versionを`1.0.0`とする。

同moduleは、private backend`scripts/_publication_projection_renderer.rb`を一括起動する。backendは既存`Gemfile.lock`のJekyll `4.4.1`、Kramdown `2.5.2`、`kramdown-parser-gfm` `1.1.0`、Liquid `4.0.4`を`input: GFM`で使用する。Python ownerはprotocol/runtime/schemaを検証し、typed field、Layer C向け`normalized_text`、destinationの有限normalization、diagnostic、location、order、deduplicationを確定する。

private backendを含む一つのcomponentがLayer Bである。両fileにchapter番号、canonical path、Artifact/Case ID、Content Safety Policy grammarを置かない。

## Contract

### Input

順序付きの`document_id`とUTF-8 Markdown source。1 batchは256文書、1文書2,000,000 bytes、合計8,000,000 bytesまでに制限する。

### Output field types

- `reader_visible_text`: renderer structureに基づくbounded reader-visible field。
- `reader_visible_attribute`: front matter title/description、link/image title、image alt、abbreviation title、task checkbox state等。
- `destination`: rendererが確定したlink/image destination。`normalized_text`へ有限browser-special normalizationを持つ。
- `hidden_metadata`: generated heading ID等。Policyへ自動委譲しない。

`text`はtyped publication valueを保持する。visible fieldの`normalized_text`はLayer Cへの一方向handoffであり、renderer出力をsource Markdown / HTMLとして再解釈させない。Layer Cがsource記法として除去するliteral `[]()*~`、backtick、backslashは、obfuscation-resistantなtoken連結を維持して除去する。ampersandとangle bracketはLayer Cの一回decode後にもliteralであるよう二重保護し、underscore等の通常文字は保持する。destinationの`normalized_text`は後述の有限URL normalization結果とする。

各fieldは`document_id:L<source-line>:F<ordinal>`を同一入力に対する決定的なdiagnostic locationとする。table cellの個別lineがrenderer ASTにない場合は、owning tableのlineを使用する。これは編集をまたぐsemantic keyではない。Layer Aはdocument path、field type、element kind、attribute、exact text、exactly-once cardinality、projected orderとbounded heading membershipを組み合わせる。reviewed provenance destinationは、同じsource lineで直前に投影されたexact reader-visible ownerとのrelationも必須とし、別contextへURLだけを移動してexemptionを継承できない。

### Structural association

finite supported corpusでは次を一つのbounded fieldとして関連付ける。

- headingと直後のbody unit。
- top-level list itemとそのnested list / continuation。
- blockquote内のparagraph。
- table headerと各body row。
- definition termと各definition。複数pairをdefinition list全体へflattenせず、同じtermに複数definitionがある場合も各pairを独立ownerとする。
- footnote referenceとdefinition。
- rendererが一つと判定したfenced / indented / inline code。
- image alt replacement text、link / image title、abbreviation titleとinline parent。attributeはtyped accessibility fieldとしても保持するが、`scan_owner=inline_parent`によりLayer Cで二重scanしない。
- GFM task itemのgenerated disabled checkbox。`checked` / `unchecked`を`task_checkbox.state` accessibility fieldとして保持する。

fieldの重複keyはordinal付与前に除外し、renderer orderを保持する。

### Attribute/entity boundary

attribute contextではKramdownが返したvalueに対し、direct `&Tab;` / `&NewLine;`とCGIのnumeric/basic named entityを一回decodeする。direct named referenceとして許容するのは`Tab`、`NewLine`、`amp`、`lt`、`gt`、`quot`、`apos`だけであり、それ以外は`PP1001`とする。通常textに同じattribute decoderを適用しない。image altをinline parentへ含める場合も、この一回decode後のvalueを使用する。

### Destination boundary

URLはleading/trailing C0/spaceを除去し、ASCII tab/LF/CRをscheme判定前に除去する。有限WHATWG network-special scheme（FTP、HTTP(S)、WS(S)）とscheme-relative destinationはbackslash、mixed-slash authority、authority-less formだけをnormalizeし、hostname/portを検証する。ただしproduction baseと同じHTTPS schemeのauthority-less formはbrowser上でbase依存のsame-origin pathとなるため、外部authorityを合成せず`PP1002`でfail closedとする。`javascript`、`vbscript`、`file`を拒否する。

relative path/fragmentはsite build/link checkerの責務とし、明示schemeを持つすべてのabsolute destination（HTTP(S)以外のFTP、WebSocket、mailto等を含む）はLayer C host policyへ渡す。

### Fail-closed behavior

次は共通code`PP1001`（unsupported source）で出版前にfail closedとする。

- Liquid construct。JekyllはMarkdown code内もMarkdown変換前にLiquid処理するため、source全体で検出し、実行しない。
- raw HTML/comment（parser-generated inert task checkboxとattribute-free `br`を除く）。
- Kramdown IAL / interpreted extension / math。
- interpreted CDATA。exact AST内のtext / fenced / indented / inline code nodeにliteralとして残るopenerだけをsource occurrenceとして対応付け、ASTからopenerが消える解釈結果をfail closedとする。reference title / alt等の展開属性は一つのsource definitionから複製されるためliteral occurrenceの証明に使用しない。同じsource-identity規則をinterpreted Kramdown extensionにも適用する。
- renderer warning / exception / unknown block type。
- front matterのreader-visible title/descriptionがscalarでない場合。
- finite HTML attribute entity contract外のnamed reference。
- documentまたはbatchのfield / projected text / rendered HTML / diagnostic budget超過。

Liquidと、ASTでinterpreter consumptionが確定したCDATA / Kramdown extensionは、exact HTML変換を開始せず、field / HTMLのpartial publication surfaceを返さない。これによりinterpreted optionがfootnote等のuse-siteへ展開される前にstable diagnosticで停止する。

executable destinationまたはparse不能なspecial network destinationは`PP1002`でfail closedとする。

本contractはcomplete CommonMark、Kramdown extension、Liquid、HTML、browser accessibility tree、HTML named entity table、WHATWG URL parserを実装または主張しない。新syntaxはshared corpusとADRでcontractを明示的に拡張するまでunsupportedである。

## Exact production parity

- YAML front matterはJekyll `4.4.1`の`YAML_FRONT_MATTER_REGEXP`と`SafeYAML`で分離する。
- Liquidは安全上実行せずfail closedとする。
- tracked production generator `scripts/sync_site_source.py`の`render_config(book-config.json)`をPython ownerからprivate backendへ渡し、Jekyllのdefault merge/validationを適用する。これによりclean checkoutでも未追跡のgenerated `docs/_config.yml`へ依存せず、同じproduction configurationを使用する。`Jekyll::Converters::Markdown`のproduction HTMLと、field抽出に使用した`Kramdown::JekyllDocument` ASTのHTMLがbyte-for-byte一致しなければfail closedとする。`hard_wrap: false`と`syntax_highlighter: rouge`もruntime contractである。
- Site、layout、include、plugin、Liquidをroot projectionで実行しない。最終siteのrewrite、link、anchor、layoutはBook QAのexact formatter / Jekyll build gateで別途検証する。
- generic fixtureはtyped fieldsと`rendered_html`を固定し、exact renderer/version handshakeも検証する。
- handshakeはRuby 3.3 series、Jekyll `4.4.1`、Kramdown `2.5.2`、`Kramdown::Parser::GFM`、GFM parser `1.1.0`、Liquid `4.0.4`、production base scheme `https`、`hard_wrap: false`、Rougeを検証する。
- runtime/dependency未準備、version mismatch、invalid JSON/schema、45秒timeoutは`ProjectionRuntimeError`でfail closedとする。

## Security, determinism, and performance

- Jekyll Site、plugin、include、network、任意file readを実行しない。
- 新規dependencyを追加しない。既存lockだけを使用する。
- environmentはrepository `Gemfile`、`BUNDLE_FROZEN=true`、`JEKYLL_ENV=production`、UTF-8 localeに固定し、呼出元の`RUBYOPT`、`RUBYLIB`、`BUNDLE_PATH`、`BUNDLE_BIN_PATH`を継承しない。
- hash-based iterationへ依存せず、入力順、renderer順、full key deduplication、sorted diagnosticsを用いる。
- input budgetに加えて、exact HTML生成前のAST expansion costを1文書8,000,000 bytes、生成後は1文書あたりfield 5,000、projected text 2,000,000 bytes、rendered HTML 4,000,000 bytes、diagnostic 1,000、batchではそれぞれ10,000、4,000,000 bytes、8,000,000 bytes、2,000に制限する。reference titleやfootnote等のuse-site展開はpre-render costへ各回計上し、巨大HTMLを構築する前にfail closedとする。document超過は`renderer-error`、batch超過は全documentをpartial outputなしの`batch-budget`へ置換し、いずれも`PP1001`とする。
- Linux/Unixのprivate renderer childにはaddress space 384 MiB、CPU 30秒のOS limitも適用し、Python側45秒timeoutと合わせてparser/renderer内部の未知の資源増幅を境界化する。親processがそれより厳しいsoft/hard limitを持つ場合は既存limitを緩和せず小さい値を継承し、pre-exec failureも`ProjectionRuntimeError`へ変換する。
- generic contractは183 fixtureを一batchで検査し、全70 historical threadの一意ownership、stable order/deduplication、safe/unsafe/unsupported result、seed `0/1/7/42`の決定性、document/batch resource limitを固定する。
- architecture spikeではcanonical第2章3文書を警告0で約1.07秒、最大RSS約60 MiBでbatch投影した。

## Alternatives

### Rejected: Chapter 2-specific renderer emulation

責務境界に違反し、review variantごとにregex/precedence branchを追加する。62個のgeneric top-level itemを持ち、Chapter 4/25と重複するため削除する。

### Rejected: finite shared parser seeded from the current emulation

fallback spikeで62件のLayer B counterexampleを比較した結果、locked rendererのvisible fieldと一致したのは7件、55件が不一致だった。これを共有fileへ移すだけでは二重rendererを維持し、security、renderer parity、保守性を改善しない。

### Rejected: full Jekyll site render per contract document

layout/plugin/includeまで実行すると、root contractに不要なfile/plugin surface、I/O、performance、source-location喪失が増える。locked parser/HTML parityとfail-closed Liquidで必要な出版境界を満たす。

## Consequences

- Book Contract / Book QAは`npm test`より前にlocked Ruby environmentを準備する。
- 第2章checkerはcanonical documentとH1/H2 inventoryを選択し、Layer B fieldsをPolicy `1.2.0`へ渡す。Layer Aのsemantic/exemption identityはabsolute lineへ固定せず、exact projected owner、order、bounded section、heading path、cardinality、およびprovenance relationで移動・重複をfail closedとする。Gate bodyとSource IDのbody/reference occurrenceもreader-visible projectionだけで有限に検証し、hidden metadataやcode literalでは代替できない。
- 第4章/第25章のlegacy parsingは本PRで全面移行しない。Layer B generic corpusと代表章contractを非回帰gateとし、完全移行はfocused follow-upで扱う。
- Issue #67のshared host-token defectはLayer Cであり、本ADR/PRでは修正しない。

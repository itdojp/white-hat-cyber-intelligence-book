"""Local, offline publication assets; no chapter or Markdown parsing."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERMAID_VERSION = "12.0.0"
MERMAID_SHA256 = "9f2807e402479d2864bfd9a95052076fc69d0ff45a0b25148b84b70fc33425b9"
MERMAID_ASSET = f"assets/js/mermaid-{MERMAID_VERSION}.tiny.js"
LOCAL_ASSETS = {
    "publication/mermaid/loader.js": "assets/js/mermaid-loader.js",
    "publication/mermaid/diagrams.css": "assets/css/mermaid-diagrams.css",
}


def load_publication_assets(root: Path = ROOT) -> dict[str, bytes]:
    """Validate everything before the generator can replace its output."""
    package = root / "node_modules/@mermaid-js/tiny"
    metadata = json.loads((package / "package.json").read_text(encoding="utf-8"))
    if metadata.get("name") != "@mermaid-js/tiny" or metadata.get("version") != MERMAID_VERSION:
        raise ValueError("Mermaid package differs from audited version; run npm ci --ignore-scripts")
    data = (package / "dist/mermaid.tiny.js").read_bytes()
    if hashlib.sha256(data).hexdigest() != MERMAID_SHA256:
        raise ValueError("Mermaid distribution SHA-256 mismatch")
    assets = {MERMAID_ASSET: data}
    for source, target in LOCAL_ASSETS.items():
        assets[target] = (root / source).read_bytes()
        if not assets[target]:
            raise ValueError(f"Empty publication asset: {source}")
    return assets


def layout_assets() -> tuple[str, str]:
    css = '    <link rel="stylesheet" href="{{ "/assets/css/mermaid-diagrams.css" | relative_url }}">\n'
    script = (
        '    <script defer src="{{ "/assets/js/mermaid-loader.js" | relative_url }}" '
        f'data-mermaid-src="{{{{ "/{MERMAID_ASSET}" | relative_url }}}}"></script>\n'
    )
    return css, script

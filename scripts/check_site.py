#!/usr/bin/env python3
"""Validate all generated local destinations, fragments, and content coverage."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.titles = set(), [], 0
        self.in_head = False
        self.in_title = False
        self.title_text = ""
        self.duplicate_ids = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        if tag == "title" and self.in_head:
            self.titles += 1
            self.in_title = True
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicate_ids.append(attrs["id"])
            self.ids.add(attrs["id"])
        for attr in ["href", "src"]:
            if attrs.get(attr):
                self.refs.append(attrs[attr])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.in_head = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", default="")
    parser.add_argument("--directory", default="dist")
    args = parser.parse_args()
    root = Path(args.directory).resolve()
    base = "/" + args.base_path.strip("/") if args.base_path.strip("/") else ""
    parsed = {}
    title_owners = {}
    errors = []
    for path in root.rglob("*.html"):
        text = path.read_text()
        rel = path.relative_to(root).as_posix()
        page = Page(text)
        parsed[rel] = page
        for asset in ("app.js", "style.css"):
            digest = hashlib.sha256((root / "assets" / asset).read_bytes()).hexdigest()[:12]
            if f"{base}/assets/{asset}?v={digest}" not in page.refs:
                errors.append(f"{rel}: missing current content version for {asset}")
        if page.title_text in title_owners:
            errors.append(f"{rel}: duplicate document title also used by {title_owners[page.title_text]}")
        title_owners[page.title_text] = rel
        if page.titles != 1 or "<html lang=\"en\">" not in text:
            errors.append(f"{rel}: missing page title or language")
        if page.duplicate_ids:
            errors.append(f"{rel}: duplicate IDs {page.duplicate_ids}")
        if "{{" in text or re.search(r"\$(?:base|content|navigation)\b", text):
            errors.append(f"{rel}: unexpanded template")
    checked = 0
    for rel, page in parsed.items():
        origin = "https://local.invalid" + base + "/" + rel
        for ref in page.refs:
            if urlsplit(ref).scheme or ref.startswith("//"):
                continue
            url = urlsplit(urljoin(origin, ref))
            url_path = unquote(url.path)
            if base and not (url_path == base or url_path.startswith(base + "/")):
                errors.append(f"{rel}: link escapes GitHub Pages project path: {ref}")
                continue
            target_rel = url_path[len(base):].lstrip("/")
            target = root / target_rel
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{rel}: missing local destination {ref}")
            elif url.fragment and target.suffix == ".html":
                target_page = parsed.get(target.relative_to(root).as_posix())
                if not target_page or unquote(url.fragment) not in target_page.ids:
                    errors.append(f"{rel}: missing fragment {ref}")
            checked += 1
    curriculum = json.loads(Path("curriculum.json").read_text())
    if [item["day"] for item in curriculum] != list(range(1, 22)):
        errors.append("Curriculum must cover exactly days 1 to 21")
    for item in curriculum:
        rel = f"days/{item['slug']}/index.html"
        if rel not in parsed:
            errors.append(f"Missing day {item['day']}")
        source = Path(f"content/lessons/{item['day']:02}-{item['slug']}.md").read_text()
        for section in ["## Today's practice", "## Checkpoint"]:
            if section not in source and not (item['day'] == 21 and section == "## Today's practice"):
                errors.append(f"Day {item['day']}: missing {section}")
        if "https://" not in source:
            errors.append(f"Day {item['day']}: missing primary source")
    index = json.loads((root/"search-index.json").read_text())
    if len([entry for entry in index if entry.get("day")]) != 21:
        errors.append("Search does not cover 21 days")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Verified {len(parsed)} pages, {checked} local references, 21 lessons, and search coverage")


if __name__ == "__main__":
    main()

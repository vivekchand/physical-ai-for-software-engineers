#!/usr/bin/env python3
"""Build readable, searchable static pages from the original Markdown chapters."""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
from string import Template
import markdown

ROOT = Path(__file__).resolve().parents[1]
# Legacy day/week identifiers preserve public URLs, book anchors, and saved progress.
REPO = "https://github.com/vivekchand/physical-ai-for-software-engineers"
ORIGIN = "https://vivekchand.github.io"
FIELD_NOTES = [
    ("setup", "Choose your starting setup", "A laptop path for everyone, a GPU path when you are ready."),
    ("manipulation", "Pick it up. Put it down. Prove it.", "One arm, a red cube, and a tray. A practical path from kinematics to learned manipulation."),
    ("hardware", "Your first arm, at your budget", "Dated supplier prices and package details, from portable simulation to a bimanual research station."),
    ("models", "Meet the robot models", "Dream-1, VLAs, world-action models, and the interface that connects a model to your arm."),
    ("robot-learning", "How robots learn a task", "Choose a learning method, build a dataset, and connect model outputs to a controller."),
    ("cloud-lab", "Run your first cloud Isaac lab", "Use a remote GPU from your laptop, verify one experiment, and bring the evidence home."),
    ("isaac-foundations", "Build and debug an Isaac Sim scene", "Verify the GPU, understand USD and contacts, and measure what your sensors and clocks mean."),
    ("evaluation", "Evaluate a pick-and-place robot", "Compare outcomes, interventions, and held-out conditions before claiming improvement."),
    ("applications", "Plan a useful robot application", "Turn the arm exercise into a bounded pilot with measurable work, quality, and costs."),
    ("nvidia", "The NVIDIA robotics map", "A source-linked map of what each tool is for, and what to install first."),
    ("resources", "Go deeper, deliberately", "The original references behind the guide, organized by the question you are trying to answer."),
    ("glossary", "A working vocabulary", "Plain-language definitions you can use in an engineering conversation."),
    ("roadmap", "Keep learning", "Turn a first project into deeper engineering competence."),
    ("labs", "Small experiments. Real intuition.", "Run the portable labs before adding simulation infrastructure."),
    ("privacy", "Newsletter privacy", "What happens to your email when you subscribe to Physical AI Field Notes.")
]


def resolve_links(text, base):
    # One placeholder keeps Markdown readable in GitHub and portable in a project site.
    text = text.replace("{{base}}", base)
    # Source-relative links work on GitHub; compiled links work in chapters and the book.
    for slug, _, _ in FIELD_NOTES:
        text = re.sub(r'\]\((?:\.\./pages/)?' + re.escape(slug) + r'\.md(#[^)]*)?\)',
                      lambda match, slug=slug: f']({base}/{slug}/{match[1] or ""})', text)
    return text


def render_md(text, base):
    text = resolve_links(text, base)
    engine = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "admonition", "attr_list"])
    body = engine.convert(text)
    legacy_fragments = {"practice": "todays-practice", "own-one-algorithm": "weeks-46-own-one-algorithm",
                        "own-one-integration": "weeks-79-own-one-integration", "own-one-evaluation": "weeks-1012-own-one-evaluation"}
    for current, previous in legacy_fragments.items():
        body = body.replace(f'<h2 id="{current}">', f'<span id="{previous}" aria-hidden="true"></span><h2 id="{current}">')
    return body, engine.toc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", default="")
    parser.add_argument("--output", default="dist")
    args = parser.parse_args()
    base = "/" + args.base_path.strip("/") if args.base_path.strip("/") else ""
    out = ROOT / args.output
    if out.resolve() == ROOT or ROOT not in out.resolve().parents:
        parser.error("Output must be a subdirectory of the project")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", out / "assets")
    shutil.copytree(ROOT / "examples", out / "examples", ignore=shutil.ignore_patterns("__pycache__"))
    curriculum = json.loads((ROOT / "curriculum.json").read_text())
    hardware = json.loads((ROOT / "data/hardware.json").read_text())
    def price_table(rows):
        table = ["| Option / supplier link | Listed USD | Package scope | Learning fit |",
                 "|---|---:|---|---|"]
        for row in rows:
            price = "Quote" if row["price"] is None else f'${row["price"]:,.0f}'
            table.append(f'| [{row["name"]}]({row["url"]}) | {price} | {row["package"]} | {row["fit"]} |')
        return "\n".join(table)
    def with_hardware_tables(text):
        return text.replace("{{single_arm_table}}", price_table(hardware["single_arm_options"])).replace(
            "{{bimanual_table}}", price_table(hardware["bimanual_options"]))
    shell = Template((ROOT / "templates/base.html").read_text())
    asset_versions = {name: hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:12]
                      for name in ("app.js", "style.css")}
    search = []
    urls = []

    def page(path, title, description, content, active="", toc="", day="", source=""):
        dest = out / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        nav = []
        for week, label in [(1, "01 / Understand the robot"), (2, "02 / Build the system"), (3, "03 / Learn, deploy, observe")]:
            nav.append(f'<p class="nav-group">{label}</p>')
            for item in curriculum:
                if item["week"] != week:
                    continue
                cls = ' class="active" aria-current="page"' if active == item["slug"] else ""
                nav.append(f'<a{cls} data-day-link="{item["day"]}" href="{base}/days/{item["slug"]}/"><span class="day-num">{item["day"]:02}</span><span>{html.escape(item["title"])}</span><span class="nav-check" aria-hidden="true"></span></a>')
        nav.append('<p class="nav-group">Field notes</p>')
        for slug, note_title in [("manipulation", "Pick-and-place lab"), ("hardware", "Buy your first arm"), ("models", "VLAs & Dream Labs"), ("nvidia", "NVIDIA map"),
                                 ("isaac-foundations", "Isaac Sim workshop"), ("robot-learning", "Robot learning"), ("cloud-lab", "Cloud Isaac lab"), ("evaluation", "Evaluation & sim-to-real"), ("applications", "Applications & costs")]:
            cls = ' class="active" aria-current="page"' if path == f"{slug}/index.html" else ""
            nav.append(f'<a{cls} href="{base}/{slug}/">{html.escape(note_title)}</a>')
        canonical = f"{ORIGIN}{base}/" + (path[:-10] if path.endswith("index.html") else path)
        result = shell.substitute(base=base, title=html.escape(title), description=html.escape(description, quote=True),
            canonical=canonical, content=content, navigation="".join(nav), toc=toc, day=day,
            repo=REPO, source=source, script_version=asset_versions["app.js"], style_version=asset_versions["style.css"],
            body_class="home-page" if not path.startswith("days/") else "lesson-page")
        dest.write_text(result)
        urls.append(canonical)

    newsletter = (ROOT / "templates/newsletter.html").read_text().replace("{{base}}", base)
    home = (ROOT / "templates/home.html").read_text().replace("{{base}}", base).replace("{{newsletter}}", newsletter)
    weeks = []
    for week, title, subtitle in [(1, "Understand the robot", "Build intuition before adding tools."), (2, "Build the system", "ROS 2, NVIDIA Isaac, and your first integration."), (3, "Learn, deploy, observe", "Policies, data, operational evidence, and a capstone.")]:
        rows = []
        for item in curriculum:
            if item["week"] == week:
                rows.append(f'''<a class="curriculum-row" href="{base}/days/{item['slug']}/" data-course-day="{item['day']}">
                  <span class="row-day">{item['day']:02}</span><span class="row-copy"><strong>{html.escape(item['title'])}</strong><span>{html.escape(item['summary'])}</span></span>
                  <span class="row-tag">{html.escape(item['tag'])}</span><span class="row-arrow" aria-hidden="true">↗</span></a>''')
        weeks.append(f'<section class="week" id="week-{week}"><div class="week-heading"><span class="eyebrow">PART {week:02}</span><h3>{title}</h3><p>{subtitle}</p></div><div class="week-lessons">{"".join(rows)}</div></section>')
    page("index.html", "Physical AI for Software Engineers", "A free, open-source, self-paced guide to robotics, ROS 2, NVIDIA Isaac, and physical AI. Original lessons, runnable labs, and a pick-and-place project.", home.replace("{{curriculum}}", "".join(weeks)))

    for i, item in enumerate(curriculum):
        source = f"content/lessons/{item['day']:02}-{item['slug']}.md"
        text = (ROOT / source).read_text()
        body, toc = render_md(text, base)
        words = len(re.findall(r"\b\w+\b", re.sub(r"<[^>]*>", " ", body)))
        previous = curriculum[i-1] if i else None
        following = curriculum[i+1] if i+1 < len(curriculum) else None
        prev_link = f'<a href="{base}/days/{previous["slug"]}/"><small>← PREVIOUS</small>{html.escape(previous["title"])}</a>' if previous else f'<a href="{base}/"><small>← THE GUIDE</small>All lessons</a>'
        next_link = f'<a href="{base}/days/{following["slug"]}/"><small>NEXT →</small>{html.escape(following["title"])}</a>' if following else f'<a href="{base}/roadmap/"><small>KEEP GOING →</small>Explore further</a>'
        content = f'''<div class="lesson-header"><a class="breadcrumb" href="{base}/#learning-path">The learning path</a><p class="eyebrow">LESSON {item['day']:02} / PART {item['week']:02} / {html.escape(item['tag'].upper())}</p><h1>{html.escape(item['title'])}</h1><p class="lesson-deck">{html.escape(item['summary'])}</p><div class="lesson-meta"><span>{max(2, math.ceil(words/180))} min read</span><span>Self-paced practice</span><span>Original, open material</span></div></div>
        <details class="reader-toc"><summary>In this lesson</summary>{toc}</details><div class="reader-layout"><article class="prose" id="lesson-content">{body}
        <div class="completion-box"><div><strong>Can you explain it without the page?</strong><p>Try the checkpoint first. Your progress stays in this browser.</p></div><button class="button primary" data-complete="{item['day']}" aria-pressed="false">Mark lesson complete</button></div><p class="edit-link"><a href="{REPO}/edit/main/{source}">Improve this lesson on GitHub ↗</a></p><nav class="chapter-nav" aria-label="Previous and next lesson">{prev_link}{next_link}</nav></article></div>{newsletter}'''
        page(f"days/{item['slug']}/index.html", item["title"] + " · Lesson " + str(item["day"]), item["summary"], content, item["slug"], toc, str(item["day"]), source)
        plain = html.unescape(re.sub(r"<[^>]+>", " ", body))
        search.append({"title":item["title"], "day":item["day"], "url":f"{base}/days/{item['slug']}/", "text":re.sub(r"\s+", " ", plain)})

    for slug, title, deck in FIELD_NOTES:
        source = f"content/pages/{slug}.md"
        text = with_hardware_tables((ROOT/source).read_text())
        body, toc = render_md(text, base)
        content = f'<div class="lesson-header"><p class="eyebrow">FIELD NOTES / {slug.upper()}</p><h1>{title}</h1><p class="lesson-deck">{deck}</p></div><details class="reader-toc"><summary>In this guide</summary>{toc}</details><article class="prose">{body}</article>'
        page(f"{slug}/index.html", title, deck, content, toc=toc, source=source)
        search.append({"title":title,"day":None,"url":f"{base}/{slug}/", "text":re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))})
    chapters, manuscript = [], ["# Physical AI for Software Engineers\n\nA free, open-source, self-paced guide to robotics, ROS 2, and NVIDIA Isaac. Learn by building a pick-and-place robot.\n\nText: CC BY 4.0, Vivek Chand and contributors. Code: MIT. External sources retain their own licenses.\n\nDocumentation reviewed 23 October 2026. GPU reference exercises are not independently executed by this project's CPU tests.\n"]
    contents = []
    for item in curriculum:
        raw = (ROOT/f"content/lessons/{item['day']:02}-{item['slug']}.md").read_text()
        body, _ = render_md(raw, base)
        body = re.sub(r'id="([^"]+)"', lambda m: f'id="day-{item["day"]}-{m[1]}"', body)
        body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#day-{item["day"]}-{m[1]}"', body)
        body = body.replace('<h3', '<h4').replace('</h3>', '</h4>').replace('<h2', '<h3').replace('</h2>', '</h3>')
        chapters.append(f'<section class="book-chapter" id="day-{item["day"]}"><p class="eyebrow">LESSON {item["day"]:02}</p><h2>{html.escape(item["title"])}</h2>{body}</section>')
        contents.append(f'<li><a href="#day-{item["day"]}">{item["day"]:02}. {html.escape(item["title"])}</a></li>')
        manuscript.append(f'\n\n# Lesson {item["day"]:02}: {item["title"]}\n\n{resolve_links(raw, ORIGIN + base)}')
    for slug, title in [("manipulation", "Pick-and-place field note"), ("models", "Robot models and Dream Labs"), ("hardware", "Hardware buying guide"),
                        ("isaac-foundations", "Isaac Sim scene-building workshop"), ("robot-learning", "Robot learning and datasets"), ("cloud-lab", "Cloud Isaac lab"),
                        ("evaluation", "Evaluation and sim-to-real"), ("applications", "Applications and pilot economics")]:
        raw = with_hardware_tables((ROOT/f"content/pages/{slug}.md").read_text())
        body, _ = render_md(raw, base)
        body = re.sub(r'id="([^"]+)"', lambda m: f'id="appendix-{slug}-{m[1]}"', body)
        body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#appendix-{slug}-{m[1]}"', body)
        body = body.replace('<h3', '<h4').replace('</h3>', '</h4>').replace('<h2', '<h3').replace('</h2>', '</h3>')
        chapters.append(f'<section class="book-chapter" id="appendix-{slug}"><p class="eyebrow">FIELD NOTE</p><h2>{title}</h2>{body}</section>')
        contents.append(f'<li><a href="#appendix-{slug}">{title}</a></li>')
        manuscript.append(f'\n\n# Field note: {title}\n\n{resolve_links(raw, ORIGIN + base)}')
    book = f'<div class="lesson-header"><p class="eyebrow">THE READING EDITION</p><h1>Physical AI for<br>Software Engineers</h1><p class="lesson-deck">All 21 lessons and eight practical field notes, from choosing an arm and building a scene to learning, cloud setup, evaluation, and application costs. Work at your own pace. Use your browser’s Print command to save a personal PDF.</p><a class="text-link" href="{base}/book.md" download>Download the Markdown manuscript ↓</a></div><article class="prose"><h2>Contents</h2><ol class="book-contents">{"".join(contents)}</ol>{"".join(chapters)}</article>'
    page("book/index.html", "The reading edition", "All 21 original lessons in a printable reading edition.", book)
    (out/"book.md").write_text("\n".join(manuscript))
    page("404.html", "Page not found", "Find your way back to the field guide.", f'<div class="lesson-header"><p class="eyebrow">404 / OFF THE MAP</p><h1>Let’s find your way back.</h1><p class="lesson-deck">This page has moved or does not exist.</p><a class="button primary" href="{base}/">Open the learning path →</a></div>')
    (out/"search-index.json").write_text(json.dumps(search, ensure_ascii=False))
    (out/".nojekyll").touch()
    (out/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}{base}/sitemap.xml\n")
    (out/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{html.escape(u)}</loc></url>' for u in urls if not u.endswith('404.html')) + '</urlset>')
    print(f"Built {len(urls)} pages and {len(search)} search entries into {out}")


if __name__ == "__main__":
    main()

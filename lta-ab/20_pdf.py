"""
20_pdf.py -- build lta-ab/NOTE.pdf from NOTE.md and the two chart SVGs.

  python3 lta-ab/20_pdf.py

NOTE.md is the only source of the PDF's text, so the number manifest check on
NOTE.md (14_manifest.py --check) covers the PDF. The charts are the SVGs in
figs/, inlined. Route: NOTE.md -> HTML (a small converter for the Markdown
subset NOTE.md uses: headings, paragraphs, bold, italics, code, bullet lists,
one table, images, bare URLs) -> A4 PDF printed by headless Chromium through
Playwright, with page numbers and the repository link in the footer.

The build asserts that the text is pure ASCII before printing. Chromium stamps
a creation date into the PDF, so NOTE.pdf is not byte-reproducible and is not
in CHECKSUMS.md5; rebuild it with this script after any change to NOTE.md.
Needs the "playwright" package and its Chromium (see tools/README.md).
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTE = os.path.join(HERE, "NOTE.md")
PDF = os.path.join(HERE, "NOTE.pdf")
REPO = "https://github.com/jacobbuildmodel/coe-analysis"
CHART_WIDTH = "100%"

CSS = """
@page { size: A4; margin: 15mm 17mm 17mm 17mm; }
html { color-scheme: light; }
body { font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; font-size: 9.5pt;
       line-height: 1.38; color: #0b0b0b; margin: 0;
       font-variant-ligatures: none; font-feature-settings: "liga" 0, "clig" 0; }
h1 { font-size: 15pt; line-height: 1.25; margin: 0 0 6pt 0; }
h2 { font-size: 11.5pt; margin: 13pt 0 4pt 0; break-after: avoid; }
p { margin: 0 0 6pt 0; }
p.byline { color: #444; font-size: 9pt; }
ul { margin: 0 0 6pt 0; padding-left: 16pt; }
li { margin: 0 0 2pt 0; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.5pt; }
table { border-collapse: collapse; margin: 4pt 0 8pt 0; font-size: 9.5pt; break-inside: avoid; }
th, td { border-bottom: 0.5pt solid #bbb; padding: 2pt 8pt 2pt 0; text-align: left; }
td:not(:first-child), th:not(:first-child) { text-align: right; }
figure { float: right; width: 60%; margin: 2pt 0 8pt 12pt; break-inside: avoid; }
h2 { clear: both; }
figure svg { width: """ + CHART_WIDTH + """; height: auto; }
a { color: #0b0b0b; }
.form { border: 0.5pt solid #999; padding: 6pt 8pt; break-inside: avoid; }
"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(https?://[^\s<)]+[^\s<).,;])", r'<a href="\1">\1</a>', s)
    return s


def svg(path):
    t = open(os.path.join(HERE, path), encoding="utf-8").read()
    t = re.sub(r'\swidth="\d+" height="\d+"', "", t, count=1)
    return t


def to_html(md):
    lines = md.split("\n")
    out, para, i = [], [], 0
    in_form = False

    def flush():
        if para:
            text = " ".join(x.strip() for x in para)
            cls = ' class="byline"' if text.startswith("*Evidence note") else ""
            out.append(f"<p{cls}>{inline(text)}</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# "):
            flush(); out.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.startswith("## "):
            flush()
            if in_form:
                out.append("</div>")
                in_form = False
            out.append(f"<h2>{inline(ln[3:])}</h2>")
            if ln.startswith("## For the feedback form"):
                out.append('<div class="form">')
                in_form = True
        elif re.match(r"!\[[^\]]*\]\([^)]*\)", ln):
            flush()
            alt, src = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", ln).groups()
            out.append(f'<figure aria-label="{html.escape(alt)}">{svg(src)}</figure>')
        elif ln.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells):
                    rows.append(cells)
                i += 1
            t = ["<table>", "<tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"]
            t += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:]]
            out.append("\n".join(t + ["</table>"]))
            continue
        elif re.match(r"\s*- ", ln):
            flush()
            items = []
            while i < len(lines) and (re.match(r"\s*- ", lines[i]) or (lines[i].startswith("  ") and items)):
                m = re.match(r"(\s*)- (.*)", lines[i])
                if m:
                    items.append([len(m[1]) // 2, m[2]])
                else:
                    items[-1][1] += " " + lines[i].strip()
                i += 1
            depth, h = -1, []
            for lvl, text in items:
                while depth < lvl:
                    h.append("<ul>"); depth += 1
                while depth > lvl:
                    h.append("</ul>"); depth -= 1
                h.append(f"<li>{inline(text)}</li>")
            h += ["</ul>"] * (depth + 1)
            out.append("".join(h))
            continue
        elif ln.strip() == "":
            flush()
        elif in_form:
            flush(); out.append(f"<p>{inline(ln)}</p>")
        else:
            para.append(ln)
        i += 1
    flush()
    if in_form:
        out.append("</div>")
    return "\n".join(out)


def main():
    md = open(NOTE, encoding="utf-8").read()
    bad = sorted({c for c in md if ord(c) > 127})
    assert not bad, f"NOTE.md is not pure ASCII: {bad}"
    body = to_html(md)
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>COE Categories A and B: '
           f'evidence note</title><style>{CSS}</style></head><body>{body}</body></html>')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.emulate_media(media="print", color_scheme="light")
        pg.set_content(doc, wait_until="load")
        footer = ('<div style="font-size:8pt;color:#555;width:100%;padding:0 17mm;'
                  'font-family:DejaVu Sans,Helvetica,Arial,sans-serif;display:flex;justify-content:space-between">'
                  f'<span>{REPO} (lta-ab)</span>'
                  '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
        pg.pdf(path=PDF, format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>", footer_template=footer,
               margin={"top": "15mm", "bottom": "17mm", "left": "17mm", "right": "17mm"})
        b.close()
    import pypdf
    r = pypdf.PdfReader(PDF)
    text = "".join(pg.extract_text() for pg in r.pages)
    nonascii = sorted({c for c in text if ord(c) > 127})
    print(f"  wrote NOTE.pdf: {len(r.pages)} pages; non-ASCII characters in extracted text: {nonascii or 'none'}")
    assert 2 <= len(r.pages) <= 3, "NOTE.pdf is not 2-3 pages"
    return 0


if __name__ == "__main__":
    sys.exit(main())

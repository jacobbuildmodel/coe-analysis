"""
20_pdf.py -- build lta-ab/NOTE.pdf from NOTE.md and Figure 1.

  python3 lta-ab/20_pdf.py

Layout: the checker's research-paper design (office/redesign/note.html). It
uses A4, a Source Serif 4 body at 9.6pt and Source Sans 3 headings. The footer
holds the author, a short title and "page x / y", set in CSS page-margin boxes.
The fonts are embedded from lta-ab/fonts/.

NOTE.md is the only source of the PDF's text, so the number-manifest check on
NOTE.md (14_manifest.py --check) covers the PDF. Everything from the heading
"## For the feedback form" on stays out of the PDF. NOTE.md uses pandoc-style
fenced blocks (::: kicker, meta, summary, figure, method) for the layout's
boxes. A "Table N." line directly before a table becomes its caption. A
paragraph starting "Notes:" takes the small notes style.

The route is NOTE.md, then HTML, then a PDF printed by headless Chromium
through Playwright, with Figure 1 embedded as figs/lta_ab_fig1.png (220 dpi).
Chromium stamps a creation date, so NOTE.pdf is not byte-reproducible and is
not in CHECKSUMS.md5. The build asserts pure-ASCII text, two pages, and fonts
embedded.
"""
import html
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NOTE = os.path.join(HERE, "NOTE.md")
PDF = os.path.join(HERE, "NOTE.pdf")
FONTS = os.path.join(HERE, "fonts")
TITLE = "COE Categories A and B: Evidence from the Bidding Record, 2010-2026"

# note.html's stylesheet, verbatim except for the font URLs and the ligature rule at the end.
CSS = """
@font-face{font-family:"Source Serif 4";src:url(FONTDIR/SourceSerif4-Regular.ttf);font-weight:400}
@font-face{font-family:"Source Serif 4";src:url(FONTDIR/SourceSerif4-It.ttf);font-style:italic}
@font-face{font-family:"Source Serif 4";src:url(FONTDIR/SourceSerif4-Semibold.ttf);font-weight:600}
@font-face{font-family:"Source Sans 3";src:url(FONTDIR/SourceSans3-Regular.ttf);font-weight:400}
@font-face{font-family:"Source Sans 3";src:url(FONTDIR/SourceSans3-Semibold.ttf);font-weight:600}
@font-face{font-family:"Source Sans 3";src:url(FONTDIR/SourceSans3-Bold.ttf);font-weight:700}
@page{size:A4;margin:17mm 19mm 16mm 19mm;
  @bottom-left{content:"Jacob Ong | COE Categories A and B: evidence from the bidding record";font:7.5pt "Source Sans 3";color:#6b6a66}
  @bottom-right{content:counter(page) " / " counter(pages);font:7.5pt "Source Sans 3";color:#6b6a66}}
html{font-variant-ligatures:none}
body{font:9.6pt/1.42 "Source Serif 4";color:#141413;margin:0}
.kicker{font:600 8pt "Source Sans 3";letter-spacing:.06em;text-transform:uppercase;color:#1f3a5f;margin:0 0 6pt}
h1{font:700 17pt/1.2 "Source Sans 3";margin:0 0 8pt;color:#0b0b0b}
.meta{font:8.5pt/1.45 "Source Sans 3";color:#52514e;border-top:0.6pt solid #c9c8c3;border-bottom:0.6pt solid #c9c8c3;padding:6pt 0;margin-bottom:12pt}
.meta b{color:#141413;font-weight:600}
h2{font:600 11pt "Source Sans 3";margin:11pt 0 3pt;color:#0b0b0b}
p{margin:0 0 6pt;text-align:left;hyphens:auto}
.summary{background:#f3f2ee;padding:7pt 11pt 4pt;margin:0 0 2pt}
.summary h2{margin-top:0}
.summary ul{margin:0;padding-left:13pt}.summary li{margin-bottom:4pt}
table{border-collapse:collapse;width:78%;font:8.5pt "Source Sans 3";margin:4pt 0 3pt}
caption{caption-side:top;text-align:left;font:600 8.5pt "Source Sans 3";padding-bottom:4pt;color:#0b0b0b}
th,td{padding:3pt 6pt;border-bottom:0.5pt solid #e0dfda;text-align:right}
th:first-child,td:first-child{text-align:left}
thead th{border-bottom:0.8pt solid #52514e;font-weight:600;color:#141413}
tbody tr:last-child td{border-bottom:0.8pt solid #52514e}
.note{font:7.5pt/1.4 "Source Sans 3";color:#52514e;margin:0 0 8pt}
figure{margin:10pt 0 6pt;break-inside:avoid}
figure .ftitle{font:600 9pt "Source Sans 3";margin-bottom:4pt}
figure img{width:100%}
ul.method{padding-left:12pt;margin:0;font:7.8pt/1.35 "Source Sans 3";color:#3a3936}ul.method li{margin-bottom:2pt}
.small{font-size:9pt}
/* added: the shorthand "font:" on body and other elements resets html's
   font-variant-ligatures, so Chromium set ff/fi ligatures (U+FB00, U+FB01)
   and the PDF text was not pure ASCII. This restores the intent. */
*{font-variant-ligatures:none !important}
"""


def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def blocks(lines):
    """Split lines into paragraphs, tables, lists and headings."""
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("#"):
            out.append(("h", ln))
            i += 1
        elif ln.startswith("|"):
            t = []
            while i < len(lines) and lines[i].startswith("|"):
                t.append(lines[i]); i += 1
            out.append(("table", t))
        elif ln.startswith("- "):
            t = []
            while i < len(lines) and lines[i].startswith("- "):
                t.append(lines[i][2:]); i += 1
            out.append(("ul", t))
        elif ln.startswith("!["):
            out.append(("img", ln)); i += 1
        else:
            t = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ", "![")):
                t.append(lines[i].strip()); i += 1
            out.append(("p", " ".join(t)))
    return out


def render(bl, ul_class=None):
    h, pending_caption = [], None
    for kind, v in bl:
        if kind == "h":
            lvl = len(v) - len(v.lstrip("#"))
            h.append(f"<h{lvl}>{inline(v[lvl:].strip())}</h{lvl}>")
        elif kind == "p" and re.match(r"Table \d+\. ", v):
            pending_caption = v
        elif kind == "p":
            cls = ' class="note"' if v.startswith("Notes:") else ""
            h.append(f"<p{cls}>{inline(v)}</p>")
        elif kind == "ul":
            cls = f' class="{ul_class}"' if ul_class else ""
            h.append(f"<ul{cls}>" + "".join(f"<li>{inline(x)}</li>" for x in v) + "</ul>")
        elif kind == "img":
            alt, src = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", v).groups()
            h.append(f'<img src="file://{os.path.join(HERE, src)}" alt="{html.escape(alt)}">')
        elif kind == "table":
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in v]
            rows = [r for r in rows if not all(re.fullmatch(r"-+", c) for c in r)]
            t = ["<table>"]
            if pending_caption:
                t.append(f"<caption>{inline(pending_caption)}</caption>")
                pending_caption = None
            t.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr></thead><tbody>")
            t += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:]]
            h.append("".join(t) + "</tbody></table>")
    return "\n".join(h)


def to_html(md):
    md = md.split("## For the feedback form")[0]
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"::: (\w+)$", lines[i])
        if m:
            name, j = m[1], i + 1
            while lines[j].strip() != ":::":
                j += 1
            inner = lines[i + 1:j]
            if name == "kicker":
                out.append(f'<div class="kicker">{inline(" ".join(inner).strip())}</div>')
            elif name == "meta":
                out.append(f'<div class="meta">{inline(" ".join(x.strip() for x in inner))}</div>')
            elif name == "summary":
                out.append(f'<div class="summary">{render(blocks(inner))}</div>')
            elif name == "method":
                out.append(render(blocks(inner), ul_class="method"))
            elif name == "figure":
                bl = blocks(inner)
                assert bl[0][0] == "p"
                out.append(f'<figure><div class="ftitle">{inline(bl[0][1])}</div>{render(bl[1:])}</figure>')
            else:
                raise ValueError(f"unknown block ::: {name}")
            i = j + 1
            continue
        j = i
        while j < len(lines) and not re.match(r"::: \w+$", lines[j]):
            j += 1
        out.append(render(blocks(lines[i:j])))
        i = j
    return "\n".join(out)


def main():
    md = open(NOTE, encoding="utf-8").read()
    bad = sorted({c for c in md if ord(c) > 127})
    assert not bad, f"NOTE.md is not pure ASCII: {bad}"
    css = CSS.replace("FONTDIR", "file://" + FONTS)
    doc = (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n<title>{TITLE}</title>\n'
           f"<style>{css}</style></head><body>\n{to_html(md)}\n</body></html>\n")
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as tmp:
        page_html = os.path.join(tmp, "note.html")
        open(page_html, "w", encoding="utf-8").write(doc)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.emulate_media(media="print", color_scheme="light")
            pg.goto("file://" + page_html, wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.pdf(path=PDF, prefer_css_page_size=True, print_background=True)
            b.close()
    import pypdf
    r = pypdf.PdfReader(PDF)
    text = "".join(p.extract_text() for p in r.pages)
    nonascii = sorted({c for c in text if ord(c) > 127})
    fonts = set()
    for p in r.pages:
        for f in (p["/Resources"].get("/Font") or {}).values():
            fo = f.get_object()
            desc = fo.get("/FontDescriptor") or (fo.get("/DescendantFonts") or [{}])[0].get_object().get("/FontDescriptor")
            embedded = bool(desc and any(k in desc.get_object() for k in ("/FontFile", "/FontFile2", "/FontFile3")))
            fonts.add((str(fo.get("/BaseFont")).split("+")[-1], embedded))
    print(f"  wrote NOTE.pdf: {len(r.pages)} pages; fonts {sorted(fonts)}; "
          f"non-ASCII in extracted text: {nonascii or 'none'}")
    assert len(r.pages) == 2, "NOTE.pdf is not 2 pages"
    assert all(e for _, e in fonts), "a font is not embedded"
    assert not nonascii
    return 0


if __name__ == "__main__":
    sys.exit(main())

from lxml import etree, html
from lxml.html import builder, HtmlElement
from lxml.etree import QName, ElementTree, Element, SubElement
import matplotlib.pyplot as plt
import typer
import re
from ns import NS, NS_TEI, NS_UD

FP_REMOVE_S = "xsl/remove_s.xsl"
FP_TOHTML = "xsl/tohtml.xsl"
Q_START = "«"
Q_END = "»"


def apply_xslt(fp_xslt: str, tree: ElementTree) -> ElementTree:
    xsl_remove_s = etree.parse(fp_xslt)
    xsl_remove_s = etree.XSLT(xsl_remove_s)
    tree = xsl_remove_s(tree)
    return tree


def add_q(tree: Element) -> None:
    """Add <q> elements."""
    paragraphs = tree.iterfind(".//p", NS)
    for p in paragraphs:
        end = False
        while not end:
            for n, i in enumerate(p):
                if i.text == Q_END:
                    for n_prev, prev in enumerate(reversed(p)):
                        if prev.text == Q_START:
                            n_prev = n - n_prev
                            q = Element("q", {})
                            for w in p[n_prev:n]:
                                q.append(w)
                            p.insert(n_prev, q)
                    break
            end = True
        if p[0].text == Q_START:
            p.tag = 'blockquote'


def make_plot_from_verb_ud_attr(
    tree: ElementTree,
    att_name: str,
    values_up: tuple,
    values_down: tuple,
) -> None:
    att = QName(NS_UD, att_name)
    cur_x = 0
    cur_y = 0
    x = [cur_x]
    y = [cur_y]
    paragraphs = tree.iterfind(".//p", NS)
    for p in paragraphs:
        for v in p.iterfind(".//w", NS):
            if v.attrib["pos"] not in ("AUX", "VERB"):
                continue
            if att in v.attrib:
                tense = v.attrib[att]
                if tense in values_up:
                    cur_y -= 1
                elif tense in values_down:
                    cur_y += 1
                else:
                    continue
                cur_x += 1
                x.append(cur_x)
                y.append(cur_y)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()


def to_text(p: Element) -> str:
    """Get text from a <p> element.
    Spaces between tokens are added according to french typographic rules.
    """
    # TODO: mmmmh no. i need to colorize verbes dependings on their Mood/Tense.
    words = (
        i.text
        for i in p.iterdescendants()
        if QName(i.tag).localname in ("w", "pc")
    )
    text = " ".join(words)
    text = re.sub(r"(['’\(\[\{]) +", r"\1", text)
    text = re.sub(r" +([-.,?!:;)…\]\}])", r"\1", text)
    return text


def make_html_document(title: str, stylesheet: str) -> HtmlElement:
    """Make the minimal structure of an HTML page."""
    doc = builder.HTML(
        builder.HEAD(
            builder.LINK(
                rel="stylesheet", href=stylesheet, type="text/css"
            ),
            builder.TITLE(title),
        ),
        builder.BODY(),
    )
    return doc


def make_svg_curve_from_verb(
    tree: ElementTree,
    htmldoc: Element,
    att_name: str,
    values_up: tuple,
    values_down: tuple,
) -> None:
    att = QName(NS_UD, att_name)
    x = 0
    y = 0
    paragraphs = tree.iterfind(".//text//p", NS)
    body = htmldoc.find(".//body")
    h1 = SubElement(body, "h1", {})
    h1.text = "Les temps de la fin du monde"
    pts = []
    for n, p in enumerate(paragraphs):
        hp = SubElement(body, "p", {"id": str(n)})
        hp.text = to_text(p)
        for v in p.iterfind(".//w", NS):
            if v.attrib["pos"] not in ("AUX", "VERB"):
                continue
            if att in v.attrib:
                tense = v.attrib[att]
                if tense in values_up:
                    y -= 1
                elif tense in values_down:
                    y += 1
                else:
                    continue
                x += 1
                pts.append((x, y, n))
    ys = [i[1] for i in pts]
    max_y = max(ys)
    min_y = min(ys)
    assert max_y > min_y
    div = SubElement(body, "div", {"class": "svg-container"})
    svg_att = {
        "viewBox": f"0 0 {str(len(pts))} 6000",
        "preserveAspectRatio": "none",
    }
    svg = SubElement(div, "svg", svg_att)
    for x, y, ref in pts:
        a = SubElement(svg, "a", {"href": f"#{ref}"})
        _ = SubElement(a, "circle", {"cx": str(x), "cy": str(-y)})
        body.insert(0, svg)


# def make_svg_curve_from_verb_percent(
#     tree: ElementTree,
#     htmldoc: Element,
#     att_name: str,
#     values_up: tuple,
#     values_down: tuple,
# )


def main(fp_in: str, fp_css: str, fp_out: str) -> None:
    tree = etree.parse(fp_in)
    tree = apply_xslt(FP_REMOVE_S, tree)
    hdoc = apply_xslt(FP_TOHTML, tree)
    hdoc = make_html_document("la fin du monde", fp_css)
    # make_svg_curve_from_verb(
    #     tree,
    #     hdoc,
    #     "Tense",
    #     ("Past", "Imp"),
    #     ("Pres", "Fut"),
    # )
    with open(fp_out, "bw") as f:
        f.write(
            html.tostring(hdoc, encoding="utf-8", pretty_print=True)
        )


if __name__ == "__main__":
    typer.run(main)

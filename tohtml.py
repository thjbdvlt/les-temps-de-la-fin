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

TAGS_NEWLINE = [
    "div",
    "head",
    "html",
    "p",
    "meta",
    "body",
    "link",
    "h1",
    "h2",
    "h3",
    "h4",
]


def apply_xslt(fp_xslt: str, tree: ElementTree) -> ElementTree:
    """Apply an XSLT on a tree and returns the new tree."""
    xsl_remove_s = etree.parse(fp_xslt)
    xsl_remove_s = etree.XSLT(xsl_remove_s)
    tree = xsl_remove_s(tree)
    return tree


def _find_add_one_pair_pc(
    p: Element,
    tag: QName,
    pc_open: str,
    pc_close: str,
    remove_pc: bool = True
) -> None:
    """Make an Element from a found pair of punctuation signs, like () or «».
    This function only find one pair. It creates an Element that contains every elements between the opening and closing signs. By default, it also remove the punctuation signs (can be turned off using `remove_pc=False`).
    """
    for n, i in enumerate(p):
        if i.text == pc_close:
            for n_prev, prev in enumerate(reversed(p[:n])):
                if prev.text == pc_open:
                    n_prev = n - n_prev
                    # make the <q> elemeent
                    q = Element(tag, {})
                    # populate the <q> elements with everything between the start/end quotes, including the quotes.
                    for w in p[n_prev - 1 : n + 1]:
                        q.append(w)
                    # remove the quotes signs
                    if remove_pc:
                        q.remove(q[0])
                        q.remove(q[-1])
                    # put the <q> element at the right place
                    p.insert(n_prev - 1, q)
                    return


def find_add_pairs_pc(
    p: Element,
    tag: QName,
    pc_open: str,
    pc_close: str,
    remove_pc: bool = True
) -> None:
    """Make Elements from punctuation signs pairs, like () or «»."""
    while any((i.text == pc_close for i in p)) and any(
        (i.text == pc_open for i in p)
    ):
        _find_add_one_pair_pc(p, tag, pc_open, pc_close, remove_pc)


def add_q(tree: Element) -> None:
    """Add <q> elements."""
    paragraphs = tree.iterfind(".//p", NS)
    for p in paragraphs:
        find_add_pairs_pc(p, QName(NS_TEI, "q"), Q_START, Q_END)
        # remove empty paragraph
        if len(p) == 0:
            p.getparent().remove(p)
        else:
            # if a paragraph only contains a start tag (and no end tag), and if it starts with a start tag, make a blockquote with it.
            if p[0].text == Q_START:
                q = Element(QName(NS_TEI, "q"), {})
                for i in p:
                    q.append(i)
                q.remove(q[0])
                p.append(q)


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
        for v in p.iterfind(".//em", NS):
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
    att_name: str,
    values_up: tuple,
    values_down: tuple,
) -> None:
    att = QName(NS_UD, att_name)
    x = 0
    y = 0
    paragraphs = tree.iterfind(".//body//p", NS)
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


def format_indent(s: str) -> str:
    # remove useless new lines
    s = s.replace("\n", " ")
    # remove over-indentation
    s = re.sub(r"  +", " ", s)
    # apply french typography for spaces and punctuation signs
    s = re.sub(r"([\(\[\{’'])[\n ]+", r"\1", s)
    s = re.sub(r"[\n ]+([-.,:;?!\)\]\}…])", r"\1", s)
    # add newlines after some tags, e.g. <p>, <body>, ... but not after <q> or <em>. it prevents the addition of unwanted spaces inside paragraphs.
    tags = r'|'.join(TAGS_NEWLINE)
    s = re.sub(rf"(<(?:{tags})[ \n>])", r"\n\1", s)
    # add missing spaces in cases like "passerait.</q>La foule"
    s = re.sub(r"(</(?:em|q)>)(\w)", r"\1 \2", s)
    return s


def main(fp_in: str, fp_css: str, fp_out: str) -> None:
    tree = etree.parse(fp_in)
    # remove sentence, to avoid overlapping with q (and because it's simplier like this)
    tree = apply_xslt(FP_REMOVE_S, tree)
    # add q and blockquotes
    add_q(tree)
    # apply xslt to produce html
    hdoc = apply_xslt(FP_TOHTML, tree)
    # add the svg at the top of the file
    # make_svg_curve_from_verb(
    #     tree,
    #     "Tense",
    #     ("Past", "Imp"),
    #     ("Pres", "Fut"),
    # )
    s = html.tostring(
        hdoc, encoding="utf-8", pretty_print=True
    ).decode()
    s = format_indent(s)
    with open(fp_out, "w") as f:
        f.write(s)


if __name__ == "__main__":
    typer.run(main)

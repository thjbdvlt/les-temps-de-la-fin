from lxml import etree, html
from lxml.etree import ElementTree, Element, SubElement
from typing import Generator, Callable
import typer
import re

DOCTYPE = "<!DOCTYPE PUBLIC>"
SVG_HTML = f"""{DOCTYPE}
<html>
<head>
<meta name="author" content="Thibault Ziegler"/>
<link rel="stylesheet" href="svg.css"/>
</head>
<body>
<p><a href="les-temps-de-la-fin.html">Retour</a>
</p>
<div class="svg-container">
</div>
</body>
</html>
"""
SVG_HEIGHT = 400


def apply_xslt(fp_xslt: str, tree: ElementTree) -> ElementTree:
    """Apply an XSLT on a tree and returns the new tree."""
    return etree.XSLT(etree.parse(fp_xslt))(tree)


def add_pid(tree: ElementTree) -> None:
    """Add @id attribut to paragraphs."""
    for n, p in enumerate(tree.iterfind(".//body//p"), 1):
        p.attrib["id"] = str(n)


class Verb:
    keys = {"f", "t", "m"}
    lookup = {}

    def __init__(self, el: Element):
        cl = el.attrib["class"]
        if cl in Verb.lookup:
            attrs = Verb.lookup[cl]
        else:
            attrs = cl.split()
            self.pos = attrs[0]
            attrs = attrs[1:]
            attrs = [i.split("-") for i in attrs]
            attrs = {key: value.lower() for key, value in attrs}
            for i in Verb.keys:
                if i not in attrs:
                    attrs[i] = None
            Verb.lookup[cl] = attrs
        for i in attrs:
            setattr(self, i, attrs[i])
        self.d = attrs
        self.q = el.getparent().tag == "q"


def get_verbs(tree: ElementTree) -> Generator:
    """Get verbs classes (morphology) and paragraph id."""
    for p in tree.iterfind(".//body//p"):
        ref = p.attrib["id"]
        for v in p.iterfind(".//em"):
            yield Verb(v), ref


def init_svg(pts: list[tuple], h: int, add_atts: dict = None):
    """Init a SVG element."""
    attrs = {
        "viewBox": f"0 0 {str(len(pts))} {h}",
        "preserveAspectRatio": "none",
        "x": "0",
        "y": "0",
        "width": "100%",
        "height": "100",
    }
    if add_atts:
        attrs.update(add_atts)
    return Element("svg", attrs)


def link(
    svg: Element, tag: str, attrs: dict, pid, href_pref: str = ""
) -> Element:
    """Create an Element enclosed within an <a> referencing to a <p>."""
    a = SubElement(svg, "a", {"href": f"{href_pref}#{pid}"})
    for i in attrs:
        attrs[i] = str(attrs[i])
    SubElement(a, tag, attrs)


def make_svg(tree: Element, func: Callable, href_pref: str = '') -> None:
    """Make a svg with colors."""
    pts = [
        (x, func(v), pid) for x, (v, pid) in enumerate(get_verbs(tree))
    ]
    svg = init_svg(pts, SVG_HEIGHT)
    for x, y, pid in pts:
        attrs = {
            "x1": x,
            "x2": x,
            "y1": 0,
            "y2": SVG_HEIGHT,
            "class": y,
        }
        link(svg, "line", attrs, pid, href_pref)
    return svg


def make_svg_inq_outq(
    tree: Element, morph: dict, title: str, fp_text: str
) -> None:
    """Make two SVG for verbs inside or outside quotes."""
    def hasmorph(v):
        return all([v.d[i] in morph[i] for i in morph])

    def func_inq(v):
        return 'line1' if hasmorph(v) and v.q else 'line0'

    def func_outq(v):
        return 'line1' if hasmorph(v) and not v.q else 'line0'

    div = Element("div")
    h2 = Element("h2")
    h2.text = title
    div.append(h2)

    for cl, f, head in (
        ("outq", func_outq, "hors citations"),
        ("inq", func_inq, "dans des citations"),
    ):
        h3 = Element("h3")
        h3.text = head
        div.append(h3)
        svg = make_svg(tree, f, fp_text)
        div.append(svg)
    return div


def format_indent(s: str) -> str:
    """Format and indent the html. Add or rempve space when needed."""
    # remove useless new lines
    s = s.replace("\n", " ")
    # remove over-indentation
    s = re.sub(r"  +", " ", s)
    # apply french typography for spaces and punctuation signs
    s = re.sub(r"([\(\[\{’'])[\n ]+", r"\1", s)
    s = re.sub(r"[\n ]+([-.,:;?!\)\]\}…])", r"\1", s)
    # add newlines after some tags, e.g. <p>, <body>, ... but not after <q> or <em>. it prevents the addition of unwanted spaces inside paragraphs.
    tags = [
        # html structure
        "head",
        "html",
        "meta",
        "body",
        "link",
        # main text structure
        "div",
        "p",
        # headers
        "h1",
        "h2",
        "h3",
        "h4",
        # svg
        "svg",
        "a",
        # navigation bar
        "nav",
        "ul",
        "li",
    ]
    tags = r"|".join(tags)
    s = re.sub(rf"(<(?:{tags})[ \n>])", r"\n\1", s)
    # add missing spaces in cases like "passerait.</q>La foule"
    s = re.sub(r"(</(?:em|q)>)(\w)", r"\1 \2", s)
    return s


def add_to_nav(
    tree: ElementTree, text: str, href: str, add_attrs: dict
) -> None:
    """Add a link to the navigation bar."""
    ul = tree.find(".//nav/ul")
    li = SubElement(ul, "li", {})
    attrs = {"href": href}
    if add_attrs:
        attrs.update(add_attrs)
    a = SubElement(li, "a", attrs)
    a.text = text


def create_svg_xml(svg: Element, name: str, fp: str) -> None:
    """Serialize the SVG embedded in a HTML file."""
    tree = html.fromstring(SVG_HTML)
    div = tree.find('.//body/div[@class="svg-container"]')
    div.append(svg)
    with open(fp, "bw") as f:
        f.write(html.tostring(tree, encoding="utf-8", doctype=DOCTYPE))


def main(fp_in: str, fp_css: str, fp_out: str) -> None:
    """Make the HTML files."""
    tree = etree.parse(fp_in)
    tree = apply_xslt("xsl/tohtml.xsl", tree)
    tree = apply_xslt("xsl/remove_namespaces.xsl", tree)
    add_pid(tree)

    # the main SVG index, which is placed on the same page
    svg = make_svg(tree, lambda i: i.t)
    div = tree.find('.//div[@id="index"]')
    div.append(svg)

    # external svg, to avoid an HUGE unloadable html file
    for name, d, title in [
        ("fut", {"t": ["fut"]}, "futur"),
        ("cnd", {"m": ["cnd"]}, "conditionnel"),
        ("pres", {"t": ["pres"]}, "présent"),
        ("imp", {"t": ["imp"]}, "imparfait"),
        ("past", {"t": ["past"], "m": ["ind"]}, "passé simple"),
    ]:
        svg = make_svg_inq_outq(tree, d, title, fp_out)
        fp = f"{name}.html"
        create_svg_xml(svg, name, fp)
        add_to_nav(tree, name, fp, {"class": name})

    s = html.tostring(
        tree, encoding="utf-8", pretty_print=True, doctype=DOCTYPE
    ).decode()
    s = format_indent(s)
    with open(fp_out, "w") as f:
        f.write(s)


if __name__ == "__main__":
    typer.run(main)

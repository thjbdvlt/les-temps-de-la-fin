from lxml import etree
from lxml.etree import QName, ElementTree, Element, SubElement
import typer
from ns import NS, NS_TEI, NS_UD

FP_REMOVE_S = "xsl/remove_s.xsl"
Q_START = "«"
Q_END = "»"


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
    paragraphs = tree.iterfind(".//body//p", NS)
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


def main(fp: str):
    x = etree.parse(fp)
    x = apply_xslt("xsl/remove_s.xsl", x)
    add_q(x)
    x.write(fp, encoding='utf-8')


if __name__ == '__main__':
    typer.run(main)

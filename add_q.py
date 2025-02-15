from lxml import etree
from lxml.etree import Element, ElementTree, SubElement
from ns import NS, NS_TEI, NS_UD
import typer

Q_START = "«"
Q_END = "»"


def add_q(tree: Element) -> None:
    paragraphs = tree.iterfind('.//p', NS)
    for p in paragraphs:
        end = False
        while not end:
            for n, i in enumerate(p):
                if i.text == Q_END:
                    for n_prev, prev in enumerate(reversed(p)):
                        if prev.text == Q_START:
                            n_prev = n - n_prev
                            q = Element('q', {})
                            for w in p[n_prev:n]:
                                q.append(w)
                            p.insert(n_prev, q)
                    break
            end = True
        for n, i in enumerate(p):
            if i.text == Q_START:
                q = Element('q', {})
                for w in p[n:]:
                    q.append(w)
                p.insert(n, q)


def main(fp_in: str, fp_out: str) -> None:
    tree = etree.parse(fp_in)
    xsl_remove_s = etree.parse("./xsl/remove_s.xsl")
    xsl_remove_s = etree.XSLT(xsl_remove_s)
    tree = xsl_remove_s(tree)
    add_q(tree)
    tree.write(fp_out, pretty_print=True)


if __name__ == "__main__":
    typer.run(main)

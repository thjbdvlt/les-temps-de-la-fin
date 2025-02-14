from lxml import etree
from lxml.etree import QName
import typer


NS_TEI = "http://www.tei-c.org/ns/1.0"
NS_UD = "https://universaldependencies.org/u/feat"
NS = {None: NS_TEI, "ud": NS_UD}

FEAT_ORDER = [
    "VerbForm",
    "PronType",
    "Definite",
    "NumType",
    "Mood",
    "Tense",
    "Person",
    "Number",
    "Number_psor",
    "Voice",
    "Poss",
    "Polarity",
    "Reflex",
]


def ud_to_msd(attrs: dict) -> dict:
    """Move @ud:Tense, @ud:Mood, etc., to a @msd label."""
    attrs = {QName(i): attrs[i] for i in attrs}
    ud = {}
    non_ud = {}
    for i in attrs:
        if i.namespace == NS_UD:
            ud[i.localname] = attrs[i]
        else:
            non_ud[i] = attrs[i]
    ord_ud = {}
    for i in FEAT_ORDER:
        if i in ud:
            ord_ud[i] = ud[i]
    label_parts = [v if v != "Yes" else k for k, v in ord_ud.items()]
    label = ".".join(label_parts)
    non_ud["msd"] = label
    return non_ud


def main(fp_in: str, fp_out: str) -> None:
    x = etree.parse(fp_in)
    for i in x.findall(".//w", NS):
        attrs = ud_to_msd(i.attrib)
        i.attrib.clear()
        i.attrib.update(attrs)
    x.write(fp_out)


if __name__ == "__main__":
    typer.run(main)

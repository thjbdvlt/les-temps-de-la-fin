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
    """Move @ud:Tense, @ud:Mood, etc., to a @msd label.
    The @msd label will look like 'Cnd.Pres.3.Sing': it's made from values of all FEATS, in a determined order. There is one exception: FEATS that hold boolean value (i.e. 'Yes') are used instead of that value, because the value is alwayes positive (there is no FEAT such as 'Reflex=No').
    """
    attrs = {QName(i): attrs[i] for i in attrs}
    ud = {}
    non_ud = {}
    for i in attrs:
        if i.namespace == NS_UD:
            ud[i.localname] = attrs[i]
        else:
            non_ud[i] = attrs[i]
    ud = [(i, ud[i]) for i in FEAT_ORDER if i in ud]
    ud = [v if v != 'Yes' else k for k, v in ud]
    label = ".".join(ud)
    non_ud["msd"] = label
    return non_ud


def main(fp_in: str, fp_out: str) -> None:
    """Update the attributes of every words in a document."""
    x = etree.parse(fp_in)
    for i in x.findall(".//w", NS):
        attrs = ud_to_msd(i.attrib)
        i.attrib.clear()
        i.attrib.update(attrs)
    x.write(fp_out, encoding="utf-8")


if __name__ == "__main__":
    typer.run(main)

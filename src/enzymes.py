"""
A lightweight Python toolkit for simulating proteolytic cleavage of peptide sequences.
Cleavage rules for trypsin and chymotrypsin are implemented using rule-based string
processing to mimic enzymatic specificity in silico.
"""


def cleave(seq, *, cut_after, block_if_next=None):
    """
    This function split a peptide sequence into fragments based on cleavage rules

    Parameters:
    seq (str): Amino acid sequence
    cut after (set[str]): Residues where cleavage occurs on the C-terminal side
    block_if_next (set[str]): Residues that block cleavage if they appear
        immediately after a cut site

    Returns:
    list of strings, list of peptide fragments in order
    """
    cut_after = {str(x).upper() for x in cut_after}
    block_if_next = {str(x).upper() for x in block_if_next} if block_if_next else None

    segments = []
    start = 0

    for i in range(len(seq)):
        is_cut_residue = seq[i] in cut_after
        is_blocked = (
            (i + 1 < len(seq)) and block_if_next and (seq[i + 1] in block_if_next)
        )
        if is_cut_residue and not is_blocked:
            segments.append(seq[start : i + 1])
            start = i + 1
    if start < len(seq):
        segments.append(seq[start:])
    return segments


def trypsin_cleave(seq):
    """Cleave peptide after K or R, unless followed by P."""
    return cleave(seq, cut_after={"R", "K"}, block_if_next={"P"})


def chymotrypsin_cleave(seq):
    """Cleave peptide after Y, W, F, L, or M, unless followed by P."""
    return cleave(seq, cut_after={"Y", "W", "F", "L", "M"}, block_if_next={"P"})


if __name__ == "__main__":
    print(trypsin_cleave("KMKAFLRGYV"))
    print(chymotrypsin_cleave("AFYMWLGA"))

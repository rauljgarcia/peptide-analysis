"""
sequence_tools.py

This module provides tools for working with peptide fragments, including
validation of cleavage consistency and sequence reconstruction from ordered fragments.
Designed to complement the enzyme cleavage functions in enzymes.py.

Constants:
VALID_AMINO_ACIDS:
Set of the 20 canonical amino acid single-letter codes.
Used for validating peptide sequences and fragments in cleavage
and reconstruction workflows.

Note:
- This excludes ambiguous or non-standard residues like "X", "B", "Z".
- Extend this set if supporting additional amino acids or modifications.
"""

VALID_AMINO_ACIDS = {
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
}


def validate_ordered_fragments(
    fragments: list[str], *, cut_after: set[str], block_if_next: set[str]
) -> tuple[bool, dict]:

    for frag_index, frag in enumerate(fragments):
        for char_index, aa in enumerate(frag):
            if aa not in VALID_AMINO_ACIDS:
                return False, {
                    "error": "invalid character",
                    "fragment": frag,
                    "position": char_index,
                }


def reconstruct_from_ordered(fragments: list[str]) -> str:
    """
    Reconstructs a peptide sequence from an ordered list of fragments.

    Parameters:
    fragments : list[str]: List of peptide fragments (strings) in order.

    Returns:
    str: Full reconstructed peptide sequence.
    """
    pass


if __name__ == "__main__":
    print(
        validate_ordered_fragments(
            ["AK", "R", "MK", "YP"], cut_after={"K", "R"}, block_if_next={"P"}
        )
    )

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


def _validate_characters(
    fragment: str, valid_set: set[str], check_position: str
) -> tuple[bool, dict]:
    """
    Helper to validate characters in a fragment.
    check_position can be 'full', 'end', or 'start' to control what to check.
    Returns (True, {}) if valid, or (False, error_dict) if not.
    """
    pass


def validate_ordered_fragments(
    fragments: list[str], *, cut_after: set[str], block_if_next: set[str]
) -> tuple[bool, dict]:
    """
    Verifies valid fragments based on proper character for the amino acid, and valid
    cut-off points

    Parameters:
    fragments: list[str] — ordered fragments
    cut_after: set[str] — residues allowed at the end of each non-final fragment
    block_if_next: set[str] — residues not allowed at the start of the following fragment

    Returns:
    tuple[bool, dict] — (is_valid, details)
    dictionary: if False was returned, a message with the error type, and position
        if True, an empty error type and the number of fragments that passed
    """

    fragments = list(map(str.upper, fragments))
    cut_after = set(map(str.upper, cut_after))
    block_if_next = set(map(str.upper, block_if_next))

    if not fragments:
        return False, {"error": "empty_fragment_list"}

    # Check that each character in the fragment list is a valid amino acid
    for frag_index, frag in enumerate(fragments):
        if frag == "":
            return False, {
                "error": "empty fragment",
                "frag_index": frag_index,
                "fragment": "",
            }
        for char_index, amin_ac in enumerate(frag):
            if amin_ac not in VALID_AMINO_ACIDS:
                return False, {
                    "error": "invalid_character",
                    "char_index": char_index,
                    "residue": amin_ac,
                    "fragment": frag,
                }
    # Check that each fragment was cutoff after the appropriate amino acid
    for i, frag in enumerate(fragments[:-1]):
        if frag[-1] not in cut_after:
            return False, {
                "error": "invalid_cutoff",
                "frag_index": i,
                "residue": frag[-1],
                "fragment": frag,
            }
    # Check that no fragment begins with the block if next amino acid
    for i, frag in enumerate(fragments[1:]):
        if frag[0] in block_if_next:
            return False, {
                "error": "blocked_by_next",
                "frag_index": i + 1,
                "residue": frag[0],
                "fragment": frag,
            }
    return True, {
        "errors": [],
        "total_fragments": len(fragments),
        "checked_boundaries": len(fragments) - 1,
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

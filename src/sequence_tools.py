from collections.abc import Iterable
from typing import Optional

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


def _validate_residues(fragments: list[str]) -> tuple[bool, dict]:
    """Normalize and verify all fragments contain only valid amino acid residues."""
    if not fragments:
        # The list is empty
        return False, {"error": "empty_fragment_list"}

    normalized = []

    for frag_index, raw_frag in enumerate(fragments):
        frag = raw_frag.strip().upper()
        if frag == "":
            # The fragment is empty
            return False, {
                "error": "empty fragment",
                "fragment_index": frag_index,
            }

        for char_index, aa in enumerate(frag):
            if aa not in VALID_AMINO_ACIDS:
                return False, {
                    "error": "invalid_residue",
                    "residue_index": char_index,
                    "residue": aa,
                    "fragment": frag,
                }
        normalized.append(frag)

    return True, {"normalized": normalized, "total_fragments": len(normalized)}


def _validate_rule_set(rule_set: set[str], name: str) -> tuple[bool, dict]:
    for residue in rule_set:
        char = residue.strip().upper()
        if char not in VALID_AMINO_ACIDS:
            return False, {
                "error": "invalid_residue",
                "residue": char,
                "input_value": residue,
                "where": name,
            }
    return True, {"normalized": {r.strip().upper() for r in rule_set}}


def validate_ordered_fragments(
    fragments: list[str],
    *,
    cut_after: Iterable[str],
    block_if_next: Optional[Iterable[str]]
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
    # baseline residue validation
    ok, details = _validate_residues(fragments)
    if not ok:
        return False, details

    fragments = details["normalized"]

    # cut_after residue validation
    cut_after_ok, cut_after_details = _validate_rule_set(cut_after, name="cut_after")
    if not cut_after_ok:
        return False, cut_after_details
    cut_after = cut_after_details["normalized"]

    # block_if_next validation
    if block_if_next:
        block_ok, block_details = _validate_rule_set(
            block_if_next, name="block_if_next"
        )
        if not block_ok:
            return False, block_details
        block_if_next = block_details["normalized"]
    else:
        block_if_next = set()

    # check that last residue in each fragment is in the cut_after list
    for i, frag in enumerate(fragments[:-1]):
        if frag[-1] not in cut_after:
            return False, {
                "error": "invalid_cutoff",
                "char_index": len(frag) - 1,
                "fragment": frag,
                "frag_index": i,
                "residue": frag[-1],
            }

    # check that first residue in each fragment is not in the block_if_next list
    for i, frag in enumerate(fragments[1:]):
        if frag[0] in block_if_next:
            return False, {
                "error": "blocked_by_next",
                "char_index": 0,
                "fragment": frag,
                "frag_index": i + 1,
                "residue": frag[0],
            }

    return True, {
        "normalized_fragments": fragments,
        "normalized_cut_after": cut_after,
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

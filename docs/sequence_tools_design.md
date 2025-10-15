### Helper Function Build
```
1) A single helper for the whole list

Name/role: _normalize_and_validate_fragments  
Purpose: Take the entire fragments list, normalize each item, and verify every character is a valid amino acid. Do this once, up front.

**Inputs**  
- fragments: list[str]  
- (No enzyme rules here—this helper is rule-agnostic.)

**Processing (in order)**
1. If the list is empty → fail (empty_fragment_list).  
2. For each fragment:
* strip() and upper()
* If empty after strip → fail (empty_fragment, include frag_index)
* Scan chars left→right; on first invalid char → fail (invalid_character, include frag_index, char_index, residue)
3. If all pass, return the normalized list.

**Outputs**
* On success: (True, {"normalized": <list[str]>, "total_fragments": n})
* On failure: (False, {"error": <code>, ...context keys...})

**Key idea:** this helper returns the clean, normalized fragments so your main validator doesn’t have to normalize again or re-scan characters.

2) Main validator flow (high level)

Inside validate_ordered_fragments:
1. Normalize rule sets once at the top (uppercased).
2. Call the helper once:
* If it fails → return that failure as-is.
* If it succeeds → replace fragments with the returned normalized list.
3. Boundary pass (two lightweight checks):
* Cut-after: for each fragment except the last, check last residue ∈ cut_after.
* On fail → invalid_cutoff with frag_index, residue, fragment
* Blocked-by-next: for each fragment from index 1 onward, check first residue ∉ block_if_next.
* On fail → blocked_by_next with frag_index (i+1 due to slicing), residue, fragment
4. Success return: True with a small summary (e.g., total_fragments, checked_boundaries).


3) Error codes and fields (keep them consistent)
* empty_fragment_list
* empty_fragment (frag_index)
* invalid_character (frag_index, char_index, residue)
* invalid_cutoff (frag_index, residue, fragment)
* blocked_by_next (frag_index, residue, fragment)

4) Tiny decisions to lock in
* Rule-set normalization: Uppercase cut_after and block_if_next in the main validator (not in the helper), since the helper is rule-agnostic.
* Whitespace policy: The helper does strip() + upper() on every fragment. That ensures boundary checks work with clean strings.
* Empty block_if_next: Treat as “no blockers” (the blocked-by-next loop just never trips).

5) Micro test plan (to run right after you wire it)
* [] → empty_fragment_list
* [""] → empty_fragment at frag_index=0
* ["AXA"] → invalid_character at char_index=1, residue X
* Trypsin rules (cut_after={R,K}, block_if_next={P}):
* ["MAGWR", "K", "TPY"] → valid
* ["AK", "PAAA"] → blocked_by_next at frag_index=1, residue P
* ["AKA", "AAA"] → invalid_cutoff at frag_index=0, residue A
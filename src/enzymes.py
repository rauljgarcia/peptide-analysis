'''
enzymes.py

Contains functions for peptide cleavage by proteases.
Currently supports trypsin cleavage.
'''

def cleave(seq, *, cut_after, block_if_next=None, case="upper"):
    '''
    This function split a peptide sequence into fragments based on cleavage rules

    Parameters:
    seq (str): Amino acid sequence
    cut after (set[str]): Residues where cleavage occurs on the C-terminal side
    block_if_next (set[str]): Residues that block cleavage if they appear 
        immediately after a cut site
    
    Returns:
    list of strings, list of peptide fragments in order
    '''
    pass

def trypsin_cleave(ply_pep):
    '''
    Cleaves a peptide sequence according to trypsin rules.

        Trypsin cleaves on the C-terminal side of 'K' (Lysine) or 'R' (Arginine),
        except when followed by 'P' (Proline).

        Parameters:
        ply_pep (str):
            Input peptide sequence (string of one-letter amino acid codes).

        Returns:
        list of str
            Peptide fragments produced by trypsin cleavage.
    '''
    ply_pep = ply_pep.upper()
    segs = []
    start = 0
    for i in range(len(ply_pep)):
        if (
            ply_pep[i] in {"R", "K"} 
            and (i+1 == len(ply_pep) or ply_pep[i+1] != "P")
        ):
            segs.append(ply_pep[start:i+1])
            start = i+1
    if start < len(ply_pep):
        segs.append(ply_pep[start:])
    return segs

def main():
    print(trypsin_cleave("KMKAFLRGYV"))
if __name__ == "__main__":
    main()
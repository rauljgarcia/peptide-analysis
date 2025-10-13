Peptide Analysis — in silico Edman Degradation Simulation

This project is a Python-based toolkit for modeling protease cleavage and sequence reconstruction, inspired by the classical Edman degradation method for peptide sequencing.
It is designed to evolve into a more complete simulation pipeline capable of selecting peptides from a database, cleaving them using defined enzymatic rules, and attempting to reconstruct the original sequences computationally.

Current Functionality
• Protease cleavage
Functions that simulate enzymatic cleavage patterns (e.g., trypsin, chymotrypsin).

• Fragment validation
Logic to ensure that cleavage fragments contain valid amino acid residues and follow expected boundary rules (cut_after, block_if_next).

• Sequence reconstruction (in progress)
Planned functions to rebuild sequences from ordered fragment lists and verify their consistency.

• Notebook-based testing
Interactive Jupyter notebooks allow for quick validation of logic, visualization of steps, and iterative development.

⸻

Project Vision

Ultimately, this tool aims to:
1. Access a database containing thousands of known peptides.
2. Randomly select sequences for in silico cleavage.
3. Simulate Edman degradation steps.
4. Reconstruct full sequences from fragments.
5. Compare reconstructed sequences to the originals to assess accuracy and robustness of the reconstruction algorithm.

This framework could be extended to explore:
• Effects of incomplete cleavage
• Noise/error simulation
• Integration with MS-based approaches

## Project Structure
```
peptide-analysis/
│
├── notebooks/
│   ├── 01_protease_cleavage.ipynb        # Exploratory cleavage testing
│   └── 02_reconstruction_testing.ipynb   # Fragment validation & reconstruction logic
│
├── src/
│   ├── enzymes.py                        # Enzymatic cleavage functions
│   └── sequence_tools.py                 # Fragment validation & reconstruction
│
├── .gitignore
└── README.md
```

## Example Usage
```
from src.enzymes import trypsin_cleave
from src.sequence_tools import validate_ordered_fragments

# Example peptide
peptide = "MAGWRKTPY"

# Cleave
fragments = trypsin_cleave(peptide)

# Validate
is_valid, details = validate_ordered_fragments(
    fragments,
    cut_after={"R", "K"},
    block_if_next={"P"}
)
print(is_valid, details)
```

Roadmap
• Core cleavage functions
• Amino acid residue validation
• Fragment boundary validation rules
• Sequence reconstruction logic
• Database integration for peptide selection
• Reconstruction accuracy scoring and reporting
• Optional error simulation layer

 Development Notes
• This project is structured for incremental, test-driven development through Jupyter notebooks.
• Scratch notebooks are ignored via .gitignore to keep the repo clean.
• Code modules in src/ are written to be reusable and independently testable.


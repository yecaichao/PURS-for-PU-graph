<img width="1089" height="558" alt="image" src="https://github.com/user-attachments/assets/77131222-ff7c-46d7-b5d4-1488e8abb9c3" />


1.High throughput identification of polymer-units(repeating units) from SMILES codes of polymers

2.GNN models based on polymer-unit - Model acceleration and interpretative enhancement

## PURS for PU-graph v1.1

This release provides a package for polymer-unit recognition and the associated PU-based learning workflows.

### Included in this package
- Core PURS recognition workflow
- Sample input file: `test.csv`
- Packaged `PU-gn-exp` workflow
- Packaged `PU-MPNN` workflow
- Installation guide: `INSTALL.md`
- Reproducible environment file: `environment_purs.yml`

### Main improvements
- Fixed duplicate-name handling so repeated sample names no longer overwrite each other
- Improved robustness of molecule embedding with fallback coordinate generation
- Reduced repeated lookup overhead in several hot paths
- Added packaged sample input and quick-start instructions
- Vendored the minimal helper modules required by `PU-gn-exp`
- Vendored the minimal utility code required by `PU-MPNN`
- Added compatibility fixes for newer PyTorch and TensorFlow runtime stacks
- Cleaned package-level documentation and user-facing workflow descriptions

### Installation
Please follow:
- `INSTALL.md`
- `environment_purs.yml`

### Notes
- `PU-gn-exp` depends on `torchgraphs`, which is installed from GitHub through the provided environment file.
- `PU-MPNN` requires TensorFlow, RDKit, NumPy, scikit-learn, and sparse, also covered by the provided environment file.


## When using PURS in your research PLEASE cite the paper:  
[1] Xinyue Zhang, Ye Sheng, Xiumin Liu, Jiong Yang, William A. Goddard III, Caichao Ye*, Wenqing Zhang*. Polymer-unit Graph: Advancing Interpretability in Graph Neural Network Machine Learning for Organic Polymer Semiconductor Materials. J. Chem. Theory Comput., 2024, 20(7), 2908-2920.  
[2] Xinyue Zhang, Genwang Wei, Ye Sheng, Wenjun Bai, Jiong Yang, Wenqing Zhang*, Caichao Ye*. Polymer-Unit Fingerprint (PUFp): An Accessible Expression of Polymer Organic Semiconductors for Machine Learning. ACS Appl. Mater. Interfaces, 2023, 15(17), 21537–21548.  
[3] Caichao Ye, Tao Feng, Weishu Liu*, Wenqing Zhang*. Functional Unit: A New Perspective on Materials Science Research Paradigms. Acc. Mater. Res., 2025, 6(8), 914-920.

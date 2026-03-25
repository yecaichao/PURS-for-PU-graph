# Python-based-polymer-unit-recognition-script-PURS-2.0
<img width="1089" height="558" alt="image" src="https://github.com/user-attachments/assets/77131222-ff7c-46d7-b5d4-1488e8abb9c3" />


1.High throughput identification of polymer-units(repeating units) from SMILES codes of polymers

2.GNN models based on polymer-unit - Model acceleration and interpretative enhancement

## Installation
#### 1.Use only the recognition function
```
conda create -n PURS
conda activate PURS
pip install -r requirements.yml
```

For a validated full-package environment and deployment steps, see `INSTALL.md`
and `environment_purs.yml`.

#### Sample input
`test.csv` is included in the package as a runnable example input file.
It has been verified locally with the recognition workflow in `PURS.py`.

#### Quick start
Run the recognition workflow with:
```bash
python -c "import PURS; PURS.main('test.csv')"
```
#### 2.Interpretable GNNS based on polymer-units--PU-gn-exp

PU-gn-exp is included in this package with the minimal helper modules vendored locally.
You do not need to clone the original `graph-network-explainability` repository just to run the packaged workflow.
You still need its runtime dependencies such as `torchgraphs`, `tensorboardX`, `munch`, and `pyaml`.

#### 3.Prediction model based on polymer-unit--PU-MPNN
PU-MPNN is included in this package with the required baseline utility code vendored locally.
You do not need to clone the original `mol_mpnn` repository just to run the packaged workflow.
You still need the runtime stack used by this branch, especially TensorFlow, RDKit, NumPy, scikit-learn, and sparse.

## When using PURS in your research PLEASE cite the paper:  
[1] Xinyue Zhang, Ye Sheng, Xiumin Liu, Jiong Yang, William A. Goddard III, Caichao Ye*, Wenqing Zhang*. Polymer-unit Graph: Advancing Interpretability in Graph Neural Network Machine Learning for Organic Polymer Semiconductor Materials. J. Chem. Theory Comput., 2024, 20(7), 2908-2920.  
[2] Xinyue Zhang, Genwang Wei, Ye Sheng, Wenjun Bai, Jiong Yang, Wenqing Zhang*, Caichao Ye*. Polymer-Unit Fingerprint (PUFp): An Accessible Expression of Polymer Organic Semiconductors for Machine Learning. ACS Appl. Mater. Interfaces, 2023, 15(17), 21537–21548.  
[3] Caichao Ye, Tao Feng, Weishu Liu*, Wenqing Zhang*. Functional Unit: A New Perspective on Materials Science Research Paradigms. Acc. Mater. Res., 2025, 6(8), 914-920.

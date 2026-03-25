PU-MPNN

Overview
This folder contains the packaged PU-MPNN variant together with the minimal utility code required to run it without cloning the original mol_mpnn repository.

Workflow
1. Prepare the MPNN input data following preprocessing_pu.ipynb or an equivalent scripted preprocessing flow.
2. Activate the packaged environment described in the repository-level INSTALL.md and environment_purs.yml.
3. Run training from the pu-mpnn/pu-mpnn directory:
   python train.py

Notes
- This branch requires TensorFlow, RDKit, NumPy, scikit-learn, and sparse.
- preprocessing_pu.ipynb is included as a reference workflow.
- The release_check_* scripts are intended for internal validation only and do not need to be shipped in an end-user release.

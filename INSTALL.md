# Installation and Deployment

This package has been checked locally with the environment defined in
`environment_purs.yml`.

## 1. Create the environment

```bash
conda env create -f environment_purs.yml
conda activate purs-review-py39
```

If the environment already exists:

```bash
conda activate purs-review-py39
```

## 2. Run the core PURS recognition workflow

The package ships with a validated sample input file:

```bash
python -c "import PURS; PURS.main('test.csv')"
```

## 3. PU-gn-exp

The package now vendors the minimal helper modules that were previously taken
from the original `graph-network-explainability` baseline, so you do not need
to clone that repository just to run the packaged workflow.

Expected csv columns:

- `Compound ID`
- `PCE_max`
- `smiles`

Run training from the `pu-gn-exp/pu-gn-exp` directory:

```bash
python -m polymer_unit.train --experiment polymer_unit/train.yaml
```

Run prediction from the same directory:

```bash
python -m polymer_unit.predict --model path/to/experiment.latest.yaml --data path/to/data.csv --options batch_size=2 --output path/to/output_dir
```

## 4. PU-MPNN

The package now vendors the minimal utility code that was previously taken from
the original `mol_mpnn` baseline, so you do not need to clone that repository
just to run the packaged workflow.

This branch still requires TensorFlow and uses the preprocessing flow from the
packaged `preprocessing_pu.ipynb` / helper scripts.

The release-check helpers included in `pu-mpnn/pu-mpnn` are:

- `release_check_prepare.py`
- `release_check_train.py`

They are mainly for local validation and regression testing.

## 5. Recommended files to include in a release package

- `PURS.py`
- `README.md`
- `INSTALL.md`
- `environment_purs.yml`
- `test.csv`
- `pu-gn-exp/`
- `pu-mpnn/`

## 6. Notes

- The package was validated in a Windows environment.
- Some RDKit and TensorFlow file operations are more reliable when temporary
  outputs are written to ASCII-only paths.
- `PU-gn-exp` depends on `torchgraphs`, which is installed from GitHub through
  the environment file.

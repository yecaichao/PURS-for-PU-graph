PU-gn-exp

Training
1. Prepare a csv file with at least these columns: Compound ID, PCE_max, smiles.
2. Activate the packaged environment described in the repository-level INSTALL.md and environment_purs.yml.
3. Run training from the pu-gn-exp/pu-gn-exp directory:
   python -m polymer_unit.train --experiment polymer_unit/train.yaml
4. Trained checkpoints will be written to the output folder defined in the yaml config.

Prediction
1. Run prediction from the same directory:
   python -m polymer_unit.predict --model path/to/experiment.latest.yaml --data path/to/data.csv --options batch_size=2 --output path/to/output_dir

Notes
- The packaged version already vendors the minimal helper modules required from the original gn-exp baseline.
- You still need runtime dependencies such as torchgraphs, tensorboardX, munch, and pyaml.
- polymer_unit.ipynb is optional and mainly intended for exploratory work.

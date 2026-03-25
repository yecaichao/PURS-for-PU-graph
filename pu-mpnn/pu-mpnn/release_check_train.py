#!/usr/bin/env python
import pickle as pkl
from pathlib import Path
import tempfile

import numpy as np
from sklearn.preprocessing import StandardScaler

from MPNN import Model


def main():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "DATA" / "genwl3.pkl"
    save_path = Path(tempfile.gettempdir()) / "purs_release_check_model.ckpt"

    with data_path.open("rb") as f:
        DV, DE, DP, DY, Dsmi = pkl.load(f)

    DV = np.asarray(DV.todense(), dtype=np.float32)
    DE = np.asarray(DE.todense(), dtype=np.float32)
    DP = np.expand_dims(np.asarray(DP, dtype=np.float32), 3)

    scaler = StandardScaler()
    DY = scaler.fit_transform(DY).astype(np.float32)

    if len(DY) < 4:
        raise ValueError(f"Need at least 4 samples for the release check, got {len(DY)}")

    split = max(2, len(DY) - 2)
    DV_trn = DV[:split]
    DE_trn = DE[:split]
    DP_trn = DP[:split]
    DY_trn = DY[:split]

    DV_val = DV[split:]
    DE_val = DE[split:]
    DP_val = DP[split:]
    DY_val = DY[split:]

    n_max = DV.shape[1]
    dim_node = DV.shape[2]
    dim_edge = DE.shape[3]
    dim_atom = 19
    dim_y = DY.shape[1]

    model = Model(n_max, dim_node, dim_edge, dim_atom, dim_y, batch_size=2, useGPU=False)
    with model.sess:
        model.train(
            DV_trn,
            DE_trn,
            DP_trn,
            DY_trn,
            DV_val,
            DE_val,
            DP_val,
            DY_val,
            load_path=None,
            save_path=save_path.as_posix(),
            max_epoch=2,
        )
        mae = model.test_mae(DV_val, DE_val, DP_val, DY_val, 1)

    print("saved", save_path.as_posix())
    print("val_mae", mae)


if __name__ == "__main__":
    main()

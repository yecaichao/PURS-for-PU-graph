#!/usr/bin/env python
import csv
import pickle as pkl
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd
import sparse
from rdkit import Chem
from sklearn.metrics.pairwise import euclidean_distances

from API import get_mpnn_input, bondFeatures2


def build_release_check_csv(src_csv: Path, dst_csv: Path, limit: int = 12):
    df = pd.read_csv(src_csv).head(limit).copy()
    df["target"] = np.arange(len(df), dtype=np.float64)
    df = df[["name", "smiles", "target"]]
    df.to_csv(dst_csv, index=False)
    return df


def build_graph_pkl(csv_path: Path, sdf_path: Path, out_path: Path):
    feature_df = pd.read_csv(csv_path)
    index_dict, pu_dict, pair_atom_dict, adj_list, pu_feature, structure, n_max, dim_node = get_mpnn_input(
        csv_path.as_posix(), sdf_path.as_posix()
    )
    pu_feature_df = pd.DataFrame(pu_feature)

    dim_edge = 8
    DV = []
    DE = []
    DP = []
    DY = []
    Dsmi = []

    for i, mol in enumerate(structure):
        if mol is None:
            continue
        try:
            Chem.SanitizeMol(mol)
        except Exception:
            continue

        name = mol.GetProp("_Name")
        if name not in pu_dict:
            continue

        smi = Chem.MolToSmiles(mol)
        if "." in smi:
            continue

        num_index = list(pu_dict[name].values())
        num_node = len(num_index)
        node_name = list(pu_dict[name].keys())
        pair_atom = pair_atom_dict[name]
        adj = adj_list[i]
        rings = mol.GetRingInfo().AtomRings()

        node = np.zeros((n_max, dim_node), dtype=np.int8)
        for j in range(num_node):
            index = num_index[j]
            node[j, :] = pu_feature_df.loc[index].to_numpy(dtype=np.int8)

        pos = mol.GetConformer().GetPositions()
        pos_array = np.array(pos)
        node_ave = []
        for j in range(num_node):
            index = node_name[j]
            atom_num = index_dict[name][index]
            ave_pos = pos_array[atom_num].mean(axis=0)
            node_ave.append(ave_pos)
        node_pos = np.array(node_ave)
        proximity = np.zeros((n_max, n_max), dtype=np.float32)
        proximity[:num_node, :num_node] = euclidean_distances(node_pos)

        target = feature_df.loc[feature_df["name"] == name, ["target"]].iloc[0].to_numpy(dtype=np.float64)

        edge = np.zeros((n_max, n_max, dim_edge), dtype=np.float32)
        pair_lookup = {}
        for pair_idx, pair_name in enumerate(pair_atom["pair_index"]):
            pair_lookup[tuple(pair_name)] = pair_atom["pair_atom"][pair_idx]

        for j in range(num_node):
            for k in range(num_node):
                if adj[j, k] != 1:
                    continue
                j_name = node_name[j]
                k_name = node_name[k]
                j_index = num_index[j]
                k_index = num_index[k]
                pair = pair_lookup.get((j_name, k_name))
                if pair is None:
                    pair = pair_lookup.get((k_name, j_name))
                if pair is None:
                    continue
                edge[j, k, :6] = bondFeatures2(pos, pair[0], pair[1], mol, rings)
                edge[j, k, 6] = j_index * 0.01
                edge[j, k, 7] = k_index * 0.01
                edge[k, j, :] = edge[j, k, :]

        DV.append(node)
        DE.append(edge)
        DP.append(proximity)
        DY.append(target)
        Dsmi.append(smi)

    DV = sparse.COO.from_numpy(np.asarray(DV, dtype=np.int8))
    DE = sparse.COO.from_numpy(np.asarray(DE, dtype=np.float32))
    DP = np.asarray(DP, dtype=np.float32)
    DY = np.asarray(DY, dtype=np.float64)
    Dsmi = np.asarray(Dsmi)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as fw:
        pkl.dump([DV, DE, DP, DY, Dsmi], fw)

    print("saved", out_path.as_posix())
    print("shapes", DV.shape, DE.shape, DP.shape, DY.shape)


def main():
    repo_root = Path(__file__).resolve().parents[2]
    src_csv = repo_root / "test.csv"
    work_csv = Path(__file__).resolve().parent / "release_check.csv"
    work_sdf = Path(tempfile.gettempdir()) / "purs_release_check.sdf"
    out_pkl = Path(__file__).resolve().parent / "DATA" / "genwl3.pkl"

    build_release_check_csv(src_csv, work_csv)
    build_graph_pkl(work_csv, work_sdf, out_pkl)


if __name__ == "__main__":
    main()

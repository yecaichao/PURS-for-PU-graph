#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pickle as pkl
import csv, sys
from util import _permutation
from MPNN import Model
from sklearn.preprocessing import StandardScaler
import tensorflow.compat.v1 as tf
#import keras.backend as K
import os
import math

tf.disable_v2_behavior()



def get_flops(model):
    run_meta = tf.RunMetadata()
    opts = tf.profiler.ProfileOptionBuilder.float_operation()

    # We use the Keras session graph in the call to the profiler.
    flops = tf.profiler.profile(graph=K.get_session().graph,
                                run_meta=run_meta, cmd='op', options=opts)

    return print("total_float_ops: %e"%flops.total_float_ops)# Prints the "flops" of the model.



def stats_graph(graph):
    flops = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.float_operation())
    params = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.trainable_variables_parameter())
    
    print('FLOPs: {};    Trainable params: {}'.format(flops.total_float_ops, params.total_parameters))

n_max=20
dim_node=280
dim_edge=8
atom_list=['Se','H','Li','B','C','N','O','F','Na','Mg','Si','P','S','Cl','K','Ca','Br','Bi','Ge']

data_path = './DATA/genwl3.pkl'
save_path = './MPNN_model_p.ckpt'

#print(':: load data')
with open(data_path,'rb') as f:
    [DV, DE, DP, DY, Dsmi] = pkl.load(f)

DV = np.asarray(DV.todense(), dtype=np.float32)
DE = np.asarray(DE.todense(), dtype=np.float32)
DP = np.expand_dims(np.asarray(DP, dtype=np.float32), 3)

scaler = StandardScaler()
DY = scaler.fit_transform(DY).astype(np.float32)

dim_atom = len(atom_list)
dim_y = DY.shape[1]

#print(':: preprocess data')
np.random.seed(134)
[DV, DE, DP, DY, Dsmi] = _permutation([DV, DE, DP, DY, Dsmi])
batch_size=8
def get_data(path,batch_size):

    with open(path,'rb') as f:
        [DV_pre, DE_pre, DP_pre, DY_pre, Dsmi_pre] = pkl.load(f)
    DV_pre = np.asarray(DV_pre.todense(), dtype=np.float32)
    DE_pre = np.asarray(DE_pre.todense(), dtype=np.float32)
    DP_pre = np.expand_dims(np.asarray(DP_pre, dtype=np.float32), 3)
    #DY_pre = scaler.fit_transform(DY_pre)
    [DV_pre, DE_pre, DP_pre, DY_pre, Dsmi_pre] = _permutation([DV_pre, DE_pre, DP_pre, DY_pre, Dsmi_pre])
    minus_num = len(DY_pre)-len(DY_pre)%batch_size
    DV_pre = DV_pre[:minus_num]
    DE_pre = DE_pre[:minus_num]
    DP_pre = DP_pre[:minus_num]
    DY_pre = DY_pre[:minus_num]
    Dsmi_pre = Dsmi_pre[:minus_num]

    return DV_pre, DE_pre, DP_pre, DY_pre, Dsmi_pre

default_num1 = 633
default_num2 = 64
if len(DY) >= default_num1 + default_num2:
    num1 = default_num1
    num2 = default_num2
else:
    num2 = max(1, int(round(len(DY) * 0.1)))
    num1 = max(1, len(DY) - num2)
DV_trn = DV[:num1]
DE_trn = DE[:num1]
DP_trn = DP[:num1]
DY_trn = DY[:num1]
    
DV_val = DV[num1:num2+num1]
DE_val = DE[num1:num2+num1]
DP_val = DP[num1:num2+num1]
DY_val = DY[num1:num2+num1]

model = Model(n_max, dim_node, dim_edge, dim_atom, dim_y)
with model.sess:
    load_path=None
    print(model)
    #model.train(DV_trn, DE_trn, DP_trn, DY_trn, DV_val, DE_val, DP_val, DY_val, load_path, save_path)

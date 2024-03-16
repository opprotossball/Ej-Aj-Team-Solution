from utils import model_stealing_submission
from taskdataset import TaskDataset
import numpy as np
import torch
import matplotlib.pyplot as plt
from augmentation import augment
from labeldict import LabelDict

if __name__ == '__main__':
    # lbls = [10, 9, 8, 1, 3, 4, 3, 8, 1, 9]
    # dct = LabelDict(lbls)
    # codes = dct.labels2codes(lbls)
    # print(codes)
    # print(dct.codes2labels(codes))

    d = torch.load('../data/ModelStealingPub.pt')
    # lst = []
    # for l in d.labels:
    #     if l not in lst:
    #         lst.append(l)
    # print(len(lst))

    #res = augment(d, 2)
    dct = LabelDict(d.labels)
    seen = []
    for i, v in enumerate(dct.codes2labels_dct):
        print(f'{i} -> {v}')
        if v in seen:
            print("INC")
            print(v)
        seen.append(v)

    # from tensorflow.python.client import device_lib 
    # print(device_lib.list_local_devices())

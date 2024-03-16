from utils import model_stealing_submission
from taskdataset import TaskDataset
import numpy as np
import torch
import matplotlib.pyplot as plt
from augmentation import augment
from labeldict import LabelDict

if __name__ == '__main__':
    lbls = [10, 9, 8, 1, 3, 4, 3, 8, 1, 9]
    dct = LabelDict(lbls)
    codes = dct.labels2codes(lbls)
    print(codes)
    print(dct.codes2labels(codes))
    # d = torch.load('../data/ModelStealingPub.pt')
    # res = augment(d, 10)
    # print(len(d.imgs))
    # print(len(res[0]))

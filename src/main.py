from utils import model_stealing_submission
from taskdataset import TaskDataset
import numpy as np
import torch
import matplotlib.pyplot as plt
from augmentation import augment

if __name__ == '__main__':
    d = torch.load('../data/ModelStealingPub.pt')
    res = augment(d, 10)
    print(len(d.imgs))
    print(len(res[0]))

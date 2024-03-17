from utils import model_stealing_submission, model_stealing
from taskdataset import TaskDataset
import numpy as np
import torch
import matplotlib.pyplot as plt
from augmentation import augment
from labeldict import LabelDict
import random
import os
import json

def select_samples(dataset, n):
    data = list(zip(dataset.imgs, dataset.labels))
    imgs = []
    lbls = []
    random.shuffle(data)
    present = {}
    for img, lbl in data:
        if lbl not in present:
            present[lbl] = 1
        if present[lbl] <= n:
            present[lbl] = present[lbl] + 1
            imgs.append(img)
            lbls.append(lbl)
    return imgs, lbls        

def steal(img):
    img.save('img.png', 'PNG')
    res = model_stealing('img.png')
    os.unlink('img.png')
    print(type(res))
    return np.array(img.convert('RGB')), res

def save(imgs, reprs, path):
    data = {'images': [], 'representations': []}
    for image, representation in zip(imgs, reprs):
        data['images'].append(image.tolist()) 
        data['representations'].append(representation)
    with open(path, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    d = torch.load('../data/ModelStealingPub.pt')
    imgs, lbls = select_samples(d, 3)
    samples = list(zip(imgs, lbls))
    resimgs = []
    resreprs = []
    i = 0
    for s in samples:
        img, reprs = steal(s[0]) 
        resimgs.append(img)
        resreprs.append(reprs)
        i += 1
        print(f'{i} stolen')
    save(resimgs, resreprs, 'test.json')
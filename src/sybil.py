import torch
from taskdataset import TaskDataset
import json
import random
import os
from boilerplate import sybil

def select_samples(dataset, n):
    samples = list(zip(dataset.ids, dataset.imgs, dataset.labels))
    ids = []
    lbls = []
    random.shuffle(samples)
    present = {}
    for s in samples:
        lbl = s[2]
        if lbl not in present:
            present[lbl] = 1
        if present[lbl] <= n:
            present[lbl] = present[lbl] + 1
            ids.append(s[0])
            lbls.append(lbl)
    return ids, lbls        

#    return np.array(img.convert('RGB')), res

def save(ids, reprs, path):
    data = {'ids': [], 'representations': []}
    for image, representation in zip(ids, reprs):
        data['ids'].append(image.tolist()) 
        data['representations'].append(representation)
    with open(path, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    dataset = torch.load("../data/SybilAttack.pt")
    ids, lbls = select_samples(dataset, 36)
    repres = sybil(ids, 'defense', 'affine')
    
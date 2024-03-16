from imgaug import augmenters as iaa
import random
import numpy as np
import matplotlib.pyplot as plt

def augment(dataset, n):
    aug = iaa.Sequential([
        iaa.Fliplr(p=0.5),
        iaa.Flipud(p=0.5),
        iaa.AddToHueAndSaturation((-20, 20)), 
        iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 0.5))),
    ])
    imgarr = np.array([np.array(img.convert('RGB')) for img in dataset.imgs])
    all_augmented_imgs = [aug(images=imgarr) for _ in range(n)]
    all_augmented_imgs.append(imgarr)  
    augmented_imgs = np.concatenate(all_augmented_imgs, axis=0)
    labels = np.tile(dataset.labels, n + 1)
    return augmented_imgs, [int(l) for l in labels]

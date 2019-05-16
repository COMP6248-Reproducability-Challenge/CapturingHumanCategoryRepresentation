import math

import torch
import numpy as np
import matplotlib
# from PIL import Image
# import cv2
import matplotlib.pyplot as plt

from generator import Generator

ngpu = 1
nz = 100
ngf = 64
nc = 3

sd_1 = 0.25
sd_2 = 2
p = 0.5

netG = Generator(ngpu, nz, ngf, nc)

state = torch.load('./weights/G/epoch_99', map_location='cpu')
netG.load_state_dict(state)
netG.eval()

def generate(z):
    z = torch.tensor(z)
    with torch.no_grad():
        sample = netG(z.float())

    max = torch.max(sample)
    min = torch.min(sample)
    # print(max)
    # print(min)
    diff = max - min
    sample = (sample - min) / diff

    img = sample[0].detach().numpy()

    # sample = sample[0]
    # for channel in range(3):
    #     max = torch.max(sample[channel])
    #     min = torch.min(sample[channel])
    #     diff = max - min
    #     sample[channel,:,:] = (sample[channel,:,:] - min) / diff
    # img = sample.detach().numpy()

    return np.moveaxis(img, 0, 2)

def noise():
    return torch.randn(1, nz, 1, 1)

def wrap(z):
    if abs(z) < 1:
        return z
    else:
        return -np.sign(z) * (1 - (z - math.floor(z)))

def mutate(z):
    if np.random.uniform() < p:
        noise = np.random.normal(0, sd_1, (1, 100, 1, 1))
    else:
        noise = np.random.normal(0, sd_2, (1, 100, 1, 1))
    print(z.shape)
    print(noise.shape)

    return np.vectorize(wrap)(z + noise)

def save_image(img, name):
    # print((img * 255).astype(int))
    # im = Image.fromarray((img * 255).astype(int))
    # im.save(name)
    # cv2.imwrite(name, (img * 255).astype(int))
    plt.imsave(name, img)

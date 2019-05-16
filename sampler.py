import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2

from generator import Generator

ngpu = 1
nz = 100
ngf = 64
nc = 3

netG = Generator(ngpu, nz, ngf, nc)

# state = torch.load('./weights/G/2/epoch_199', map_location='cpu')
state = torch.load('./weights/G/epoch_99', map_location='cpu')
netG.load_state_dict(state)
netG.eval()

def wrap(z):
    if abs(z) < 1:
        return z
    else:
        return -np.sign(z) * (1 - (z - np.floor(z)))

# z = torch.tensor(np.random.uniform(-1, 1, (1, 100)))
b_size = 1
# noise = torch.randn(b_size, nz, 1, 1)
noise = np.vectorize(wrap)(np.random.normal(0, 1, (1, 100, 1, 1)))
noise = torch.tensor(noise).float()
print(noise.shape)

with torch.no_grad():
	sample = netG(noise)

# max = torch.zeros(3)
# min = torch.zeros(3)

'''
for i in range(3):
	max = torch.max(sample[0,i])
	min = torch.min(sample[0,i])
	range = max - min
	sample[0,i,:,:] = (sample[0,i,:,:] - min)/range
	
	print(torch.max(sample[0,i]))
	print(torch.min(sample[0,i]))

'''
max = torch.max(sample)
min = torch.min(sample)
range = max - min
sample = (sample - min)/range

img = sample[0].detach().numpy()
img = np.moveaxis(img, 0, 2)
# img = (img * 255).astype(int)
# cv2.imwrite('testing_cv2.jpg', img)
# plt.imsave('testing_plt.jpg', img)
# print(img)

plt.imshow(img)
plt.show()



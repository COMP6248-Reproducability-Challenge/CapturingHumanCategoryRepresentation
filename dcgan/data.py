import numpy as np
from joblib import load

import markov

def load_chain (type, id):
    loaded = True
    ch = None
    ind = 1
    while loaded:
        try:
            ch = load('chain_data/{}/chain_{}/{}'.format(type, id, ind * 100))
            print('Loaded chain:', '{}/chain_{}/{}'.format(type, id, ind * 100))
            ind += 1
        except FileNotFoundError:
            loaded = False

    return ch


n_chains = 4
chain_types = ['Man', 'Woman', 'Happy', 'Sad']
chains = {}

image_grid = np.zeros((64*4, 64*4, 3))

accepted = 0
total = 0

for t, type in enumerate(chain_types):
    for c in range(n_chains):
        chain_key = '{}/{}'.format(type, c)
        chain = load_chain(type, c)
        chains[chain_key] = chain

        chain_z_unique = np.zeros((0, 100, 1, 1))
        chain_z = chain.z_vals
        print(chain_z[0:1].shape)
        chain_z_unique = np.append(chain_z_unique, chain_z[0:1], axis=0)


        for i in range(1, len(chain)):
            if not np.array_equal(chain_z[i],chain_z_unique[-1]):
                chain_z_unique = np.append(chain_z_unique, chain_z[i:i+1], axis=0)
        
        total += chain_z.shape[0]
        accepted += chain_z_unique.shape[0]

        chain_z_avg = np.average(chain_z_unique, axis=0)
        chain_z_avg = np.expand_dims(chain_z_avg, axis=0)
        # print(chain_z_unique.shape)
        # print(chain_z_avg.shape)
        chain_avg = np.average(chain_z, axis=0)
        chain_avg = np.expand_dims(chain_avg, axis=0)

        img = markov.generate(chain_avg)

        image_grid[(64 * t):64 * (t+1), (64 * c):64 * (c+1)] = img

# markov.save_image(image_grid, 'image_grid_1.png')
print(accepted)
print(total)
print(accepted/total)
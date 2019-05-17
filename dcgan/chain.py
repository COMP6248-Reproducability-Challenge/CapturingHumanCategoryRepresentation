import numpy as np

class Chain():
    def __init__(self, id, type, z_dim=100):
        self.id = id
        self.type = type
        self.z_vals = np.zeros((0, z_dim, 1, 1))
        self.image_names = []
        self.proposal_z = None
        self.proposal_image = None

    def get_image(self):
        return self.image_names[-1]

    def get_z(self):
        return self.z_vals[-1,:,:,:]

    def add_link(self, z_val, image_name):
        # z_val = np.squeeze(z_val, axis=(2, 3))
        # print(np.squeeze(z_val, axis=(2, 3)).shape)
        print(self.z_vals.shape)
        self.z_vals = np.append(self.z_vals, z_val, axis=0)
        print(self.z_vals.shape)
        self.image_names.append(image_name)

    def add_proposal(self, z_val, image_name):
        self.proposal_z = z_val
        self.proposal_image = image_name

    def accept_proposal(self):
        self.add_link(self.proposal_z, self.proposal_image)
        self.reset_proposal()

    def reject_proposal(self):
        print(self.get_z().shape)
        self.add_link(np.expand_dims(self.get_z(), axis=0), self.get_image())
        self.reset_proposal()

    def reset_proposal(self):
        self.proposal_z = None
        self.proposal_image = None

    def get_proposal(self):
        return self.proposal_image

    def __len__(self):
        return len(self.image_names)


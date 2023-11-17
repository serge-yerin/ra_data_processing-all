# https://pytorch.org/blog/compiling-numpy-code/

import numpy as np
import time
import torch


# Function to use for time measurements
def kmeans(X, means):
    a = np.argmin(np.linalg.norm(X - means[:, None], axis=2), axis=0)
    # print('Hello')
    return a



# Preparing the dataset
npts = 10_000_000
X = np.repeat([[5, 5], [10, 10]], [npts, npts], axis=0)
X = X + np.random.randn(*X.shape)  # 2 distinct "blobs"
means = np.array([[5, 5], [10, 10]])

start_time = time.time()
np_pred = kmeans(X, means)
print("Just NumPy usage:    {0:2.5f} seconds".format((time.time() - start_time)))

start_time = time.time()
compiled_fn = torch.compile(kmeans)
print("Compilation took:    {0:2.5f} seconds".format((time.time() - start_time)))

# start_time = time.time()
# compiled_pred = compiled_fn(X, means)
# print("Compiled usage:      {0:2.5f} seconds".format((time.time() - start_time)))

# assert np.allclose(np_pred, compiled_pred)

for i in range(5):
    npts = 10_000_000
    X = np.repeat([[5, 5], [10, 10]], [npts, npts], axis=0)
    X = X + np.random.randn(*X.shape)  # 2 distinct "blobs"
    means = np.array([[5, 5], [10, 10]])

    start_time = time.time()
    with torch.device("cpu"):
        cuda_pred = compiled_fn(X, means)
    print("Iteration {0} took:    {1:2.5f} seconds".format(str(i), (time.time() - start_time)))
    # assert np.allclose(np_pred, cuda_pred)

# @torch.compile
# def tensor_fn(X, means):
#     X, means = X.numpy(), means.numpy()
#     ret = kmeans(X, means)
#     return torch.from_numpy(ret)
#
# def cuda_fn(X, means):
#     with torch.device("cuda"):
#         return tensor_fn(X, means)
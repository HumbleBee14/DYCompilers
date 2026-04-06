import numpy as np


def infer_shape_for_add(a: np.ndarray, b: np.ndarray):
    return np.broadcast_shapes(a.shape, b.shape)


def infer_shape_for_mul(a: np.ndarray, b: np.ndarray):
    return np.broadcast_shapes(a.shape, b.shape)


def infer_shape_for_relu(a: np.ndarray):
    return a.shape



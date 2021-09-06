import numpy as np


def collect_bounds(plotter):
    bounds = []
    for i in range(plotter.shape[0]):
        for j in range(plotter.shape[1]):
            plotter.subplot(i, j)
            bounds.append(plotter.bounds)

    return np.array(bounds).T


def get_bounds_multiview(plotter):
    bounds = collect_bounds(plotter)
    new_bounds = []
    for i in range(6):
        val = max(bounds[i]) if i % 2 else min(bounds[i])
        new_bounds.append(val)

    return np.array(new_bounds)

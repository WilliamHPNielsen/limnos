"""
Visualization of routes
"""
from .types import Route

import matplotlib.pyplot as plt


def plot_route(route: Route) -> None:

    fig, ax = plt.subplots()

    for this_point, next_point in zip(route[:-1], route[1:]):
        xs = (this_point[0], next_point[0])
        ys = (this_point[1], next_point[1])
        ax.plot(xs, ys, 'b-o')

    plt.show()

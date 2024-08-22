"""
In this assignment you should fit a model function of your choice to data
that you sample from a contour of given shape. Then you should calculate
the area of that shape.

The sampled data is very noisy so you should minimize the mean least squares
between the model you fit and the data points you sample.

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You
must make sure that the fitting function returns at most 5 seconds after the
allowed running time elapses. If you know that your iterations may take more
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment.
Note: !!!Despite previous note, using reflection to check for the parameters
of the sampled function is considered cheating!!! You are only allowed to
get (x,y) points from the given shape by calling sample().
"""

import numpy as np
import time
import random


from math import atan2
from sklearn.neighbors import NearestNeighbors

from functionUtils import AbstractShape
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt


class MyShape(AbstractShape):
    # change this class with anything you need to implement the shape
    def __init__(self,points):
        self.points = points
        pass

    def contour(self, n: int):
        pass

    def area(self) -> np.float32:
        x, y = self.points.T
        x1 = np.mean(x)
        y1 = np.mean(y)
        ### using radial sorting for all points given from DBscan and calalating area with Shoelace theorem method
        xs, ys = np.array(rotational_sort(self.points, x1, y1)).T
        area = 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))
        return np.float32(area)


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def rotational_sort(list_of_xy_coords, cx,cy):
    angles = [atan2(x-cx, y-cy) for x, y in list_of_xy_coords]
    indices = argsort(angles)
    return [list_of_xy_coords[i] for i in indices]


class Assignment5:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        solving the assignment for specific functions.
        """

        pass

    def area(self, contour: callable, maxerr=0.001)->np.float32:
        """
        Compute the area of the shape with the given contour.

        Parameters
        ----------
        contour : callable
            Same as AbstractShape.contour
        maxerr : TYPE, optional
            The target error of the area computation. The default is 0.001.

        Returns
        -------
        The area of the shape.

        """
        ### sampleing the given shape using the callable contour and calcalating the area with Shoelace theorem method
        points = np.array(contour(400))
        n = len(points)
        xs = [points[i, 0] for i in range(n)]
        ys = [points[i, 1] for i in range(n)]
        sums = [0, 0]
        for i in range(n - 1):
            sums[0] += xs[i] * ys[i + 1]
            sums[1] += xs[i + 1] * ys[i]
        area = 0.5 * abs(sums[0] + xs[-1] * ys[0] - sums[1] - xs[0] * ys[-1])
        return np.float32(area)

    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        sample : callable.
            An iterable which returns a data point that is near the shape contour.
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        An object extending AbstractShape.
        """
        #### checking delay of the given sample function
        T = time.time()
        x = sample()
        one_sample_time = time.time() - T
        maxtime = maxtime - one_sample_time
        #### deciding number of samples to take
        if one_sample_time <= 0.0001:
            n = 20000
        else:
            one_sample_time += 0.1
            n = int(((maxtime) / (one_sample_time)) * 1.3)
            if n < 0:
                n = 100
        samples = np.array([sample() for _ in range(n)])
        ##### using DBscan for reducing the number of samples
        nearst = NearestNeighbors(n_neighbors=10).fit(samples)
        dists = nearst.kneighbors(samples)[0]
        dists = np.sort(dists, axis=0)[:, 1]
        x = np.arange(0, n)
        data = np.vstack((x, dists)).T
        theta = np.arctan2(data[:, 1].max() - data[:, 1].min(), data[:, 0].max() - data[:, 0].min())
        mat = np.array(((np.cos(theta), -np.sin(theta)), (np.sin(theta), np.cos(theta))))
        vac = data.dot(mat)
        indexses = np.where(vac == vac.min())[0][0]
        dbs = DBSCAN(eps=data[indexses][1], min_samples=5).fit(samples)
        samples1 = dbs.components_
        #### making a shape with the "clean points" with in the area founction we are doing radial sort and calclating the area with Shoelace theorem method
        result = MyShape(samples1)
        return result
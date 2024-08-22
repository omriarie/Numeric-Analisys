"""
In this assignment you should fit a model function of your choice to data
that you sample from a given function.

The sampled data is very noisy so you should minimize the mean least squares
between the model you fit and the data points you sample.

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You
must make sure that the fitting function returns at most 5 seconds after the
allowed running time elapses. If you take an iterative approach and know that
your iterations may take more than 1-2 seconds break out of any optimization
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools
for solving this assignment.

"""

import sys

import numpy as np
import time
import random

class Assignment4:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        solving the assignment for specific functions.
        """

        pass

    def fit(self, f: callable, a: float, b: float, d: int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        f : callable.
            A function which returns an approximate (noisy) Y value given X.
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        a function:float->float that fits f between a and b
        """
        # checking time for call
        T = time.time()
        f(b)
        one_sample_time = time.time() - T
        maxtime = maxtime - one_sample_time
        # if too much then change the number of x line
        if one_sample_time <= 0.0001:
            num_splits = 10000
        else:
            one_sample_time += 0.1
            num_splits = int(((maxtime) / (one_sample_time)) * 1.3)
            if num_splits < 0:
                num_splits = 1
        #### sampleing the X's as mch as i can with the given maxtime
        x_line = np.linspace(a, b, num_splits)
        maxtime -= 0.6
        num_of_samples = 1
        y_samples = []
        while maxtime >= (time.time() - T):
            if num_of_samples == 1:
                try:
                    y_samples = f(x_line)
                except:
                    for num in x_line:
                        try:
                            y_samples.append(f(num))
                        except:
                            y_samples.append(0)
                y_samples = np.array(y_samples)
            else:
                try:
                    y_samples += f(x_line)
                except:
                    ys = []
                    for num in x_line:
                        try:
                            ys.append(f(num))
                        except:
                            ys.append(0)
                    y_samples += np.array(ys)
            num_of_samples += 1
        ##### making means of all of the Y's i sampled
        y_samples = y_samples / num_of_samples
        cd = 0
        differ = np.diff(y_samples)
        differ_sum = np.sum(differ)
        # trying to fine how many times the founction can be deredetived
        while differ_sum >= 0.000001:
            cd += 1
            differ = np.diff(differ)
            differ_sum = np.sum(differ)
        if cd != 0:
            d = cd + 1
        #### personal chase for sin witch gives us to hight degree.
        d = min(30, d)
        # checks if stright line
        mean = y_samples.mean()
        if abs(mean - y_samples[0]) <= 0.01:
            return lambda l: mean
        # plu decomposition using np librery
        a = np.vander(x_line, d)
        ata = a.transpose().dot(a)
        atb = a.transpose().dot(y_samples)
        c = np.linalg.inv(ata).dot(atb)
        return np.polynomial.Polynomial(np.flip(c))

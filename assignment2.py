"""
In this assignment you should find the intersection points for two functions.
"""
import numpy as np
import time
import random
import math
from collections.abc import Iterable


class Assignment2:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        solving the assignment for specific functions.
        """
        pass


    def derivative(self, f, x):
        d = 0.0000001
        g = (f(x + d) - f(x)) / d
        return g

    def newton(self, f, A, B, maxerr):
        x0 = self.bi_section(f, A, B, maxerr)
        x1 = x0
        counter = 0
        while abs(f(x1)) > maxerr and counter <= 20:
            x1 = x0 - (f(x0) / self.derivative(f, x0))
            x0 = x1
            counter += 1
        if counter > 20:
            return None
        if (A <= x1) and (x1 <= B):
            return x1

    def bi_section(self, f, a, b, maxerr):
        newp = ((b + a)) / 2
        while abs(b - a) >= maxerr:
            new_sign = (f(newp) > 0)
            fa = f(a)
            fa_sign = (fa > 0)
            if fa_sign is new_sign:
                a = newp
            else:
                b = newp
            newp = ((b + a)) / 2
        return newp


    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        ##### mking the interval number to split the line (a,b)
        interval_size = int(math.ceil(abs((b) - (a)))) * 25
        intervals_lins = np.linspace(a, b, interval_size, endpoint=True)
        ####### making g(x) witch is the founction that is created by devition of the tow given founctions.
        g = lambda x: f1(x) - f2(x)
        res = []
        #checking if a and b is an intersaction manually
        if g(intervals_lins[0]) == 0:
            res.append(intervals_lins[0])
        if g(intervals_lins[interval_size - 1]) == 0:
            res.append(intervals_lins[interval_size - 1])
        ##### cheching each interval if there is a posebility for intersaction with X axis
        for i in range(len(intervals_lins) - 1):
            i_sign = (self.derivative(g, intervals_lins[i]) > 0)
            i1_sign = (self.derivative(g, intervals_lins[i + 1]) > 0)
            con1 = (i_sign != i1_sign)
            if con1:
                root = self.newton(g, intervals_lins[i], intervals_lins[i + 1], maxerr)
                if root != None:
                    res.append(root)
                    break
            i_sign = (g(intervals_lins[i]) > 0)
            i1_sign = (g(intervals_lins[i + 1]) > 0)
            con2 = (i_sign != i1_sign)
            if con2:
                root = self.newton(g, intervals_lins[i], intervals_lins[i + 1], maxerr)
                if root != None:
                    res.append(root)

        """
        Find as many intersection points as you can. The assignment will be
        tested on functions that have at least two intersection points, one
        with a positive x and one with a negative x.
        
        This function may not work correctly if there is infinite number of
        intersection points. 


        Parameters
        ----------
        f1 : callable
            the first given function
        f2 : callable
            the second given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        maxerr : float
            An upper bound on the difference between the
            function values at the approximate intersection points.


        Returns
        -------
        X : iterable of approximate intersection Xs such that for each x in X:
            |f1(x)-f2(x)|<=maxerr.

        """

        # replace this line with your solution
        return res


##########################################################################

#
# import unittest
# from sampleFunctions import *
# from tqdm import tqdm
#
#
# class TestAssignment2(unittest.TestCase):
#
#     def test_sqr(self):
#
#         ass2 = Assignment2()
#
#         f1 = np.poly1d([-1, 0, 1])
#         f2 = np.poly1d([1, 0, -1])
#
#         X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
#
#         for x in X:
#             self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
#
#     def test_poly(self):
#
#         ass2 = Assignment2()
#
#         f1, f2 = randomIntersectingPolynomials(10)
#
#         X = ass2.intersections(f1, f2, -1, 1, maxerr=0.001)
#
#         for x in X:
#             self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
#
#
# if __name__ == "__main__":
#     unittest.main()

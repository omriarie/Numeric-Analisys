"""
In this assignment you should find the area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and
the leftmost intersection points of the two functions.

The functions for the numeric answers are specified in MOODLE.


This assignment is more complicated than Assignment1 and Assignment2 because:
    1. You should work with float32 precision only (in all calculations) and minimize the floating point errors.
    2. You have the freedom to choose how to calculate the area between the two functions.
    3. The functions may intersect multiple times. Here is an example:
        https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx
    4. Some of the functions are hard to integrate accurately.
       You should explain why in one of the theoretical questions in MOODLE.

"""

import numpy as np
import time
import random
from assignment2 import *


class Assignment3:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        solving the assignment for specific functions.
        """

        pass

    def integrate(self, f: callable, a: float, b: float, n: int) -> np.float32:
        ### integrating the founction using simpsons rule.
        if n % 2 != 0:
            n += 1
        h = (b - a) / (n - 2)
        x_axis = np.linspace(a, b, n - 1)
        y_axis = np.array(list(map(f, x_axis)))
        sums = [0, 0, 0]
        for i in range(0, len(y_axis), 2):
            sums[0] += y_axis[i]
            sums[2] += y_axis[i]
        for i in range(1, len(y_axis), 2):
            sums[1] += y_axis[i]
        sums[0] -= y_axis[len(y_axis) - 1]
        sums[1] *= 4
        sums[2] -= y_axis[0]
        """
        Integrate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the integration error. 
        Your secondary objective is minimizing the running time. The assignment
        will be tested on variety of different functions. 
        
        Integration error will be measured compared to the actual value of the 
        definite integral. 
        
        Note: It is forbidden to call f more than n times. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the integration range.
        b : float
            end of the integration range.
        n : int
            maximal number of points to use.

        Returns
        -------
        np.float32
            The definite integral of f between a and b
        """
        result = np.float32(h / 3 * np.sum(sums))
        return abs(result)




    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        ### gettting the intersections of the founction
        inters = np.sort(Assignment2().intersections(f1, f2, 1, 100))
        if len(inters) < 2:
            return np.nan
        total_area = 0
        #### calclating the area between every tow intersections using integrate from last assiment and summing up all of the results.
        for i in range(1,len(inters)):
            if f1(inters[i - 1]) - f2(inters[i - 1]) < 0:
                total_area += self.integrate(lambda x: f2(x) - f1(x), inters[i - 1], inters[i], 100)
            else:
                total_area += self.integrate(lambda x: f1(x) - f2(x), inters[i - 1], inters[i], 100)
        """
        Finds the area enclosed between two functions. This method finds 
        all intersection points between the two functions to work correctly. 
        
        Example: https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx

        Note, there is no such thing as negative area. 
        
        In order to find the enclosed area the given functions must intersect 
        in at least two points. If the functions do not intersect or intersect 
        in less than two points this function returns NaN.  
        This function may not work correctly if there is infinite number of 
        intersection points. 
        

        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """
        # replace this line with your solution
        result = np.float32(total_area)
        return result

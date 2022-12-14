import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate, scipy.optimize

def cross_point(x, y1, y2):
    #It`s necessary to lead the input data to a general form
    y1 = np.array(y1, dtype = float)
    y2 = np.array(y2, dtype = float)
    x = np.array(x, dtype = float)
    
    EPS = 1e-7

    assert len(x) == len(y1) == len(y2), "Input data lenth must be the same"
    y = y2 - y1
    count = 0
    for i in range(1, len(y)):
        if (y[i-1] < 0.0 and y[i] > 0.0) or (y[i-1] > 0.0 and y[i] < 0.0):
            count += 1
    assert count <= 1, "There should be only one intersection of two curves"
    
    if np.all((y<0) == (y<0)[0]): #Curve Intersection Check
        return None
    
    v1 = scipy.interpolate.InterpolatedUnivariateSpline(x, y1)
    v2 = scipy.interpolate.InterpolatedUnivariateSpline(x, y2)
    x0 = x[0]
    x_max = x[-1]
    while (x_max - x0) > EPS:
        x_mean = (x_max + x0) * 0.5
        dif0 = (v2(x0) - v1(x0)) < 0 #
        dif_mean = (v2(x_mean) - v1(x_mean)) < 0 
        dif_max = (v2(x_max) - v1(x_max)) < 0 
        if dif0 == dif_mean:
            x0 = x_mean
        else:
            x_max = x_mean  
    return [x_mean, (v1(x_mean) + v2(x_mean)) * 0.5]

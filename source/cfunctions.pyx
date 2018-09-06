import roots
from tkinter import *
import numpy
import math
import time

cpdef double sin(double x) except? -2:
    x = x%6.2831853
    cdef double r
    if x > 3.14159265:
        x = 6.28-x
        r = -1*16*x*(3.14159265-x)/(49.348022-4*x*(3.14159265-x))
        return r
    else:
        r = 16*x*(3.14159265-x)/(49.348022-4*x*(3.14159265-x))
        return r


cpdef double cos(double x) except? -2:
    x = x%6.2831853+1.5707963
    cdef double r
    if x > 3.14159265:
        x = 6.28-x
        r = -1*16*x*(3.14159265-x)/(49.348022-4*x*(3.14159265-x))
        return r
    else:
        r = 16*x*(3.14159265-x)/(49.348022-4*x*(3.14159265-x))
        return r

cpdef double arcsin(double x) except? -2:
    cpdef double r
    if -1<=x:
        if x<=1:
            r = x + x**3/6 + 0.15*x**5 + 0.238*x**25
            return r
        else:
            return "err"
    else:
        return "err"

cpdef double arccos(double x) except? -2:
    cpdef double asin
    asin = arcsin(x)
    if isinstance(asin, float) == True or isinstance(asin, int) == True:
        return 1.5707963-asin

cpdef double tan(double x):
    return numpy.tan(x)

cpdef double arctan(double x):
    cdef:
        double c = 0.596227
        double r
    if  x>= 0:
        r = 1.57*(c+x)*x/(1+2*c*x+x*x)
    else:
        r = 1.57*(c-x)*x/(1-2*c*x+x*x)
    return r
    
cpdef double sinh(double x):
    cdef:
        double e = 2.7182818
        double r
    r = (e**(2*x)-1)/(2*e**x)
    return r
    
cpdef double cosh(double x):
    cdef:
        double e = 2.7182818
        double r
    r = (e**(2*x)+1)/(2*e**x)
    return r

cpdef double tanh(double x):
    cdef:
        double e = 2.7182818
        double r
    r = (e**(2*x)-1)/(e**(2*x)+1)
    return r

cpdef double arcsinh(double x):
    cdef double r
    r = math.log(x+(x**2+1)**0.5)
    return r

cpdef double arccosh(double x):
    cdef double r
    if x >= 1:
        r = math.log(x+(x**2-1)**0.5)
        return r

cpdef double arctanh(double x):
    cdef double r
    if x < 1:
        if x > -1:
            r = 0.5*math.log((1+x)/(1-x))
            return r

cdef double accuracyAlg(double maxslope):
    return (1/(maxslope+0.001))**3*10
        
def getAccuracy(func, lasty, lastx):
    vals = []
    for each in lasty:
        vals.append(abs(float(roots.dydx(func, lastx, each))))
    return accuracyAlg(max(vals))

def drawExplicit(x, dx, mx, my, lastx, lasty, g11, g10, height, width, maxX, maxY, func, maxDx, color):
    start = time.time()
    accuracy = 1
    while x<maxX:
        x += accuracy*dx
        y = -eval(func.replace('x', f'({x})'))
        if abs(y) > maxY*1.1:
            pass
        elif "I" in str(y):
            accuracy = 5
            pass
        elif "I" in str(lasty):
            pass
        else:
            #Accuracy Calculator
            maxslope = abs(float(roots.dydx(func, lastx, lasty)))
            accuracy = accuracyAlg(maxslope)
            if accuracy > maxDx:
                accuracy = maxDx
            #
            g11.append(g10.create_line(lastx*mx+(width-370)/2, lasty*my+(height-100)/2, x*mx+(width-370)/2, y*my+(height-100)/2, fill = color, width=1))
        lastx = x
        lasty = y
    print(time.time()-start)
    return g11

def drawExplicitTrig(x, dx, mx, my, lastx, lasty, g11, g10, height, width, maxX, maxY, func, maxDx, color):
    accuracy = 1
    start = time.time()
    wait = 0
    while x<maxX:
        if wait == 0:
            x += accuracy*dx
        else:
            x += 0.01
        try:
            y = eval(func.replace('x', f'({x})'))
            if not y:
                y = 'err'
            else:
                try:
                    y = -y
                except:
                    pass
        except:
            y = "err"
        if wait >= 1:
            wait = 0
            pass
        elif y == "err":
            pass
        elif lasty == "err":
            accuracy = 0.5
            x = lastx
            wait = 1
            pass  
        elif abs(y) > maxY*1.1:
            pass
        elif "I" in str(y):
            accuracy = maxDx
            pass
        elif "I" in str(lasty):
            pass
        else:
            #Accuracy Calculator
            maxslope = abs(float(roots.dydx(func, lastx, lasty)))
            accuracy = accuracyAlg(maxslope)
            if accuracy > maxDx:
                accuracy = maxDx
            #
            g11.append(g10.create_line(lastx*mx+(width-370)/2, lasty*my+(height-100)/2, x*mx+(width-370)/2, y*my+(height-100)/2, fill = color, width=1))
        lastx = x
        lasty = y
    print(time.time()-start)
    return g11

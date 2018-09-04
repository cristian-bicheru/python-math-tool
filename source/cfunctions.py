import roots
from tkinter import *
import numpy

def getAccuracy(func, lasty, lastx):
    vals = []
    for each in lasty:
        vals.append(abs(float(roots.dydx(func, lastx, each))))
    return roots.accuracyAlg(max(vals))

def drawExplicit(x, dx, mx, my, lastx, lasty, g11, g10, height, width, maxX, maxY, func, maxDx, color):
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
            accuracy = roots.accuracyAlg(maxslope)
            if accuracy > maxDx:
                accuracy = maxDx
            #
            g11.append(g10.create_line(lastx*mx+(width-370)/2, lasty*my+(height-100)/2, x*mx+(width-370)/2, y*my+(height-100)/2, fill = color, width=2))
        lastx = x
        lasty = y
    return g11

def drawExplicitTrig(x, dx, mx, my, lastx, lasty, g11, g10, height, width, maxX, maxY, func, maxDx, color):
    accuracy = 1
    fFunc = roots.Format(func)
    while x<maxX:
        x += accuracy*dx
        try:
            y = -eval(fFunc.replace('x', f'({x})'))
            if str(y) == 'nan' or str(y) == 'inf':
                y = 'err'
        except:
            y = "err"
        if y == "err":
            pass
        elif lasty == "err":
            pass
        elif abs(y) > maxY*1.1:
            pass
        elif "I" in str(y):
            accuracy = 5
            pass
        elif "I" in str(lasty):
            pass
        else:
            #Accuracy Calculator
            maxslope = abs(float(roots.dydx(func, lastx, lasty)))
            accuracy = roots.accuracyAlg(maxslope)
            if accuracy > maxDx:
                accuracy = maxDx
            #
            g11.append(g10.create_line(lastx*mx+(width-370)/2, lasty*my+(height-100)/2, x*mx+(width-370)/2, y*my+(height-100)/2, fill = color, width=2))
        lastx = x
        lasty = y
    return g11

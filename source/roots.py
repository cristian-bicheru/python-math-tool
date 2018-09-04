import scipy.optimize as so
import numpy
import sympy
#import autograd.numpy as numpy
#import autograd
import time

tfunctions = ("arcsinh", "arccosh", "arctanh", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh", "sin", "cos", "tan")
tfunctions2 = ("arcsINh", "arccOSh", "arctANh", "arcsIN", "arccOS", "arctAN", "sINh", "cOSh", "tANh", "sin", "cos", "tan")
otherfunc = ("abs")

def Format(func):
    for x in range(0, len(tfunctions)):
        func = func.replace(tfunctions[x], "numpy."+tfunctions2[x])
    return func.replace("IN", "in").replace("AN", "an").replace("OS", "os").replace('^', '**')


def quickFilter(func, maxY):
    check = 0
    func = str(sympy.N(func))
    for trigF in tfunctions:
        if trigF in func:
            check += 1
            break
    for otherF in otherfunc:
        if otherF in func:
            check += 1
            break
    if check == 0:
        def f(y):
            y = str(y).replace('[', '').replace(']', '')
            return eval(func.replace('Y', f'({y})'))


        sign = 2
        croots = 1
        for i in range(-maxY*2, (maxY+1)*2):
            fi = f(i/2)
            if fi == 0:
                croots = 0
                break
            if sign == 2:
                sign = fi/abs(fi)
            if sign != fi/abs(fi):
                croots = 0
                break
    else:
        croots = 0
    return croots

def accuracyAlg(maxslope):
    return (1/(maxslope+0.001))**2*10+0.5

def existSol(func, maxY):
    test = quickFilter(func, maxY)
    func = Format(func)
    if test == 0:
        def f(y):
            y = str(y).replace('[', '').replace(']', '')
            return eval(func.replace('Y', f'({y})'))
        try:
            solution = float(str(so.fsolve(f, 5)).replace("[", '').replace("]", ''))
            solution2 = float(str(so.fsolve(f, -5)).replace("[", '').replace("]", ''))
            cap = maxY*1.15
            check = 2
            if abs(solution) > cap or abs(f(solution))>0.1:
                check += -1
            if abs(solution2) > cap or abs(f(solution2))>0.1:
                check += -1
                
            if check > 0:
                return 1
            else:
                return 0
        except:
            return 0
        
    else:
        return 0
        

prevDerivatives = {}
           
def dydx(func, a, b):
    Y = sympy.Symbol('Y')
    x = sympy.Symbol('x')
    dydxCached = prevDerivatives.get(func, None)
    if dydxCached:
        try:
            dydx = eval(dydxCached.replace('x', f'({a})').replace('Y', f'({b})'))
        except:
            dydx = 1
    else:
        try:
            adydx = Format(str(sympy.idiff(sympy.sympify(func), Y, x)))
            prevDerivatives[func] = adydx
            dydx = eval(adydx.replace('x', f'({a})').replace('Y', f'({b})'))
        except:
            dydx = 1
    return dydx

#prevADerivatives = {}

#def autodydx(func, X):   #Autograd is useful here since we need gradient optimization, 
#    dydxCached = prevDerivatives.get(func, None)
#    if dydxCached:
#        try:
#            dydx = dydxCached(X)
#        except:
#            dydx = 1
#    else:
#        try:
#            fFunc = Format(func)
#            def f(x):
#                return eval(fFunc.replace('x', f'({x})'))
#            adydx = autograd.grad()
#            prevDerivatives[func] = adydx
#            dydx = adydx(X)
#        except:
#            dydx = 1
#    return dydx

def solve(func, maxY, algorithm):
    
    hybrF = 0

    test = quickFilter(func, maxY)
    
    func = Format(func)

    

    if test == 0:
        
        solutions = []
        def f(y):
            y = str(y).replace('[', '').replace(']', '')
            return eval(func.replace('Y', f'({y})'))
        for i in range(-maxY, maxY+1):
            if i != 0:
                try:

                    if algorithm == 'nk':
                        solutions.append(float(str(so.newton_krylov(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'an':
                        solutions.append(float(str(so.anderson(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'b1':
                        solutions.append(float(str(so.broyden1(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'b2':
                        solutions.append(float(str(so.broyden2(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'em':
                        solutions.append(float(str(so.excitingmixing(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'lm':
                        solutions.append(float(str(so.linearmixing(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'db':
                        solutions.append(float(str(so.diagbroyden(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'fs':
                        solutions.append(float(str(so.fsolve(f, i)).replace("[", '').replace("]", '')))
                    elif algorithm == 'hy':
                        solutions.append(float(str(so.root(f, i, method='hybr')['x']).replace("[", '').replace("]", '')))
                    elif algorithm == 'df':
                        solutions.append(float(str(so.root(f, i, method='df-sane')['x']).replace("[", '').replace("]", '')))
                    else:
                        if i == -maxY:
                            timefs = time.time()
                            solutions.append(float(str(so.fsolve(f, i)).replace("[", '').replace("]", '')))
                            timefs = time.time()-timefs
                        if i == -maxY+1:
                            timedb = time.time()
                            solutions.append(float(str(so.diagbroyden(f, i)).replace("[", '').replace("]", '')))
                            timedb = time.time()-timefs
                        if i >= -maxY+2:
                            if timefs>timedb:
                                solutions.append(float(str(so.diagbroyden(f, i)).replace("[", '').replace("]", '')))
                            else:
                                solutions.append(float(str(so.fsolve(f, i)).replace("[", '').replace("]", '')))
                    
                except:
                    pass
        if solutions == [] and algorithm == 'hy': #sometimes hybr fails to converge
            hybrF = 1
            for i in range(-maxY, maxY+1):
                if i != 0:
                    try:
                        if i == -maxY:
                            timefs = time.time()
                            solutions.append(float(str(so.fsolve(f, i)).replace("[", '').replace("]", '')))
                            timefs = time.time()-timefs
                        if i == -maxY+1:
                            timedb = time.time()
                            solutions.append(float(str(so.diagbroyden(f, i)).replace("[", '').replace("]", '')))
                            timedb = time.time()-timefs
                        if i >= -maxY+2:
                            if timefs>timedb:
                                solutions.append(float(str(so.diagbroyden(f, i)).replace("[", '').replace("]", '')))
                            else:
                                solutions.append(float(str(so.fsolve(f, i)).replace("[", '').replace("]", '')))
                    except:
                        pass

            
        for i in range(0, len(solutions)):
            solutions[i] = round(solutions[i], 4)
        solutions = list(set(solutions))
        cap = maxY*1.15
        for each in solutions:
            if abs(each) > cap:
                solutions.remove(each)
        return [solutions, hybrF]
    else:
        return [[], 0]

def containsSpec(func):
    for each in tfunctions:
        if each in func:
            return 1
    for each in otherfunc:
        if each in func:
            return 1    
    return 0





#For Benchmarking Different Algorithms:

'''
func = "sin(Y)**(5/2)+cos(Y)**(1/3)-5*Y**(22/7)+(arctan(Y)-1)*Y**(29/8)-0.5"

a = time.time()
print(solve(func, 10, "nk"))
for x in range(0, 250):
    solve(func, 10, "nk")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "an"))
for x in range(0, 250):
    solve(func, 10, "an")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "b1"))
for x in range(0, 250):
    solve(func, 10, "b1")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "b2"))
for x in range(0, 250):
    solve(func, 10, "b2")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "em"))
for x in range(0, 250):
    solve(func, 10, "em")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "lm"))
for x in range(0, 250):
    solve(func, 10, "lm")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "db"))
for x in range(0, 250):
    solve(func, 10, "db")
print(time.time()-a)
a = time.time()
print(solve(func, 10, "fs"))
for x in range(0, 250):
    solve(func, 10, "fs")
print(time.time()-a)
'''

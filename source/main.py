from tkinter import *
from tkinter.ttk import *
import math
import numpy
import sympy
import scipy
import scipy.optimize as so
import roots
import others
import cfunctions

#############################
# Python Math Tool          #
# By: Cristian Bicheru 2018 #
#############################

#Dimensions
width = 1900
height = 1000
#Defaults
maxX = 10
maxY = 6
accuracyd = 0.1
#Colors
backgroundC = "#EAEAEA"
menuBarC = "#C0C0C0"
tabBarC = "#F1F1F1"
tabBackgroundC = "#FCFCFC"
colors = ("red", "green", "blue", "purple", "orange") #line colors for graph
#Miscellanious
maxDx = 25

tk = Tk()
canvas = Canvas(tk, width=width, height=height, bg=backgroundC)
tk.title("python math tool")
tk.resizable(False, False)
canvas.pack()

# Intro Screen

quickStartGuide = '''
------------------ Quick Start Guide ------------------


[] File Button:

Let's you create new graph panes or command line panes.


[] Tab Bar:

Let's you navigate and close tabs.


[] Graphs:

Supports implicit, explicit, and most trig functions.
SEC, CSC, COT, and their inverses and hyperbolic
equivalents are not supported. Functions in terms of
integrals or derivatives are not supported as of now.


[] Command Lines:

Let's you run code. Use output = {your output} to
specify your output.
'''

quickStart = Text(tk, state='normal', bg=backgroundC, width=55, height = 27)
quickStart.insert("end-1c", quickStartGuide)
quickStart.config(state='disabled')
quickStart.place(x=30, y=100)

#----

s = Style(tk)
s.theme_use('clam')
s.configure('flat.TButton', borderwidth=0, background=menuBarC, width=4)

fileTabVar = StringVar(tk)

class menuBar:
    def __init__(self):
        self.shape = canvas.create_rectangle(-10, -10, width+10, 35, fill=menuBarC)
        self.fileTab = OptionMenu(tk, fileTabVar, "File", "New Graph", "New Command Line", style='flat.TButton')
        self.fileTab.place(x=5, y=5)
        self.tabs = {}
        
        print("menubar loaded")
        tk.update()

    def checkFileTab(self):
        setting = fileTabVar.get()
        if setting != "File":
            self.createNew(setting)
            fileTabVar.set("File")
        tk.update()

    def createNew(self, obj):
        if obj == "New Graph":
            tabN = len(self.tabs)
            self.tabs[tabN] = [Frame(tk)]
            self.tabs[tabN].append(Canvas(self.tabs[tabN][0], width=width, height=height-75, bg=tabBackgroundC))
            self.tabs[tabN][0].place(x=0, y=70)
            self.tabs[tabN][1].pack()
            self.tabs[tabN].append(Frame(tk, height=27.5, width=130))
            self.tabs[tabN][2].pack_propagate(0)
            self.tabs[tabN][2].place(x=tabN*160+5, y=37.5)
            self.tabs[tabN].append(Button(self.tabs[tabN][2], text="Graph "+str(tabN), command=lambda : self.show(tabN)))
            self.tabs[tabN][3].pack(fill=BOTH, expand=1)
            self.tabs[tabN].append(Frame(tk, height=27.5, width=25))
            self.tabs[tabN][4].pack_propagate(0)
            self.tabs[tabN][4].place(x=tabN*160+135, y=37.5)
            self.tabs[tabN].append(Button(self.tabs[tabN][4], text="x", command=lambda : self.closeTab(tabN)))
            self.tabs[tabN][5].pack(fill=BOTH, expand=1)


            graph = self.tabs[tabN]

            graph.append(Entry(graph[0], width=32))
            graph[6].insert(0, "function")
            graph[6].place(x=12.5, y=12.5)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[6].get(), tabN, graph[28][0], graph[28][1], 1), width=14))
            graph[7].place(x=245, y=7.5)
            #
            graph.append(graph[1].create_rectangle(350, 5, width-10, height-85, outline = "grey"))
            graph.append(Frame(graph[0], height=height-100, width=width-370))
            graph[9].place(x=355,y=10)
            graph.append(Canvas(graph[9], bg="white", height=height-100, width=width-370))
            graph[10].place(x=0, y=0)
            graph.append("") #graph[11] reserved for the actual graph
            graph.append("") #graph[12] reserved for graph features
            graph[11] = []
            graph[12] = []
            #
            graph.append(Entry(graph[0], width=32))
            graph[13].insert(0, "function")
            graph[13].place(x=12.5, y=47.5)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[13].get(), tabN, graph[28][0], graph[28][1], 2), width=14))
            graph[14].place(x=245, y=42.5)
            
            graph.append(Entry(graph[0], width=32))
            graph[15].insert(0, "function")
            graph[15].place(x=12.5, y=82.5)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[15].get(), tabN, graph[28][0], graph[28][1], 3), width=14))
            graph[16].place(x=245, y=77.5)
            
            graph.append(Entry(graph[0], width=32))
            graph[17].insert(0, "function")
            graph[17].place(x=12.5, y=117.5)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[17].get(), tabN, graph[28][0], graph[28][1], 4), width=14))
            graph[18].place(x=245, y=112.5)
            
            graph.append(Entry(graph[0], width=32))
            graph[19].insert(0, "function")
            graph[19].place(x=12.5, y=152.5)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[19].get(), tabN, graph[28][0], graph[28][1], 5), width=14))
            graph[20].place(x=245, y=147.5)

            graph.append("") #graph[21] reserved for graphed functions
            graph[21] = {}
            
            graph.append(Button(graph[0], text="Clear Graph", command=lambda : self.clear(tabN, maxX, maxY, "all"), width=14))
            graph[22].place(x=125, y=185)
            
            graph.append(Entry(graph[0], width=8))
            graph[23].insert(0, "10, 6")
            graph[23].place(x=10, y=232.5)
            graph.append(Button(graph[0], text="Set Bounds", command=lambda : self.changeBounds(graph[23].get(), tabN), width=14))
            graph[24].place(x=72.5, y=227.5)

            graph.append("")
            graph.append("")
            
            graph.append(accuracyd) #graph[27] is reserved for the accuracy
            graph.append([maxX, maxY]) #graph[28] is reserved for the bounds
            
            self.initGraph(tabN, maxX, maxY)
            
        if obj == "New Command Line":
            tabN = len(self.tabs)
            self.tabs[tabN] = [Frame(tk)]
            self.tabs[tabN].append(Canvas(self.tabs[tabN][0], width=width, height=height-75, bg=tabBackgroundC))
            self.tabs[tabN][0].place(x=0, y=70)
            self.tabs[tabN][1].pack()
            self.tabs[tabN].append(Frame(tk, height=27.5, width=130))
            self.tabs[tabN][2].pack_propagate(0)
            self.tabs[tabN][2].place(x=tabN*160+5, y=37.5)
            self.tabs[tabN].append(Button(self.tabs[tabN][2], text="Command Line "+str(tabN), command=lambda : self.show(tabN)))
            self.tabs[tabN][3].pack(fill=BOTH, expand=1)
            self.tabs[tabN].append(Frame(tk, height=27.5, width=25))
            self.tabs[tabN][4].pack_propagate(0)
            self.tabs[tabN][4].place(x=tabN*160+135, y=37.5)
            self.tabs[tabN].append(Button(self.tabs[tabN][4], text="x", command=lambda : self.closeTab(tabN)))
            self.tabs[tabN][5].pack(fill=BOTH, expand=1)


            cmd = self.tabs[tabN]
            #Creates Input/Output Fields, could use some code cleanup
            boxes = {}
            b=0
            boxes[0] = [Frame(cmd[0], height=200, width=width-10)]
            boxes[0][0].pack_propagate(0)
            boxes[0][0].place(x=5, y=5+311*b)
            boxes[0].append(Text(boxes[b][0]))
            boxes[0][1].pack(fill=BOTH, expand=1)
            boxes[0].append(Button(boxes[b][0], text="Execute", width=8, command=lambda : self.executeCode(tabN, 0)))
            boxes[0][2].place(x=width-75, y=167.5)
            boxes[0].append(Frame(cmd[0], height=100, width=width-10))
            boxes[0][3].pack_propagate(0)
            boxes[0][3].place(x=5, y=211+311*b)
            boxes[0].append(Text(boxes[b][3], state="disabled"))
            boxes[0][4].pack(fill=BOTH, expand=1)
            boxes[0].append(cmd[1].create_rectangle(2, 2+311*b, width-2, 208+311*b, width=2))
            b=1
            boxes[1] = [Frame(cmd[0], height=200, width=width-10)]
            boxes[1][0].pack_propagate(0)
            boxes[1][0].place(x=5, y=5+311*b)
            boxes[1].append(Text(boxes[b][0]))
            boxes[1][1].pack(fill=BOTH, expand=1)
            boxes[1].append(Button(boxes[b][0], text="Execute", width=8, command=lambda : self.executeCode(tabN, 1)))
            boxes[1][2].place(x=width-75, y=167.5)
            boxes[1].append(Frame(cmd[0], height=100, width=width-10))
            boxes[1][3].pack_propagate(0)
            boxes[1][3].place(x=5, y=211+311*b)
            boxes[1].append(Text(boxes[b][3], state="disabled"))
            boxes[1][4].pack(fill=BOTH, expand=1)
            boxes[1].append(cmd[1].create_rectangle(2, 2+311*b, width-2, 208+311*b, width=2))
            b=2
            boxes[2] = [Frame(cmd[0], height=200, width=width-10)]
            boxes[2][0].pack_propagate(0)
            boxes[2][0].place(x=5, y=5+311*b)
            boxes[2].append(Text(boxes[b][0]))
            boxes[2][1].pack(fill=BOTH, expand=1)
            boxes[2].append(Button(boxes[b][0], text="Execute", width=8, command=lambda : self.executeCode(tabN, 2)))
            boxes[2][2].place(x=width-75, y=167.5)
            boxes[2].append(Frame(cmd[0], height=100, width=width-10))
            boxes[2][3].pack_propagate(0)
            boxes[2][3].place(x=5, y=211+311*b)
            boxes[2].append(Text(boxes[b][3], state="disabled"))
            boxes[2][4].pack(fill=BOTH, expand=1)
            boxes[2].append(cmd[1].create_rectangle(2, 2+311*b, width-2, 208+311*b, width=2))

            
            cmd.append(boxes)

            
            tk.update()

    
    def executeCode(self, tabN, b):
        cmd = self.tabs[tabN]
        cmd[6][b][4].config(state="normal")
        cmd[6][b][4].delete(1.0, "end-1c")
        cmd[6][b][4].insert("end-1c", str(others.execCode(cmd[6][b][1].get("1.0",'end-1c'))))
        cmd[6][b][4].config(state="disabled")
        
    
    def changeBounds(self, newBounds, tabN):
        graph = self.tabs[tabN]
        
        graph[28][0], maxX = int(newBounds.split(',')[0]), int(newBounds.split(',')[0])
        graph[28][1], maxY = int(newBounds.split(',')[1]), int(newBounds.split(',')[1])
        
        self.clear(tabN, maxX, maxY, "resize")

        num = 1
        for func in list(graph[21].values()):
            self.drawGraph(func, tabN, maxX, maxY, num)
            num += 1
        
        tk.update()
        

    def clear(self, tabN, maxX, maxY, condition):
        graph = self.tabs[tabN]
        
        if condition == "resize":
            for each in graph[11]:
                graph[10].delete(each)
            for each in graph[12]:
                try:
                    graph[10].delete(each)
                except:
                    try:
                        each.destroy()
                    except:
                        pass
            graph[11] = []
            graph[12] = []
            self.initGraph(tabN, maxX, maxY)
        
        elif condition == "all":
            for each in graph[11]:
                graph[10].delete(each)
            graph[11] = []
            graph[21] = {}
        tk.update()
            
    
    def initGraph(self, tabN, maxX, maxY):
        graph = self.tabs[tabN]
        
        #graph features

        graph[12].append(graph[10].create_line((width-370)/2, 0, (width-370)/2, (height-100), fill = "black", width=2))
        graph[12].append(graph[10].create_line(0, (height-100)/2, (width-370), (height-100)/2, fill = "black", width=2))

        #Draw Numbers:
        freqX = int(round(maxX/10))

        freqY = int(round(maxY/10))

        if freqX == 0:
            freqX = 1
        if freqY == 0:
            freqY = 1
        
        for x in range(maxX, 2*maxX, freqX):
            graph[12].append(Label(graph[9], text = str(-maxX+x), background="white"))
            xp = (width-370)/(2*maxX)*(x)-5
            graph[12][-1].place(x=xp, y=(height-100)/2+3)

        for x in range(maxX, 0, -freqX):
            graph[12].append(Label(graph[9], text = str(-maxX+x), background="white"))
            xp = (width-370)/(2*maxX)*(x)-5
            graph[12][-1].place(x=xp, y=(height-100)/2+3)

        for y in range(maxY, 2*maxY, freqY):
            if maxY == y:
                pass
            else:
                graph[12].append(Label(graph[9], text = str(maxY-y), background="white"))
                yp = (height-100)/(2*maxY)*(y)-10
                graph[12][-1].place(x=(width-370)/2-20, y=yp)

        for y in range(maxY, 0, -freqY):
            if maxY == y:
                pass
            else:
                graph[12].append(Label(graph[9], text = str(maxY-y), background="white"))
                yp = (height-100)/(2*maxY)*(y)-10
                graph[12][-1].place(x=(width-370)/2-20, y=yp)
                
        #Draw Grid Lines
        for x in range(maxX, 2*maxX, freqX):
            if maxX == x:
                pass
            else:
                xp = (width-370)/(2*maxX)*(x)
                graph[12].append(graph[10].create_line(xp, 0, xp, (height-100)))

        for x in range(maxX, 0, -freqX):
            if maxX == x:
                pass
            else:
                xp = (width-370)/(2*maxX)*(x)
                graph[12].append(graph[10].create_line(xp, 0, xp, (height-100)))

        for y in range(maxY, 2*maxY, freqY):
            if maxY == y:
                pass
            else:
                yp = (height-100)/(2*maxY)*(y)
                graph[12].append(graph[10].create_line(0, yp, (width-370), yp))


        for y in range(maxY, 0, -freqY):
            if maxY == y:
                pass
            else:
                yp = (height-100)/(2*maxY)*(y)
                graph[12].append(graph[10].create_line(0, yp, (width-370), yp))
        #end graph features
        tk.update()
    
    def drawGraph(self, func, tabN, maxX, maxY, prompt):
        if func == "function":
            print("invalid")
            return 0
        graph = self.tabs[tabN]

        if prompt != "null":
            graph[21][prompt] = func

        color = colors[prompt-1]
        
        if '=' not in func and roots.containsSpec(func) == 0:
            graph[11] = cfunctions.drawExplicit(-maxX, 2*maxX/(width-370), (width-370)/(2*maxX), (height-100)/(2*maxY), -maxX, -eval(func.replace('x', f'(-1*{maxX})')), graph[11], graph[10], height, width, maxX, maxY, func, maxDx, color)

        elif '=' not in func and roots.containsSpec(func) == 1:
            try:
                lasty = -eval(roots.Format(func.replace('x', f'(-1*{maxX})')))
                if str(lasty) == 'nan' or str(lasty) == 'inf':
                    lasty = 'err'
            except:
                lasty = "err"
            graph[11] = cfunctions.drawExplicitTrig(-maxX, 2*maxX/(width-370), (width-370)/(2*maxX), (height-100)/(2*maxY), -maxX, lasty, graph[11], graph[10], height, width, maxX, maxY, func, maxDx, color)
      

        elif '=' in func and 'y' in func:
            wait = 0
            alg = "auto" #hybr seemed fast in testing but seems to have problems
            func = func.replace('y', "Y")
            split = func.split('=')
            func = split[0]+"-("+split[1]+")"
            
            dx = 2*maxX/(width-370)
            mx = (width-370)/(2*maxX)
            my = (height-100)/(2*maxY)
            x = -maxX
            lastx = -maxX
            compute = roots.solve((func.replace('x', f'({x})')), maxY, alg)
            if compute[1] == 1 and alg == 'hybr':
                alg = "auto"
                print("hybr failed")
            lasty = [-float(a) for a in compute[0]]
            while x<maxX:
                if wait == 0:
                    x += graph[27]*dx
                else:
                    x += 0.01
                yvals = [-float(x) for x in roots.solve((func.replace('x', f'({x})')), maxY, alg)[0]]
                #Accuracy Calculator
                maxslope = 0
                if yvals == []:
                    graph[27] = 5
                    pass
                elif wait == 1:
                    wait = 0
                    pass
                elif lasty != []:
                    graph[27] = cfunctions.getAccuracy(func, lasty, lastx)
                    if graph[27] > maxDx:
                        graph[27] = maxDx
                elif lasty == [] and yvals != []:
                    graph[27] = 0.5
                    x = lastx
                    wait = 1
                    pass
                #
                for y in yvals:
                    try:
                        Clasty = min(lasty, key=lambda x:abs(x-y))
                    except:
                        break
                    if abs(y) > maxY*1.1:
                        pass
                    else:
                        graph[11].append(graph[10].create_line(lastx*mx+(width-370)/2, Clasty*my+(height-100)/2, x*mx+(width-370)/2, y*my+(height-100)/2, fill = color, width=1))
                lastx = x
                lasty = yvals
                
    
    def closeTab(self, tabN):
        for each in self.tabs[tabN]:
            try:
                each.destroy()
            except:
                pass
        self.tabs.pop(tabN)
        temp = list(self.tabs.values())
        self.tabs = {}
        for i in range(0, len(temp)):
            self.tabs[i] = temp[i]
        for i in range(0, len(self.tabs)):
            self.tabs[i][2].place(x=i*160+5, y=37.5)
            self.tabs[i][4].place(x=i*160+5+130, y=37.5)
            self.tabs[i][3].config(command=lambda : self.show(i))
            self.tabs[i][5].config(command=lambda : self.closeTab(i))
        tk.update()
            
            
    
    def show(self, tabN):
        self.tabs[tabN][0].tkraise()
        tk.update()
            
class tabBar:
    def __init__(self):
        self.shape = canvas.create_rectangle(-10, 35, width+10, 75, fill=tabBarC)
        
        print("tab bar loaded")
        tk.update()

menubar = menuBar()
tabBar()

def checkF(*args):
    menubar.checkFileTab()

fileTabVar.set("File")
fileTabVar.trace("w", checkF)

tk.update()
        
tk.mainloop()



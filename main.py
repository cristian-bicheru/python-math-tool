from tkinter import *
import math
import numpy
import sympy

#Dimensions
width = 1600
height = 900
#Defaults
maxX = 10
maxY = 10
accuracyd = 10
#Colors
backgroundC = "#EAEAEA"
menuBarC = "#C0C0C0"
tabBarC = "#F1F1F1"
tabBackgroundC = "#FCFCFC"
colors = ["red", "green", "blue", "purple", "orange"] #line colors for graph

tk = Tk()
canvas = Canvas(tk, width=width, height=height, bg=backgroundC)
tk.title("python math tool")
tk.resizable(False, False)
canvas.pack()

fileTabVar = StringVar(tk)

class menuBar:
    def __init__(self):
        self.shape = canvas.create_rectangle(-10, -10, width+10, 40, fill=menuBarC)
        self.fileTab = OptionMenu(tk, fileTabVar, "File", "New Graph", "New Command Line")
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
            self.tabs[tabN].append(Frame(tk, height=20, width=150))
            self.tabs[tabN][2].pack_propagate(0)
            self.tabs[tabN][2].place(x=tabN*155+5, y=45)
            self.tabs[tabN].append(Button(self.tabs[tabN][2], text="Graph "+str(tabN), command=lambda : self.show(tabN)))
            self.tabs[tabN][3].pack(fill=BOTH, expand=1)
            self.tabs[tabN].append(Frame(tk, height=20, width=20))
            self.tabs[tabN][4].pack_propagate(0)
            self.tabs[tabN][4].place(x=tabN*155+5+130, y=45)
            self.tabs[tabN].append(Button(self.tabs[tabN][4], text="X", command=lambda : self.closeTab(tabN)))
            self.tabs[tabN][5].pack(fill=BOTH, expand=1)


            graph = self.tabs[tabN]

            graph.append(Entry(graph[0]))
            graph[6].insert(0, "function")
            graph[6].place(x=10, y=10)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[6].get(), tabN, maxX, maxY, 1)))
            graph[7].place(x=115, y=7.5)
            #
            graph.append(graph[1].create_rectangle(200, 5, width-10, height-85, outline = "grey"))
            graph.append(Frame(graph[0], height=height-95, width=width-220))
            graph[9].place(x=205,y=10)
            graph.append(Canvas(graph[9], bg="white", height=height-95, width=width-220))
            graph[10].place(x=0, y=0)
            graph.append("") #graph[11] reserved for the actual graph
            graph.append("") #graph[12] reserved for graph features
            graph[11] = []
            graph[12] = []
            #
            graph.append(Entry(graph[0]))
            graph[13].insert(0, "function")
            graph[13].place(x=10, y=45)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[13].get(), tabN, maxX, maxY, 2)))
            graph[14].place(x=115, y=42.5)
            
            graph.append(Entry(graph[0]))
            graph[15].insert(0, "function")
            graph[15].place(x=10, y=80)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[15].get(), tabN, maxX, maxY, 3)))
            graph[16].place(x=115, y=77.5)
            
            graph.append(Entry(graph[0]))
            graph[17].insert(0, "function")
            graph[17].place(x=10, y=115)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[13].get(), tabN, maxX, maxY, 4)))
            graph[18].place(x=115, y=112.5)
            
            graph.append(Entry(graph[0]))
            graph[19].insert(0, "function")
            graph[19].place(x=10, y=150)
            graph.append(Button(graph[0], text="Create Graph", command=lambda : self.drawGraph(graph[29].get(), tabN, maxX, maxY, 5)))
            graph[20].place(x=115, y=147.5)

            graph.append("") #graph[21] reserved for graphed functions
            graph[21] = {}
            
            graph.append(Button(graph[0], text="Clear Graph", command=lambda : self.clear(tabN, maxX, maxY, "all")))
            graph[22].place(x=50, y=185)
            
            graph.append(Entry(graph[0]))
            graph[23].insert(0, "10, 10")
            graph[23].place(x=10, y=220)
            graph.append(Button(graph[0], text="Set Bounds", command=lambda : self.changeBounds(graph[23].get(), tabN)))
            graph[24].place(x=125, y=220)

            graph.append(Entry(graph[0]))
            graph[25].insert(0, "10")
            graph[25].place(x=10, y=255)
            graph.append(Button(graph[0], text="Set Accuracy", command=lambda : self.changeAccuracy(graph[25].get(), tabN, graph[23].get())))
            graph[26].place(x=115, y=255)
            
            graph.append(accuracyd) #graph[27] is reserved for the accuracy
            
            self.initGraph(tabN, maxX, maxY)
            
        if obj == "New Command Line":
            tabN = len(self.tabs)
            self.tabs[tabN] = [Frame(tk)]
            self.tabs[tabN].append(Canvas(self.tabs[tabN][0], width=width, height=height-75, bg=tabBackgroundC))
            self.tabs[tabN][0].place(x=0, y=70)
            self.tabs[tabN][1].pack()
            self.tabs[tabN].append(Frame(tk, height=20, width=150))
            self.tabs[tabN][2].pack_propagate(0)
            self.tabs[tabN][2].place(x=tabN*155+5, y=45)
            self.tabs[tabN].append(Button(self.tabs[tabN][2], text="Command Line "+str(tabN), command=lambda : self.show(tabN)))
            self.tabs[tabN][3].pack(fill=BOTH, expand=1)
            self.tabs[tabN].append(Frame(tk, height=20, width=20))
            self.tabs[tabN][4].pack_propagate(0)
            self.tabs[tabN][4].place(x=tabN*155+5+130, y=45)
            self.tabs[tabN].append(Button(self.tabs[tabN][4], text="X", command=lambda : self.closeTab(tabN)))
            self.tabs[tabN][5].pack(fill=BOTH, expand=1)
            tk.update()

    def changeAccuracy(self, a, tabN, coords):
        graph = self.tabs[tabN]
        graph[27] = abs(float(a))
        self.changeBounds(coords, tabN)
        
    
    def changeBounds(self, newBounds, tabN):
        graph = self.tabs[tabN]
        
        maxX = int(newBounds.split(',')[0])
        maxY = int(newBounds.split(',')[1])
        
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

        graph[12].append(graph[10].create_line((width-220)/2, 0, (width-220)/2, (height-95), fill = "black", width=2))
        graph[12].append(graph[10].create_line(0, (height-95)/2, (width-220), (height-95)/2, fill = "black", width=2))

        #Draw Numbers:
        freqX = int(round(maxX/10))

        freqY = int(round(maxY/10))
        
        for x in range(maxX, 2*maxX, freqX):
            graph[12].append(Label(graph[9], text = str(-maxX+x), bg="white"))
            xp = (width-220)/(2*maxX)*(x)-5
            graph[12][-1].place(x=xp, y=(height-95)/2+3)

        for x in range(maxX, 0, -freqX):
            graph[12].append(Label(graph[9], text = str(-maxX+x), bg="white"))
            xp = (width-220)/(2*maxX)*(x)-5
            graph[12][-1].place(x=xp, y=(height-95)/2+3)

        for y in range(maxY, 2*maxY, freqY):
            if maxY == y:
                pass
            else:
                graph[12].append(Label(graph[9], text = str(maxY-y), bg="white"))
                yp = (height-95)/(2*maxY)*(y)-10
                graph[12][-1].place(x=(width-220)/2-20, y=yp)

        for y in range(maxY, 0, -freqY):
            if maxY == y:
                pass
            else:
                graph[12].append(Label(graph[9], text = str(maxY-y), bg="white"))
                yp = (height-95)/(2*maxY)*(y)-10
                graph[12][-1].place(x=(width-220)/2-20, y=yp)
                
        #Draw Grid Lines
        for x in range(maxX, 2*maxX, freqX):
            if maxX == x:
                pass
            else:
                xp = (width-220)/(2*maxX)*(x)
                graph[12].append(graph[10].create_line(xp, 0, xp, (height-95)))

        for x in range(maxX, 0, -freqX):
            if maxX == x:
                pass
            else:
                xp = (width-220)/(2*maxX)*(x)
                graph[12].append(graph[10].create_line(xp, 0, xp, (height-95)))

        for y in range(maxY, 2*maxY, freqY):
            if maxY == y:
                pass
            else:
                yp = (height-95)/(2*maxY)*(y)
                graph[12].append(graph[10].create_line(0, yp, (width-220), yp))


        for y in range(maxY, 0, -freqY):
            if maxY == y:
                pass
            else:
                yp = (height-95)/(2*maxY)*(y)
                graph[12].append(graph[10].create_line(0, yp, (width-220), yp))
        #end graph features
        tk.update()
    
    def drawGraph(self, func, tabN, maxX, maxY, prompt):
        graph = self.tabs[tabN]

        if prompt != "null":
            graph[21][prompt] = func

        color = colors[prompt-1]
        
        if '=' not in func:
            dx = 2*maxX/(width-220)
            mx = (width-220)/(2*maxX)
            my = (height-95)/(2*maxY)
            x = -maxX
            lastx = -maxX
            lasty = -sympy.N(func.replace('x', '('+str(x)+')'))
            while x<maxX:
                x += graph[27]*dx
                y = -sympy.N(func.replace('x', '('+str(x)+')'))
                if abs(y) > maxY*1.1:
                    pass
                elif "I" in str(y):
                    pass
                elif "I" in str(lasty):
                    pass
                else:
                    graph[11].append(graph[10].create_line(lastx*mx+(width-220)/2, lasty*my+(height-95)/2, x*mx+(width-220)/2, y*my+(height-95)/2, fill = color))
                lastx = x
                lasty = y
                
    
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
            self.tabs[i][2].place(x=i*155+5, y=45)
            self.tabs[i][4].place(x=i*155+5+130, y=45)
            self.tabs[i][3].config(command=lambda : self.show(i))
            self.tabs[i][5].config(command=lambda : self.closeTab(i))
        tk.update()
            
            
    
    def show(self, tabN):
        self.tabs[tabN][0].tkraise()
        tk.update()
            
class tabBar:
    def __init__(self):
        self.shape = canvas.create_rectangle(-10, 40, width+10, 75, fill=tabBarC)
        
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



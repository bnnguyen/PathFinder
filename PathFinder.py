import tkinter as tk
import tkinter.font
import math
from tkinter import ttk
from ctypes import windll
from collections import defaultdict
import time

window = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)
window.title('PATHFINDER')
window.resizable(width=False, height=False)
window.state("zoomed")

Custom_font = tk.font.Font( family = "Courier", size = 12, weight='bold')
style=ttk.Style()
style.configure('TButton', font=('Courier', 12, 'bold'))
style.map('design1.Toolbutton', relief="sunken", background=[('selected', 'green'), ('!disabled','white')], foreground=[('selected', 'pink'), ('active','blue'), ('!disabled','blue')], font=[('selected',Custom_font),('!disabled',Custom_font)])

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight
graph = Graph()

mazeWidth= 1776
mazeHeight= 888
size= 37
MazeBackground= 'paleturquoise'
SelectedCells='white'
NonSelectedCells= 'paleturquoise'
GridLine='gray20'
PointStart='green'
PointEnd='red'
SelectImport='lime'
pointSize=4

numRow = int(mazeHeight/size)
numColumn = int(mazeWidth/size)
selectedCell = [[0]*(numColumn+1) for i in range(numRow+1)]
mazeVertex = []
allPath = []
penState=tk.StringVar(value='Maze')
mouseSecondary=tk.IntVar(value=0)
MazeSecondary=0
PointSecondary=0
Var_repeatCopy= tk.IntVar(value=1)
mouseTrace=tk.IntVar(value=0)
showGrid=tk.IntVar(value=1)
showVertex=tk.IntVar(value=0)
showPath=tk.IntVar(value=0)
showBorder=tk.IntVar(value=0)
showSolution=tk.IntVar(value=0)
gridSize=tk.IntVar(value=100)
lastMouseX, lastMouseY = 0, 0
startPointX, startPointY, endPointX, endPointY = -1, -1, -1, -1
mouseNum=0
lastPasteRow, lastPasteColumn = 0, 0

Debug_BorderVertexButton = ttk.Checkbutton(
    master=window,
    text='SHOW VERTEX',
    style='design1.Toolbutton',
    command=lambda:drawLine(),
    variable=showVertex,
    onvalue=1,
    offvalue=0
)
Debug_BorderVertexButton.place(x=800, y=10)

Debug_BorderPathButton = ttk.Checkbutton(
    master=window,
    text='SHOW VISIBILITY GRAPH',
    style='design1.Toolbutton',
    command=lambda:drawLine(),
    variable=showPath,
    onvalue=1,
    offvalue=0
)
Debug_BorderPathButton.place(x=800, y=50)

Debug_SolutionButton = ttk.Checkbutton(
    master=window,
    text='FIND SHORTEST PATH',
    style='design1.Toolbutton',
    command=lambda:drawLine(),
    variable=showSolution,
    onvalue=1,
    offvalue=0
)
Debug_SolutionButton.place(x=1050, y=10)

Maze_AddMapButton = ttk.Button(
    master=window,
    text='ADD MAP',
    style='design1.Toolbutton',
    command=lambda:(PastePattern(lastPasteRow,lastPasteColumn))
)

timerProcessing = ttk.Label(
    window,
    text='',
    font=('Courier',12),
    foreground="red"
)
timerProcessing.place(x=1400,y=10)

VcountLabel = ttk.Label(
    window,
    text='Number of verticles: 0\nNumber of edges: 0',
    font=('Courier',12),
    foreground="red"
)
VcountLabel.place(x=300, y=10)

repeatCopyButton = ttk.Spinbox(
    window,
    from_=1,
    to=9,
    state='readonly',
    textvariable=Var_repeatCopy,
)
Maze_AddMapButton.place(x=30, y=10)
repeatCopyButton.place(x=50, y=50)

howToUse = ttk.Label(
    window,
    text="Left click for start point, right click for end point",
    font=Custom_font,
    wraplength=300
)
howToUse.place(x=1050,y=40)

brg = tk.Canvas(
    master=window,
    height= mazeHeight+40,
    width= mazeWidth+40,
    bg=MazeBackground
)
brg.place(x=30, y=80)

maze = tk.Canvas(
    master=brg,
    height= mazeHeight,
    width= mazeWidth,
    bg=NonSelectedCells,
    border=0,
    borderwidth=0,
    highlightbackground="black",
    highlightthickness=0
)
maze.place(relx=0.5, rely=0.5, anchor='center')

def drawGrid():
    maze.delete('gridLine')
    global showGrid
    if showGrid.get()==1:
        for a in range(size, mazeWidth, size):
            maze.create_line(a, 0, a, mazeHeight, fill=GridLine,tags='gridLine')
        for b in range(size, mazeHeight, size):
            maze.create_line(0, b, mazeWidth, b, fill=GridLine,tags='gridLine')

def drawLine():
    global mazeVertex, showPath, showVertex, showBorder, showSolution
    maze.delete('Visual_Vertex')
    mazeVertex = []
    for row in range(0,numRow):
        for column in range(0,numColumn):
            if selectedCell[row][column]==1:
                    # outer Vertex
                if selectedCell[row - 1][column] == 0 and selectedCell[row][column - 1] == 0: mazeVertex.append([row, column])
                if selectedCell[row - 1][column] == 0 and selectedCell[row][column + 1] == 0: mazeVertex.append([row, column + 1])
                if selectedCell[row + 1][column] == 0 and selectedCell[row][column - 1] == 0: mazeVertex.append([row + 1, column])
                if selectedCell[row + 1][column] == 0 and selectedCell[row][column + 1] == 0: mazeVertex.append([row + 1, column + 1])
                if selectedCell[row - 1][column] == 1 and selectedCell[row][column - 1] == 1 and selectedCell[row - 1][column - 1] == 0: mazeVertex.append([row, column])
                if selectedCell[row - 1][column] == 1 and selectedCell[row][column + 1] == 1 and selectedCell[row - 1][column + 1] == 0: mazeVertex.append([row, column + 1])
                if selectedCell[row + 1][column] == 1 and selectedCell[row][column - 1] == 1 and selectedCell[row + 1][column - 1] == 0: mazeVertex.append([row + 1, column])
                if selectedCell[row + 1][column] == 1 and selectedCell[row][column + 1] == 1 and selectedCell[row + 1][column + 1] == 0: mazeVertex.append([row + 1, column + 1])
    if showVertex.get() == 1:
        vcnt = 0
        for i in range(len(mazeVertex)):
            row, column = mazeVertex[i]
            vcnt += 1
            maze.create_oval(column * size - 3, row * size - 3, column * size + 3, row * size + 3,fill='red', width=0, tags='Visual_Vertex')
        VcountLabel.configure(text = "Number of verticles: " + str(vcnt) + '\nNumber of edges: ' + str(vcnt))
    if showPath.get() == 1 or showSolution.get() == 1:
        drawVisual_Path()
    maze.tag_raise('Visual_Path_Point'); maze.tag_raise('Visual_Vertex'); maze.tag_raise('Visual_Border')
    maze.tag_raise('Start'); maze.tag_raise('End')

def drawVisual_Path():
    ProcessingTimer = time.time()
    maze.delete('Visual_Path')
    global mazeVertex, mazePath, allPath, showPath, showSolution, graph
    allPath=[]
    local_startX, local_startY = round(startPointX / size,1), round(startPointY / size,1)
    local_endX, local_endY = round(endPointX / size,1), round(endPointY / size,1)
    if startPointX != -1 and startPointY != -1 and endPointX != -1 and endPointY != -1:
        if legitPath(local_startX, local_startY, local_endX, local_endY, floatMode=1) == True:
            if showPath.get() == 1: maze.create_line(startPointX, startPointY, endPointX, endPointY, fill='gray', width=1,tags='Visual_Path')
            distance=math.sqrt((local_startX-local_endX)**2 + (local_startY-local_endY)**2)
            allPath.append([-2,-1,distance])
    if startPointX!=-1 and startPointY!=-1:
        for i in range(len(mazeVertex)):
            y0, x0 = mazeVertex[i]
            if legitPath(x0,y0,local_startX,local_startY,floatMode=1)==True:
                if showPath.get() == 1: maze.create_line(x0 * size, y0 * size, startPointX, startPointY, fill='gray', width=1, tags='Visual_Path')
                distance = math.sqrt((local_startX - x0) ** 2 + (local_startY - y0) ** 2)
                allPath.append([-2, i, distance])
    for i in range(len(mazeVertex)):
        y0, x0 = mazeVertex[i]
        for j in range(i+1,len(mazeVertex)):
            y1, x1 = mazeVertex[j]
            if legitPath(x0,y0,x1,y1)==True:
                if showPath.get() == 1: maze.create_line(x0 * size, y0 * size, x1 * size,y1 * size,fill='gray',width=1,tags='Visual_Path')
                distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
                allPath.append([i, j, distance])
    if endPointX!=-1 and endPointY!=-1:
        for i in range(len(mazeVertex)):
            y0, x0 = mazeVertex[i]
            if legitPath(x0,y0,local_endX,local_endY,floatMode=1)==True:
                if showPath.get() == 1: maze.create_line(x0 * size, y0 * size, endPointX, endPointY, fill='gray', width=1, tags='Visual_Path')
                distance = math.sqrt((local_endX - x0) ** 2 + (local_endY - y0) ** 2)
                allPath.append([i, -1, distance])
    graph = Graph()
    for edge in allPath:
        graph.add_edge(*edge)
    solutionList = dijsktra(graph, -2, -1)
    if solutionList ==0 : return 0
    x0, y0 = startPointX, startPointY
    plen=0.0
    if showSolution.get() == 1 and startPointX != -1 and startPointY != -1 and endPointX != -1 and endPointY != -1:
        for i in range(1,len(solutionList)):
            if solutionList[i]==-1: x1,y1 = endPointX, endPointY
            else:
                y1, x1 = mazeVertex[solutionList[i]]
                x1=x1*size; y1=y1*size
            maze.create_line(x0,y0,x1,y1, fill='yellow', width=3, tags='Visual_Path')
            plen += math.sqrt((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))/size
            x0,y0=x1,y1
        ProcessingTimer = time.time() - ProcessingTimer
        timerProcessing.configure(
            text='Lastest Processing Time: ' + str(round(ProcessingTimer, 2)) + ' s' + '\n' + 'Shortest Path Length: ' + str(round(plen,2)) + '\n')


def dijsktra(graph, initial, end):
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]
        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return 0
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


def legitPath(x0,y0,x1,y1,floatMode=0):
    if (y0 > y1): y0, y1 = y1, y0; x0, x1 = x1, x0
    dx = round(x1 - x0, 2)
    dy = round(y1 - y0, 2)
    steps = max(abs(dx), abs(dy))
    if dx == 0 and float(x0).is_integer():
        for i in range(int(y1) - int(y0) + int(float(y1).is_integer() == False)):
            if selectedCell[int(y0) + i][int(x0)]==0 and selectedCell[int(y0) + i][int(x0) - 1]==0: return False
        return True
    if dy == 0 and float(y0).is_integer():
        if dx < 0: dx = -dx; x0, x1 = x1, x0
        for i in range(int(x1) - int(x0) + int(float(x1).is_integer() == False)):
            if selectedCell[int(y0)][int(x0) + i]==0 and selectedCell[int(y0) - 1][int(x0) + i]==0: return False
        return True
    if floatMode == 1 and (x0 != x1 or float(x0).is_integer() == False) and (y0 != y1 or float(y0).is_integer() == False):
        xL = float(min(x0, x1)); xH = float(max(x0, x1))
        yL = float(min(y0, y1)); yH = float(max(y0, y1))
        if int(xL) == int(xH) and int(yL) == int(yH):
            if selectedCell[int(yL)][int(xL)] == 0: return False
            return True
        if xH.is_integer() == True: xH -= 1
        if yH.is_integer() == True: yH -= 1
        if int(xL) == int(xH) and int(yL) == int(yH):
            if selectedCell[int(yL)][int(xL)] == 0: return False
            return True
    if floatMode == 1:
        corx0 = int(x0); cory0 = int(y0)
        corx1 = int(x1); cory1 = int(y1)
        if corx0 == corx1 and cory0 == cory1:
            if selectedCell[cory0][corx0] == 0: return False
        x0 = float(x0); y0 = float(y0)
        x1 = float(x1); y1 = float(y1)

        if steps == dx:
            if selectedCell[cory0][corx0] == 0: return False
            xR = int(x0) + 1
            yR = y0 + dy * ((xR - x0) / dx)
            x0 = xR; y0 = yR
            if x1.is_integer() == False:
                if y1.is_integer() == False:
                    if selectedCell[cory1][corx1] == 0: return False
                else:
                    if selectedCell[cory1 - 1][corx1] == 0: return False
                xR = int(x1)
            else:
                if y1.is_integer() == False:
                    if selectedCell[cory1][corx1 - 1] == 0: return False
                else:
                    if selectedCell[cory1 - 1][corx1 - 1] == 0: return False
                xR = int(x1) - 1
            yR = y1 + dy * ((xR - x1) / dx)
            x1 = xR; y1 = yR
            if float(round(y1, 2)).is_integer() == False:
                if selectedCell[int(y1)][int(x1) - 1] ==0 or selectedCell[int(y1)][int(x1)] == 0: return False

        elif steps == -dx:
            if x0.is_integer() == False:
                if selectedCell[cory0][corx0] == 0: return False
                xR = int(x0)
            else:
                if selectedCell[cory0][corx0 - 1] == 0: return False
                xR = int(x0) - 1
            yR = y0 + dy * ((xR - x0) / dx)
            x0 = xR; y0 = yR
            if y1.is_integer() == False:
                if selectedCell[cory1][corx1] == 0: return False
            else:
                if selectedCell[cory1 - 1][corx1] == 0: return False
            xR = int(x1) + 1
            yR = y1 + dy * ((xR - x1) / dx)
            x1 = xR; y1 = yR
            if float(round(y1, 2)).is_integer() == False:
                if selectedCell[int(y1)][int(x1) - 1] == 0 or selectedCell[int(y1)][int(x1)] == 0: return False
        elif steps == dy:
            if dx < 0 and x0.is_integer() == True:
                if selectedCell[cory0][corx0 - 1] == 0: return False
            else:
                if selectedCell[cory0][corx0] == 0: return False
            yR = int(y0) + 1
            xR = x0 + dx * ((yR - y0) / dy)
            x0 = xR; y0 = yR
            if y0 <= int(y1):
                if y1.is_integer() == False:
                    if x1.is_integer() == False:
                        if selectedCell[cory1][corx1] == 0: return False
                    yR = int(y1)
                else:
                    if x1.is_integer() == False:
                        if selectedCell[cory1 - 1][corx1] == 0: return False
                    yR = int(y1)
                xR = x1 + dx * ((yR - y1) / dy)
                if float(xR).is_integer() == False and float(y1).is_integer() == False:
                    if selectedCell[int(yR)][int(xR)] == 0 or selectedCell[int(yR) - 1][int(xR)] == 0: return False
                x1 = xR; y1 = yR
            else:
                if float(x1).is_integer(): x1 -= 1
                if float(y1).is_integer(): y1 -= 1
                if selectedCell[int(y1)][int(x1)] == 0: return False
                return True
    x0 = float(round(x0, 2))
    y0 = float(round(y0, 2))
    x1 = float(round(x1, 2))
    y1 = float(round(y1, 2))
    if float(x0).is_integer(): x0 = int(x0)
    if float(y0).is_integer(): y0 = int(y0)
    if float(x1).is_integer(): x1 = int(x1)
    if float(y1).is_integer(): y1 = int(y1)
    if x0 == x1 and y0 == y1: return True
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))
    xinc = dx / steps
    yinc = dy / steps
    x = float(round(x0, 3))
    y = float(round(y0, 3))
    for i in range(steps):
        corx = int(x)
        cory = int(y)
        if dx == dy:
            if selectedCell[cory][corx] == 0: return False
            if dx - int(dx) != 0 and dy - int(dy) != 0:
                if selectedCell[cory + 1][corx] == 0: return False
            if x.is_integer() == False or y.is_integer() == False:
                if selectedCell[cory][corx - 1] == 0: return False
        elif dx == -dy:
            if selectedCell[cory][corx - 1] == 0: return False
            if dx - int(dx) != 0 and dy - int(dy) != 0:
                if selectedCell[cory + 1][corx] == 0: return False
            if x.is_integer() == False or y.is_integer() == False:
                if selectedCell[cory][corx] == 0: return False
        elif steps == abs(dx):
            if round(y, 8).is_integer() == False:
                if selectedCell[cory][corx] == 0: return False
                if int(x) - int(x + xinc) != 0:
                    if selectedCell[cory][corx - 1] == 0: return False
        elif steps == dy:
            if round(x, 2).is_integer() == False:
                if selectedCell[cory][corx] == 0: return False
                if int(y) - int(y + yinc) != 0:
                    if selectedCell[cory - 1][corx] == 0: return False
        x = round(x + xinc, 3)
        y = round(y + yinc, 3)
    return True

def LeftMouseAction(event):
    x, y = maze.winfo_pointerx() - maze.winfo_rootx(), maze.winfo_pointery() - maze.winfo_rooty()
    global mouseNum, startPointX, startPointY, endPointX, endPointY, pointSize
    if (x >= 0) and (y >= 0) and (x <= mazeWidth-1) and (y <= mazeHeight-1):
        if (penState.get()=='Point'):
            row = int(y / size); column = int(x / size)
            if selectedCell[row][column]==1:
                if mouseSecondary.get() == mouseNum:
                    startPointX, startPointY = x, y
                    maze.delete('Start')
                    maze.create_oval(x + pointSize, y + pointSize, x - pointSize, y - pointSize, fill=PointStart, tags='Start')
                else:
                    endPointX, endPointY = x, y
                    maze.delete('End')
                    maze.create_oval(x + pointSize, y + pointSize, x - pointSize, y - pointSize, fill=PointEnd, tags='End')
                drawLine()


def LeftMouseUp(event):
    maze.delete('Cell')
    for x in range(0, mazeWidth, size):
        for y in range(0, mazeHeight, size):
            row = int(y / size);column = int(x / size)
            if selectedCell[row][column]==1: maze.create_rectangle(x, y, x + size, y + size, fill=SelectedCells, outline='', tags='Cell')
    global mouseNum
    mouseNum=0 if event.num==3 else 1
    maze.tag_lower('Cell')
    maze.delete('debug')

def LeftMouseDown(event):
    global mouseNum, startPointX, startPointY, endPointX, endPointY, pointSize
    mouseNum=0 if event.num==1 else 1
    x, y = maze.winfo_pointerx() - maze.winfo_rootx(), maze.winfo_pointery() - maze.winfo_rooty()
    if (x >= 0) and (y >= 0) and (x <= mazeWidth - 1) and (y <= mazeHeight - 1):
        if (penState.get() == 'Point'):
            row = int(y / size);
            column = int(x / size)
            if selectedCell[row][column] == 1:
                if mouseSecondary.get() == mouseNum:
                    startPointX, startPointY = x, y
                    maze.delete('Start')
                    maze.create_oval(x + pointSize, y + pointSize, x - pointSize, y - pointSize, fill=PointStart,tags='Start')
                else:
                    endPointX, endPointY = x, y
                    maze.delete('End')
                    maze.create_oval(x + pointSize, y + pointSize, x - pointSize, y - pointSize, fill=PointEnd,tags='End')
                drawGrid()
                drawLine()

def PastePattern(reRow,reColumn):
    x, y = maze.winfo_pointerx() - maze.winfo_rootx(), maze.winfo_pointery() - maze.winfo_rooty()
    if (x >= 0) and (y >= 0) and (x <= mazeWidth-1) and (y <= mazeHeight-1) or reRow!=-1:
        for i in range(int(repeatCopyButton.get())):
            global numRow, numColumn, lastPasteRow, lastPasteColumn
            if reRow != -1 and reColumn != -1:
                row = lastPasteRow
                column = lastPasteColumn
            else: row = int(y / size);column = int(x / size)
            iarr = [[1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                    ]
            for i in range(len(iarr)):
                if row + i >= numRow: break
                for j in range(len(iarr[0])):
                    if column+j>=numColumn: break
                    selectedCell[row+i][column+j]=iarr[i][j]
            if row+len(iarr) < numRow and column+len(iarr[0]) < numColumn:
                lastPasteRow=row+len(iarr)
                lastPasteColumn=column+len(iarr[0])-1
            reRow=0
            reColumn=0
        drawLine()

window.bind("<ButtonRelease-1>",LeftMouseUp)
window.bind("<ButtonRelease-3>",LeftMouseUp)
window.bind("<ButtonPress-1>",LeftMouseDown)
window.bind("<ButtonPress-3>",LeftMouseDown)

lastPasteColumn, lastPasteRow = 0 , 0
numRow = int(mazeHeight / size)
numColumn = int(mazeWidth / size)
selectedCell = [[0] * (numColumn+1) for i in range(numRow+1)]
maze.delete('all')
drawGrid()
startPointX, startPointY, endPointX, endPointY = -1,-1,-1,-1
def slider_changed(event):
    global size, numRow, numColumn, endPointX, endPointY, startPointX, startPointY
    startPointX = float(startPointX)/size*int(changeSizeSlider.get())
    startPointY = float(startPointY)/size*int(changeSizeSlider.get())
    endPointX = float(endPointX)/size*int(changeSizeSlider.get())
    endPointY = float(endPointY)/size*int(changeSizeSlider.get())
    size = int(changeSizeSlider.get())
    numRow = int(mazeHeight / size)
    numColumn = int(mazeWidth / size)
    maze.delete('Start')
    maze.create_oval(startPointX + pointSize, startPointY + pointSize, startPointX - pointSize, startPointY - pointSize, fill=PointStart, tags='Start')
    maze.delete('End')
    maze.create_oval(endPointX + pointSize, endPointY + pointSize, endPointX - pointSize, endPointY - pointSize, fill=PointEnd, tags='End')
    drawLine()
    drawGrid()

changeSizeSlider = ttk.Scale(
    window,
    from_=37,
    to=100,
    length=400,
    orient='horizontal',
    command=slider_changed
)
changeSizeSlider.set(37)
changeSizeSlider.place(x=1400, y=50)
Maze_ClearButton = ttk.Button(
    master = window,
    text = 'CLEAR MAP',
    style = 'design1.Toolbutton',
    command = lambda:ClearMap()
)
Maze_ClearButton.place(x = 130, y = 10)

def ClearMap():
    maze.delete('Cell', 'End', 'Start', 'Visual_Path', 'Visual_Path_Point', 'Visual_Vertex', 'Visual_Border')
    maze.itemconfigure('Cell', fill='paleturquois', outline='gray20')
    global selectedCell, lastPasteRow, lastPasteColumn, mazeVertex, showBorder, startPointX, startPointY, endPointX, endPointY
    selectedCell = [[0] * (numColumn + 1) for i in range(numRow + 1)]
    lastPasteRow, lastPasteColumn = 0, 0
    mazeVertex = []
    showBorder = tk.IntVar(value=0)
    startPointX, startPointY, endPointX, endPointY = -1, -1, -1, -1
maze.tag_raise('outline')
penState.set('Point')
window.mainloop()

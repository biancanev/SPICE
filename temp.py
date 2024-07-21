import numpy as np

WF_DC = 0
WF_AC = 1
WF_SQUARE = 2

class CircuitElement:
    def __init__(self, x:int, y:int, w:int, h:int, file_name:str, index:int):
        self.x, self.y, self.w, self.h, self.index = x, y, w, h, index
        self.file_name = file_name
        self.voltage, self.current = 0, 0

    def simulate(self) -> tuple[int, int]:
        return (self.voltage, self.current)

class Node:
    def __init__(self, index:int):
        self.index = index
        self.changed = False
        self.elements: list[CircuitElement] = []
        self.voltage = int()
        self.coordinates = list[tuple[int, int]]

class TwoPinElement(CircuitElement):
    def __init__(self, x:int, y:int, w:int, h:int, file_name:str, index:int):
        super().__init__(x, y, w, h, file_name, index)
        self.topConnection = Node("")
        self.bottomConnection = Node("")
    
    def connectToNode(self, pin:int, node:Node):
        if pin == 0:
            self.topConnection = node
        elif pin == 1:
            self.bottomConnection = node
        else:
            raise "Invalid pin number"


class Ground(Node):
    def __init__(self, index:int):
        super().__init__(index)
        self.node = 0
        self.changed = True


class Resistor(TwoPinElement):
    def __init__(self, x:int, y:int, w:int, h:int, index:int, res:float=0, tol:float=0):
        super().__init__(x, y, w, h, "", index)
        self.resistance, self.tolerance = res, tol

    def simulate(self) -> tuple[int, int]:
        self.voltage = abs(self.topConnection.voltage) - abs(self.bottomConnection.voltage)
        self.current = self.voltage / self.resistance
        return (self.voltage, self.current)
    
    def getName(self) -> str:
        return "R" + str(self.index)
    
class VoltageSource(TwoPinElement):
    def __init__(self, x:int, y:int, w:int, h:int, wf:int, index:int, v:int):
        match wf:
            case 0:
                file_name = "elements/VoltageSource.svg.png"
            case 1:
                file_name = ""
            case _:
                file_name = "elements/VoltageSource.svg.png"
        super().__init__(x, y, w, h, file_name, index)
        self.voltage = v

    def simulate(self) -> tuple[int, int]:
        self.current = 0
        self.topConnection.voltage = self.bottomConnection.voltage + self.voltage
        self.topConnection.changed = True
        return self.voltage, self.current
    def getName(self) -> str:
        return "V" + str(self.index)

class Circuit:
    def __init__(self):
        self.elements = []
        self.nodes = []

    def addElement(self, element:CircuitElement):
        self.elements.append(element)

    def addNode(self, node):
        self.nodes.append(node)

    #Note: pin = 0 is +, pin = 1 is -
    def connectElementtoNode(self, elementIndex, nodeIndex, pin):
        if pin == 0:
            self.elements[elementIndex].topConnection = self.nodes[nodeIndex]
        elif pin == 1:
            self.elements[elementIndex].bottomConnection = self.nodes[nodeIndex]
        self.nodes[nodeIndex].elements.append(self.elements[elementIndex])
    
    def simulate(self):
        #find all known nodes
        A = np.zeros((len(self.nodes), len(self.nodes)))
        b = np.zeros((len(self.nodes), 1))
        #use KCL equation for each node and substitute into the matrix
        row = 0
        for node in self.nodes:
            if type(node) == Ground:
                A[row][node.index] = 1
                b[node.index][0] = 0
                break
            ignore = False
            for element in node.elements:
                other, side = element.bottomConnection.index, 1 if element.topConnection.index == node.index else element.topConnection.index, 0
                if type(element) == VoltageSource:
                    element.simulate()
                    b[row][0] = element.voltage if element.voltage > b[row][0] else b[row][0]
                    A[row][node.index] = 1
                    ignore = True
                elif type(element) == Resistor and not ignore:
                    print(node, element.topConnection, element.bottomConnection, self.nodes[other])
                    A[row][node.index] += 1 / element.resistance
                    b[row][0] += element.topConnection.voltage / element.resistance 
                elif type(element) == Ground:
                    b[row][0] = 0
                    A[row][node.index] = 1
            row += 1
        print("A:", A)
        print("b:", b)
        #solve the matrix
        x = np.linalg.solve(A, b)
        #substitute values into corresponding nodes
        print("x:", x)
        print(self.nodes)
        for nodeIndex in range(len(A)):
            self.nodes[nodeIndex].voltage = x[nodeIndex][0]
        #solve for unknown element voltages and currents
        self.outputValues()

    def outputValues(self):
        for element in self.elements:
            if type(element) != VoltageSource:
                res = element.simulate()
                v, i = res[0], res[1]
                print("Element: {0}, V = {1}, I = {2}".format(element.getName(), v, i)) #need to change naming scheme later

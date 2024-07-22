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
        self.known = False
        self.elements: list[CircuitElement] = []
        self.voltage = 0
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
        self.known = True


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
        self.topConnection.known = True
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

    def connectNodetoNode(self, node1, node2):
        node1.elements = [*node1.elements, *node2.elements] #concat node 2's elements into node 1
        for element in node2.elements: #set the relevant connections of elements in node 2 to node 1
            if element.topConnection == node2:
                element.topConnection = node1
            else:
                element.bottomConnection = node1
        for node in self.nodes[node2.index::1]: #reindex all nodes above the node
            node.index -= 1
        self.nodes.remove(node2) #delete node 2
        del node2
    
    def simulate(self):
        #find all known nodes
        A = np.zeros((len(self.nodes), len(self.nodes)))
        b = np.zeros((len(self.nodes), 1))
        #use KCL equation for each node and substitute into the matrix
        for element in self.elements:
            if type(element) == VoltageSource:
                element.simulate()
        row = 0
        for node in self.nodes:
            if node.known:
                A[row][node.index] = 1
                b[row][0] = node.voltage
            else:
                usedKnownNodes = []
                for element in node.elements:
                    otherNode = element.bottomConnection if element.topConnection == node else element.topConnection
                    if type(element) == Resistor:
                        A[row][node.index] += 1 / element.resistance
                        A[row][otherNode.index] -= 1 / element.resistance if not otherNode.known else 0
                        if otherNode.known and otherNode not in usedKnownNodes:
                            b[row][0] += otherNode.voltage / element.resistance
                            usedKnownNodes.append(otherNode)
            row += 1
        #solve the matrix
        x = np.linalg.solve(A, b)
        #substitute values into corresponding nodes
        for nodeIndex in range(len(A)):
            self.nodes[nodeIndex].voltage = x[nodeIndex][0]
        #solve for unknown element voltages and currents
        self.outputValues()

    def outputValues(self):
        for element in self.elements:
            if type(element) != VoltageSource:
                res = element.simulate()
                v, i = res[0], res[1]
                #print("Element: {0}, V = {1}, I = {2}".format(element.getName(), v, i)) #need to change naming scheme later

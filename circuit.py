import numpy as np

WF_DC = 0
WF_AC = 1
WF_SQUARE = 2

class CircuitElement:
    def __init__(self, x:int, y:int, w:int, h:int, file_name:str, index:int):
        self.x, self.y, self.w, self.h, self.index= x, y, w, h, index
        self.file_name = file_name
        self.voltage, self.current = 0, 0

    def simulate(self) -> tuple[int, int]:
        return (self.voltage, self.current)

class Node:
    def __init__(self, index):
        self.index = index
        self.elements = list[CircuitElement]
        self.voltage = int()

class TwoPinElement(CircuitElement):
    def __init__(self, x:int, y:int, w:int, h:int, file_name:str, index: int):
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
    def __init__(self, index):
        super().__init__(index)
        self.node = 0


class Resistor(TwoPinElement):
    def __init__(self, x:int, y:int, w:int, h:int, index:int, res:float=0, tol:float=0):
        super().__init__(x, y, w, h, "", index)
        self.resistance, self.tolerance = res, tol

    def simulate(self) -> tuple[int, int]:
        self.voltage = self.topConnection.voltage - self.bottomConnection.voltage
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
        
        #self.nodes[nodeIndex].elements.append(self.elements[elementIndex])
    
    def simulate(self):
        for element in self.elements:
            res = element.simulate()
            v, i = res[0], res[1]
            print("Element: {0}, V = {1}, I = {2}".format(element.getName(), v, i))



#Just for testing...
circuit = Circuit()

v1 = VoltageSource(0, 0, 2, 4, WF_DC, 1, 5)
circuit.addElement(v1)
r1 = Resistor(4, 0, 2, 4, 1, 10)
circuit.addElement(r1)
u1 = Node("u1")
circuit.addNode(u1)
gnd = Ground("gnd")
circuit.addNode(gnd)
circuit.connectElementtoNode(circuit.elements.index(v1), circuit.nodes.index(u1), 0)
circuit.connectElementtoNode(circuit.elements.index(v1), circuit.nodes.index(gnd), 1)
circuit.connectElementtoNode(circuit.elements.index(r1), circuit.nodes.index(u1), 0)
circuit.connectElementtoNode(circuit.elements.index(r1), circuit.nodes.index(gnd), 1)

circuit.simulate()




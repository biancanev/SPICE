import numpy as np
import unittest

#Add Tests to ensure all functionality works
class DC_Analysis_Test(unittest.TestCase):
    def test_ohms_law(self):
        circuit = Circuit()
        v1 = VoltageSource(0, 0, 2, 4, WF_DC, 0, 5)
        circuit.addElement(v1)
        r1 = Resistor(4, 0, 2, 4, 1, 10)
        circuit.addElement(r1)
        u1 = Node(0)
        circuit.addNode(u1)
        gnd = Ground(1)
        circuit.addNode(gnd)
        circuit.connectElementtoNode(circuit.elements.index(v1), circuit.nodes.index(u1), 0)
        circuit.connectElementtoNode(circuit.elements.index(v1), circuit.nodes.index(gnd), 1)
        circuit.connectElementtoNode(circuit.elements.index(r1), circuit.nodes.index(u1), 0)
        circuit.connectElementtoNode(circuit.elements.index(r1), circuit.nodes.index(gnd), 1)

        circuit.simulate()
        self.assertEqual(v1.voltage, 5)
        self.assertEqual(r1.voltage, 5)
        self.assertEqual(r1.current, 0.5)
    
    def test_nodal_analysis(self):
        circuit2 = Circuit()
        v1 = VoltageSource(0, 0, 2, 4, WF_DC, 0, 5)
        r1 = Resistor(4, 0, 2, 4, 1, 2)
        circuit2.addElement(v1)
        circuit2.addElement(r1)
        r2 = Resistor(4, 0, 2, 4, 2, 2)
        r3 = Resistor(4, 0, 2, 4, 3, 4)
        circuit2.addElement(r2)
        circuit2.addElement(r3)
        u1 = Node(0)
        u2 = Node(1)
        gnd = Ground(2)
        circuit2.addNode(u1)
        circuit2.addNode(u2)
        circuit2.addNode(gnd)
        circuit2.connectElementtoNode(circuit2.elements.index(v1), circuit2.nodes.index(u1), 0)
        circuit2.connectElementtoNode(circuit2.elements.index(v1), circuit2.nodes.index(gnd), 1)
        circuit2.connectElementtoNode(circuit2.elements.index(r1), circuit2.nodes.index(u1), 0)
        circuit2.connectElementtoNode(circuit2.elements.index(r1), circuit2.nodes.index(u2), 1)
        circuit2.connectElementtoNode(circuit2.elements.index(r2), circuit2.nodes.index(u2), 0)
        circuit2.connectElementtoNode(circuit2.elements.index(r2), circuit2.nodes.index(gnd), 1)
        circuit2.connectElementtoNode(circuit2.elements.index(r3), circuit2.nodes.index(u2), 0)
        circuit2.connectElementtoNode(circuit2.elements.index(r3), circuit2.nodes.index(gnd), 1)

        circuit2.simulate()
        self.assertEqual(abs(r1.current), (5-2/3)/2)
        self.assertEqual(abs(r1.voltage), 5 - 2/3)
        self.assertEqual(abs(r2.current), 2)
        self.assertEqual(abs(r2.voltage), 4)
        self.assertEqual(abs(r3.current), 2/3/4)
        self.assertEqual(abs(r3.voltage), 2/3)

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
            col = 0
            print(node.elements)
            for element in node.elements:
                print(row, col, ":", node, element)
                if type(element) == VoltageSource:
                    print("VS")
                    A[row][element.index] += element.voltage
                    b[row][0] += element.voltage
                elif type(element) == Resistor:
                    print("R")
                    A[row][node.index] += 1 / element.resistance
                col += 1
            row += 1
        print(A)
        print(b)
        #solve the matrix
        x = np.linalg.solve(A, b)
        #substitute values into corresponding nodes
        print(x)
        print(self.nodes)
        for nodeIndex in range(len(A)):
            self.nodes[nodeIndex].voltage = x[nodeIndex][0]
        #solve for unknown element voltages and currents
        self.outputValues()

    def outputValues(self):
        for element in self.elements:
            res = element.simulate()
            v, i = res[0], res[1]
            print("Element: {0}, V = {1}, I = {2}".format(element.getName(), v, i)) #need to change naming scheme later

if __name__ == '__main__':
    unittest.main()

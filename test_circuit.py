import unittest
from circuit import *

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
        self.assertEqual(abs(v1.voltage), 5)
        self.assertEqual(abs(r1.voltage), 5)
        self.assertEqual(abs(r1.current), 0.5)
    
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
        self.assertEqual(abs(r1.current), 1.5)
        self.assertEqual(abs(r1.voltage), 3)
        self.assertEqual(abs(r2.current), 1)
        self.assertEqual(abs(r2.voltage), 2)
        self.assertEqual(abs(r3.current), 0.5)
        self.assertEqual(abs(r3.voltage), 2)

    def test_bridge_circuit(self):
        circuit = Circuit()

        v1 = VoltageSource(0,0,0,0, WF_DC, 0, 5)
        r1=Resistor(0,0,0,0,1,1)
        r2=Resistor(0,0,0,0,2,2)
        r3=Resistor(0,0,0,0,3,3)
        r4=Resistor(0,0,0,0,4,4)
        r5=Resistor(0,0,0,0,5,5)
        u1 = Node(0)
        u2 = Node(1)
        u3 = Node(2)
        u4 = Ground(3)
        circuit.addElement(v1)
        circuit.addElement(r1)
        circuit.addElement(r2)
        circuit.addElement(r3)
        circuit.addElement(r4)
        circuit.addElement(r5)
        circuit.addNode(u1)
        circuit.addNode(u2)
        circuit.addNode(u3)
        circuit.addNode(u4)
        circuit.connectElementtoNode(circuit.elements.index(v1), circuit.nodes.index(u1), 0)
        circuit.connectElementtoNode(circuit.elements.index(v1), circuit.nodes.index(u4), 1)
        circuit.connectElementtoNode(circuit.elements.index(r1), circuit.nodes.index(u1), 0)
        circuit.connectElementtoNode(circuit.elements.index(r1), circuit.nodes.index(u2), 1)
        circuit.connectElementtoNode(circuit.elements.index(r2), circuit.nodes.index(u2), 0)
        circuit.connectElementtoNode(circuit.elements.index(r2), circuit.nodes.index(u4), 1)
        circuit.connectElementtoNode(circuit.elements.index(r3), circuit.nodes.index(u1), 0)
        circuit.connectElementtoNode(circuit.elements.index(r3), circuit.nodes.index(u3), 1)
        circuit.connectElementtoNode(circuit.elements.index(r4), circuit.nodes.index(u3), 0)
        circuit.connectElementtoNode(circuit.elements.index(r4), circuit.nodes.index(u4), 1)
        circuit.connectElementtoNode(circuit.elements.index(r5), circuit.nodes.index(u2), 0)
        circuit.connectElementtoNode(circuit.elements.index(r5), circuit.nodes.index(u3), 1)

        circuit.simulate()

        self.assertAlmostEqual(r1.voltage, 1.71, 2)
        self.assertAlmostEqual(r2.voltage, 3.29, 2)
        self.assertAlmostEqual(r3.voltage, 2.03, 2)
        self.assertAlmostEqual(r4.voltage, 2.97, 2)
        self.assertAlmostEqual(r5.voltage, 0.323, 3)
        self.assertAlmostEqual(r1.current, 1.71, 2)
        self.assertAlmostEqual(r2.current, 1.65, 2)
        self.assertAlmostEqual(r3.current, 0.677, 3)
        self.assertAlmostEqual(r4.current, 0.742, 2)
        self.assertAlmostEqual(r5.current, 0.0645, 3)

    def test_node_connection(self):
        circuit = Circuit()
        u1 = Node(0)
        u2 = Node(1)
        u3 = Node(2)
        u4 = Node(3)
        r1 = Resistor(0,0,0,0,0,1)
        r2 = Resistor(0,0,0,0,1,2)
        circuit.addNode(u1)
        circuit.addNode(u2)
        circuit.addNode(u3)
        circuit.addNode(u4)
        circuit.addElement(r1)
        circuit.addElement(r2)
        circuit.connectElementtoNode(r1.index, u1.index, 0)
        circuit.connectElementtoNode(r2.index, u2.index, 0)
        circuit.connectNodetoNode(u1, u2)

        self.assertEqual(len(u1.elements), 2)
        self.assertEqual(u1.elements[1], r2)
        self.assertEqual(len(circuit.nodes), 3)

class DC_Transient_Test(unittest.TestCase):
    def none_right_now(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DC_Analysis_Test('test_ohms_law'))
    suite.addTest(DC_Analysis_Test('test_nodal_analysis'))
    suite.addTest(DC_Analysis_Test('test_bridge_circuit'))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
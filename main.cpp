#include <iostream>
#include "elements/circuit.h"

using namespace std;

int main(){
    Circuit circuit;
    Resistor* r1 = new Resistor(1.0, "r1");
    circuit.addElement(r1);
    VoltageSource* v1 = new VoltageSource(0, 0, 5, WF_DC, "V1");
    return 0;
}

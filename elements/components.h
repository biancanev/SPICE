#ifndef COMPONENTS_H
#define COMPONENTS_H

#define WF_DC 0
#define WF_AC 1
#define WF_SQUARE 2

#include <string>
#include <vector>
using namespace std;


//Define the base element object
class CircuitElement{
    public:
        double x, y, width, height;
        string src, name;
        CircuitElement() = default;
        CircuitElement(string namein){
            x = 0;
            y = 0;
            width = 2;
            height = 4;
            name = namein;
        }
        CircuitElement(int xin, int yin, int win, int hin, string srcin, string name){
            x = xin;
            y = yin;
            width = win;
            height = hin;
            src = srcin;
        }

};

//Define a node struct
class Node{
    public:
        vector<CircuitElement> elements;
        int voltage;
};

//Define resistors
class Resistor : public CircuitElement{
    public:
        double resistance, tolerance = 0;
        Resistor(double res, string name){
            CircuitElement(name);
            resistance = res;
        }
        Resistor(double res, double tol){resistance = res; tolerance = tol;}
};




//Voltage Sources

class VoltageSource : public CircuitElement{
    public:
        double maxVoltage, bias;
        int waveform;
        VoltageSource(int x, int y, int vin, int wf, string name){
            CircuitElement(x, y, 2, 4, "VOLTAGE_SOURCE.svg.png", name);
            waveform = wf;
        }

};

#endif

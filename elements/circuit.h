#ifndef CIRCUIT_H
#define CIRCUIT_H

#include "components.h"

using namespace std;

class Circuit{
    public:
        vector<Node*> nodes;
        vector<CircuitElement*> elements;


        void addElement(CircuitElement* element){
            elements.push_back(element);
        }

        void addWire(CircuitElement el1, CircuitElement el2){
            Node* node = new Node;
            node->elements.push_back(el1);
            node->elements.push_back(el2);
        }

        void addWire(CircuitElement el, Node* node){
            node->elements.push_back(el);
        }

        int simulate(){
            CircuitElement el;
            for(CircuitElement* element : elements){
                el = *element;
                if(typeid(el) == typeid(VoltageSource)){

                }else if(typeid(el) == typeid(Resistor)){

                }
            }
        }

        ~Circuit(){
            for(Node* node : nodes){
                delete node;
                nodes.pop_back();
            }
            for(CircuitElement* element : elements){
                delete element;
                nodes.pop_back();
            }
        }
};

#endif

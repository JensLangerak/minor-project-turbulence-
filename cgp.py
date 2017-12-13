# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 09:46:08 2017

@author: jens
"""
import math

node_size = 3
outputs = 2
operations = 3

def translate(features, solutionList):
 #   print (inputs)
    nr_nodes = math.floor(len(solutionList) / node_size)
    nr_features = len(features);
    operationlist=['+', '-', '*', '/'] #what if division by zero?
    newlist= [0] * len(solutionList)
    if (nr_features > 3):
        print (features)
    for i in range(nr_nodes): #turns numbers into the right numbers/operation
        newlist[node_size*i]=solutionList[node_size*i]%(nr_features+i)
        newlist[node_size*i+1]=solutionList[node_size*i+1]%(nr_features+i)
        newlist[node_size*i+2]=operationlist[solutionList[node_size*i+2]%operations]
    return newlist


def cgp(features, solutionList): #function that interpretes solution in terms of features -> returns two outputs
    nr_nodes = math.floor(len(solutionList) / node_size)
    nr_features = len(features);
    inputs = [None] * (nr_features + nr_nodes) #length of final input features 
    for i in range(len(features)):
        inputs[i] = features[i] #make deep copy of features
    newlist = translate(features, solutionList)
#    print(newlist)
#    print ('begin')
    output1 = calculateInput(newlist, nr_nodes + len(features)- 1, inputs, nr_features)
 #   print (inputs)
    output2 = calculateInput(newlist, nr_nodes + len(features)- 2, inputs, nr_features)
 #   print ('end')

    return [output1,output2]

def calculateInput(newlist, input_id, inputs, nr_features):
    if (inputs[input_id] is not None):
    #    print( "return" , input_id)
        return inputs[input_id]

 #   print( "calc" , input_id)
    node_id = input_id - nr_features

    a_index =newlist[node_size*(node_id)]
    b_index =newlist[node_size*(node_id)+1]

    a = calculateInput(newlist, a_index,inputs, nr_features)
    b = calculateInput(newlist, b_index, inputs, nr_features)
    o = newlist[node_size * node_id + 2]
    
    if o =='+':
        output1=a+b
    elif o =='-':
        output1=a-b
    elif o =='*':
        output1=a*b
    else: 
        output1=a/b
    inputs[input_id]=output1
    return output1


#main program

#newlist=[1,2,'+',4,0,'*']
#features=[1,2,3,4]
#input_id=5
#print( calculateInput(newlist, input_id, features))

    
#cgp(features, [1,2,0, 1,2,0, 4,3,2])



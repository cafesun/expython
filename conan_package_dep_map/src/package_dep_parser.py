#!/usr/bin/python
# -*- coding:utf8 -*-
#from graphviz import Digraph
import pydot
#import graphviz
#import os

if __name__ == "__main__" :
    print("TODO")
 #   dotFile = open(r"../data/dependency.dot", "r")
 #   dotContext = dotFile.read()
 #   graphviz.Source(dotContext)

    dots = pydot.graph_from_dot_file(r"../data/dependency.dot")
    dot = dots[0]
    edges = dot.get_edge_list()

    packageDict = {}
    for itEdge in edges:
        edge = itEdge
        objDict = edge.obj_dict
        pointTpl = objDict["points"]
        curNode = pointTpl[0]
        packageDict[curNode] = "t"
        subNodes = pointTpl[1]["nodes"]
        for itSubNode in subNodes.keys():
            packageDict[itSubNode]="t"

    print("current project relative package cnt:%d" %len(packageDict))
    for itPkg in packageDict.keys():
        print("pkg: %s" %itPkg)
#    nodes = dot.get_node_list()
#    for it in nodes:
#       print(it)

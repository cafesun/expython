#!/usr/bin/python
# -*- coding:utf8 -*-
import ast
import os

class ConanFileVisitor(ast.NodeVisitor):
    def __init__(self):
        self._poperties = {}

    def visit_ClassDef(self, node):
        for iterBody in node.body:
            if (isinstance(iterBody, ast.Assign)) :
                targets = iterBody.targets
                id = None
                if (len(targets) > 0) :
                    id = targets[0].id
                value = iterBody.value
                if (isinstance(value, ast.Str)) :
                    if (id != None):
                        self._poperties[id] = value.s

    def getProperty(self, strKey):
        return self._poperties.get(strKey)

class ConanFileParserWarapper(object) :
    def __init__(self, conanfile):
        self._visitor = ConanFileVisitor()
        self._conanfile = conanfile

    def parse(self):
        with open(self._conanfile) as filePy:
            sourceCode = filePy.read()
            pt = ast.parse(sourceCode)
            self._visitor.visit(pt)

    def getAttribute(self, strKey):
        return self._visitor.getProperty(strKey)

def main():
    print("Enter main")
    conanfileParser = ConanFileParserWarapper("./conanfile.py")
    conanfileParser.parse()
    version = conanfileParser.getAttribute("version")
    print("version=%s" %(version))




if __name__ == "__main__":
    print("begin")
    main()
    print("end")

import ast
import os

class ConanFileVisitor(ast.NodeVisitor):
    def visit_Str(self, node):
        print('Found %s stringvalue = "%s"' % (node.__class__.__name__, node.s))
        if node.s == "123456":
            node.s = "45678"

    def visit_FunctionDef(self, node):
        print('Found function ', node._fields)

    def visit_ClassDef(self, node):
        for iterBody in node.body:
            if (isinstance(iterBody, ast.Assign)) :
                targets = iterBody.targets
                id = None
                if (len(targets) > 0) :
                    id = targets[0].id
                value = iterBody.value
                if (isinstance(value, ast.Str)) :
                    print("value = %s" %(value.s))


def main():
    print("Enter main")
    with open("./conanfile.py") as filePy:
        sourceCode = filePy.read()
        pt = ast.parse(sourceCode)
        visitor = ConanFileVisitor()
        visitor.visit(pt)



if __name__ == "__main__":
    print("begin")
    main()
    print("end")

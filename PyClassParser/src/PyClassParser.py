import pyclbr
import os

import pyclbr
import os
from operator import itemgetter

def show_class(name,class_data):
    print('Class:',name)
    filename = os.path.basename(class_data.file)
    print('  File:{0} [{1}]'.format(
        filename,class_data.lineno))
    show_super_classes(name,class_data)
    show_methods(name,class_data)
    print()


def show_methods(class_name,class_data):
    for name,lineno in sorted(class_data.methods.items(),
                              key=itemgetter(1)):
        print('  Method:{0} [{1}]'.format(name,lineno))

def show_super_classes(name,class_data):
    super_class_names = []
    for super_class in class_data.super:
        if super_class == 'object':
            continue
        if isinstance(super_class,str):
            super_class_names.append(super_class)
        else:
            super_class_names.append(super_class.name)
    if super_class_names:
        print('  Super classes:',super_class_names)

def main():
    example_data = pyclbr.readmodule('conanfile')
    #for name, class_data in sorted(example_data.items(),
    #                               key=lambda x: x[1].lineno):
    for name, class_data in example_data.items() :
        show_class(name, class_data)

if __name__ == "__main__":
    main()

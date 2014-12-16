#!/usr/bin/python
# expects gccxml to be available via $PATH
# e.g. on Mac OS X you can install via: $ sudo port install gccxml


import sys
import subprocess
from xml.etree import ElementTree


#-- Config --#

STK_DIR='stk'


#-- Data model --#

class CppClass:
    def __init__(self, name='(none)', parent=None):
        self.name = name
        self.parent = parent
        self.methods = [] # list of Method
        self.fields = [] # list of Var
        
    def __str__(self):
        s = ''
        s += 'class %s:\n' % self.name
        s += '    parent: %s\n' % self.parent
        
        if len(self.methods) > 0:
            s += '    methods: \n'
            for method in self.methods:
                s+= '        %s\n' % method
        else:
            s += '    methods: (none)\n'
        
        if len(self.fields) > 0:
            s += '    fields: \n'
            for field in self.fields:
                s += '        %s\n' % field
        else:
            s += '    fields: (none)\n'
        return s

class Method:
    def __init__(self, name='fun'):
        self.type = 'void'
        self.name = name
        self.args = [] # Var
        self.static = False
        
    def __str__(self):
        return '%s %s(%s)' % (self.type, self.name, ', '.join([str(arg) for arg in self.args]))

class Var:
    def __init__(self):
        self.type = 'int'
        self.name = 'v'
    
    def __str__(self):
        return '%s %s' % (self.type, self.name)


#-- Call gccxml --#

STK_INCLUDE_DIR=STK_DIR+'/include'
stk_class = sys.argv[1]
stk_header = STK_INCLUDE_DIR+('/%s.h'%stk_class)
xml_file = stk_class + '.xml'
chuck_file = 'ugen_%s.cpp' % stk_class

# subprocess.check_call(['gccxml', stk_header, '-fxml=%s'%xml_file, '-I%s'%STK_INCLUDE_DIR])

tree = ElementTree.parse(xml_file)
root = tree.getroot()


#-- Construct index of all elements with ids --#

idx = dict()
for item in root.iter():
    if 'id' in item.attrib:
        idx[item.attrib['id']] = item


#-- Create mapping of C++ types -> ChucK types (int, float, string) --#

ck_types = dict()
for item in root.iter('FundamentalType'):
    if 'int' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'int'
    elif 'char' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'int'
    elif 'bool' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'int'
    elif 'float' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'float'
    elif 'double' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'float'
    elif 'string' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'string'
    elif 'void' in item.attrib['name']:
        ck_types[item.attrib['id']] = 'void'
    else:
        pass # print 'unhandled FundamentalType %s' % item.attrib['name']

for item in root.iter('Typedef'):
    if item.attrib['type'] in ck_types:
        ck_types[item.attrib['id']] = ck_types[item.attrib['type']]
    else:
        # recurse through typedefs until base type is found
        item_id = item.attrib['id']
        item_name = item.attrib['name']
        while item != None and item.attrib['type'] not in ck_types:
            if item.attrib['type'] in idx:
                item = idx[item.attrib['type']]
                if 'type' not in item.attrib: item = None
            else:
                item = None
        if item != None:
            ck_types[item_id] = ck_types[item.attrib['type']]
        else:
            pass # print 'unhandled Typedef %s' % item_name


#-- Create internal representation of the class --#

class_info = CppClass(stk_class)

# find id attribute for this class
for item in root.iter('Class'):
    if item.attrib['name'] == stk_class:
        class_id = item.attrib['id']
        break
        # print _class.attrib

# for item in root.iter('Constructor'):
#     if item.attrib['context'] == class_id and 'artificial' not in item.attrib:
#         print item.attrib['name']
# for item in root.iter('Destructor'):
#     if item.attrib['context'] == class_id and 'artificial' not in item.attrib:
#         print item.attrib['name']

# go through fields
for item in root.iter('Field'):
    if item.attrib['context'] == class_id and 'artificial' not in item.attrib:
        if item.attrib['access'] == 'public':
            if item.attrib['type'] in ck_types:
                var = Var()
                var.type = ck_types[item.attrib['type']]
                var.name = item.attrib['name']
                class_info.fields.append(var)
            else:
                print "ignoring field '%s': unhandled type '%s'" % (item.attrib['name'], item.attrib['type'])

# go through methods
for item in root.iter('Method'):
    if item.attrib['context'] == class_id and 'artificial' not in item.attrib:
        if item.attrib['access'] == 'public':
            if item.attrib['returns'] in ck_types:
                method = Method()
                
                method.type = ck_types[item.attrib['returns']]
                method.name = item.attrib['name']
                
                for arg in item.iter('Argument'):
                    argvar = Var()
                    if arg.attrib['type'] in ck_types:
                        argvar.type = ck_types[arg.attrib['type']]
                        if 'name' in arg.attrib: argvar.name = arg.attrib['name']
                        method.args.append(argvar)
                    else:
                        print "ignoring method '%s': unhandled argument type '%s'" % (item.attrib['name'], arg.attrib['type'])
                        method = None
                        break
                
                if method is not None:
                    class_info.methods.append(method)
            else:
                print "ignoring method '%s': unhandled type '%s'" % (item.attrib['name'], item.attrib['returns'])

# go through enums
# for item in root.iter('Enumeration'):
#     if item.attrib['context'] == class_id:
#         print item.attrib['name']


#-- print class info --#

print class_info



# import clang.cindex
#
# def find_typerefs(node, typename):
#     """ Find all references to the type named 'typename'
#     """
#     if node.kind.is_reference():
#         ref_node = node.get_definition()
#         print ref_node.spelling, ref_node.displayname
#         if ref_node.spelling == typename or ref_node.displayname == typename:
#             print 'Found %s [line=%s, col=%s]' % (typename, node.location.line, node.location.column)
#     # Recurse for children of this node
#     for c in node.get_children():
#         find_typerefs(c, typename)
#
# index = clang.cindex.Index.create()
# tu = index.parse(sys.argv[1], args=sys.argv[3:])
# print 'Translation unit:', tu.spelling
# find_typerefs(tu.cursor, sys.argv[2])



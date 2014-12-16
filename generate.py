#!/usr/bin/python

#-- Config --#

CONFIG_PATH='config'
CONFIG_FILENAME='config.json'
STK_DIR='stk'
STK_CLASS_PREFIX='x'


#-- --#
CONFIG_FILE='%s/%s'%(CONFIG_PATH,CONFIG_FILENAME)
STK_INCLUDE_DIR='%s/include'%STK_DIR
STK_SRC_DIR='%s/src'%STK_DIR


import sys
import json
import pprint

sys.path.append('.')
from CppClass import CppClass
import templates

with open(CONFIG_FILE, 'r') as config_file:
    config = json.load(config_file)

for stk_class in config['classes']:
    try:
        with open('%s/%s.json'%(CONFIG_PATH,stk_class), 'r') as class_config_file:
            class_config = json.load(class_config_file)
    except IOError:
        class_config = dict()
    
    stk_header = '%s/%s.h'%(STK_INCLUDE_DIR,stk_class)
    xml_file = stk_class + '.xml'
    
    class_info = CppClass.generateFromFile(stk_class, stk_header, ['-I%s'%STK_INCLUDE_DIR,])
    
    class_queries = ''
    
    generated_filename = 'ugen_%s.cpp' % stk_class
    with open(generated_filename, 'w') as gf:
        
        class_info_str = '  Generated ChucK bindings for %s\n\n' % stk_class
        class_info_str += '  Class description: \n  %s\n\n' % class_info
        class_info_str += '  Class configuration: \n  %s\n\n' % pprint.pformat(class_config)
        
        
        
        gf.write(templates.STK_CLASS_TOPLEVEL.format(
            class_name=stk_class,
            class_info=class_info_str,
            class_includes='#include "%s.h"'%stk_class,
            ck_class_name='%s%s'%(STK_CLASS_PREFIX,stk_class),
            ck_class_parent='UGen',
            class_imports='',
        ))
        
        if len(class_info.fields) > 0: raise





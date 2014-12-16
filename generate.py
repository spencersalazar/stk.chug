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
        
        ext_class_methods = ''
        ext_class_mvars = ''
        ck_mfun_defs = ''
        ck_mfun_imports = ''
        
        for prop in class_info.properties:
            # properties in the class_info list should already have a setter + mvar
            add_getter = not prop.readonly
            add_mvar = False
            add_setter = False
            
            Prop_name = prop.name[:1].upper()+prop.name[1:]
            
            if add_getter:
                ext_class_methods += templates.EXT_GETTER.format(
                    prop_type=prop.type,
                    Prop_name=Prop_name,
                    mvar_name='%s_'%prop.name
                )
            
            ck_mfun_defs += templates.DEFINE_GETTER.format(
                class_name=stk_class,
                prop_name=prop.name,
                ck_return=templates.CK_RETURN[prop.type],
                getter_name='ext_get%s'%Prop_name if add_getter else 'get%s'%Prop_name
            )
            ck_mfun_imports += templates.IMPORT_GETTER.format(
                class_name=stk_class,
                prop_name=prop.name,
                prop_type=prop.type,
                ck_getter_name=prop.name,
            )
            
            if not prop.readonly:
                ck_mfun_defs += templates.DEFINE_SETTER.format(
                    class_name=stk_class,
                    prop_name=prop.name,
                    ckinternal_type=templates.CKINTERNAL_TYPE[prop.type],
                    ck_get_arg_type=templates.CK_GET_ARG_TYPE[prop.type],
                    ck_return=templates.CK_RETURN[prop.type],
                    setter_name='ext_set%s'%Prop_name if add_setter else 'set%s'%Prop_name,
                    getter_name='ext_get%s'%Prop_name if add_getter else 'get%s'%Prop_name,
                    )
                ck_mfun_imports += templates.IMPORT_SETTER.format(
                    class_name=stk_class,
                    prop_name=prop.name,
                    prop_type=prop.type,
                    ck_setter_name=prop.name,
                )
                
        
        ext_class_def = templates.EXT_CLASS.format(
            class_name=stk_class,
            ext_methods=ext_class_methods,
            ext_mvars=ext_class_mvars
        )
        
        gf.write(templates.STK_CLASS_TOPLEVEL.format(
            class_name=stk_class,
            class_info=class_info_str,
            class_includes='#include "%s.h"'%stk_class,
            ck_class_name='%s%s'%(STK_CLASS_PREFIX,stk_class),
            ck_class_parent='UGen',
            ext_class_def=ext_class_def,
            ck_function_defs=ck_mfun_defs,
            class_imports=ck_mfun_imports,
        ))
        
        if len(class_info.fields) > 0: raise





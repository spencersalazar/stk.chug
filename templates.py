
STK_MAIN="""
/*----------------------------------------------------------------------------
  stk.chug
  Chuck STK module

  Copyright (c) 2014 Spencer Salazar.  All rights reserved.
  https://ccrma.stanford.edu/~spencer/

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
  U.S.A.
-----------------------------------------------------------------------------*/

{class_query_defs}

{chugin_query}
{{
    // hmm, don't change this...
    QUERY->setname(QUERY, "STK");
    
{class_queries}
    
    return TRUE;

error:
    return FALSE;
}}

"""

CHUGIN_QUERY_DYNAMIC="CK_DLL_QUERY( STK )"
CHUGIN_QUERY_STATIC="t_CKBOOL STK_query(Chuck_DL_Query *QUERY)"

STK_CLASS_TOPLEVEL="""
/*----------------------------------------------------------------------------
  stk.chug
  Chuck STK module

  Copyright (c) 2014 Spencer Salazar.  All rights reserved.
  https://ccrma.stanford.edu/~spencer/

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
  U.S.A.
-----------------------------------------------------------------------------*/

/*----------------------------------------------------------------------------
{class_info}
-----------------------------------------------------------------------------*/

#include "chuck_dl.h"
#include "chuck_def.h"
#include "chuck_type.h"

#undef TWO_PI // for STK

// general includes
#include <stdio.h>
#include <limits.h>

{class_includes}

using namespace stk;

{ext_class_def}

t_CKINT stk_{class_name}_offset_data = 0;

CK_DLL_CTOR(stk_{class_name}_ctor)
{{
    ext_{class_name} *stk_obj = new ext_{class_name};
    OBJ_MEMBER_INT(SELF, stk_{class_name}_offset_data) = (t_CKINT) stk_obj;
}}

CK_DLL_DTOR(stk_{class_name}_dtor)
{{
    ext_{class_name} *stk_obj = (ext_{class_name} *) OBJ_MEMBER_INT(SELF, stk_{class_name}_offset_data);
    delete stk_obj;
    OBJ_MEMBER_INT(SELF, stk_{class_name}_offset_data) = 0;
}}

{ck_function_defs}

t_CKBOOL stk_{class_name}_query(Chuck_DL_Query *QUERY)
{{
    QUERY->begin_class(QUERY, "{ck_class_name}", "{ck_class_parent}");
    
    stk_{class_name}_offset_data = QUERY->add_mvar(QUERY, "int", "@{class_name}_data", FALSE);
    
    QUERY->add_ctor(QUERY, stk_{class_name}_ctor);
    QUERY->add_dtor(QUERY, stk_{class_name}_dtor);
    
{class_imports}
    QUERY->end_class(QUERY);
    
    return TRUE;
    
error:
    return FALSE;
}}
"""

EXT_CLASS="""
class ext_{class_name} : public {class_name}
{{
public:
{ext_methods}
protected:
{ext_mvars}
}};

"""

EXT_GETTER="""    {prop_type} ext_get{Prop_name}() {{ return {mvar_name}; }}
"""
EXT_OVERRIDE_SETTER="""    void ext_set{Prop_name}({prop_type} prop) {{ {mvar_name} = prop; {stk_setter_name}(prop); }}
"""

CK_RETURN={
    "int": "RETURN->v_int",
    "float": "RETURN->v_float",
}
CK_GET_ARG_TYPE={
    "int": "GET_NEXT_INT(ARGS)",
    "float": "GET_NEXT_FLOAT(ARGS)",
}
CKINTERNAL_TYPE={
    "int": "t_CKINT",
    "float": "t_CKFLOAT"
}

DEFINE_SETTER="""CK_DLL_MFUN(stk_{class_name}_set_{prop_name})
{{
    ext_{class_name} *stk_obj = (ext_{class_name} *) OBJ_MEMBER_INT(SELF, stk_{class_name}_offset_data);
    {ckinternal_type} prop = {ck_get_arg_type};
    stk_obj->{setter_name}(prop);
    {ck_return} = stk_obj->{getter_name}();
}}

"""
IMPORT_SETTER="""    QUERY->add_mfun(QUERY, stk_{class_name}_set_{prop_name}, "{prop_type}", "{ck_setter_name}");
    QUERY->add_arg(QUERY, "{prop_type}", "prop");
    
"""

DEFINE_GETTER="""CK_DLL_MFUN(stk_{class_name}_get_{prop_name})
{{
    ext_{class_name} *stk_obj = (ext_{class_name} *) OBJ_MEMBER_INT(SELF, stk_{class_name}_offset_data);
    {ck_return} = stk_obj->{getter_name}();
}}

"""
IMPORT_GETTER="""    QUERY->add_mfun(QUERY, stk_{class_name}_get_{prop_name}, "{prop_type}", "{ck_getter_name}");
    
"""


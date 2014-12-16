
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

// general includes
#include <stdio.h>
#include <limits.h>

{class_includes}

{ext_class_def}

t_CKINT stk_{class_name}_offset_data = 0;

CK_DLL_CTOR(stk_{class_name}_ctor)
{{
    OBJ_MEMBER_OBJECT(SELF, stk_{class_name}_offset_data) = new {class_name};
}}

CK_DLL_DTOR(stk_{class_name}_ctor)
{{
    
    OBJ_MEMBER_OBJECT(SELF, stk_{class_name}_offset_data) = NULL;
}}

t_CKBOOL stk_{class_name}_query(Chuck_DL_Query *QUERY)
{{
    QUERY->begin_class(QUERY, "{ck_class_name}", "{ck_class_parent}");
    
{class_imports}
    
    QUERY->end_class();
    
    return TRUE;
    
error:
    return FALSE;
}}
"""

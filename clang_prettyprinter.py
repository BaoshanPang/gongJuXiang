#!/usr/bin/env python3
from __future__ import print_function
import struct
import sys

import gdb.printing
import gdb.types

class SourceLocationPrinter:
    """Print an clang::SourceLocation object."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        # https://stackoverflow.com/questions/22774067/gdb-python-api-is-it-possible-to-make-a-call-to-a-class-struct-method
        eval_string = "(*("+str(self.val.type)+"*)("+str(self.val.address)+")).dump(this->getSourceManager())"
        return gdb.parse_and_eval(eval_string);

class MultiLevelTemplateArgumentListPrinter:
    "MultiLevelTemplateArgumentList"

    def __init__(self, val):
        self.val = val

    def to_string(self):
       eval_string = "(*("+str(self.val.type)+"*)("+str(self.val.address)+")).TemplateArgumentLists.size()"
       depth = int(gdb.parse_and_eval(eval_string))
       strstr = ""
       for i in range(depth):
           eval_string = "(*("+str(self.val.type)+"*)("+str(self.val.address)+")).TemplateArgumentLists[{}].size()".format(i)
           sz = int(gdb.parse_and_eval(eval_string))
           strstr += "\nlevel {}: args {}".format(i, sz)
           for j in range(sz):
               eval_string = "p (*("+str(self.val.type)+"*)("+str(self.val.address)+")).TemplateArgumentLists[{}][{}].dump()".format(i,j)
               gdb.execute(eval_string,True,True)
       return  strstr

pp = gdb.printing.RegexpCollectionPrettyPrinter("CLANGSupport")
pp.add_printer('SourceLocationPrinter',
               '^clang::SourceLocation$',
               SourceLocationPrinter)
pp.add_printer('MultiLevelTemplateArgumentListPrinter',
               '^clang::MultiLevelTemplateArgumentList$',
               MultiLevelTemplateArgumentListPrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, True)

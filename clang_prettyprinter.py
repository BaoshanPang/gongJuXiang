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


pp = gdb.printing.RegexpCollectionPrettyPrinter("CLANGSupport")
pp.add_printer('SourceLocationPrinter', '^clang::SourceLocation$', SourceLocationPrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, True)

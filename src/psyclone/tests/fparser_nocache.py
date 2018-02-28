#!/usr/bin/env python
import fparser.api
from fparser.parsefortran import FortranParser

# Workaround to call fparser without using its cache
class api():
    @staticmethod
    def parse(*args, **kwargs):
        FortranParser.cache = {}
        return fparser.api.parse(*args, **kwargs)

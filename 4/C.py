#!/bin/env python
import sys
import re

name = '(,?\s*[a-zA-Z.]+)'
r_from = '(?<=from )' + name + '(?= import)'
r_import = '(?<=import )' + name + '+'
modules = set()
for line in sys.stdin.readlines():
    l = line.split(';')
    for expr in l:
        for mod in re.finditer(r_from, expr):
            res = mod.group()
            for module in res.split(','):
                modules.add(module.strip())
        if re.search(r_from, expr):
            continue
        for mod in re.finditer(r_import, expr):
            res = mod.group()
            for module in res.split(','):
                modules.add(module.strip())
modules = sorted(modules)
print (', '.join(modules))

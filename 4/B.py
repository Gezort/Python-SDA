#!/bin/env python
import sys
import re

for line in sys.stdin.readlines():
    r = re.compile(r'''([0-9]{4,4}(?P<sep1>[./-])[0-9]{2}(?P=sep1)[0-9]{2} |
            [0-9]{2}(?P<sep2>[./-])[0-9]{2}(?P=sep2)[0-9]{4} |
            [0-9]{1,2}\s*[а-яА-Я]+\s*[0-9]{4})$''', re.VERBOSE)
    if r.match(line):
        print ('YES')
    else:
        print ('NO')

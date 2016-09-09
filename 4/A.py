#!/bin/env python
import sys
import re

text = sys.stdin.read()
langs, lines = re.split(r'\n\n', text)
langs = langs.split('\n')
lines = lines.split('\n')
if lines[-1] == '':
    lines = lines[:-1]
languages = {}
for l in langs:
    k, v = l.split(' ')
    languages[k] = re.compile('[' + v + ']', flags=re.IGNORECASE)
for line in lines:
    answer = set()
    for word in line.split():
        count = 0
        lang = ''
        for k in sorted(languages.keys()):
            n = len(re.findall(languages[k], word))
            if n > count:
                count = n
                lang = k
        answer.add(lang)
    for lang in sorted(answer):
        print (lang, end=' ')
    print()

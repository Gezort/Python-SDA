import sys
result = {}
for line in sys.stdin.readlines():
    for ch in line.lower():
        if ch.isalpha():
            result[ch] = result.get(ch,0) + 1
for (x,y) in sorted(result.items(), key = lambda x : (-x[1], x[0])):
    print (x + ': ' + str(y))

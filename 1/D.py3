import sys
sz = int(sys.stdin.readline())
for line in sys.stdin.readlines():
    line = line[:-1].replace('  ', ' ').split()
    curr_len = 0
    output = ''
    for word in line:
        if curr_len == 0:
            curr_len = len(word)
            output = word
        elif curr_len + len(word) < sz:
            curr_len += len(word) + 1
            output += ' ' + word
        else:
            print(output)
            output = word
            curr_len = len(word)
    print (output)

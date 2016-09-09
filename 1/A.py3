n = int(input())
x = 0
y = 1
for i in range(n):
    x, y = y, x + y
print (x)

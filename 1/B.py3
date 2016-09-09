from functools import reduce
p = float(input())
a = list(map(float, input().split()))
print (reduce(lambda x,y: x + abs(y) ** p, a,0) ** (1 / p))

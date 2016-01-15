maxRes = 0
maxW = 0
maxH = 0


for w in range(1, 1081):
    h = (1080 - w) / 2
    res = w*h
    if res > maxRes:
        maxRes = res
        maxW = w
        maxH = h


print maxRes, maxW ,maxH 

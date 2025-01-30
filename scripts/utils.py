def get_quarter(x, y):
    quarters = [x*4 for x in range(0, int(y/4) + 1)]
    for i in range(len(quarters)-1):
        if quarters[i] <= x <= quarters[i+1]:
            return i+1

def companiesFilter(func):
    for x in func():
        yield list(x[1:]),x[0]

def generalFilter(func,*filtingBy,isReducing = False):
    if not isReducing:
        for x in func():
            yield [v for i,v in enumerate(x,1) if i in list(filtingBy)]
    else:
        for x in func():
            yield [v for i, v in enumerate(x,1) if i not in list(filtingBy)]




if __name__ == '__main__':
    def f():
        return [[1, 2, 3], [4, 5, 6], [6, 7, 8]]
    for x in generalFilter(f,1,2,isReducing=True):
        print(x)
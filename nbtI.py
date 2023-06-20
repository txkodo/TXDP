
def a():
    print(x)

aa = a

x = 100

def b():
    aa()
    print(x)

b()
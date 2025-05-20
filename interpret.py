#any imports..?

def read(filename):
    f = open(filename, "r")
    s = f.read()
    return s

def parsePy(s):
    
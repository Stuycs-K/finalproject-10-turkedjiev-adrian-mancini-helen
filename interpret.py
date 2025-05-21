#any imports..?

def read(filename):
    f = open(filename, "r") #does this work for python files? will newlines and indents '\t' be read into the string?
    s = f.read()
    return s

def parsePy(s):
    lines = s.splitline()
    l = ""
    for i in range(len(lines)):
        l = lines[i]
        if l[0] == '#': #removes lines that are commented out
            #seperate function to deal with these since they're easy??
        if l[0] == '\t': #checks if there's an indent (maybe?) and concatinates with command before? <-- not sure if this is the logic you want to use, so we can change it...
            #more stuff here, plus conditions if there are multiple indents
    return lines

def checkCommand(s):
    #classify expressions, maybe output array [type, arguments...]
    return l

def translate(c): #input the array w/ type and arguments
    #a bunch of if statements for dif command types...

def overalFunc(filename):
    #this will put everything together, call the read command and then output the translated code??

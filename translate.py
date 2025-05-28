#any imports..?

def read(filename):
    f = open(filename, "r") #does this work for python files? will newlines and indents '\t' be read into the string?
    s = f.read()
    return s

def parseLOL(s):
    '''
    https://github.com/justinmeza/lolcode-spec/blob/master/v1.3/lolcode-spec-v1.3.md
    '''
    lines = s.splitlines()
    for line in lines:
        prediction = ""
        bare_content = stripStatement(line)
        if bare_content == "":
            prediction += "empty line"
        if "HAI" in bare_content:
            prediction += "start of file; ignore"
        if "KTHXBYE" in bare_content:
            prediction += "end of file; ignore"
        if "I HAS A" in bare_content:
            if "ITZ A" in bare_content:
                prediction += "instantiates and initializes a variable"
            elif "ITZ" in bare_content:
                prediction += "declares variable"
            else:
                prediction += "instatiates a variable and initializes it to NOOB"
        if " R " in bare_content:
            prediction += "assinging value to variable"
        if "R NOOB" in bare_content:
            prediction += "deallocation"

        


        print(f'{line} ---> {prediction}')

    return lines

def stripStatement(statement):
    '''
    Given a certain statment, it returns it without:
        - leading or trailing whitespace 
        - comments
        - the contents of strings
    '''
    ret = ''
    commentIndex = statement.find('BTW') # find index at which you have to start removing comment
    adding = True
    for i in range(len(statement)):
        if statement[i] == '"': # replace any string "content" with ""
            adding = not adding
            ret += '"'
            continue
        if commentIndex != -1 and i >= commentIndex: # don't add in comments
            adding = False
        if adding:
            ret += statement[i]
    ret = ret.strip() # remove leading and trailing whitespace 
    return ret



def checkCommand(s):
    #classify expressions, maybe output array [type, arguments...]
    return l

def translate(c): #input the array w/ type and arguments

    pass
    #a bunch of if statements for dif command types...

def overalFunc(filename):
    pass
    #this will put everything together, call the read command and then output the translated code??





#### TESTING

LOLCODE = read("sampleLOL_3.txt")
parseLOL(LOLCODE)

# stripStatement("I HAS A VAR ITZ 12          BTW VAR = 12")
# stripStatement('I HAS A name ITZ "var"')
# stripStatement('I Has A misleading_variable ITZ "KTHXBYE" AND ITS AWESOME')









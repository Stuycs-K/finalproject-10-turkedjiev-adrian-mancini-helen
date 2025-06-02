'''
File Structure:

- each statement becomes a list entry 
- each list entry is a dictionary = {
    "id" : (give each statment a number, starting at 1)
    "original" : (the original statement)
    "type" : (one of a pre-set list of possible functionalities)
    "arguments" : [literal_value, "variable name", expr(id)]
    "body" : (dependent on the type, contains additional information)
}

ID corresponds to scope depth. EX:

                CODE:                               IDS:

def func(arg1, arg2):   
    arg3 R 9                1
    arg1 += 4                           1.1 --> arg1 = (val)
                                        1.2 --> val = (arg1 + 4)
    if arg1 > arg2:                     1.3   
        arg2 = mod(arg1, arg2)          1.31 --> arg2 = (val)
                                        1.32 --> val = mod(arg1, arg2)

TYPES:

declare
    "arguments" : ["variable_name"]

deallocate
    "arguments" : ["variable_name"]

instatiate
    "arguments" : ["variable_name", "assigned_type"]

assign
    "arguments" : ["variable_name", "assigned_value"]

math
    "arguments" : ["operator", "argument_1", "argument_2"]

comment
    "arguments" : ["content"]

print
    "arguments" : ["value"]

if
    "arguments" : ["condition", "content"]

loop
    "arguments" : ["condition", "content"]
    
function
    "arguments" : ["function_name", "variable1", "variable2", "content"]

'''

global ast, latest_id, latest_scope
ast = []
latest_id = 0
latest_scope = 0


def calc_id():
    return latest_id + (1 * 10**-latest_scope)

def read(filename):
    f = open(filename, "r") #does this work for python files? will newlines and indents '\t' be read into the string?
    s = f.read()
    return s

def parseLOL(line):
    global ast
    '''
    https://github.com/justinmeza/lolcode-spec/blob/master/v1.3/lolcode-spec-v1.3.md
    '''
    prediction = ""
    bare_content = stripStatement(line)
    ret = {}
    if bare_content == "":
        prediction += "empty line"
    if "HAI" in bare_content:
        #should this have a dictionary entry if no arguments?
        prediction += "start of file; ignore"
    if "KTHXBYE" in bare_content:
        prediction += "end of file; ignore"
    if "I HAS A" in bare_content:
        if "ITZ A" in bare_content:
            # I HAS A <x> ITZ A <y>
            tokens = line.split()
            variable_name = tokens[3]
            assigned_type = tokens[6]
            ret = {
                "id" : calc_id(),
                "original" : line,
                "type" : "instatiate",
                "arguments" : [variable_name, assigned_type],
                "body" : []
            }
            prediction += "instantiates and gives it a type"
        elif "ITZ" in bare_content:
            # I HAS A <X> ITZ <3 + 4 / 2>
            tokens = line.split()
            variable_name = tokens[3]
            recur = ""
            for i in range(len(tokens)-6):
                recur += tokens[i+6]  + " " #concatinates all from ITZ onwards with spaces between
            assigned_value = parseLOL(recur) 
            ret = {
                "id" : calc_id(),
                "original" : line,
                "type" : "assign",
                "arguments" : [variable_name, assigned_value],
                "body" : []
            }
            prediction += "assigns value to variable"
        else:
            tokens = line.split()
            variable_name = tokens[3]
            ret = {
                "id" : calc_id(),
                "original" : line,
                "type" : "declare",
                "arguments" : [variable_name],
                "body" : []
            }
            prediction += "declares a variable "
    if " R " in bare_content:
        tokens = line.split()
        variable_name = tokens[0]
        recur = ""
        for i in range(len(tokens)-index-2):
            recur += tokens[i+index+2]  + " " #concatinates all after R
        assigned_value = parseLOL(recur)
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "assign", #this is the same type as initializing and assigning-- is that okay...
            "arguments" : [variable_name, assigned_value], 
            "body" : []
        }    
        prediction += "assinging value to variable"
    #are we including SRS, YARN & regular identifier?
    if "VISIBLE" in bare_content:
        tokens = line.split()
        value = " ".join(tokens[1:])
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "print",
            "arguments" : [value],
            "body" : []
        }
    #MATH
    if "SUM OF" in bare_content:
        ret = mathParse(line, "+")
        prediction += "addition"
    if "DIFF OF" in bare_content:
        ret = mathParse(line, "-")
        prediction += "subtraction"
    if "PRODUKT OF" in bare_content:
        ret = mathParse(line, "*")
        prediction += "multiplication"
    if "QUOSHUNT OF" in bare_content:
        ret = mathParse(line, "/")
        prediction += "division"
    if "MOD OF" in bare_content:
        ret = mathParse(line, "%")
        prediction += "mod"
    if "BIGGR OF" in bare_content:
        ret = mathParse(line, ">")
        prediction += "min"
    if "SMALLR OF" in bare_content:
        ret = mathParse(line, "<")
        prediction += "max"
    #COMMENTS
    if "BTW " in bare_content:
        content = line[4:]
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "comment",
            "arguments" : [content], 
            "body" : []
            }
    if "OBTW" in bare_content:
        content[0] = line[5:]
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "comment",
            "arguments" : [content], 
            "body" : []
            }
    if "IM IN YR" in bare_content:
        ...
    if "HOW IZ I" in bare_content:
        ...
    print(f'{line} ---> {prediction}')

    return ret

def run(s):
    global ast
    lines = s.splitlines()
    for line in lines:
        ast += [parseLOL(line)]
    print_ast()
    translate()

def parseMulti(line):
    pass

def run():
    global latest_scope
    lines = s.splitlines()
    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        latest_scope = leading_spaces/4
        if lastest_scope > 0:
            parseMulti(line)
        else:
        ast += parseLOL(line)

#made a function to not repeat math code...
def mathParse(l, o):
    tokens = l.split() 
    operator = o
    #for i in (len(tokens)-4): #THIS NEEDS TO BE EDITED TO FIND THE CORRECT AN and recur both sides of it... not sure how to do that... 
    #    recur += tokens[i+2] + " " #concatinates entire string between SUM OF [...] AN # (not sure if this will work..!
    #agr1 = parseLOL(recur)
    '''
    Make sure to account for recursive case for inbetween SUM OF ... AN #
    EXAMPLE:
        HAI 1.2
        VISIBLE "Welcome to JDoodle!!"
        VISIBLE SUM OF 9 AN PRODUKT OF 6 AN QUOSHUNT OF 4 AN 6                  BTW answer 0
        KTHXBYE
    '''
    arg1 = tokens[2]
    arg2 = tokens[len(tokens) -1]
    ret = {
        "id" : calc_id(),
        "original" : line,
        "type" : "math",
        "arguments" : [operator, arg1, arg2],
        "body" : []
        }
    return ret

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

def translate(): #input the array w/ type and arguments
'''
- each list entry is a dictionary = {
    "id" : (give each statment a number, starting at 1)
    "original" : (the original statement)
    "type" : (one of a pre-set list of possible functionalities)
    "arguments" : [literal_value, "variable name", expr(id)]
    "body" : (dependent on the type, contains additional information)
}

'''
    global ast 
    ret = ""
    for dictionary in ast:
        if dictionary == {}:
            pass
        else:



        ret += '\n'
    pass    #a bunch of if statements for dif command types...

def print_ast():
    global ast
    print("AST:: [")
    for dictionary in ast:
        print(dictionary)
    print("]")

#### TESTING

LOLCODE = read("sampleLOL_3.txt")
run(LOLCODE)

# stripStatement("I HAS A VAR ITZ 12          BTW VAR = 12")
# stripStatement('I HAS A name ITZ "var"')
# stripStatement('I Has A misleading_variable ITZ "KTHXBYE" AND ITS AWESOME')

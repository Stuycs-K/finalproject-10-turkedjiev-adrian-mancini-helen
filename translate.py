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

instatiate
    "arguments" : ["variable_name", "assigned_type"]

assign
    "arguments" : ["variable_name", "assigned_value"]

math
    "arguments" : ["operator", "argument_1", "argument_2"]

comment
    "arguments" : ["line_index", "content"]

print
    "arguments" : ["value"]



'''

global ast = []
global latest_id = 0
global latest_scope = 0


def calc_id():
    return latest_id + (1 * 10**-latest_scope)

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
                # I HAS A <x> ITZ A <y>
                tokens = line.split()
                variable_name = tokens[3]
                assigned_type = tokens[6]
                ast += {
                    "id" : calc_id(),
                    "original" : line,
                    "type" : "instatiate",
                    "arguments" : [variable_name, assigned_type],
                    "body" : []
                }
                prediction += "instantiates and gives it a type"
            elif "ITZ" in bare_content:
                # I HAS A <X> ITZ <3 + 4 / 2>
                prediction += "assigns value to variable"
            else:
                prediction += "declares a variable "
        if " R " in bare_content:
            prediction += "assinging value to variable"
        if "R NOOB" in bare_content:
            prediction += "deallocation"
        #are we including SRS, YARN & regular identifier?
    
        #MATH
        if "SUM OF" in bare_content:
            mathParse(line, "+")
            prediction += "addition"
        if "DIFF OF" in bare_content:
            mathParse(line, "-")
            prediction += "subtraction"
        if "PRODUKT OF" in bare_content:
            mathParse(line, "*")
            prediction += "multiplication"
        if "QUOSHUNT OF" in bare_content:
            mathParse(line, "/")
            prediction += "division"
        if "BIGGR OF" in bare_content:
            mathParse(line, ">")
            prediction += "min"
        if "SMALLR OF" in bare_content:
            mathParse(line, "<")
            prediction += "max"
        


        print(f'{line} ---> {prediction}')

    return lines

#made a function to not repeat math code...
def mathParse(l, o):
    tokens = l.split() 
    operator = o
    for i in (len(tokens)-4):
        recur += tokens[i+2] #concatinates entire string between SUM OF [...] AN # (not sure if this will work..!
    agr1 = parseLOL(recur)
    '''
    Make sure to account for recursive case for inbetween SUM OF ... AN #
    EXAMPLE:
        HAI 1.2
        VISIBLE "Welcome to JDoodle!!"
        VISIBLE SUM OF PRODUKT OF 6 AN QUOSHUNT OF 4 AN 6 AN 9 <-- answer 0
        KTHXBYE
    '''
    arg2 = tokens[len(tokens) -1]
    ast += {
        "id" : calc_id(),
        "original" : line,
        "type" : "math",
        "arguments" : [operator, arg1, arg2],
        "body" : []
        }
    #doesn't have a return because just adding to a global

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

sum of [product of 3 and 4] and 6





#### TESTING

LOLCODE = read("sampleLOL_3.txt")
parseLOL(LOLCODE)

# stripStatement("I HAS A VAR ITZ 12          BTW VAR = 12")
# stripStatement('I HAS A name ITZ "var"')
# stripStatement('I Has A misleading_variable ITZ "KTHXBYE" AND ITS AWESOME')









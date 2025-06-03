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

def func(arg1, arg2):                   1
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

print
    "arguments" : ["value"]

boolean
    "arguments" : ["operator", "argument_1", "argument_2"]
    
MULTILINE:

comment
    "arguments" : ["content"]
    
comparison
    "arguments" : ["operator", "argument_1", "argument_2"]
    
--> if statements...

loop
    "arguments" : ["condition", "content"]
    
function
    "arguments" : ["function_name", "variable1", "variable2", "content"]

literal
    "arguments" : ["value"]
'''

#~~~~~~~~~~~ SET UP ~~~~~~~~~~~#

global ast, latest_id, latest_multi_id, latest_scope
ast = []
latest_id = 0
latest_multi_id = 0
latest_scope = 0

def calc_id():
    global latest_id, latest_scope
    return latest_id + (1 * 10**-latest_scope)


def read(filename):
    f = open(filename, "r") #does this work for python files? will newlines and indents '\t' be read into the string?
    s = f.read()
    return s


def print_ast():
    global ast
    print("AST:: [")
    for dictionary in ast:
        print(dictionary)
    print("]")


#~~~~~~~~~~~ PARSE LOLCODE ~~~~~~~~~~~#


def mathParse(l, o):
    tokens = l.split() 
    operator = o
    '''
    Make sure to account for recursive case for inbetween SUM OF ... AN #
    EXAMPLE:
        HAI 1.2
        VISIBLE "Welcome to JDoodle!!"
        VISIBLE SUM OF 9 AN PRODUKT OF 6 AN QUOSHUNT OF 4 AN 6                  BTW answer 0
        KTHXBYE
    '''
    arg1 = tokens[2]
    arg2 = tokens[4]
    ret = {
        "id" : calc_id(),
        "original" : l,
        "type" : "math",
        "arguments" : [operator, arg1, arg2],
        "body" : []
        }
    return ret


def booleanParse(l, o):
    tokens = l.split() 
    operator = o
    arg1 = tokens[2]
    arg2 = tokens[4]
    ret = {
        "id" : calc_id(),
        "original" : line,
        "type" : "boolean",
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


def parseMulti(line):
    global latest_multi_id
    for dictionary in ast:
        if dictionary == {}:
            pass
        else:
            if dictionary["id"] == lastest_multi_id:
                if dictionary["type"] == "comment":
                    dictionary["arguments"] += line
                if dictionary["type"] == "":
                    pass      
    pass


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
    elif "KTHXBYE" in bare_content:
        prediction += "end of file; ignore"
    elif "I HAS A" in bare_content:
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
            recur = " ".join(tokens[5:])
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
    elif " R " in bare_content:
        tokens = line.split()
        variable_name = tokens[0]
        recur = " ".join(tokens[2:])
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
    elif "VISIBLE" in bare_content:
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
    elif "SUM OF" in bare_content:
        ret = mathParse(line, "+")
        prediction += "addition"
    elif "DIFF OF" in bare_content:
        ret = mathParse(line, "-")
        prediction += "subtraction"
    elif "PRODUKT OF" in bare_content:
        ret = mathParse(line, "*")
        prediction += "multiplication"
    elif "QUOSHUNT OF" in bare_content:
        ret = mathParse(line, "/")
        prediction += "division"
    elif "MOD OF" in bare_content:
        ret = mathParse(line, "%")
        prediction += "mod"
    elif "BIGGR OF" in bare_content:
        ret = mathParse(line, ">")
        prediction += "min"
    elif "SMALLR OF" in bare_content:
        ret = mathParse(line, "<")
        prediction += "max"
    #COMMENTS
    elif "BTW " in bare_content:
        content = line[4:]
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "comment",
            "arguments" : [content], 
            "body" : []
            }
    elif "OBTW" in bare_content:
        content = []
        content[0] = line[5:]
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "comment",
            "arguments" : [content], 
            "body" : []
            }
    elif "IM IN YR" in bare_content:
        ...
    elif "HOW IZ I" in bare_content:
        ...
    #BOOLEAN
    elif "BOTH OF" in bare_content:
        ret = booleanParse(line, "and")
    elif "EITHER OF" in bare_content:
        ret = booleanParse(line, "or")
    elif "WON OF" in bare_content:
        ret = booleanParse(line, "xor")
    elif "NOT" in bare_content:
        arg1 = tokens[1]
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "boolean",
            "arguments" : [operator, arg1],
            "body" : []
            }
    #COMPARISON --> if statements
    elif "BOTH SAEM" in bare_content:
        pass
    elif "DIFFRINT" in bare_content:
        pass
    else:
        ret = {
            "id" : calc_id(),
            "original" : line,
            "type" : "literal",
            "arguments" : [line],
            "body" : []
        }
        
    #print(f'{line} ---> {prediction}')

    return ret

#~~~~~~~~~~~ TRANSLATE TO PYTHON ~~~~~~~~~~~#


def translate(): 
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
            #print(dictionary)
            temp_id = dictionary["id"]
            temp_type = dictionary["type"]
            temp_args = dictionary["arguments"]
            ret += "    " * (len(str(temp_id).strip(".0")) - 1)
            if temp_type == "declare":
                ret += temp_args[0]
            elif temp_type == "deallocate":
                ret += f'{temp_args[0]} = None'
            elif temp_type == "instatiate":
                assigned_type = ""
                match temp_args[1]:
                    case "YARN":
                        assigned_type = "String"
                    case "NUMBR":
                        assigned_type = "int"
                    case "NUMBAR":
                        assigned_type = "float"
                    case "TROOF":
                        assigned_type = "bool"
                ret += f'{assigned_type} {temp_args[0]}'
            elif temp_type == "assign":
                assigned_value = translate_expression(temp_args[1])
                ret += f'{temp_args[0]} = {assigned_value}'
            elif temp_type == "math":
                ret += f'{temp_args[1]} {temp_args[0]}  {temp_args[2]}'
            elif temp_type == "print":
                ret += f'print({temp_args[0]})'
        ret += '\n'
    print(ret)

def translate_expression(dictionary):
    if dictionary["type"] == "literal":
        return dictionary["arguments"][0]
    else:
        return ""

#~~~~~~~~~~~ RUN ~~~~~~~~~~~#

def run(s):
    global latest_scope, ast
    lines = s.splitlines()
    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        latest_scope = leading_spaces/4
        if latest_scope > 0:
            pass
            #parseMulti(line)
        else:
            ast += [parseLOL(line)]

#~~~~~~~~~~~ TESTING ~~~~~~~~~~~#


LOLCODE = read("sampleLOL_4.txt")
print(f'ORIGINAL::\n\n{LOLCODE}')
run(LOLCODE)
print('-------\nTRANSLATED::')
translate()
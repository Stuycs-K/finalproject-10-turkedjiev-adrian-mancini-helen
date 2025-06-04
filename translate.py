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

conditional
    "arguments" : ["operator", "argument_1", "argument_2", "content"]
    
if-else
    "arguments" : ["if_or_else", "content"]

loop
    "arguments" : ["operation", "variable", "limit", "content"]
    
function
    "arguments" : ["def_or_call", "function_name", "argument_1", "argument_2", "content"]

return
    "arguments" : ["value"]
    
literal
    "arguments" : ["value"]
'''

#~~~~~~~~~~~ SET UP ~~~~~~~~~~~#

global ast, latest_id, latest_multi_id, latest_scope, trans_func, trans_loop, line_reading_in
ast = []
latest_id = 0
latest_multi_id = 0
latest_scope = 0
trans_func = False
trans_loop = False
line_reading_in = 1

def calc_id():

    global latest_id, latest_scope
    new_id = round(line_reading_in*100 + latest_id + (1 * 10**-latest_scope), int(latest_scope))
    print("LATEST ID: " + str(new_id))
    #print("older ID: " + str(latest_id + (1 * 10**-latest_scope)))
    return new_id


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
    global latest_id
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
    latest_id = calc_id()
    ret = {
        "id" : latest_id,
        "original" : l,
        "type" : "math",
        "arguments" : [operator, arg1, arg2],
        "body" : []
        }
    return ret


def booleanParse(l, o):
    global latest_id
    tokens = l.split() 
    operator = o
    arg1 = tokens[2]
    arg2 = tokens[4]
    latest_id = calc_id()
    ret = {
        "id" : latest_id,
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
    commentIndex = statement.find('BTW')
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

def parseLOL(line):
    global latest_id, ast
    '''
    https://github.com/justinmeza/lolcode-spec/blob/master/v1.3/lolcode-spec-v1.3.md
    '''
    prediction = ""
    bare_content = stripStatement(line)
    ret = {}
    if bare_content == "":
        prediction += "empty line"
    if "HAI" in bare_content:
        prediction += "start of file; ignore"
    elif "KTHXBYE" in bare_content:
        prediction += "end of file; ignore"
        #COMMENTS
    elif "OBTW" in line:
        content = line[5:]
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "comment",
            "arguments" : [content], 
            "body" : []
            }
    elif "BTW" in line:
        content = line[4:]
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "comment",
            "arguments" : [content], 
            "body" : []
            }
    elif "TLDR" in bare_content:
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "end_func",
            "arguments" : [], 
            "body" : []
            }
        #ignore, ends function
        pass
    elif "IM IN YR" in bare_content: #JUST DOING TWO TYPES: UPPIN (increment by one) and NERFIN (decrement by one AKA range(10, 0, -1)
        tokens = line.split()
        operation = tokens[4] #UPPIN or NERFIN
        variable = tokens[6]
        limit = tokens[12] #assuming every loop ends with BOTH SAEM condition
        content = []
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "loop",
            "arguments" : [operation, variable, limit, content], 
            "body" : []
            }
    elif "IM OUTTA YR" in bare_content:
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "end_loop",
            "arguments" : [], 
            "body" : []
            }
        #ignore, not in python...
        pass
    elif "I IZ" in bare_content:
        tokens = line.split()
        def_or_call = "call"
        function_name = tokens[2]
        if "[YR" in bare_content:
            argument_1 = tokens[4] #after [YR
        if "[AN YR" in bare_content:
            argument_2 = tokens[7].strip(']]') #after [AN YR
        content = []
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "function",
            "arguments" : [def_or_call, function_name, argument_1, argument_2], #doesn't have content because call
            "body" : []
            }
    elif "HOW IZ I" in bare_content: #limited to two arguments!
        tokens = line.split()
        def_or_call = "def"
        function_name = tokens[3]
        if "[YR" in bare_content:
            argument_1 = tokens[5] #after [YR
        else:
            argument_1 = ""
        if "[AN YR" in bare_content:
            argument_2 = tokens[8].strip(']]')#after [AN YR
        else:
            argument_2 = ""
        content = []
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "function",
            "arguments" : [def_or_call, function_name, argument_1, argument_2, content], 
            "body" : []
            }
    elif "FOUND YR" in bare_content: #return statement is its own type, in the multiline
        strip = line.strip()
        value = parseLOL(strip[9:])
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "return",
            "arguments" : [value], #doesn't have content because call
            "body" : []
            }
    elif "IF U SAY SO" in bare_content:
        #ignore, ends function
        pass
    #COMPARISON --> if statements
    elif "O RLY?" in bare_content:
        tokens = line.split()
        content = []
        if "BOTH SAEM" in bare_content:
            operator = "=="
            argument_1 = tokens[2]
            argument_2 = tokens[4].strip(',')
        elif "DIFFRINT" in bare_content:
            operator = "!="
            argument_1 = tokens[1]
            argument_2 = tokens[2].strip(',')
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "conditional",
            "arguments" : [operator, argument_1, argument_2, content],
            "body" : []
            }
    elif "YA RLY" in bare_content: #THREE COMMANDS POSSIBLE... 
        if_or_else = "if"
        content = []
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "if-else",
            "arguments" : [if_or_else, content],
            "body" : []
        }
    elif "NO WAI" in bare_content: 
        if_or_else = "else"
        content = [] 
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "if-else",
            "arguments" : [if_or_else, content],
            "body" : []
        }
    elif "OIC" in bare_content:
        #ignore, if statement ended
        pass
    elif "I HAS A" in bare_content:
        if "ITZ A" in bare_content:
            # I HAS A <x> ITZ A <y>
            tokens = line.split()
            variable_name = tokens[3]
            assigned_type = tokens[6]
            latest_id = calc_id()
            ret = {
                "id" : latest_id,
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
            latest_id = calc_id()
            ret = {
                "id" : latest_id,
                "original" : line,
                "type" : "assign",
                "arguments" : [variable_name, assigned_value],
                "body" : []
            }
            prediction += "assigns value to variable"
        else:
            tokens = line.split()
            variable_name = tokens[3]
            latest_id = calc_id()
            ret = {
                "id" : latest_id ,
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
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "assign", #this is the same type as initializing and assigning-- is that okay...
            "arguments" : [variable_name, assigned_value], 
            "body" : []
        }    
        prediction += "assinging value to variable"
    #are we including SRS, YARN & regular identifier?
    elif "VISIBLE" in bare_content:
        tokens = line.split()
        value = parseLOL(" ".join(tokens[1:]))
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
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
    #BOOLEAN
    elif "BOTH OF" in bare_content:
        ret = booleanParse(line, "and")
    elif "EITHER OF" in bare_content:
        ret = booleanParse(line, "or")
    elif "WON OF" in bare_content:
        ret = booleanParse(line, "^")
    elif "NOT" in bare_content:
        tokens = line.split()
        arg1 = tokens[1]
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "boolean",
            "arguments" : ["not", arg1],
            "body" : []
            }
    else:
        latest_id = calc_id()
        ret = {
            "id" : latest_id,
            "original" : line,
            "type" : "literal",
            "arguments" : [line],
            "body" : []
        }
    #print(f'{line} ---> {prediction}')

    return ret

def parseMulti(line):
    global latest_multi_id, ast
    for dictionary in ast:
        if dictionary == {}:
            pass
        else:
            #print(dictionary["id"])
            if dictionary["id"] == latest_multi_id:
                if dictionary["type"] == "comment":
                    dictionary["arguments"][0] += line
                elif dictionary["type"] == "loop" or dictionary["type"] == "conditional":
                    #print("parsing multi line: " + line)
                    #print(parseLOL(line))
                    dictionary["arguments"][3] += [parseLOL(line)]
                elif dictionary["type"] == "function":
                    dictionary["arguments"][4] += [parseLOL(line)]
                elif dictionary["type"] == "if-else":
                    dictionary["arguments"][2] += [parseLOL(line)]
    pass


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
    print("STARTING TRANSLATION")
    for dictionary in ast:
        if dictionary == {}:
            pass
        else:
            #print(dictionary)
            #ret += "    " * (len(str(dictionary["id"]).strip(".0")) - 1)
            ret += translate_expression(dictionary)
                
        ret += '\n'
    print(ret)

def translate_expression(dictionary):
    global trans_func, trans_loop
    if dictionary == {}:
        return ""
    ret = ""
    #if trans_func:
    #    ret += "    "
    #if trans_loop:
    #    ret += "    "
    temp_id = dictionary["id"]
    temp_type = dictionary["type"]
    temp_args = dictionary["arguments"]
    if temp_type == "literal":
        ret = temp_args[0]
    elif temp_type == "declare":
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
        ret += f'{temp_args[1]} {temp_args[0]} {temp_args[2]}'
    elif temp_type == "print":
        ret += f'print({translate_expression(temp_args[0])})'
    elif temp_type == "comment":
        ret += f'#{temp_args[0]}'.strip()
    elif temp_type == "boolean":
        if len(temp_args) == 2:
            ret += f'{temp_args[0]} {temp_args[1]}'
        else:
            ret += f'{temp_args[1]} {temp_args[0]} {temp_args[2]}'
    elif temp_type == "function":
        if temp_args[0] == 'def':
            #trans_func = True
            ret += f'def {temp_args[1]}('
            if temp_args[2] != "":
                ret += temp_args[2]
            if temp_args[3] != "":
                ret += f', {temp_args[3]}'
            ret += '):\n'
            for child_line in temp_args[4]:
                ret += f'{translate_expression(child_line)}\n'
        elif temp_args[0] == 'call': 
            ret += f'{temp_args[1]}('
            if temp_args[2] != "":
                ret += temp_args[2]
            if temp_args[3] != "":
                ret += f', {temp_args[3]}'
            ret += ')'
    elif temp_type == "end_func":
        #trans_func = False
        ret = ""
    elif temp_type == "end_loop":
        #trans_loop = False
        ret = ""
    elif temp_type == "loop":
        #trans_loop = True
        if temp_args[0] == "UPPIN":
            ret += f'for {temp_args[1]} in range({temp_args[2]}):'
        else:
            ret += f'for {temp_args[1]} in range(0,{temp_args[2]},-1):'
    elif temp_type == "return":
        ret += f'return {translate_expression(temp_args[0])}'
    elif temp_type == "conditional":
        ret += f'if {temp_args[1]} {temp_args[0]} {temp_args[2]}:'
    elif temp_type == "if-else" and temp_args[0] == 'else':
        ret += 'else:'

    return ret

#~~~~~~~~~~~ RUN ~~~~~~~~~~~#

def run(s):
    global latest_id, latest_multi_id, latest_scope, ast, line_reading_in
    lines = s.splitlines()
    for line in lines:
        leading_spaces = len(line) - len(line.strip())
        latest_scope = leading_spaces/4
        if latest_scope > 0:
            #print("latest multi " + str(latest_multi_id))
            parseMulti(line)

        else:
            ast += [parseLOL(line)]
            latest_multi_id = latest_id
        print(1)
        line_reading_in += 1
    print_ast()
    print('-------\nTRANSLATED::')
    translate()

#~~~~~~~~~~~ TESTING ~~~~~~~~~~~#


LOLCODE = read("sampleLOL.txt")
print(f'ORIGINAL::\n\n{LOLCODE}')
run(LOLCODE)


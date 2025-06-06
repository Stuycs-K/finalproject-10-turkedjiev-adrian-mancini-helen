# Dev Log:

This document must be updated daily every time you finish a work session.

## Helen Mancini
### 2025-05-15 - Cloned repo, began research on esolang LOLCAT, made plan
Decided between esoteric coding languages, decided to begin coding a language interpreter for a subset of python (print statements, while loops, conditionals, vars, arithmatic etc...). 
- https://en.wikipedia.org/wiki/LOLCODE
- https://gist.github.com/sharmaeklavya2/8a0e2581baf969be0f64
  
We also made codeplan.txt and outlined our plan for coding the interpreter. 

### 2025-05-16 - ABSENT
### 2025-05-19 - ABSENT

### 2025-05-20 - Began interpret.py
Wrote the read function
Researched more about LOLCODE interpreters:
- https://lokalise.com/blog/lolcode-tutorial-on-programming-language-for-cat-lovers/#Installing_LOLCODE_interpreter
- COMPREHENSIVE DOCUMENTATION: https://github.com/justinmeza/lolcode-spec/blob/master/v1.2/lolcode-spec-v1.2.md
- NOTES: LOLCODE files (ex. program.lol) must start with HAI 1.2. Comments start with BTW. All programs end in KTHXBYE.
- Most LOLCODE interpreters interpret lolcode into other languages to run them-- we may want to make a program that translates python into lolcode as a method of obfuscation rather than a standard interpreter...

### 2025-05-21 - Worked on interpret.py, parse function
Spliting strings of python into arrays to be catagorized as different python functions and translated
Possibly can use AST (what Adrian researched for this)?

### 2025-05-22 - ABSENT, AP Calc BC Exam
### 2025-05-23 - ABSENT, excused for national debate tournament
### 2025-05-25 - HOMEWORK: Pivoting project to something more manageable per Mr. K's advice?
- Found MD5 implementation walkthrough materials: https://www.youtube.com/watch?v=HWpaz5XsECc
- Notes: MD5 takes a message of any length and outputs a digest that is always 128 bits. It's a broken secure hash, but important historically...
- Need to make sure we get it correct including "asdf"

### 2025-05-27 - Decided on modified project (not MD5): lolcode translator.
- updated sample code
- planned out parse handling of multiline commands, began implementation...

### 2025-05-28 - ABSENT, SICK
### 2025-05-29 - implementation in translate.py, specifically math functions
- began with SUM OF, spliting command into arguments w/ in math type
- need to figure out how to handle things like SUM OF QUOTIENT OF... (recursive)
- testing with this online interpreter: https://www.jdoodle.com/execute-lolcode-online

### 2025-05-29 - HOMEWORK: continuing implementing math type
- made function mathParse so wouldn't need to repeat code
- using list indices to do recursive call, need to test if dictionary gets correctly printed
- missing mod function.. any others?

### 2025-05-30 - implementing all types in dictionary
- used same recursive logic to find parts of a line that need to be parsed again for other commands
- implemented LOLCODE parsing for variable assign, variable instantiate, print commands
- also added mod to math

### 2025-05-30 - 2025-06-1 - HOMEWORK: issues with math function
- needs recursion on both sides of "AN" but need to find how to identify (when there are multiple "AN"s in a statement)

### 2025-06-2 - parsing more types & parsing through multiline code
- parsing through booleans with booleanParse(line)
- parsing comments (BTW and OBTW)
- create latest_multi_id to track the first line of a multiline piece of code
- parseMulti() recursively calls parseLOL() for indented lines after ^

### 2025-06-2 - HOMEWORK:
- parse through loops, if statements, functions and calls, multiline comments
- add to parseMulti()

### 2025-06-3 - : continued debugging parse, wrote more test code, and filmed video!
- submitted project

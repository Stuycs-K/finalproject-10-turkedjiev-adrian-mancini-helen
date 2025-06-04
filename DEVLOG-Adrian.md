# Dev Log:

This document must be updated daily every time you finish a work session.

## Adrian Turkedjiev

### 2025-05-15 - Research

- Looked at a number of esoteric coding languages (brainfuck, whitespace, LOLCAT, malborn) and decided on LOLCAT, as it is most similar to python and easiest to read.
- Tried to find LOLCAT documentation:
    - https://gist.github.com/sharmaeklavya2/8a0e2581baf969be0f64
    - https://clever-thompson-493f7c.netlify.app/docs/operators/
    - https://lokalise.com/blog/lolcode-tutorial-on-programming-language-for-cat-lovers/

### 2025-05-16 - More Research

- I started looking into how we could parse python code into distinct expressions. It seems like the way to do this is to use AST, a built-in python module.
- I began trying to learn about AST's syntax and Abstract Syntax Trees using these sources:
    - https://docs.python.org/3/library/ast.html (the documentation for AST)
    - https://medium.com/@wshanshan/intro-to-python-ast-module-bbd22cd505f7
    - https://github.com/xbeat/Machine-Learning/blob/main/Exploring%20Python's%20Abstract%20Syntax%20Tree%20Manipulation.md
 
### 2025-05-19 - ABSENT (Traveling) 

### 2025-05-20 - ABSENT (Traveling) 

### 2025-05-21 - ABSENT (AP Test)

### 2025-05-22 - ABSENT (AP Test)

### 2025-05-(23-26) - Reorienting Project

- Recieved feedback that intial project was unfeasible.
- Decided to instead translate LOLCODE into Python code, with the potential extension of translating LOLCODE to other similar esoteric languages
- Updated README

### 2025-05-27 - Start of Implementation 

- created stripStatement() method to aid in classification of LOLCODE statements.
- began work on parseLOL() method, simply identifying what is happening in each line of LOLCODE. 
    - working based of this LOLCODE documentation: https://github.com/justinmeza/lolcode-spec/blob/master/v1.3/lolcode-spec-v1.3.md
    - Have so far ommitted the following aspects of LOLCODE: 
        - Function types are declared/initialized using the HOW DUZ I / IF U SAY SO blocks, however they behave the same as variables
        - The SRS operation can be used to interpret a YARN (or something castable to a YARN) as an identifier. This operator may be used anywhere that a regular identifier is expected.

### 2025-05-28 - Fleshing out Syntax

- continued work on parse method, began running into problems of nest statments (e.g., '+=')
- reorganized code for recursive approach

### 2025-05-29 - AST
- Researched ASTs to refine approach to ast dictionary, using these sources: https://lisperator.net/pltut/parser/; https://www.alternetsoft.com/blog/code-parsing-explained
- Defined the general structure of our ast dictionary 

### 2025-30-02 - ABSENT (Sick)

### 2025-06-02 - Building out translation to python
- created translate() with helper translate_expression() to take AST dictionary and output string of python code. So far implemented for variable assignments / declarations, math and printing. 

### 2025-06-03 - Final
- Finished all elements of translate
- Debugged code
- created makefile
- Recorded final video!

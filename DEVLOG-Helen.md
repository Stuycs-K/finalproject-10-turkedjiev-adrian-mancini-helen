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

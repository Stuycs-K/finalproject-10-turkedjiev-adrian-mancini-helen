[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/am3xLbu5)
# LOLCODE INTERP
 
### HEN-TURKEY

Members: Helen Mancini and Adrian Turkedjiev

### Project Description:

We are making a LOLCODE to Python Langage Translator, wherein LOLCODE is translated into a python file, which can then be run. 

### Instructions:

Nothing needs to be installed for this program. A user simply has to create a text file containing the LOLCODE they wish to be translated. If you want to generate a python file from LOLCODE, run the following command:

```
make translate ARGS="<input_LOLCODE_file_name> <output_PYTHON_file_name>"
```

If you want to simply run a LOLCODE file, you can run:

```
make run ARGS="<input_LOLCODE_file_name>"
```

This creates a temporary Python file with the translated LOLCODE, executes it, and then deletes it. 

### Resources / References:

#### LOLCODE Documentation:
- https://github.com/justinmeza/lolcode-spec/blob/master/v1.3/lolcode-spec-v1.3.md (primarily used)
- https://gist.github.com/sharmaeklavya2/8a0e2581baf969be0f64
- https://clever-thompson-493f7c.netlify.app/docs/operators/
- https://lokalise.com/blog/lolcode-tutorial-on-programming-language-for-cat-lovers/

#### AST Resources:
- https://docs.python.org/3/library/ast.html (the documentation for Python's AST)
- https://medium.com/@wshanshan/intro-to-python-ast-module-bbd22cd505f7
- https://github.com/xbeat/Machine-Learning/blob/main/Exploring%20Python's%20Abstract%20Syntax%20Tree%20Manipulation.md
- https://lisperator.net/pltut/parser/
- https://www.alternetsoft.com/blog/code-parsing-explained

While we didn't end up using Python's AST module, we used these resources to understand how parsing into Abstract Syntax Trees for later translation should be approached. 

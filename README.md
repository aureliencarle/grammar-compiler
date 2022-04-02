# Grammar Compiler

Provides a grammar compiler taking as input a grammar file (EBNF format, see 
[the wiki](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form))
and generates a parser program for this particular grammar.

The generated program should be able to parse a file written in the language
the grammar defines and store the file content in a human-readable tree-like
object. This is in particular the first step to create a new programming
language.

**Example:** The string "int a = 5;" parsed with the C grammar should 
correspond to an internal object, created by the generated parser, such as:
```
{
  instruction: {
    type: 'assignement',
    lhs: { var: { 'type': 'int', 'name': 'a' } },
    rhs: { integer: { 5 } }
  }
}
```
The grammar compiler must in this case read the C grammar file and generate
the parser able to parse C programs and provide users a simple object 
representation of the file for further processing.

**Note:** The generated parser will have no knowledge of the language meaning,
its purpose is only to decompose the file in tokens corresponding to the 
grammar. Processing the tokens to actually interpret the language and do 
something with it is an independent task.

### Grammars

Grammar files should be stored in the `grammars/` directory (except possible
test grammars) and have the `.grm` extension.

All grammars should use the EBNF format (see `grammars/ebnf.grm` to see
the associated grammar).


### Authors

- A. Carle
- G. Uhlrich

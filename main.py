from classes.lexer import Lexer
from classes.parser import Parser

lex = Lexer()
lexer = lex.build()
file = open("./tests/ph2test2.txt")
text_input = file.read()
file.close()
# result = open("result3.txt", "w")
lexer.input(text_input)
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     result.write(str(tok))
#     result.write("\n")
# result.close()
parser = Parser()
parser.build().parse(text_input, lexer, False)

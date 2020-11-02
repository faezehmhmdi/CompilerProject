from lexer import Lexer

lex = Lexer()
lexer = lex.build()
file = open("test3.txt")
text_input = file.read()
file.close()
result = open("result3.txt", "w")
lexer.input(text_input)
while True:
    tok = lexer.token()
    if not tok:
        break
    result.write(str(tok))
    result.write("\n")
result.close()

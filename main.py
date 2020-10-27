from lexer import Lexer

lex = Lexer()
lexer = lex.build()
file = open("test3.txt")
text_input = file.read()
file.close()
lexer.input(text_input)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

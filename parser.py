from ply import yacc
from classes.lexer import Lexer


class Parser:
    tokens = Lexer().tokens

    def __init__(self):
        pass

    # program
    def p_program(self, p):
        """program : declist MAIN LRB RRB block"""
        print("program : declist MAIN LRB RRB block")

    # declist
    # declist -> dec is removed
    def p_declist(self, p):
        """declist : declist dec
        | """
        print("declist : declist dec | ")

    # dec
    def p_dec(self, p):
        """dec : vardec
        | funcdec"""
        print("dec : vardec | funcdec")

    # type
    def p_type(self, p):
        """type : INTEGER
        | FLOAT
        | BOOLEAN"""
        print("type : INTEGER | FLOAT | BOOLEAN")

    # iddec
    def p_iddec(self, p):
        """iddec : ID
        | ID LSB exp RSB
        | ID ASSIGN exp"""
        print("iddec : ID | ID LSB exp RSB | ID ASSIGN exp")

    # idlist
    def p_idlist(self, p):
        """idlist : iddec
        | idlist COMMA iddec"""
        print("idlist : iddec | idlist COMMA iddec")

    # vardec
    def p_vardec(self, p):
        """vardec : idlist COLON type SEMICOLON"""
        print("vardec : idlist COLON type SEMICOLON")

    # funcdec
    def p_funcdec(self, p):
        """funcdec : FUNCTION ID LRB paramdecs RRB COLON type block
        | FUNCTION ID LRB paramdecs RRB block"""
        print(
            "funcdec : FUNCTION ID LRB paramdecs RRB COLON type block | FUNCTION ID LRB paramdecs RRB block")

    # paramdecs
    def p_paramdecs(self, p):
        """paramdecs : paramdecslist
        | """
        print("paramdecs : paramdecslist | ")

    # paramdecslist
    def p_paramdecslist(self, p):
        """paramdecslist : paramdec
        | paramdecslist COMMA paramdec"""
        print("paramdecslist : paramdec | paramdecslist COMMA paramdec")

    # paramdec
    def p_paramdec(self, p):
        """paramdec : ID COLON type
        | ID LSB RSB COLON type"""
        print("paramdec : ID COLON type | ID LSB RSB COLON type")

    # block
    def p_block(self, p):
        """block : LCB stmtlist RCB"""
        print("block : LCB stmtlist RCB")

    # stmtlist
    # stmtlist -> stmt is removed
    def p_stmtlist(self, p):
        """stmtlist : stmtlist stmt
        | """
        print("stmtlist : stmtlist stmt | ")

    # lvalue rule is removed
    # def p_lvalue(self, p):
    #     """ID
    #     | ID LSB exp RSB"""

    # case
    def p_case(self, p):
        """case : WHERE const COLON stmtlist"""
        print("case : WHERE const COLON stmtlist")

    # cases
    # cases -> case is removed
    def p_cases(self, p):
        """cases : cases case
        | """
        print("cases : cases case | ")

    # stmt
    # precedence used for dangling elseif and else
    def p_stmt(self, p):
        """stmt : RETURN exp SEMICOLON
        | exp SEMICOLON
        | block
        | vardec
        | WHILE LRB exp RRB stmt
        | ON LRB exp RRB LCB cases RCB SEMICOLON
        | FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt
        | FOR LRB ID IN ID RRB stmt
        | IF LRB exp RRB stmt elseiflist %prec IF
        | IF LRB exp RRB stmt elseiflist ELSE stmt
        | PRINT LRB ID RRB SEMICOLON"""
        print(
            "stmt : RETURN exp SEMICOLON | exp SEMICOLON | block | vardec | WHILE LRB exp RRB stmt | ON LRB exp RRB LCB cases RCB SEMICOLON | FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt | FOR LRB ID IN ID RRB stmt | IF LRB exp RRB stmt elseiflist %prec IFCONTROL | IF LRB exp RRB stmt elseiflist ELSE stmt | PRINT LRB ID RRB SEMICOLON")

    # elseiflist
    # elseiflist -> ELSEIF LRB exp RRB stmt is removed
    def p_elseiflist(self, p):
        """elseiflist : elseiflist ELSEIF LRB exp RRB stmt
        | """
        print("elseiflist : elseiflist ELSEIF LRB exp RRB stmt | ")

    # relopexp
    # relope chnaged
    def p_relopexp(self, p):
        """relopexp : exp GT exp
        | exp LT exp
        | exp NE exp
        | exp EQ exp
        | exp LE exp
        | exp GE exp"""
        print("relop : exp GT exp | exp LT exp | exp NE exp | exp EQ exp | exp LE exp | exp GE exp")

    # operatorexp
    # operator changed
    def p_operatorexp(self, p):
        """operatorexp : exp AND exp
        | exp OR exp
        | exp SUM exp
        | exp SUB exp
        | exp DIV exp
        | exp MOD exp
        | exp MUL exp"""
        print(
            "operator : exp AND exp | exp OR exp | exp SUM exp | exp SUB exp | exp DIV exp | exp MOD exp | exp MUL exp")

    # exp
    # exp -> exp operator exp changed to exp -> operator
    # exp -> relopexp changed to exp -> relop
    def p_exp(self, p):
        """exp : ID ASSIGN exp
        | ID LSB exp RSB ASSIGN exp
        | operatorexp
        | relopexp
        | const
        | ID
        | ID LSB exp RSB
        | ID LRB explist RRB
        | LRB exp RRB
        | SUB exp
        | NOT exp"""
        print(
            "exp : ID ASSIGN exp | ID LSB exp RSB ASSIGN exp | operator | relop | const | ID | ID LSB exp RSB | ID LRB explist RRB | LRB exp RRB | SUB exp | NOT exp")

    # const
    def p_const(self, p):
        """const : FLOATNUMBER
        | INTEGERNUMBER
        | TRUE
        | FALSE"""
        print("const : FLOATNUMBER | INTEGERNUMBER | TRUE | FALSE")

    # explist
    def p_explist(self, p):
        """explist : exp
        | explist COMMA exp"""
        print("explist : exp | explist COMMA exp")

    def p_error(self, p):
        print('Parsing Error : Invalid grammar at : ', p)
        # raise Exception('Parsing Error : Invalid grammar at ', p.value)

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'NOT'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GE'),
        ('left', 'LT', 'LE'),
        ('right', 'ASSIGN'),
        ('left', 'MOD'),
        ('left', 'SUM', 'SUB'),
        ('left', 'MUL', 'DIV'),
        ('left', 'IF'),
        ('left', 'ELSE', 'ELSEIF')
    )

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

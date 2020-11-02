from ply import lex


class Lexer:
    # Reserved
    reserved = {
        'int': 'INTEGER',
        'float': 'FLOAT',
        'bool': 'BOOLEAN',
        'fun': 'FUNCTION',
        'True': 'TRUE',
        'False': 'FALSE',
        'print': 'PRINT',
        'return': 'RETURN',
        'main': 'MAIN',
        'if': 'IF',
        'else': 'ELSE',
        'elseif': 'ELSEIF',
        'while': 'WHILE',
        'on': 'ON',
        'where': 'WHERE',
        'for': 'FOR',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'in': 'IN'
    }
    # Tokens
    tokens = [
        'ID', 'INTEGERNUMBER', 'FLOATNUMBER', 'INTEGER', 'FLOAT', 'BOOLEAN', 'FUNCTION',
        'TRUE', 'FALSE', 'PRINT', 'RETURN', 'MAIN', 'IF', 'ELSE', 'ELSEIF', 'WHILE', 'ON',
        'WHERE', 'FOR', 'AND', 'OR', 'NOT', 'IN', 'ASSIGN', 'SUM', 'SUB', 'MUL', 'DIV',
        'MOD', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'LCB', 'RCB', 'LRB', 'RRB', 'LSB', 'RSB',
        'SEMICOLON', 'COLON', 'COMMA', 'ERROR'
    ]

    # Check for correct IDs
    def t_ID(self, t):
        r'[a-z_]([a-zA-Z0-9_])*'
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        return t

    # Check True (Because it's similar to identifier starting with capital letter)
    def t_TRUE(self, t):
        r'True'
        return t

    # Check False (Because it's similar to identifier starting with capital letter)
    def t_FALSE(self, t):
        r'False'
        return t

    # ERROR
    def t_ERROR(self, t):
        r"""([0-9A-Z]([0-9]*[a-zA-Z_][0-9]*)+)
        | ([A-Z][0-9a-zA-Z_]*)
        | (\.[0-9]+)
        | (([0-9]+\.[0-9]+\.)[0-9\.]*)
        | (0*((?=[0-9]{10,}\.)(([1-9]+0*)+|0)\.((0*[1-9]+)+|0))0*)
        | (0*[1-9][0-9]{9,})
        | [/%\-\*\+](\s*[/%\-\*\+])+
        """
        # (0*((([1-9]+0*)+|0)(?=\.[0-9]{10,}[1-9])\.((0*[1-9]+)+|0))0*) #decimal part more than 10 digits without trailing zero
        return t

    # Check float
    def t_FLOATNUMBER(self, t):
        r'0*((([1-9]+0*)+|0)\.((0*[1-9]+)+|0))0*'
        t.value = float(t.value)
        return t

    # Check integer
    def t_INTEGERNUMBER(self, t):
        # r'([1-9][0-9]{0,9}(?![0-9]*\.))|0'
        r'[1-9]\d{0,9}|0'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise Exception('Error at ', t.value[0])

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    # Lexeme
    t_ASSIGN = r'\='
    t_SUM = r'\+'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_MOD = r'\%'
    t_GT = r'\>'
    t_GE = r'\>='
    t_LT = r'\<'
    t_LE = r'\<='
    t_EQ = r'\=='
    t_NE = r'\!='
    t_LCB = r'\{'
    t_RCB = r'\}'
    t_LRB = r'\('
    t_RRB = r'\)'
    t_LSB = r'\['
    t_RSB = r'\]'
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_ignore = '\n \t\r\f\v'

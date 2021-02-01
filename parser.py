from ply import yacc
from classes.lexer import Lexer
from classes.nonTerminal import NonTerminal


class Parser:
    tokens = Lexer().tokens

    def __init__(self):
        self.tempCount = 0
        self.labelCount = 0
        self.nextState = 0
        self.file = open('output.c', 'w')
        self.file.write("#include <stdio.h>\nint array[(int)1e6];\nint arr_pointer = 0;\n")
        self.arr_start = 0
        self.arr_last = 0
        self.value_label = {}
        pass

    def p_program(self, p):
        """program : declist MAIN LRB RRB block"""
        p[0] = NonTerminal()
        p[0].code = "int " + p[2] + " " + p[3] + p[4] + "{\n" + p[1].code + p[5].code + "}"
        self.file.write(p[0].code)
        pass

    def p_declist_declistdec(self, p):
        """declist : declist dec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + "\n" + p[2].code
        pass

    def p_declist_epsilon(self, p):
        """declist : """
        p[0] = NonTerminal()
        p[0].code = ""
        pass

    def p_dec_vardec(self, p):
        """dec : vardec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_dec_funcdec(self, p):
        """dec : funcdec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_type_int(self, p):
        """type : INTEGER"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_type_float(self, p):
        """type : FLOAT"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_type_boolean(self, p):
        """type : BOOLEAN"""
        p[0] = NonTerminal()
        p[0].type = p[1]

    def p_iddec_id(self, p):
        """iddec : ID"""
        p[0] = NonTerminal()
        p[0].code = "int " + p[1]
        pass

    def p_iddec_idlsbrsb(self, p):
        """iddec : ID LSB exp RSB"""
        p[0] = NonTerminal()
        p[0].code = "int " + p[1] + " = " + "arr_pointer;\n" + "arr_pointer += " + str(p[3].get_value())
        # self.arr_last += p[3].get_value()
        pass

    def p_iddec_idassignexp(self, p):
        """iddec : ID ASSIGN exp"""
        p[0] = NonTerminal()
        p[0].code = p[3].code + "int " + p[1] + " " + p[2] + " " + str(p[3].get_value())
        pass

    def p_idlist_iddec(self, p):
        """idlist : iddec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_idlist_comma(self, p):
        """idlist : idlist COMMA iddec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + ";\n" + p[3].code
        pass

    def p_vardec(self, p):
        """vardec : idlist COLON type SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + p[4] + "\n"
        pass

    def p_funcdec_1(self, p):
        """funcdec : FUNCTION ID LRB paramdecs RRB COLON type block"""
        p[0] = NonTerminal()
        p[0].code = p[1] + p[2] + p[3] + p[4].code + p[5] + p[6] + p[7].value + p[8]
        pass

    def p_funcdec_2(self, p):
        """funcdec : FUNCTION ID LRB paramdecs RRB block"""
        p[0] = NonTerminal()
        p[0].code = p[1] + p[2] + p[3] + p[4].code + p[5] + p[6].code
        pass

    def p_paramdecs_paramdecslist(self, p):
        """paramdecs : paramdecslist"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code
        pass

    def p_paramdecs_epsilon(self, p):
        """paramdecs : """
        p[0] = NonTerminal()
        p[0].code = ""
        pass
        # print("paramdecs : ")

    def p_paramdecslist_paramdec(self, p):
        """paramdecslist : paramdec"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code
        pass

    def p_paramdecslist_extended(self, p):
        """paramdecslist : paramdecslist COMMA paramdec"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code + p[2] + p[3].code
        print(p[0].code)
        pass

    def p_paramdec_1(self, p):
        """paramdec : ID COLON type"""
        p[0] = NonTerminal()
        p[0].place = p[1].place
        p[0].code = p[1] + p[2] + p[3].value
        print(p[0].code)
        pass

    def p_paramdec_2(self, p):
        """paramdec : ID LSB RSB COLON type"""

    def p_block(self, p):
        """block : LCB stmtlist RCB"""
        p[0] = NonTerminal()
        p[0].code = p[2].code
        pass

    def p_stmtlist_stmtliststmt(self, p):
        """stmtlist : stmtlist stmt"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + p[2].code
        pass

    def p_stmtlist_epsilon(self, p):
        """stmtlist : """
        p[0] = NonTerminal()
        pass

    def p_case(self, p):
        """case : WHERE exp COLON stmtlist"""
        p[0] = NonTerminal()
        label = self.new_label()

        p[0].switchValue = str(p[2].get_value())
        p[0].switchLabel = label
        self.value_label[str(p[2].get_value())] = label
        p[0].code = label + ": ;\n{" + p[4].code + "goto Last;\n}\n"

    def p_cases_casescase(self, p):
        """cases : cases case"""
        p[0] = NonTerminal()
        self.value_label[p[2].switchValue] = p[2].switchLabel
        p[0].code = p[1].code + p[2].code

    def p_cases_epsilon(self, p):
        """cases : """
        p[0] = NonTerminal()
        pass

    def p_stmt_return(self, p):
        """stmt : RETURN exp SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = p[2].code + p[1] + " " + p[2].get_value() + p[3]
        pass

    def p_stmt_expsemicolon(self, p):
        """stmt : exp SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_stmt_block(self, p):
        """stmt : block"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_stmt_vardec(self, p):
        """stmt : vardec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_stmt_while(self, p):
        """stmt : WHILE LRB exp RRB stmt"""
        p[0] = NonTerminal()
        p[0].begin = self.new_label()
        p[0].after = self.new_label()
        p[0].code = p[0].begin + ": ;\n" + p[3].code + "if (" + str(p[3].get_value()) + " == 0" + "){\ngoto " + p[
            0].after + ";\n}\n"
        p[0].code += p[5].code + "\n"
        if p[3].isRel:
            p[0].code += "goto " + "L" + str(self.labelCount - 6) + ";\n"
        else:
            p[0].code += "goto " + p[0].begin + ";\n"
        p[0].code += p[0].after + ": ;\n"

    def p_stmt_on(self, p):
        """stmt : ON LRB exp RRB LCB cases RCB SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = ""
        for key in self.value_label:
            p[0].code += "if (" + str(p[3].get_value()) + " == " + str(key) + "){\ngoto " + self.value_label[
                key] + ";\n}\n"
        p[0].code += p[6].code
        p[0].code += "Last: ;\n"

    def p_stmt_for1(self, p):
        """stmt : FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt"""
        p[0] = NonTerminal()
        p[0].begin = self.new_label()
        # pMiddle = self.new_label()
        p[0].after = self.new_label()
        # s = p[5].code.split("\n")
        # pAgain = s[1].split(":")
        p[0].code = p[3].code + p[0].begin + ": ;\n" + p[5].code + "if (" + str(
            p[5].get_value()) + " == 0" + "){\ngoto " + p[0].after + ";\n}\n"
        p[0].code += p[9].code
        p[0].code += p[7].code + "\ngoto " + p[0].begin + ";\n"
        p[0].code += p[0].after + ": ;\n"

    def p_stmt_for2(self, p):
        """stmt : FOR LRB ID IN ID RRB stmt"""
        p[0] = NonTerminal()
        p[0].begin = self.new_label()
        # pMiddle = self.new_label()
        p[0].after = self.new_label()
        counter = self.new_temp()
        p[0].code = "int " + counter + " = 0;\n"
        p[0].code += p[0].begin + ": ;\n" + p[
            3] + " = array[" + counter + "];\nif (" + counter + " == arr_pointer){\ngoto " + p[
                         0].after + ";\n}\n"
        # p[0].code += "goto " + p[0].after + ";\n"
        p[0].code += p[7].code + counter + " += 1;\ngoto " + "L" + str(self.labelCount - 2) + ";\n"
        p[0].code += p[0].after + ": ;\n"

    def p_stmt_if1(self, p):
        """stmt : IF LRB exp RRB stmt elseiflist %prec IF"""
        p[0] = NonTerminal()
        # p[0].begin = self.new_label()
        pElse = self.new_label()
        p[0].after = self.new_label()
        if p[6].code != "":
            p[0].code = p[3].code + "if (" + str(
                p[3].get_value()) + " == 0" + "){\ngoto " + pElse + ";\n}\n" + p[5].code
            p[0].code += "goto " + p[0].after + ";\n"
            p[0].code += pElse + ": ;\n" + p[6].code
            p[0].code += p[0].after + ": ;\n"
        else:
            if p[3].isRel:
                p[0].code = p[3].code + "if (" + str(p[3].get_value()) + " == 0" + "){\ngoto " + p[0].after + ";\n}\n"
                # p[0].code += p[5].code
                p[0].code += p[0].after + ": ;\n" + p[5].code
            else:
                p[0].code = p[3].code + "if (" + str(p[3].get_value()) + " == 0" + "){\ngoto " + p[0].after + ";\n}\n"
                p[0].code += p[5].code
                p[0].code += p[0].after + ": ;\n"

    def p_stmt_if2(self, p):
        """stmt : IF LRB exp RRB stmt elseiflist ELSE stmt %prec IF"""
        p[0] = NonTerminal()
        # p[0].begin = self.new_label()
        pElse = self.new_label()
        p[0].after = self.new_label()
        if p[6].code != "":
            p[0].code = p[3].code + "if (" + str(
                p[3].get_value()) + " == 0" + "){\ngoto " + pElse + ";\n}\n" + p[5].code
            p[0].code += "goto " + p[0].after + ";\n"
            p[0].code += pElse + ": ;\n" + p[6].code
            p[0].code += p[0].after + ": ;\n"
        else:
            p[0].code = p[3].code + "if (" + str(
                p[3].get_value()) + " == 0" + "){\ngoto " + pElse + ";\n}\n" + p[5].code
            p[0].code += "goto " + p[0].after + ";\n"
            p[0].code += pElse + ": ;\n" + p[8].code
            p[0].code += p[0].after + ": ;\n"

    def p_elseiflist_extended(self, p):
        """elseiflist : elseiflist ELSEIF LRB exp RRB stmt"""
        p[0] = NonTerminal
        p[0].code = p[4].code + p[1].code + " " + p[2] + " " + p[3] + str(p[4].get_value()) + p[5] + p[6].code + "\n"

    def p_elseiflist_epsilon(self, p):
        """elseiflist : """
        p[0] = NonTerminal()

    def p_stmt_print(self, p):
        """stmt : PRINT LRB ID RRB SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = "printf" + p[2] + '"%d", ' + p[3] + p[4] + p[5] + "\n"
        pass

    def p_relopexp_GT(self, p):
        """relopexp : exp GT exp %prec EQ"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1
        pass

    def p_relopexp_LT(self, p):
        """relopexp : exp LT exp %prec EQ"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1
        pass

    def p_relopexp_NE(self, p):
        """relopexp : exp NE exp %prec EQ"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1
        pass

    def p_relopexp_EQ(self, p):
        """relopexp : exp EQ exp %prec EQ"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1
        pass

    def p_relopexp_LE(self, p):
        """relopexp : exp LE exp %prec EQ"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1
        pass

    def p_relopexp_GE(self, p):
        """relopexp : exp GE exp %prec EQ"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1
        pass

    def p_exp_sum(self, p):
        """exp : exp SUM exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code + p[3].code + "int " + p[0].place + " = "
        p[0].code += str(p[1].get_value()) + " " + p[2] + " " + str(p[3].get_value()) + ";\n"
        pass

    def p_exp_sub(self, p):
        """exp : exp SUB exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code + p[3].code + "int " + p[0].place + " = "
        p[0].code += str(p[1].get_value()) + " " + p[2] + " " + str(p[3].get_value()) + ";\n"
        pass

    def p_exp_mul(self, p):
        """exp : exp MUL exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code + p[3].code + "int " + p[0].place + " = "
        p[0].code += str(p[1].get_value()) + " " + p[2] + " " + str(p[3].get_value()) + ";\n"
        pass

    def p_exp_div(self, p):
        """exp : exp DIV exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code + p[3].code + "int " + p[0].place + " = "
        p[0].code += str(p[1].get_value()) + " " + p[2] + " " + str(p[3].get_value()) + ";\n"
        pass

    def p_exp_mod(self, p):
        """exp : exp MOD exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = p[1].code + p[3].code + "int " + p[0].place + " = "
        p[0].code += str(p[1].get_value()) + " " + p[2] + " " + str(p[3].get_value()) + ";\n"
        pass

    def p_exp_and(self, p):
        """exp : exp AND exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + p[0].place + " = " + str(p[1].get_value()) + " && " + str(
            p[3].get_value()) + ";\n"

        pass

    def p_exp_or(self, p):
        """exp : exp OR exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + p[0].place + " = " + str(p[1].get_value()) + " || " + str(
            p[3].get_value()) + ";\n"
        pass

    def p_exp_idassign1(self, p):
        """exp : ID ASSIGN exp"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        p[0].code = p[3].code + p[1] + " " + p[2] + " " + str(p[3].get_value()) + ";\n"
        pass

    def p_exp_idassign2(self, p):
        """exp : ID LSB exp RSB ASSIGN exp"""
        p[0] = NonTerminal()
        # p[0].isArray = True
        p[0].value = "array[" + p[1] + " + " + str(p[3].get_value()) + "]"
        p[0].code = p[6].code + "array[" + p[1] + " + " + str(p[3].get_value()) + "] " + p[5] + " " + str(
            p[6].get_value()) + ";\n"
        pass

    # def p_exp_const(self, p):
    #     """exp : const"""
    #     p[0] = NonTerminal()
    #     p[0].value = p[1].value
    #     p[0].isBoolean = p[1].isBoolean
    #     pass
    #     # print("exp : const")

    # def p_relopexp(self, p):
    #     """relopexp : exp relop exp %prec EQ"""
    #     p[0] = NonTerminal()
    #     p[0].isRel = True
    #     p[0].place = self.new_temp()
    #     first = self.new_label()
    #     sec = self.new_label()
    #     third = self.new_label()
    #     fourth = self.new_label()
    #     fifth = self.new_label()
    #     p[0].code = "int " + p[0].place + ";\n"
    #     p[0].code += p[1].code + p[3].code + first + ": ;\n" + "if (" + str(p[1].get_value()) + " " + p[
    #         2].value + " " + str(
    #         p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
    #     p[0].code += sec + ": ;\n" + p[0].place + " = " + str(0) + ";\n"
    #     p[0].code += third + ": ;\n" + "goto " + fifth + ";\n"
    #     p[0].code += fourth + ": ;\n" + p[0].place + " = " + str(1) + ";\n"
    #     # p[0].code += fifth + ": ;\n"
    #     self.labelCount -= 1
    #     # p[0].code = "if " + str(p[1].get_value()) + " " + p[2].value + " " + str(p[3].get_value()) + " goto " + p[
    #     #     0].true + "in;\n"
    #     # p[0].code += "goto " + p[0].false + "oon;\n"
    #     # p[0].true_list = self.make_list(self.nextState)
    #     # next_state = self.nextState + 1
    #     # p[0].false_list = self.make_list(next_state)
    #     # next_state += 1
    #     # p[0].code = str(self.nextState) + " : " + "if " + str(p[1].get_value()) + " " + p[2].value + " " + str(
    #     #     p[3].get_value()) + " goto "
    #     # p[0].code += "goto "
    #     # self.nextState += 4
    #     pass

    def p_relopexp_extended1(self, p):
        """relopexp : relopexp GT exp"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        p[0].code += after + ": ;\n"
        # p[0].code += p[0].place + " = " + str(p[1].get_value()) + " && " + str(p[0].get_value()) + ";\n"
        self.labelCount -= 1

    def p_relopexp_extended2(self, p):
        """relopexp : relopexp LT exp"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        # p[0].code += p[0].place + " = " + str(p[1].get_value()) + " && " + str(p[0].get_value()) + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1

    def p_relopexp_extended3(self, p):
        """relopexp : relopexp NE exp"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        # p[0].code += p[0].place + " = " + str(p[1].get_value()) + " && " + str(p[0].get_value()) + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1

    def p_relopexp_extended4(self, p):
        """relopexp : relopexp EQ exp"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        # p[0].code += p[0].place + " = " + str(p[1].get_value()) + " && " + str(p[0].get_value()) + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1

    def p_relopexp_extended5(self, p):
        """relopexp : relopexp LE exp"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        # p[0].code += p[0].place + " = " + str(p[1].get_value()) + " && " + str(p[0].get_value()) + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1

    def p_relopexp_extended6(self, p):
        """relopexp : relopexp GE exp"""
        p[0] = NonTerminal()
        p[0].isRel = True
        p[0].place = self.new_temp()
        p[0].trueVal = p[0].place + " = " + str(1)
        p[0].falseVal = p[0].place + " = " + str(0)
        p[0].lastExp = str(p[3].get_value())
        first = self.new_label()
        sec = self.new_label()
        third = self.new_label()
        fourth = self.new_label()
        fifth = self.new_label()
        after = self.new_label()
        x = self.new_label()

        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[1].code + p[3].code + "if (" + str(p[1].get_value()) + " " + p[
            2] + " " + str(
            p[3].get_value()) + "){\n\tgoto " + fourth + ";\n}\n"
        p[0].code += sec + ": ;\n" + p[0].falseVal + ";\n"
        p[0].code += third + ": ;\n" + "goto " + after + ";\n"
        p[0].code += fourth + ": ;\n" + p[0].trueVal + ";\n"
        # p[0].code += p[0].place + " = " + str(p[1].get_value()) + " && " + str(p[0].get_value()) + ";\n"
        p[0].code += after + ": ;\n"
        self.labelCount -= 1

    def p_exp_relop(self, p):
        """exp : relopexp %prec EXP"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        p[0].place = p[1].place

    def p_exp_id(self, p):
        """exp : ID"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_exp_idlsbrsb(self, p):
        """exp : ID LSB exp RSB"""
        p[0] = NonTerminal()
        p[0].value = "array[" + p[1] + " + " + str(p[3].get_value()) + "]"
        p[0].code = p[3].code
        pass

    def p_exp_idexplist(self, p):
        """exp : ID LRB explist RRB"""
        p[0] = NonTerminal()
        p[0].code = p[1] + p[2] + p[3].code + p[4]
        pass

    def p_exp_lrbexprrb(self, p):
        """exp : LRB exp RRB"""
        p[0] = NonTerminal()
        p[0].place = p[2].place
        p[0].code = p[2].code
        pass

    def p_exp_expsub(self, p):
        """exp : SUB exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].code = "int " + p[0].place + ";\n"
        p[0].code += p[2].code + p[0].place + " = " + p[1] + str(p[2].get_value()) + ";\n"
        pass

    def p_exp_expnot(self, p):
        """exp : NOT exp"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        # p[0].true_list = p[2].false_list
        # p[0].false_list = p[2].true_list
        p[0].code = p[2].code + p[0].place + " = " + "!" + str(p[2].get_value()) + ";\n"
        pass

    def p_const_integernumber(self, p):
        """exp : INTEGERNUMBER"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_const_floatnumber(self, p):
        """exp : FLOATNUMBER"""
        p[0] = NonTerminal()
        p[0].value = int(p[1])
        pass

    def p_const_true(self, p):
        """exp : TRUE"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].value = 1
        # p[0].true_list = self.make_list(self.nextState)
        # p[0].code = "goto " + p[0].label + "manam;\n"
        pass

    def p_exp_false(self, p):
        """exp : FALSE"""
        p[0] = NonTerminal()
        p[0].place = self.new_temp()
        p[0].value = 0
        # p[0].false_list = self.make_list(self.nextState)
        # p[0].code = "goto " + p[0].label + "anam;\n"
        pass

    def p_explist_exp(self, p):
        """explist : exp"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        pass

    def p_explist_extendec(self, p):
        """explist : explist COMMA exp"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + p[2] + " " + p[3].code

    def p_error(self, p):
        print('Parsing Error : Invalid grammar at : ', p)
        raise Exception('Parsing Error : Invalid grammar at ', p.value)

    def new_temp(self):
        temp = "T" + str(self.tempCount)
        self.tempCount += 1
        return temp

    def new_label(self):
        label = "L" + str(self.labelCount)
        self.labelCount += 1
        return label

    precedence = (
        ('left', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EXP'),
        ('left', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT'),
        ('left', 'NOT'),
        ('left', 'MOD'),
        ('left', 'SUM', 'SUB'),
        ('left', 'MUL', 'DIV'),
        ('left', 'IF'),
        ('left', 'ELSEIF', 'ELSE')
    )

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

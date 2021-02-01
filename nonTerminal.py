class NonTerminal:

    def __init__(self):
        self.value = ""
        self.code = ""
        self.place = ""
        self.true = ""
        self.false = ""
        self.quad = ""
        self.isBoolean = False
        self.isArray = False
        self.hasCode = False
        self.lastExp = ""
        self.switchValue = ""
        self.switchLabel = ""
        self.begin = ""
        self.isRel = False
        self.trueVal = ""
        self.falseVal = ""

    def get_value(self):
        if self.value == "":
            return self.place
        return self.value

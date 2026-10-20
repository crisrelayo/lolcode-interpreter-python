TEST = """
BTW start of the program
HAI
    WAZZUP
        BTW variable dec
        I HAS A num ITZ 17
    BUHBYE

    BTW print literals and variables
    VISIBLE num
KTHXBYE
"""

main(TEST)

def main():
    def __init__(self, code):
        self.code = code

    def isHAI(self):
        re = new Regex(r"")
        if re.ismatch(code):
            self.code.remove(match)
            return True
        else:
            return False

    def isStatement(self):
        pass

    def isKTHXBYE(self):
        pass

    def isComment(self):
        pass

    def isNewline(self):
        pass

    def isProgram(self):
        if self.isHAI(self.code):
            self.isStatement(self.code)

            if self.isKTHXBYE(self.code):
                # while self.isComment(self.code) or self.isNewline(self.code):
                if self.code:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


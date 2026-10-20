import re

TEST = """
HAI
    WAZZUP
        I HAS A num ITZ 17
    BUHBYE

    VISIBLE num
KTHXBYE
"""

("HAI", "start")

class Main:
    def __init__(self, code):
        self.code = code
        self.lex_tab = []
        self.tokens = [
            # Code Delimiters
            (r'HAI\b', 'Code Delimiter'),
            (r'KTHXBYE\b', 'Code Delimiter'),
            
            # Comments 
            (r'BTW.*', 'Comment Line'),
            (r'OBTW\b', 'Comment Line'),
            (r'TLDR\b', 'Comment Line'),
            
            # Variable Declaration Section 
            (r'WAZZUP\b', 'Variable Declaration Section'),
            (r'BUHBYE\b', 'Variable Declaration Section'),
            # Variable Declaration and Assignment
            (r'I HAS A\b', 'Variable Declaration'),
            (r'ITZ\b', 'Variable Assignment'),
            (r'R\b', 'Variable Assignment'),
            
            # Arithmetic Operations 
            (r'SUM OF\b', 'Arithmetic Operation'),
            (r'DIFF OF\b', 'Arithmetic Operation'),
            (r'PRODUKT OF\b', 'Arithmetic Operation'),
            (r'QUOSHUNT OF\b', 'Arithmetic Operation'),
            (r'MOD OF\b', 'Arithmetic Operation'),
            (r'BIGGR OF\b', 'Arithmetic Operation'),
            (r'SMALLR OF\b', 'Arithmetic Operation'),
            
            # Boolean Operations
            (r'BOTH OF\b', 'Boolean Operation'),
            (r'EITHER OF\b', 'Boolean Operation'),
            (r'WON OF\b', 'Boolean Operation'),
            (r'NOT\b', 'Boolean Operation'),
            (r'ANY OF\b', 'Boolean Operation'),
            (r'ALL OF\b', 'Boolean Operation'),
            
            # Comparison Operations
            (r'BOTH SAEM\b', 'Comparison Operation'),
            (r'DIFFRINT\b', 'Comparison Operation'),
            
            # String Operations
            (r'SMOOSH\b', 'String Concatenation'),
            
            # Typecasting
            (r'IS NOW A\b', 'Typecasting Operation'),
            (r'MAEK\b', 'Typecasting Operation'),
            (r'A\b', 'Typecasting Operation'),
            
            # I/O Operations
            (r'VISIBLE\b', 'Output Keyword'),
            (r'!', 'Output Separator'),  # Newline suppression
            (r'\+', 'Output Separator'),
            (r'GIMMEH\b', 'Input Keyword'),
            
            # Conditionals 
            (r'O RLY\?', 'If-then Keyword'),
            (r'YA RLY\b', 'If-then Keyword'),
            (r'MEBBE\b', 'If-then Keyword'),
            (r'NO WAI\b', 'If-then Keyword'),
            (r'OIC\b', 'Exit Keyword'),
            
            # Switch-Case
            (r'WTF\?', 'Switch-Case Keyword'),
            (r'OMG\b', 'Switch-Case Keyword'),
            (r'OMGWTF\b', 'Switch-Case Keyword'),
            
            # Loops
            (r'IM IN YR\b', 'Loop Keyword'),
            (r'IM OUTTA YR\b', 'Loop Keyword'),
            (r'UPPIN\b', 'Loop Operation'),
            (r'NERFIN\b', 'Loop Operation'),
            (r'YR\b', 'Loop Variable Assignment'),
            (r'TIL\b', 'Loop Keyword'),
            (r'WILE\b', 'Loop Keyword'),
            
            # Functions
            (r'HOW IZ I\b', 'Function Keyword'),
            (r'IF U SAY SO\b', 'Function Keyword'),
            (r'FOUND YR\b', 'Return Keyword'),
            (r'GTFO\b', 'Return Keyword'),
            (r'I IZ\b', 'Function Call'),
            (r'MKAY\b', 'Function Call Delimiter'),
            
            # Literals - STRING MUST COME BEFORE OTHER PATTERNS
            (r'\"[^\"]*\"', 'YARN Literal'),  # Closed strings
            (r'-?[0-9]+\.[0-9]+', 'NUMBAR Literal'),
            (r'-?[0-9]+', 'NUMBR Literal'),
            (r'(WIN|FAIL)', 'TROOF Literal'),
            (r'(NUMBR|NUMBAR|YARN|TROOF|NOOB)', 'Type Literal'),
            
            # Parameter Delimiter
            (r'AN\b', 'Parameter Delimiter'),
            
            # Else, Identifiers
            (r'[a-z][a-zA-Z0-9_]*', 'Variable Identifier'),
        ]

        self.isProgram()

    # def isHAI(self):
    #     re = new Regex(r"")
    #     if re.ismatch(code):
    #         self.code.remove(match)
    #         return True
    #     else:
    #         return False

    # def isStatement(self):
    #     pass

    # def isKTHXBYE(self):
    #     pass

    # def isComment(self):
    #     pass

    # def isNewline(self):
    #     pass

    def isProgram(self):
        lines = [line for line in self.code.splitlines() if line]

        for line in lines:
            values = line.split()

            for value in values:
                for pattern, token_type in self.tokens:
                    regex = re.compile(pattern)
                    match = regex.match(value)
                    
                    if match:
                        pair = (value, token_type)
                        self.lex_tab.append(pair)
        
        for pair in self.lex_tab:
            print(pair)

        # if self.isHAI(self.code):

        #     self.isStatement(self.code)

        #     if self.isKTHXBYE(self.code):
        #         # while self.isComment(self.code) or self.isNewline(self.code):
        #         if self.code:
        #             return True
        #         else:
        #             return False
        #     else:
        #         return False
        # else:
        #     return False

Main(TEST)

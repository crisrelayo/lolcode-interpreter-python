class LexerError(Exception):
    pass


class Token:
    def __init__(self, token_type, lexeme, line, col, classification):
        self.type = token_type
        self.lexeme = lexeme
        self.line = line  # starts at 1
        self.col = col  # starts at 1
        self.classification = classification

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r}, line {self.line})"


# keywords from our req 1 table, in the same order
# each row is (token type, keyword text, classification)
KEYWORDS = [
    ("HAI", "HAI", "Code Delimiter"),
    ("KTHXBYE", "KTHXBYE", "Code Delimiter"),
    ("WAZZUP", "WAZZUP", "Variable Section Delimiter"),
    ("BUHBYE", "BUHBYE", "Variable Section Delimiter"),
    ("BTW", "BTW", "Comment Delimiter"),
    ("OBTW", "OBTW", "Comment Delimiter"),
    ("TLDR", "TLDR", "Comment Delimiter"),
    ("I_HAS_A", "I HAS A", "Variable Declaration"),
    ("ITZ", "ITZ", "Variable Assignment"),
    ("R", "R", "Assignment Operator"),
    ("SUM_OF", "SUM OF", "Arithmetic Operator"),
    ("DIFF_OF", "DIFF OF", "Arithmetic Operator"),
    ("PRODUKT_OF", "PRODUKT OF", "Arithmetic Operator"),  # req 1 has a typo here, ^PRODUKT OF&$
    ("QUOSHUNT_OF", "QUOSHUNT OF", "Arithmetic Operator"),
    ("MOD_OF", "MOD OF", "Arithmetic Operator"),
    ("BIGGR_OF", "BIGGR OF", "Arithmetic Operator"),
    ("SMALLR_OF", "SMALLR OF", "Arithmetic Operator"),
    ("BOTH_OF", "BOTH OF", "Boolean Operator"),
    ("EITHER_OF", "EITHER OF", "Boolean Operator"),
    ("WON_OF", "WON OF", "Boolean Operator"),
    ("NOT", "NOT", "Boolean Operator"),
    ("ANY_OF", "ANY OF", "Infinite Arity Boolean Operator"),
    ("ALL_OF", "ALL OF", "Infinite Arity Boolean Operator"),
    ("BOTH_SAEM", "BOTH SAEM", "Comparison Operator"),
    ("DIFFRINT", "DIFFRINT", "Comparison Operator"),
    ("SMOOSH", "SMOOSH", "Concatenation Operator"),
    ("MAEK", "MAEK", "Typecast Operator"),
    ("A", "A", "Typecast Separator"),
    ("IS_NOW_A", "IS NOW A", "Recast Operator"),
    ("VISIBLE", "VISIBLE", "Output Keyword"),
    ("GIMMEH", "GIMMEH", "Input Keyword"),
    ("O_RLY", "O RLY?", "If-Else Delimiter"),
    ("YA_RLY", "YA RLY", "If Clause"),
    ("MEBBE", "MEBBE", "Else-If Clause"),
    ("NO_WAI", "NO WAI", "Else Clause"),
    ("OIC", "OIC", "Flow Control End Delimiter"),
    ("WTF", "WTF?", "Switch-Case Delimiter"),
    ("OMG", "OMG", "Case Keyword"),
    ("OMGWTF", "OMGWTF", "Default Case Keyword"),
    ("IM_IN_YR", "IM IN YR", "Loop Delimiter"),
    ("UPPIN", "UPPIN", "Loop Operation"),
    ("NERFIN", "NERFIN", "Loop Operation"),
    ("YR", "YR", "Parameter Keyword"),
    ("TIL", "TIL", "Loop Condition Keyword"),
    ("WILE", "WILE", "Loop Condition Keyword"),
    ("IM_OUTTA_YR", "IM OUTTA YR", "Loop Delimiter"),
    ("HOW_IZ_I", "HOW IZ I", "Function Delimiter"),
    ("IF_U_SAY_SO", "IF U SAY SO", "Function Delimiter"),
    ("GTFO", "GTFO", "Break Keyword"),
    ("FOUND_YR", "FOUND YR", "Return Keyword"),
    ("I_IZ", "I IZ", "Function Call Keyword"),
    ("MKAY", "MKAY", "Expression End Delimiter"),
    ("AN", "AN", "Operand Separator"),  # not in req 1, but needed to separate operands
]

import re


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

# a keyword can't be followed by a letter, digit or _, so R doesn't match the start of Rvar
# we can't use \b because there's no word boundary right after the ? in O RLY?
END_OF_WORD = r"(?![A-Za-z0-9_])"

# longer keywords are tried first, so I HAS A is tried before A
KEYWORD_PATTERNS = []
for token_type, text, classification in sorted(KEYWORDS, key=lambda row: len(row[1]), reverse=True):
    pattern = re.compile(re.escape(text) + END_OF_WORD)  # re.escape makes the ? in O RLY? a normal character
    KEYWORD_PATTERNS.append((pattern, token_type, classification))

# NUMBAR before NUMBR, or 17.0 would be read as the NUMBR 17
# a number can't be followed by a letter, digit, _ or ., so 12abc and 1.2.3 are errors
LITERAL_PATTERNS = [
    (re.compile(r"-?[0-9]*\.[0-9]+(?![A-Za-z0-9_.])"), "NUMBAR_LITERAL", "NUMBAR Literal"),
    (re.compile(r"-?[0-9]+(?![A-Za-z0-9_.])"), "NUMBR_LITERAL", "NUMBR Literal"),
    (re.compile(r"(WIN|FAIL)" + END_OF_WORD), "TROOF_LITERAL", "TROOF Literal"),
    (re.compile(r"(NOOB|NUMBR|NUMBAR|YARN|TROOF)" + END_OF_WORD), "TYPE_LITERAL", "Type Literal"),
]

IDENTIFIER_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


def match_pattern(patterns, line, pos):
    for pattern, token_type, classification in patterns:
        match = pattern.match(line, pos)
        if match:
            return match.group(), token_type, classification
    return None


def classify_identifier(tokens):
    # all three identifier kinds use the same regex, so we check the token before it
    previous = ""
    if len(tokens) > 0:
        previous = tokens[-1].type

    if previous == "HOW_IZ_I" or previous == "I_IZ":
        return "FUNCIDENT", "Function Identifier"
    if previous == "IM_IN_YR" or previous == "IM_OUTTA_YR":
        return "LOOPIDENT", "Loop Identifier"
    return "VARIDENT", "Variable Identifier"


def tokenize(source):
    tokens = []
    # splitlines also handles windows \r\n line endings
    for line_number, line in enumerate(source.splitlines(), start=1):
        tokenize_line(line, line_number, tokens)
    return tokens


def tokenize_line(line, line_number, tokens):
    pos = 0
    while pos < len(line):
        if line[pos].isspace():
            pos += 1
            continue

        col = pos + 1

        # keywords and literals before identifiers, so ITZ and WIN are never read as variables
        found = match_pattern(KEYWORD_PATTERNS, line, pos)
        if found is None:
            found = match_pattern(LITERAL_PATTERNS, line, pos)
        if found:
            text, token_type, classification = found
            tokens.append(Token(token_type, text, line_number, col, classification))
            pos += len(text)
            continue

        # + separates VISIBLE operands, ! at the end of VISIBLE skips the newline
        if line[pos] == "+":
            next_char = line[pos + 1:pos + 2]
            if next_char.isdigit() or next_char == ".":
                raise LexerError(f"Line {line_number}, col {col}: positive numbers can't have a + sign")
            tokens.append(Token("PLUS", "+", line_number, col, "Output Separator"))
            pos += 1
            continue
        if line[pos] == "!":
            tokens.append(Token("BANG", "!", line_number, col, "Newline Suppressor"))
            pos += 1
            continue

        match = IDENTIFIER_PATTERN.match(line, pos)
        if match:
            token_type, classification = classify_identifier(tokens)
            tokens.append(Token(token_type, match.group(), line_number, col, classification))
            pos += len(match.group())
            continue

        bad_text = line[pos:].split()[0]
        raise LexerError(f"Line {line_number}, col {col}: unrecognized lexeme '{bad_text}'")

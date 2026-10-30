#Binary operations
BINARY_OPS = ("SUM_OF", "DIFF_OF", "PRODUKT_OF", "QUOSHUNT_OF", "MOD_OF",
        "BIGGR_OF", "SMALLR_OF", "BOTH_OF", "EITHER_OF", "WON_OF",
        "BOTH_SAEM", "DIFFRINT")

class ParserError(Exception):
    pass


class Program:
    def __init__(self, functions, declarations, statements):
        self.functions = functions
        self.declarations = declarations
        self.statements = statements

# added the Node class to represent nodes in the parse tree, with a kind, value, and list of children
# kind: what it is, like "NUMBR_LITERAL".
# value: its text, like "x" or "5".
# children: a list of other nodes nested inside it.
class Node:
    def __init__(self, kind, value=None, children=None):
        self.kind = kind
        self.value = value
        self.children = children or []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # looks at a token without moving, returns None past the end
    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    # checks token type
    def at(self, *token_types):
        token = self.peek()
        return token is not None and token.type in token_types
        
    # takes the current token if it's the right type, otherwise stops with an error
    def expect(self, token_type, what):
        token = self.peek()
        if token is None or token.type != token_type:
            self.error(f"expected {what}, found {self.describe(token)}")
        return self.advance()

    def error(self, message):
        token = self.peek()
        if token is None and len(self.tokens) > 0:
            token = self.tokens[-1]  # past the end, so point at the last line
        line = token.line if token else 1
        raise ParserError(f"Line {line}: {message}")

    def describe(self, token):
        if token is None:
            return "end of file"
        if token.type == "NEWLINE":
            return "end of line"
        return f"'{token.lexeme}'"

    # <program> ::= <function_list> HAI <linebreak> <var_section> <statement_list> KTHXBYE <linebreak> <function_list>
    # for now only HAI and KTHXBYE, the other parts get added in the next steps
    def parse_program(self):
        self.expect("HAI", "HAI")
        self.expect("NEWLINE", "end of line after HAI")

        declarations = self.parse_variable()
        statements = self.parse_statement_list()
        
        self.expect("KTHXBYE", "KTHXBYE")
        self.expect("NEWLINE", "end of line after KTHXBYE")
        if self.peek() is not None:
            self.error(f"expected end of file after KTHXBYE, found {self.describe(self.peek())}")
        return Program([], declarations, statements)

    def parse_variable(self):
        declarations = []
        if not self.at("WAZZUP"):
            return declarations
            
        self.advance()
        self.expect("NEWLINE", "end of line after WAZZUP")
        
        while self.at("I_HAS_A"):
            declarations.append(self.parse_declaration())
            # if self.tokens[self.pos + 1]
            #     break 
        
        # self.expect("BUHBYE", "BUHBYE")
        # self.expect("NEWLINE", "NEWLINE")
        
        if not self.at("BUHBYE"):
            self.error(f"expected I HAS A or BUHBYE inside the variable section, found {self.describe(self.peek())}")
        
        self.advance()
        self.expect("NEWLINE", "end of line after BUHBYE")
        return declarations

    def parse_declaration(self):
        start = self.advance()
        name = self.expect("VARIDENT", "a variable name after I HAS A")
        children = []

        if self.at("ITZ"):
            self.advance()
            children.append(self.parse_expression())
        self.expect("NEWLINE", "end of line after the variable declaration")
        return Node("declaration", name.lexeme, children)
    
    def parse_expression(self):
        token = self.peek()

        if self.at(*BINARY_OPS):
            self.advance()
            left = self.parse_expression()
            self.expect("AN", "AN between the two operands")
            right = self.parse_expression()
            return Node(token.type, None, [left, right])

        if self.at("NUMBR_LITERAL", "NUMBAR_LITERAL", "TROOF_LITERAL", "TYPE_LITERAL", "VARIDENT"):
            self.advance()
            return Node(token.type, token.lexeme)
        if self.at("STRING_DELIM"):
            self.advance()
            text = self.expect("YARN_LITERAL", "text inside the quotes")
            self.expect("STRING_DELIM", "a closing quote")
            return Node("YARN_LITERAL", text.lexeme)
        self.error(f"expected a value, found {self.describe(token)}")

    def parse_statement_list(self):
        statements = []
        while self.peek() is not None and not self.at("KTHXBYE"):
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        if self.at("VISIBLE"):
            return self.parse_visible()
        if self.at("GIMMEH"):
            return self.parse_input()
        self.error(f"expected a statement, found {self.describe(self.peek())}")

    def parse_visible(self):
        self.advance()  # VISIBLE
        children = [self.parse_expression()]
        while self.at("PLUS"):
            self.advance()
            children.append(self.parse_expression())
        if self.at("BANG"):
            self.advance()
            children.append(Node("BANG", "!"))
        self.expect("NEWLINE", "end of line after VISIBLE")
        return Node("VISIBLE", None, children)

    def parse_input(self):
        self.advance()  # GIMMEH
        name = self.expect("VARIDENT", "a variable name after GIMMEH")
        self.expect("NEWLINE", "end of line after GIMMEH")
        return Node("GIMMEH", name.lexeme)

# prints the tree with two spaces of indent per level
def print_tree(node, indent=0):
    space = "  " * indent
    if isinstance(node, Program):
        print(space + "Program")
        print(space + "  functions:")
        for function in node.functions:
            print_tree(function, indent + 2)
        print(space + "  declarations:")
        for declaration in node.declarations:
            print_tree(declaration, indent + 2)
        print(space + "  statements:")
        for statement in node.statements:
            print_tree(statement, indent + 2)
    elif isinstance(node, Node):
        label = node.kind if node.value is None else f"{node.kind}: {node.value}"
        print(space + label)
        for child in node.children:
            print_tree(child, indent + 1)
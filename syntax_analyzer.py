class ParserError(Exception):
    pass


class Program:
    def __init__(self, functions, declarations, statements):
        self.functions = functions
        self.declarations = declarations
        self.statements = statements


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
        
        self.expect("KTHXBYE", "KTHXBYE")
        self.expect("NEWLINE", "end of line after KTHXBYE")
        if self.peek() is not None:
            self.error(f"expected end of file after KTHXBYE, found {self.describe(self.peek())}")
        return Program([], [], [])

    def parse_variable(self):
        declarations = []
        if not self.at("WAZZUP"):
            return declarations
            
        self.advance()
        self.expect("NEWLINE", "end of line after WAZZUP")
        
        while self.expect("I_HAS_A")
            declarations.append(self.parse_declaration())
        
        if not self.at("BUHBYE"):
            self.error(f"expected I HAS A or BUHBYE inside the variable section, found {self.describe(self.peek())}")
        
        self.advance()
        self.expect("NEWLINE", "end of line after BUHBYE")
        if self.peek() is not None:
            self.error(f"expected end of file after KTHXBYE, found {self.describe(self.peek())}")

    def parse_declaration(self):
        start = self.advance()
        name = self.expect("VARIDENT", "a variable name after I HAS A")
        children = []

        if self.at("ITZ"):
            self.advance()
            children.append(self.parse_expression())
        self.expect("NEWLINE", "end of line after the variable declaration")


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

class SemanticError(Exception):
    pass

ARITHMETIC = ("SUM_OF", "DIFF_OF", "PRODUKT_OF", "QUOSHUNT_OF", "MOD_OF", "BIGGR_OF", "SMALLR_OF")

class SemanticAnalyzer:
    def __init__(self):
        self.variables = {"IT": None} #IT will be used as an implicit variable in some cases, so we will initialize it to None
        self.functions = {} #will be used to store function definitions

    def run(self, program):
        for declaration in program.declarations:
            self.declare(declaration)
        for statement in program.statements:
            self.execute(statement)

    def declare(self, node):
        value = None # no ITZ means it is NOOB
        if node.children:
            value = self.evaluate(node.children[0])
        self.variables[node.value] = value

    #this is for statements, it takes one node and looks at its kind and executes the appropriate action
    def execute(self, node):
        kind = node.kind
        if kind == "VISIBLE":
            parts = [self.evaluate(child) for child in node.children if child.kind != "BANG"]
            text = "".join(self.to_text(part) for part in parts)
            suppress_newline = any(child.kind == "BANG" for child in node.children)
            print(text, end="" if suppress_newline else "\n")
        elif kind == "GIMMEH":
            self.require_declared(node.value)
            self.variables[node.value] = input()
        elif kind == "R":
            self.require_declared(node.value)
            self.variables[node.value] = self.evaluate(node.children[0])
        elif kind == "expression":
            self.variables["IT"] = self.evaluate(node.children[0])
        else:
            raise SemanticError(f"{kind} is not supported yet")

    #this is for expressions
    #evaluate converts the literal's text into a value of the right type
    def evaluate(self, node):
        kind = node.kind
        if kind == "NUMBR_LITERAL":
            return int(node.value)
        if kind == "NUMBAR_LITERAL":
            return float(node.value)
        if kind == "YARN_LITERAL":
            return node.value
        if kind == "TROOF_LITERAL":
            return node.value == "WIN"
        if kind == "VARIDENT":
            self.require_declared(node.value)
            return self.variables[node.value]
        if kind in ARITHMETIC:
            return self.arithmetic(kind, self.evaluate(node.children[0]), self.evaluate(node.children[1]))
        raise SemanticError(f"{kind} is not supported yet")

    #does the actual math for the arithmetic operations, and also converts the operands to numbers if they are not already
    def arithmetic(self, kind, left, right):
        a, b = self.to_number(left), self.to_number(right)
        if kind == "SUM_OF":
            return a + b
        if kind == "DIFF_OF":
            return a - b
        if kind == "PRODUKT_OF":
            return a * b
        if kind == "BIGGR_OF":
            return max(a, b)
        if kind == "SMALLR_OF":
            return min(a, b)
        if b == 0:
            raise SemanticError("division by zero")
        if kind == "QUOSHUNT_OF":
            return a / b if isinstance(a, float) or isinstance(b, float) else int(a / b)
        return a % b  # MOD_OF

    #helper functions
    #this requires that a variable has been declared before it is used, otherwise it raises a SemanticError
    def require_declared(self, name):
        if name not in self.variables:
            raise SemanticError(f"variable '{name}' is used before it is declared")

    #make sures that values used in arithmetic are actual numbers
    def to_number(self, value):
        if isinstance(value, bool):
            return 1 if value else 0
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            try:
                return float(value) if "." in value else int(value)
            except ValueError:
                pass
        raise SemanticError(f"cannot treat {self.to_text(value)!r} as a number")

    #used by VISIBLE to convert values to strings for printing
    def to_text(self, value):
        if value is None:
            return "NOOB"
        if isinstance(value, bool):
            return "WIN" if value else "FAIL"
        return str(value)
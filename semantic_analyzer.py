class SemanticError(Exception):
    pass

ARITHMETIC = ("SUM_OF", "DIFF_OF", "PRODUKT_OF", "QUOSHUNT_OF", "MOD_OF", "BIGGR_OF", "SMALLR_OF")

class SemanticAnalyzer:
    # the gui can pass its own functions here instead of print and input
    def __init__(self, output=print, read_input=input):
        self.variables = {"IT": None} #IT will be used as an implicit variable in some cases, so we will initialize it to None
        self.functions = {} #will be used to store function definitions
        self.output = output
        self.read_input = read_input

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
            self.output(text, end="" if suppress_newline else "\n")
        elif kind == "GIMMEH":
            self.require_declared(node.value)
            self.variables[node.value] = self.read_input()
        elif kind == "R":
            self.require_declared(node.value)
            self.variables[node.value] = self.evaluate(node.children[0])
        elif kind == "IS_NOW_A":
            self.require_declared(node.value)
            self.variables[node.value] = self.cast(self.variables[node.value], node.children[0].value)
        elif kind == "expression":
            self.variables["IT"] = self.evaluate(node.children[0])
        elif kind == "O_RLY":
            self.run_if(node)
        else:
            raise SemanticError(f"{kind} is not supported yet")

    def run_block(self, statements):
        for statement in statements:
            self.execute(statement)

    # YA RLY runs if IT is WIN, otherwise the first MEBBE that is WIN runs, otherwise NO WAI
    def run_if(self, node):
        if self.to_troof(self.variables["IT"]):
            self.run_block(node.children[0].children)
            return
        for clause in node.children[1:]:
            if clause.kind == "NO_WAI":
                self.run_block(clause.children)
                return
            # the first child of MEBBE is its condition
            if self.to_troof(self.evaluate(clause.children[0])):
                self.run_block(clause.children[1:])
                return

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
        if kind == "MAEK":
            return self.cast(self.evaluate(node.children[0]), node.children[1].value)
        if kind == "BOTH_SAEM":
            return self.is_same(self.evaluate(node.children[0]), self.evaluate(node.children[1]))
        if kind == "DIFFRINT":
            return not self.is_same(self.evaluate(node.children[0]), self.evaluate(node.children[1]))
        if kind in ("NOT", "BOTH_OF", "EITHER_OF", "WON_OF", "ALL_OF", "ANY_OF"):
            return self.boolean(kind, [self.to_troof(self.evaluate(child)) for child in node.children])
        if kind == "SMOOSH":
            values = [self.evaluate(child) for child in node.children]
            # this cast is implicit, and a NOOB can only be implicitly cast to a TROOF
            if None in values:
                raise SemanticError("cannot use a NOOB value in SMOOSH")
            return "".join(self.to_text(value) for value in values)
        raise SemanticError(f"{kind} is not supported yet")

    #does the actual math for the arithmetic operations, and also converts the operands to numbers if they are not already
    def arithmetic(self, kind, left, right):
        a, b = self.to_number(left), self.to_number(right)
        # if one operand is a NUMBAR, the result has to be a NUMBAR
        if isinstance(a, float) or isinstance(b, float):
            a, b = float(a), float(b)
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

    # values is a list of TROOFs, with 1 value for NOT and 2 for BOTH OF, EITHER OF and WON OF
    def boolean(self, kind, values):
        if kind == "NOT":
            return not values[0]
        if kind == "WON_OF":
            return values[0] != values[1]
        if kind in ("BOTH_OF", "ALL_OF"):
            return all(values)
        return any(values)  # EITHER_OF and ANY_OF

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
        # only digits, hyphens and periods count, python's int() would also allow things like "1_000"
        if isinstance(value, str) and all(char in "0123456789-." for char in value):
            try:
                return float(value) if "." in value else int(value)
            except ValueError:
                pass
        raise SemanticError(f"cannot treat {self.to_text(value)!r} as a number")

    # comparisons don't typecast, the bool check is needed because python says 1 == True
    def is_same(self, left, right):
        if isinstance(left, bool) != isinstance(right, bool):
            return False
        return left == right

    # used by MAEK and IS NOW A, only these explicit casts can turn a NOOB into another type
    def cast(self, value, type_name):
        if type_name == "NOOB":
            return None
        if value is None:
            return {"NUMBR": 0, "NUMBAR": 0.0, "YARN": "", "TROOF": False}[type_name]
        if type_name == "TROOF":
            return self.to_troof(value)
        if type_name == "YARN":
            return self.to_text(value)
        if type_name == "NUMBR":
            return int(self.to_number(value))
        return float(self.to_number(value))

    # NOOB, "" and zero are FAIL, everything else is WIN, this is the same as python's bool()
    def to_troof(self, value):
        return bool(value)

    #used by VISIBLE to convert values to strings for printing
    def to_text(self, value):
        if value is None:
            return "NOOB"
        if isinstance(value, bool):
            return "WIN" if value else "FAIL"
        # keeps 2 decimals without rounding, going through 10 decimals first removes float noise
        if isinstance(value, float):
            return f"{value:.10f}"[:-8]
        return str(value)
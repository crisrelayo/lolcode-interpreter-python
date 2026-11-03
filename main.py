from lexer import tokenize, gui_tokens, parser_tokens, LexerError
from syntax_analyzer import Parser, ParserError, print_tree

# add new test files here
TEST_FILES = [
    "01_variables.lol",
    "02_gimmeh.lol",
    "03_arith.lol",
    "04_smoosh_assign.lol",
    "05_bool.lol",
    "06_comparison.lol",
    "07_ifelse.lol",
    "08_switch.lol",
    "09_loops.lol",
    "10_functions.lol",
]


def main():
    number = int(input("Test file number: "))

    with open("test_cases/" + TEST_FILES[number - 1], encoding="utf-8") as file:
        source = file.read()

    try:
        tokens = tokenize(source)
    except LexerError as error:
        print(error)
        return

    # print(f"{'Line':<6}{'Lexeme':<24}Classification")
    # for token in gui_tokens(tokens):
    #     print(f"{token.line:<6}{token.lexeme:<24}{token.classification}")
    # print()

    try:
        program = Parser(parser_tokens(tokens)).parse_program()
    except ParserError as error:
        print(error)
        return

    print_tree(program)


if __name__ == "__main__":
    main()

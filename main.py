from lexer import tokenize, gui_tokens, parser_tokens, LexerError
from syntax_analyzer import Parser, ParserError, print_tree

# change this to run a different test file
FILE_PATH = "test_cases/01_variables.lol"


def main():
    with open(FILE_PATH, encoding="utf-8") as file:
        source = file.read()

    try:
        tokens = tokenize(source)
    except LexerError as error:
        print(error)
        return

    print(f"{'Line':<6}{'Lexeme':<24}Classification")
    for token in gui_tokens(tokens):
        print(f"{token.line:<6}{token.lexeme:<24}{token.classification}")
    print()

    try:
        program = Parser(parser_tokens(tokens)).parse_program()
    except ParserError as error:
        print(error)
        return

    print_tree(program)


if __name__ == "__main__":
    main()

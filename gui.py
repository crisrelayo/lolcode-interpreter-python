import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from lexer import LexerError, gui_tokens, parser_tokens, tokenize
from semantic_analyzer import SemanticAnalyzer, SemanticError
from syntax_analyzer import Parser, ParserError

class LOLCodeGUI:
    """Build the six required GUI sections and connect them to the interpreter."""

    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter")
        self.root.geometry("1200x760")
        self.root.minsize(850, 550)
        self.current_file = None  # Tracks the file selected using the Open button.

def main():
    root = tk.Tk()
    LOLCodeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from lexer import LexerError, gui_tokens, parser_tokens, tokenize
from semantic_analyzer import SemanticAnalyzer, SemanticError
from syntax_analyzer import Parser, ParserError

class LOLCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter")
        self.root.geometry("1200x760")
        self.root.minsize(850, 550)
        self.current_file = None  # Tracks the file selected using the Open button.

        self._build_layout()

        def _build_layout(self):
            outer = ttk.Frame(self.root, padding=10)
            outer.pack(fill="both", expand=True)

            # TOP BAR: FILE EXPLORER ENTRY POINT
            toolbar = ttk.Frame(outer)
            toolbar.pack(fill="x", pady=(0, 8))
            ttk.Button(toolbar, text="Open .lol File", command=self.open_file).pack(side="left")
            ttk.Button(toolbar, text="Save", command=self.save_file).pack(side="left", padx=(6, 0))
            ttk.Button(toolbar, text="Save As", command=self.save_as_file).pack(side="left", padx=(6, 0))
            self.file_label = ttk.Label(toolbar, text="No file selected")
            self.file_label.pack(side="left", padx=12)

            # UPPER AREA: EDITOR AND TABLES
            upper = ttk.Panedwindow(outer, orient="horizontal")
            upper.pack(fill="both", expand=True)
            editor_panel = ttk.LabelFrame(upper, text="LOLCODE Text Editor", padding=6)
            tables_panel = ttk.Frame(upper)
            upper.add(editor_panel, weight=3)
            upper.add(tables_panel, weight=2)


def main():
    root = tk.Tk()
    LOLCodeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
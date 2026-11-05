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
        editor_panel = ttk.LabelFrame(upper, text="LOLCODE Text Editor", padding=6)
        tables_panel = ttk.Frame(upper)
        upper.add(editor_panel, weight=3)
        upper.add(tables_panel, weight=2)

        self.editor = tk.Text(
            editor_panel,
            wrap="none",
            font=("Consolas", 11),
            undo=True
        )
        editor_y = ttk.Scrollbar(editor_panel, orient="vertical", command=self.editor.yview)
        editor_x = ttk.Scrollbar(editor_panel, orient="horizontal", command=self.editor.xview)
        self.editor.configure(yscrollcommand=editor_y.set, xscrollcommand=editor_x.set)
        # packed before the editor so a small window can't push them out
        editor_y.pack(side="right", fill="y")
        editor_x.pack(side="bottom", fill="x")
        self.editor.pack(side="left", fill="both", expand=True)

        tables_panel.rowconfigure(0, weight=1)
        tables_panel.rowconfigure(1, weight=1)
        tables_panel.columnconfigure(0, weight=1)
        tokens_frame = ttk.LabelFrame(tables_panel, text="List of Tokens", padding=5)
        tokens_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        self.token_table = self._make_table(
            tokens_frame, ("lexeme", "classification"), ("Lexeme", "Classification")
        )

        # SYMBOL TABLE: IDENTIFIERS AND VALUES
        symbols_frame = ttk.LabelFrame(tables_panel, text="Symbol Table", padding=5)
        symbols_frame.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        self.symbol_table = self._make_table(
            symbols_frame, ("identifier", "value"), ("Identifier", "Value")
        )

        console_frame = ttk.LabelFrame(outer, text="Console (Input / Output)", padding=6)
        console_frame.pack(side="bottom", fill="x")
        console_frame.configure(height=180)
        console_frame.pack_propagate(False)
        self.console = tk.Text(
            console_frame, height=9, wrap="word", state="disabled", font=("Consolas", 10)
        )
        self.console.pack(side="left", fill="both", expand=True)
        console_y = ttk.Scrollbar(console_frame, orient="vertical", command=self.console.yview)
        console_y.pack(side="right", fill="y")
        self.console.configure(yscrollcommand=console_y.set)

        ttk.Button(outer, text="EXECUTE / RUN", command=self.execute).pack(
            side="bottom", fill="x", pady=(8, 8)
        )

        # packed last so it only gets the leftover space, this keeps execute and the console visible
        upper.pack(fill="both", expand=True)

    @staticmethod
    def _make_table(parent, columns, headings):
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        table = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for column, heading in zip(columns, headings):
            table.heading(column, text=heading)
            table.column(column, width=145, minwidth=80, stretch=True)
        table.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        table.configure(yscrollcommand=scrollbar.set)
        return table

    def open_file(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Open LOLCODE file",
            filetypes=[("LOLCODE files", "*.lol"), ("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return  # The user canceled file selection.
        # edit_modified is true if the text changed since the last open or save
        if self.editor.edit_modified():
            message = "You have unsaved changes. Open this file anyway?"
            if not messagebox.askyesno("Unsaved Changes", message, parent=self.root):
                return
        try:
            source = Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            messagebox.showerror("Open Failed", str(error), parent=self.root)
            return
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", source)
        self.editor.edit_reset()  # so undo can't go back to before the file was opened
        self.editor.edit_modified(False)
        self.current_file = Path(path)
        self.file_label.configure(text=self.current_file.name)

    def save_file(self):
        if self.current_file is None:
            return self.save_as_file()
        try:
            self.current_file.write_text(self.editor.get("1.0", "end-1c"), encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Save Failed", str(error), parent=self.root)
            return False
        self.editor.edit_modified(False)
        return True

    def save_as_file(self):
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save LOLCODE file",
            defaultextension=".lol",
            filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")],
        )
        if not path:
            return False
        old_file = self.current_file
        self.current_file = Path(path)
        if not self.save_file():
            self.current_file = old_file
            return False
        self.file_label.configure(text=self.current_file.name)
        return True

    @staticmethod
    def _clear_table(table):
        for item in table.get_children():
            table.delete(item)

    def _write_console(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")
        self.root.update_idletasks()

    def _output(self, *values, sep=" ", end="\n"):
        self._display_symbols()
        self._write_console(sep.join(str(value) for value in values) + end)

    def _read_input(self):
        self._display_symbols()
        answer = simpledialog.askstring("GIMMEH Input", "Enter a value:", parent=self.root)
        if answer is None:
            raise SemanticError("Input canceled during GIMMEH")
        self._write_console(f"> {answer}\n")
        return answer

    def _display_tokens(self, tokens):
        for token in gui_tokens(tokens):
            self.token_table.insert("", "end", values=(token.lexeme, token.classification))

    # called before each VISIBLE and GIMMEH and at the end of the run, so the values stay current
    def _display_symbols(self):
        self._clear_table(self.symbol_table)
        for identifier, value in self.analyzer.variables.items():
            self.symbol_table.insert(
                "", "end", values=(identifier, self.analyzer.to_text(value))
            )

    def execute(self):
        source = self.editor.get("1.0", "end-1c")
        self._clear_table(self.token_table)
        self._clear_table(self.symbol_table)
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

        if not source.strip():
            self._write_console("No LOLCODE source to execute.\n")
            return

        try:
            tokens = tokenize(source)
            self._display_tokens(tokens)
            program = Parser(parser_tokens(tokens)).parse_program()
        except (LexerError, ParserError) as error:
            self._write_console(f"{type(error).__name__}: {error}\n")
            return

        self.analyzer = SemanticAnalyzer(output=self._output, read_input=self._read_input)
        try:
            self.analyzer.run(program)
        except SemanticError as error:
            self._write_console(f"SemanticError: {error}\n")
        except (ArithmeticError, ValueError, TypeError) as error:
            # Defensive handling for Python errors in the interpreter's operations.
            self._write_console(f"Runtime error: {error}\n")
        finally:
            self._display_symbols()

def main():
    root = tk.Tk()
    LOLCodeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

#from lexer import LexerError, gui_tokens, parser_tokens, tokenize
#from semantic_analyzer import SemanticAnalyzer, SemanticError
#from syntax_analyzer import Parser, ParserError

class LOLCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter")
        self.root.geometry("1200x760")
        self.root.minsize(850, 550)
        self.current_file = None  # Tracks the file selected using the Open button.

        self._build_layout()

        print("Available methods:", dir(self))
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

        self.editor = tk.Text(editor_panel, wrap="none", font=("Consolas", 11))
        self.editor.pack(fill="both", expand=True)

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
        try:
            source = Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            messagebox.showerror("Open Failed", str(error), parent=self.root)
            return
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", source)
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

def main():
    root = tk.Tk()
    LOLCodeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
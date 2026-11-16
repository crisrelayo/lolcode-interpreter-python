# LOL Code Interpreter in Python

Meru, Omamalin, Regala, Relayo  
CMSC 124, ST-2L

Lexer, parser and interpreter for LOLCODE with a Tkinter GUI. 

## Requirements

Python 3.8+ with Tkinter. Check with `python3 -m tkinter`.

- **Windows / macOS:** the python.org installer includes Tkinter.
- **Debian / Ubuntu:** `sudo apt install python3 python3-tk`
- **macOS (Homebrew):** `brew install python-tk`

On Windows, use `py` instead of `python3`.

## Run

For GUI run, navigate to the project folder and enter:

```
python3 gui.py
```

Open a `.lol` file, edit if needed, and press **EXECUTE / RUN**. `GIMMEH` prompts through a dialog box.

For a console run, enter:

```
python3 main.py
```

This automatically uses files in `test_cases/`. Enter the file number of choice.

## Files

- `lexer.py`: lexical analyzer
- `syntax_analyzer.py`: parser (builds the parse tree)
- `semantic_analyzer.py`: semantic checks and execution
- `gui.py`: GUI
- `main.py`: console test runner
- `test_cases/`: sample programs

## Reference Repos

https://github.com/coleenagsao/python-lolcode-interpreter
https://github.com/sh1roee/LOLCode-Interpreter
from ternaryengine.tryte import *
import logging
from TokenBuffer import TokenBuffer, Token
import os, readline, atexit
from replmodule.Ast import AST
from replmodule.read import READ
from replmodule.eval import EVAL

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# Set registers to ternary zero
registers = [tZ for num in range(-13, 13)]


def print_value(value: str) -> str:
    return f'{value} = {tryteToInt(value)}'


def PRINT(ast: AST) -> str:
    result = str(ast)
    if ast.type == 'value':
        result = print_value(ast.data)
    if ast.type == 'string':
        result = ast.data
    if ast.type == 'list':
        result = '\n'.join(PRINT(item) for item in ast.children)
    if ast.type == 'error':
        result = f'ERROR: {ast.data}'
    return result

def rep(buffer: TokenBuffer) -> str:
    global registers
    return PRINT(EVAL(READ(buffer), registers))
    

if __name__ == "__main__":
    atexit.register(readline.write_history_file, "history.txt")

    patterns = {
        'INTEGER': r'-?[0-9]+',
        'REGISTER': r'[rR][nzpNZP]+',
        'OPEN_PAREN': r'\(',
        'CLOSE_PAREN': r'\)',
        'IDENTIFIER': r'\w+|[\<\+\*]+'
    }

    buffer = TokenBuffer()
    buffer.init_patterns(patterns)
    buffer.config(skip_white_space = True)

    try:
        readline.read_history_file("history.txt")
        readline.set_history_length(100)
        while True:
            in_str = input("\nrepl-> ")
            buffer.add_lines('user input', [in_str])
            buffer.tokenize()
            
            while not buffer.out_of_tokens():
                print(rep(buffer))
    
    except FileNotFoundError:
        print("Line history will be saved in history.txt.")
    except EOFError:
        print("\nExiting.")
        exit(0)

from ternaryengine.tryte import *
import logging
from TokenBuffer import TokenBuffer, Token
import os, readline, atexit
from dataclasses import dataclass
from typing import List, Any

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# Set registers to ternary zero
registers = [tZ for num in range(-13, 13)]

@dataclass
class AST:
    type: str = 'nil'
    data: str = ''
    children = []


def read_list(end_type: str, buffer: TokenBuffer) -> List:
    result = []
    while not buffer.out_of_tokens() and buffer.peek().type != end_type:
        result.append(READ(buffer))
    return result


def READ(buffer: TokenBuffer) -> AST:
    result = AST()
    if not buffer.out_of_tokens():
        peek = buffer.peek()
        logger.debug(f'parsing: "{peek.type} = {peek.value}"')
        match peek.type:
            case 'OPEN_PAREN':
                logger.debug('matched list')
                result.type = 'list'
                buffer.consume()
                result.children = read_list('CLOSE_PAREN', buffer)
                if not buffer.expect_type('CLOSE_PAREN'):
                    result.type = 'error'
                    result.data = 'Unbalanced parentheses.'
            case 'TERNARY':
                logger.debug('matched ternary value')
                result.type = 'value'
                result.data = peek.value
            case 'REGISTER':
                logger.debug('matched register')
                result.type = 'register'
                result.data = peek.value[1:]
            case 'INTEGER':
                logger.debug('matched decimal value')
                result.type = 'value'
                result.data = intToTryte(int(peek.value))
            case 'IDENTIFIER':
                logger.debug('matched identifier')
                result.type = 'ident'
                result.data = peek.value
            case _:
                logger.debug('did not match input')
                result.type = 'error'
                result.data = 'Unable to parse input'
        buffer.consume()    
    return result

def EVAL(ast: AST) -> AST:
    return ast

def PRINT(ast: AST) -> str:
    result = str(ast)
    if ast.type == 'value':
        result = f'{ast.data} = {tryteToInt(ast.data)}'
    if ast.type == 'error':
        result = f'ERROR: {ast.data}'
    return result

def rep(buffer: TokenBuffer) -> str:
    return PRINT(EVAL(READ(buffer)))
    

if __name__ == "__main__":
    atexit.register(readline.write_history_file, "history.txt")

    patterns = {
        'TERNARY': r'[nzpNZP]+',
        'INTEGER': r'-?[0-9]+',
        'REGISTER': r'[rR][nzpNZP]+',
        'OPEN_PAREN': r'\(',
        'CLOSE_PAREN': r'\)',
        'IDENTIFIER': r'\w+'
    }

    buffer = TokenBuffer()
    buffer.init_patterns(patterns)
    buffer.config(skip_white_space = True)

    try:
        readline.read_history_file("history.txt")
        readline.set_history_length(100)
        while True:
            in_str = input("user> ")
            buffer.add_lines('user input', [in_str])
            buffer.tokenize()
            
            print(rep(buffer))
    
    except FileNotFoundError:
        print("Line history will be saved in history.txt.")
    except EOFError:
        print("\nExiting.")
        exit(0)

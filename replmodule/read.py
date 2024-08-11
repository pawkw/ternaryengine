import logging
from TokenBuffer import TokenBuffer
from typing import List, Any
from replmodule.Ast import AST
from ternaryengine.tryte import intToTryte

logger = logging.getLogger(__name__)


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
                logger.debug('\n\n')
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

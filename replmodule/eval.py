import logging
from TokenBuffer import TokenBuffer
from typing import List, Callable
from replmodule.Ast import AST
from ternaryengine.tryte import tryteToInt, trit_chars, trits_per_tryte
from replmodule.functions import get_function, get_function_list

logger = logging.getLogger(__name__)


def register_index(tryte: str) -> int:
    result = tryteToInt(tryte) + 13
    logger.debug(f'register index: {result}')
    return result


bct_bits = ['10', '00', '01']
def EVAL(ast: AST, register_file: List) -> AST:
    if ast.type == 'value' or ast.type == 'error' or ast.type == 'string':
        logger.debug(f'returning {ast.type} {ast.data}')
        return ast
    
    if ast.type == 'register':
        return AST(type='value', data=register_file[register_index(ast.data)])
    
    if ast.type == 'function':
        old = ast
        ast = AST(type='list', data='')
        ast.children = [old]
    
    if ast.type == 'list':
        if ast.children[0].type == 'error':
            return ast.children[0]
        func_name = ast.children[0].data
        param_list = ast.children[1:]

        if func_name == 'help' or func_name == 'list':
            result = AST(type='string', data='Available functions: ')
            result.data += ', '.join([x for x in get_function_list()])
            return result

        if func_name == 'set':
            if len(param_list) != 2:
                return AST(type='error', data=f'Requires two parameters: {param_list}.')
            value = EVAL(param_list[1], register_file)
            if value.type == 'error':
                return value
            register_file[register_index(param_list[0].data)] = value.data
            return value
        
        if func_name == 'bct':
            result = ''
            for count, trit in enumerate(param_list[0].data):
                result += bct_bits[trit_chars.index(trit)]
                if (count+1)%3 == 0:
                    result += '-'
            if trits_per_tryte%3 == 0:
                result = result[:-1]
            ast = AST(type='string', data=result)
            return ast
        
        func, param_len = get_function(func_name)
        if len(param_list) != param_len:
                return AST(type='error', data=f'Requires {param_len} parameters: {param_list}.')
        
        logger.debug(f'using function: {func}')
        if func == 'error':
            return AST(type='error', data=f'Could not find function {func_name}')
        
        data = []
        for param in param_list:
            result = EVAL(param, register_file)
            logger.debug(f'using parameter: {result}')
            if result.type == 'error':
                return result
            data.append(result.data)
        return AST(type='value', data=func(*data))



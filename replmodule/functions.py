import logging
from typing import List, Callable
from ternaryengine.tryte import *
from replmodule.Ast import AST


function_dict = {
    'sign': (pSign, 1),
    'ispos': (tIsPos, 1),
    'clampdown': (tClampDown, 1),
    'iszero': (tIsZero, 1),
    'invertmask': (tInvertMask, 1),
    'notneg': (tNotNeg, 1),
    'clampup': (tClampUp, 1),
    'inc': (tInc, 1),
    'isneg': (tIsNeg, 1),
    'dec': (tDec, 1),
    'notzero': (tNotZero, 1),
    'notpos': (tNotPos, 1),
    'min': (tMin, 2),
    'max': (tMax, 2),
    'antimax': (tAntimax, 2),
    'antimin': (tAntimin, 2),
    'sum': (tSum, 2),
    'xor': (tXor, 2),
    'xnor': (tXnor, 2),
    'mask': (tMask, 2),
    'consensus': (tConsensus, 2),
    'any': (tAny, 2),
    'same': (tSame, 2),
    'equal': (tEqual, 2),
    'diff': (tDiff, 2),
    'mul': (tMul, 2),
    'compare': (tCompare, 2),
    '<<': (lambda tright, amount: tShiftLeft(tright, tryteToInt(amount)), 2),
    '>>': (lambda tright, amount: tShiftRight(tright, tryteToInt(amount)), 2),
    'negate': (tNegate, 1),
    '+': (tAdd, 2),
    '*': (tMultiply, 2),
}

logger = logging.getLogger(__name__)

def get_function_list() -> List:
    return function_dict.keys()


def get_function(name: str) -> Callable:
    if name in function_dict.keys():
        result = function_dict[name]
        logger.debug(f'returning {result}')
        return result
    return 'error', 0
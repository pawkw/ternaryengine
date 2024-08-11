import logging
from typing import List, Callable
from ternaryengine.tryte import *

function_dict = {
    'sign': tSign,
    'min': tMin,
    'max': tMax,
    'antimax': tAntimax,
    'antimin': tAntimin,
    'sum': tSum,
    'xor': tXor,
    'consensus': tConsensus,
    'any': tAny,
    'same': tSame,
    'equal': tEqual,
    'diff': tDiff,
    'mul': tMul,
    'compare': tCompare,
    '<<': lambda tright, amount: tShiftLeft(tright, tryteToInt(amount)),
    'negate': tNegate,
    '+': tAdd,
    '*': tMultiply,
}

logger = logging.getLogger(__name__)

def funcShiftLeft(tryte: str, amount: str) -> Callable:
    int_amount = tryteToInt(amount)
    return tShiftLeft(tryte, int_amount)


def get_function_list() -> List:
    return function_dict.keys()


def get_function(name: str) -> Callable:
    if name in function_dict.keys():
        return function_dict[name]
    return 'error'
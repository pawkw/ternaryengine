from ternaryengine.defs import *
from typing import Callable, Any
from functools import partial
import ternaryengine.monadic as monadic
import ternaryengine.diadic as diadic
import logging

logger = logging.getLogger(__name__)

##### Decorators

def makeTryte(func: Callable[..., Any]) -> Callable[..., Any]:
    def convertToTryte(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        if len(result) > trits_per_tryte:
            logger.warn(f'Tryte overflow produced by {func.__name__}: {result}.')
        return (tZ*trits_per_tryte + result)[-trits_per_tryte:]
    return convertToTryte


def makeTrit(func: Callable[..., Any]) -> Callable[..., Any]:
    def checkTrit(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        if len(result) != 1:
            logger.warn(f'Bad trit produced by {func.__name__}: {result}')
        return result[-1]
    return checkTrit


##### Helpers

def strip(tryte: str) -> str:
    logger.debug(f'tryte {tryte}')
    return tryte.lstrip(tZ)


@makeTryte
def pad(tryte: str) -> str:
    logger.debug(f'tryte {tryte}')
    return tryte


@makeTryte
def __apply_unary_to_tryte(operation: str, tryte: str) -> str:
    logger.debug(f'operation {operation} tryte {tryte}')
    function = partial(monadic.apply_operator, operation)
    return ''.join(list(map(function, tryte)))


@makeTryte
def __apply_to_tryte(operation: str, tryte1: str, tryte2: str) -> str:
    logger.debug(f'operation {operation} tryte1 {tryte1} tryte2 {tryte2}')
    function = partial(diadic.apply_operator, operation)
    return ''.join(list(map(function, tryte1, tryte2)))


@makeTrit
def __apply_to_trit(operation: str, trit) -> str:
    logger.debug(f'operation {operation} trit {trit}')
    return monadic.apply_operator(operation, trit)


@makeTrit
def __apply_to_trit(operation: str, trit1: str, trit2: str) -> str:
    logger.debug(f'operation {operation} trit1 {trit1} trit2 {trit2}')
    return diadic.apply_operator(operation, trit1, trit2)

##### Tritwise operators

def tritSum(trit1: str, trit2: str) -> str:
    return __apply_to_trit('sum', trit1, trit2)


def tritConsensus(trit1: str, trit2: str) -> str:
    return __apply_to_trit('consensus', trit1, trit2)


def tritMul(trit1: str, trit2: str) -> str:
    return __apply_to_trit('mul', trit1, trit2)
    


##### Tryte predicates

@makeTrit
def tSign(tryte: str) -> str:
    tryte = strip(tryte)
    if len(tryte) == 0:
        return tZ
    return tryte[0]


def tIsZero(tryte: str) -> bool:
    return tSign(tryte) == tZ


def tIsNeg(tryte: str) -> bool:
    return tSign(tryte) == tN


def tIsPos(tryte: str) -> bool:
    return tSign(tryte) == tP


##### Tryte Operators

@makeTryte
def tMin(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('min', tryte1, tryte2)


@makeTryte
def tMax(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('max', tryte1, tryte2)


@makeTryte
def tAntimin(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('antimin', tryte1, tryte2)


@makeTryte
def tAntimax(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('min', tryte1, tryte2)


@makeTryte
def tSum(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('sum', tryte1, tryte2)


@makeTryte
def tXor(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('xor', tryte1, tryte2)


@makeTryte
def tConsensus(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('consensus', tryte1, tryte2)


@makeTryte
def tAny(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('any', tryte1, tryte2)


@makeTryte
def tSame(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('same', tryte1, tryte2)


@makeTryte
def tEqual(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('equal', tryte1, tryte2)


@makeTryte
def tDiff(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('diff', tryte1, tryte2)


@makeTryte
def tMul(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('mul', tryte1, tryte2)


@makeTryte
def tCompare(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('compare', tryte1, tryte2)


@makeTryte
def tShiftLeft(tryte: str, amount: int) -> str:
    return (tryte+tZ*amount)[-trits_per_tryte:]


@makeTryte
def tNegate(tryte: str) -> str:
    return __apply_unary_to_tryte('negate', tryte)


@makeTryte
def tAdd(tryte1: str, tryte2: str) -> str:
    if tIsZero(tryte1):
        return tryte2
    if tIsZero(tryte2):
        return tryte1
    
    tryte1 = pad(tryte1)
    tryte2 = pad(tryte2)
    sum = __apply_to_tryte('sum', tryte1, tryte2)
    carry = tShiftLeft(__apply_to_tryte('consensus', tryte1, tryte2), 1)
    acc = __apply_to_tryte('sum', sum, carry)
    logger.debug(f'adding {tryte1} and {tryte2} = {acc}.')
    logger.debug(f'sum: {sum} carry: {carry}')
    return acc


@makeTryte
def tMultiply(tryte1: str, tryte2: str) -> str:
    if tIsZero(tryte1) or tIsZero(tryte2):
        return tZ
    
    mul1 = strip(tryte1)
    mul2 = strip(tryte2)

    if len(tryte2) > len(tryte1):
        mul1 = tryte2
        mul2 = tryte1

    result_list = []
    mul2 = mul2[::-1]
    for trit in mul2:
        if trit == tZ:
            continue
        result = ''.join([tritMul(trit, t2) for t2 in mul1])
        result_list.append(result)
        mul1 = tShiftLeft(mul1, 1)
    
    result = tZ
    for tryte in result_list:
        result = tAdd(result, tryte)
    
    return result


##### Conversions

def tryteToInt(tryte: str) -> int:
    acc = 0
    exponent = 1
    logger.debug(f'tryte: {tryte}')
    tryte = tryte[::-1]
    logger.debug(f'reverse tryte: {tryte}')
    for trit in tryte:
        value = trit_chars.index(trit) -1
        acc += value * exponent
        logger.debug(f'trit: {trit} value: {value} exponent: {exponent} accumulated: {acc}')
        exponent *= 3
    return acc


@makeTryte
def intToTryte(number: int) -> str:
    negative = False
    if number < 0:
        negative = True
        number *= -1
    
    exponent = tP
    result = tZ
    while number > 0:
        current = decimal_index[number % 10]
        value = tMultiply(current, exponent)
        result = tAdd(result, value)
        exponent = tAdd(tShiftLeft(exponent, 2), exponent)
        number = number // 10
        logger.debug(f'current: {current} value: {value} exponent: {exponent}')

    if negative:
        result = tNegate(result)

    return result
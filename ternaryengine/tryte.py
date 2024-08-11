from ternaryengine.defs import *
from typing import Callable, Any
from functools import partial
import ternaryengine.monadic as monadic
import ternaryengine.diadic as diadic
import logging

logger = logging.getLogger(__name__)
log_depth = 0
indent = '  '

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
    # logger.debug(f'tryte {tryte}')
    return tryte.lstrip(tZ)


@makeTryte
def pad(tryte: str) -> str:
    # logger.debug(f'tryte {tryte}')
    return tryte


@makeTryte
def __apply_unary_to_tryte(operation: str, tryte: str) -> str:
    tryte = pad(tryte)
    logger.debug(f'operation {operation} tryte {tryte}')
    function = partial(monadic.apply_operator, operation)
    return ''.join(list(map(function, tryte)))


@makeTryte
def __apply_to_tryte(operation: str, tryte1: str, tryte2: str) -> str:
    tryte1 = pad(tryte1)
    tryte2 = pad(tryte2)
    logger.debug(f'operation {operation} tryte1 {tryte1} tryte2 {tryte2}')
    function = partial(diadic.apply_operator, operation)
    return ''.join(list(map(function, tryte1, tryte2)))


@makeTrit
def __apply_to_trit(operation: str, trit) -> str:
    # logger.debug(f'operation {operation} trit {trit}')
    return monadic.apply_operator(operation, trit)


@makeTrit
def __apply_to_trit(operation: str, trit1: str, trit2: str) -> str:
    # logger.debug(f'operation {operation} trit1 {trit1} trit2 {trit2}')
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
def pSign(tryte: str) -> str:
    tryte = strip(tryte)
    if len(tryte) == 0:
        return tZ
    return tryte[0]


def pIsZero(tryte: str) -> bool:
    return pSign(tryte) == tZ


def pIsNeg(tryte: str) -> bool:
    return pSign(tryte) == tN


def pIsPos(tryte: str) -> bool:
    return pSign(tryte) == tP


##### Tryte Operators

@makeTryte
def tStrip(tryte: str) -> str:
    result = trits_per_tryte - len(strip(tryte))
    return intToTryte(result)


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
def tXnor(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('xnor', tryte1, tryte2)


@makeTryte
def tMask(tryte1: str, tryte2: str) -> str:
    return __apply_to_tryte('mask', tryte1, tryte2)


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
    global log_depth, indent
    logger.debug(f'{indent * log_depth}>>>>> shift left {tryte} {amount}')
    return (tryte+(tZ*amount))[-trits_per_tryte:]


@makeTryte
def tShiftRight(tryte: str, amount: int) -> str:
    global log_depth, indent
    logger.debug(f'{indent * log_depth}>>>>> shift left {tryte} {amount}')
    return ((tZ*amount)+tryte)[:trits_per_tryte]


@makeTryte
def tNegate(tryte: str) -> str:
    return __apply_unary_to_tryte('negate', tryte)


@makeTryte
def tIsPos(tryte: str) -> str:
    return __apply_unary_to_tryte('isPos', tryte)


@makeTryte
def tClampDown(tryte: str) -> str:
    return __apply_unary_to_tryte('clampDown', tryte)


@makeTryte
def tIsZero(tryte: str) -> str:
    return __apply_unary_to_tryte('isZero', tryte)


@makeTryte
def tInvertMask(tryte: str) -> str:
    return __apply_unary_to_tryte('invertMask', tryte)


@makeTryte
def tNotNeg(tryte: str) -> str:
    return __apply_unary_to_tryte('notNeg', tryte)


@makeTryte
def tClampUp(tryte: str) -> str:
    return __apply_unary_to_tryte('clampUp', tryte)


@makeTryte
def tInc(tryte: str) -> str:
    return __apply_unary_to_tryte('inc', tryte)


@makeTryte
def tIsNeg(tryte: str) -> str:
    return __apply_unary_to_tryte('isNeg', tryte)


@makeTryte
def tDec(tryte: str) -> str:
    return __apply_unary_to_tryte('dec', tryte)


@makeTryte
def tNotZero(tryte: str) -> str:
    return __apply_unary_to_tryte('notZero', tryte)


@makeTryte
def tNotPos(tryte: str) -> str:
    return __apply_unary_to_tryte('notPos', tryte)


@makeTryte
def tAdd(tryte1: str, tryte2: str) -> str:
    global log_depth, indent
    logger.debug(f'{indent * log_depth}>>>>> add {tryte1} {tryte2}')
    log_depth += 1
    if pIsZero(tryte1):
        log_depth -= 1
        return tryte2
    if pIsZero(tryte2):
        log_depth -= 1
        return tryte1
    
    len1 = len(tryte1)
    len2 = len(tryte2)
    add1 = tryte1[::-1] if len1 > len2 else tryte2[::-1]
    add2 = tryte2[::-1] if len2 < len1 else tryte1[::-1]
    len1 = len(add1)
    len2 = len(add2)

    carry = tZ
    acc = tZ
    index = 0
    result = ''
    while index < len1:
        t1 = add1[index]
        t2 = tZ if index > (len2-1) else add2[index]
        carry1 = __apply_to_trit('consensus', carry, t1)
        acc = __apply_to_trit('sum', carry, t1)
        carry2 = __apply_to_trit('consensus', acc, t2)
        acc = __apply_to_trit('sum', acc, t2)
        carry = __apply_to_trit('sum', carry1, carry2)
        result = acc + result
        logger.debug(f'{indent * log_depth}{t1} + {t2} = {acc} carry {carry} accumulated {result}')
        index += 1
        
    logger.debug(f'{indent * log_depth}***** returning: {result}')
    log_depth -= 1
    return result


@makeTryte
def tMultiply(tryte1: str, tryte2: str) -> str:
    global log_depth, indent
    logger.debug(f'{indent * log_depth}>>>>> multiply {tryte1} {tryte2}')
    log_depth += 1
    if pIsZero(tryte1) or pIsZero(tryte2):
        log_depth -= 1
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
            mul1 = tShiftLeft(mul1, 1)
            continue
        result = ''.join([tritMul(trit, t2) for t2 in mul1])
        logger.debug(f'{indent * log_depth}result for {trit} = {result}')
        result_list.append(result)
        mul1 = tShiftLeft(mul1, 1)
    
    result = tZ
    for tryte in result_list:
        result = tAdd(result, tryte)
    
    logger.debug(f'{indent * log_depth}***** returning: {result}')
    log_depth -= 1
    return result


##### Conversions

def tryteToInt(tryte: str) -> int:
    global log_depth, indent
    logger.debug(f'{indent * log_depth}>>>>> {tryte}')
    log_depth += 1
    acc = 0
    exponent = 1
    logger.debug(f'{indent * log_depth}tryte: {tryte}')
    tryte = tryte[::-1]
    logger.debug(f'{indent * log_depth}reverse tryte: {tryte}')
    for trit in tryte:
        value = trit_chars.index(trit) -1
        acc += value * exponent
        logger.debug(f'{indent * log_depth}trit: {trit} value: {value} exponent: {exponent} accumulated: {acc}')
        exponent *= 3
    logger.debug(f'{indent * log_depth}***** returning: {acc}')
    log_depth -= 1
    return acc


@makeTryte
def intToTryte(number: int) -> str:
    global log_depth, indent
    logger.debug(f'{indent*log_depth}>>>>> {number}')
    log_depth += 1
    negative = False
    if number < 0:
        logger.debug(f'{indent * log_depth}!!! Negative set to True.')
        negative = True
        number *= -1
    
    exponent = tP
    result = tZ
    while number > 0:
        logger.debug(f'{indent * log_depth}getting value')
        current = number % 10
        digit = decimal_index[current]
        value = tMultiply(digit, exponent)
        result = tAdd(result, value)
        logger.debug(f'{indent * log_depth}current: {current} ternary: {digit} value: {value} exponent: {exponent} acc: {result}\n')
        number = number // 10
        if number > 0:
            logger.debug(f'{indent * log_depth}getting exponent')
            exponent = tAdd(tShiftLeft(exponent, 2), exponent)

    if negative:
        result = tNegate(result)

    logger.debug(f'{indent * log_depth}***** returning: {result}')
    log_depth -= 1
    return result
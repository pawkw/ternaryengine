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
def __apply_to_tryte(operation: str, tryte: str) -> str:
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
def tShiftLeft(tryte: str) -> str:
    return (tryte+tZ)[-trits_per_tryte:]

@makeTryte
def tAdd(tryte1: str, tryte2: str) -> str:
    if tIsZero(tryte1):
        return tryte2
    if tIsZero(tryte2):
        return tryte1
    
    logger.debug(f'tAdd adding {tryte1} and {tryte2}.')

    sum = __apply_to_tryte('sum', tryte1, tryte2)
    carry = tShiftLeft(__apply_to_tryte('consensus', tryte1, tryte2))
    acc = __apply_to_tryte('sum', sum, carry)
    print(sum)
    print(carry)
    return acc
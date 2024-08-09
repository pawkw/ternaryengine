from defs import *
from typing import Callable, Any
from functools import partial
import monadic, diadic
import logging

logger = logging.getLogger(__name__)


##### Decorators

def makeTryte(func: Callable[..., Any]) -> Callable[..., Any]:
    def convertToTryte(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        if len(result) > trits_per_tryte:
            logger.warn(f'Tryte overflow produced by {func.__name__}: {result}.')
        return ('zzzzzzzzz' + result)[-trits_per_tryte:]
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
    return tryte.lstrip('z')


@makeTryte
def pad(tryte: str) -> str:
    logger.debug(f'tryte {tryte}')
    return tryte


@makeTryte
def __apply_to_tryte(operation: str, tryte: str) -> str:
    logger.debug(f'operation {operation} tryte {tryte}')
    function = partial(monadic.apply_operand, operation)
    return ''.join(list(map(function, tryte)))


@makeTryte
def __apply_to_tryte(operation: str, tryte1: str, tryte2: str) -> str:
    logger.debug(f'operation {operation} tryte1 {tryte1} tryte2 {tryte2}')
    function = partial(diadic.apply_operand, operation)
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
    diadic.app

##### Tryte predicates

@makeTrit
def tSign(tryte: str) -> str:
    tryte = strip(tryte)
    if len(tryte) == 0:
        return 'z'
    return tryte[0]


def tIsZero(tryte: str) -> bool:
    return tSign(tryte) == 'z'


def tIsNeg(tryte: str) -> bool:
    return tSign(tryte) == 'n'


def tIsPos(tryte: str) -> bool:
    return tSign(tryte) == 'p'


##### Tryte Operators

@makeTryte
def tAdd(tryte1: str, tryte2: str) -> str:
    if tIsZero(tryte1):
        return tryte2
    if tIsZero(tryte2):
        return tryte1
    
    operand1 = strip(tryte1)
    operand2 = strip(tryte2)
    len1 = len(operand1)
    len2 = len(operand2)

    acclen = len1
    if len1 != len2:
        if len1>len2:
            tryte2 = f"{'z'*(len1-len2)}{tryte2}"
        else:
            tryte1 = f"{'z'*(len2-len1)}{tryte1}"
            acclen = len2
    logger.debug(f'tAdd adding {tryte1} and {tryte2}.')


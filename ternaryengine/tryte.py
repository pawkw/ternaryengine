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


##### Tritwise operators


##### Tryte Operators

def tConstNeg(tryte: str) -> str:
    logger.debug(f'tryte {tryte}')
    return __apply_to_tryte('constNeg', tryte)


def tIsPos(tryte: str) -> str:
    logger.debug(f'tryte {tryte}')
    return __apply_to_tryte('isPos', tryte)
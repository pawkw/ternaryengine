from ternaryengine.tryte import *
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.WARN, format=FORMAT)

d1 = 10
d2 = 20
t1 = intToTryte(d1)
t2 = intToTryte(d2)
print(f'adding: {d1} {d2}')
print(f'adding: {t1} {t2}')
result = tAdd(t1, t2)
decimal = tryteToInt(result)
print(f'result: {result} = {decimal}')
if decimal != (d1+d2):
    print('Error!')
print()
print(f'multiplying: {t1} {t2}')
result = tMultiply(t1, t2)
decimal = tryteToInt(result)
print(f'result: {result} = {decimal}')
if decimal != (d1*d2):
    print('Error!')

for number in range(-13, 13):
    tryte = intToTryte(number)
    decimal = tryteToInt(tryte)
    print(f'{number} {tryte} {decimal} {'Error!' if number != decimal else ''}')

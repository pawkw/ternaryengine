from ternaryengine.defs import *

monadic_list = [
    'nnn',
    'nnz',
    'nnp',
    'nzn',
    'nzz',
    'nzp',
    'npn',
    'npz',
    'npp',
    'znn',
    'znz',
    'znp',
    'zzn',
    'zzz',
    'zzp',
    'zpn',
    'zpz',
    'zpp',
    'pnn',
    'pnz',
    'pnp',
    'pzn',
    'pzz',
    'pzp',
    'ppn',
    'ppz',
    'ppp',
]

operator_dict = {
'constNeg': 0,
# : 1,
'isPos': 2,
'true': 2,
'>': 2,
# : 3,
'clampDown' : 4,
'id': 5,
'isZero': 6,
'unKnown': 6,
'=': 6,
# : 7,
'notNeg': 8,
'notFalse': 8,
'>=': 8,
# : 9,
# : 10,
# : 11,
# : 12,
'constZero': 13,
'clampUp' : 14,
'inc': 15,
# : 16,
# : 17,
'isNeg': 18,
'false': 18,
'<': 18,
'dec': 19,
'notZero': 20,
'known': 20,
'!=': 20,
'negate': 21,
# : 22,
# : 23,
'notPos': 24,
'notTrue': 24,
'<=': 24,
# : 25,
'constPos': 26,
}

def apply_operator(operator: str, trit: str) -> str:
    if operator not in operator_dict.keys():
        raise ValueError(f'Bad operator: {operator}')
    
    if trit not in trit_chars:
        raise ValueError(f'Bad trit {trit}')
    
    index = operator_dict[operator]
    return monadic_list[index][trit_chars.index(trit)]
from ternaryengine.defs import *

operator_dict = {
    'min': 'nnnnzznzp',
    'max': 'nzpzzpppp',
    'antimin': 'ppppzzpzn',
    'antimax': 'pznppnnnn',
    'sum': 'pnznzpzpn',
    'xor': 'nzpzzzpzn',
    'consensus': 'nzzzzzzzp',
    'any': 'nnznzpzpp',
    'same': 'pnnnpnnnp',
    'equal': 'pnnnpnnnp',
    'diff': 'npppnpppn',
    'mul': 'pznzzznzp',
    'compare': 'zppnzpnnz'
}


def apply_operator(operator: str, trit1: str, trit2: str) -> str:
    if operator not in operator_dict.keys():
        raise ValueError(f'Bad operator: {operator}')
    
    if trit1 not in trit_chars or trit2 not in trit_chars:
        raise ValueError(f'Bad trit {trit1} or {trit2}')
    
    index1 = trit_chars.index(trit1)
    index2 = trit_chars.index(trit2)
    return operator_dict[operator][index1*3 + index2]
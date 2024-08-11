from dataclasses import dataclass

@dataclass
class AST:
    type: str = 'nil'
    data: str = ''
    children = []
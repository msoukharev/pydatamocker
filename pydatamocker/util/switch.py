from typing import Dict, TypeVar

V = TypeVar('V')
R = TypeVar('R')

def switch(test: V, switch: Dict[V, R]) -> R:
    return switch[test]

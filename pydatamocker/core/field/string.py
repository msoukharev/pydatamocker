from typing import Any
from pydatamocker.types import FieldGenerator


def append(gen: FieldGenerator, arg: Any) -> FieldGenerator:
    return lambda size: gen(size).map(lambda x: str(x) + str(arg))


def prepend(gen: FieldGenerator, arg: Any) -> FieldGenerator:
    return lambda size: gen(size).map(lambda x: str(arg) + str(x))

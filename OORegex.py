from dataclasses import dataclass
from typing import Union, Pattern, Optional
import re


@dataclass
class OORegexBase:
    value: "OOValue" = ""

    def build(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return self.build()

    def __or__(self, other: "OOValue"):
        if self.value == "":
            return other if isinstance(other, OORegexBase) else Str(other)
        other_value = str(other)
        return OORegexBase(f"{self}|{other_value}")

    def __add__(self, other):
        return OORegexBase(f"{self}{other}")

    def __and__(self, other):
        return self + other

    def regex(self) -> Pattern:
        return re.compile(self.build())


OOValue = Union[OORegexBase, str]


@dataclass
class Str(OORegexBase):
    value: "OOValue" = ""


@dataclass
class Group(OORegexBase):
    name: Optional[str] = None

    def build(self) -> str:
        if self.name is None:
            return f"({self.value})"
        return f"(?P<{self.name}>{self.value})"


@dataclass
class Quantifier(OORegexBase):
    min: int = 0
    max: int = -1

    def build(self) -> str:
        assert self.min >= 0
        assert self.min <= self.max or self.max == -1
        max_occurrences = "" if self.max == -1 else self.max
        value = (
            self.value
            if isinstance(self.value, OORegexBase) or len(self.value) == 1
            else Group(self.value)
        )
        return f"{value}{{{self.min},{max_occurrences}}}"


@dataclass
class Unforced(Quantifier):
    min: int = 0
    max: int = 1


class OORegex(OORegexBase):
    def __init__(self, contain_elem: Optional[OOValue] = None):
        self._starts_with = None
        self._ends_with = None
        if contain_elem is not None:
            self._contain_elements = [contain_elem]
        else:
            self._contain_elements = []

    def starts_with(self, value: OOValue) -> "OORegex":
        self._starts_with = value
        return self

    def ends_with(self, value: OOValue) -> "OORegex":
        self._ends_with = value
        return self

    def then(self, value: OOValue) -> "OORegex":
        self.contains(value)
        return self

    def contains(self, value: OOValue) -> "OORegex":
        self._contain_elements.append(value)
        return self

    def build(self):
        build_str = ""
        if self._starts_with is not None:
            build_str += f"^{self._starts_with}"
        for elem in self._contain_elements:
            build_str += str(elem)
        if self._ends_with is not None:
            build_str += f"^{self._ends_with}$"
        return build_str

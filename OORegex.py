import math
import re
from typing import Optional, Pattern, Union

unlimited = math.inf
OORValue = Union["OORegexBase", str]


class OORegexBase:
    _D_value: OORValue = ""

    def __init__(self, value: OORValue = None):
        self._value = value or self._D_value

    def build(self) -> str:
        return str(self._value)

    def __str__(self) -> str:
        return self.build()

    def __or__(self, other: OORValue):
        if self._value == "":
            return other if isinstance(other, OORegexBase) else R(other)
        other_value = str(other)
        return OORegexBase(f"{self}|{other_value}")

    def __add__(self, other):
        return OORegexBase(f"({self})({other})")

    def __and__(self, other):
        return self + other

    def __neg__(self):
        return OORegex(f"(?!{self._value})")

    def regex(self) -> Pattern:
        return re.compile(self.build())


class R(OORegexBase):
    _D_min_occurrences: Optional[int] = None
    _D_max_occurrences: Optional[int] = None
    _D_group: Optional[str] = None

    def __init__(
        self,
        value: OORValue = None,
        min_occurrences: Optional[int] = None,
        max_occurrences: Optional[int] = None,
        group: Optional[str] = None,
    ):
        super().__init__(value)
        self._min_occurrences = min_occurrences or self._D_min_occurrences
        self._max_occurrences = max_occurrences or self._D_max_occurrences
        self._group = group or self._D_group

    def build(self) -> str:
        if self._max_occurrences is not None or self._min_occurrences is not None:
            self._value = Quantifier(
                value=self._value, min=self._min_occurrences, max=self._max_occurrences
            ).build()
        if self._group is not None:
            self._value = Group(value=self._value, name=self._group).build()
        return super().build()


class Group(OORegexBase):
    def __init__(self, value: OORValue, name: Optional[str] = None):
        super().__init__(value)
        self._name = name

    def build(self) -> str:
        if self._name is None:
            return f"({self._value})"
        return f"(?P<{self._name}>{self._value})"


class Quantifier(OORegexBase):
    _D_min: Optional[int] = None
    _D_max: Optional[int] = None

    def __init__(
        self, value: OORValue, min: Optional[int] = None, max: Optional[int] = None
    ):
        super().__init__(value)
        self._min = min or self._D_min
        self._max = max or self._D_max

        if self._max is not None:
            self._min = self._min or 0

        if self._min is not None:
            self._max = self._max or unlimited

        assert self._min is None or self._min >= 0
        assert self._max is None or self._max >= 1 or self._max == unlimited

    def build(self) -> str:
        assert self._min >= 0
        assert self._min <= self._max
        max_occurrences = "" if self._max == unlimited else self._max
        value = (
            self._value
            if isinstance(self._value, OORegexBase) or len(self._value) == 1
            else Group(self._value)
        )
        return f"{value}{{{self._min},{max_occurrences}}}"


class Unforced(Quantifier):
    _D_min: int = 0
    _D_max: int = 1


class OORegex:
    def __init__(self, contain_elem: Optional[OORValue] = None):
        self._starts_with = None
        self._ends_with = None
        if contain_elem is not None:
            self._contain_elements = [contain_elem]
        else:
            self._contain_elements = []

    def starts_with(self, value: OORValue) -> "OORegex":
        self._starts_with = value
        return self

    def ends_with(self, value: OORValue) -> "OORegex":
        self._ends_with = value
        return self

    def then(self, value: OORValue) -> "OORegex":
        self.contains(value)
        return self

    def contains(self, value: OORValue) -> "OORegex":
        self._contain_elements.append(value)
        return self

    def build(self):
        build_str = ""
        if self._starts_with is not None:
            build_str += f"^{self._starts_with}"
        for elem in self._contain_elements:
            build_str += str(elem)
        if self._ends_with is not None:
            build_str += f"{self._ends_with}$"
        return build_str

    def regex(self) -> Pattern:
        return re.compile(self.build())

import pytest

from ooregex import Group
from ooregex import Digit


@pytest.mark.parametrize(
    "match, result",
    [
        ["0", False],
        ["1", True],
        ["3", True],
        ["6", True],
        ["9", True],
        ["11", True],
        ["12", True],
        ["02", False],
        ["15", False],
        ["001", False],
    ],
)
def test_month(match, result):
    d = Digit(min=1, max=12, group="month").regex()
    assert (d.fullmatch(match) is not None) == result


@pytest.mark.parametrize(
    "match, result",
    [
        ["0", False],
        ["3", True],
        ["01", True],
        ["05", True],
        ["11", True],
        ["12", True],
        ["012", False],
        ["15", False],
        ["001", False],
    ],
)
def test_month_with_optional_0(match, result):
    oore = Digit(min=1, max=12, optional_zfill=True).regex()
    assert (oore.fullmatch(match) is not None) == result


def test_group_and_multi_number():
    d = Digit(min=1, max=3, min_occurrences=2)
    d.build()


@pytest.mark.parametrize(
    "word, matches, groups_count",
    [["aa", ["baa", "aaaa", "baabaa", "baba"], [1, 2, 2, 0]]],
)
def test_group_matches_result(word, matches, groups_count):
    q = Group(word)
    for i, match in enumerate(matches):
        groups = q.regex().findall(match)
        assert len(groups) == groups_count[i]

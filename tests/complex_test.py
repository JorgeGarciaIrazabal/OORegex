import pytest

from OORegex import Quantifier, Group, OORegex, Unforced, Str
from any_in_group import Digit


@pytest.mark.parametrize(
    "match, result",
    [
        ["1", True],
        ["9", True],
        ["03", True],
        ["11", True],
        ["12", True],
        ["15", False],
        ["001", False],
        ["021", False],
    ],
)
def test_month(match, result):
    oore = (
        OORegex().contains(Group(Unforced("0") + Digit(max=12), name="month")).regex()
    )
    assert (oore.fullmatch(match) is not None) == result


@pytest.mark.parametrize(
    "word, matches, groups_count",
    [["aa", ["baa", "aaaa", "baabaa", "baba"], [1, 2, 2, 0]]],
)
def test_group_matches_result(word, matches, groups_count):
    q = Group(word)
    for i, match in enumerate(matches):
        groups = q.regex().findall(match)
        assert len(groups) == groups_count[i]
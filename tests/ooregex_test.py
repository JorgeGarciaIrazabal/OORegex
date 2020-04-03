import pytest

from OORegex import Quantifier, Group
from any_in_group import Digit


@pytest.mark.parametrize(
    "word, min, max, matches,not_matches",
    [
        ["a", 0, 3, ["a", "aa", "aaa"], ["aaaa", "ba"]],
        ["a", 0, -1, ["a", "aa", "aaaaaa"], ["ba"]],
        ["a", 3, -1, ["aaa", "aaaaaa"], ["ba", "a", "aa"]],
        ["abc", 0, 3, ["abc", "abcabc", "abcabcabc"], ["a", "ab", "abcabcabcabcabc"]],
    ],
)
def test_quantifier_matches_result(word, min, max, matches, not_matches):
    q = Quantifier(word, min=min, max=max)
    for match in matches:
        assert q.regex().fullmatch(match) is not None
    for not_match in not_matches:
        assert not q.regex().fullmatch(not_match)


@pytest.mark.parametrize(
    "word, matches, groups_count",
    [["aa", ["baa", "aaaa", "baabaa", "baba"], [1, 2, 2, 0]]],
)
def test_group_matches_result(word, matches, groups_count):
    q = Group(word)
    for i, match in enumerate(matches):
        groups = q.regex().findall(match)
        assert len(groups) == groups_count[i]


@pytest.mark.parametrize(
    "min, max, matches,not_matches",
    [
        [0, 3, [0, 2, 3], [5, 12, 22]],
        [0, 34, [4, 12, 22, 31], [38, 55, -3]],
        [0, 123, [4, 12, 22, 122], [-38, 1929, -3, 149, 500]],
    ],
)
def test_digit_matches_result(min, max, matches, not_matches):
    q = Digit(min=min, max=max)
    for match in matches:
        assert q.regex().fullmatch(str(match)) is not None
    for not_match in not_matches:
        assert not q.regex().fullmatch(str(not_match))

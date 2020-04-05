import pytest

from OORegex import Quantifier, Group, unlimited, R
from any_in_group import Digit, Punctuation


@pytest.mark.parametrize(
    "word, min, max, matches,not_matches",
    [
        ["a", 0, 3, ["a", "aa", "aaa"], ["aaaa", "ba"]],
        ["a", 0, unlimited, ["a", "aa", "aaaaaa"], ["ba"]],
        ["a", 3, unlimited, ["aaa", "aaaaaa"], ["ba", "a", "aa"]],
        ["abc", 0, 3, ["abc", "abcabc", "abcabcabc"], ["a", "ab", "abcabcabcabcabc"]],
    ],
)
def test_quantifier_matches_result(word: str, min: int, max: int, matches, not_matches):
    q = R(word, min_occurrences=min, max_occurrences=max)
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
    "word, matches, result",
    [["aa", ["baa", "aaaa", "baabaa", "baba"], [True, True, True, False]]],
)
def test_named_group(word, matches, result):
    q = R(word, group="my_group")
    for i, match in enumerate(matches):
        if result[i]:
            assert ("my_group" in q.regex().search(match).groupdict()) == result[i]
        else:
            assert q.regex().search(match) is None


@pytest.mark.parametrize(
    "min, max, matches,not_matches",
    [
        [None, None, [0, 2, 3, 1], [58, 12, 22]],
        [0, 3, [0, 2, 3], [5, 12, 22]],
        [0, 34, [4, 12, 22, 31], [38, 55, -3]],
        [0, 123, [4, 12, 22, 122], [-38, 1929, -3, 149, 500]],
        [5, 8, [5, 8, 6], [4, -6, 9, 11]],
    ],
)
def test_digit_matches_result(min: int, max: int, matches, not_matches):
    q = Digit(min=min, max=max)
    for match in matches:
        assert q.regex().fullmatch(str(match)) is not None
    for not_match in not_matches:
        assert not q.regex().fullmatch(str(not_match))


@pytest.mark.parametrize("match, result", [[".", True], ["-", True], ["a", False]])
def test_punctuation_matches_result(match, result):
    q = Punctuation()
    assert (q.regex().fullmatch(str(match)) is not None) == result

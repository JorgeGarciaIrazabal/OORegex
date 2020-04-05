from ooregex import R


def bounded_regex_for_range(
    min_, max_, zfill=False, optional_zfill=False
):
    return r"\b({})\b".format(
        regex_for_range(min_, max_, zfill, optional_zfill)
    )


def regex_for_range(min_, max_, zfill=False, optional_zfill=False):
    """
    > regex_for_range(12, 345)
    '1[2-9]|[2-9]\d|[1-2]\d{2}|3[0-3]\d|34[0-5]'
    """
    positive_subpatterns = []
    negative_subpatterns = []

    if min_ < 0:
        min__ = 1
        if max_ < 0:
            min__ = abs(max_)
        max__ = abs(min_)

        negative_subpatterns = _split_to_patterns(
            min__, max__, zfill, optional_zfill
        )
        min_ = 0

    if max_ >= 0:
        positive_subpatterns = _split_to_patterns(
            min_, max_, zfill, optional_zfill
        )

    negative_only_subpatterns = [
        "-" + val for val in negative_subpatterns if val not in positive_subpatterns
    ]
    positive_only_subpatterns = [
        val for val in positive_subpatterns if val not in negative_subpatterns
    ]
    intersected_subpatterns = [
        "-?" + val for val in negative_subpatterns if val in positive_subpatterns
    ]

    subpatterns = (
        negative_only_subpatterns + intersected_subpatterns + positive_only_subpatterns
    )
    return "|".join(subpatterns)


def _split_to_patterns(min_, max_, zfill, optional_zfill):
    subpatterns = []
    digits_count = len(str(max_))

    start = min_
    for stop in _split_to_ranges(min_, max_):
        range_to_pattern = _range_to_pattern(start, stop, zfill, optional_zfill, digits_count)
        subpatterns.append(range_to_pattern)
        start = stop + 1

    return subpatterns


def _split_to_ranges(min_, max_):
    stops = {max_}

    nines_count = 1
    stop = _fill_by_nines(min_, nines_count)
    while min_ <= stop < max_:
        stops.add(stop)

        nines_count += 1
        stop = _fill_by_nines(min_, nines_count)

    zeros_count = 1
    stop = _fill_by_zeros(max_ + 1, zeros_count) - 1
    while min_ < stop <= max_:
        stops.add(stop)

        zeros_count += 1
        stop = _fill_by_zeros(max_ + 1, zeros_count) - 1

    stops = list(stops)
    stops.sort()

    return stops


def _fill_by_nines(integer, nines_count):
    return int(str(integer)[:-nines_count] + "9" * nines_count)


def _fill_by_zeros(integer, zeros_count):
    return integer - integer % 10 ** zeros_count


def _range_to_pattern(start, stop, zfill, optional_zfill, digits_count):
    pattern = ""
    any_digit_count = 0

    for start_digit, stop_digit in zip(str(start), str(stop)):
        if start_digit == stop_digit:
            pattern += start_digit
        elif start_digit != "0" or stop_digit != "9":
            pattern += "[{}-{}]".format(start_digit, stop_digit)
        else:
            any_digit_count += 1

    if any_digit_count:
        pattern += r"\d"

    if any_digit_count > 1:
        pattern += "{{{}}}".format(any_digit_count)

    if zfill or optional_zfill:
        start_digits_count = len(str(start))
        zeros = digits_count - start_digits_count
        if zeros > 0:
            return str(
                R(
                    "0",
                    min_occurrences=0 if optional_zfill else zeros,
                    max_occurrences=zeros,
                )
            ) + pattern

    return pattern

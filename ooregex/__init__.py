from ooregex.OORegex import *
from ooregex.any_in_group import *


if __name__ == "__main__":
    a = (
        OORegex()
        .starts_with(Digit(min=1500, max=3999, group="year"))
        .then("-")
        .then(Digit(min=1, max=12, zfill=True, group="month"))
        .then("-")
        .ends_with(Digit(min=1, max=31, zfill=True, group="day"))
    )


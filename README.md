# OORegex
Object Oriented regular expression

## What is the goal of this library

If you are like me, every time you have to write a regular expression you search on google and try to learn this "language" that is not intuitive and has too many symbols.

In a lot of cases checking if a string contains a date or it is a valid library version ends up with small peaces of regular expression but with a lot of comments around it.

I personally believe we can do better, there has to be a way to convert those comments in real code and then you voila! you get a readable code that doesn't need comments and hopefully less searching time to build it.

 
## Examples

Date regex:

```python

from ooregex import Digit, OORegex

r = (
    OORegex()
    .starts_with(Digit(min=1500, max=3999, group="year"))
    .then("-")
    .then(Digit(min=1, max=12, zfill=True, group="month"))
    .then("-")
    .ends_with(Digit(min=1, max=31, zfill=True, group="day"))
)
```

returns this regex:

`^(?P<year>150\d|15[1-9]\d|1[6-9]\d{2}|[2-3]\d{3})(-)(?P<month>0{1}[1-9]|1[0-2])(-)(?P<day>0{1}[1-9]|[1-2]\d|3[0-1])$`


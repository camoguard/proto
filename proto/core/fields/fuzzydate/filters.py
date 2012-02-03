from django.conf import settings
from django.template import defaultfilters
from django.utils import dateformat

from core import FuzzyDate, DATE_PRECISIONS

FUZZYDATE_FORMATS = {
    DATE_PRECISIONS.DAY: getattr(settings, 'DATE_FORMAT', 'd m Y'),
    DATE_PRECISIONS.MONTH: 'M Y',
    DATE_PRECISIONS.YEAR: 'Y',
    DATE_PRECISIONS.QUARTER: '%QQ Y',
    DATE_PRECISIONS.HALFYEAR: '%H\\H Y',
}

def date(value, arg=None):
    """
    Version of the default date filter that supports fuzzy dates. The argument
    is a |-separated string that contains the format strings for each precision
    in the order they appear in the DatePrecision enum. They are all optional
    though, and if you want to skip one and use the default, that's fine - just
    leave it empty, e.g. { val|date:"dayformat|monthformat|||yearformat"}

    If you prefix the format string with *, then only one format is accepted,
    which will be used for all possibly precisions. Of course, this might
    possibly fail, so be careful.

    Note that the tag is backwards-compatible with the default tag for
    non-fuzzy dates, so you can just add it to builtins and are done.
    """
    # what was passed in overwrites everything else
    if arg:
        if arg.startswith('*'):
            # use the string for all formats
            arg = arg[1:]
            for precision in DATE_PRECISIONS:
                FUZZYDATE_FORMATS[precision] = arg
        else:
            # replace with passed in arguments
            args = arg.split('|')
            c = 0
            for precision in DATE_PRECISIONS:
                if c >= len(args): break
                FUZZYDATE_FORMATS[precision] = args[c]
                c += 1

    # for fuzzy dates, do our custom handling; unfortunately, django wants to
    # use PHP's formatting style here, so we can't use FuzzyDate.strftime()
    if isinstance(value, FuzzyDate):
        format = FUZZYDATE_FORMATS[value.precision[0]]
        format = format.replace('%Q', str((value.date.month-1)//3+1))
        format = format.replace('%H', str((value.date.month-1)//6+1))
        return dateformat.format(value.date, format)
    # for non-fuzzy dates, fall back to the default formatting filter
    else:
        return defaultfilters.date(value, arg)
date.is_safe = False

from django.template import Library
register = Library()
register.filter(date)
import re, time, datetime
from django.forms import widgets
from django.forms import fields
from django.utils.functional import curry
from core import FuzzyDate, DATE_PRECISIONS


__all__ = (
    'FuzzyDateInput',
    'FuzzyDateField'
)


class FuzzyDateInput(widgets.DateInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, FuzzyDate):
            value = value.strftime(
                    fpmonth='%Y-%m',
                    fpquarter='%%Y-%dQ',
                    fphalfyear='%%Y-%dH',
                    fpyear='%Y',
                )
        return super(FuzzyDateInput, self).render(name, value, attrs)


class FuzzyDateField(fields.DateField):
    widget = FuzzyDateInput

    def parse_with_re(value, regex, month_factor, precision):
        m = regex.match(value.strip())
        if not m: raise ValueError()
        else:
            m = m.groups()
            return FuzzyDate(
                date=datetime.date(int(m[0]), (int(m[1])-1)*month_factor+1, 1),
                precision=precision)

    """e.g. 2007/1q, 2007-1Q"""
    quarter_re = re.compile('^(\d{4})(?:\s+|/|-)([1-4])q$', re.I)
    """e.g. 2007/1h, 2007-1H"""
    halfyear_re = re.compile('^(\d{4})(?:\s+|/|-)([1-2])h$', re.I)

    FORMAT_STRINGS = {
        DATE_PRECISIONS.MONTH: ['%m/%Y', '%Y/%m', '%Y-%m', '%m-%Y'],
        DATE_PRECISIONS.YEAR: ['%Y'],
        DATE_PRECISIONS.QUARTER: [curry(parse_with_re, regex=quarter_re,
                                      month_factor=3, precision=DATE_PRECISIONS.QUARTER)],
        DATE_PRECISIONS.HALFYEAR: [curry(parse_with_re, regex=halfyear_re,
                                       month_factor=6, precision=DATE_PRECISIONS.HALFYEAR)]
    }

    def clean(self, value):
        """
        Validates that the input can be converted to a date. Returns a
        FuzzyDate object.
        """
        # FuzzyDate instances are easy
        if isinstance(value, FuzzyDate):
            pass
        # Try to convert fuzzy date strings
        for precision, formats in self.FORMAT_STRINGS.items():
            for format in formats:
                try:
                    if callable(format):
                        return format(value)
                    else:
                        return FuzzyDate(date=datetime.date(*time.strptime(value, format)[:3]),
                                         precision=precision)
                except ValueError:
                    pass
        # Everything we can't or don't want to handle we pass on to the base
        # class. This could also be a datetime instance for example.
        return FuzzyDate(date=super(FuzzyDateField, self).clean(value),
                         precision=DATE_PRECISIONS.DAY)
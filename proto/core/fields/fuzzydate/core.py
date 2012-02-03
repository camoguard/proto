import datetime

class Enumeration(object):
    """
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.

    Example:
        MY_ENUM = Enumeration([
            (100, 'MY_NAME', 'My verbose name'),
            (200, 'MY_AGE', 'My verbose age'),
        ])
        assert MY_ENUM.MY_AGE == 100
        assert MY_ENUM[1] == (200, 'My verbose age')
    """

    def __init__(self, *enum_list):
        self.enum_list = [(item[0], item[2]) for item in enum_list]
        self.enum_dict = {}
        for item in enum_list:
            self.enum_dict[item[1]] = item[0]

    def __contains__(self, v):
        return (v in self.enum_list)

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, v):
        if isinstance(v, basestring):
            return self.enum_dict[v]
        elif isinstance(v, int):
            return self.enum_list[v]

    def __getattr__(self, name):
        return self.enum_dict[name]

    def __iter__(self):
        return self.enum_list.__iter__()


DATE_PRECISIONS = Enumeration(
        (0, 'DAY', 'Day precision'),
        (1, 'MONTH', 'Month precision'),
        (2, 'QUARTER', 'Quarter precision'),
        (3, 'HALFYEAR', 'Half-year precision'),
        (4, 'YEAR', 'Year precision')
    )


class FuzzyDate(object):
    """
    For now, basically just a wrapper around a date instance and
    a precision value. Immutable.
    """
    def __new__(cls, date, precision=DATE_PRECISIONS.DAY):
        self = object.__new__(cls)
        self.__date = date
        if isinstance(precision, (int, long,)):
            precision = precision or DATE_PRECISIONS.DAY
        self.__precision = precision
        return self

    def _get_date(self):
        """
        Make sure the fuzzy parts of the date are always represented by the
        same values in the date instance we provide.
        """
        if self.precision == DATE_PRECISIONS.MONTH:
            return self.__date.replace(day=1)
        elif self.precision == DATE_PRECISIONS.QUARTER:
            return self.__date.replace(day=1, month=(self.__date.month-1)//3*3+1)
        elif self.precision == DATE_PRECISIONS.HALFYEAR:
            return self.__date.replace(day=1, month=(self.__date.month-1)//6*6+1)
        elif self.precision == DATE_PRECISIONS.YEAR:
            return self.__date.replace(day=1, month=1)
        else:
            return self.__date

    date = property(_get_date)
    precision = property(lambda self: self.__precision)

    def __repr__(self):
        return "%s (%s)" % (repr(self.date), self.precision[1])

    def __str__(self):
        return self.strftime()

    def __getattr__(self, attr):
        """
        Fall back to the date objects for attributes that don't exist.
        Although this makes us backwords-compatible with the default
        DateField, it will also make it more difficult to spot places
        were changes are needed, so you might want to remove or disable
        this, at least for migration.
        """
        return getattr(self.date, attr)

    def __cmp__(self, other):
        if isinstance(other, datetime.datetime):
            return cmp(self.date, other.date())
        elif isinstance(other, datetime.date):
            return cmp(self.date, other)
        elif isinstance(other, FuzzyDate):
            result = cmp(self.date, other.date)
            if result != 0:
                return result
            else:
                return cmp(self.precision, other.precision)

        return cmp(id(self), id(other))

    def __hash__(self):
        return hash((self.date, self.precision,))

    def strftime(self, fpday='%Y-%m-%d', fpmonth='%m/%Y', fpquarter='%dQ %%Y',
                 fphalfyear='%s half %%Y', fpyear='%Y'):
        """
        Format the day. Can take a separate format argument for each possible
        precision - if one is missing, it falls back to a default. The quarter
        and year format string formatted before passed on to the original
        strftime, so you need to make sure that the actual date format variables
        are escaped via a double %%. So the default format strings for each
        precision.
        """
        if self.precision == DATE_PRECISIONS.MONTH:
            format = fpmonth
        elif self.precision == DATE_PRECISIONS.QUARTER:
            format = fpquarter%((self.date.month-1)//3+1)
        elif self.precision == DATE_PRECISIONS.HALFYEAR:
            format = fphalfyear % ((self.date.month-1)//6+1)
        elif self.precision == DATE_PRECISIONS.YEAR:
            format = fpyear
        else:
            format = fpday
        return self.date is not None and self.date.strftime(format) or ''

    def is_fuzzy(self):
        return self.precision != DATE_PRECISIONS.DAY

    def replace(self, date=None, precision=None, **kwargs):
        """
        Like the replace method from the datetime module, but supports an
        additional precision parameter. Instead of just replacing a part of
        a date, you can also pass in a date instance. You can even mix:

        field.replace(date=datetime.date.today(), day=1)

        Which will set the date to the beginning of the current month.
        """
        return FuzzyDate(
                            # both kwargs and date passed => use modified date
                            (kwargs and date) and date.replace(**kwargs) or
                            # if only kwargs passed: use modified self.date
                            kwargs and self.date.replace(**kwargs) or
                            # if only date passed: use it
                            date and date or
                            # otherwise, use self.date (don't change)
                            self.date,
                         precision = precision or self.precision)
from django.template.defaultfilters import slugify
from django.db.models import SlugField
import re


class AutoSlugField(SlugField):
    """ AutoSlugField

    By default, sets editable=False, blank=True.

    Required arguments:

    populate_from
        Specifies which field or list of fields the slug is populated from.

    Optional arguments:

    separator
        Defines the used separator (default: '-')

    overwrite
        If set to True, overwrites the slug on every save (default: False)

    Inspired by SmileyChris' Unique Slugify snippet:
    http://www.djangosnippets.org/snippets/690/

    Modified from the AutoSlugField in django_extensions to better handle slugs
    that end with a number.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        populate_from = kwargs.pop('populate_from', None)
        if populate_from is None:
            raise ValueError("missing 'populate_from' argument")
        else:
            self._populate_from = populate_from
        self.separator = kwargs.pop('separator', u'-')
        self.overwrite = kwargs.pop('overwrite', False)
        self.allow_duplicates = kwargs.pop('allow_duplicates', False)
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def _slug_strip(self, value):
        """
        Cleans up a slug by removing slug separator characters that occur at
        the beginning or end of a slug.

        If an alternate separator is used, it will also replace any instances
        of the default '-' separator with the new separator.
        """
        re_sep = '(?:-|%s)' % re.escape(self.separator)
        value = re.sub('%s+' % re_sep, self.separator, value)
        return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)

    def slugify_func(self, content):
        if content:
            return slugify(content)
        return ''

    def create_slug(self, model_instance, add):
        # get fields to populate from and slug field to set
        if not isinstance(self._populate_from, (list, tuple)):
            self._populate_from = (self._populate_from, )
        slug_field = model_instance._meta.get_field(self.attname)

        if not add and not self.overwrite:
            # no point in recalculating a slug if we already have a
            # perfectly good one stored on the instance
            slug = self._slug_strip(getattr(model_instance, self.attname))
            return slug

        # slugify the original field content and set next step to 2
        slug_for_field = lambda field: self.slugify_func(getattr(model_instance, field))
        slug = self.separator.join(map(slug_for_field, self._populate_from))
        next = 2

        # strip slug depending on max_length attribute of the slug field
        # and clean-up
        slug_len = slug_field.max_length
        if slug_len:
            slug = slug[:slug_len]
        slug = self._slug_strip(slug)
        original_slug = slug

        if self.allow_duplicates:
            return slug

        # exclude the current model instance from the queryset used in finding
        # the next valid slug
        queryset = model_instance.__class__._default_manager.all()
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        # form a kwarg dict used to implement any unique_together contraints
        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)
        kwargs[self.attname] = slug

        # increases the number while searching for the next valid slug
        # depending on the given slug, clean-up
        while not slug or queryset.filter(**kwargs):
            slug = original_slug
            end = '%s%s' % (self.separator, next)
            end_len = len(end)
            if slug_len and len(slug) + end_len > slug_len:
                slug = slug[:slug_len - end_len]
                slug = self._slug_strip(slug)
            slug = '%s%s' % (slug, end)
            kwargs[self.attname] = slug
            next += 1
        return slug

    def pre_save(self, model_instance, add):
        value = unicode(self.create_slug(model_instance, add))
        setattr(model_instance, self.attname, value)
        return value

    def get_internal_type(self):
        return "SlugField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = '%s.AutoSlugField' % self.__module__
        args, kwargs = introspector(self)
        kwargs.update({
            'populate_from': repr(self._populate_from),
            'separator': repr(self.separator),
            'overwrite': repr(self.overwrite),
            'allow_duplicates': repr(self.allow_duplicates),
        })
        # That's our definition!
        return (field_class, args, kwargs)

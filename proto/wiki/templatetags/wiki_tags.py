from django import template
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter()
def get_verbose_name(value):
    if isinstance(value, QuerySet):
        return value.model._meta.verbose_name
    return value._meta.verbose_name


@register.filter()
def get_verbose_name_plural(value):
    if isinstance(value, QuerySet):
        return value.model._meta.verbose_name_plural
    return value._meta.verbose_name_plural


@register.filter(is_safe=True)
def creole(value):
    try:
        import creole
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in {% creole %} filter: The Python creole library isn't installed.")
        return force_unicode(value)
    else:
        return mark_safe(force_unicode(creole.creole2html(value)))

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


register = template.Library()

# @register.filter(is_safe=True)
@register.filter()
def creole(value):
    try:
        import creole
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in {% creole %} filter: The Python creole library isn't installed.")
        return force_unicode(value)
    else:
        return mark_safe(force_unicode(creole.creole2html(value)))

creole.is_safe = True

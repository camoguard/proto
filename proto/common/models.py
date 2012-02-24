from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.related import RelatedObject


class InheritanceMixIn(models.Model):
    _class = models.CharField(max_length=100, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            parent = self._meta.parents.keys()[0]
            subclasses = parent._meta.get_all_related_objects()
            for klass in subclasses:
                if isinstance(klass, RelatedObject) and klass.field.primary_key \
                    and klass.opts == self._meta:
                    self._class = klass.get_accessor_name()
                    break
        return super(InheritanceMixIn, self).save(*args, **kwargs)

    def get_object(self):
        try:
            if self._class and self._meta.get_field_by_name(self._class)[0].opts != self._meta:
                return getattr(self, self._class)
        except FieldDoesNotExist:
            pass
        return self


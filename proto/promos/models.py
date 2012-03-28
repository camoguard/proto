from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from proto.news.models import Article
from proto.reviews.models import Review
from proto.videos.models import Video


MAX_NUM_PROMOS = 20


class PromoContainer(models.Model):
    site = models.ForeignKey(Site, unique=True, editable=False)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = 'promo'

    def __unicode__(self):
        return '%s promos' % self.site


class Promo(models.Model):
    promo_container = models.ForeignKey(PromoContainer)
    content_type = models.ForeignKey(ContentType, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey()
    position = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.id:
            # Assign the promo to the associated site's promo container
            obj, created = PromoContainer.objects.get_or_create(site=self.content_object.site)
            self.promo_container = obj
            self.position = self.promo_container.promo_set.count() + 1
        super(Promo, self).save(*args, **kwargs)


@receiver(post_save, sender=Article)
@receiver(post_save, sender=Review)
@receiver(post_save, sender=Video)
def create_new_promo(sender, instance, created, **kwargs):
    if created:
        Promo.objects.create(content_object=instance)

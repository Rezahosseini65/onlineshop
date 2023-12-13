import hashlib

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from onlineshop.apps.media.exceptions import DuplicateImageException


# Create your models here.
class Image(models.Model):
    title = models.CharField(_('Title'),max_length=64,blank=True,null=True)
    image = models.ImageField(_('Image'),width_field='width',height_field='height',upload_to='images/')

    width = models.IntegerField(_('Width'),editable=False)
    height = models.IntegerField(_('height'),editable=False)

    file_hash = models.CharField(_('File hash'),max_length=40,editable=False,db_index=True)
    file_size = models.PositiveIntegerField(_('File size'),null=True,editable=False)

    focal_point_x = models.PositiveIntegerField(_('Focal point X'),null=True,blank=True)
    focal_point_y = models.PositiveIntegerField(_('Focal point Y'),null=True,blank=True)
    focal_point_width = models.PositiveIntegerField(_('Focal point width'),blank=True,null=True)
    focal_point_height = models.PositiveIntegerField(_('Focal point height'),null=True,blank=True)

    def save(self,*args,**kwargs):
        if self.image.file.closed:
            self.file_size = self.image.size

            hasher = hashlib.sha1()
            for chunk in self.image.file.chunks():
                hasher.update(chunk)
            self.file_hash = hasher.hexdigest()
        super().save(*args,**kwargs)

@receiver(pre_save, sender=Image)
def check_duplicate_hash(sender, instance, **kwargs):
    existed = Image.objects.filter(file_hash=instance.file_hash).exclude(pk=instance.pk).exists()
    if existed:
        raise DuplicateImageException("Duplicate")


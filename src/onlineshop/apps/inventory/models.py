from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class StockRecord(models.Model):
    product = models.ForeignKey('catalogue.Product',on_delete=models.CASCADE,
                                related_name='stockrecords',verbose_name=_('Stock record'))
    sku = models.CharField(_('SKU'),max_length=64,blank=True,null=True,unique=True)
    buy_price = models.PositiveBigIntegerField(null=True,blank=True)
    sale_price = models.PositiveBigIntegerField()
    num_stock = models.PositiveIntegerField(default=0)
    threshold_low_stack = models.PositiveIntegerField(null=True, blank=True)

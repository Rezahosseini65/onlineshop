from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from treebeard.mp_tree import MP_Node

from onlineshop.apps.catalogue.managers import CategoryQuerySet
from onlineshop.utils.db.fields import UppercaseField


# Create your models here.

class Category(MP_Node):
    name = models.CharField(_('Name'),max_length=255,db_index=True)
    slug = models.SlugField(_('Slug'),max_length=255,allow_unicode=True,unique=True)
    description = models.TextField(_('Description'),blank=True)
    meta_title = models.CharField(_('Meta Title'),max_length=255,null=True,blank=True)
    meta_description = models.TextField(_('Meta Description'),blank=True,null=True)
    is_public = models.BooleanField(_('Is public'),default=True,db_index=True)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ["path"]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class ProductClass(models.Model):
    name = models.CharField(_('Name'),max_length=128)
    slug = models.SlugField(_('Slug'),max_length=128,unique=True,allow_unicode=True)
    description = models.TextField(_('Description'),null=True,blank=True)

    required_shipping = models.BooleanField(_('Required Shipping'),default=True)
    track_stock = models.BooleanField(_("Track stock levels?"), default=True)

    options = models.ManyToManyField('Option',blank=True)

    @property
    def has_attributes(self):
        return self.attributes.exists()

    class Meta:
        ordering = ('name',)
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        TEXT = _('Text')
        INTEGER = _('Integer')
        BOOLEAN = _('True / False')
        FLOAT = _('Float')
        DATE = _('Date')
        DATETIME = _('Datetime')
        OPTION = _('Option')
        MULTI_OPTION = _('Multi Option')
    product_class = models.ForeignKey(ProductClass,on_delete=models.CASCADE,null=True,blank=True,related_name='attributes')
    name = models.CharField(_('Name'),max_length=128)
    type = models.CharField(_('Type'),max_length=20,choices=AttributeTypeChoice.choices,default=AttributeTypeChoice.TEXT)
    required = models.BooleanField(_('Required'),default=False)
    option_group = models.ForeignKey("AttributeOptionGroup",on_delete=models.PROTECT,related_name='product_attribute',null=True,blank=True)

    class Meta:
        verbose_name = _('Product Attribute')
        verbose_name_plural = _('Product Attributes')

    def __str__(self):
        return self.name


class Product(models.Model):

    STANDALONE, PARENT, CHILD = "standalone", "parent", "child"
    STRUCTURE_CHOICES = (
        (STANDALONE, _("Stand-alone product")),
        (PARENT, _("Parent product")),
        (CHILD, _("Child product")),
    )

    structure = models.CharField(_('Structure'),max_length=20,choices=STRUCTURE_CHOICES,
                                 default=STANDALONE)
    is_public = models.BooleanField(_('Is public'),db_index=True,default=True)
    upc = UppercaseField(_('UPC'),max_length=64,blank=True,null=True,unique=True)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,
                               related_name='children',verbose_name=_('Parent Product'))
    title = models.CharField(_('Title'),max_length=255,db_index=True,blank=True)
    slug = models.SlugField(_('Slug'),max_length=255,unique=False,allow_unicode=True)
    description = models.TextField(_('Description'),null=True,blank=True)
    meta_title = models.CharField(_('Meta title'),max_length=255,blank=True,null=True)
    meta_description = models.TextField(_('Meta description'),blank=True,null=True)
    date_created = models.DateTimeField(_('Date created'),auto_now_add=True,db_index=True)
    date_updated = models.DateTimeField(_('Date updated'),auto_now=True,db_index=True)

    is_discountable = models.BooleanField(_('Is discountable?'),default=True)

    product_class=models.ForeignKey(ProductClass,on_delete=models.PROTECT,null=True,blank=True,
                                    related_name='products',verbose_name=_('Product type'))
    attribute = models.ManyToManyField(ProductAttribute,through='ProductAttributeValue',
                                       verbose_name=_('Attributes'))
    product_option = models.ManyToManyField('Option',blank=True,verbose_name=_('Product options'))
    recommended_products = models.ManyToManyField('catalogue.Product',through='ProductRecommendation',blank=True,
                                                   verbose_name=_('Recommended products'))
    categories = models.ManyToManyField(Category,verbose_name=_('Categories'),blank=True)

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None


    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=_('Product'),related_name='attribute_values')
    attribute = models.ForeignKey(ProductAttribute,on_delete=models.CASCADE,verbose_name=_('Attribute'),
                                  related_name='product_attribute')
    value_text = models.TextField(_('Text'),blank=True,null=True)
    value_integer = models.IntegerField(_('Integer'),blank=True,null=True)
    value_boolean = models.BooleanField(_('Boolean'),blank=True,null=True)
    value_float = models.FloatField(_('Float'),blank=True,null=True)
    value_date = models.DateField(_('Date'),blank=True,null=True)
    value_datetime = models.DateTimeField(_('DateTime'),blank=True,null=True)
    value_option = models.ForeignKey('AttributeOption',blank=True,null=True,on_delete=models.CASCADE,
                                     verbose_name=_('Value option'))
    value_multi_option = models.ManyToManyField('AttributeOption',blank=True,related_name='multi_valued_attribute_values',
                                                verbose_name=_('Value multi option'))



class ProductRecommendation(models.Model):
    primary = models.ForeignKey(Product,on_delete=models.CASCADE,
                                related_name='primary_recommendation',verbose_name=_('Primary product'))
    recommendation = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=_('Recommendation product'))
    rank = models.PositiveSmallIntegerField(_('Rank'),default=0,db_index=True)

    class Meta:
        ordering = ('primary','-rank')
        unique_together = ('primary','recommendation')
        verbose_name = _('Product recommendation')
        verbose_name_plural = _('Product recommendations')


class AttributeOptionGroup(models.Model):
    name = models.CharField(_('Name'),max_length=128)

    class Meta:
        verbose_name = 'Attribute Option Group'
        verbose_name_plural = 'Attribute Option Groups'

    def __str__(self):
        return self.name

class AttributeOption(models.Model):
    group = models.ForeignKey(AttributeOptionGroup,on_delete=models.CASCADE,related_name='options',
                              verbose_name=_('Group'))
    option = models.CharField(_('Option'),max_length=255)

    class Meta:
        unique_together = ('group','option')
        verbose_name = 'Attribute Option'
        verbose_name_plural = 'Attribute Options'

    def __str__(self):
        return self.option


class Option(models.Model):
    class OptionTypeChoice(models.TextChoices):
        TEXT = _('Text')
        INTEGER = _('Integer')
        FLOAT = _('Float')
        BOOLEAN = _('True / False')
        DATE = _('Date')
        MULTI_OPTION = _('Multi Option')

    name = models.CharField(_('Name'),max_length=128,db_index=True)
    type = models.CharField(_('Type'),max_length=16,choices=OptionTypeChoice.choices,default=OptionTypeChoice.TEXT)
    required = models.BooleanField(_('s this option required?'),default=False)
    option_group = models.ForeignKey(AttributeOptionGroup,blank=True,null=True,on_delete=models.CASCADE,
                                    related_name="product_options",verbose_name=_("Option Group"),
                                    help_text=_('Select an option group if using type "Option" or "Multi Option"'),)

    order = models.IntegerField(_("Ordering"),null=True,blank=True,db_index=True,
                                help_text=_("Controls the ordering of product options on product detail pages"),)

    class Meta:
        ordering = ('order','name')
        verbose_name = _("Option")
        verbose_name_plural = _("Options")


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ForeignKey('media.Image',on_delete=models.PROTECT)

    display_order = models.PositiveSmallIntegerField(_('Display order'),default=0)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        for index, image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()

    class Meta:
        ordering = ('display_order',)
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')


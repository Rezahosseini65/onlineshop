from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from onlineshop.apps.catalogue.models import Category, ProductAttributeValue, ProductRecommendation, ProductAttribute, \
    ProductClass, Product, Option, AttributeOption, AttributeOptionGroup, ProductImage


# Register your models here.

class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    prepopulated_fields = {'slug':('name',)}

class AttributeInline(admin.TabularInline):
    model = ProductAttributeValue

class ProductRecommendationInline(admin.TabularInline):
    model = ProductRecommendation
    fk_name = "primary"
    raw_id_fields = ["primary","recommendation"]

class CategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2
@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('name','slug','track_stock','required_shipping','has_attributes')
    list_filter = ('track_stock','required_shipping')
    prepopulated_fields = {'slug':('name',)}

    inlines = [ProductAttributeInline]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):


    date_hierarchy = "date_created"
    list_display = ('title','slug','structure','is_public','date_created','upc','get_category')
    list_filter = ('structure','is_discountable','is_public','date_created','date_updated')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('upc','title')
    raw_id_fields = ["parent"]


    inlines = [AttributeInline,ProductRecommendationInline,CategoryInline,ProductImageInline]

    def get_category(self,obj):
        return [category.name for category in obj.categories.all()]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name','type','required','product_class')

class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption

@admin.register(AttributeOptionGroup)
class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

    inlines = [AttributeOptionInline]

@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product','attribute')



admin.site.register(Category,CategoryAdmin)
admin.site.register(AttributeOption)

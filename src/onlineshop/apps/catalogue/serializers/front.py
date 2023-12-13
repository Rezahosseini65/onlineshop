from rest_framework import serializers

from onlineshop.apps.catalogue.models import Category, Product, ProductClass, ProductAttribute, AttributeOptionGroup, \
    AttributeOption


class CategoryFrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','slug','description','meta_title','meta_description')



class AttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeOption
        fields = ('option',)

class AttributeOptionGroupSerializer(serializers.ModelSerializer):
    options = AttributeOptionSerializer(many=True)
    class Meta:
        model = AttributeOptionGroup
        fields = ('name','options')

class ProductAttributeSerializer(serializers.ModelSerializer):
    option_group = AttributeOptionGroupSerializer()
    class Meta:
        model = ProductAttribute
        fields = ('name','option_group')



class ProductChildSerializer(serializers.ModelSerializer):
    attribute = ProductAttributeSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id','slug','meta_title','description','meta_description','attribute')

class ProductClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductClass
        fields = ('name','slug','description','required_shipping')

class ProductParentSerializer(serializers.ModelSerializer):
    product_class = ProductClassSerializer()
    children = ProductChildSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id','structure','title','slug','stockrecords','meta_title','description','meta_description','product_class','children','images')




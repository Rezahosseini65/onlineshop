from rest_framework import viewsets

from onlineshop.apps.catalogue.models import Category, Product
from onlineshop.apps.catalogue.serializers.front import CategoryFrontSerializer, ProductParentSerializer


class CategoryFrontViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.browsable()
    serializer_class = CategoryFrontSerializer

class ProductFrontViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.exclude(product_class=None)
    serializer_class = ProductParentSerializer
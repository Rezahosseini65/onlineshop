from rest_framework.routers import SimpleRouter

from onlineshop.apps.catalogue.views.front import CategoryFrontViewSet, ProductFrontViewSet

router = SimpleRouter()
router.register('categories',CategoryFrontViewSet)
router.register('products',ProductFrontViewSet)
urlpatterns = [

]+router.urls
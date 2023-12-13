from rest_framework.routers import SimpleRouter

from onlineshop.apps.catalogue.views.admin import CategoryAdminViewSet

router = SimpleRouter()
router.register('categories',CategoryAdminViewSet,basename='Category')

urlpatterns = [

]+router.urls
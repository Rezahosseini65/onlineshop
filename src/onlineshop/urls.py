"""
URL configuration for onlineshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin_urlpatterns =[
    path('api/admin/users/',include(('onlineshop.auths.users.urls.admin','onlineshop.auths.users'),
                                    namespace='admin-login')),
    path('api/admin/catalogue/',include(('onlineshop.apps.catalogue.urls.admin','onlineshop.apps.catalogue'),
                                        namespace='admin-category')),
]

front_urlpatterns = [
    path('api/front/users/',include(('onlineshop.auths.users.urls.front','onlineshop.auths.users'),
                                    namespace='front-login')),
    path('api/front/catalogue/',include(('onlineshop.apps.catalogue.urls.front','onlineshop.apps.catalogue'),
                                        namespace='front-catalogue')),
]

doc_urlpatterns =[
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
]+admin_urlpatterns+front_urlpatterns+doc_urlpatterns

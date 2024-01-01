from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Cakes API",
      default_version='v1',
      description="Cakes API with Yum! factor",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="samumatt@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   validators=['ssv']
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('documentation<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('documentation/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-web'),
    path('api/', include('api.urls')),
]

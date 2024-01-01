from api import views
from django.urls import path

urlpatterns = [
    path('cakes/list/', views.ListCakeAPIView.as_view(),
         name='cakes-list'),

    path('cakes/create/', views.CreateCakeAPIView.as_view(),
         name='cakes-create'),

    path('cakes/delete/<int:pk>', views.DeleteCakeAPIView.as_view(),
         name='cakes-delete'),

    path('yum/create/', views.CreateYumAPIView.as_view(),
         name='yum-create'),
]

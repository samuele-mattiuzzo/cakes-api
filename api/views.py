from api.serializers import CakeSerializer, YumSerializer
from app.models import Cake, YumRating
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics


@method_decorator(name='get', decorator=cache_page(60 * 60 * 2))
@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id="List cakes"
))
class ListCakeAPIView(generics.ListAPIView):
    """
        API endpoint to list all the cakes in the system
    """
    serializer_class = CakeSerializer
    queryset = Cake.objects.all()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id="Create cakes"
))
class CreateCakeAPIView(generics.CreateAPIView):
    """
        API endpoint to add a new cake
    """
    serializer_class = CakeSerializer
    queryset = Cake.objects.all()


@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_id="Delete cakes"
))
class DeleteCakeAPIView(generics.DestroyAPIView):
    """
        API endpoint to delete an existing cake
    """
    serializer_class = CakeSerializer
    queryset = Cake.objects.all()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id="Create yum ratings"
))
class CreateYumAPIView(generics.CreateAPIView):
    """
        API endpoint to rate an existing cake
    """
    serializer_class = YumSerializer
    queryset = YumRating.objects.all()

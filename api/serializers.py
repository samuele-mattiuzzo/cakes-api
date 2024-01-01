from app.models import Cake, YumRating
from rest_framework import serializers


class CakeSerializer(serializers.ModelSerializer):
    yumFactor = serializers.ReadOnlyField()

    class Meta:
        model = Cake
        fields = ['id', 'name', 'comment', 'imageUrl', 'yumFactor']


class YumSerializer(serializers.ModelSerializer):

    class Meta:
        model = YumRating
        fields = ['id', 'cake', 'rating']

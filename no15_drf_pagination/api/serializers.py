from rest_framework import serializers

from . import models

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        fields = ['name', 'price', 'brand']
""" Convert Python-types to JSON compatible data """

from rest_framework import serializers

from api_service import models


class DatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DatasetModel
        fields = '__all__'
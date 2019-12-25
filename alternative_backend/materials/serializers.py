from workers.models import Worker
from currency.models import Currency
from materials.models import Material
from rest_framework import serializers
from materials.services import MaterialService
from materials.models import (
    MaterialDelivery,
    MaterialCategory,
    MaterialDeliveryPosition,
)


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory 
        fields = ('id', 'name', 'description')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'description', 'unit', 'category', 'price', 'currency')

    category = serializers.SlugRelatedField(many=False,
                                            queryset=MaterialCategory.objects.all(),
                                            slug_field='name')
    currency = serializers.SlugRelatedField(many=False,
                                            queryset=Currency.objects.all(),
                                            slug_field='symbol')


class MaterialDeliverySerializer(serializers.ModelSerializer):
    worker = serializers.SlugRelatedField(many=False,
                                          queryset=Worker.objects.all(),
                                          slug_field='username')

    class Meta:
        model = MaterialDelivery
        fields = ('id', 'timestamp', 'worker')


class MaterialDeliveryPositionSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(many=False,
                                            queryset=Material.objects.all(),
                                            slug_field='name')

    class Meta:
        model = MaterialDeliveryPosition
        fields = ('id', 'quantity', 'material')


class MaterialDeliveryDetailedSerializer(serializers.ModelSerializer):
    positions = MaterialDeliveryPositionSerializer(many=True)
    worker = serializers.SlugRelatedField(many=False,
                                          queryset=Worker.objects.all(),
                                          slug_field='username')

    def create(self, validated_data):
        return MaterialService().create_material_delivery(validated_data=validated_data)

    def update(self, instance, validated_data):
        MaterialService().update_material_delivery(instance=instance,
                                                   validated_data=validated_data)

        return instance

    class Meta:
        model = MaterialDelivery
        fields = ('id', 'timestamp', 'worker', 'positions')

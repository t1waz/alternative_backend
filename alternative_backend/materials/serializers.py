from rest_framework import serializers
from materials.models import (
    MaterialCategory,
    Material,
    BoardModelComponent,
)


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory 
        fields = ('id', 'name', 'description')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'description', 'unit', 'category')

    category = serializers.SlugRelatedField(many=False,
                                            queryset=MaterialCategory.objects.all(),
                                            slug_field='name')


class BoardModelComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModelComponent
        fields = ('id', 'material', 'quantity')

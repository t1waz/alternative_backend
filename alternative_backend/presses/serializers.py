from rest_framework import serializers
from .models import Press
from boards.models import BoardModel


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ('id', 'name', 'mold')

    mold = serializers.SlugRelatedField(many=False,
                                        queryset=BoardModel.objects.all(),
                                        slug_field='name')

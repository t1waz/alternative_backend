from rest_framework import serializers

from boards.models import BoardModel
from presses.models import Press
from presses.services import PressService


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ('id', 'name', 'mold', 'press_time')

    mold = serializers.SlugRelatedField(many=False,
                                        queryset=BoardModel.objects.all(),
                                        slug_field='name',
                                        allow_null=True)

    def create(self, validated_data):
        press = super().create(validated_data)
        mold = validated_data.get('mold')
        if mold:
            PressService().start_mold_history_record(press=press,
                                                     mold=validated_data['mold'],
                                                     worker=self.context['worker'])

        return press

    def update(self, instance, validated_data):
        new_mold = validated_data.get('mold')

        if new_mold:
            worker = self.context['worker']

            PressService().handle_history(press=instance,
                                          mold=validated_data['mold'],
                                          worker=worker)

        return super().update(instance, validated_data)

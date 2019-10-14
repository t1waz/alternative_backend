from workers.models import Worker
from boards.models import BoardModel
from rest_framework import serializers
from presses.services import PressService
from presses.models import (
    Press,
    MoldHistory,
)


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ('id', 'name', 'mold', 'press_time')

    mold = serializers.SerializerMethodField()

    def get_mold(self, obj):
        open_record = PressService().get_open_mold_history_records(press=obj)

        return open_record.mold.name


class MoldHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoldHistory
        fields = ('worker', 'press', 'mold')

    worker = serializers.SlugRelatedField(many=False,
                                          queryset=Worker.objects.all(),
                                          slug_field='barcode')
    press = serializers.SlugRelatedField(many=False,
                                        queryset=Press.objects.all(),
                                        slug_field='name')
    mold = serializers.SlugRelatedField(many=False,
                                        queryset=BoardModel.objects.all(),
                                        slug_field='name')

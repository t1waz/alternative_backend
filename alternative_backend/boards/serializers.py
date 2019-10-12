from workers.models import Worker
from stations.models import Station
from orders.models import SendedBoard
from rest_framework import serializers
from boards.services import BoardService
from rest_framework.validators import UniqueTogetherValidator
from boards.models import (
    BoardCompany,
    BoardModel,
    Board,
    BoardScan,
)
from boards.validators import (
    BoardCompanyValidation,
    BoardModelValidation,
    BoardValidation,
)


class BoardCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCompany
        fields = ('id', 'description', 'name', 'code')
        validators = [BoardCompanyValidation()]


class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ('id', 'description', 'year', 'company', 'name', 'code')
        validators = [BoardModelValidation()]


class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('second_category', )


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('barcode', 'model', 'company')

    model = serializers.SlugRelatedField(many=False,
                                         queryset=BoardModel.objects.all(),
                                         slug_field='name')
    company = serializers.SlugRelatedField(many=False,
                                           queryset=BoardCompany.objects.all(),
                                           slug_field='name')


class BoardDetailViewSerializer(BoardListSerializer):
    class Meta:
        model = Board
        fields = ('barcode', 'model', 'company', 'second_category',
                  'year', 'customer', 'production_history')

    customer = serializers.SerializerMethodField()
    production_history = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_customer(self, obj):
        try:
            sended = SendedBoard.objects.select_related(
                'order').filter(board=obj.id)
            client = sended[0].order.client.name
        except:
            client = ""
        return client

    def get_production_history(self, obj):
        scans = BoardScan.objects.filter(barcode=obj.id).select_related(
            'station')
        return ["{} : {}".format(e.station.name, e.timestamp) for e in scans]

    def get_year(self, obj):
        return obj.model.year


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('barcode',)
        validators = [BoardValidation()]

    def create(self, validated_data):
        barcode = validated_data['barcode']
        new_board = BoardService().create_new_board_from_barcode(barcode=barcode)

        return new_board


class BoardScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardScan
        fields = ('worker', 'station', 'barcode', 'comment')
        validators = [UniqueTogetherValidator(queryset=BoardScan.objects.all(),
                                              fields=('barcode', 'station'))]

    barcode = serializers.SlugRelatedField(many=False,
                                           queryset=Board.objects.all(),
                                           slug_field='barcode')
    worker = serializers.SlugRelatedField(many=False,
                                          queryset=Worker.objects.all(),
                                          slug_field='username')
    station = serializers.SlugRelatedField(many=False,
                                           queryset=Station.objects.all(),
                                           slug_field='name')

    def create(self, validated_data):
        BoardService().add_missing_scans(last_scan=validated_data)

        return super().create(validated_data)

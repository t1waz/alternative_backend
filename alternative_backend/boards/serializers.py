from workers.models import Worker
from .services import BoardService
from stations.models import Station
from orders.models import SendedBoard
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .validators import (
    BoardCompanyValidation,
    BoardModelValidation,
    BoardValidation,
)
from .models import (
    BoardCompany,
    BoardModel,
    Board,
    BoardScan,
)


class BoardCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCompany
        fields = ('id', 'description', 'name', 'code')
        validators = (BoardCompanyValidation(fields), )


class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ('id', 'description', 'year', 'company', 'name', 'code')
        validators = (BoardModelValidation(fields),)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'barcode', 'model', 'company', 'press_time')
        write_only_fields = ('model', 'company')
        read_only_fields = ('press_time',)
        validators = (BoardValidation(fields),)

    def update_initial_data(self):
        # TODO make more clear
        barcode = self.initial_data.get('barcode')

        model = BoardService().get_model(barcode=barcode)
        company = BoardService().get_company(barcode=barcode)
        if model and company:
            self.initial_data.update({
                'model': model.id,
                'company': company.id
            })

    def is_valid(self, raise_exception=False):
        self.update_initial_data()

        return super().is_valid(raise_exception=False)


class BoardPresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('company', 'model', 'year', 'barcode', 'customer', 'production_history')

    model = serializers.SlugRelatedField(many=False,
                                         queryset=BoardModel.objects.all(),
                                         slug_field='name')

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


class BoardSecondCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('barcode', 'second_category')


class BoardScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardScan
        fields = ('worker', 'station', 'barcode', 'timestamp', 'comment')
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
    timestamp = serializers.DateTimeField(required=False)
    comment = serializers.CharField(required=False)

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from alternative_backend.exceptions import AppException
from alternative_backend.settings import BARCODE_LENGHT
from workers.models import Worker
from stations.models import Station
from orders.models import SendedBoard
from .models import (
    BoardCompany,
    BoardModel,
    Board,
    BoardScan
)


class BoardCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCompany
        fields = ('id', 'description', 'name', 'code')


class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ('id', 'description', 'year', 'company')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('barcode', 'model', 'company')
        write_only_fields = ('model', 'company')

    def is_valid(self, raise_exception=False):
        try:
            model_code = int(str(self.initial_data['barcode'])[2:4])
            company_code = int(str(self.initial_data['barcode'])[4:6])

            model_id = BoardModel.objects.get(code=model_code,
                                              company__code=company_code).id
            company_id = BoardCompany.objects.get(code=company_code).id
        except:
            return False
        self.initial_data.update({'model': model_id})
        self.initial_data.update({'company': company_id})

        return super().is_valid(raise_exception=True)

    def validate_barcode(self, barcode):
        if not len(str(barcode)) == BARCODE_LENGHT:
            raise AppException("barcode number not valid")
        board_code = int(str(barcode)[2:4])
        company_code = int(str(barcode)[4:6])
        if not BoardModel.objects.filter(code=board_code,
                                         company__code=company_code).exists():
            raise AppException("barcode model or company not valid")

        return barcode


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

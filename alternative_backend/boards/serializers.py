from rest_framework import serializers
from .models import BoardCompany, BoardModel, Board, BoardScan
from workers.models import Worker
from stations.models import Station
from alternative_backend.exceptions import AppException
from rest_framework.validators import UniqueTogetherValidator
from orders.models import SendedBoard



class BoardCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCompany
        fields = ('id', 'description', 'name', 'code')


class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ('id', 'description', 'year', 'company')


class BoardSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        model_code = int(str(self.initial_data['barcode'])[2:4])
        company_code = int(str(self.initial_data['barcode'])[4:6])
        try:
            model_id = BoardModel.objects.get(code=model_code).id
            company_id = BoardCompany.objects.get(code=company_code).id
        except:
            return False
        self.initial_data.update({'model': model_id})
        self.initial_data.update({'company': company_id})

        return super().is_valid(raise_exception=True)

    def validate_barcode(self, barcode):
        if not 10000000000000 <= int(barcode) <= 99999999999999:
            raise AppException("barcode number not valid")
        board_code = int(str(barcode)[2:4])
        company_code = int(str(barcode)[4:6])
        if not BoardModel.objects.filter(code=board_code,
                                         company__code=company_code).exists():
            raise AppException("barcode model or company not valid")
        return barcode


    class Meta:
        model = Board
        fields = ('barcode', 'model', 'company')


class BoardPresentationSerializer(serializers.ModelSerializer):
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
        scans = BoardScan.objects.filter(barcode_scan=obj.id).select_related('station')
        production_list = list()
        for each in scans:
            production_record = "%s : %s" %(each.station.name, each.timestamp)
            production_list.append(production_record)
        return production_list

    def get_year(self, obj):
        return obj.model.year

    class Meta:
        model = Board
        fields = ('company', 'model', 'year', 'barcode', 'customer', 'production_history')


class BoardScanSerializer(serializers.ModelSerializer):
    barcode_scan = serializers.SlugRelatedField(many=False,
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

    class Meta:
        model = BoardScan
        fields = ('worker', 'station', 'barcode_scan', 'timestamp', 'comment')
        write_only_fields = ('model', 'company')
        validators = [ UniqueTogetherValidator(queryset=BoardScan.objects.all(),
                                               fields=('barcode_scan', 'station')) ]




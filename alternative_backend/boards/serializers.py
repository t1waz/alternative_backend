from rest_framework import serializers
from .models import BoardCompany, BoardModel, Board, BoardScan
from workers.models import Worker
from stations.models import Station
from alternative_backend.exceptions import AppException
from rest_framework.validators import UniqueTogetherValidator




class BoardCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCompany
        fields = ('id', 'description', 'company_name', 'company_code')


class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ('id', 'description', 'year', 'company')


class BoardSerializer(serializers.ModelSerializer):
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
        fields = ('model', 'year', 'company', 'barcode')


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

    class Meta:
        model = BoardScan
        fields = ('worker', 'station', 'barcode_scan', 'timestamp')
        validators = [ UniqueTogetherValidator(queryset=BoardScan.objects.all(),
                                               fields=('barcode_scan', 'station')) ]




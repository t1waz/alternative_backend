from rest_framework import serializers
from .models import BoardCompany, BoardModel, Board, BoardScan
from workers.models import Worker
from stations.models import Station

class BoardCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardCompany
		fields = ('id', 'description', 'company_name', 'company_code')


class BoardModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardModel
		fields = ('id', 'description', 'year', 'company')


class BoardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Board
		fields = ('model','company', 'barcode')


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


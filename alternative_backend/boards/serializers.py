from rest_framework import serializers
from .models import BoardCompany, BoardModel, Board, BoardScan


class BoardCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardCompany
		fields = ('id', 'description', 'company_name')


class BoardModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardModel
		fields = ('id', 'description', 'year', 'company')


class BoardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Board
		fields = ('id', 'model', 'barcode', 'company')


class BoardScanSerializer(serializers.ModelSerializer):
	barcode_scan = serializers.PrimaryKeyRelatedField(many=False, 
													  queryset=Board.objects.all())
	class Meta:
		model = BoardScan
		fields = ('worker','station', 'barcode_scan', 'timestamp')


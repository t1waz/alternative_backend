from rest_framework import serializers
from .models import BoardCompany, BoardModel, Board, BoardScan


class BoardCompanySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = BoardCompany
		fields = ('id', 'description', 'company_name')


class BoardModelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = BoardModel
		fields = ('id', 'description', 'year', 'company')


class BoardSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Board
		fields = ('id', 'model', 'barcode', 'company')


class BoardScanSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = BoardScan
		fields = ('id', 'board', 'worker', 'station', 'timestamp')


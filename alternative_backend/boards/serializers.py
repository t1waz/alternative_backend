from workers.models import Worker
from stations.models import Station
from rest_framework import serializers
from boards.services import BoardService
from rest_framework.validators import UniqueTogetherValidator
from materials.models import Material
from boards.models import (
    Board,
    Layout,
    BoardScan,
    BoardModel,
    BoardCompany,
    BoardGraphic,
    BoardModelMaterial,
)
from boards.validators import (
    BoardValidation,
    BoardModelValidation,
    BoardCompanyValidation,
    BoardModelMaterialValidation,
)


class BoardCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCompany
        fields = ('id', 'description', 'name', 'code')
        validators = [BoardCompanyValidation()]


class BoardGraphicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGraphic
        fields = ('name')


class BoardModelMaterialSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(many=False,
                                            queryset=Material.objects.all(),
                                            slug_field='name')

    class Meta:
        model = BoardModelMaterial
        fields = ('material', 'quantity')
        validators = [BoardModelMaterialValidation()]


class BoardModelMaterialsSerializer(serializers.ModelSerializer):
    components = BoardModelMaterialSerializer(many=True)

    class Meta:
        model = BoardModel
        fields = ('components',)

    def update(self, instance, validated_data):
        BoardService().update_components(model=instance,
                                         components=validated_data['components'])

        return instance


class BoardModelLayoutSerializer(serializers.ModelSerializer):
    top_graphic = serializers.SlugRelatedField(many=False,
                                               queryset=BoardGraphic.objects.all(),
                                               slug_field='name',
                                               allow_null=True)
    bottom_graphic = serializers.SlugRelatedField(many=False,
                                                  queryset=BoardGraphic.objects.all(),
                                                  slug_field='name',
                                                  allow_null=True)
    top_material = serializers.SlugRelatedField(many=False,
                                                queryset=Material.objects.all(),
                                                slug_field='name',
                                                allow_null=True)
    bottom_material = serializers.SlugRelatedField(many=False,
                                                   queryset=Material.objects.all(),
                                                   slug_field='name',
                                                   allow_null=True)

    class Meta:
        model = Layout
        fields = ('top_graphic', 'bottom_graphic', 
                  'top_material', 'bottom_material',)


class BoardModelSerializer(serializers.ModelSerializer):
    layout = BoardModelLayoutSerializer(many=False)
    production_price = serializers.SerializerMethodField()

    def get_production_price(self, obj):
        return round(BoardService().get_price_for_model(model=obj), 2)

    def create(self, validated_data):
        return BoardService().create_new_model(**validated_data)

    class Meta:
        model = BoardModel
        validators = [BoardModelValidation()]
        fields = ('id', 'description', 'year', 'company', 'layout_material_quantity',
                  'name', 'code', 'layout', 'production_price')


class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('second_category', )


class BoardListSerializer(serializers.ModelSerializer):
    model = serializers.SlugRelatedField(many=False,
                                         queryset=BoardModel.objects.all(),
                                         slug_field='name')
    company = serializers.SlugRelatedField(many=False,
                                           queryset=BoardCompany.objects.all(),
                                           slug_field='name')

    class Meta:
        model = Board
        fields = ('barcode', 'model', 'company')


class BoardDetailViewSerializer(BoardListSerializer):
    customer = serializers.SerializerMethodField()
    production_history = serializers.SerializerMethodField()
    production_price = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_customer(self, obj):
        return BoardService().get_board_customer(barcode=obj.barcode)

    def get_production_history(self, obj):
        return BoardService().get_board_production_history(barcode=obj.barcode)

    def get_production_price(self, obj):
        return BoardService().get_price_for_board(board=obj)

    def get_year(self, obj):
        return obj.model.year

    class Meta:
        model = Board
        fields = ('barcode', 'model', 'company', 'second_category',
                  'year', 'customer', 'production_history', 'production_price')


class BoardCreateSerializer(serializers.ModelSerializer):
    layout = BoardModelLayoutSerializer(many=False,
                                        required=False,
                                        allow_null=True)

    def create(self, validated_data):
        return BoardService().create_new_board(**validated_data)

    class Meta:
        model = Board
        validators = [BoardValidation()]
        fields = ('barcode', 'layout')


class BoardScanSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = BoardScan
        fields = ('worker', 'station', 'barcode', 'comment')
        validators = [UniqueTogetherValidator(queryset=BoardScan.objects.all(),
                                              fields=('barcode', 'station'))]

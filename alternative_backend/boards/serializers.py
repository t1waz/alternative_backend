from workers.models import Worker
from stations.models import Station
from rest_framework import serializers
from boards.services import BoardService
from rest_framework.validators import UniqueTogetherValidator
from materials.models import Material
from boards.fields import (
    TopGraphicField,
    BottomGraphicField,
    TopMaterialField,
    BottomMaterialField,
)
from boards.models import (
    BoardCompany,
    BoardModel,
    Board,
    BoardScan,
    BoardModelMaterial,
    BoardGraphic,
)
from boards.validators import (
    BoardCompanyValidation,
    BoardModelValidation,
    BoardValidation,
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


class BoardModelSerializer(serializers.ModelSerializer):
    production_price_pln = serializers.SerializerMethodField()

    def get_production_price_pln(self, obj):
        return round(BoardService().get_price_for_model(model=obj), 2)

    class Meta:
        model = BoardModel
        validators = [BoardModelValidation()]
        fields = ('id', 'description', 'year', 'company', 
                  'name', 'code', 'production_price_pln')


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
    top_graphic = TopGraphicField(source='*',
                                  required=False)
    bottom_graphic = BottomGraphicField(source='*',
                                        required=False)
    top_material = TopMaterialField(source='*',
                                    required=False)
    bottom_material = BottomMaterialField(source='*',
                                          required=False)

    def create(self, validated_data):
        return BoardService().create_new_board(**validated_data)

    class Meta:
        model = Board
        validators = [BoardValidation()]
        fields = ('barcode', 'top_graphic', 'bottom_graphic', 
                  'top_material', 'bottom_material')
        non_required_fields = ('top_graphic', 'bottom_graphic', 
                               'top_material', 'bottom_material')


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

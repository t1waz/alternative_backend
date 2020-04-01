from django.db.models import Count, Sum

from boards.models import (
    BoardScan,
    BoardModelMaterial
)
from materials.models import (
    Material,
    MaterialDelivery,
    MaterialDeliveryPosition,
)


class MaterialService:
    def get_material_from_name(self, material_name):
        return Material.objects.filter(name=material_name).first() or None

    def create_delivery_positions(delivery, positions):
        for position in positions:
            position['delivery'] = delivery
            MaterialDeliveryPosition.objects.create(**position)

    def create_material_delivery(self, validated_data):
        positions = validated_data.pop('positions')

        delivery = MaterialDelivery.objects.create(**validated_data)

        self.create_delivery_positions(delivery=delivery,
                                       positions=positions)

        return delivery

    def update_material_delivery(self, instance, validated_data):
        if 'positions' in validated_data:
            instance.positions.all().delete()

            positions = validated_data.pop('positions')
            self.create_delivery_positions(delivery=instance,
                                           positions=positions)

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        instance.save()

    def get_material_stock_info(self):
        materials = {material: value for material, value in
                     MaterialDeliveryPosition.objects.all().values_list(
                         'material__name').annotate(quantity_sum=Sum('quantity'))}

        model_materials_data = BoardModelMaterial.objects.all().values_list(
            'model__name', 'material__name').annotate(quantity_sum=Sum('quantity'))

        manufactured_models_count = {model_name: model_count for model_name, model_count in
                                     BoardScan.objects.all().values_list(
                                         'barcode__model__name').annotate(
                                         barcode_count=Count('barcode'))}

        for data in model_materials_data:
            if data[1] in materials.keys():
                materials[data[1]] -= data[2] * manufactured_models_count[data[0]]
                if materials[data[1]] < 0:
                    materials[data[1]] = 0

        return materials

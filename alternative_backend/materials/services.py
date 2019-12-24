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

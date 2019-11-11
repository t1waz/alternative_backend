from boards.services import BoardService
from materials.services import MaterialService
from rest_framework import serializers
from django.core.exceptions import ValidationError


class TopGraphicField(serializers.Field):
    def to_representation(self, value):
        return getattr(value.layout.top_graphic, 'name', '')

    def to_internal_value(self, data):
        if data:
            graphic = BoardService().get_graphic_from_name(name=data)

            if not graphic:
                raise ValidationError('graphic name is incorrect')
        else:
            graphic = None

        return {'top_graphic': graphic}


class BottomGraphicField(serializers.Field):
    def to_representation(self, value):
        return getattr(value.layout.bottom_graphic, 'name', '')

    def to_internal_value(self, data):
        if data:
            graphic = BoardService().get_graphic_from_name(name=data)

            if not graphic:
                raise ValidationError('graphic name is incorrect')
        else:
            graphic = None

        return {'bottom_graphic': graphic}


class TopMaterialField(serializers.Field):
    def to_representation(self, value):
        return getattr(value.layout.top_material, 'name', '')

    def to_internal_value(self, data):
        if data:
            material = MaterialService().get_material_from_name(material_name=data)

            if not material:
                raise ValidationError('graphic name is incorrect')
        else:
            material = None

        return {'top_material': material}


class BottomMaterialField(serializers.Field):
    def to_representation(self, value):
        return getattr(value.layout.bottom_material, 'name', '')

    def to_internal_value(self, data):
        if data:
            material = MaterialService().get_material_from_name(material_name=data)

            if not material:
                raise ValidationError('graphic name is incorrect')
        else:
            material = None

        return {'bottom_material': material}

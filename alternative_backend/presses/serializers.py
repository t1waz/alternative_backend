from rest_framework import serializers
from .models import Press


class PressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Press
		fields = ('name', 'mold')

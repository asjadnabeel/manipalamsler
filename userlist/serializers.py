from rest_framework import serializers
from .models import AmslerGrid

class AmslerGridSerializer(serializers.ModelSerializer):
	class Meta:
		model = AmslerGrid
		fields = '__all__'

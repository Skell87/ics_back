from rest_framework import serializers
from.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# class DivisionSerializer(serializers.Serializer):
#     class Meta:
#         model = Division
#         fields = ['name', 'count']

# class WarehouseSerializer(serializers.ModelSerializer):
#     divisions = DivisionSerializer(many=True)
#     class Meta:
#         model = Warehouse
#         fields = ['name', 'divisions']

#     def create(self, validated_data):
#         divisions_data = validated_data.pop('divisions')
#         warehouse = Warehouse.objects.create(**validated_data)
#         for division_data in divisions_data:
#             Division.objects.create(warehouse=warehouse, **division_data)
#         return warehouse
    

# =======================================================================================
# new stuff
    
class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        fields = '__all__'
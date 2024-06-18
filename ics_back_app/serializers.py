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


# =======================================================================================
# new stuff
# highest level warehouse section SECTION
class WarehouseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseSection
        # fields = ['name']
        fields = '__all__'
    
class WarehouseSubSectionSerializer(serializers.ModelSerializer):
    section = WarehouseSectionSerializer()
    class Meta:
        model = WarehouseSubSection
        # fields = ['name', 'section']
        fields = '__all__'

# lowest level warehouse section SUB SUB SECTION
class WarehouseSubSubSectionSerializer(serializers.ModelSerializer):
    # sub_section = WarehouseSubSectionSerializer()
    class Meta:
        model = WarehouseSubSubSection
        # fields = ['name', 'sub_section']
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        # fields = ['name', 'make', 'model', 'color', 'notes']
        fields = '__all__'

class InventoryDetailSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer()
    sub_sub_section = serializers.PrimaryKeyRelatedField(queryset=WarehouseSubSubSection.objects.all())
    
    class Meta:
        model = InventoryDetails
        # fields = ['quantity', 'inventory_item', 'sub_sub_section_id']
        fields = '__all__'
                  
    def create(self, validated_data):
        inventory_item_data = validated_data.pop('inventory_item')
        sub_sub_section_id = validated_data.pop('sub_sub_section')

        inventory_item, _ = InventoryItems.objects.get_or_create(**inventory_item_data)

        # sub_sub_section, _ = WarehouseSubSubSection.objects.get_or_create(id=sub_sub_section_id)

        inventory_detail = InventoryDetails.objects.create(
            quantity=validated_data['quantity'],
            inventory_item=inventory_item,
            sub_sub_section=sub_sub_section_id
        )

        return inventory_detail


class DeleteInventoryItemSerializer(serializers.Serializer):
    quantity_to_delete = serializers.IntegerField()



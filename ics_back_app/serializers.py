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

class WarehouseSubSectionReadSerializer(serializers.ModelSerializer):
    section = WarehouseSectionSerializer(read_only=True)
    class Meta:
        model = WarehouseSubSection
        # fields = ['name', 'section']
        fields = '__all__'


class WarehouseSubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseSubSection
        # fields = ['name', 'section']
        fields = '__all__'

# lowest level warehouse section SUB SUB SECTION
class WarehouseSubSubSectionReadSerializer(serializers.ModelSerializer):
    sub_section = WarehouseSubSectionReadSerializer(read_only=True)
    class Meta:
        model = WarehouseSubSubSection
        # fields = ['name', 'sub_section']
        fields = '__all__'

class WarehouseSubSubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseSubSubSection
        # fields = ['name', 'sub_section']
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        # fields = ['name', 'make', 'model', 'color', 'notes']
        fields = '__all__'

class InventoryDetailReadSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer(read_only=True)
    sub_sub_section = WarehouseSubSubSectionReadSerializer(read_only=True)

    class Meta:
        model = InventoryDetails
        # fields = ['quantity', 'inventory_item', 'sub_sub_section_id']
        fields = '__all__'    

class InventoryDetailSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer()

    class Meta:
        model = InventoryDetails
        # fields = ['quantity', 'inventory_item', 'sub_sub_section_id']
        fields = '__all__'
                  
    def create(self, validated_data):
        inventory_item_data = validated_data.pop('inventory_item')
        sub_sub_section_id = validated_data.pop('sub_sub_section')

        inventory_item, _ = InventoryItems.objects.get_or_create(**inventory_item_data)

        inventory_detail = InventoryDetails.objects.create(
            quantity=validated_data['quantity'],
            inventory_item=inventory_item,
            sub_sub_section=sub_sub_section_id
        )

        return inventory_detail


class DeleteInventoryItemSerializer(serializers.Serializer):
    quantity_to_delete = serializers.IntegerField()



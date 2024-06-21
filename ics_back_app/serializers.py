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

        def create(self, validated_data):
            user = self.context['request'].user
            section = WarehouseSection.objects.create(user=user, **validated_data)
            return section
        
        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance

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
        extra_kwargs = {
            'user': {'required': False}
        }
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

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
        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        # fields = ['name', 'make', 'model', 'color', 'notes']
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }

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
        extra_kwargs = {
            'user': {'required': False}
        }
                  
    def create(self, validated_data):
        user = self.context['request'].user
        inventory_item_data = validated_data.pop('inventory_item')
        sub_sub_section_id = validated_data.pop('sub_sub_section')

        inventory_item, _ = InventoryItems.objects.get_or_create(**inventory_item_data, user=user)

        inventory_detail = InventoryDetails.objects.create(
            user=user,
            quantity=validated_data['quantity'],
            inventory_item=inventory_item,
            sub_sub_section=sub_sub_section_id
        )

        return inventory_detail


class DeleteInventoryItemSerializer(serializers.Serializer):
    quantity_to_delete = serializers.IntegerField()


class InventoryDetailUpdateSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer()
    sub_sub_section_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = InventoryDetails
        fields = ['quantity', 'inventory_item', 'sub_sub_section_id']

    def update(self, instance, validated_data):
        user = self.context.get('user')
        inventory_item_data = validated_data.pop('inventory_item')
        sub_sub_section_id = validated_data.pop('sub_sub_section_id')

        if instance.user != user:
            raise serializers.ValidationError("You do not have permission to update this inventory detail.")

        if inventory_item_data:
            InventoryItemSerializer().update(instance.inventory_item, inventory_item_data)

        if instance.sub_sub_section.id != sub_sub_section_id:
            sub_sub_section = WarehouseSubSubSection.objects.get(id=sub_sub_section_id, user=user)
            instance.sub_sub_section = WarehouseSubSubSection.objects.get(id=sub_sub_section_id)

        instance.quantity = validated_data.get('quantity', instance.quantity)
        
        instance.save()
        return instance




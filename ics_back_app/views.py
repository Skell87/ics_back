from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from itertools import product
from rest_framework.views import APIView

from .models import *
from .serializers import *

# for profiles.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    serialzer = ProfileSerializer(profile, many=False)
    return Response(serialzer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_user(request):
    print ('request here', request)
    if request.user.is_staff:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)



# -------------------------------------------------------------------------
# item views::::::::::::::::::::

# use this or the bottom, whichever works
# new stuff
# @api_view(['POST'])
# @permission_classes([])
# def add_inventory_items(request):
    
#         serializer = InventoryItemSerializer(data=request.data)
#         # serializer.is_valid()
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# saves inventory items to the back
# @api_view(['POST'])
# @permission_classes([])
# def add_inventory_items(request):
#     item_data = {
#         'name': request.data.get('name'),
#         'make': request.data.get('make'),
#         'model': request.data.get('model'),
#         'color': request.data.get('color'),
#         'notes': request.data.get('notes'),
#     }
#     quantity = request.data.get('quantity')

#     item_serializer = InventoryItemSerializer(data=item_data)
#     if item_serializer.is_valid():
#         item_instance = item_serializer.save()

#         details_data = {
#             'sub_sub_section': request.data.get('subsubsection'),  # Adjust this based on your logic
#             'inventory_item': item_instance.id,
#             'quantity': quantity,
#         }
#         details_serializer = InventoryDetailSerializer(data=details_data)
#         if details_serializer.is_valid():
#             details_serializer.save()
#             return Response(item_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             item_instance.delete()  # Rollback if details creation fails
#             return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# gets inventory items from the back to the front
# @api_view(['GET'])
# @permission_classes([])
# def get_inventory_items(requst):
#     items = InventoryDetails.objects.select_related('inventory_item', 'sub_sub_section', 'sub_sub_section__sub_section', 'sub_sub_section__sub_section__section').all
#     serializer = InventoryDetailSerializer(items, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([])
def inventory_detail_list(request):
    if request.method == 'GET':
        print("Request data:", request.data)
        inventory_details = InventoryDetails.objects.all()
        
        serializer = InventoryDetailSerializer(inventory_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        print('INVENTORY DETAIL LIST: POST: REQUEST: ', request.data)
        # sss = WarehouseSubSubSection.objects.get(pk=request.data['sub_sub_section'])
        # sub_section = WarehouseSubSection.objects.get(pk = sss.sub_section.pk)
        # section = WarehouseSection.objects.get(pk=sub_section.section.pk)
        # section_dict = {
        #     'name': section.name
        # }
        # sub_section_dict = {
        #     'name': sub_section.name,
        #     'section': section_dict
        # }
        # sss_dict = {
        #     'name': sss.name,
        #     'sub_section': sub_section_dict
        # }
        # print('BLAMMO: SSS: ', sss_dict)

        # data = {
        #     'quantity': request.data['quantity'],
        #     'sub_sub_section': sss_dict,
        #     'inventory_item': request.data['inventory_item']
        # }

        serializer = InventoryDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('INVENTORY DETAIL LIST: ERROR: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['DELETE'])
# @permission_classes([])
# def delete_inventory_item(request, pk):
#     try:
#         inventory_item = InventoryDetails.objects.get(pk=pk)
#     except InventoryDetails.DoesNotExist:
#         return Response({"error": "Quantity to delete exceeds available quantity"}, status=status.HTTP_400_BAD_REQUEST)
    
#     serializer = DeleteInventoryItemSerializer(data=request.data)
#     if serializer.is_valid():
#         quantity_to_delete = serializer.validated_data['quantity_to_delete']
#         if quantity_to_delete > inventory_item.quantity:
#             return Response({'error': "quantity to delete exceeds available quantity"}, status=status.HTTP_400_BAD_REQUEST)
        
#         inventory_item.quantity -= quantity_to_delete
#         if inventory_item.quantity == 0:
#             inventory_item.delete()
#         else:
#             inventory_item.save()
        
#         return Response({'message': 'Inventory item updated successfully'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([])
def delete_inventory_item(request, pk):
    try:
        inventory_item = InventoryDetails.objects.get(pk=pk)
    except InventoryDetails.DoesNotExist:
        return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    quantity_to_delete = request.data.get('quantity_to_delete')
    if quantity_to_delete is None:
        return Response({"error": "quantity_to_delete field is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        quantity_to_delete = int(quantity_to_delete)
        if quantity_to_delete <= 0:
            return Response({"error": "quantity_to_delete must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity_to_delete > inventory_item.quantity:
            return Response({"error": "Quantity to delete exceeds available quantity"}, status=status.HTTP_400_BAD_REQUEST)
        
        inventory_item.quantity -= quantity_to_delete
        if inventory_item.quantity <= 0:
            inventory_item.delete()
        else:
            inventory_item.save()
        
        return Response({'message': 'Inventory item updated successfully'}, status=status.HTTP_200_OK)
    
    except ValueError:
        return Response({"error": "quantity_to_delete must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)



# ====================================================================================================
# these are currently for populating the dropdowns.
@api_view(['POST', 'GET'])
@permission_classes([])
def add_warehouse_section(request):
    if request.method == 'GET':
        sections = WarehouseSection.objects.all()
        serializer = WarehouseSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print("Received POST request data:", request.data)
        serializer = WarehouseSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([])
def add_warehouse_sub_section(request):
    section_id = request.query_params.get('section_id')
    if not section_id:
        return Response({'error': 'section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    subsections = WarehouseSubSection.objects.filter(section_id=section_id)
    serializer = WarehouseSubSectionSerializer(subsections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([])
def add_warehouse_sub_sub_section(request):
    sub_section_id = request.query_params.get('sub_section_id')
    if not sub_section_id:
        return Response({'error': 'sub_section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    subsubsections = WarehouseSubSubSection.objects.filter(sub_section_id=sub_section_id)
    serializer = WarehouseSubSubSectionSerializer(subsubsections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

# @api_view(['GET'])
# def get_inventory_details(request):
#     inventory_details = InventoryDetails.objects.all()
#     serializer = InventoryDetailSerializer(inventory_details, many=True)
#     return Response(serializer.data)
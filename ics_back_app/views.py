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



@api_view(['GET', 'POST'])
@permission_classes([])
def inventory_detail_list(request):
    if request.method == 'GET':
        print("Request data:", request.data)
        inventory_details = InventoryDetails.objects.all()
        
        serializer = InventoryDetailReadSerializer(inventory_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        print('INVENTORY DETAIL LIST: POST: REQUEST: ', request.data)
        serializer = InventoryDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('INVENTORY DETAIL LIST: ERROR: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
    if request.method == 'GET':
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
    

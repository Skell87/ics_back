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

# original working version with staff
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def register_user(request):
#     print ('request here', request)
#     if request.user.is_staff:
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([])
def register_user(request):  
    try:
        # create a user
        user = User.objects.create(
            username = request.data['username']
        )
        user.set_password(request.data['password'])
        user.save()
    except Exception as er:
        print('OH NO!  OH NO! ', er)
        user.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)

    print('BLAMMO!  USER: ', user.username)
    print('BLAMMO: REQUEST: ', request.data)
    # create a profile and attach it to the user!
    try:
        profile_data = {
            'user': user.id,
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'email': request.data['email']
        }
        profile_data_serializer = ProfileSerializer(data=profile_data)
        if profile_data_serializer.is_valid():
            profile_data_serializer.save()

            return Response(profile_data_serializer.data, status=status.HTTP_201_CREATED)

        else:
            user.delete()
            return Response(profile_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print('THERE HAS BEEN A TERRIBLE ERROR: ', e)



# original working
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def inventory_detail_list(request):
#     if request.method == 'GET':
#         print("Request data:", request.data)
#         inventory_details = InventoryDetails.objects.all()
        
#         serializer = InventoryDetailReadSerializer(inventory_details, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         print('INVENTORY DETAIL LIST: POST: REQUEST: ', request.data)
#         serializer = InventoryDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print('INVENTORY DETAIL LIST: ERROR: ', serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def inventory_detail_list(request):
    # user = request.user  # Access the user from the request
    if request.method == 'GET':
        print("Request data:", request.data)
        # Only fetch inventory details that belong to the logged-in user
        inventory_details = InventoryDetails.objects.filter(user=request.user)
        serializer = InventoryDetailReadSerializer(inventory_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        print('INVENTORY DETAIL LIST: POST: REQUEST: ', request.data)
        # Ensure new inventory details are associated with the logged-in user
        serializer = InventoryDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Save with the user attached
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('INVENTORY DETAIL LIST: ERROR: ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

# original working
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_inventory_item(request, pk):
#     try:
#         inventory_item = InventoryDetails.objects.get(pk=pk)
#     except InventoryDetails.DoesNotExist:
#         return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     quantity_to_delete = request.data.get('quantity_to_delete')
#     if quantity_to_delete is None:
#         return Response({"error": "quantity_to_delete field is required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         quantity_to_delete = int(quantity_to_delete)
#         if quantity_to_delete <= 0:
#             return Response({"error": "quantity_to_delete must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if quantity_to_delete > inventory_item.quantity:
#             return Response({"error": "Quantity to delete exceeds available quantity"}, status=status.HTTP_400_BAD_REQUEST)
        
#         inventory_item.quantity -= quantity_to_delete
#         if inventory_item.quantity <= 0:
#             inventory_item.delete()
#         else:
#             inventory_item.save()
        
#         return Response({'message': 'Inventory item updated successfully'}, status=status.HTTP_200_OK)
    
#     except ValueError:
#         return Response({"error": "quantity_to_delete must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_inventory_item(request, pk):
    user = request.user  # Access the user from the request
    try:
        # Ensure that only inventory items belonging to the logged-in user are accessible
        inventory_item = InventoryDetails.objects.get(pk=pk, user=user)
    except InventoryDetails.DoesNotExist:
        return Response({"error": "Inventory item not found or not accessible"}, status=status.HTTP_404_NOT_FOUND)
    
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_inventory_item(request, pk):
    print('update info:', request.data)
    try:
        inventory_detail = InventoryDetails.objects.get(pk=pk, user=request.user)
    except InventoryDetails.DoesNotExist:
        return Response({'error': 'Inventory detail not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = InventoryDetailUpdateSerializer(inventory_detail, data=request.data, context={'user': request.user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================================================================================================
# these are currently for populating the dropdowns.

# original working
# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# def add_warehouse_section(request):
#     if request.method == 'GET':
#         sections = WarehouseSection.objects.all()
#         serializer = WarehouseSectionSerializer(sections, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         print("Received POST request data:", request.data)
#         serializer = WarehouseSectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def add_warehouse_section(request):
    user = request.user
    if request.method == 'GET':
        # Filter sections to only those belonging to the authenticated user
        sections = WarehouseSection.objects.filter(user=user)
        serializer = WarehouseSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        print("Received POST request data:", request.data)
        # Include the user in the POST data before passing to the serializer
        serializer = WarehouseSectionSerializer(data={**request.data, 'user': user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# original working 
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def add_warehouse_sub_section(request):
#     if request.method == 'GET':
#         section_id = request.query_params.get('section_id')
#         if not section_id:
#             return Response({'error': 'section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         subsections = WarehouseSubSection.objects.filter(section_id=section_id)
#         serializer = WarehouseSubSectionSerializer(subsections, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         serializer = WarehouseSubSectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_warehouse_sub_section(request):
    # user = request.user
    if request.method == 'GET':
        section_id = request.query_params.get('section_id')
        if not section_id:
            return Response({'error': 'section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure subsections are fetched for the user's own sections
        subsections = WarehouseSubSection.objects.filter(section_id=section_id, user=request.user)
        serializer = WarehouseSubSectionSerializer(subsections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Include user in the POST data before passing to the serializer
        # This assumes the 'section' field already contains 'section_id' and 'user' is the owner of that section
        serializer = WarehouseSubSectionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# original working
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def add_warehouse_sub_sub_section(request):
#     if request.method == 'GET':
#         sub_section_id = request.query_params.get('sub_section_id')
#         if not sub_section_id:
#             return Response({'error': 'sub_section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         subsubsections = WarehouseSubSubSection.objects.filter(sub_section_id=sub_section_id)
#         serializer = WarehouseSubSubSectionSerializer(subsubsections, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method =='POST':
#         serializer = WarehouseSubSubSectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_warehouse_sub_sub_section(request):
    # user = request.user
    if request.method == 'GET':
        sub_section_id = request.query_params.get('sub_section_id')
        if not sub_section_id:
            return Response({'error': 'sub_section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure subsubsections are fetched for sub_sections owned by the user
        subsubsections = WarehouseSubSubSection.objects.filter(sub_section_id=sub_section_id, user=request.user)
        serializer = WarehouseSubSubSectionSerializer(subsubsections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Include user in the POST data before passing to the serializer
        # This assumes the 'sub_section' field already contains 'sub_section_id' and 'user' is the owner of that subsection
        serializer = WarehouseSubSubSectionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# original working
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_warehouse_section(request, section_id):
#     # section_id = request.query_params.get('section_id')
#     # if not section_id:
#     #     return Response({'error': 'section_id is required'}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         section = WarehouseSection.objects.get(pk=section_id)
#         section.delete()
#         return Response({'message': 'Section deleted successfully'}, status=status.HTTP_200_OK)
#     except WarehouseSection.DoesNotExist:
#         return Response({'error', 'section not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_warehouse_section(request, section_id):
    user = request.user
    try:
        # Ensure the section to delete is owned by the authenticated user
        section = WarehouseSection.objects.get(pk=section_id, user=user)
        section.delete()
        return Response({'message': 'Section deleted successfully'}, status=status.HTTP_200_OK)
    except WarehouseSection.DoesNotExist:
        return Response({'error': 'Section not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

# original working
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_warehouse_sub_section(request, sub_section_id):
#     print('id:', sub_section_id)
#     try:
#         subsection = WarehouseSubSection.objects.get(pk=sub_section_id)
#         subsection.delete()
#         return Response({'message': 'SubSection deleted successfully'}, status=status.HTTP_200_OK)
#     except WarehouseSubSection.DoesNotExist:
#         return Response({'error', 'sub section not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_warehouse_sub_section(request, sub_section_id):
    user = request.user
    try:
        # Ensure the subsection to delete is owned by the authenticated user
        subsection = WarehouseSubSection.objects.get(pk=sub_section_id, user=user)
        subsection.delete()
        return Response({'message': 'SubSection deleted successfully'}, status=status.HTTP_200_OK)
    except WarehouseSubSection.DoesNotExist:
        return Response({'error': 'Sub section not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

# original working
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_warehouse_sub_sub_section(request, sub_sub_section_id):
#     try:
#         subsubsection = WarehouseSubSubSection.objects.get(pk=sub_sub_section_id)
#         subsubsection.delete()
#         return Response({'message': 'SubSubSection deleted successfully'}, status=status.HTTP_200_OK)
#     except WarehouseSubSubSection.DoesNotExist:
#         return Response({'error', 'sub sub section not found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_warehouse_sub_sub_section(request, sub_sub_section_id):
    user = request.user
    try:
        # Ensure the subsubsection to delete is owned by the authenticated user
        subsubsection = WarehouseSubSubSection.objects.get(pk=sub_sub_section_id, user=user)
        subsubsection.delete()
        return Response({'message': 'SubSubSection deleted successfully'}, status=status.HTTP_200_OK)
    except WarehouseSubSubSection.DoesNotExist:
        return Response({'error': 'Sub sub section not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def register_warehouse(request):
#     if request.user.is_staff:
#         print('request data', request.data)
#         serializer = WarehouseSerializer(data=request.data)
        
#         if serializer.is_valid():
#             warehouse = serializer.save()

#             divisions = Division.objects.filter(warehouse=warehouse)
#             division_ranges = [(d.name, range(1, d.count + 1)) for d in divisions]
#             print('division reanges', division_ranges)

#             combinations = product(*[[(name, i) for i in r] for name, r in division_ranges])
#             result = list(combinations)
#             print('combinations', result)

#             locations = []
#             for combination in combinations:
#                 location_str = ', '.join([f'{name} {i}' for name, i in combination])
#                 locations.append(WarehouseLocation(warehouse=warehouse, location = location_str))
#             # this print comes up empty 
#             print('locations', locations)

#             WarehouseLocation.objects.bulk_create(locations)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

# -------------------------------------------------------------------------
# new stuff
@api_view(['POST'])
@permission_classes([])
def add_inventory_items(request):
    
        serializer = InventoryItemSerializer(data=request.data)
        # serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




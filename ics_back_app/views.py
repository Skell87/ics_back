from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets

from .models import *
from .serializers import *

# for profiles.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = request.profile
    serialzer = ProfileSerializer(profile, many=False)
    return Response(serialzer.data)

from rest_framework import serializers
from.models import *


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = '__all__'
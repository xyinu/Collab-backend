from rest_framework import serializers
from .models import User
from django.utils import timezone, dateformat
from django.db.models import Q

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
from rest_framework import serializers
from .models import User, UserAccess
from django.utils import timezone, dateformat
from django.db.models import Q
from django.core.mail import send_mail

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CreateAccessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAccess
        fields = ['email', 'access']
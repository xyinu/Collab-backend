from rest_framework import serializers
from .models import User, UserAccess, Task, Ticket, Thread
from django.utils import timezone, dateformat
from django.db.models import Q
from django.core.mail import send_mail

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class AccessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAccess
        fields = ['email', 'access']

class TaskSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.last_name')
    prof= serializers.CharField(source='prof.last_name')
    class Meta:
        model = Task
        fields = ['id','date', 'TA', 'prof', 'title', 'details', 'dueDate', 'status']

class TicketSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.last_name')
    prof= serializers.CharField(source='prof.last_name')
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'title', 'details', 'category', 'severity', 'status']

class ThreadSerializer(serializers.ModelSerializer):
    by = serializers.CharField(source='by.last_name')
    ticketTitle= serializers.CharField(source='Ticket.title')
    class Meta:
        model = Thread
        fields = ['date', 'by', 'ticketTitle', 'details',]
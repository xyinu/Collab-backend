from rest_framework import serializers
from .models import User, Task, Ticket, Thread, StudentGroup, Group,Student, Course
from django.utils import timezone, dateformat
from django.db.models import Q
from django.core.mail import send_mail

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class TaskSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.first_name')
    prof= serializers.CharField(source='prof.first_name')
    class Meta:
        model = Task
        fields = ['id','date', 'TA', 'prof', 'title', 'details', 'dueDate', 'status']

class ThreadSerializer(serializers.ModelSerializer):
    by = serializers.CharField(source='by.last_name')
    ticketTitle= serializers.CharField(source='Ticket.title')
    class Meta:
        model = Thread
        fields = ['id', 'date', 'by', 'ticketTitle', 'details',]
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['name','VMS']

class ClassSerializer(serializers.ModelSerializer):
    student=StudentSerializer()

    class Meta:
        model = StudentGroup
        fields = ['student']

class GroupSerializer(serializers.ModelSerializer):
    group_code=serializers.CharField(source='code')
    students=ClassSerializer(source='group',many=True)
    class Meta:
        model = Group
        fields = ['type','group_code','students']

class CourseSerializer(serializers.ModelSerializer):
    group = GroupSerializer(source='course_group',many=True)

    class Meta:
        model = Course
        fields = ['code', 'name','group']

class TicketSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.first_name')
    prof= serializers.CharField(source='prof.first_name')
    student=StudentSerializer()
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'student','title', 'details', 'category', 'severity', 'status']

class ThreadSerializer(serializers.ModelSerializer):
    by=serializers.CharField(source='by.first_name')
    class Meta:
        model = Thread
        fields = ['by', 'details', 'date']

class TicketThreadSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.first_name')
    prof= serializers.CharField(source='prof.first_name')
    student=StudentSerializer()
    thread = ThreadSerializer(source='ticket_thread',many=True)
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'student','title', 'details', 'category', 'severity', 'status','thread']
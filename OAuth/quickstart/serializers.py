from rest_framework import serializers
from .models import User, Task, Ticket, Thread, StudentGroup, Group,Student, Course, FAQ
from django.utils import timezone, dateformat
from django.db.models import Q

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class TaskSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
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
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
    student=StudentSerializer()
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'student','title', 'details', 'category', 'severity', 'status','final_comment']

class ThreadSerializer(serializers.ModelSerializer):
    by=serializers.CharField(source='by.name')
    type=serializers.CharField(source='by.user_type')
    class Meta:
        model = Thread
        fields = ['by', 'type','details', 'date']

class TicketThreadSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
    student=StudentSerializer()
    thread = ThreadSerializer(source='ticket_thread',many=True)
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'student','title', 'details', 'category', 'severity', 'status','thread','upload','final_comment']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id','title', 'details', 'date']
from rest_framework import serializers
from .models import User, Task, Ticket, Thread, StudentGroup, Group,Student, Course, FAQ, TaskThread
from django.utils import timezone, dateformat
from django.db.models import Q

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

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
    students=ClassSerializer(source='group_student',many=True)
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

class TaskThreadSerializer(serializers.ModelSerializer):
    by=serializers.CharField(source='by.name')
    type=serializers.CharField(source='by.user_type')
    class Meta:
        model = TaskThread
        fields = ['by', 'type','details', 'date']

class TaskSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
    thread = TaskThreadSerializer(source='task_thread',many=True)

    class Meta:
        model = Task
        fields = ['id','date', 'TA', 'prof', 'title', 'details', 'dueDate', 'status','thread']
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

class GroupDetailSerializer(serializers.ModelSerializer):
    course_code=serializers.CharField(source='course_code.code')
    class Meta:
        model=Group
        fields = ['code','type','course_code']
class StudentGroupSerializer(serializers.ModelSerializer):
    group=GroupDetailSerializer()
    class Meta:
        model=StudentGroup
        fields = ['group']

class StudentDetailsSerializer(serializers.ModelSerializer):
    group_course=StudentGroupSerializer(source='student_group',many=True)

    class Meta:
        model=Student
        fields = ['name','VMS','program_year','student_type','course_type','nationality','group_course']
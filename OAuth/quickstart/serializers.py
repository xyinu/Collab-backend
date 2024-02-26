from rest_framework import serializers
from .models import User, Task, TAGroup,Ticket, Thread, StudentGroup, Group,Student, Course, FAQ, TaskThread, TicketCategory, FAQCategory
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

class TicketSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
    student=StudentSerializer()
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'student','title', 'details', 'category', 'severity', 'status']

class ThreadSerializer(serializers.ModelSerializer):
    by=serializers.CharField(source='by.name')
    type=serializers.CharField(source='by.user_type')
    email=serializers.CharField(source='by.email')

    class Meta:
        model = Thread
        fields = ['by', 'type','details', 'date','file_name','id','email']

class TaskThreadSerializer(serializers.ModelSerializer):
    by=serializers.CharField(source='by.name')
    type=serializers.CharField(source='by.user_type')
    email=serializers.CharField(source='by.email')

    class Meta:
        model = TaskThread
        fields = ['by', 'type','details', 'date','file_name','id','email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id','title', 'details', 'date','category']

class GroupDetailSerializer(serializers.ModelSerializer):
    course_code=serializers.CharField(source='course_code.code')
    class Meta:
        model=Group
        fields = ['code','type','course_code']

class TAGroupSerializer(serializers.ModelSerializer):
    details=GroupDetailSerializer(source='group')
    class Meta:    
        model=TAGroup
        fields=['details']
    
class TASerializer(serializers.ModelSerializer):
    group=TAGroupSerializer(source='group_TA',many=True)
    class Meta:
        model = User
        fields = ['name','email','group']

class TaskSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
    thread = TaskThreadSerializer(source='task_thread',many=True)
    group=GroupDetailSerializer()
    class Meta:
        model = Task
        fields = ['id','date', 'TA', 'prof', 'title', 'details', 'dueDate', 'status','thread','file_name','group']

class TicketThreadSerializer(serializers.ModelSerializer):
    TA = serializers.CharField(source='TA.name')
    prof= serializers.CharField(source='prof.name')
    student=StudentSerializer()
    thread = ThreadSerializer(source='ticket_thread',many=True)
    group=GroupDetailSerializer()
    class Meta:
        model = Ticket
        fields = ['id','date', 'TA', 'prof', 'student','title', 'details', 'category', 'severity', 'status','thread','file_name','group']
class StudentGroupSerializer(serializers.ModelSerializer):
    group=GroupDetailSerializer()
    class Meta:
        model=StudentGroup
        fields = ['group']

class TicketDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Ticket
        fields = ['title','status','category']
class StudentDetailsSerializer(serializers.ModelSerializer):
    group_course=StudentGroupSerializer(source='student_group',many=True)
    tickets=TicketDetailSerializer(source='Ticket_student',many=True)
    class Meta:
        model=Student
        fields = ['id','name','VMS','program_year','student_type','course_type','nationality','group_course','tickets']

class StudentDetailsSerializerTA(serializers.ModelSerializer):
    group_course=StudentGroupSerializer(source='student_group',many=True)
    tickets=TicketDetailSerializer(source='Ticket_student',many=True)
    class Meta:
        model=Student
        fields = ['id','name','VMS','program_year','group_course','tickets']

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=TicketCategory
        fields = ['category']

class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=FAQCategory
        fields = ['category']

class ClassSerializer(serializers.ModelSerializer):
    student=StudentDetailsSerializer()

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

class GetGroupSerializer(serializers.ModelSerializer):
    group_code=serializers.CharField(source='code')
    cour_code=serializers.CharField(source='course_code.code')
    class Meta:
        model = Group
        fields = ['type','group_code','cour_code']
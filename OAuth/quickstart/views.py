from .serializers import UserCreateSerializer,  TaskSerializer, TicketSerializer, ThreadSerializer, ClassSerializer, CourseSerializer, TicketThreadSerializer
from django.shortcuts import render, redirect
from .models import Student, StudentGroup, Task, Thread, Ticket, FAQ, Course, Group, User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import pandas as pd 
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.


class getUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user=request.user
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)
    
# class getTAs(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
        
#         serializer = UserCreateSerializer(user)
#         return Response(serializer.data)

# class getProf(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user=request.user
#         serializer = UserCreateSerializer(user)
#         return Response(serializer.data)
class login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # user=request.user
        # user.name=request.auth['name']
        # user.save()
        User.objects.create_superuser('admin@gmail.com','admin','admin')
        return Response({"success":f"successfully signed up for {request.auth['name']}"})
    
class getClass(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        course=Course.objects.all()
        serializer=CourseSerializer(course,many=True)
        return Response(serializer.data)

class createClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        excel_file = request.FILES['file']
        df= pd.read_excel(excel_file,header=None)
        course_code=df.iloc[2][0].split()[1]
        class_type=df.iloc[3][0].split()[2]
        [current_course, created]=Course.objects.get_or_create(code=course_code,name=request.data['course_name'])

        i=0
        tempgroup=''
        while(i<len(df)):
            if(isinstance(df.iloc[i][0], str) and df.iloc[i][0].startswith('Class Group:')):
                [tempgroup,created]=Group.objects.get_or_create(code=df.iloc[i][0].split()[2],type=class_type,course_code=current_course)
            if(isinstance(df.iloc[i][0], str) and df.iloc[i][0].startswith('No.')):
                i+=1
                while(i<len(df) and not pd.isna(df.iloc[i][0])):
                    value=df.iloc[i]
                    student_type='Exchange'
                    program_year=None
                    
                    if('Exchange' not in value[2]):
                        program_year=value[2].split()[0]
                        student_type=value[2].split()[1]
                    [student, created]=Student.objects.get_or_create(
                        VMS=value[5],
                        name=value[1],
                        program_year=program_year,
                        student_type=student_type,
                        course_type=value[3],
                        nationality=value[4]
                        )
                    StudentGroup.objects.get_or_create(
                        group=tempgroup,
                        student=student
                    )
                    i+=1
            i+=1
        return Response({'success':'success'})
    
class createAccess(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return
        # [access,created]=UserAccess.objects.get_or_create(email=request.data['email'], access=request.data['access'])
        # prof=User.objects.get(email=request.data['prof'])
        # ta=request.data['ta']
        # #need send email
        # try:
        #     send_mail(
        #         'sign up for TA collaboration service',
        #         f'Dear {ta}, you have been allocated by {prof.last_name}, please click on link to sign up ...',
        #         'hello@account.com',
        #         ['igc21.xunyi@gmail.com'],
        #     )
        # except Exception as error:
        #     print(error)
        #     return Response({'failure':'sending of email fail'})
        # if(created):
        #     return Response({'success':'created and emailed'})
        # else:
        #     return Response({'success':'already created, emailed again'})

class getTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task=Task.objects.all().filter(prof=request.user)
        serializer = TaskSerializer(task,many=True)
        return Response(serializer.data)
    
class createTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ta=User.objects.get(email=request.data['ta'])
        task=Task.objects.create(prof=request.user, 
                                 TA=ta, 
                                 date=timezone.now(), 
                                 title=request.data['title'], 
                                 details=request.data['details'],
                                 dueDate=request.data['dueDate'],
                                 status="ongoing")
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request):
        task=Task.objects.get(id=request.data['id'])
        task.title=request.data['title']
        task.details=request.data['details']
        task.dueDate=request.data['dueDate']
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    
class completeTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        task=Task.objects.get(id=request.data['id'])
        task.status='completed'
        serializer = TaskSerializer(task)
        return Response(serializer.data)

class getTicket(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ticket=Ticket.objects.all().filter(TA=request.user)
        serializer = TicketSerializer(ticket,many=True)
        return Response(serializer.data)
    
class getTicketWithThread (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ticket=Ticket.objects.all().filter(TA=request.user)
        serializer = TicketThreadSerializer(ticket,many=True)
        return Response(serializer.data)

class createTicket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prof=User.objects.get(email=request.data['prof'])
        student=Student.objects.get(VMS=request.data['student'])
        task=Ticket.objects.create(prof=prof, 
                                 TA=request.user, 
                                 date=timezone.now(), 
                                 title=request.data['title'], 
                                 details=request.data['details'],
                                 category=request.data['category'],
                                 severity=request.data['severity'],
                                 student=student,
                                 status="ongoing")
        serializer = TicketSerializer(task)
        return Response(serializer.data)

    def put(self, request):
        ticket=Ticket.objects.get(id=request.data['id'])
        ticket.title=request.data['title']
        ticket.details=request.data['details']
        ticket.category=request.data['category']
        ticket.severity=request.data['severity']
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    
class completeTicket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        ticket=Ticket.objects.get(id=request.data['id'])
        ticket.status='completed'
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    
class getThread(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, id):
        ticket=Ticket.objects.get(id=id)
        thread=Thread.objects.all().filter(Ticket=ticket)
        serializer = ThreadSerializer(thread,many=True)
        return Response(serializer.data)
    
class createThread(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        ticket=Ticket.objects.get(id=request.data['id'])
        thread=Thread.objects.create( 
                                 by=request.user, 
                                 date=timezone.now(), 
                                 details=request.data['details'],
                                 Ticket=ticket,
                                 )
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request):
        thread=Thread.objects.get(id=request.data['id'])
        thread.details=request.data['details']
        thread.save()
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)


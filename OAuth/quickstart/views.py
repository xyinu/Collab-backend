from .serializers import FAQSerializer,StudentDetailsSerializer,UserSerializer,TaskSerializer, TicketSerializer, ThreadSerializer, TaskThreadSerializer,StudentSerializer, CourseSerializer, TicketThreadSerializer
from .models import Student, StudentGroup, Task, Thread, Ticket, FAQ, Course, Group, User, TaskThread
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import pandas as pd 
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from quickstart.func import send_ticket,send_access,send_task,send_thread,send_ticket_approve,send_completed_ticket,send_completed_task

from django_q.models import Schedule

class getUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userTA=User.objects.all().filter(user_type='TA')
        serializerTA = UserSerializer(userTA,many=True)
        userProf=User.objects.all().filter(user_type='Prof')
        serializerProf = UserSerializer(userProf,many=True)

        return Response({
            'TA':serializerTA.data,
            'prof':serializerProf.data
        })
    
class getUserType(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userType=request.user.user_type
        return Response({"type":userType})
    
class getTAs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ta=User.objects.filter(user_type='TA',name__isnull=False)
        serializer = UserSerializer(ta,many=True)
        return Response(serializer.data)

class getProf(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prof=User.objects.filter(user_type='Prof',name__isnull=False)
        serializer = UserSerializer(prof,many=True)
        return Response(serializer.data)

class getStudent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student=Student.objects.all()
        serializer = StudentDetailsSerializer(student,many=True)
        return Response(serializer.data)
        
class login(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        if(not user.name):
            user.name=request.auth['name']
            user.save()
            return Response({"success":f"Successfully signed up for {request.auth['name']}"})
        else:
            return Response({"success":f"Already signed up for {request.auth['name']}"})

    
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
        current_course=Course.objects.filter(code=course_code).first()
        if(not current_course):
            current_course=Course.objects.create(code=course_code,name=request.data['course_name'])

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
                    student=Student.objects.filter(VMS=value[5]).first()
                    if(not student):
                        student=Student.objects.create(
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
        [user,created]=User.objects.get_or_create(email=request.data['email'], user_type=request.data['access'])
        prof=request.user
        #need send email
        Schedule.objects.create(
            func="quickstart.func.send_access",
            kwargs={"name": f"{prof.name}","email":f"{request.data['email']}"},
            name="send email to TA for access",
            schedule_type=Schedule.ONCE,
            next_run=timezone.now(),
        )
        if(created):
            return Response({'success':'created and emailed'})
        else:
            return Response({'success':'already created, emailed again'})

class getTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task=Task.objects.all().filter(prof=request.user, status='ongoing').order_by('date')
        if(task):
            serializer = TaskSerializer(task,many=True)
            return Response(serializer.data)
        else:
            task=Task.objects.all().filter(TA=request.user, status='ongoing').order_by('date')
            serializer = TaskSerializer(task,many=True)
            return Response(serializer.data)
        
class getCompletedTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task=Task.objects.all().filter(prof=request.user, status='completed').order_by('date')
        if(task):
            serializer = TaskSerializer(task,many=True)
            return Response(serializer.data)
        else:
            task=Task.objects.all().filter(TA=request.user, status='completed').order_by('date')
            serializer = TaskSerializer(task,many=True)
            return Response(serializer.data)
    
class createTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tas=request.data.getlist('tas[]')
        file=None
        if 'file' in request.FILES:
            file = request.FILES['file']

        for ta in tas:
            User_Ta=User.objects.get(email=ta)
            Task.objects.create(prof=request.user, 
                                    TA=User_Ta, 
                                    date=timezone.now(), 
                                    title=request.data['title'], 
                                    details=request.data['details'],
                                    dueDate=request.data['dueDate'],
                                    upload=file,
                                    status="ongoing"),
            Schedule.objects.create(
            func="quickstart.func.send_task",
            kwargs={"title": f"{request.data['title']}",
                    "Prof":f"{request.user.name}",
                    "details":f"{request.data['details']}",
                    "dueDate":f"{request.data['dueDate']}",
                    "email":f"{User_Ta.email}"},
            name="send email for task",
            schedule_type=Schedule.ONCE,
            next_run=timezone.now(),
            )
        return Response({"success":"success"})

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
        task.save()
        Schedule.objects.create(
            func="quickstart.func.send_completed_task",
            kwargs={"title": f"{task.title}",
                    "Prof":f"{task.prof.name}",
                    "details":f"{task.details}",
                    "dueDate":f"{task.dueDate}",
                    "email":f"{task.prof.email}",
                    "TA":f"{request.user.name}"
            },
            name="send email for completed task",
            schedule_type=Schedule.ONCE,
            next_run=timezone.now(),
            )
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
class reopenTicket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        ticket=Ticket.objects.get(id=request.data['id'])
        ticket.status=request.user.name
        ticket.save()
        thread=Thread.objects.create( 
                            by=request.user, 
                            date=timezone.now(), 
                            details=request.data['comment'],
                            Ticket=ticket,
                            )
        Schedule.objects.create(
                func="quickstart.func.send_completed_ticket",
                kwargs={"title": f"{ticket.title}",
                        "TA":f"{ticket.TA.name}",
                        "student":f"{ticket.student.name}",
                        "category":f"{ticket.category}",
                        "severity":f"{ticket.severity}",
                        "details":f"{ticket.details}",
                        "email":f"{ticket.TA.email}",
                        "Prof":f"{request.user.name}",
                        "comment":f"{request.data['comment']}"
                        },
                name="send email for approved ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        return Response({"success":"success"})
    
class getTicketWithThread (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ticket=Ticket.objects.all().filter(Q(prof=request.user)& ~Q(status='completed')).order_by('date')
        if(ticket):
            serializer = TicketThreadSerializer(ticket,many=True)
            return Response(serializer.data)
        else:
            ticket=Ticket.objects.all().filter(Q(TA=request.user)& ~Q(status='completed')).order_by('date')
            serializer = TicketThreadSerializer(ticket,many=True)
            return Response(serializer.data)

class getCompletedTicketWithThread (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ticket=Ticket.objects.all().filter(Q(prof=request.user) & Q(status='completed')).order_by('date')
        if(ticket):
            serializer = TicketThreadSerializer(ticket,many=True)
            return Response(serializer.data)
        else:
            ticket=Ticket.objects.all().filter(Q(TA=request.user) & Q(status='completed')).order_by('date')
            serializer = TicketThreadSerializer(ticket,many=True)
            return Response(serializer.data)
        
class createTicket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prof=User.objects.get(email=request.data['prof'])
        student=Student.objects.get(VMS=request.data['student'])
        file=None
        if 'file' in request.FILES:
            file = request.FILES['file']
        ticket=Ticket.objects.create(prof=prof, 
                                 TA=request.user, 
                                 date=timezone.now(), 
                                 title=request.data['title'], 
                                 details=request.data['details'],
                                 category=request.data['category'],
                                 severity=request.data['severity'],
                                 student=student,
                                 upload=file,
                                 status=request.user.name)
        Schedule.objects.create(
            func="quickstart.func.send_ticket_approve",
            kwargs={"title": f"{request.data['title']}",
                    "TA":f"{request.user.name}",
                    "student":f"{student.name}",
                    "category":f"{request.data['category']}",
                    "severity":f"{request.data['severity']}",
                    "details":f"{request.data['details']}",
                    "email":f"{prof.email}",
                    "id":f"{ticket.pk}"
                    },
            name="send email for ticket approval",
            schedule_type=Schedule.ONCE,
            next_run=timezone.now(),
        )
        serializer = TicketSerializer(ticket)
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
        ticket.final_comment=request.data['comment']
        ticket.save()
        Schedule.objects.create(
                func="quickstart.func.send_completed_ticket",
                kwargs={"title": f"{ticket.title}",
                        "TA":f"{ticket.TA.name}",
                        "student":f"{ticket.student.name}",
                        "category":f"{ticket.category}",
                        "severity":f"{ticket.severity}",
                        "details":f"{ticket.details}",
                        "email":f"{ticket.TA.email}",
                        "Prof":f"{request.user.name}",
                        "comment":f"{request.data['comment']}"
                        },
                name="send email for approved ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        return Response({'response':'Successfully complete ticket'})

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
        ticket=Ticket.objects.get(id=request.data['id'])
        ticket.status=request.user.name
        ticket.save()
        thread=Thread.objects.create( 
                                 by=request.user, 
                                 date=timezone.now(), 
                                 details=request.data['details'],
                                 Ticket=ticket,
                                 )
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_thread",
                kwargs={
                        "by":f"{request.user.name}",
                        "ticket":f"{ticket.title}",
                        "details":f"{request.data['details']}",
                        "email":f"{ticket.prof.email}"},
                name="send email for ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        else:
            Schedule.objects.create(
                func="quickstart.func.send_thread",
                kwargs={
                        "by":f"{request.user.name}",
                        "ticket":f"{ticket.title}",
                        "details":f"{request.data['details']}",
                        "email":f"{ticket.TA.email}"},
                name="send email for ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request):
        thread=Thread.objects.get(id=request.data['id'])
        thread.details=request.data['details']
        thread.save()
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

class createTaskThread(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task=Task.objects.get(id=request.data['id'])
        thread=TaskThread.objects.create( 
                                 by=request.user, 
                                 date=timezone.now(), 
                                 details=request.data['details'],
                                 Task=task,
                                 )
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_task_thread",
                kwargs={
                        "by":f"{request.user.name}",
                        "ticket":f"{task.title}",
                        "details":f"{request.data['details']}",
                        "email":f"{task.prof.email}"},
                name="send email for ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        else:
            Schedule.objects.create(
                func="quickstart.func.send_task_thread",
                kwargs={
                        "by":f"{request.user.name}",
                        "ticket":f"{task.title}",
                        "details":f"{request.data['details']}",
                        "email":f"{task.TA.email}"},
                name="send email for ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        serializer = TaskThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request):
        thread=Thread.objects.get(id=request.data['id'])
        thread.details=request.data['details']
        thread.save()
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

class count(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        ticket=Ticket.objects.all().filter(prof=request.user)
        if(ticket):
            ticketbyuser=Ticket.objects.all().filter(Q(prof=request.user) & Q(status=request.user.name)).count()
            ticketbyother=Ticket.objects.all().filter(Q(prof=request.user) & ~Q(status=request.user.name) & ~Q(status='completed')).count()
            ticketcompleted=Ticket.objects.all().filter(Q(prof=request.user)  & Q(status='completed')).count()
            taskcompleted=Task.objects.all().filter(prof=request.user, status='completed').count()
            taskongoing=Task.objects.all().filter(Q(prof=request.user) & ~Q(status='completed')).count()  
            return Response({
                'ticket':[ticketbyuser,ticketbyother,ticketcompleted],
                'task':[taskongoing,taskcompleted]
            })      
        else:
            ticketbyuser=Ticket.objects.all().filter(Q(TA=request.user) & Q(status=request.user.name)).count()
            ticketbyother=Ticket.objects.all().filter(Q(TA=request.user) & ~Q(status=request.user.name) & ~Q(status='completed')).count()
            ticketcompleted=Ticket.objects.all().filter(Q(TA=request.user) & Q(status='completed')).count()
            taskcompleted=Task.objects.all().filter(TA=request.user, status='completed').count()
            taskongoing=Task.objects.all().filter(Q(TA=request.user) & ~Q(status='completed')).count()
            return Response({
                'ticket':[ticketbyuser,ticketbyother,ticketcompleted],
                'task':[taskongoing,taskcompleted]
            })
        
class Faq(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        faqs=FAQ.objects.all()
        serializer=FAQSerializer(faqs, many=True)
        return Response(serializer.data)
    def put(self, request):

        faq=FAQ.objects.get(id=request.data['id'])
        if(request.data.get('details')):
            faq.details=request.data['details']
        if(request.data.get('title')):
            faq.title=request.data['title']
        faq.date=timezone.now()
        faq.save()
        return Response({'success':'success'})
    
    def post(self, request):
        faq=FAQ.objects.create(title=request.data['title'], details=request.data['details'])
        return Response({'success':'success'})
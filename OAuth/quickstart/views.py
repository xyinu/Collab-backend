from .serializers import GetGroupSerializer,TASerializer,StudentDetailsSerializerTA,FAQSerializer,TicketCategorySerializer,FAQCategorySerializer,StudentDetailsSerializer,UserSerializer,TaskSerializer, TicketSerializer, ThreadSerializer, TaskThreadSerializer,StudentSerializer, CourseSerializer, TicketThreadSerializer
from .models import Student, StudentGroup, TAGroup,FAQCategory,TicketCategory,Task, Thread, Ticket, FAQ, Course, Group, User, TaskThread
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
import pandas as pd 
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from quickstart.func import send_ticket,send_access,send_task,send_thread,send_ticket_approve,send_completed_ticket,send_completed_task
from quickstart.management.azure_file_controller import download_blob, upload_file_to_blob
from django_q.models import Schedule
from pathlib import Path
import mimetypes
from django.http import HttpResponse
from django.db.models import Count
   
class getUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userTA=User.objects.all().filter(user_type='TA')
        serializerTA = TASerializer(userTA,many=True)
        
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
        email=request.user.email
        return Response({"type":userType,"email":email})
    
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

class addStudent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        groups=request.data.getlist('groups[]')
        check=Student.objects.filter(VMS=request.data['VMS'])
        if(check):
            return Response({'error':'VMS already exists'},status=status.HTTP_400_BAD_REQUEST)
        student=Student.objects.create(
            VMS=request.data['VMS'],
            name=request.data['name'],
            program_year=request.data['program_year'],
            student_type=request.data['student_type'],
            course_type=request.data['course_type'],
            nationality=request.data['nationality']
        )
        for group in groups:
            split=group.split()
            cur=Group.objects.get(course_code_id=split[0], code=split[1], type=split[2])
            StudentGroup.objects.create(group=cur, student=student)

        serializer = StudentDetailsSerializer(student)
        return Response(serializer.data)
    
class editStudent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student=Student.objects.get(id=request.data['id'])
        if(request.data.get('VMS')):
            student.VMS=request.data['VMS']
        if(request.data.get('name')):
            student.name=request.data['name']
        if(request.data.get('program_year')):
            student.program_year=request.data['program_year']
        if(request.data.get('student_type')):
            student.student_type=request.data['student_type']
        if(request.data.get('course_type')):
            student.course_type=request.data['course_type']
        if(request.data.get('nationality')):
            student.nationality=request.data['nationality']
        student.save()
        studentGroups=StudentGroup.objects.filter(student=student)
        groups=request.data.getlist('groups[]')
        for group in groups:
            split=group.split()
            cur=Group.objects.get(course_code_id=split[0], code=split[1], type=split[2])
            check=StudentGroup.objects.filter(group=cur, student=student).first()
            if(not check):
                new=StudentGroup.objects.create(group=cur, student=student)
                studentGroups=studentGroups.exclude(pk=new.pk)
            else:
                studentGroups=studentGroups.exclude(pk=check.pk)
        for i in studentGroups:
            i.delete()
        return Response({'success':'success'})

class getGroups(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if(request.user.user_type=='TA'):
            groups=Group.objects.filter(group_Ta__TA=request.user)
            serializer=GetGroupSerializer(groups,many=True)
            return Response(serializer.data)
        else:
            groups=Group.objects.all()
            serializer=GetGroupSerializer(groups,many=True)
            return Response(serializer.data)
    
class getStudent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if(request.user.user_type=='TA'):
            tagroups=Group.objects.filter(group_Ta__TA=request.user)
            student=Student.objects.filter(student_group__group__in=tagroups).prefetch_related('student_group','Ticket_student').order_by('id')
            serializer = StudentDetailsSerializerTA(student,many=True)
            return Response(serializer.data)
        else:
            student=Student.objects.all().prefetch_related('student_group','Ticket_student').order_by('id')
            serializer = StudentDetailsSerializer(student,many=True)
            return Response(serializer.data)
    
class getStudentTrunc(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student=Student.objects.all()
        serializer = StudentSerializer(student,many=True)
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
        course=Course.objects.all().prefetch_related('course_group__group_student__student','course_group__group_student__group')
        serializer=CourseSerializer(course,many=True)
        return Response(serializer.data)
    
class editClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        students=request.data['students']
        course=Course.objects.filter(code=request.data['course_code']).first()
        group=Group.objects.filter(code=request.data['group_code'],course_code=course).first()
        for i in students:
            student=Student.objects.filter(VMS=i).first()
            StudentGroup.objects.create(student=student,group=group)

        return Response({'success':'success'})

class deleteClass(APIView):

    def post(self, request):
        students=request.data['students']
        course=Course.objects.filter(code=request.data['course_code']).first()
        group=Group.objects.filter(code=request.data['group_code'],course_code=course).first()
        for i in students:
            student=Student.objects.filter(VMS=i).first()
            stugroup=StudentGroup.objects.filter(student=student,group=group).first()
            stugroup.delete()

        return Response({'success':'success'})
    
class createClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        excel_file = request.FILES['file']
        df= pd.read_excel(excel_file,header=None,engine='openpyxl')
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

class deleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email=request.data['email']
        user=User.objects.get(email=email)
        user.delete()
        return Response({'success':'success'})

class editAccess(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        groups=request.data.getlist('group[]')
        user=User.objects.filter(email=request.data['email']).first()
        existing=TAGroup.objects.filter(TA=user)
        for i in groups:
            split=i.split()
            cur=Group.objects.get(course_code_id=split[0], code=split[1], type=split[2])
            check=TAGroup.objects.filter(TA=user,group=cur).first()
            if(not check):
                newTAGroup=TAGroup.objects.create(TA=user,group=cur)
                existing=existing.exclude(pk=newTAGroup.pk)
            else:
                existing=existing.exclude(pk=check.pk)
        for i in existing:
            i.delete()
        return Response({'success':'success'})


class createAccess(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        groups=request.data.getlist('group[]')
        email=request.data['email']
        if(request.data['access']=='Prof'):
            hold=request.data['email'].split('@')
            email=hold[0]+'@staff.main.'+hold[1]
        [user,created]=User.objects.get_or_create(email=email, send=request.data['email'],user_type=request.data['access'])
        if(request.data['access']=='TA'):
            for i in groups:
                split=i.split()
                cur=Group.objects.get(course_code_id=split[0], code=split[1], type=split[2])
                check=TAGroup.objects.filter(TA=user,group=cur)
                if(not check):
                    TAGroup.objects.create(TA=user,group=cur)
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
        task=Task.objects.all().filter(Q(prof=request.user) & ~Q(status='completed')).order_by('date')
        if(task):
            serializer = TaskSerializer(task,many=True)
            return Response(serializer.data)
        else:
            task=Task.objects.all().filter(Q(TA=request.user) & ~Q(status='completed')).order_by('date')
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
    
class downloadTaskFile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        task = Task.objects.filter(pk=request.data['id']).first()
        file_name = task.file_name
        file_type, _ = mimetypes.guess_type(file_name)
        url = task.url
        blob_name = url.split("/")[-1]
        blob_content = download_blob(blob_name)
        if blob_content:
            response = HttpResponse(blob_content.readall(), content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        return Response({"fail","fail"})

class createTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tas=request.data.getlist('tas[]')
        split=request.data['group'].split()
        cur=Group.objects.get(course_code_id=split[0], code=split[1], type=split[2])
        file=None
        if 'file' in request.FILES:
            file = request.FILES['file']
            url = upload_file_to_blob(file)
        for ta in tas:
            User_Ta=User.objects.get(email=ta)
            task=Task.objects.create(prof=request.user, 
                                    TA=User_Ta, 
                                    date=timezone.now(), 
                                    title=request.data['title'], 
                                    details=request.data['details'],
                                    dueDate=request.data['dueDate'],
                                    group=cur,
                                    status=request.user.name)
            if 'file' in request.FILES:
                task.url=url
                task.file_name = file.name
                task.save()
            Schedule.objects.create(
            func="quickstart.func.send_task",
            kwargs={"title": f"{request.data['title']}",
                    "Prof":f"{request.user.name}",
                    "details":f"{request.data['details']}",
                    "dueDate":f"{request.data['dueDate']}",
                    "email":f"{User_Ta.send}"},
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
        thread=TaskThread.objects.create( 
                            by=request.user, 
                            date=timezone.now(), 
                            details=request.data['comment'],
                            Task=task,
                            )
        task.save()
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_completed_task",
                kwargs={"title": f"{task.title}",
                        "Prof":f"{task.prof.name}",
                        "details":f"{task.details}",
                        "dueDate":f"{task.dueDate}",
                        "email":f"{task.prof.send}",
                        "TA":f"{request.user.name}",
                        "comment":f"{request.data['comment']}"
                },
                name="send email for completed task",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
                )
        else:
            Schedule.objects.create(
                func="quickstart.func.send_completed_task",
                kwargs={"title": f"{task.title}",
                        "Prof":f"{task.prof.name}",
                        "details":f"{task.details}",
                        "dueDate":f"{task.dueDate}",
                        "email":f"{task.TA.send}",
                        "TA":f"{request.user.name}",
                        "comment":f"{request.data['comment']}"
                },
                name="send email for completed task",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
                )
        serializer = TaskSerializer(task)
        return Response(serializer.data)

class reopenTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        task=Task.objects.get(id=request.data['id'])
        task.status=request.user.name
        task.save()
        thread=TaskThread.objects.create( 
                            by=request.user, 
                            date=timezone.now(), 
                            details=request.data['comment'],
                            Task=task,
                            )
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_reopen_task",
                kwargs={"title": f"{task.title}",
                        "Prof":f"{task.prof.name}",
                        "details":f"{task.details}",
                        "dueDate":f"{task.dueDate}",
                        "email":f"{task.prof.send}",
                        "TA":f"{request.user.name}",
                        "comment":f"{request.data['comment']}"
                },
                name="send email for reopened task ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        else:
            Schedule.objects.create(
                    func="quickstart.func.send_reopen_task",
                    kwargs={"title": f"{task.title}",
                            "Prof":f"{task.prof.name}",
                            "details":f"{task.details}",
                            "dueDate":f"{task.dueDate}",
                            "email":f"{task.TA.send}",
                            "TA":f"{request.user.name}",
                            "comment":f"{request.data['comment']}"
                    },
                    name="send email for reopened task ticket",
                    schedule_type=Schedule.ONCE,
                    next_run=timezone.now(),
                )
        return Response({"success":"success"})

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
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_reopen_ticket",
                kwargs={"title": f"{ticket.title}",
                        "TA":f"{ticket.TA.name}",
                        "student":f"{ticket.student.name}",
                        "category":f"{ticket.category}",
                        "severity":f"{ticket.severity}",
                        "details":f"{ticket.details}",
                        "email":f"{ticket.prof.send}",
                        "Prof":f"{request.user.name}",
                        "comment":f"{request.data['comment']}"
                        },
                name="send email for approved ticket",
                schedule_type=Schedule.ONCE,
                next_run=timezone.now(),
            )
        else:
            Schedule.objects.create(
                    func="quickstart.func.send_reopen_ticket",
                    kwargs={"title": f"{ticket.title}",
                            "TA":f"{ticket.TA.name}",
                            "student":f"{ticket.student.name}",
                            "category":f"{ticket.category}",
                            "severity":f"{ticket.severity}",
                            "details":f"{ticket.details}",
                            "email":f"{ticket.TA.send}",
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
        ticket=Ticket.objects.all().filter((Q(prof=request.user) |Q(TA=request.user))& ~Q(status='completed')).order_by('date')
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

class downloadFile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        ticket = Ticket.objects.filter(pk=request.data['id']).first()
        file_name = ticket.file_name
        file_type, _ = mimetypes.guess_type(file_name)
        url = ticket.url
        blob_name = url.split("/")[-1]
        blob_content = download_blob(blob_name)
        if blob_content:
            response = HttpResponse(blob_content.readall(), content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        return Response({"fail","fail"})
    
class downloadThreadFile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        thread = Thread.objects.filter(pk=request.data['id']).first()
        file_name = thread.file_name
        file_type, _ = mimetypes.guess_type(file_name)
        url = thread.url
        blob_name = url.split("/")[-1]
        blob_content = download_blob(blob_name)
        if blob_content:
            response = HttpResponse(blob_content.readall(), content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        return Response({"fail","fail"})
    
class downloadTaskThreadFile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        thread = TaskThread.objects.filter(pk=request.data['id']).first()
        file_name = thread.file_name
        file_type, _ = mimetypes.guess_type(file_name)
        url = thread.url
        blob_name = url.split("/")[-1]
        blob_content = download_blob(blob_name)
        if blob_content:
            response = HttpResponse(blob_content.readall(), content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        return Response({"fail","fail"})

class createTicket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prof=User.objects.get(email=request.data['prof'])
        student=Student.objects.get(VMS=request.data['student'])
        split=request.data['group'].split()
        cur=Group.objects.get(course_code_id=split[0], code=split[1], type=split[2])
        ticket=Ticket.objects.create(prof=prof, 
                                 TA=request.user, 
                                 date=timezone.now(), 
                                 title=request.data['title'], 
                                 details=request.data['details'],
                                 category=request.data['category'],
                                 severity=request.data['severity'],
                                 student=student,
                                 group=cur,
                                 status=request.user.name)
        file=None
        if 'file' in request.FILES:
            file = request.FILES['file']
            url = upload_file_to_blob(file)
            if not url:
                return Response({'fail':'fail'})
            ticket.url=url
            ticket.file_name = file.name
            ticket.save()
        Schedule.objects.create(
            func="quickstart.func.send_ticket_approve",
            kwargs={"title": f"{request.data['title']}",
                    "TA":f"{request.user.name}",
                    "student":f"{student.name}",
                    "category":f"{request.data['category']}",
                    "severity":f"{request.data['severity']}",
                    "details":f"{request.data['details']}",
                    "email":f"{prof.send}",
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
        thread=Thread.objects.create( 
                                 by=request.user, 
                                 date=timezone.now(), 
                                 details=request.data['comment'],
                                 Ticket=ticket,
                                 )
        ticket.status='completed'
        ticket.save()
        Schedule.objects.create(
                func="quickstart.func.send_completed_ticket",
                kwargs={"title": f"{ticket.title}",
                        "TA":f"{ticket.TA.name}",
                        "student":f"{ticket.student.name}",
                        "category":f"{ticket.category}",
                        "severity":f"{ticket.severity}",
                        "details":f"{ticket.details}",
                        "email":f"{ticket.TA.send}",
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
        file=None
        if 'file' in request.FILES:
            file = request.FILES['file']
            url = upload_file_to_blob(file)
            if not url:
                return Response({'fail':'fail'})
            thread.url=url
            thread.file_name = file.name
            thread.save()
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_thread",
                kwargs={
                        "by":f"{request.user.name}",
                        "ticket":f"{ticket.title}",
                        "details":f"{request.data['details']}",
                        "email":f"{ticket.prof.send}"},
                name="send email for thread",
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
                        "email":f"{ticket.TA.send}"},
                name="send email for thread",
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
        file=None
        if 'file' in request.FILES:
            file = request.FILES['file']
            url = upload_file_to_blob(file)
            if not url:
                return Response({'fail':'fail'})
            thread.url=url
            thread.file_name = file.name
            thread.save()
        if(request.user.user_type=='TA'):
            Schedule.objects.create(
                func="quickstart.func.send_task_thread",
                kwargs={
                        "by":f"{request.user.name}",
                        "ticket":f"{task.title}",
                        "details":f"{request.data['details']}",
                        "email":f"{task.prof.send}"},
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
                        "email":f"{task.TA.send}"},
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
        ticketbyuser=Ticket.objects.all().filter((Q(prof=request.user) |Q(TA=request.user)) & Q(status=request.user.name)).count()
        ticketbyother=Ticket.objects.all().filter((Q(prof=request.user) |Q(TA=request.user)) & ~Q(status=request.user.name) & ~Q(status='completed')).count()
        ticketcompleted=Ticket.objects.all().filter((Q(prof=request.user) |Q(TA=request.user))  & Q(status='completed')).count()
        taskcompleted=Task.objects.all().filter((Q(prof=request.user) |Q(TA=request.user)) &Q(status='completed')).count()
        taskbyuser=Task.objects.all().filter((Q(prof=request.user) |Q(TA=request.user)) & Q(status=request.user.name)).count()
        taskbyother=Task.objects.all().filter((Q(prof=request.user) |Q(TA=request.user)) & ~Q(status=request.user.name) & ~Q(status='completed')).count()
        return Response({
            'ticket':[ticketbyuser,ticketbyother,ticketcompleted],
            'task':[taskbyuser,taskbyother,taskcompleted]
        })      
        
class Faq(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        faqs=FAQ.objects.all().order_by('-date')
        serializer=FAQSerializer(faqs, many=True)
        return Response(serializer.data)
    def put(self, request):

        faq=FAQ.objects.get(id=request.data['id'])
        if(request.data.get('details')):
            faq.details=request.data['details']
        if(request.data.get('title')):
            faq.title=request.data['title']
        if(request.data.get('category')):
            faq.category=request.data['category']
        faq.date=timezone.now()
        faq.save()
        return Response({'success':'success'})
    
    def post(self, request):
        faq=FAQ.objects.create(title=request.data['title'], details=request.data['details'], category=request.data['category'])
        return Response({'success':'success'})

class DeleteFaq(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        faq=FAQ.objects.get(id=request.data['id'])
        faq.delete()
        return Response({"success":"success"})

class TicketCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        category=TicketCategory.objects.all()
        serializer=TicketCategorySerializer(category,many=True)
        return Response(serializer.data)
        

    def post(self, request):
        category=category=TicketCategory.objects.filter(
            category=request.data['category']
        ).first()
        if(request.data['category']=='' or category):
            return Response({'error':'already created'})
        
        category=TicketCategory.objects.create(
            category=request.data['category']
        )
        serializer=TicketCategorySerializer(category)
        return Response(serializer.data)

class FAQCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        category=FAQCategory.objects.all()
        serializer=FAQCategorySerializer(category,many=True)
        return Response(serializer.data)
        

    def post(self, request):
        category=category=FAQCategory.objects.filter(
            category=request.data['category']
        ).first()
        if(request.data['category']=='' or category):
            return Response({'error':'already created'})
        category=FAQCategory.objects.create(
            category=request.data['category']
        )
        serializer=FAQCategorySerializer(category)
        return Response(serializer.data)
    
class data(APIView):
 
    def get(self, request):    
        category= TicketCategory.objects.all()
        ticketCategoryLabel=[]
        ticketCategoryCount=[]
        for i in category:
            tick=Ticket.objects.filter(category=i.category).count()
            ticketCategoryLabel.append(i.category)
            ticketCategoryCount.append(tick)
        course= Course.objects.all()
        ticketCourseCount=[]
        ticketCourseLabel=[]
        taskCourseCount=[]
        taskCourseLabel=[]
        for i in course:
            group=Group.objects.filter(course_code=i.code)
            tickcount=0
            taskcount=0
            for k in group:
                tick=Ticket.objects.filter(group=k).count()
                tickcount+=tick
                task=Task.objects.filter(group=k).count()
                taskcount+=task
            ticketCourseCount.append(tickcount)
            ticketCourseLabel.append(i.code)
            taskCourseCount.append(taskcount)
            taskCourseLabel.append(i.code)
        group=Group.objects.all()
        ticketGroupCount=[]
        ticketGroupLabel=[]
        taskGroupCount=[]
        taskGroupLabel=[]
        for i in group:
            tick=Ticket.objects.filter(group=i).count()
            ticketGroupLabel.append(f"{i.course_code}, {i.code}, {i.type}")
            ticketGroupCount.append(tick)
            task=Task.objects.all().filter(group=i).count()
            taskGroupLabel.append(f"{i.course_code}, {i.code}, {i.type}")
            taskGroupCount.append(task)
        students=Student.objects.filter(Ticket_student__isnull=False).annotate(num=Count('Ticket_student')).order_by('-num').distinct()
        studentCount=[]
        studentLabel=[]
        count=0
        for i in students:
            if(count==5):
                break
            count+=1
            tick=Ticket.objects.filter(student=i).count()
            studentCount.append(tick)
            studentLabel.append(i.name)
        
        return Response({
            'ticket':{
                'Category':{
                    'label':ticketCategoryLabel,
                    'count':ticketCategoryCount
                },
                'Course':{
                    'label':ticketCourseLabel,
                    'count':ticketCourseCount
                },
                'Group':{
                    'label':ticketGroupLabel,
                    'count':ticketGroupCount
                },
                'Student':{
                    'label':studentLabel,
                    'count':studentCount
                }
            },
            'task':{
                'Course':{
                    'label':taskCourseLabel,
                    'count':taskCourseCount
                },
                'Group':{
                    'label':taskGroupLabel,
                    'count':taskGroupCount
                }
            }
        })

            
        
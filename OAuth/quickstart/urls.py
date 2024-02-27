from django.urls import path
from .views import getUser, editAccess,data,getGroups,downloadTaskThreadFile,downloadThreadFile,deleteUser,reopenTask,addStudent,editStudent,downloadFile,downloadTaskFile,DeleteFaq,getStudentTrunc,deleteClass,editClass,TicketCategoryView,FAQCategoryView,reopenTicket,Faq,getUserType,createClass, createTaskThread,login, createAccess, createTask, createTicket, createThread, completeTask,completeTicket,getTask,getClass,getThread, getTicketWithThread,getProf,getStudent,getTAs, getCompletedTask, getCompletedTicketWithThread,count

app_name = 'quickstart'

urlpatterns = [
    path('user/', getUser.as_view(), name='getUser'),
    path('usertype/', getUserType.as_view(), name='getUserType'),
    path('class/', getClass.as_view(), name='getClass'),
    path('createclass/', createClass.as_view(), name='createClass'),
    path('editclass/', editClass.as_view(), name='editClass'),
    path('deleteclass/', deleteClass.as_view(), name='deleteClass'),
    path('deleteuser/', deleteUser.as_view(), name='deleteUser'),
    path('login/', login.as_view(), name='login'),
    path('createaccess/', createAccess.as_view(), name='createAccess'),
    path('editaccess/', editAccess.as_view(), name='editAccess'),
    path('task/', getTask.as_view(), name='getTask'),
    path('completedtask/', getCompletedTask.as_view(), name='getCompletedTask'),
    path('createtask/', createTask.as_view(), name='createTask'),
    path('completetask/', completeTask.as_view(), name='completeTask'),
    path('completedticket/', getCompletedTicketWithThread.as_view(), name='getCompletedTicketWithThread'),
    path('ticketthread/', getTicketWithThread.as_view(), name='getTicketThread'),
    path('createticket/', createTicket.as_view(), name='createTicket'),
    path('completeticket/', completeTicket.as_view(), name='completeTicket'),
    path('reopenticket/', reopenTicket.as_view(), name='reopenTicket'),
    path('reopentask/', reopenTask.as_view(), name='reopenTask'),
    path('thread/<id>', getThread.as_view(), name='getThread'),
    path('createthread/', createThread.as_view(), name='createThead'),
    path('createtaskthread/', createTaskThread.as_view(), name='createTaskThead'),
    path('prof/', getProf.as_view(), name='getProf'),
    path('student/', getStudent.as_view(), name='getStudent'),
    path('addstudent/',addStudent.as_view(),name='addstudent'),
    path('editstudent/', editStudent.as_view(),name='editStudent'),
    path('studenttrunc/', getStudentTrunc.as_view(), name='getStudentTrunc'),
    path('ta/', getTAs.as_view(), name='getTAs'),
    path('count/',count.as_view(),name='count'),
    path('faq/',Faq.as_view(),name='faq'),
    path('deletefaq/',DeleteFaq.as_view(),name='deletefaq'),
    path('ticketcategory/',TicketCategoryView.as_view(),name='ticketcategory'),
    path('faqcategory/',FAQCategoryView.as_view(),name='faqcategory'),
    path('downloadfile/',downloadFile.as_view(),name='downloadfile'),
    path('downloadthreadfile/',downloadThreadFile.as_view(),name='downloadThreadFile'),
    path('downloadtaskfile/',downloadTaskFile.as_view(),name='downloadTaskFile'),
    path('downloadtaskthreadfile/',downloadTaskThreadFile.as_view(),name='downloadTaskThreadFile'),
    path('group/', getGroups.as_view(), name='getGroups'),
    path('data/', data.as_view(), name='data'),
    ]


        # course=Course.objects.all()
        # hold=[]
        # for i in course:
        #     each={}
        #     each['code']=i.code
        #     group=Group.objects.filter(course_code=i)
        #     holdGroup=[]
        #     for j in group:
        #         studentgroups=StudentGroup.objects.filter(group=j).select_related('student')
        #         holdstudents=[]
        #         for students in studentgroups:
        #             tickets=Ticket.objects.filter(student__pk=students.pk).only('title','status','category')
        #             tickethold=[]
        #             for tick in tickets:
        #                 tickethold.append({
        #                     'title':tick.title,
        #                     'status':tick.status,
        #                     'category':tick.category
        #                 })
        #             groupstudents=StudentGroup.objects.filter(student=students.student).select_related('group')
        #             groupshold=[]
        #             for grouping in groupstudents:
        #                 groupshold.append({
        #                     'code':grouping.group.code,
        #                     'type':grouping.group.type,
        #                     'course_code':grouping.group.course_code.code
        #                 })

        #             holdstudents.append({
        #                 'id':students.student.id,
        #                 'name':students.student.name,
        #                 'VMS':students.student.VMS,
        #                 'program_year':students.student.program_year,
        #                 'group_course':groupshold,
        #                 'tickets':tickethold
        #             })
        #         GroupDict={
        #             'type':j.type,
        #             'group_code':j.code,
        #             'name':j.name,
        #             'students':holdstudents
        #         }
        #         holdGroup.append(GroupDict)
        #     hold.append({
        #         'group':holdGroup,
        #         'code':i.code
        #     })
        # return Response(hold)
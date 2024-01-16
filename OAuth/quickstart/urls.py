from django.urls import path
from .views import getUser, downloadFile,downloadTaskFile,DeleteFaq,getStudentTrunc,deleteClass,editClass,TicketCategoryView,FAQCategoryView,reopenTicket,Faq,getUserType,createClass, createTaskThread,login, createAccess, createTask, createTicket, createThread, completeTask,completeTicket,getTask,getClass,getThread, getTicketWithThread,getProf,getStudent,getTAs, getCompletedTask, getCompletedTicketWithThread,count

app_name = 'quickstart'

urlpatterns = [
    path('user/', getUser.as_view(), name='getUser'),
    path('usertype/', getUserType.as_view(), name='getUserType'),
    path('class/', getClass.as_view(), name='getClass'),
    path('createclass/', createClass.as_view(), name='createClass'),
    path('editclass/', editClass.as_view(), name='editClass'),
    path('deleteclass/', deleteClass.as_view(), name='deleteClass'),
    path('login/', login.as_view(), name='login'),
    path('createaccess/', createAccess.as_view(), name='createAccess'),
    path('task/', getTask.as_view(), name='getTask'),
    path('completedtask/', getCompletedTask.as_view(), name='getCompletedTask'),
    path('createtask/', createTask.as_view(), name='createTask'),
    path('completetask/', completeTask.as_view(), name='completeTask'),
    path('completedticket/', getCompletedTicketWithThread.as_view(), name='getCompletedTicketWithThread'),
    path('ticketthread/', getTicketWithThread.as_view(), name='getTicketThread'),
    path('createticket/', createTicket.as_view(), name='createTicket'),
    path('completeticket/', completeTicket.as_view(), name='completeTicket'),
    path('reopenticket/', reopenTicket.as_view(), name='reopenTicket'),
    path('thread/<id>', getThread.as_view(), name='getThread'),
    path('createthread/', createThread.as_view(), name='createThead'),
    path('createtaskthread/', createTaskThread.as_view(), name='createTaskThead'),
    path('prof/', getProf.as_view(), name='getProf'),
    path('student/', getStudent.as_view(), name='getStudent'),
    path('studenttrunc/', getStudentTrunc.as_view(), name='getStudentTrunc'),
    path('ta/', getTAs.as_view(), name='getTAs'),
    path('count/',count.as_view(),name='count'),
    path('faq/',Faq.as_view(),name='faq'),
    path('deletefaq/',DeleteFaq.as_view(),name='deletefaq'),
    path('ticketcategory/',TicketCategoryView.as_view(),name='ticketcategory'),
    path('faqcategory/',FAQCategoryView.as_view(),name='faqcategory'),
    path('downloadfile/',downloadFile.as_view(),name='downloadfile'),
    path('downloadtaskfile/',downloadTaskFile.as_view(),name='downloadtaskfile'),
    ]

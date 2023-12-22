from django.urls import path
from .views import getUser, createClass, login, createAccess, createTask, createTicket, createThread, completeTask,completeTicket,getTicket,getTask,getClass,getThread, getTicketWithThread

app_name = 'quickstart'

urlpatterns = [
    path('user/', getUser.as_view(), name='getUser'),
    path('class/', getClass.as_view(), name='getClass'),
    path('createclass/', createClass.as_view(), name='createClass'),
    path('login/', login.as_view(), name='login'),
    path('createaccess/', createAccess.as_view(), name='createAccess'),
    path('task/', getTask.as_view(), name='getTask'),
    path('createtask/', createTask.as_view(), name='createTask'),
    path('completetask/', completeTask.as_view(), name='completeTask'),
    path('ticket/', getTicket.as_view(), name='getTicket'),
    path('ticketthread/', getTicketWithThread.as_view(), name='getTicketThread'),
    path('createticket/', createTicket.as_view(), name='createTicket'),
    path('completeticket/', completeTicket.as_view(), name='completeTicket'),
    path('thread/<id>', getThread.as_view(), name='getThread'),
    path('createthread/', createThread.as_view(), name='createThead'),
]

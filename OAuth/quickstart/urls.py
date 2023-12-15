from django.urls import path
from .views import getUser, createClass, login, createAccess, createTask, createTicket, createThread, completeTask,completeTicket

app_name = 'quickstart'

urlpatterns = [
    path('user/', getUser.as_view(), name='getUser'),
    path('createclass/', createClass.as_view(), name='createClass'),
    path('login/', login.as_view(), name='login'),
    path('createaccess/', createAccess.as_view(), name='createAccess'),
    path('createtask/', createTask.as_view(), name='createTask'),
    path('completetask/', completeTask.as_view(), name='completeTask'),
    path('createticket/', createTicket.as_view(), name='createTicket'),
    path('completeticket/', completeTicket.as_view(), name='completeTicket'),
    path('createthread/', createThread.as_view(), name='createThead'),
]

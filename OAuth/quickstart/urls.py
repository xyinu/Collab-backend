from django.urls import path
from .views import getUser, createClass, login

app_name = 'quickstart'

urlpatterns = [
    path('user/', getUser.as_view(), name='getUser'),
    path('createclass/', createClass.as_view(), name='createClass'),
    path('login/', login.as_view(), name='login'),

]

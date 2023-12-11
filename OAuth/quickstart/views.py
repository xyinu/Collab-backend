from .serializers import POdetailSerializer, POSerializer, ContainerDetailSerializer, PObacklogSerializer, UserCreateSerializer, SKUSerializer
from django.shortcuts import render
from .models import Student, StudentGroup, Task, Thread, Ticket, FAQ, Course, Group
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status
# Create your views here.


class getUser(APIView):

    def get(self, request):
        user=request.user
        serializer = POSerializer(user)
        return Response(serializer.data)
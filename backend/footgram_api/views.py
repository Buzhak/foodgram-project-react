from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
from users.models import User
from users.serializers import ListUserSerializer, CreateUserSerializer


class CreateUserAndListView(APIView):
    def get(self, request): 
        users = User.objects.all()  
        serializer = ListUserSerializer(users, many=True, context=request.user)
        return Response(serializer.data)
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

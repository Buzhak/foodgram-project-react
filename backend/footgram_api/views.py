from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, generics, viewsets
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import CreateUserSerializer, DetailUserSerializer


class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        users = User.objects.all()  
        serializer = DetailUserSerializer(users, many=True, context=request.user)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = DetailUserSerializer(user)
        return Response(serializer.data) 

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        # permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):

        user = get_object_or_404(User, username=request.user)
        if request.method == 'GET':
            serializer = DetailUserSerializer(user)
            return Response(serializer.data)
        serializer = DetailUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        url_path='set_password',
        methods=['post'],
        # permission_classes=[permissions.IsAuthenticated]
    )
    def get_password(self, request):
        #нужно создать серилизатор для проверки старого и нового пароля. нужен валидатор для этого дела и если все ок запись в бд.
        pass
        # user = get_object_or_404(User, username=request.user)
        # serializer = DetailUserSerializer(
        #     user,
        #     data=request.data,
        #     partial=True
        # )
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
# from api.permissions import IsAdmin
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import AdvancedAdminSerializer, AdvancedUserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin | permissions.IsAdminUser]
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = AdvancedAdminSerializer
    lookup_field = 'username'

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):

        user = get_object_or_404(User, username=request.user)
        if request.method == 'GET':
            serializer = AdvancedUserSerializer(user)
            return Response(serializer.data)
        serializer = AdvancedUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

from core.constants import CODE_LENGTH
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Code, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class AdvancedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role', )


class AdvancedAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=CODE_LENGTH)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if Code.objects.filter(
            user=user,
            code=data['confirmation_code']
        ).exists():
            return data
        raise serializers.ValidationError('Неверные данные')

from core.constants import CODE_LENGTH
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Code, User, Follow


class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class DefaultUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(user__username=str(self.context),author__username=obj.username).exists()


# class UserCodeSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150)
#     confirmation_code = serializers.CharField(max_length=CODE_LENGTH)

#     def validate(self, data):
#         user = get_object_or_404(User, username=data['username'])
#         if Code.objects.filter(
#             user=user,
#             code=data['confirmation_code']
#         ).exists():
#             return data
#         raise serializers.ValidationError('Неверные данные')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    def validate(self, data):
        if User.objects.filter(
            username=data['username'],
            password=data['password']
        ).exists():
            return data
        raise serializers.ValidationError('Неверный логин или пароль')

from core.constants import CODE_LENGTH
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from .models import User, Follow
from .validators import not_self_subscribe


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
        '''
        Проверка подписан ли пользаователь делающий запрос на выбранного автора.
        Если запрос делает анонимный пользователь, функция будет возвращать "False".
        '''
        if self.context["request"].user.username == '':
            return False
        return Follow.objects.filter(user=self.context["request"].user,author=obj).exists()


# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=150)
#     password = serializers.CharField(max_length=150)

#     def validate(self, data):
#         if User.objects.filter(
#             email=data['email'],
#             password=data['password']
#         ).exists():
#             return data
#         raise serializers.ValidationError('Неверный email или пароль')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta():
        model = Follow
        fields = ('user', 'author')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message=_("Вы уже подписаны на этого пользователя")
            )
        ]

    def validate(self, data):
        """
        Проверка подписки на самого себя
        """
        if data['user'] == data['author']:
            raise serializers.ValidationError("Нельзя подписыватья на самого себя.")
        return data


from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions, mixins
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from rest_framework.serializers import ModelSerializer
from django.db.models import Model

from core.core import create_shopping_list
from users.models import Follow, User
from recipes.models import Recipe, Tag, Shoping_cart, Favorite
from recipes.serializers import RecipeSerializer, TagSerializer, CreateRecipeSerializer, RecipeShortSerializer, ShopingCatdSerializer, FavoriteSerializer, SubscibeUserSerializer
# from users.models import User
# from users.serializers import CreateUserSerializer, DefaultUserSerializer, LoginSerializer


# class UserViewSet(viewsets.ViewSet):

#     def list(self, request):
#         permission_classes = [permissions.AllowAny]
#         users = User.objects.all()  
#         serializer = DefaultUserSerializer(users, many=True, context=request.user)
#         return Response(serializer.data)

#     def create(self, request):
#         permission_classes = [permissions.AllowAny]
#         serializer = CreateUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED) 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk):
#         permission_classes = [permissions.AllowAny]
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = DefaultUserSerializer(user)
#         return Response(serializer.data) 

#     @action(
#         detail=False,
#         url_path='me',
#         methods=['get', 'patch'],
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def me(self, request):

#         user = get_object_or_404(User, username=request.user)
#         if request.method == 'GET':
#             serializer = DefaultUserSerializer(user)
#             return Response(serializer.data)
#         serializer = DefaultUserSerializer(
#             user,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     @action(
#         detail=False,
#         url_path='set_password',
#         methods=['post'],
#         permission_classes=[permissions.IsAuthenticated]
#     )
#     def get_password(self, request):
#         #нужно создать серилизатор для проверки старого и нового пароля. нужен валидатор для этого дела и если все ок запись в бд.
#         pass
#         # user = get_object_or_404(User, username=request.user)
#         # serializer = DetailUserSerializer(
#         #     user,
#         #     data=request.data,
#         #     partial=True
#         # )
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         # return Response(serializer.data)    

def create_cart_or_favorite(user: User, recipe: Recipe, serializer: ModelSerializer) -> Response():
    data = {'user': user.id, 'recipe': recipe.id}
    shop_cart_serializer = serializer(data=data)
    if shop_cart_serializer.is_valid():
        shop_cart_serializer.save()
        resipe_serializer = RecipeShortSerializer(recipe)
        return Response(resipe_serializer.data, status=status.HTTP_201_CREATED)
    return Response(shop_cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_cart_or_favorite(user: User, recipe: Recipe, model: Model, title: str) -> Response():
    if model.objects.filter(user=user.id, recipe=recipe.id).exists():
        model.objects.filter(user=user.id, recipe=recipe.id).delete()
        message = {'errors': f'рецепт удалён из списка {title}'}
        return Response(message ,status=status.HTTP_400_BAD_REQUEST)
    message = {'errors': f'репепт отсутствует в списке {title}'}
    return Response(message ,status=status.HTTP_400_BAD_REQUEST)


class RetriveListViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass

class OnlyListViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pass


class TagViewSet(RetriveListViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):     
    permission_classes = [permissions.AllowAny]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request):
        serializer = CreateRecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            
            reсipe = get_object_or_404(Recipe, id=serializer.data['id'])
            serializer = RecipeSerializer(reсipe)
            serializer.context['request'] = self.request
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = CreateRecipeSerializer(instance=recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        reсipe = get_object_or_404(Recipe, id=serializer.data['id'])
        serializer = RecipeSerializer(reсipe)
        serializer.context['request'] = self.request
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=True)
    def shoping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            return create_cart_or_favorite(user, recipe, ShopingCatdSerializer)
        return delete_cart_or_favorite(user, recipe, Shoping_cart, 'покупок')

    @action(detail=False)
    def download_shopping_cart(self, request):
        filename = "shoping_list.txt"
        content = create_shopping_list(request.user)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            return create_cart_or_favorite(user, recipe, FavoriteSerializer)
        return delete_cart_or_favorite(user, recipe, Favorite, 'избранного')


class SubscribeViewSet(viewsets.ViewSet):
    @action(detail=False)
    def subscriptions(self, request):
        subscriptions = Follow.objects.filter(user=request.user).values_list('author', flat=True)
        users = User.objects.filter(id__in=subscriptions)
        serializer = SubscibeUserSerializer(users, many=True)
        serializer.context['request'] = self.request

        return Response(serializer.data, status=status.HTTP_200_OK)

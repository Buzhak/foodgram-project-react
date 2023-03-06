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
from recipes.models import Recipe, Tag, Shoping_cart, Favorite, Product
from recipes.serializers import RecipeSerializer, TagSerializer, CreateRecipeSerializer, RecipeShortSerializer, ShopingCatdSerializer, FavoriteSerializer, SubscibeUserSerializer, ProductSerializer
from users.serializers import FollowSerializer
from .permissions import AuthorOrAdminOrReadOnly


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
    permission_classes = [AuthorOrAdminOrReadOnly]
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
        if request.user == recipe.author or request.user.is_staff:
            serializer = CreateRecipeSerializer(instance=recipe, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            reсipe = get_object_or_404(Recipe, id=serializer.data['id'])
            serializer = RecipeSerializer(reсipe)
            serializer.context['request'] = self.request
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = {'detail': "У вас нет прав для выполнения этой операции."}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            return create_cart_or_favorite(user, recipe, ShopingCatdSerializer)
        return delete_cart_or_favorite(user, recipe, Shoping_cart, 'покупок')

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
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
        users = User.objects.filter(following__user=self.request.user)
        serializer = SubscibeUserSerializer(users, many=True)
        serializer.context['request'] = self.request
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        if request.method == 'POST':
            data = {'user': user.id, 'author': author.id}
            print(data)
            serialzer = FollowSerializer(data=data)
            if serialzer.is_valid():
                serialzer.save()
                subscribe_serializer = SubscibeUserSerializer(author)
                subscribe_serializer.context['request'] = self.request
                return Response(subscribe_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user.id, author=author.id).exists():
            Follow.objects.filter(user=user.id, author=author.id).delete()
            message = {'errors': f'вы отписались от пользовалетя {author.username}'}
            return Response(message ,status=status.HTTP_400_BAD_REQUEST)
        message = {'errors': f'Подписки не существует'}
        return Response(message ,status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(RetriveListViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions, mixins
from django.shortcuts import get_object_or_404, get_list_or_404

from core.core import print_recipes
from recipes.models import Recipe, Tag, Shoping_cart, Ingredient
from recipes.serializers import RecipeSerializer, TagSerializer, CreateRecipeSerializer, RecipeShortSerializer, ShopingCatdSerializer
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
            data = {'user': user.id, 'recipe': recipe.id}
            shop_cart_serializer = ShopingCatdSerializer(data=data)
            if shop_cart_serializer.is_valid():
                shop_cart_serializer.save()
                resipe_serializer = RecipeShortSerializer(recipe)
                return Response(resipe_serializer.data, status=status.HTTP_201_CREATED)
            return Response(shop_cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if Shoping_cart.objects.filter(user=user.id, recipe=recipe.id).exists():
            Shoping_cart.objects.filter(user=user.id, recipe=recipe.id).delete()
            message = {'errors': 'рецепт удалён из списка покупок'}
            return Response(message ,status=status.HTTP_400_BAD_REQUEST)
        message = {'errors': 'репепт отсутствует в списке покупок'}
        return Response(message ,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False)
    def download_shopping_cart(self, request):
        print_recipes(request.user)
        message = {'response': 'держи файлик, чувак'}
        return Response(message ,status=status.HTTP_200_OK)


# class ShopingCartViewSet(viewsets.ViewSet):
#     @action(methods=['post', 'delete'], detail=True, url_path='{r_pk}/shoping_cart/')
#     def shoping_cart(self, r_pk, request):
#         if request.method=='POST':
#             recipe = get_object_or_404(Recipe, pk=r_pk) 
#             user = request.user
#             Shoping_cart.objects.create(user=user, pecipe=recipe)
#             return Response(status=status.HTTP_201_CREATED)


# class ShopingCartViewSet(viewsets.ViewSet):
    


    # def create(self, request, r_pk):
    #     recipe = get_object_or_404(Recipe, pk=r_pk)
    #     user = request.user
    #     Shoping_cart.objects.create(user=user, pecipe=recipe)
    #     return Response(status=status.HTTP_201_CREATED)

    # def delete(self, request, r_pk):
    #     recipe = get_object_or_404(Recipe, pk=pk)
    #     user = request.user
    #     Shoping_cart.objects.delete(user=user, pecipe=recipe)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)




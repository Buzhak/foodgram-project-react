import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from users.models import Follow, User
from users.serializers import DefaultUserSerializer

from .core import create_ingredients
from .models import Favorite, Ingredient, Product, Recipe, ShopingCart, Tag


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ProductSerializer(serializers.ModelSerializer):

    class Meta():
        model = Product
        fields = ('name', 'measurement_unit', 'id')


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id', read_only=True)
    name = serializers.CharField(
        source='product.name'
    )
    measurement_unit = serializers.CharField(
        source='product.measurement_unit'
    )
    amount = serializers.SerializerMethodField()

    class Meta():
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):        
        return obj.amount


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    author = DefaultUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta():
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        if self.context["request"].user.username == '':
            return False
        return Favorite.objects.filter(
            user=self.context["request"].user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context["request"].user.username == '':
            return False
        return ShopingCart.objects.filter(
            user=self.context["request"].user,
            recipe=obj
        ).exists()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta():

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = Tag
        fields = ('id')


class IngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    
    class Meta():
        model = Ingredient
        fields = ('id', 'amount')




class ShopingCatdSerializer(serializers.ModelSerializer):
    class Meta():
        model = ShopingCart
        fields = ('user', 'recipe')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShopingCart.objects.all(),
                fields=('user', 'recipe'),
                message=_("Рецепт уже добавлен в корзину покупок")
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta():
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message=_("Рецепт уже добавлен в избранное")
            )
        ]


class CreateRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientCreateSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta():
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        read_only_fields = ('id', 'author',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.tags.set(tags)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.save()
        Ingredient.objects.filter(recipe=instance).delete()
        create_ingredients(ingredients, instance)
        return instance

    def delete(self, instance):
        instance.delete()
        Ingredient.objects.filter(recipe=instance).delete()


class SubscibeUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeShortSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context["request"].user, author=obj
        ).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'measurement_unit')

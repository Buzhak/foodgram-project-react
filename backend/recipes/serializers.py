import base64
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from .models import Product, Recipe, Tag, Favorite, Shoping_cart, Ingredient, TagRecipe
from users.serializers import DefaultUserSerializer


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
        fields = ('name', 'measurement_unit')


class IngredientSerializer(serializers.ModelSerializer): 
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
        if obj.amount == 0 or obj.amount is None:
            return 'по вкусу'
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
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(user=self.context["request"].user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Shoping_cart.objects.filter(user=self.context["request"].user, recipe=obj).exists()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = Tag
        fields = ('id')


class IngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    class Meta():
        model = Ingredient
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientCreateSerializer(many=True)
    class Meta():
        model = Recipe
        fields = ('id', 'author' ,'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')
        read_only_fields = ('id', 'author',)
    
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Product, pk=ingredient['product']['id'])
            Ingredient.objects.create(
                product=current_ingredient, amount=ingredient['amount'], recipe=recipe
            )
    
        return recipe

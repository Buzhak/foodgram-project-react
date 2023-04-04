from django.shortcuts import get_object_or_404

from .models import Ingredient, Product, Recipe


def create_ingredients(ingredients: list, instance: Recipe):
    for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Product,
                pk=int(ingredient['product']['id'])
            )
            Ingredient.objects.create(
                product=current_ingredient,
                amount=ingredient['amount'],
                recipe=instance
            )

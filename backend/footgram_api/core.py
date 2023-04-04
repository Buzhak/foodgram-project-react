from django.shortcuts import get_list_or_404
from recipes.models import Ingredient, ShopingCart


def create_shopping_list(user) -> str:
    cart = ShopingCart.objects.filter(user=user)
    shopping_list = ''
    for recipe in cart:
        shopping_list += ('_' * 30 + '\n')
        shopping_list += ('' + '\n')
        shopping_list += (f'{recipe.recipe}' + '\n')
        shopping_list += ('' + '\n')
        ingredients = get_list_or_404(Ingredient, recipe=recipe.recipe)
        count = 0
        for ingredient in ingredients:
            count += 1
            shopping_list += (f'{count}. {ingredient}' + '\n')
    shopping_list += ('_' * 30 + '\n')
    return shopping_list
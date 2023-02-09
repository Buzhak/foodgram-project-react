from django.contrib import admin
from .models import Ingredient, Favorite, Product, Recipe, Shoping_cart, Tag, TagRecipe


class ChoiceInline(admin.StackedInline):
    model = Ingredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name', 'text', 'image', 'cooking_time', 'author', 'tags')}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Product)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Shoping_cart)
admin.site.register(TagRecipe)
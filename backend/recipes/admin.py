from django.contrib import admin
from .models import Ingredient, Product, Recipe, Tag


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
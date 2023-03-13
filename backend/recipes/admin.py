from django.contrib import admin
from .models import Ingredient, Favorite, Product, Recipe, Shoping_cart, Tag


class ChoiceInline(admin.StackedInline):
    model = Ingredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name', 'text', 'image', 'cooking_time', 'author', 'tags')}),
    ]
    inlines = [ChoiceInline]
    list_display = ['name', 'author', 'pub_date', 'in_favorite']
    list_filter = ['name', 'author', 'tags']

    def in_favorite(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result

    in_favorite.short_description = 'В избраном'


    class Meta:
        model = Recipe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name', 'measurement_unit']
    list_filter = []

    class Meta:
        model = Product


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['product', 'amount', 'recipe']
    list_filter = []

    class Meta:
        model = Ingredient


admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Shoping_cart)

from django.contrib import admin

from .models import Favorite, Ingredient, Product, Recipe, ShopingCart, Tag


class ChoiceInline(admin.StackedInline):
    model = Ingredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': (
            'name',
            'text',
            'image',
            'cooking_time',
            'author',
            'tags'
        )}),
    ]
    inlines = [ChoiceInline]
    list_display = ['name', 'author', 'pub_date', 'in_favorite']
    list_filter = ['name', 'author', 'tags']

    def in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    in_favorite.short_description = 'В избраном'

    class Meta:
        model = Recipe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['id', 'name', 'measurement_unit']
    list_filter = []

    class Meta:
        model = Product


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['product', 'id', 'amount', 'recipe']
    list_filter = []

    class Meta:
        model = Ingredient


admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShopingCart)

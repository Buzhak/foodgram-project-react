from django_filters import FilterSet, ModelMultipleChoiceFilter, NumberFilter
from recipes.models import Recipe, Tag


class ProductFilter(FilterSet):
    autrhor = NumberFilter(
        field_name='author__id',
        lookup_expr='exact'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = NumberFilter(method='filter_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_shopping_cart')

    def filter_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == 1:
                return queryset.filter(
                    favorites__user=self.request.user
                )
            if value == 0:
                return queryset.exclude(
                    favorites__user=self.request.user
                )
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == 1:
                return queryset.filter(
                    shopingcarts__user=self.request.user
                )
            if value == 0:
                return queryset.exclude(
                    shopingcarts__user=self.request.user
                )
        return queryset

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'tags', 'author']
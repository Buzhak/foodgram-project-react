from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, RecipeViewSet, SubscribeViewSet, TagViewSet

router_tag = SimpleRouter()
router_tag.register('', TagViewSet)
router_resipe = SimpleRouter()
router_resipe.register('', RecipeViewSet)
router_users = SimpleRouter()
router_users.register('', SubscribeViewSet, basename='subscriptions')
router_ingredients = SimpleRouter()
router_ingredients.register('', ProductViewSet, basename='ingredients')

urlpatterns = [
    path('users/', include(router_users.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('tags/', include(router_tag.urls)),
    path('recipes/', include(router_resipe.urls)),
    path('ingredients/', include(router_ingredients.urls))
]

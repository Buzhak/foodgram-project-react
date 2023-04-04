from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (ProductViewSet, RecipeViewSet, SubscribeViewSet,
                    SubscriptionsViewSet, TagViewSet)


router = SimpleRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', ProductViewSet, basename='ingredients')
router.register('users', SubscribeViewSet, basename='subscribe')
router.register(
    'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

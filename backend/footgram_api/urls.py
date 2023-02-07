
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TagViewSet, RecipeViewSet

router = SimpleRouter() 
router.register('tags', TagViewSet, basename='tags')
router.register('resipes', RecipeViewSet, basename='resipes')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)), 
]


from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TagViewSet, RecipeViewSet, SubscribeViewSet

router_tag = SimpleRouter() 
router_tag.register('tags', TagViewSet, basename='tags')
router_resipe = SimpleRouter() 
router_resipe.register('', RecipeViewSet)
router_users = SimpleRouter()
# router_users.register('users', SubscribeViewSet, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_tag.urls)),
    path('recipes/', include(router_resipe.urls))
    # path('', include(router_users.urls))
]

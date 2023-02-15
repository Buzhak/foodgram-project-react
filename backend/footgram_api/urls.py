
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TagViewSet, RecipeViewSet

router_tag = SimpleRouter() 
router_tag.register('tags', TagViewSet, basename='tags')
router_resipe = SimpleRouter() 
router_resipe.register('', RecipeViewSet)
# router_resipe.register(r'^(?P<r_pk>\d+)/shoping_cart/$', ShopingCartViewSet, basename='shoping_cart')
# router_resipe.register('', ShopingCartViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_tag.urls)),
    path('recipes/', include(router_resipe.urls))
]


from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

router = SimpleRouter() 
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
# urlpatterns = [

#     path('auth/', include('djoser.urls.authtoken')),
# ]
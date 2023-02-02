
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, Login, Logout

router = SimpleRouter() 
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', Login.as_view()),
    path('auth/logout/', Logout.as_view()),
]
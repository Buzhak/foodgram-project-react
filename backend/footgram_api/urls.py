from django.urls import include, path

from .views import CreateUserAndListView

urlpatterns = [
    path('users/', CreateUserAndListView.as_view()),
]
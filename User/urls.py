from django.urls import path

from User.views import UserRegisterView, UserLoginView

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', UserLoginView.as_view())
]

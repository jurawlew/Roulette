from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include('Game.urls')),
    path('user/', include('User.urls')),
]

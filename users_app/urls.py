from django.urls import path, include

from users_app import api_views


urlpatterns = [
    path('register/', api_views.UserCreate.as_view()),
    path('', include('django.contrib.auth.urls'))
]

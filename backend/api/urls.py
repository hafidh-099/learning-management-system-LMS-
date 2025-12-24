from api.views import myTokenObtainPairView
from django.urls import path

urlpatterns = [
    path('user/login/',myTokenObtainPairView.as_view())
]

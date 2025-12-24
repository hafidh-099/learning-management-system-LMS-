from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauth.models import CustomUser
from rest_framework.permissions import AllowAny


# Create your views here.
class myTokenObtainPairView(TokenObtainPairView): #we create view for jwt
    serializer_class = api_serializer.MyTokenObtainPairSerializer
    
class RegistrationView(generics.CreateAPIView):
    serializer_class = api_serializer.RegisterSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

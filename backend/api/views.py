from api import serializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class myTokenObtainPairView(TokenObtainPairView): #we create view for jwt
    serializer_class = serializer.MyTokenObtainPairSerializer

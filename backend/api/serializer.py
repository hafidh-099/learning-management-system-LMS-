#bcs this is baise app all serializer ("userauth",etc) come hire
from rest_framework import serializers
from userauth.models import CustomUser,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):#class and user(whho try to access or token is alredy)
        token =  super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = CustomUser
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Profile
        fields = "__all__"
#bcs this is baise app all serializer ("userauth",etc) come hire
from rest_framework import serializers
from userauth.models import CustomUser,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

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
        model = CustomUser
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Profile
        fields = "__all__"
        
#Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    #user registration field
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])#automatic validated by django
    password2 = serializers.CharField(write_only=True,required=True)
    
    class Meta:
        model = CustomUser
        fields = ['full_name','email','password','password2']
    
    def check_validation(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"Password":"password not match"})
        return data
    def create(self,validate_data):
        #email_username,_ = user.email.split("@") #Note underscore .it mean alphabet afer username i.e @
        email_user = validate_data['email'].split("@")[0]
        user = CustomUser.objects.create_user(
            username=email_user,
            full_name =validate_data['full_name'],
            email =validate_data['email'],
        )
        user.set_password = validate_data['password']
        user.save()
        return user 
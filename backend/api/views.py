import random
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauth.models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
class myTokenObtainPairView(TokenObtainPairView): #we create view for jwt
    serializer_class = api_serializer.MyTokenObtainPairSerializer
    
class RegistrationView(generics.CreateAPIView):
    serializer_class = api_serializer.RegisterSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

#Reset password

    #overite get method
def generate_random_otp(length=7):#generate random token
    otp = ''.join([str(random.randint(0,9)) for _ in range(length)])
    return otp

#send email

class PasswordResetEmailVarifyView(generics.RetrieveAPIView):
    #retrive bcs we want to get single item
    permission_classes = [AllowAny]
    #user serializer bcs we want to update user password
    serializer_class = api_serializer.UserSerializer
    
    
    def get_object(self):
        email = self.kwargs['email']#in this we get #api/v1/password-email-verify/hafid@gmail.com . so we take that email
        
        #and fetch from db
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            uuidb64 = user.pk #uuidb64 is id of user we want to validate(pk of user we got)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            
            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"
              # ✅ SEND EMAIL USING GMAIL
            send_mail(
                subject="Password Reset Link",
                message=f"Hi {user.username} \nClick the link below to reset your password:\n\n{link}",
                from_email=settings.EMAIL_HOST_USER,  # uses DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=False,
            )
        return user

#reset password now
class PasswordChangeViews(generics.CreateAPIView):
    #create new object
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer
    
    def create(self, request, *args, **kwargs):
        # request.data store information that come from frontend 
        payload = request.data #we take user infromation(otp,uuid etc) and store it into payload
        otp = payload['otp']
        #or this still same
        uuidb64 = request.data['uuidb64']
        password = payload['password']
        
        #fetch user who have that info
        user = CustomUser.objects.get(id=uuidb64,otp=otp)
        if user:
            user.set_password(password)#this password we take from frontend
            user.otp = "" #we clear otp after getting new password
            user.save()
            return Response({"message":"password change succefully"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"user dont exists"},status=status.HTTP_404_NOT_FOUND)
        
        
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
from api import models as api_model



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
        
class CategoryListView(generics.ListAPIView):
    #queryset = api_model.Category.objects.all()#note you can pass any query here
    #Example if you want to filter by someone who is active
    queryset = api_model.Category.objects.filter(active=True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]
    
class CourseListView(generics.ListAPIView):
    queryset = api_model.Course.objects.filter(platform_stauts = "Published",teacher_course_status = "Published")
    serializer_class = api_serializer.CourseSerializer 
    permission_classes = [AllowAny]
    
class CourseDetailViews(generics.RetrieveAPIView):
    #retrive is fetch only one field 
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]
    #we want to retrive course by slug name instead of id so we must overide default get
    # localhost:8000/course/1/ but instead be localhost:8000/course/react-native/
    def get_object(self):
        #grub slug from url passed(we use kwargs to catch something passed on url)
        slug = self.kwargs['slug']
        course = api_model.Course.objects.get(slug=slug,platform_stauts = "Published",teacher_course_status = "Published")
        return course
    
class CartListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.CartSerializer
    
    def get_queryset(self):
        #get cart by userid 
        cart_id = self.kwargs['cart_id']
        queryset = api_model.Cart.objects.filter(cart_id=cart_id)
        return queryset

class CartItemDeletedView(generics.DestroyAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['id']
        return api_model.Cart.objects.filter(cart_id=cart_id,id=item_id).first()
    
    
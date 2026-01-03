#bcs this is baise app all serializer ("userauth",etc) come hire
from rest_framework import serializers
from userauth.models import CustomUser,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from api import models as api_model


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
        user.set_password(validate_data['password'])
        user.save()
        return user 

class VariantItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.VariantItem

class CartOrderItemSerializer(serializers.ModelSerializer):
    # order_id =None
    # payment_status =None
    class Meta:
        fields = [
            "teacher","order","course","coupons","tax_fee","total","initial_total","saved","applied_cupon","oid","date","order_id","payment_status",
        ]
        model = api_model.CartOrderItem
        
class VariantSerializer(serializers.ModelSerializer):
    variant_items = VariantItemSerializer(many=True)
    class Meta:
        fields = [
            "course","title","variant_id","date","variant_items",
        ]
        model = api_model.Variant

class CompletedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.CompletedLesson

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Note
    
class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)
    class Meta:
        fields = [
            "course","user","review","rating","reply","date","active","profile",
                ]
        model = api_model.Review

class Question_Answer_MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Question_Answer_Message

class Question_AnswerSerializer(serializers.ModelSerializer):
    message=Question_Answer_MessageSerializer(many=True)
    profile=ProfileSerializer(many=False) #we need only one user profile
    class Meta:
        fields = [
            "course","user","title","qa_id","date","message","profile",
                ]
        model = api_model.Question_Answer

class EnrolledCourseSerializer(serializers.ModelSerializer):
    lecture = VariantItemSerializer(many=True,read_only=True)
    complete_lesson = CompletedLessonSerializer(many=True,read_only=True)
    curriculum = VariantSerializer(many=True,read_only=True)
    note = NoteSerializer(many=True,read_only=True)
    question_answer = Question_AnswerSerializer(many=True,read_only=True)
    review = ReviewSerializer(many=True,read_only=True)
    class Meta:
        fields = [
        "course","user","teacher","enrollment_id","date","order_item","lecture","complete_lesson","curriculum","note","question_answer","review",
        ]
        model = api_model.EnrolledCourse

class CourseSerializer(serializers.ModelSerializer):
    #we need to tell django to know where this field must work
    student = EnrolledCourseSerializer(many=True)#expected many student to be passed in field
    curriculum = VariantItemSerializer(many=True)
    lectures = VariantItemSerializer(many=True)
    average_rating = ReviewSerializer(many=True)
    # rating_count = ReviewSerializer(many=True)
    # reviews = ReviewSerializer(many=True)
    
    class Meta:
        fields = [
            "category","teacher","file","image","title","description","price","language","level","platform_stauts","teacher_course_status","featured","course_id","slug","date",
            #we also call all method we define in actual model
            "student","curriculum","lectures","average_rating","rating_count","reviews"
            ]
        model = api_model.Course
class CategorySerializer(serializers.ModelSerializer):
    # course_count = CourseSerializer(many=True)
    class Meta:
        fields = ["title","image","slug","course_count"]
        model = api_model.Category
        
class TeacherSerializer(serializers.ModelSerializer):
    students = CartOrderItemSerializer(many=True)
    courses = CourseSerializer(many=True)
    review = CourseSerializer(many=True)
    class Meta:
        fields = [
            "user","image","full_name","bio","facebook","twitter","linkedIn","about","country","students","courses","review",
        ]
        model = api_model.Teacher
       
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Cart


class CartOrderSerializer(serializers.ModelSerializer):
    order_items = CartOrderItemSerializer(many=True)
    class Meta:
        fields = [
                "student","teacher","sub_total","tax_fee","total","initial_total","payment_status","full_name","email","country","coupons","stripe_session_id","oid","date","saved","order_items",
                  ]
        model = api_model.CartOrder       

class CirtificateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Cirtificate

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Notification


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Coupon

class WhichlistSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Whichlist
    
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = api_model.Country
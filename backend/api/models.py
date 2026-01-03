from django.db import models
from userauth.models import CustomUser,Profile
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
# from moviepy.editor import videoFileClip
# from moviepy.editors import videoFileClip
from moviepy.video import VideoClip
import math
 
 
# Create your models here.
LANGUAGE = (
    ("English","English"),#key and value
    ("Spanish","Spanish"),
    ("French","French"),
    ("Kiswahili","Kiswahili"),
)
LEVEL = (
    ("Begginer","Begginer"),
    ("Intermidiate","Intermidiate"),
    ("Advance","Advance"),
)
#Teacher course can be either publish it,put in on draft or disabled it
TEACHER_STATUS=(
    ("Draft","Draft"),
    ("Disabled","Disabled"),
    ("Published","Published"),
)
PAYMENT_STATUS=(
    ("Processing","Processing"),
    ("Paid","Paid"),
    ("Failed","Failed")
)

#as plaftwe we can decide how course will be .Either will be accepted and pulished,puted on draft,or disabled
PLATFORM_STATUS=(
    ("Draft","Draft"),
    ("Rejected","Rejected"),
    ("Review","Review"),
    ("Disabled","Disabled"),
    ("Published","Published"),
)

RATING=(
    ("New Order","New Order"),
    ("New Review","New Review"),
    ("New Course Question","New Course Question"),
    ("New Published","New Published"),
)
NOT_TYPE = (
    (1,"1 Star"),
    (3,"2 Star"),
    (2,"3 Star"),
    (4,"4 Star"),
    (5,"5 Star"),   
)

class Teacher (models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.FileField(upload_to='course-file',blank=True,null=True,default='default.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100,null=True ,blank=True)
    facebook = models.URLField(null=True,blank=True)
    twitter = models.URLField(null=True,blank=True)
    linkedIn = models.URLField(null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.full_name
    
    # related method to model 
    
    # count student it have
    def students(self):
        return CartOrderItem.objects.filter(teacher=self) #teacher = self i.e teacher = teacher class
    
    def courses(self):
        return Course.objects.filter(teacher = self)
    
    def review(self):
        return Course.objects.filter(teacher = self).count()
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='course-file',blank=True,null=True,default='default.jpg')
    slug = models.SlugField(unique=True,null=True,blank=True)
    active = models.BooleanField(default=False)
    
    #what to appear in my admin backend
    class Meta:
        verbose_name_plural = "Category"
        ordering = ["title"]
    
    def __str__(self):
        return self.title
    
    #count course available in this category
    def course_count(self):
        return Course.objects.filter(category=self).count()
    
    def save(self,*args, **kwargs):
        if self.slug == "" or self.slug==None:
            self.slug = slugify(self.title)#eg course title is  learn python so it will be learn-python
        super(Category,self).save(*args, **kwargs)

class Course(models.Model):
    
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)#when course deleted the category will be blank
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    file = models.FileField(upload_to='course-file',blank=True,null=True)
    image = models.FileField(upload_to='course-file',blank=True,null=True) #course thumbnail 
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    language = models.CharField(choices=LANGUAGE,default="English",max_length=100)
    level = models.CharField(choices=LEVEL,default="Begginer",max_length=100)
    platform_stauts = models.CharField(choices=PLATFORM_STATUS,default="Published",max_length=100)
    teacher_course_status = models.CharField(choices=TEACHER_STATUS,default="Published",max_length=100)
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")#unique id is genereted on alphabet given
    slug = models.SlugField(unique=True,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if self.slug == "" or self.slug==None:
            self.slug = slugify(self.title)#eg course title is  learn python so it will be learn-python
        super(Course,self).save(*args, **kwargs)
    #to know student who enroll to course
    
    def student(self):
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return VariantItem.objects.filter(variant__course=self)# two underscore (__) it mean any field on given table
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self)
    
    def average_rating(self):
        average_rating  = Review.objects.filter(course=self,active=True).aggregate(avg_rating=models.Avg('rating')) #rating is our field so we find it avg
        return average_rating['avg_rating'] #return actual avg_rating field
    def rating_count(self):
        return Review.objects.filter(course=self,active=True).count()
    
    def reviews(self):
        return Review.objects.filter(course=self,active=True)
   
#(section)like a all lecture will be in section
class Variant(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    variant_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantItem.objects.filter(variant=self)
    
class VariantItem(models.Model):
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='variant_items')
    title = models.CharField(max_length=100)
    decription = models.TextField(null=True,blank=True)
    variant_items_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to="course-file")#if user have any
    content_duration = models.DurationField(max_length=200,null=True,blank=True)
    duration = models.DurationField(null=True,blank=True)
    preview = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.variant.title} - {self.title}"

    def save (self,*args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.file:
            clip = VideoClip(self.file.path)#give actual path(we want to extract time of video)
            duration_second = clip.duration
            #convert duration into min and second
            
            minute,remainder = divmod(duration_second,60)#divmod is take 2 no as argument and return minute with it reminder
            #Note time will be 60.34324 so with floor into it nearest one
            minutes = math.floor(minute)
            seconds = math.floor(remainder)
            duration_text = f"{minutes}m {seconds}s"
            #store it into content duration
            self.content_duration = duration_text
            super.save(updated_fields=['content_duration'])
            
class Question_Answer(models.Model):
    course =  models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    qa_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    #ordering the QA
    class Meta:
        ordering = ['-date']
    
    def message(self):
        return Question_Answer_Message.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
class Question_Answer_Message(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Answer,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    qam_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    #ordering the QA
    class Meta:
        ordering = ['date']
    
    def message(self):
        return Question_Answer_Message.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
class Cart(models.Model):
    course =  models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    tax_fee =models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    country = models.CharField(max_length=100,null=True,blank=True)
    cart_id = ShortUUIDField(length=6,max_length=20,alphabet="abcdef123456789")
    
    def __str__(self):
        return self.course.title
class CartOrder(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    teacher = models.ManyToManyField(Teacher,blank=True)
    sub_total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    tax_fee = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    initial_total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    payment_status = models.CharField(choices=PAYMENT_STATUS,default="Processing",max_length=100)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    coupons = models.ManyToManyField('api.Coupon',blank=True)
    #note:null=True dont work on ManyToMany
    stripe_session_id = models.CharField(max_length=1000,null=True,blank=True)
    oid = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)
    saved = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    
    class Meta:
        ordering = ['-date']
        
    def order_items(self):
        return CartOrderItem.objects.filter(order=self)
    
    def __str__(self):
        return self.oid
    
class CartOrderItem(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="orderitem")
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE,related_name="order_item")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    coupons = models.ForeignKey('api.Coupon',on_delete=models.SET_NULL,null=True,blank=True)
    tax_fee = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    initial_total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    saved = models.DecimalField(max_digits=12,default=0.00,decimal_places=2)
    applied_cupon = models.BooleanField(default=True)
    oid = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")#unique id is genereted on alphabet given
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']
        
    def order_id(self):
        return f"Order ID #{self.oid}"
    
    def payment_status(self):
        return f"{self.order.payment_status}"
    
    def __str__(self):
        return self.oid
    
class Cirtificate(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    cirtificate_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.course.title

class CompletedLesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    variant_item = models.ForeignKey(VariantItem,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.course.title

class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True)
    enrollment_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    date = models.DateTimeField(default=timezone.now)
    order_item = models.ForeignKey(CartOrderItem,on_delete=models.CASCADE)
    
    #Note: when object created all of this method will be executed to
    def lecture(self):
        return VariantItem.objects.filter(variant__course=self.course)
    
    def complete_lesson(self):
        return CompletedLesson.objects.filter(course=self.course,user=self.user)
    
    def curriculum(self):
        return Variant.objects.filter(course=self.course)
    
    def note(self):
        return Note.objects.filter(course=self.course,user=self.user)
    
    def question_answer(self):
        return Question_Answer.objects.filter(course=self.course)
    
    def review(self):
        return Review.objects.filter(course=self.course,user=self.user).first()#get first items
    
    def __str__(self):
        return self.course.title

class Note(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    note_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="abcdef123456789")
    title = models.CharField(max_length=1000,null=True,blank=True)
    note = models.TextField()
    
    def __str__(self):
        return self.title

class Review(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING,default=None)
    reply = models.CharField(max_length=1000,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.course.title
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(CartOrder,on_delete=models.SET_NULL,null=True,blank=True)
    order_item = models.ForeignKey(CartOrderItem,on_delete=models.SET_NULL,null=True,blank=True)
    review = models.ForeignKey(Review,on_delete=models.SET_NULL,null=True,blank=True)
    type = models.IntegerField(choices=NOT_TYPE,default=None)
    date = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.type
    
class Coupon(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True)
    used_by = models.ManyToManyField(CustomUser,blank=True)
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.code
    
class Whichlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    tax_rate = models.IntegerField(default=True)
    acitve  = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
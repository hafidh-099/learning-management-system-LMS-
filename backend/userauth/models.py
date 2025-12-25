from django.db import models
from django.contrib.auth.models import AbstractUser
#signal help to trigger action before or after happen .eg user created
from django.db.models.signals import post_save

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    otp = models.CharField(max_length=100,blank=True,null=True)#bcs it can combination of Int and char
    refresh_token = models.CharField(max_length=255,blank=True,null=True)
    
    
    USERNAME_FIELD = 'email' #which field will be used for login as username
    REQUIRED_FIELDS = ['username'] # this is field which we need to
    
    def __str__(self):
        return self.email
    #we can overite to provide our own information
    #overide save
    def save(self,*args, **kwargs):
        email_username,full_name = self.email.split("@")#we take email we split and store firstname and username
        if self.full_name == "" or self.full_name==None:
            #if full name is empty string or is Node so emailusername will be used as full name
            self.full_name = email_username
        if self.username == "" or self.username==None:
            self.username = email_username
        return super(CustomUser,self).save(*args, **kwargs)
#we can make system smooth by distinguish 
class Profile(models.Model):
    #OneToOneField one user have only one profile
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder',default='default-user.jpg',null=True,blank=True)#use image field instead of image field(sometime user can use different extension)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100,null=True,blank=True)
    about = models.TextField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)

    def save(self,*args, **kwargs):
        if self.full_name == "" or self.full_name==None:
            self.full_name = self.user.full_name
        return super().save(*args, **kwargs)

def create_user_profile(sender,instance,created,**kwargs):
    if created:
    #if user created by default it create profile by instance of that user created
        return Profile.objects.create(user=instance)

# def save_user(sender,instance,created,**kwargs):
#     return instance.profile.save()

post_save.connect(create_user_profile,sender=CustomUser)
# post_save.connect(save_user,sender=CustomUser)

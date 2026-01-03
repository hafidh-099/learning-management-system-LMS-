from api import views as api_views 
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    #Authentication and authorization
    path('user/token/access/',api_views.myTokenObtainPairView.as_view()),
    path('user/token/refresh/',TokenRefreshView.as_view()),
    path('user/register/',api_views.RegistrationView.as_view()),
    path('user/password-reset/<email>/',api_views.PasswordResetEmailVarifyView.as_view()),
    path('user/password-change/',api_views.PasswordChangeViews.as_view()),
    #core endpoint
    path('course/category/',api_views.CategoryListView.as_view()),
    path('course/course-list/',api_views.CourseListView.as_view()),
    path('course/course-detail/<slug>/',api_views.CourseDetailViews.as_view()),
    path('course/cart-list/<cart_id>/',api_views.CartListView.as_view()),  
    path('course/cart-item-delete/<cart_id>/<id>/',api_views.CartItemDeletedView.as_view()),
]

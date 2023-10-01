from . import views
from django.urls import path
from rest_framework import routers

# create a router object
router = routers.DefaultRouter()
# router.register(r'Register',views.userView)
# router.register(r'Login',login)


urlpatterns = [
    # path('',include(router.urls)),
    path('Register/', views.register_api.as_view()),
    path('Login/', views.login_api.as_view()),
    path('GetUser/',views.get_user_data),
    path('get_user_money/',views.get_user_money)
]
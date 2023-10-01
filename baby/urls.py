from . import views
from django.urls import path
from rest_framework import routers

# create a router object
router = routers.DefaultRouter()
# router.register(r'Register',views.userView)
# router.register(r'Login',login)


urlpatterns = [
    # path('',include(router.urls)),
    path('baby/', views.baby.as_view()),
    path('buy_baby',views.buy_baby.as_view())
]
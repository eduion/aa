from . import views
from django.urls import path
from rest_framework import routers

# create a router object
router = routers.DefaultRouter()
# router.register(r'Register',views.userView)
# router.register(r'Login',login)


urlpatterns = [
    # path('',include(router.urls)),
    path('cost/', views.cost_detail.as_view()),
    path('cost_record/', views.cost_record),
    path('cost_record_month/', views.cost_record_month)
]
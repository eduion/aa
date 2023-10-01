from . import views
from django.urls import path

urlpatterns = [
    path('label/',views.get_label)
]
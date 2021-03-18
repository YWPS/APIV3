from django.urls import path
from .views import *
urlpatterns = [
    path('product/create/<name>', CreateProduct),
    path('product/get/<hash>', GetProduct),
    path('product/update/<hash>', UpdateProduct),
    path('product/delete/<hash>', DeleteProduct),

    path('user/create/<username>', CreateUser),
    path('user/get/<username>', GetUser),
    path('user/updateusername', UpdateUsername),
    path('user/updatepassword', UpdatePassword),
    path('user/delete/<username>', DeleteUser),
    path('user/auth/<username>', AuthUser)
]
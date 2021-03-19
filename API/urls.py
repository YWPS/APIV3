from django.urls import path
from .views import *
urlpatterns = [
    path('product/create/<name>', CreateProduct),
    path('product/get/<hash>', GetProduct),
    path('image/create/<name>', CreateImage),
    path('image/get/<name>', GetImage),
]

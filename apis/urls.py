from django.urls import path
from home.views import  index, process_image, list_cropped_images

urlpatterns = [
    path('index/', index),
    path('process_image/', process_image),
    path('list_cropped_images/', list_cropped_images)   
 
]
from django.urls import path,include
from sprintapp.views import *


urlpatterns = [
   path('sprints/',Sprints,name='sprints'),
   
    
]



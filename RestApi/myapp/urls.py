from django.urls import path
from myapp.views import *
urlpatterns = [
    path('api',BlogClassBase.as_view()),
    path('apis/',FunctionBase),
    



]
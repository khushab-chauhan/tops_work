from rest_framework import serializers
from myapp.models import *

class Blogserializes(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
    

        
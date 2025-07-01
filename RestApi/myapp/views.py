from django.shortcuts import render,get_object_or_404
from myapp.models import Blog
from myapp.serializes import Blogserializes
from rest_framework.decorators import  api_view ,APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

#class base api  (CBV)
class BlogClassBase(APIView):
    def get(self,request):
        try : 
            blog = Blog.objects.all()
            ser = Blogserializes(blog,many = True)
            return Response(ser.data , status=status.HTTP_200_OK)
        except Exception as e:
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
    
        try:
            ser = Blogserializes(data = request.data )
            if ser.is_valid():
                ser.save()
                return Response(ser.data , status=status.HTTP_201_CREATED)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        try:
            blog = get_object_or_404(Blog,pk = request.data['id'])
            ser = Blogserializes(blog ,  request.data )
            if ser.is_valid():
                ser.save()
                return Response(ser.data,status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        try:
            blog = get_object_or_404(Blog,pk = request.data['id'])
            ser = Blogserializes(blog ,  request.data ,partial = True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data,status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            blog = get_object_or_404(Blog, id = request.data['id'])
            blog.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        
    
#function base api (FBV)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def FunctionBase(request, id=None):
    if request.method == 'POST':
        ser = Blogserializes(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    blog = get_object_or_404(Blog, id=id)

    if request.method == 'GET':
        ser = Blogserializes(blog)
        return Response(ser.data)

    elif request.method == 'PUT':
        ser = Blogserializes(blog, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        ser = Blogserializes(blog, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        blog.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)


#generic base api 



#VIEWSETS AND ROUTER 


#JWT  OR TOKEN -BASES API FOR SECURITY (OPTIONS)



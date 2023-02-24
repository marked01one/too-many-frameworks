from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, permissions, status, authentication
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import TodoListSerializer, TodoUserSerializer, TodoSerializer
from api.models import Todo, TodoList, TodoUser

# Create your views here.
class TodoUserViewSet(viewsets.ViewSet):
  '''
  API endpoints that allows for getting & editing user data
  '''
  
  @action(detail=False, methods=['GET', 'POST'], url_path='users')
  def get_make_users(self, request):
    '''
    API endpoints concerning creating & getting user data
    '''
    
    # Get user depends on the request parameters, or lack thereof
    if request.method == 'GET':
      try:
        # Return the user with the given id. 
        # If the id does not exists, return a 404 error
        try:
          user = TodoUser.objects.get(pk=request.query_params['id'])
          serializer = TodoUserSerializer(user)
          return Response({
            "statusCode": status.HTTP_200_OK,
            "user": serializer.data
          })
          
        except TodoUser.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND, data={
            "statusCode": status.HTTP_404_NOT_FOUND,
            "error": f"User with id of '{request.query_params['id']}' does not exists"
          })
          
      # Get all users if no 'id' params is provided
      except MultiValueDictKeyError:
        queryset = TodoUser.objects.all()
        serializer = TodoUserSerializer(queryset, many=True)
        return Response({"users": serializer.data})
    
    # Create a new user in the database, as long as the format fits
    elif request.method == 'POST':
      serializer = TodoUserSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "error": "Bad request error. Potentially caused by improper request body or failing username/email validations."
      })
    
  
  
  
  # @action(detail=True, methods=['GET'], url_path='users')
  # def get_user(self, request, pk=None):
  #   if pk == None or type(pk) != int:
  #     return Response({
  #       "response": "404 Not Found",
  #       "errorCode": "Invalid user id"
  #     })
    
  #   user = get_object_or_404(TodoUser, pk=pk)
  #   serializer = TodoUserSerializer(user)
  #   return Response(serializer.data)
    
      
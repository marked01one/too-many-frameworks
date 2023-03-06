from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, permissions, status, authentication
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import TodoListSerializer, TodoUserSerializer, TodoSerializer
from api.models import Todo, TodoList, TodoUser

import jwt

key = 'secret'

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
            "content": serializer.data
          })
          
        except TodoUser.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND, data={
            "statusCode": status.HTTP_404_NOT_FOUND,
            "message": f"Not found error. User with id of '{request.query_params['id']}' does not exists"
          })
          
      # Get all users if no 'id' params is provided
      except MultiValueDictKeyError:
        queryset = TodoUser.objects.all()
        serializer = TodoUserSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data={
          "statusCode": status.HTTP_200_OK,
          "users": serializer.data
        })
    
    # Create a new user in the database, as long as the format fits
    elif request.method == 'POST':
      
      serializer = TodoUserSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": "Bad request error. Potentially caused by improper request body or failing username/email validations."
      })
    
  
  
  @action(detail=False, methods=['POST'], url_path='login')
  async def login(self, request):
    '''
    API endpoint for logging the user in
    '''
    
    # Handle invalid HTTP methods
    if request.method != 'POST':
      return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={
        "statusCode": status.HTTP_405_METHOD_NOT_ALLOWED,
        "message": f"Method '{request.method}' not allowed. Only 'POST' allowed on this endpoint."
      })
      
    # Handle invalid response body
    try:
      user_name, user_password = await request.data['user_name'], request.data['user_password']
      if len(request.data.keys()) != 2:
        raise KeyError()
      
    except KeyError:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": "Bad request error. Invalid request body. Make sure to follow the example below",
        "sample": {
          "user_name": "<sample_username_here>",
          "user_password": "<sample_password_here>"
        }
      })
    
    # Handle invalid user details given in body
    try:
      user = await TodoUser.objects.get(user_name=user_name, user_password=user_password)
      serializer = TodoUserSerializer(user, many=False)
      
      
    except TodoUser.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": "A user with these details cannot be found. Retry with a different username or password."
      })
    
    return Response(status=status.HTTP_200_OK, data={
      "statusCode": status.HTTP_200_OK,
      "message": "User logged in successfully",
      "content": serializer.data
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


class TodoListViewSet(viewsets.ViewSet):
  '''
  API endpoints regarding todo lists
  '''
  @action(detail=False, methods=['GET', 'POST', 'PUT', 'DELETE'], url_path='lists')
  def all_lists(self, request):
    
    # Get user depends on the request parameters, or lack thereof
    if request.method == 'GET':
      try:
        # Return the list with the given id. 
        # If the id does not exists, return a 404 error
        try:
          user = TodoList.objects.get(
            pk=request.query_params['id'], 
            user_id=request.query_params['user']
          )
          serializer = TodoListSerializer(user)
          return Response({
            "statusCode": status.HTTP_200_OK,
            "content": serializer.data
          })
        
        except MultiValueDictKeyError:
          return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "message": f"Bad request error. Please include the field 'user' for the user ID"
          })
        
        except TodoList.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND, data={
            "statusCode": status.HTTP_404_NOT_FOUND,
            "message": f"Not found error. List with id of '{request.query_params['id']}' for this user does not exists"
          })
          
      # Get all users if no 'id' params is provided
      except MultiValueDictKeyError:
        queryset = TodoList.objects.filter(user_id=request.query_params['user'])
        serializer = TodoListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data={
          "statusCode": status.HTTP_200_OK,
          "content": serializer.data
        })
    
    
    if request.method == 'POST':
      # Handle case where given user ID does not exists
      try:
        user = TodoUser.objects.get(pk=request.data['user_id'])
      except TodoUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={
          "statusCode": status.HTTP_404_NOT_FOUND,
          "message": f"Not found error. User with ID of '{request.data['user_id']}' does not exist."
        })
  

      # Handle all cases where the given keys in the request body is incorrect
      try:
        TodoList.objects.create(user_id=request.data['user_id'], name=request.data['name'])
        return Response(status=status.HTTP_201_CREATED, data={
          "statusCode": 201,
          "message": "New Todo List successfully created for:",
          "content": {
            "user_name": user.user_name,
            "list_name": request.data['name']
          }
        })
        
      except KeyError or IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
          "statusCode": status.HTTP_400_BAD_REQUEST,
          "message": "Bad request error. Potentially caused by improper request body."
        })
        


class TodoViewSet(viewsets.ViewSet):
  @action(detail=False, methods=['GET', 'POST', 'DELETE'], url_path='todos')
  def all_todos(self, request):
    pass
  

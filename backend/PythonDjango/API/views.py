from django.db import IntegrityError
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
  
  @action(detail=False, methods=['GET'], url_path='users')
  def get_make_users(self, request):
    '''
    API endpoints concerning creating & getting user data
    '''
    
    # Get user depends on the request parameters, or lack thereof
    try:
      # Return the user with the given id. 
      try:
        user = TodoUser.objects.get(pk=request.query_params['id'])
        return Response({
          "statusCode": status.HTTP_200_OK,
          "content": {"id": user.pk, 'userName': user.user_name}
        })
      # If the id does not exists, return a 404 error
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
        "content": [
          {"id": user['id'], "userName": user['user_name']} 
          for user in serializer.data
        ]
      })
    
  
  @action(detail=False, methods=['POST'], url_path='users/create')
  def create_new_user(self, request):
    '''
    Create a new user in the database, as long as the format fits
    
    ### Request body:
    ```json
    {
      "user_name": <users_name_goes_here>,
      "user_password": <users_password_goes_here>,
      "user_email": <users_email_goes_here>
    }
    ```
    '''
    serializer = TodoUserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": "Bad request error. Potentially caused by improper request body or failing username/email validations."
      })
  
  
  @action(detail=False, methods=['POST'], url_path='users/login')
  def login(self, request):
    '''
    API endpoint for logging the user in
    ### Request body:
    ```json
    {
      "user_name": <users_name_goes_here>,
      "user_password": <users_password_goes_here>
    }
    ```
    '''
    # Handle invalid HTTP methods
    if request.method != 'POST':
      return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={
        "statusCode": status.HTTP_405_METHOD_NOT_ALLOWED,
        "message": f"Method '{request.method}' not allowed. Only 'POST' allowed on this endpoint."
      })
      
    # Handle invalid response body
    try:
      user_name, user_password = request.data['userName'], request.data['userPassword']
      if len(request.data.keys()) != 2:
        raise KeyError() 
    except KeyError:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": "Bad request error. Invalid request body. Make sure to follow the example below",
        "sample": {
          "userName": "<sample_username_here>",
          "userPassword": "<sample_password_here>"
        }
      })
    
    # Handle invalid user details given in body
    try:
      user = TodoUser.objects.get(user_name=user_name, user_password=user_password)
    except TodoUser.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": "A user with these details cannot be found. Retry with a different username or password."
      })
    
    # Return a 200 OK response for now with user details
    return Response(status=status.HTTP_200_OK, data={
      "statusCode": status.HTTP_200_OK,
      "message": "User logged in successfully",
      "content": {
        "userName": user.user_name,
        "userEmail": user.user_email
      }
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
  @action(detail=False, methods=['GET', 'POST'], url_path='lists')
  def all_lists(self, request):
    # Handle case where given user ID does not exists
    try:
      user = TodoUser.objects.get(pk=request.data['user_id'])
    except TodoUser.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": f"Not found error. User with ID of '{request.data['user_id']}' does not exist."
      })
    
    
    # Get user depends on the request parameters, or lack thereof
    if request.method == 'GET':
      try:
        # Return the list with the given id. 
        # If the id does not exists, return a 404 error
        todo_list = TodoList.objects.get(
          name=request.data['name'], 
          user=user
        )
        return Response({
          "statusCode": status.HTTP_200_OK,
          "content": {
            "id": todo_list.pk,
            "user": user.user_name,
            "name": todo_list.name
          }
        })
      except TodoList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={
          "statusCode": status.HTTP_404_NOT_FOUND,
          "message": f"Not found error. List with name '{request.data['name']}' for this user does not exists"
        })
          
      # Get all users if no 'id' params is provided
      except KeyError:
        try:
          queryset = TodoList.objects.filter(user=user)
        except KeyError:
          return Response(status=status.HTTP_404_NOT_FOUND, data={
          "statusCode": status.HTTP_404_NOT_FOUND,
          "message": f"Not found error. Please provide a 'user_id' field in your request body"
        })
        
        serializer = TodoListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data={
          "statusCode": status.HTTP_200_OK,
          "content": [
            {
              "id": todo_list['id'],
              "user": user.user_name,
              "name": todo_list['name']
            } for todo_list in serializer.data
          ] 
        })
    
    # Create new todo list belonging to the authenticated user
    if request.method == 'POST':
      try:
        obj = TodoList.objects.create(user=user, name=request.data['name'])
        return Response(status=status.HTTP_201_CREATED, data={
          "statusCode": 201,
          "message": f"New Todo List successfully 'created' for:",
          "content": {
            "id": obj.pk,
            "user_name": obj.user.user_name,
            "list_name": obj.name
          }
        })
      # Handle all cases where the given keys in the request body is incorrect
      except KeyError or IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
          "statusCode": status.HTTP_400_BAD_REQUEST,
          "message": "Bad request error. Potentially caused by improper request body."
        })

  
  @action(detail=False, methods=['POST'], url_path='lists/update')
  def update_list(self, request):
    try:
      user = TodoUser.objects.get(pk=request.data['user_id'])
    except TodoUser.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": f"Not found error. User with ID of '{request.data['user_id']}' does not exist."
      })
    
    try:
      new_list_name = request.data['name']
      obj = TodoList.objects.get(pk=request.data['id'], user=user)
      obj.update(name=new_list_name)
      return Response(status=status.HTTP_201_CREATED, data={
        "statusCode": 201,
        "message": f"New Todo List successfully 'created' for:",
        "content": {
          "id": obj.pk,
          "user_name": obj.user.user_name,
          "list_name": obj.name
        }
      })
    # Handle all cases where the given keys in the request body is incorrect
    except KeyError or IntegrityError:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": "Bad request error. Potentially caused by improper request body."
      })
    
  

  @action(detail=False, methods=['DELETE'], url_path='lists/delete')
  def delete_lists(self, request):
    try:
      user = TodoUser.objects.get(pk=request.data['user_id'])
    except TodoUser.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": f"Not found error. User with ID of '{request.data['user_id']}' does not exist."
      })
    
    try:
      TodoList.objects.get(user=user, name=request.data['name']).delete()
      return Response(status=status.HTTP_202_ACCEPTED, data={
        "statusCode": 200,
        "message": f"List '{request.data['name']}' has been successfully deleted"
      })
    # Handle case where given name of list does not exists
    except TodoList.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": 404,
        "message": f"List '{request.data['name']}' does not exist for this user"
      })



class TodoViewSet(viewsets.ViewSet):
  '''
  API endpoints regarding todos
  '''
  def get_specific_user(self, pk: int) -> TodoUser:
    '''
    Get user details from request
    '''
    try:
      return TodoUser.objects.get(pk=pk)
    except TodoUser.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": f"Not found error. User with ID of '{pk}' does not exist."
      })
  
  
  def get_specific_list(self, pk: int, user: TodoUser) -> TodoList:
    '''
    Get list details form request
    ''' 
    try:
      return TodoList.objects.get(pk=pk, user=user)
    except TodoList.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": f"No list with ID of '{pk}' exists for this user."
      })
  
  @action(detail=False, methods=['GET'], url_path='todos')
  def all_todos(self, request):
    try:
      user = self.get_specific_user(pk=request.data['user_id'])
    except KeyError:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": f"Bad request error. Potentially caused by an improper request body."
      })
    
    try:
      todo_list = self.get_specific_list(pk=request.data['list_id'], user=user)
    except KeyError:
      queryset = Todo.objects.filter(user=user)
      serializer = TodoUserSerializer(queryset, many=True)
      return Response(status=status.HTTP_200_OK, data={
        "statusCode": status.HTTP_200_OK,
        "content": {
          "userName": user.user_name,
          "todos": serializer.data
        }
      })
    
    # Return the user with the given id. 
    try:
      todo = Todo.objects.get(user=user, todo_list=todo_list, pk=request.data['id'])
    # If the id does not exists, return a 404 error
    except Todo.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND, data={
        "statusCode": status.HTTP_404_NOT_FOUND,
        "message": f"Not found error. User with id of '{request.data['id']}' does not exists"
      })
    # Get all todos if no 'id' params is provided
    except KeyError:
      queryset = Todo.objects.filter(user=user, todo_list=todo_list)
      serializer = TodoUserSerializer(queryset, many=True)
      return Response(status=status.HTTP_200_OK, data={
        "statusCode": status.HTTP_200_OK,
        "content": serializer.data
      })
    # Return a 200 OK if no errors are found
    else:
      serializer = TodoSerializer(todo)
      return Response({
        "statusCode": status.HTTP_200_OK,
        "content": serializer.data
      })

  
  @action(detail=False, methods=['POST'], url_path='todos/create')
  def create_todos(self, request):
    user = TodoUser.objects.get(pk=request.data['user_id'])
    todo_list = TodoList.objects.get(pk=request.data['list_id'], user=user)
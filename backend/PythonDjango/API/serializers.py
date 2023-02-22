from rest_framework import serializers
from models import Todo, TodoUser, TodoList


class TodoUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = TodoUser
    fields = ('id', 'user_name', 'user_password', 'user_email')


class TodoListSerializer(serializers.ModelSerializer):
  class Meta:
    model = TodoList
    fields = ('id', 'user_id', 'name')


class TodoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Todo
    fields = ('id', 'user_id', 'todo_list_id', 'title', 'description', 'completed')
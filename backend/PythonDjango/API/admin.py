from django.contrib import admin
from .models import TodoUser, TodoList, Todo


# Register your models here.
admin.site.register(TodoUser)
admin.site.register(TodoList)
admin.site.register(Todo)
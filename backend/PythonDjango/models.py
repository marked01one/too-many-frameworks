# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TodoLists(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('TodoUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'todo_lists'


class TodoUsers(models.Model):
    user_name = models.CharField(unique=True, max_length=31)
    user_password = models.CharField(max_length=31)
    user_email = models.CharField(unique=True, max_length=31)

    class Meta:
        managed = False
        db_table = 'todo_users'


class Todos(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(blank=True, null=True)
    todo_list = models.ForeignKey(TodoLists, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(TodoUsers, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'todos'

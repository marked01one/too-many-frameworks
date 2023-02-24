from django.db import models
from django.core.validators import validate_slug, validate_email, RegexValidator


# Model class for users
class TodoUser(models.Model):
  user_name = models.CharField(unique=True, max_length=31, validators=[validate_slug])
  user_password = models.CharField(max_length=31, validators=[
    RegexValidator("(?=^.{6,31}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&amp;*()_+}{&quot;:;'?/&gt;.&lt;,])(?!.*\s).*$")
  ])
  user_email = models.CharField(unique=True, max_length=31, validators=[validate_email])
  
  class Meta:
    app_label = 'api'
    managed = True
    db_table = 'todo_users'
    
  def __str__(self) -> str:
    return self.user_name


# Model class for the Todo lists
class TodoList(models.Model):
  user = models.ForeignKey(TodoUser, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  
  class Meta:
    app_label = 'api'
    managed = True
    db_table = 'todo_lists'
  
  def __str__(self) -> str:
    return self.name
  

# Model class for each Todo
class Todo(models.Model):
  user = models.ForeignKey(TodoUser, on_delete=models.CASCADE)
  todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  description = models.TextField()
  completed = models.BooleanField(default=False)
  
  class Meta:
    app_label = 'api'
    managed = True
    db_table = 'todos'
  
  def __str__(self) -> str:
    return self.title


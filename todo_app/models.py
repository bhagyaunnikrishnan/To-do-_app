from django.db import models

class Todo(models.Model):
    id =  models.AutoField(primary_key=True)
    task = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
# Create your models here.

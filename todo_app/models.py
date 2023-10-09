from django.db import models

class Todo(models.Model):
    id =  models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    
    
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Signup(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField()
    age=models.IntegerField()
    sex=models.CharField()

class HealthRecord(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    bp=models.IntegerField()
    sugar=models.IntegerField()
    oxy=models.IntegerField()
    pulse=models.IntegerField()
    temperature=models.IntegerField()

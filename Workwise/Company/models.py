from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
import math
# Create your models here.


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    otp = models.IntegerField(default=459)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.email


class Company(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cname = models.CharField(unique=True, max_length=50)
    city = models.CharField(max_length=20)
    id_proof = models.FileField(upload_to="media/documents")
    c_pic = models.FileField(upload_to="media/images")

    def __str__(self):
        return self.cname



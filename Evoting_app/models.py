from django.db import models
from django.utils import timezone
# Create your models here.
class Candidate(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    party_name = models.CharField(max_length=50, default="")
    district = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=50,default="")
    mobile = models.IntegerField()
    aadhar_number = models.IntegerField()
    register_date = models.DateField(default=timezone.now)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name+"   "+str(self.vote_count)

class Voter(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    district = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=50,default="")
    mobile = models.IntegerField()
    aadhar_number = models.CharField(max_length=12)
    register_date = models.DateField(default=timezone.now)
    dob = models.DateField()

    def __str__(self):
        return self.name

class Official(models.Model):
    id= models.AutoField
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Voted(models.Model):
    id=models.AutoField
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
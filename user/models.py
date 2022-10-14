from django.db import models
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class myform(models.Model):
  id = models.AutoField(auto_created = True, primary_key = True,
serialize = False, verbose_name ='ID')
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100, unique=True)
  phone = models.CharField(max_length=10, unique=True)
  password = models.CharField(max_length=16)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_authenticated = models.BooleanField(default=False)
  
  
  def __str__(self):
    return "  %d \t |  \t %s " % (self.id, self.username)

  class Meta:
    db_table = 'register'

class Blog(models.Model):
    headline = models.CharField(max_length=500)
    fname = models.CharField(max_length=100)
    pub_date = models.DateField(default=now)
    #author = models.ForeignKey(myform, on_delete=models.CASCADE)

    def __str__(self):
      return self.headline

    class Meta:
      db_table = 'blog'
      ordering = ['headline']
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import myform, Blog
from .auth import *
import os
from django.conf import settings
from datetime import datetime
from django.utils.timezone import now
from django.contrib import messages
import mysql.connector as sql
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password 
# Create your views here.
#@login_required(login_url="login/")
def home(request):
  blog = Blog.objects.all()
  path ='../static/img/'
  try:
    use = User.objects.get(username=request.session['username'])
  except:
    pass
  try:
    if (request.session['username']is not None or request.session['password'] is not None) or use.is_authenticated:
      auth = myform.objects.get(username=request.session['username'], password=request.session['password'])
      users = myform.objects.all()
      try:
        passwd = check_password(request.session['password'], use.password)
      except:
        passwd = False
      return render(request, 'home.html', {'user': auth, 'use':passwd, 'users':users, 'blog':blog, 'path': path})
    else:
      messages.error(request, "login First man")
    return redirect('login/')

  except Exception:
    messages.error(request, "login First")
    return redirect('login/')
  
def signup(request):
  form = myform()
  try :
    auth = myform.objects.filter(username=request.session['username'], password=request.session['password'])
  except:
    auth = None
  if not auth:
    if request.method == "POST":
      form.username = request.POST.get('username')
      form.email = request.POST.get('email')
      form.phone = request.POST.get('phone')
      form.password = request.POST.get('password')
      form.save()
      return redirect('/login')
  else:
    messages.error(request, "please logout first")
    return redirect("/")
  return render(request, 'sign-up.html', {'user': auth})
  
def login(request):
  try:
    authed = myform.objects.filter(username=request.session['username'], password=request.session['password'])
  except:
    authed = None

  if authed:
    messages.info(request, "you have to log out to log in to another account!")
    return redirect('/')
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    authname = myform.objects.filter(username=username)
    authpass = myform.objects.filter(password=password)
    print(authname, authpass)
    if authname and authpass:
      auth = myform.objects.get(username=username)
      loginer(request, auth)
      messages.success(request, "you have successfully loged in! ")
      return redirect('/')
    else:
      messages.error(request, "invalid username or password")
  #print(dir(login_required))
  try:
    return render(request, 'login.html', {'user': authed})
  except:
    return render(request, 'login.html')
  
def logout(request):
  logouter(request)
  messages.success(request, "You have successfully loged out!")
  return redirect('/login')
  
def blog(request):
  try:
    authed = myform.objects.get(username=request.session['username'], password=request.session['password'])
  except:
   authed = None
  if authed is None:
    messages.error(request, "login first! ")
    return redirect('/login/')
  path = os.getcwd()
  news = Blog()
  try:
    if request.method == "POST":
      headline = request.POST.get('blog')
      file = request.FILES['file']
      news.headline = headline
      news.fname = file.name
      with open(os.path.join(os.getcwd() + f'/user/static/img/{file.name}'), 'wb') as f:
        f.write(file.read())
      news.save()
      messages.success(request, "Your blog is sent!")
      return redirect('/blog')
  except:
    messages.error(request, "Fill all the input!")
    return redirect('/blog')
  return render(request, 'blog.html', {'user': authed})
  
def delete(request, id):
  d = Blog.objects.get(id=id)
  f = d.fname
  file_path = os.path.join(os.getcwd() + f'/user/static/img/{f}')
  if os.path.isfile(file_path):
    os.remove(file_path)
    print("File has been deleted")
  else:
    print("File does not exist")
  d.delete()
  return redirect('/')
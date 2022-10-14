from .models import myform

def loginer(request, auth):
  auth.is_authenticated = True
  auth.is_staff = True
  auth.save()
  request.session['username'] = auth.username
  request.session['password'] = auth.password
  


def logouter(request):
  auth = myform.objects.get(username=request.session['username'], password=request.session['password'])
  auth.is_authenticated = False
  auth.is_staff = False
  auth.save()
  request.session['password'] = None
  request.session['username'] = None
  
  
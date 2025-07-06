from http.client import HTTPResponse

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.
message = ""
def register(request):
    message = ""
    if(request.method == "POST"):
        user = request.POST["uuuu"]#user posted something
        email = request.POST["eee"]
        #check password validity
        if request.POST["ppp"] == request.POST["ccc"] :
            passe = request.POST["ppp"]
        else:
            return  render(request, 'register.html', {'mess':"password mismatch"})
        #check if user exists with an email
        if User.objects.filter(email=email).exists():
            message = "Account already exists"
            return redirect('login');
        #check if username is taken(email is new one
        if  User.objects.filter(username=user).exists():
            message = "username taken"
            return render(request, 'register.html', {'mess': message});

        User.objects.create_user(username=user, email=email, password=passe)#row adding to the table
        request.session['log_user'] = user
        return redirect('dashboard')

    return render(request, 'register.html');



def login(request):
    #create a small memory that user logged in
    if request.method == "POST":
        # get the username and password posted by user
        user = request.POST['user']
        passw = request.POST['pass']

        #authenticate the user
        auth = authenticate(username = user, password = passw)
        if auth is not None: #if correct username and password
            request.session["log_user"] = user #create a session for the user so that he can surf the app through differnt url's without logging in again and agian
        else:
            return render(request, 'login.html', {'mess' : "Invalid"})
        return redirect('dashboard')

    return render(request, 'login.html', {'mess' :message});


# @login_required
# def dashboard(request):
#     if 'log_user' in request.session:
#         return render(request, 'dash.html', {'name': request.session['log_user']})
#     return redirect('login')



def profile(request):
    if 'log_user' in request.session:
        return render(request, 'prof.html', {'name': request.session['log_user']})
    return redirect('login')
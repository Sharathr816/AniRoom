from http.client import HTTPResponse

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate

from django.contrib.auth import authenticate, login as auth_login



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
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        if user is not None:
            # ✅ Proper login that Django recognizes
            auth_login(request, user)

            # ✅ Redirect to where user wanted to go (like /animesdashboard/)
            next_url = request.GET.get('next')
            return redirect(next_url) if next_url else redirect('dashboard')

        else:
            return render(request, 'login.html', {'mess': "Invalid"})

    return render(request, 'login.html')



# @login_required
# def dashboard(request):
#     if 'log_user' in request.session:
#         return render(request, 'dash.html', {'name': request.session['log_user']})
#     return redirect('login')



def profile(request):
    return render(request, 'prof.html')

from http.client import HTTPResponse

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from .models import profile
from animes.models import Room, JoinedRooms #works as animes is mention in INSTALLEDAPPS
from django.contrib.auth import authenticate, login as auth_login


def authorize(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        # Proper login that Django recognizes
        auth_login(request, user)
        # Redirect to where user wanted to go (like /animesdashboard/)
        next_url = request.GET.get('next')
        return redirect(next_url) if next_url else redirect('dashboard')

    return render(request, 'login.html', {"mess":"Invalid credential"})


# Create your views here.
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

        #check if username is taken(email is new one
        if  User.objects.filter(username=user).exists():
            return render(request, 'register.html', {'mess': "username taken"});
        #check if user exists with an email
        if User.objects.filter(email=email).exists():
            return redirect('login')

        User.objects.create_user(username=user, email=email, password=passe)#row adding to the table
        #authorize the user
        user_data = User.objects.get(username=user)
        profile.objects.create(user=user_data)
        #for register authorize is always true
        return authorize(request, user, passe)

    return render(request, 'register.html')





def login(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['pass']

        return authorize(request, username, password)

    return render(request, 'login.html')




def Profile(request):
    user_data = User.objects.get(username=request.user)
    profile_data = profile.objects.get(user=user_data)
    room_data = Room.objects.filter(uploaded_by = user_data)
    joined_data = JoinedRooms.objects.filter(user = user_data)

    if request.GET.get('back'):
       return redirect('profy')

    if request.method == "POST":
        pic = request.FILES.get("pic")
        user = request.POST.get("Username")
        bio = request.POST.get("bio")
        if user:
            user_data.username = user
        if bio:
            profile_data.bio = bio
        if pic:
            profile_data.pic = pic #Django automatically stores in media
        profile_data.save()
        user_data.save()
        return redirect('profy')

    return render(request, 'prof.html', {'user':user_data, 'room':room_data, 'profile':profile_data, 'joined':joined_data})

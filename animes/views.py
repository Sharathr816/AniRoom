from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Room
from django.contrib import messages
# Create your views here.

@login_required #default login url is "login/", should have default in urls.py or change in settings.py LOGIN_URL = /Login/
def dashboard(request):
    query = request.GET.get("q")
    if query:
        room = Room.objects.filter(title__icontains = query)
    else:
        room = Room.objects.all().order_by('-id')
    return render(request, 'dash.html', {'rooms' : room})


@login_required
def create_room(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description")
        img = request.FILES.get("image")
        uploady = request.user

        if title and desc and img:
            Room.objects.create(title=title, desc=desc, image=img, uploaded_by=uploady)

            #Post/Redirect/Get pattern (PRG) to prevent form resubmission
            messages.success(request, "Anime uploaded successfully!")  #for one timw message showing
            return redirect('UpPage')  # This sends a GET request to /animes/Uppage/
    return render(request,'AniFold/upload.html')


def room_details(request, id=id):
    if request.method == "GET":
        room_data = Room.objects.get(id = id)
        return render(request, 'roompage.html', {'room' : room_data})



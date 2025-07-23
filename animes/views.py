from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Content, ChatMsg, JoinedRooms
from django.contrib import messages
from django.contrib.auth.models import User
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
    room_data = Room.objects.get(id=id)
    room_cont = Content.objects.filter(room=room_data)

    if request.method == "GET":
        return render(request, 'roompage.html', {'room': room_data, 'cont': room_cont})

    elif  request.user == Room.uploaded_by and request.method == "POST":
        img = request.FILES.get('img')
        vid = request.FILES.get('vid')
        mus = request.FILES.get('mus')
        #because room foreign key expects an object, not int
        Content.objects.create(room=room_data, img=img, vid=vid, mus=mus)
        return render(request, 'roompage.html', {'room': room_data})

    return render(request, 'roompage.html', {'room': room_data, 'cont': room_cont})


def chillPage(request, id=id):
    room_data = Room.objects.get(id=id)
    room_cont = Content.objects.filter(room=room_data)
    messages = ChatMsg.objects.filter(room=room_data)#fetch latest 50 or 100 messages

    #Authenticate the user here
    if request.GET.get('ShowPage'):
        user_data = User.objects.get(username = request.user)
        JoinedRooms.objects.create(user = user_data, room = room_data)
        return render(request, 'ChatPage.html', {'room': room_data, 'cont':room_cont, 'Msg': messages})

    #saving the chat messages
    elif request.POST.get('textContent'):
        texts = request.POST.get('textContent')
        ChatMsg.objects.create(room=room_data, user= request.user, chats=texts)
        #to prevent the "Form resubmission"
        return redirect('ChillPage', id=id)

    return render(request, 'ChatPage.html', {'room': room_data, 'cont': room_cont, 'Msg': messages})


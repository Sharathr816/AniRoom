from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Content, ChatMsg, JoinedRooms
from django.contrib import messages #to store temparory messages like success, error, warning in queue
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.

#default login url is "login/", should have default in urls.py or change in settings.py LOGIN_URL = /Login/
def dashboard(request):
    query = request.GET.get("q")
    if query:
        room = Room.objects.filter(title__icontains = query)
    else:
        room = Room.objects.all().order_by('-id')
    return render(request, 'dash.html', {'rooms' : room})



def create_room(request):
    if request.user.is_authenticated:
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
    try:
        room_data = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return HttpResponse('room dosent exists')

    #Only authenticated user has to previllage to join or manage rooms
    if request.user.is_authenticated:
        joined_room = JoinedRooms.objects.filter(user=request.user, room=room_data)  # None if the user is the uploader
        if joined_room.exists() and request.GET.get("Leave"):
            joined_room.delete()
            return redirect('profy')

        #if already joined room (To prevent integrity error in JoinedRooms)
        if joined_room.exists():#use filter to handle "no object found error"
            return redirect('ChillPage', id=id)

        #authenticate user
        if request.user == room_data.uploaded_by:
            #Room details update
            if request.method == "POST" and request.POST.get("Roomedit"):
                img = request.FILES.get("photo")
                title = request.POST.get("title")
                desc = request.POST.get("desc")
                if title:
                    room_data.title = title
                if desc:
                    room_data.desc = desc
                if img:
                    room_data.image = img
                room_data.save()
                return redirect('RoomPage', id=id)

            #room deletion
            if request.GET.get("delete"):
                room_data.delete()
                return redirect('profy')


            #content upload logic
            if  request.POST.get("RoomUp") and request.method == "POST":
                files = request.FILES.getlist("files")
                for file in files:
                    if file.size > 50*1024*1024:
                        messages.error(request, "File size is greater")
                        return redirect('RoomPage', id=id)
                    if file.content_type.startswith('image/'):
                        Content.objects.create(room=room_data, img=file)
                    elif file.content_type.startswith('video/'):
                        Content.objects.create(room=room_data, vid=file)
                    elif file.content_type.startswith('audio/'):
                        Content.objects.create(room=room_data, mus=file)
                    else:
                        continue
                return redirect('RoomPage', id=id)

    return render(request, 'roompage.html', {'room': room_data})


def chillPage(request, id=id):
    room_data = Room.objects.get(id=id)
    room_cont = Content.objects.filter(room=room_data)
    #usgae of django pagination
    messages = ChatMsg.objects.filter(room=room_data).order_by('-time_stamp')[:50:-1]#order by gives in decreasing order of timestamp

    #Authenticate the user here
    if request.GET.get('join-room'):
        user_data = User.objects.get(username = request.user)
        JoinedRooms.objects.create(user = user_data, room = room_data)
        return render(request, 'ChatPage.html', {'room': room_data, 'cont':room_cont, 'Msg': messages})

    #saving the chat messages
    elif request.POST.get('textContent'):
        texts = request.POST.get('textContent')
        ChatMsg.objects.create(room=room_data, user= request.user, chats=texts)
        #to prevent the "Form resubmission"
        return redirect('ChillPage', id=id)

    # user can enter directly only if he has joined earlier and not the room uploader
    if not JoinedRooms.objects.filter(user = request.user, room = room_data) and not request.user == room_data.uploaded_by:
        return redirect('RoomPage', id=id)
    #if he is a room uploader then he can enter directly
    return render(request, 'ChatPage.html', {'room': room_data, 'cont': room_cont, 'Msg': messages})



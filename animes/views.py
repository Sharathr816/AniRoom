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
        #User side
        joined_room = JoinedRooms.objects.filter(user=request.user, room=room_data, status="accept")  # None if the user is the uploader
        if joined_room.exists() and request.GET.get("Leave"):
            joined_room.delete()
            return redirect('profy')

        #if already joined room (To prevent integrity error in JoinedRooms)
        if joined_room.exists():#use filter to handle "no object found error"
            return redirect('ChillPage', id=id)

        #creator side
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
    #usage of django pagination
    messages = ChatMsg.objects.filter(room=room_data).order_by('-time_stamp')[:50:-1]#order by gives in decreasing order of timestamp

    #Authenticate the user here
    if request.GET.get('joinRoom'):
        mess = ""
        user_data = User.objects.get(username = request.user)
        joined_room = JoinedRooms.objects.filter(user = user_data, room = room_data)
        if not joined_room.exists():
            JoinedRooms.objects.create(user = user_data, room = room_data, status = "pending")
            mess = "Your request to join has been sent \n If accepted the room will be shown in your profile"
        else:
            for joined in joined_room:
                if joined.status == "block":# if in case the creator pressed block by mistake
                    mess = "You are blocked by the room creator and cannot join again"
                elif joined.status == "reject":
                    joined.status = "pending"
                    mess = "Request sent again \n (Your request was rejected by the creator in previous attempt)"
                joined.save()
        return render(request, 'roompage.html', {'room': room_data, 'message':mess})

    #saving the chat messages
    elif request.POST.get('textContent'):
        texts = request.POST.get('textContent')
        ChatMsg.objects.create(room=room_data, user= request.user, chats=texts)
        #to prevent the "Form resubmission"
        return redirect('ChillPage', id=id)

    # user who havent joined + not an uploader, cannot enter the room(during leave and pressing back in browser)
    if not JoinedRooms.objects.filter(user = request.user, room = room_data) and not request.user == room_data.uploaded_by:
         return redirect('RoomPage', id=id)

    #if he is a room uploader/user has already joined then he can enter directly
    return render(request, 'ChatPage.html', {'room': room_data, 'cont': room_cont, 'Msg': messages})

def Approve(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST.get("username"))
        room = Room.objects.get(id=request.POST.get("roomid"))
        joined = JoinedRooms.objects.get(user=user,room=room)
        if request.POST.get("approve"):
            joined.status = "accept"
        elif request.POST.get("reject"):
            joined.status = "reject"
        elif request.POST.get("block"):
            joined.status = "block"
        joined.save()
        return redirect("approvals")

    room_data = Room.objects.filter(uploaded_by=request.user)
    creator_room_in_joined = []
    for room in room_data:
        joined = JoinedRooms.objects.filter(room=room, status="pending")
        if joined.exists():
            creator_room_in_joined.append(joined)
    return render(request, 'MessageBox.html', {'room_json':creator_room_in_joined})






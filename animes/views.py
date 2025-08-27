from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Content, ChatMsg, JoinedRooms, Messages
from django.contrib import messages #to store temparory messages like success, error, warning in queue
from django.contrib.auth.models import User
from django.http import HttpResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
        #creator side
        if request.user == room_data.uploaded_by:
            #Room details update
            if request.POST.get("Roomedit"):
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
            #content upload logic
            if  request.POST.get("RoomUp"):
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
            #Removing a user from room
            if request.POST.get("userRemove"):
                user = User.objects.get(username=request.POST.get("userRemove"))
                joined_qs = JoinedRooms.objects.get(user=user, room=room_data)
                joined_qs.delete()
                Messages.objects.create(user=user, room=room_data, msg_type="removed")
                return redirect('RoomPage', id=id)
            # room deletion
            if request.GET.get("delete"):
                room_data.delete()
                return redirect('profy')

        # User side
        else:
            joined_room = JoinedRooms.objects.filter(user=request.user, room=room_data, status="accept")
            if joined_room.exists() and request.GET.get("Leave"):
                joined_room.delete()
                return redirect('profy')

            # request to join room
            if request.GET.get('joinRoom'):
                mess = ""
                joined_room = JoinedRooms.objects.filter(user=request.user, room=room_data)
                if not joined_room.exists():
                    JoinedRooms.objects.create(user=request.user, room=room_data, status="pending")
                    mess = "Your request to join has been sent"
                else:
                    for joined in joined_room:
                        if joined.status == "block":  # if in case the creator pressed block by mistake
                            mess = "You are blocked by the room creator and cannot join again"
                        elif joined.status == "reject":
                            joined.status = "pending"
                            mess = "Request sent again to join"
                        joined.save()
                return render(request, 'roompage.html', {'room': room_data, 'message': mess})

            # if already joined room (To prevent integrity error in JoinedRooms)
            if joined_room.exists():  # use filter to handle "no object found error"
                return redirect('ChillPage', id=id, user=request.user)

    return render(request, 'roompage.html', {'room': room_data, 'joined': JoinedRooms.objects.filter(room=room_data, status='accept')})


def chillPage(request, id, user):
    room_data = Room.objects.get(id=id)
    contents = Content.objects.filter(room=room_data)
    messages = ChatMsg.objects.filter(room=room_data)

    context = {
        'room_name':room_data.title,
        'room_contents':contents,
        'messages':messages,
        'user':user,
    }



    return render(request, 'ChatPage.html', context)



# Creators choice to let someone in or kick someone out
def Message_box(request):
    if request.POST.get("roomid"):
        user = User.objects.get(username=request.POST.get("username"))
        room = Room.objects.get(id=request.POST.get("roomid"))
        joined = JoinedRooms.objects.get(user=user,room=room)
        if request.POST.get("approve"):
            joined.status = "accept"
            Messages.objects.create(user=user, room=room, msg_type="accepted")
        elif request.POST.get("reject"):
            joined.status = "reject"
            Messages.objects.create(user=user, room=room, msg_type="rejected")
        elif request.POST.get("block"):# need a pop up message here
            joined.status = "block"
            Messages.objects.create(user=user, room=room, msg_type="blocked")
        joined.save()
        return redirect("approvals")

    # Get user requests to join the room of the current user(creator)
    room_data = Room.objects.filter(uploaded_by=request.user)
    creator_room_in_joined = []
    for room in room_data:
        joined = JoinedRooms.objects.filter(room=room, status="pending")
        if joined.exists():
            creator_room_in_joined.append(joined)

    # Get messages for the current user regarding joining others room
    message_data = Messages.objects.filter(user=request.user)
    return render(request, 'MessageBox.html', {'room_json':creator_room_in_joined, 'messages':message_data})





    #saving the chat messages
    # if request.POST.get('textContent'):
    #     texts = request.POST.get('textContent')
    #     ChatMsg.objects.create(room=room_data, user= request.user, chats=texts)
    #     #to prevent the "Form resubmission"
    #     return redirect('ChillPage', id=id)


    # room_data = Room.objects.get(id=id)
    # room_cont = Content.objects.filter(room=room_data)
    # #usage of django pagination
    # messages = ChatMsg.objects.filter(room=room_data).order_by('-time_stamp')#[:50:-1]#order by gives in decreasing order of timestamp
    #
    # channel_layer = get_channel_layer()
    #
    # # Send to all consumers in the group "room_1"
    # async_to_sync(channel_layer.group_send)(
    #     "room_1",
    #     {
    #         "type": "chat.message",  # will call consumer method `chat_message(self, event)`
    #         "message": "Hello room!"
    #     }
    # )
    #
    #
    # # user who havent joined + not an uploader, cannot enter the room(during leave and pressing back in browser)
    # if not JoinedRooms.objects.filter(user = request.user, room = room_data) and not request.user == room_data.uploaded_by:
    #      return redirect('RoomPage', id=id)
    #
    # #if he is a room uploader/user has already joined then he can enter directly
    # return render(request, 'ChatPage.html', {'room': room_data, 'cont': room_cont, 'Msg': messages})


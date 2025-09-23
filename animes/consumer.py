import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from animes.models import *


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}" #create a room name variable
        # channel layer: It represents the layer that handles groups and channels
        await self.channel_layer.group_add(self.room_name, self.channel_name) #channel name : Unique channel name automatically assigned to this connection by Django
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        # call send_message function
        event = {
            "type":"send_message",
            "message":message, # this consists of sender, room name and messages
        }

        await self.channel_layer.group_send(self.room_name, event)# send to the room so everyone can see the message(front end)

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = { # sending one user message to all in the room
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data})) #send to recv method

    # save it in database
    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(title=data['room_name'])
        if not ChatMsg.objects.filter(chats=data['message']).exists(): # check out some edge cases here
            new_message = ChatMsg(room=get_room_by_name, user=data['sender'], chats=data['message'])
            new_message.save()
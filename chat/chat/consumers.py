import json

from channels import Group
from channels.sessions import channel_session
from rooms.models import Room

@channel_session
def ws_connect(message):
    try:
        prefix, label = message['path'].strip('/').split('/')
        if prefix != "chat":
            return
        room = Room.objects.get(label=label)
    except ValueError:
        print 'invalid websocket path=%s' % message['path']
        return
    except Room.DoesNotExist:
        print 'websocket room does not exist label=%s' % label
        return

    room = Room.objects.get(label=label)
    Group('chat-' + label, channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        print 'no room in channel_session'
        return
    except Room.DoesNotExit:
        print 'received message, but room does not exist label=%s' % label
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        print 'websocket message is not json text=%s' % message['text']
        return

    if set(data.keys()) != set(('handle', 'message')):
        print 'websocket message unexpected format data=%s' % data

    if data:
        print 'chat message room=%s handle=%s message=%s' % (room.label, data['handle'], data['message'])
        m = room.messages.create(**data)

        Group('chat-' + label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-' + label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass

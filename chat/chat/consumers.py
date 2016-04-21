import json

from channels import Group
from channels.sessions import channel_session
from rooms.models import Room, Profile

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

    if set(data.keys()) != set(('message', 'owner')):
        print 'websocket message unexpected format data=%s' % data

    if data:
        print 'chat message room={0} message={1} owner={2}'.format(room.label, data['message'], data['owner'])
        profile = Profile.objects.get(pk=data['owner'])
        m = room.messages.create(message=data['message'],
                                 owner=profile)

        Group('chat-' + label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-' + label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass

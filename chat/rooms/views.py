from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, "room/about.html")


def chat_room(request, label):
    # If the room with the given label doesn't exit,
    # automatically create it.
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "room/room.html", {
        'room': room,
        'messages': messages
    })

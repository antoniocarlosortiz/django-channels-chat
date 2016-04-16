# django-channels-chat
a replica of [https://github.com/jacobian/channels-example](https://github.com/jacobian/channels-example) with a few changes.

##HOW TO RUN
1. `pip install -r requirements.txt`
2. run redis with its default config; inside redis folder: `src/redis-server`
3. in another terminal `daphne chat.asgi:channel_layer --port 8888`
4. in another terminal `python manage.py runworker`

##TODO
- [ ] Use Facebook OAuth to create unique users
- [ ] Fix design
- [ ] Show rooms Facebook Users are part of.
- [ ] Show number of members each room
- [ ] Show most recent message as preview to the room
- [ ] Add JS seen by

# django-channels-chat
a replica of [https://github.com/jacobian/channels-example](https://github.com/jacobian/channels-example) with a few changes.

##HOW TO RUN
####Setup
1. `pip install -r requirements.txt`
2. create a web app in developers facebook and add the key and secret to env variables **SOCIAL_AUTH_FACEBOOK_KEY**, and **SOCIAL_AUTH_FACEBOOK_SECRET** respectively.
3. Facebook will be asking for a legit url but for development, just write there anything like `djangochat.com:8888` (just make sure the port is correct).
4. on your local, open `/etc/hosts` (assuming linux) then add `127.0.0.1 djangochat.com`. This will allow you to access `127.0.0.1` with `djangochat.com`.

####Running the app
1. run redis with its default config; inside redis folder: `src/redis-server`
2. in another terminal `daphne chat.asgi:channel_layer --port 8888`
3. in another terminal `python manage.py runworker`

##TODO
- [ ] Use Facebook OAuth to create unique users
- [ ] Fix design
- [ ] Show rooms Facebook Users are part of.
- [ ] Show number of members each room
- [ ] Show most recent message as preview to the room
- [ ] Add JS seen by

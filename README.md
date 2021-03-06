<img src="https://raw.githubusercontent.com/kellya/notipy/master/images/notipy.svg" width="200">

# noti.py
Simple Python-based notification script to post to a matrix server via the Matrix client/server API

This is not an interactive chat bot.  The use case is to have scripts send alerts to a single alert channel.

# How to install
I may eventually get this up in pypi, but for now:
1.  clone the repo
2.  install the requirements `pip install -r requirements.txt`
3.  `cp example-config.yaml config.yaml`
4.  Edit the config.yaml to your local needs
5.  Then just use `./noti.py --help` to figure out what options you can specify

# How do I use this thing?
start with `noti.py --help` to see a list of the commands you can use.  Generally you are going to need to do the following things:

1. Create a user on your server for this script to connect as
2. Connect to a room by either:
    1. Creating a new room `noti.py create`
    or
    2. Joining a room `noti.py join` if you've already invited the user from step 1 with a different user
3.  Edit the config.yaml to put in your access token and all your homeserver configuration.  If you don't know your token, you can get it by running `./noti.py token`

At this point you should be able to send a message with: `./noti.py send "message to send"` or if you are so inclined, you can pipe stdin to the script with `echo "message to send"|./noti.py send`
# Inspiration
I tried to use [mnotify](https://matrix.org/docs/projects/client/mnotify) which is written in go.  When I ran `make`, it gave a segfault upon running `mnotify`.  Rather than try to learn go, I decided to just try to do the same thing in python.

# Contribute
Feel free to fork, make updates and submit a pull request for new things or to fix some horrible python atrocity I have commited ;)

# Chat
You can join me on matrix at https://matrix.to/#/#noti.py:arachnitech.com

# Notes
I started using matrix 3 days ago.  There are a lot of things about its operation that I haven't figure out yet.  This will hopefully progress as I figure things out, but beware that this approach may not be the best one.

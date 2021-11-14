![build status](https://build.arachnitech.com/badges/noti.py.png) ![latest Release](https://img.shields.io/github/v/release/kellya/notipy) ![Latest in dev](https://img.shields.io/github/v/tag/kellya/notipy?label=latest%20%28dev%29)

<img src="https://raw.githubusercontent.com/kellya/notipy/master/images/notipy.svg" width="200">

# noti.py
Simple Python-based notification script to post to a matrix server via the Matrix client/server API

This is not an interactive chat bot.  The use case is to have scripts send alerts to a single alert channel.

# Documentation

Full documentation is available at
[notipy.readthedocs.io](https://notipy.readthedocs.io)

# How to install
## Via PyPi
As of version 0.0.6, noti.py has been published to PyPi, so installing (should
be) as easy as
`pip install noti_py`

This will also create a `notipy` "entrypoint" to use as the binary to run.

## Via git
1.  clone the repo
2.  install the requirements `pip install -r requirements.txt`
3.  `cp example-config.yaml <config_dir>config.yaml`
4.  Edit the config.yaml to your local needs
5.  Then just use `./noti.py --help` to figure out what options you can specify

<config_dir> referenced in step 3 above will be checked in the following order
or preference
1. . (current directory)
2. ~/.config/noti_py
3. /etc/noti_py

If you want it in another location completely, specify the `--config` option to
override.

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

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

# Inspiration
I tried to use [mnotify](https://matrix.org/docs/projects/client/mnotify) which is written in go.  When I ran `make`, it gave a segfault.  Rather than try to learn go, I decided to just try to do the same thing in python.

# Notes
I started using matrix 3 days ago.  There are a lot of things about its operation that I haven't figure out yet.  This will hopefully progress as I figure things out, but beware that this approach may not be the best one.  I already don't particularly like using the client/server API for this, but the python libraries that I have found so far are WAY overkill because they assume you are writing an interactive bot

#!/usr/bin/env python

import requests
import urllib.parse
import sys
import select
import click
from config import Config

cf = Config()
__version__ = "0.0.1"


def login(username, password):
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    login = requests.post(
        f"{base}/login",
        json={
            "type": "m.login.password",
            "user": username,
            "password": password,
        },
    )
    return login


def send_message(token, messagetext):
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    roomid = urllib.parse.quote(cf.config['room']['id'])
    roomurl = (
        f"{base}/rooms/{roomid}/send/m.room.message"
        f"?access_token=" + token
    )
    message = requests.post(roomurl, json={"msgtype": "m.text", "body": messagetext})
    return message


@click.command()
@click.option('-m', '--message', help="Message text to send")
@click.option('-c', '--config', type=click.Path(),
              help="Alternate path to config file",
              default="./config.yaml")
@click.option('--version', type=click.BOOL, is_flag=True, help="Display version information")
def main(message, config, version):
    if version:
        print(__version__)
        sys.exit()
    cf.load_config(config)
    mylogin = login(cf.config['user']['name'], cf.config['user']['pass'])
    token = mylogin.json()['access_token']
    # I don't really understand what select does here, but it's used to figure
    # out if we have data from stdin or not
    if select.select(
        [
            sys.stdin,
        ],
        [],
        [],
        0.0,
    )[0]:
        send_message(token, sys.stdin.readline())
    else:
        send_message(token, message)


if __name__ == "__main__":
    main()

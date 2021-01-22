#!/usr/bin/env python

import requests
import urllib.parse
import sys
import select
import click
from config import Config

__version__ = "0.0.1"

cf = Config() # Config object we will use globally for options


def login(username, password):
    """
    Attempt to login to the homeserver with the username and password specified
    :param username:
    :param password:
    :return: requests object
    """
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
    """
    Sends the message specified to your configured homeserver
    :param token: Authtoken that is qcquired from 'login'
    :param messagetext: text of the message you wish to send
    :return:  requests object
    """
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    roomid = urllib.parse.quote(cf.config["room"]["id"])
    roomurl = f"{base}/rooms/{roomid}/send/m.room.message" f"?access_token=" + token
    message = requests.post(roomurl, json={"msgtype": "m.text", "body": messagetext})
    return message


@click.command()
@click.option("-m", "--message", help="Message text to send")
@click.option(
    "-c",
    "--config",
    type=click.Path(),
    help="Alternate path to config file",
    default="./config.yaml",
)
@click.option(
    "--version", type=click.BOOL, is_flag=True, help="Display version information"
)
def main(message, config, version):
    """
    Main program logic
    :param message:  click option
    :param config:  click option
    :param version: click option
    :return: None
    """
    if version:
        print(__version__)
        sys.exit()
    cf.load_config(config)
    mylogin = login(cf.config["user"]["name"], cf.config["user"]["pass"])
    token = mylogin.json()["access_token"]
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

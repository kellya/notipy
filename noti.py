#!/usr/bin/env python

import requests
import urllib.parse
import sys
import json

import select
import click
from config import Config

__version__ = "0.0.3"

cf = Config()  # Config object we will use globally for options


@click.group(name="main", invoke_without_command=True)
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
def main(config, version):
    if version:
        print(__version__)
        sys.exit()
    cf.load_config(config)


@main.command()
@click.option("-u", "--user", prompt=True)
@click.option(
    "-p", "--password", prompt=True, confirmation_prompt=False, hide_input=True
)
def token(user, password):
    """Get an auth token for the user"""
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    login = requests.post(
        f"{base}/login",
        json={
            "type": "m.login.password",
            "user": user,
            "password": password,
        },
    )
    try:
        token = login.json()["access_token"]
    except KeyError:
        print("Username/password combination is not valid")
        sys.exit()
    print(token)


@main.command()
def join():
    """Join a room as the user configured with token in config.yaml"""
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    joinurl = f'{base}/join/{cf.config["room"]["id"]}'
    room_join = requests.post(
        joinurl,
        json={},
        headers={
            "Authorization": "Bearer " + cf.config["user"]["token"],
        },
    )
    print(room_join.content)


@main.command()
@click.argument("messagetext", required=False)
def send(messagetext):
    "Send a message to your alert room defined in config.yaml"

    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    roomid = urllib.parse.quote(cf.config["room"]["id"])
    roomurl = f"{base}/rooms/{roomid}/send/m.room.message"
    if select.select(
        [
            sys.stdin,
        ],
        [],
        [],
        0.0,
    )[0]:
        messagetext_stream = click.get_text_stream("stdin")
        messagetext = messagetext_stream.read().strip()
    message = requests.post(
        roomurl,
        json={
            "msgtype": "m.text",
            "body": messagetext,
        },
        headers={
            "Authorization": "Bearer " + cf.config["user"]["token"],
        },
    )


if __name__ == "__main__":
    main()

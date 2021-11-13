#!/usr/bin/env python

from pathlib import Path
import select
import sys
import urllib.parse
import requests
import click
from noti_py.config.config import Config

__version__ = "0.3.1"

cf = Config()  # Config object we will use globally for options


def get_default_config_path(test=False):
    """
    Try known paths for config.yaml and return None if file is not found in
    default locations.
    """
    if not test:
        base_dirs = [".", f"{str(Path.home())}/.config/noti_py", "/etc/noti_py/"]
    else:
        base_dirs = ["fake"]
    for config_dir in base_dirs:
        path = Path(f"{config_dir}/config.yaml")
        if path.is_file():
            return path
    return None


@click.group(name="main", invoke_without_command=True)
@click.option(
    "-c",
    "--config",
    type=click.Path(),
    help="Alternate path to config file",
    default=get_default_config_path(),
)
@click.option(
    "--version", type=click.BOOL, is_flag=True, help="Display version information"
)
def main(config, version):
    """main function"""
    if version:
        print(__version__)
        sys.exit()
    if config:
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
@click.option("-n", "--name", prompt=True)
def create(name):
    """Create a room with an alias named <name>"""
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    roomurl = f"{base}/createRoom"
    create_room = requests.post(
        roomurl,
        json={
            "room_alias_name": name,
        },
        headers={
            "Authorization": "Bearer " + cf.config["user"]["token"],
        },
    )
    print(create_room.content)


def get_dm_room_id(dm_user=None):
    """Get or create a direct message room for the user"""
    try:
        # If we have a room configured, use it
        dm_room_id = cf.config["dm"]["room"]
    except KeyError:
        if not dm_user:
            print("Need to specify a user to DM")
            sys.exit()
        # Otherwise, create a new room
        base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
        # Create a new room
        cr = requests.post(
            f"{base}/createRoom",
            json={
                "body": {
                    "preset": "trusted_private_chat",
                    "invite": [dm_user],
                    "is_direct": "true",
                }
            },
            headers={
                "Authorization": "Bearer " + cf.config["user"]["token"],
            },
        )
        dm_room_id = cr.json()["room_id"]
    return dm_room_id


@main.command()
@click.argument("messagetext", required=False)
@click.option(
    "-i",
    "--roomid",
    multiple=True,
    default=lambda: cf.config["room"]["id"],
)
@click.option("-l", "--level", default=0, help="Severity level 1-3")
@click.option(
    "--dm", is_flag=True, default=False, help="Send message as direct message"
)
def send(messagetext, roomid, level, dm):
    "Send a message to your alert room defined in config.yaml"
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
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
    if dm:
        roomid = [get_dm_room_id()]
        print(roomid)
    for room in roomid:
        roomurl = f"{base}/rooms/{urllib.parse.quote(room)}/send/m.room.message"
        colors = [
            "#FFFFFF",
            "#00FF00",
            "#FFFF00",
            "#FF9933",
            "#FF0000",
        ]
        message = requests.post(
            roomurl,
            json={
                "msgtype": "m.text",
                "body": messagetext,
                "format": "org.matrix.custom.html",
                "formatted_body": f"<table><tr><td><span data-mx-bg-color='{colors[level]}'>&nbsp;&nbsp;</td></span><td>{messagetext}</td></tr></table>",
            },
            headers={
                "Authorization": "Bearer " + cf.config["user"]["token"],
            },
        )
    if message.status_code > 200:
        print("There was an issue posting the message")


@main.command()
def rooms():
    """Get a list of rooms of which configured user is joined"""
    base = cf.config["homeserver"]["base"] + cf.config["homeserver"]["api_base"]
    roomurl = f"{base}/joined_rooms"
    room_list = requests.get(
        roomurl,
        headers={
            "Authorization": "Bearer " + cf.config["user"]["token"],
        },
    )
    print(room_list.content)


if __name__ == "__main__":
    main()

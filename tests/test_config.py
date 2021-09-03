""" Test the base noti.py functions"""
from noti_py.config.config import Config


def test_get_config():
    """Verify we can get a configuration file loaded and get a value out of it"""
    cf = Config()
    cf.load_config("ci/config.yaml")
    assert type(cf.config["room"]) == dict
    assert cf.config["room"]["id"][0] == "!BVCLZxeaUsSaSNCaCW:arachnitech.com"
    cf_fail = Config()
    cf_fail.load_config("ci/bogus.yaml")

from noti_py.noti import main as notipy_main
from noti_py.noti import __version__ as notipy_version
from noti_py.noti import get_default_config_path
from click.testing import CliRunner
from pathlib import Path

runner = CliRunner()


def test_main():
    """Verify that main runs successuflly"""
    if notipy_main:
        response = runner.invoke(notipy_main)
        assert response.exit_code == 0


def test_rooms():
    """Verify that we get a list of rooms"""
    response = runner.invoke(notipy_main, ["rooms"])
    assert response.exit_code == 0


def test_config():
    """Verify that we get a config returned, should be local for testing"""
    config_path = get_default_config_path()
    assert config_path is not None
    assert str(config_path) in ["config.yaml"]

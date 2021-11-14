""" Test the base noti.py functions"""
from click.testing import CliRunner
from noti_py.noti import main as notipy_main
from noti_py.noti import get_default_config_path

runner = CliRunner()


def test_main():
    """verify the main function runs successfully with a 0 return code"""
    response = runner.invoke(notipy_main)
    assert response.exit_code == 0
    response = runner.invoke(notipy_main, ["--version"])
    assert response.exit_code == 0
    response = runner.invoke(notipy_main, ["--config", "ci/config.yaml"])
    assert response.exit_code == 0


def test_rooms():
    """Validate that calling --rooms terminates successfully"""
    response = runner.invoke(notipy_main, ["rooms"])
    assert response.exit_code == 0


def test_get_default_config():
    """Verify we get a path returned for the config search function"""
    config_file = get_default_config_path()
    assert config_file is not None
    config_file_fail = get_default_config_path(True)
    assert config_file_fail is None
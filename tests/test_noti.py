from noti_py.noti import main as notipy_main
from noti_py.noti import __version__ as notipy_version
from click.testing import CliRunner

runner = CliRunner()


def test_main():
    if notipy_main:
        response = runner.invoke(notipy_main)
        assert response.exit_code == 0


def test_rooms():
    response = runner.invoke(notipy_main, ["rooms"])
    assert response.exit_code == 0

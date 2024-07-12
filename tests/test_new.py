from datetime import datetime
from unittest.mock import patch

from binary_cookies_parser.models import Cookie
from msteams_tickler.main import check
from polyfactory.factories.pydantic_factory import ModelFactory


class CookieFactory(ModelFactory):
    __model__ = Cookie
    name = "fpc"
    expiry_datetime = datetime(2001, 1, 1)


@patch("msteams_tickler.main.notify")
@patch("msteams_tickler.main.read_binary_cookies_file")
def test_check(mock_read_binary_cookies_file, mock_notify):
    mock_token = CookieFactory.build()
    mock_read_binary_cookies_file.return_value = [mock_token]
    check("~/path/to/cookies", "fpc")
    mock_notify.assert_called_once()

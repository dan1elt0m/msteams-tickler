from datetime import datetime
from unittest.mock import MagicMock, patch

from msteams_tickler.main import tickle_token
from msteams_tickler.models import Cookies


@patch("msteams_tickler.main.notify")
@patch("msteams_tickler.main.select_token")
@patch("sqlmodel.create_engine")
def test_tickle_token(mock_create_engine, mock_select_token, mock_notify):
    expires_utc = int((datetime.now() - datetime(1601, 1, 1)).total_seconds() * 1_000_000)
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    mock_token = Cookies(name="authtoken", expires_utc=expires_utc)
    mock_select_token.return_value = mock_token

    tickle_token()

    mock_notify.assert_called_once()

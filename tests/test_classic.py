from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from msteams_tickler.classic.models import Cookies
from msteams_tickler.classic.token import check, is_expired, select_token
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel


class CookiesFactory(ModelFactory):
    __model__ = Cookies
    name = "authtoken"


@patch("msteams_tickler.classic.token.notify")
@patch("msteams_tickler.classic.token.select_token")
@patch("sqlmodel.create_engine")
def test_check(mock_create_engine, mock_select_token, mock_notify):
    expires_utc = int((datetime.now(UTC) - datetime(1601, 1, 1, tzinfo=UTC)).total_seconds() * 1_000_000)
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    mock_token = Cookies(name="authtoken", expires_utc=expires_utc)
    mock_select_token.return_value = mock_token

    check()

    mock_notify.assert_called_once()


def test_is_expired():
    expires_utc_future = int(
        (datetime.now(UTC) + timedelta(hours=1) - datetime(1601, 1, 1, tzinfo=UTC)).total_seconds() * 1_000_000
    )
    token = Cookies(name="authtoken", expires_utc=expires_utc_future)
    assert not is_expired(token)

    expires_utc_past = int(
        (datetime.now(UTC) - timedelta(hours=1) - datetime(1601, 1, 1, tzinfo=UTC)).total_seconds() * 1_000_000
    )
    token = Cookies(name="authtoken", expires_utc=expires_utc_past)
    assert is_expired(token)


def test_select_token(tmp_path: Path):
    test_token = CookiesFactory.build()
    expected = test_token.dict()
    tmp_db_path = str(tmp_path / "testing.db")
    engine = create_engine(f"sqlite:///{tmp_db_path}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(test_token)
        session.commit()

    result = select_token(engine, "authtoken")
    assert result.dict() == expected


def test_select_token_not_found(tmp_path: Path):
    test_token = CookiesFactory.build()
    tmp_db_path = str(tmp_path / "testing.db")
    engine = create_engine(f"sqlite:///{tmp_db_path}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(test_token)
        session.commit()

    with pytest.raises(ValueError, match="No auth token with name 'unknowntoken' found"):
        select_token(engine, "unknowntoken")

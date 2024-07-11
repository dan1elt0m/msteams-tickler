from datetime import datetime, timedelta
from pathlib import Path

import pytest
from msteams_tickler.models import Cookies
from msteams_tickler.token import is_expired, select_token
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel


class CookiesFactory(ModelFactory):
    __model__ = Cookies
    name = "authtoken"


def test_is_expired():
    expires_utc_future = int((datetime.now() + timedelta(hours=1) - datetime(1601, 1, 1)).total_seconds() * 1_000_000)
    token = Cookies(name="authtoken", expires_utc=expires_utc_future)
    assert not is_expired(token)

    expires_utc_past = int((datetime.now() - timedelta(hours=1) - datetime(1601, 1, 1)).total_seconds() * 1_000_000)
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

import logging
import os
from datetime import UTC, datetime
from typing import Optional

import pytz
import typer
from sqlalchemy import Engine, create_engine
from sqlmodel import Session, select

from msteams_tickler.classic.config import DEFAULT_COOKIES_PATH
from msteams_tickler.classic.models import Cookies
from msteams_tickler.notify import notify

logger = logging.getLogger(__name__)

classic_cli = typer.Typer(help="Teams classic")


def select_token(engine: Engine, token_name: str) -> Cookies:
    """Queries the cookies table for the provided token_name"""
    with Session(engine) as session:
        stmt = select(Cookies).where(Cookies.name == token_name)
        result = session.exec(stmt).first()
        if not result:
            raise ValueError(f"No auth token with name '{token_name}' found")
        return result


def is_expired(token: Cookies) -> bool:
    """Checks whether token is expired"""
    logger.info(f"token expires at: {token.expires_datetime}")
    return pytz.utc.localize(token.expires_datetime) < datetime.now(UTC)


@classic_cli.command()
def check(cookies_path: Optional[str] = DEFAULT_COOKIES_PATH, token_name: str = "SSOAUTHCOOKIE"):
    """Teams Token Expiration Checker CLI tool"""

    if cookies_path.startswith("~"):
        cookies_path = os.path.expanduser(cookies_path)

    sqlite_url = f"sqlite:///{cookies_path}"

    engine = create_engine(sqlite_url)
    auth_token = select_token(engine, token_name)

    if is_expired(auth_token):
        notify(message="Time to login again!", title="Token expired!", app_name="Microsoft Teams", sound_name="beep")

    print(f"Token is still valid until {pytz.utc.localize(auth_token.expires_datetime).isoformat()}")  # noqa: T201

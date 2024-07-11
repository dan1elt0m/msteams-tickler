import logging
from datetime import datetime

from msteams_tickler.models import Cookies
from sqlalchemy import Engine
from sqlmodel import Session, select

logger = logging.getLogger(__name__)


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
    return token.expires_datetime < datetime.now()

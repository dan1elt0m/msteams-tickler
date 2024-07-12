import logging
import os
from datetime import UTC, datetime
from typing import Optional

import pytz
import typer
from binary_cookies_parser.models import Cookie
from binary_cookies_parser.parser import read_binary_cookies_file

from msteams_tickler.classic.token import classic_cli
from msteams_tickler.config import DEFAULT_COOKIES_PATH
from msteams_tickler.notify import notify

logger = logging.getLogger(__name__)

main_cli = typer.Typer()
main_cli.add_typer(classic_cli, name="classic")


def is_expired(token: Cookie) -> bool:
    """Checks whether token is expired"""
    return pytz.utc.localize(token.expiry_datetime) < datetime.now(UTC)


@main_cli.command()
def check(cookies_path: Optional[str] = DEFAULT_COOKIES_PATH, token_name: str = "fpc"):
    if cookies_path.startswith("~"):
        cookies_path = os.path.expanduser(cookies_path)

    [token] = [cookie for cookie in read_binary_cookies_file(cookies_path) if cookie.name == token_name]
    if not token:
        raise ValueError(f"No auth token with name '{token_name}' found")

    if is_expired(token):
        notify(message="Time to login again!", title="Token expired!", app_name="Microsoft Teams", sound_name="beep")
        print("Token expired!")  # noqa: T201

    print(f"Token is still valid until {pytz.utc.localize(token.expiry_datetime).isoformat()}")  # noqa: T201


def main():
    """Entry point for the CLI tool"""
    main_cli()


if __name__ == "__main__":
    typer.run(main)

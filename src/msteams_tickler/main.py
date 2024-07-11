import os
import platform
from typing import Optional

import typer
from msteams_tickler.notify import notify
from msteams_tickler.token import is_expired, select_token
from sqlmodel import create_engine

DEFAULT_COOKIES_PATH = "~/Library/Application Support/Microsoft/Teams/Cookies"


def check_os():
    """Checks if the OS is macOS, raises an error if not."""
    if platform.system() != "Darwin":
        raise NotImplementedError("This tool only supports macOS")


def tickle_token(cookies_path: Optional[str] = DEFAULT_COOKIES_PATH, token_name: str = "authtoken"):
    """Teams Token Expiration Checker CLI tool"""
    check_os()

    if cookies_path.startswith("~"):
        cookies_path = os.path.expanduser(cookies_path)

    sqlite_url = f"sqlite:///{cookies_path}"

    engine = create_engine(sqlite_url)
    auth_token = select_token(engine, token_name)

    if is_expired(auth_token):
        notify()


def main():
    """Entry point for the CLI tool"""
    typer.run(tickle_token)


if __name__ == "__main__":
    typer.run(main)

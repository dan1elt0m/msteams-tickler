from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import Field, SQLModel


def convert_utc_to_datetime(utc_timestamp: int) -> datetime:
    # Chromium's timestamp is the number of microseconds since January 1, 1601
    chromium_epoch = datetime(1601, 1, 1)
    return chromium_epoch + timedelta(microseconds=utc_timestamp)


class Cookies(SQLModel, table=True):
    creation_utc: Optional[int] = Field(default=None)
    host_key: Optional[str] = Field(default=None)
    top_frame_site_key: Optional[str] = Field(default=None)
    name: str = Field(primary_key=True)
    value: Optional[str] = Field(default=None)
    encrypted_value: Optional[bytes] = Field(default=None)
    path: Optional[str] = Field(default=None)
    expires_utc: Optional[int] = Field(default=None)
    is_secure: Optional[int] = Field(default=None)
    is_httponly: Optional[int] = Field(default=None)
    last_access_utc: Optional[int] = Field(default=None)
    has_expires: Optional[int] = Field(default=None)
    is_persistent: Optional[int] = Field(default=None)
    priority: Optional[int] = Field(default=None)
    samesite: Optional[int] = Field(default=None)
    source_scheme: Optional[int] = Field(default=None)
    source_port: Optional[int] = Field(default=None)
    is_same_party: Optional[int] = Field(default=None)

    @property
    def expires_datetime(self) -> Optional[datetime]:
        return convert_utc_to_datetime(self.expires_utc) if self.expires_utc else None

    @property
    def creation_datetime(self) -> Optional[datetime]:
        return convert_utc_to_datetime(self.creation_utc) if self.expires_utc else None

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class UserCreateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    favourite_color: Optional["Color"] = Field(alias="favouriteColor")
    location: Optional["LocationInput"]


class LocationInput(BaseModel):
    city: Optional[str]
    country: Optional[str]


class NotificationsPreferencesInput(BaseModel):
    receive_mails: bool = Field(alias="receiveMails")
    receive_push_notifications: bool = Field(alias="receivePushNotifications")
    receive_sms: bool = Field(alias="receiveSms")
    title: str


class UserPreferencesInput(BaseModel):
    lucky_number: Optional[int] = Field(alias="luckyNumber", default=7)
    favourite_word: Optional[str] = Field(alias="favouriteWord", default="word")
    color_opacity: Optional[float] = Field(alias="colorOpacity", default=1.0)
    excluded_tags: Optional[list[str]] = Field(
        alias="excludedTags", default_factory=lambda: ["offtop", "tag123"]
    )
    notifications_preferences: "NotificationsPreferencesInput" = Field(
        alias="notificationsPreferences",
        default=NotificationsPreferencesInput.parse_obj(
            {
                "receiveMails": True,
                "receivePushNotifications": True,
                "receiveSms": False,
                "title": "Mr",
            }
        ),
    )


UserCreateInput.update_forward_refs()
LocationInput.update_forward_refs()
NotificationsPreferencesInput.update_forward_refs()
UserPreferencesInput.update_forward_refs()

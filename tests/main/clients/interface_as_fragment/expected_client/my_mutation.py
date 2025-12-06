from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .fragments import Item, ItemError


class MyMutation(BaseModel):
    change_item: Optional["MyMutationChangeItem"]


class MyMutationChangeItem(BaseModel):
    contacts: Optional[list["MyMutationChangeItemContacts"]]
    errors: Optional[
        list[
            Annotated[
                Union["MyMutationChangeItemErrorsItemServiceInternalError",],
                Field(discriminator="typename__"),
            ]
        ]
    ]


class MyMutationChangeItemContacts(Item):
    pass


class MyMutationChangeItemErrorsItemServiceInternalError(ItemError):
    typename__: Literal["ItemServiceInternalError"] = Field(alias="__typename")


MyMutation.model_rebuild()
MyMutationChangeItem.model_rebuild()

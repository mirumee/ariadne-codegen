from typing import Annotated, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel


class ListUnion(BaseModel):
    query_list_u: List[
        Annotated[
            Union[
                "ListUnionQueryListUTypeA",
                "ListUnionQueryListUTypeB",
                "ListUnionQueryListUTypeC",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="queryListU")


class ListUnionQueryListUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class ListUnionQueryListUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


class ListUnionQueryListUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")


ListUnion.update_forward_refs()
ListUnionQueryListUTypeA.update_forward_refs()
ListUnionQueryListUTypeB.update_forward_refs()
ListUnionQueryListUTypeC.update_forward_refs()

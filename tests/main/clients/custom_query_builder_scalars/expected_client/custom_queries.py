from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from .custom_fields import CheckoutFields, OrderFields


class Query:
    @classmethod
    def checkout(cls, *, token: Optional[UUID] = None) -> CheckoutFields:
        arguments: dict[str, dict[str, Any]] = {
            "token": {"type": "UUID", "value": token}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CheckoutFields(field_name="checkout", arguments=cleared_arguments)

    @classmethod
    def order(cls, id: str, *, created_at: Optional[datetime] = None) -> OrderFields:
        arguments: dict[str, dict[str, Any]] = {
            "id": {"type": "ID!", "value": id},
            "createdAt": {"type": "DateTime", "value": created_at},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return OrderFields(field_name="order", arguments=cleared_arguments)

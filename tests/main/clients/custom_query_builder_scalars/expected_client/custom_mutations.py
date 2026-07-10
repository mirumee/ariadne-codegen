from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from .custom_fields import PaymentFields


class Mutation:
    @classmethod
    def create_payment(
        cls, amount: Decimal, *, requested_at: Optional[datetime] = None
    ) -> PaymentFields:
        arguments: dict[str, dict[str, Any]] = {
            "amount": {"type": "Decimal!", "value": amount},
            "requestedAt": {"type": "DateTime", "value": requested_at},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PaymentFields(field_name="createPayment", arguments=cleared_arguments)

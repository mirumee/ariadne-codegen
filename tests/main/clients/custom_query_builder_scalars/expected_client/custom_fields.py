from decimal import Decimal
from typing import Any, Optional, Union

from .base_operation import GraphQLField, GraphQLLeafField
from .custom_typing_fields import (
    CheckoutGraphQLField,
    OrderGraphQLField,
    PaymentGraphQLField,
    PaymentMethodGraphQLField,
)


class CheckoutFields(GraphQLField):
    id = GraphQLLeafField("id", CheckoutGraphQLField)

    @classmethod
    def stored_payment_methods(
        cls, *, amount: Optional[Decimal] = None
    ) -> "PaymentMethodFields":
        arguments: dict[str, dict[str, Any]] = {
            "amount": {"type": "Decimal", "value": amount}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PaymentMethodFields("storedPaymentMethods", arguments=cleared_arguments)

    def fields(
        self, *subfields: Union[CheckoutGraphQLField, "PaymentMethodFields"]
    ) -> "CheckoutFields":
        """Subfields should come from the CheckoutFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CheckoutFields":
        self._alias = alias
        return self


class OrderFields(GraphQLField):
    id = GraphQLLeafField("id", OrderGraphQLField)
    token = GraphQLLeafField("token", OrderGraphQLField)

    def fields(self, *subfields: OrderGraphQLField) -> "OrderFields":
        """Subfields should come from the OrderFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OrderFields":
        self._alias = alias
        return self


class PaymentFields(GraphQLField):
    id = GraphQLLeafField("id", PaymentGraphQLField)
    total = GraphQLLeafField("total", PaymentGraphQLField)

    def fields(self, *subfields: PaymentGraphQLField) -> "PaymentFields":
        """Subfields should come from the PaymentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PaymentFields":
        self._alias = alias
        return self


class PaymentMethodFields(GraphQLField):
    id = GraphQLLeafField("id", PaymentMethodGraphQLField)

    def fields(self, *subfields: PaymentMethodGraphQLField) -> "PaymentMethodFields":
        """Subfields should come from the PaymentMethodFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PaymentMethodFields":
        self._alias = alias
        return self

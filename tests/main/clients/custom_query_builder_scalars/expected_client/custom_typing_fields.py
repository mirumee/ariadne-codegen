from .base_operation import GraphQLField


class CheckoutGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "CheckoutGraphQLField":
        self._alias = alias
        return self


class PaymentMethodGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "PaymentMethodGraphQLField":
        self._alias = alias
        return self


class OrderGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "OrderGraphQLField":
        self._alias = alias
        return self


class PaymentGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "PaymentGraphQLField":
        self._alias = alias
        return self

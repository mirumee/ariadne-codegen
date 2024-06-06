from .base_operation import GraphQLField


class WebhookGraphQLField(GraphQLField):
    pass


class NodeInterface(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "NodeInterface":
        self._inline_fragments[type_name] = subfields
        return self


class WebhookEventGraphQLField(GraphQLField):
    pass


class WebhookEventSyncGraphQLField(GraphQLField):
    pass


class WebhookEventAsyncGraphQLField(GraphQLField):
    pass


class AppGraphQLField(GraphQLField):
    pass


class ObjectWithMetadataInterface(GraphQLField):
    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "ObjectWithMetadataInterface":
        self._inline_fragments[type_name] = subfields
        return self


class MetadataItemGraphQLField(GraphQLField):
    pass


class PermissionGraphQLField(GraphQLField):
    pass


class AppTokenGraphQLField(GraphQLField):
    pass


class AppExtensionGraphQLField(GraphQLField):
    pass


class AppBrandGraphQLField(GraphQLField):
    pass


class AppBrandLogoGraphQLField(GraphQLField):
    pass


class EventDeliveryCountableConnectionGraphQLField(GraphQLField):
    pass


class PageInfoGraphQLField(GraphQLField):
    pass


class EventDeliveryCountableEdgeGraphQLField(GraphQLField):
    pass


class EventDeliveryGraphQLField(GraphQLField):
    pass


class EventDeliveryAttemptCountableConnectionGraphQLField(GraphQLField):
    pass


class EventDeliveryAttemptCountableEdgeGraphQLField(GraphQLField):
    pass


class EventDeliveryAttemptGraphQLField(GraphQLField):
    pass


class WarehouseGraphQLField(GraphQLField):
    pass


class AddressGraphQLField(GraphQLField):
    pass


class CountryDisplayGraphQLField(GraphQLField):
    pass


class VATGraphQLField(GraphQLField):
    pass


class ReducedRateGraphQLField(GraphQLField):
    pass


class ShippingZoneCountableConnectionGraphQLField(GraphQLField):
    pass


class ShippingZoneCountableEdgeGraphQLField(GraphQLField):
    pass


class ShippingZoneGraphQLField(GraphQLField):
    pass


class MoneyRangeGraphQLField(GraphQLField):
    pass


class MoneyGraphQLField(GraphQLField):
    pass


class ShippingMethodTypeGraphQLField(GraphQLField):
    pass


class ShippingMethodTranslationGraphQLField(GraphQLField):
    pass


class LanguageDisplayGraphQLField(GraphQLField):
    pass


class ShippingMethodTranslatableContentGraphQLField(GraphQLField):
    pass


class ShippingMethodChannelListingGraphQLField(GraphQLField):
    pass


class ChannelGraphQLField(GraphQLField):
    pass


class ShippingMethodsPerCountryGraphQLField(GraphQLField):
    pass


class ShippingMethodGraphQLField(GraphQLField):
    pass


class WeightGraphQLField(GraphQLField):
    pass


class StockSettingsGraphQLField(GraphQLField):
    pass


class OrderSettingsGraphQLField(GraphQLField):
    pass


class CheckoutSettingsGraphQLField(GraphQLField):
    pass


class PaymentSettingsGraphQLField(GraphQLField):
    pass


class TaxConfigurationGraphQLField(GraphQLField):
    pass


class TaxConfigurationPerCountryGraphQLField(GraphQLField):
    pass


class ShippingMethodPostalCodeRuleGraphQLField(GraphQLField):
    pass


class ProductCountableConnectionGraphQLField(GraphQLField):
    pass


class ProductCountableEdgeGraphQLField(GraphQLField):
    pass


class ProductGraphQLField(GraphQLField):
    pass


class ProductTypeGraphQLField(GraphQLField):
    pass


class TaxTypeGraphQLField(GraphQLField):
    pass


class TaxClassGraphQLField(GraphQLField):
    pass


class TaxClassCountryRateGraphQLField(GraphQLField):
    pass


class AttributeGraphQLField(GraphQLField):
    pass


class AttributeValueCountableConnectionGraphQLField(GraphQLField):
    pass


class AttributeValueCountableEdgeGraphQLField(GraphQLField):
    pass


class AttributeValueGraphQLField(GraphQLField):
    pass


class AttributeValueTranslationGraphQLField(GraphQLField):
    pass


class AttributeValueTranslatableContentGraphQLField(GraphQLField):
    pass


class AttributeTranslatableContentGraphQLField(GraphQLField):
    pass


class AttributeTranslationGraphQLField(GraphQLField):
    pass


class FileGraphQLField(GraphQLField):
    pass


class ProductTypeCountableConnectionGraphQLField(GraphQLField):
    pass


class ProductTypeCountableEdgeGraphQLField(GraphQLField):
    pass


class AssignedVariantAttributeGraphQLField(GraphQLField):
    pass


class AttributeCountableConnectionGraphQLField(GraphQLField):
    pass


class AttributeCountableEdgeGraphQLField(GraphQLField):
    pass


class CategoryGraphQLField(GraphQLField):
    pass


class CategoryCountableConnectionGraphQLField(GraphQLField):
    pass


class CategoryCountableEdgeGraphQLField(GraphQLField):
    pass


class ImageGraphQLField(GraphQLField):
    pass


class CategoryTranslationGraphQLField(GraphQLField):
    pass


class CategoryTranslatableContentGraphQLField(GraphQLField):
    pass


class ProductVariantGraphQLField(GraphQLField):
    pass


class ProductVariantChannelListingGraphQLField(GraphQLField):
    pass


class PreorderThresholdGraphQLField(GraphQLField):
    pass


class VariantPricingInfoGraphQLField(GraphQLField):
    pass


class TaxedMoneyGraphQLField(GraphQLField):
    pass


class SelectedAttributeGraphQLField(GraphQLField):
    pass


class ProductImageGraphQLField(GraphQLField):
    pass


class ProductMediaGraphQLField(GraphQLField):
    pass


class ProductVariantTranslationGraphQLField(GraphQLField):
    pass


class ProductVariantTranslatableContentGraphQLField(GraphQLField):
    pass


class DigitalContentGraphQLField(GraphQLField):
    pass


class DigitalContentUrlGraphQLField(GraphQLField):
    pass


class StockGraphQLField(GraphQLField):
    pass


class PreorderDataGraphQLField(GraphQLField):
    pass


class ProductPricingInfoGraphQLField(GraphQLField):
    pass


class TaxedMoneyRangeGraphQLField(GraphQLField):
    pass


class ProductChannelListingGraphQLField(GraphQLField):
    pass


class MarginGraphQLField(GraphQLField):
    pass


class CollectionGraphQLField(GraphQLField):
    pass


class CollectionTranslationGraphQLField(GraphQLField):
    pass


class CollectionTranslatableContentGraphQLField(GraphQLField):
    pass


class CollectionChannelListingGraphQLField(GraphQLField):
    pass


class ProductTranslationGraphQLField(GraphQLField):
    pass


class ProductTranslatableContentGraphQLField(GraphQLField):
    pass


class StockCountableConnectionGraphQLField(GraphQLField):
    pass


class StockCountableEdgeGraphQLField(GraphQLField):
    pass


class WarehouseCountableConnectionGraphQLField(GraphQLField):
    pass


class WarehouseCountableEdgeGraphQLField(GraphQLField):
    pass


class TranslatableItemConnectionGraphQLField(GraphQLField):
    pass


class TranslatableItemEdgeGraphQLField(GraphQLField):
    pass


class TranslatableItemUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "TranslatableItemUnion":
        self._inline_fragments[type_name] = subfields
        return self


class PageTranslatableContentGraphQLField(GraphQLField):
    pass


class PageTranslationGraphQLField(GraphQLField):
    pass


class PageGraphQLField(GraphQLField):
    pass


class PageTypeGraphQLField(GraphQLField):
    pass


class VoucherTranslatableContentGraphQLField(GraphQLField):
    pass


class VoucherTranslationGraphQLField(GraphQLField):
    pass


class VoucherGraphQLField(GraphQLField):
    pass


class VoucherCodeCountableConnectionGraphQLField(GraphQLField):
    pass


class VoucherCodeCountableEdgeGraphQLField(GraphQLField):
    pass


class VoucherCodeGraphQLField(GraphQLField):
    pass


class CollectionCountableConnectionGraphQLField(GraphQLField):
    pass


class CollectionCountableEdgeGraphQLField(GraphQLField):
    pass


class ProductVariantCountableConnectionGraphQLField(GraphQLField):
    pass


class ProductVariantCountableEdgeGraphQLField(GraphQLField):
    pass


class VoucherChannelListingGraphQLField(GraphQLField):
    pass


class MenuItemTranslatableContentGraphQLField(GraphQLField):
    pass


class MenuItemTranslationGraphQLField(GraphQLField):
    pass


class MenuItemGraphQLField(GraphQLField):
    pass


class MenuGraphQLField(GraphQLField):
    pass


class PromotionTranslatableContentGraphQLField(GraphQLField):
    pass


class PromotionTranslationGraphQLField(GraphQLField):
    pass


class PromotionRuleTranslatableContentGraphQLField(GraphQLField):
    pass


class PromotionRuleTranslationGraphQLField(GraphQLField):
    pass


class SaleTranslatableContentGraphQLField(GraphQLField):
    pass


class SaleTranslationGraphQLField(GraphQLField):
    pass


class SaleGraphQLField(GraphQLField):
    pass


class SaleChannelListingGraphQLField(GraphQLField):
    pass


class TaxConfigurationCountableConnectionGraphQLField(GraphQLField):
    pass


class TaxConfigurationCountableEdgeGraphQLField(GraphQLField):
    pass


class TaxClassCountableConnectionGraphQLField(GraphQLField):
    pass


class TaxClassCountableEdgeGraphQLField(GraphQLField):
    pass


class TaxCountryConfigurationGraphQLField(GraphQLField):
    pass


class ShopGraphQLField(GraphQLField):
    pass


class PaymentGatewayGraphQLField(GraphQLField):
    pass


class GatewayConfigLineGraphQLField(GraphQLField):
    pass


class ExternalAuthenticationGraphQLField(GraphQLField):
    pass


class DomainGraphQLField(GraphQLField):
    pass


class ShopTranslationGraphQLField(GraphQLField):
    pass


class StaffNotificationRecipientGraphQLField(GraphQLField):
    pass


class UserGraphQLField(GraphQLField):
    pass


class CheckoutGraphQLField(GraphQLField):
    pass


class GiftCardGraphQLField(GraphQLField):
    pass


class GiftCardEventGraphQLField(GraphQLField):
    pass


class GiftCardEventBalanceGraphQLField(GraphQLField):
    pass


class GiftCardTagGraphQLField(GraphQLField):
    pass


class CheckoutLineGraphQLField(GraphQLField):
    pass


class CheckoutLineProblemUnion(GraphQLField):
    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "CheckoutLineProblemUnion":
        self._inline_fragments[type_name] = subfields
        return self


class CheckoutLineProblemInsufficientStockGraphQLField(GraphQLField):
    pass


class CheckoutLineProblemVariantNotAvailableGraphQLField(GraphQLField):
    pass


class DeliveryMethodUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "DeliveryMethodUnion":
        self._inline_fragments[type_name] = subfields
        return self


class TransactionItemGraphQLField(GraphQLField):
    pass


class OrderGraphQLField(GraphQLField):
    pass


class FulfillmentGraphQLField(GraphQLField):
    pass


class FulfillmentLineGraphQLField(GraphQLField):
    pass


class OrderLineGraphQLField(GraphQLField):
    pass


class AllocationGraphQLField(GraphQLField):
    pass


class InvoiceGraphQLField(GraphQLField):
    pass


class JobInterface(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "JobInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PaymentGraphQLField(GraphQLField):
    pass


class TransactionGraphQLField(GraphQLField):
    pass


class CreditCardGraphQLField(GraphQLField):
    pass


class OrderEventGraphQLField(GraphQLField):
    pass


class OrderEventOrderLineObjectGraphQLField(GraphQLField):
    pass


class OrderEventDiscountObjectGraphQLField(GraphQLField):
    pass


class OrderDiscountGraphQLField(GraphQLField):
    pass


class OrderErrorGraphQLField(GraphQLField):
    pass


class OrderGrantedRefundGraphQLField(GraphQLField):
    pass


class OrderGrantedRefundLineGraphQLField(GraphQLField):
    pass


class TransactionEventGraphQLField(GraphQLField):
    pass


class UserOrAppUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "UserOrAppUnion":
        self._inline_fragments[type_name] = subfields
        return self


class StoredPaymentMethodGraphQLField(GraphQLField):
    pass


class CheckoutProblemUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "CheckoutProblemUnion":
        self._inline_fragments[type_name] = subfields
        return self


class CheckoutCountableConnectionGraphQLField(GraphQLField):
    pass


class CheckoutCountableEdgeGraphQLField(GraphQLField):
    pass


class GiftCardCountableConnectionGraphQLField(GraphQLField):
    pass


class GiftCardCountableEdgeGraphQLField(GraphQLField):
    pass


class OrderCountableConnectionGraphQLField(GraphQLField):
    pass


class OrderCountableEdgeGraphQLField(GraphQLField):
    pass


class UserPermissionGraphQLField(GraphQLField):
    pass


class GroupGraphQLField(GraphQLField):
    pass


class CustomerEventGraphQLField(GraphQLField):
    pass


class PaymentSourceGraphQLField(GraphQLField):
    pass


class LimitInfoGraphQLField(GraphQLField):
    pass


class LimitsGraphQLField(GraphQLField):
    pass


class GiftCardSettingsGraphQLField(GraphQLField):
    pass


class TimePeriodGraphQLField(GraphQLField):
    pass


class DigitalContentCountableConnectionGraphQLField(GraphQLField):
    pass


class DigitalContentCountableEdgeGraphQLField(GraphQLField):
    pass


class PaymentCountableConnectionGraphQLField(GraphQLField):
    pass


class PaymentCountableEdgeGraphQLField(GraphQLField):
    pass


class PageCountableConnectionGraphQLField(GraphQLField):
    pass


class PageCountableEdgeGraphQLField(GraphQLField):
    pass


class PageTypeCountableConnectionGraphQLField(GraphQLField):
    pass


class PageTypeCountableEdgeGraphQLField(GraphQLField):
    pass


class OrderEventCountableConnectionGraphQLField(GraphQLField):
    pass


class OrderEventCountableEdgeGraphQLField(GraphQLField):
    pass


class MenuCountableConnectionGraphQLField(GraphQLField):
    pass


class MenuCountableEdgeGraphQLField(GraphQLField):
    pass


class MenuItemCountableConnectionGraphQLField(GraphQLField):
    pass


class MenuItemCountableEdgeGraphQLField(GraphQLField):
    pass


class GiftCardTagCountableConnectionGraphQLField(GraphQLField):
    pass


class GiftCardTagCountableEdgeGraphQLField(GraphQLField):
    pass


class PluginGraphQLField(GraphQLField):
    pass


class PluginConfigurationGraphQLField(GraphQLField):
    pass


class ConfigurationItemGraphQLField(GraphQLField):
    pass


class PluginCountableConnectionGraphQLField(GraphQLField):
    pass


class PluginCountableEdgeGraphQLField(GraphQLField):
    pass


class SaleCountableConnectionGraphQLField(GraphQLField):
    pass


class SaleCountableEdgeGraphQLField(GraphQLField):
    pass


class VoucherCountableConnectionGraphQLField(GraphQLField):
    pass


class VoucherCountableEdgeGraphQLField(GraphQLField):
    pass


class PromotionGraphQLField(GraphQLField):
    pass


class PromotionRuleGraphQLField(GraphQLField):
    pass


class PromotionEventUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "PromotionEventUnion":
        self._inline_fragments[type_name] = subfields
        return self


class PromotionCreatedEventGraphQLField(GraphQLField):
    pass


class PromotionEventInterfaceInterface(GraphQLField):
    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "PromotionEventInterfaceInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PromotionUpdatedEventGraphQLField(GraphQLField):
    pass


class PromotionStartedEventGraphQLField(GraphQLField):
    pass


class PromotionEndedEventGraphQLField(GraphQLField):
    pass


class PromotionRuleCreatedEventGraphQLField(GraphQLField):
    pass


class PromotionRuleEventInterfaceInterface(GraphQLField):
    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "PromotionRuleEventInterfaceInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PromotionRuleUpdatedEventGraphQLField(GraphQLField):
    pass


class PromotionRuleDeletedEventGraphQLField(GraphQLField):
    pass


class PromotionCountableConnectionGraphQLField(GraphQLField):
    pass


class PromotionCountableEdgeGraphQLField(GraphQLField):
    pass


class ExportFileGraphQLField(GraphQLField):
    pass


class ExportEventGraphQLField(GraphQLField):
    pass


class ExportFileCountableConnectionGraphQLField(GraphQLField):
    pass


class ExportFileCountableEdgeGraphQLField(GraphQLField):
    pass


class CheckoutLineCountableConnectionGraphQLField(GraphQLField):
    pass


class CheckoutLineCountableEdgeGraphQLField(GraphQLField):
    pass


class AppInstallationGraphQLField(GraphQLField):
    pass


class AppCountableConnectionGraphQLField(GraphQLField):
    pass


class AppCountableEdgeGraphQLField(GraphQLField):
    pass


class AppExtensionCountableConnectionGraphQLField(GraphQLField):
    pass


class AppExtensionCountableEdgeGraphQLField(GraphQLField):
    pass


class AddressValidationDataGraphQLField(GraphQLField):
    pass


class ChoiceValueGraphQLField(GraphQLField):
    pass


class UserCountableConnectionGraphQLField(GraphQLField):
    pass


class UserCountableEdgeGraphQLField(GraphQLField):
    pass


class GroupCountableConnectionGraphQLField(GraphQLField):
    pass


class GroupCountableEdgeGraphQLField(GraphQLField):
    pass


class WebhookCreateGraphQLField(GraphQLField):
    pass


class WebhookErrorGraphQLField(GraphQLField):
    pass


class WebhookDeleteGraphQLField(GraphQLField):
    pass


class WebhookUpdateGraphQLField(GraphQLField):
    pass


class EventDeliveryRetryGraphQLField(GraphQLField):
    pass


class WebhookDryRunGraphQLField(GraphQLField):
    pass


class WebhookDryRunErrorGraphQLField(GraphQLField):
    pass


class WebhookTriggerGraphQLField(GraphQLField):
    pass


class WebhookTriggerErrorGraphQLField(GraphQLField):
    pass


class WarehouseCreateGraphQLField(GraphQLField):
    pass


class WarehouseErrorGraphQLField(GraphQLField):
    pass


class WarehouseUpdateGraphQLField(GraphQLField):
    pass


class WarehouseDeleteGraphQLField(GraphQLField):
    pass


class WarehouseShippingZoneAssignGraphQLField(GraphQLField):
    pass


class WarehouseShippingZoneUnassignGraphQLField(GraphQLField):
    pass


class TaxClassCreateGraphQLField(GraphQLField):
    pass


class TaxClassCreateErrorGraphQLField(GraphQLField):
    pass


class TaxClassDeleteGraphQLField(GraphQLField):
    pass


class TaxClassDeleteErrorGraphQLField(GraphQLField):
    pass


class TaxClassUpdateGraphQLField(GraphQLField):
    pass


class TaxClassUpdateErrorGraphQLField(GraphQLField):
    pass


class TaxConfigurationUpdateGraphQLField(GraphQLField):
    pass


class TaxConfigurationUpdateErrorGraphQLField(GraphQLField):
    pass


class TaxCountryConfigurationUpdateGraphQLField(GraphQLField):
    pass


class TaxCountryConfigurationUpdateErrorGraphQLField(GraphQLField):
    pass


class TaxCountryConfigurationDeleteGraphQLField(GraphQLField):
    pass


class TaxCountryConfigurationDeleteErrorGraphQLField(GraphQLField):
    pass


class TaxExemptionManageGraphQLField(GraphQLField):
    pass


class TaxSourceObjectUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "TaxSourceObjectUnion":
        self._inline_fragments[type_name] = subfields
        return self


class TaxExemptionManageErrorGraphQLField(GraphQLField):
    pass


class StockBulkUpdateGraphQLField(GraphQLField):
    pass


class StockBulkResultGraphQLField(GraphQLField):
    pass


class StockBulkUpdateErrorGraphQLField(GraphQLField):
    pass


class StaffNotificationRecipientCreateGraphQLField(GraphQLField):
    pass


class ShopErrorGraphQLField(GraphQLField):
    pass


class StaffNotificationRecipientUpdateGraphQLField(GraphQLField):
    pass


class StaffNotificationRecipientDeleteGraphQLField(GraphQLField):
    pass


class ShopDomainUpdateGraphQLField(GraphQLField):
    pass


class ShopSettingsUpdateGraphQLField(GraphQLField):
    pass


class ShopFetchTaxRatesGraphQLField(GraphQLField):
    pass


class ShopSettingsTranslateGraphQLField(GraphQLField):
    pass


class TranslationErrorGraphQLField(GraphQLField):
    pass


class ShopAddressUpdateGraphQLField(GraphQLField):
    pass


class OrderSettingsUpdateGraphQLField(GraphQLField):
    pass


class OrderSettingsErrorGraphQLField(GraphQLField):
    pass


class GiftCardSettingsUpdateGraphQLField(GraphQLField):
    pass


class GiftCardSettingsErrorGraphQLField(GraphQLField):
    pass


class ShippingMethodChannelListingUpdateGraphQLField(GraphQLField):
    pass


class ShippingErrorGraphQLField(GraphQLField):
    pass


class ShippingPriceCreateGraphQLField(GraphQLField):
    pass


class ShippingPriceDeleteGraphQLField(GraphQLField):
    pass


class ShippingPriceBulkDeleteGraphQLField(GraphQLField):
    pass


class ShippingPriceUpdateGraphQLField(GraphQLField):
    pass


class ShippingPriceTranslateGraphQLField(GraphQLField):
    pass


class ShippingPriceExcludeProductsGraphQLField(GraphQLField):
    pass


class ShippingPriceRemoveProductFromExcludeGraphQLField(GraphQLField):
    pass


class ShippingZoneCreateGraphQLField(GraphQLField):
    pass


class ShippingZoneDeleteGraphQLField(GraphQLField):
    pass


class ShippingZoneBulkDeleteGraphQLField(GraphQLField):
    pass


class ShippingZoneUpdateGraphQLField(GraphQLField):
    pass


class ProductAttributeAssignGraphQLField(GraphQLField):
    pass


class ProductErrorGraphQLField(GraphQLField):
    pass


class ProductAttributeAssignmentUpdateGraphQLField(GraphQLField):
    pass


class ProductAttributeUnassignGraphQLField(GraphQLField):
    pass


class CategoryCreateGraphQLField(GraphQLField):
    pass


class CategoryDeleteGraphQLField(GraphQLField):
    pass


class CategoryBulkDeleteGraphQLField(GraphQLField):
    pass


class CategoryUpdateGraphQLField(GraphQLField):
    pass


class CategoryTranslateGraphQLField(GraphQLField):
    pass


class CollectionAddProductsGraphQLField(GraphQLField):
    pass


class CollectionErrorGraphQLField(GraphQLField):
    pass


class CollectionCreateGraphQLField(GraphQLField):
    pass


class CollectionDeleteGraphQLField(GraphQLField):
    pass


class CollectionReorderProductsGraphQLField(GraphQLField):
    pass


class CollectionBulkDeleteGraphQLField(GraphQLField):
    pass


class CollectionRemoveProductsGraphQLField(GraphQLField):
    pass


class CollectionUpdateGraphQLField(GraphQLField):
    pass


class CollectionTranslateGraphQLField(GraphQLField):
    pass


class CollectionChannelListingUpdateGraphQLField(GraphQLField):
    pass


class CollectionChannelListingErrorGraphQLField(GraphQLField):
    pass


class ProductCreateGraphQLField(GraphQLField):
    pass


class ProductDeleteGraphQLField(GraphQLField):
    pass


class ProductBulkCreateGraphQLField(GraphQLField):
    pass


class ProductBulkResultGraphQLField(GraphQLField):
    pass


class ProductBulkCreateErrorGraphQLField(GraphQLField):
    pass


class ProductBulkDeleteGraphQLField(GraphQLField):
    pass


class ProductUpdateGraphQLField(GraphQLField):
    pass


class ProductBulkTranslateGraphQLField(GraphQLField):
    pass


class ProductBulkTranslateResultGraphQLField(GraphQLField):
    pass


class ProductBulkTranslateErrorGraphQLField(GraphQLField):
    pass


class ProductTranslateGraphQLField(GraphQLField):
    pass


class ProductChannelListingUpdateGraphQLField(GraphQLField):
    pass


class ProductChannelListingErrorGraphQLField(GraphQLField):
    pass


class ProductMediaCreateGraphQLField(GraphQLField):
    pass


class ProductVariantReorderGraphQLField(GraphQLField):
    pass


class ProductMediaDeleteGraphQLField(GraphQLField):
    pass


class ProductMediaBulkDeleteGraphQLField(GraphQLField):
    pass


class ProductMediaReorderGraphQLField(GraphQLField):
    pass


class ProductMediaUpdateGraphQLField(GraphQLField):
    pass


class ProductTypeCreateGraphQLField(GraphQLField):
    pass


class ProductTypeDeleteGraphQLField(GraphQLField):
    pass


class ProductTypeBulkDeleteGraphQLField(GraphQLField):
    pass


class ProductTypeUpdateGraphQLField(GraphQLField):
    pass


class ProductTypeReorderAttributesGraphQLField(GraphQLField):
    pass


class ProductReorderAttributeValuesGraphQLField(GraphQLField):
    pass


class DigitalContentCreateGraphQLField(GraphQLField):
    pass


class DigitalContentDeleteGraphQLField(GraphQLField):
    pass


class DigitalContentUpdateGraphQLField(GraphQLField):
    pass


class DigitalContentUrlCreateGraphQLField(GraphQLField):
    pass


class ProductVariantCreateGraphQLField(GraphQLField):
    pass


class ProductVariantDeleteGraphQLField(GraphQLField):
    pass


class ProductVariantBulkCreateGraphQLField(GraphQLField):
    pass


class ProductVariantBulkResultGraphQLField(GraphQLField):
    pass


class ProductVariantBulkErrorGraphQLField(GraphQLField):
    pass


class BulkProductErrorGraphQLField(GraphQLField):
    pass


class ProductVariantBulkUpdateGraphQLField(GraphQLField):
    pass


class ProductVariantBulkDeleteGraphQLField(GraphQLField):
    pass


class ProductVariantStocksCreateGraphQLField(GraphQLField):
    pass


class BulkStockErrorGraphQLField(GraphQLField):
    pass


class ProductVariantStocksDeleteGraphQLField(GraphQLField):
    pass


class StockErrorGraphQLField(GraphQLField):
    pass


class ProductVariantStocksUpdateGraphQLField(GraphQLField):
    pass


class ProductVariantUpdateGraphQLField(GraphQLField):
    pass


class ProductVariantSetDefaultGraphQLField(GraphQLField):
    pass


class ProductVariantTranslateGraphQLField(GraphQLField):
    pass


class ProductVariantBulkTranslateGraphQLField(GraphQLField):
    pass


class ProductVariantBulkTranslateResultGraphQLField(GraphQLField):
    pass


class ProductVariantBulkTranslateErrorGraphQLField(GraphQLField):
    pass


class ProductVariantChannelListingUpdateGraphQLField(GraphQLField):
    pass


class ProductVariantReorderAttributeValuesGraphQLField(GraphQLField):
    pass


class ProductVariantPreorderDeactivateGraphQLField(GraphQLField):
    pass


class VariantMediaAssignGraphQLField(GraphQLField):
    pass


class VariantMediaUnassignGraphQLField(GraphQLField):
    pass


class PaymentCaptureGraphQLField(GraphQLField):
    pass


class PaymentErrorGraphQLField(GraphQLField):
    pass


class PaymentRefundGraphQLField(GraphQLField):
    pass


class PaymentVoidGraphQLField(GraphQLField):
    pass


class PaymentInitializeGraphQLField(GraphQLField):
    pass


class PaymentInitializedGraphQLField(GraphQLField):
    pass


class PaymentCheckBalanceGraphQLField(GraphQLField):
    pass


class TransactionCreateGraphQLField(GraphQLField):
    pass


class TransactionCreateErrorGraphQLField(GraphQLField):
    pass


class TransactionUpdateGraphQLField(GraphQLField):
    pass


class TransactionUpdateErrorGraphQLField(GraphQLField):
    pass


class TransactionRequestActionGraphQLField(GraphQLField):
    pass


class TransactionRequestActionErrorGraphQLField(GraphQLField):
    pass


class TransactionRequestRefundForGrantedRefundGraphQLField(GraphQLField):
    pass


class TransactionRequestRefundForGrantedRefundErrorGraphQLField(GraphQLField):
    pass


class TransactionEventReportGraphQLField(GraphQLField):
    pass


class TransactionEventReportErrorGraphQLField(GraphQLField):
    pass


class PaymentGatewayInitializeGraphQLField(GraphQLField):
    pass


class PaymentGatewayConfigGraphQLField(GraphQLField):
    pass


class PaymentGatewayConfigErrorGraphQLField(GraphQLField):
    pass


class PaymentGatewayInitializeErrorGraphQLField(GraphQLField):
    pass


class TransactionInitializeGraphQLField(GraphQLField):
    pass


class TransactionInitializeErrorGraphQLField(GraphQLField):
    pass


class TransactionProcessGraphQLField(GraphQLField):
    pass


class TransactionProcessErrorGraphQLField(GraphQLField):
    pass


class StoredPaymentMethodRequestDeleteGraphQLField(GraphQLField):
    pass


class PaymentMethodRequestDeleteErrorGraphQLField(GraphQLField):
    pass


class PaymentGatewayInitializeTokenizationGraphQLField(GraphQLField):
    pass


class PaymentGatewayInitializeTokenizationErrorGraphQLField(GraphQLField):
    pass


class PaymentMethodInitializeTokenizationGraphQLField(GraphQLField):
    pass


class PaymentMethodInitializeTokenizationErrorGraphQLField(GraphQLField):
    pass


class PaymentMethodProcessTokenizationGraphQLField(GraphQLField):
    pass


class PaymentMethodProcessTokenizationErrorGraphQLField(GraphQLField):
    pass


class PageCreateGraphQLField(GraphQLField):
    pass


class PageErrorGraphQLField(GraphQLField):
    pass


class PageDeleteGraphQLField(GraphQLField):
    pass


class PageBulkDeleteGraphQLField(GraphQLField):
    pass


class PageBulkPublishGraphQLField(GraphQLField):
    pass


class PageUpdateGraphQLField(GraphQLField):
    pass


class PageTranslateGraphQLField(GraphQLField):
    pass


class PageTypeCreateGraphQLField(GraphQLField):
    pass


class PageTypeUpdateGraphQLField(GraphQLField):
    pass


class PageTypeDeleteGraphQLField(GraphQLField):
    pass


class PageTypeBulkDeleteGraphQLField(GraphQLField):
    pass


class PageAttributeAssignGraphQLField(GraphQLField):
    pass


class PageAttributeUnassignGraphQLField(GraphQLField):
    pass


class PageTypeReorderAttributesGraphQLField(GraphQLField):
    pass


class PageReorderAttributeValuesGraphQLField(GraphQLField):
    pass


class DraftOrderCompleteGraphQLField(GraphQLField):
    pass


class DraftOrderCreateGraphQLField(GraphQLField):
    pass


class DraftOrderDeleteGraphQLField(GraphQLField):
    pass


class DraftOrderBulkDeleteGraphQLField(GraphQLField):
    pass


class DraftOrderLinesBulkDeleteGraphQLField(GraphQLField):
    pass


class DraftOrderUpdateGraphQLField(GraphQLField):
    pass


class OrderAddNoteGraphQLField(GraphQLField):
    pass


class OrderCancelGraphQLField(GraphQLField):
    pass


class OrderCaptureGraphQLField(GraphQLField):
    pass


class OrderConfirmGraphQLField(GraphQLField):
    pass


class OrderFulfillGraphQLField(GraphQLField):
    pass


class FulfillmentCancelGraphQLField(GraphQLField):
    pass


class FulfillmentApproveGraphQLField(GraphQLField):
    pass


class FulfillmentUpdateTrackingGraphQLField(GraphQLField):
    pass


class FulfillmentRefundProductsGraphQLField(GraphQLField):
    pass


class FulfillmentReturnProductsGraphQLField(GraphQLField):
    pass


class OrderGrantRefundCreateGraphQLField(GraphQLField):
    pass


class OrderGrantRefundCreateErrorGraphQLField(GraphQLField):
    pass


class OrderGrantRefundCreateLineErrorGraphQLField(GraphQLField):
    pass


class OrderGrantRefundUpdateGraphQLField(GraphQLField):
    pass


class OrderGrantRefundUpdateErrorGraphQLField(GraphQLField):
    pass


class OrderGrantRefundUpdateLineErrorGraphQLField(GraphQLField):
    pass


class OrderLinesCreateGraphQLField(GraphQLField):
    pass


class OrderLineDeleteGraphQLField(GraphQLField):
    pass


class OrderLineUpdateGraphQLField(GraphQLField):
    pass


class OrderDiscountAddGraphQLField(GraphQLField):
    pass


class OrderDiscountUpdateGraphQLField(GraphQLField):
    pass


class OrderDiscountDeleteGraphQLField(GraphQLField):
    pass


class OrderLineDiscountUpdateGraphQLField(GraphQLField):
    pass


class OrderLineDiscountRemoveGraphQLField(GraphQLField):
    pass


class OrderNoteAddGraphQLField(GraphQLField):
    pass


class OrderNoteAddErrorGraphQLField(GraphQLField):
    pass


class OrderNoteUpdateGraphQLField(GraphQLField):
    pass


class OrderNoteUpdateErrorGraphQLField(GraphQLField):
    pass


class OrderMarkAsPaidGraphQLField(GraphQLField):
    pass


class OrderRefundGraphQLField(GraphQLField):
    pass


class OrderUpdateGraphQLField(GraphQLField):
    pass


class OrderUpdateShippingGraphQLField(GraphQLField):
    pass


class OrderVoidGraphQLField(GraphQLField):
    pass


class OrderBulkCancelGraphQLField(GraphQLField):
    pass


class OrderBulkCreateGraphQLField(GraphQLField):
    pass


class OrderBulkCreateResultGraphQLField(GraphQLField):
    pass


class OrderBulkCreateErrorGraphQLField(GraphQLField):
    pass


class DeleteMetadataGraphQLField(GraphQLField):
    pass


class MetadataErrorGraphQLField(GraphQLField):
    pass


class DeletePrivateMetadataGraphQLField(GraphQLField):
    pass


class UpdateMetadataGraphQLField(GraphQLField):
    pass


class UpdatePrivateMetadataGraphQLField(GraphQLField):
    pass


class AssignNavigationGraphQLField(GraphQLField):
    pass


class MenuErrorGraphQLField(GraphQLField):
    pass


class MenuCreateGraphQLField(GraphQLField):
    pass


class MenuDeleteGraphQLField(GraphQLField):
    pass


class MenuBulkDeleteGraphQLField(GraphQLField):
    pass


class MenuUpdateGraphQLField(GraphQLField):
    pass


class MenuItemCreateGraphQLField(GraphQLField):
    pass


class MenuItemDeleteGraphQLField(GraphQLField):
    pass


class MenuItemBulkDeleteGraphQLField(GraphQLField):
    pass


class MenuItemUpdateGraphQLField(GraphQLField):
    pass


class MenuItemTranslateGraphQLField(GraphQLField):
    pass


class MenuItemMoveGraphQLField(GraphQLField):
    pass


class InvoiceRequestGraphQLField(GraphQLField):
    pass


class InvoiceErrorGraphQLField(GraphQLField):
    pass


class InvoiceRequestDeleteGraphQLField(GraphQLField):
    pass


class InvoiceCreateGraphQLField(GraphQLField):
    pass


class InvoiceDeleteGraphQLField(GraphQLField):
    pass


class InvoiceUpdateGraphQLField(GraphQLField):
    pass


class InvoiceSendNotificationGraphQLField(GraphQLField):
    pass


class GiftCardActivateGraphQLField(GraphQLField):
    pass


class GiftCardErrorGraphQLField(GraphQLField):
    pass


class GiftCardCreateGraphQLField(GraphQLField):
    pass


class GiftCardDeleteGraphQLField(GraphQLField):
    pass


class GiftCardDeactivateGraphQLField(GraphQLField):
    pass


class GiftCardUpdateGraphQLField(GraphQLField):
    pass


class GiftCardResendGraphQLField(GraphQLField):
    pass


class GiftCardAddNoteGraphQLField(GraphQLField):
    pass


class GiftCardBulkCreateGraphQLField(GraphQLField):
    pass


class GiftCardBulkDeleteGraphQLField(GraphQLField):
    pass


class GiftCardBulkActivateGraphQLField(GraphQLField):
    pass


class GiftCardBulkDeactivateGraphQLField(GraphQLField):
    pass


class PluginUpdateGraphQLField(GraphQLField):
    pass


class PluginErrorGraphQLField(GraphQLField):
    pass


class ExternalNotificationTriggerGraphQLField(GraphQLField):
    pass


class ExternalNotificationErrorGraphQLField(GraphQLField):
    pass


class PromotionCreateGraphQLField(GraphQLField):
    pass


class PromotionCreateErrorGraphQLField(GraphQLField):
    pass


class PromotionUpdateGraphQLField(GraphQLField):
    pass


class PromotionUpdateErrorGraphQLField(GraphQLField):
    pass


class PromotionDeleteGraphQLField(GraphQLField):
    pass


class PromotionDeleteErrorGraphQLField(GraphQLField):
    pass


class PromotionRuleCreateGraphQLField(GraphQLField):
    pass


class PromotionRuleCreateErrorGraphQLField(GraphQLField):
    pass


class PromotionRuleUpdateGraphQLField(GraphQLField):
    pass


class PromotionRuleUpdateErrorGraphQLField(GraphQLField):
    pass


class PromotionRuleDeleteGraphQLField(GraphQLField):
    pass


class PromotionRuleDeleteErrorGraphQLField(GraphQLField):
    pass


class PromotionTranslateGraphQLField(GraphQLField):
    pass


class PromotionRuleTranslateGraphQLField(GraphQLField):
    pass


class PromotionBulkDeleteGraphQLField(GraphQLField):
    pass


class DiscountErrorGraphQLField(GraphQLField):
    pass


class SaleCreateGraphQLField(GraphQLField):
    pass


class SaleDeleteGraphQLField(GraphQLField):
    pass


class SaleBulkDeleteGraphQLField(GraphQLField):
    pass


class SaleUpdateGraphQLField(GraphQLField):
    pass


class SaleAddCataloguesGraphQLField(GraphQLField):
    pass


class SaleRemoveCataloguesGraphQLField(GraphQLField):
    pass


class SaleTranslateGraphQLField(GraphQLField):
    pass


class SaleChannelListingUpdateGraphQLField(GraphQLField):
    pass


class VoucherCreateGraphQLField(GraphQLField):
    pass


class VoucherDeleteGraphQLField(GraphQLField):
    pass


class VoucherBulkDeleteGraphQLField(GraphQLField):
    pass


class VoucherUpdateGraphQLField(GraphQLField):
    pass


class VoucherAddCataloguesGraphQLField(GraphQLField):
    pass


class VoucherRemoveCataloguesGraphQLField(GraphQLField):
    pass


class VoucherTranslateGraphQLField(GraphQLField):
    pass


class VoucherChannelListingUpdateGraphQLField(GraphQLField):
    pass


class VoucherCodeBulkDeleteGraphQLField(GraphQLField):
    pass


class VoucherCodeBulkDeleteErrorGraphQLField(GraphQLField):
    pass


class ExportProductsGraphQLField(GraphQLField):
    pass


class ExportErrorGraphQLField(GraphQLField):
    pass


class ExportGiftCardsGraphQLField(GraphQLField):
    pass


class ExportVoucherCodesGraphQLField(GraphQLField):
    pass


class FileUploadGraphQLField(GraphQLField):
    pass


class UploadErrorGraphQLField(GraphQLField):
    pass


class CheckoutAddPromoCodeGraphQLField(GraphQLField):
    pass


class CheckoutErrorGraphQLField(GraphQLField):
    pass


class CheckoutBillingAddressUpdateGraphQLField(GraphQLField):
    pass


class CheckoutCompleteGraphQLField(GraphQLField):
    pass


class CheckoutCreateGraphQLField(GraphQLField):
    pass


class CheckoutCreateFromOrderGraphQLField(GraphQLField):
    pass


class CheckoutCreateFromOrderUnavailableVariantGraphQLField(GraphQLField):
    pass


class CheckoutCreateFromOrderErrorGraphQLField(GraphQLField):
    pass


class CheckoutCustomerAttachGraphQLField(GraphQLField):
    pass


class CheckoutCustomerDetachGraphQLField(GraphQLField):
    pass


class CheckoutEmailUpdateGraphQLField(GraphQLField):
    pass


class CheckoutLineDeleteGraphQLField(GraphQLField):
    pass


class CheckoutLinesDeleteGraphQLField(GraphQLField):
    pass


class CheckoutLinesAddGraphQLField(GraphQLField):
    pass


class CheckoutLinesUpdateGraphQLField(GraphQLField):
    pass


class CheckoutRemovePromoCodeGraphQLField(GraphQLField):
    pass


class CheckoutPaymentCreateGraphQLField(GraphQLField):
    pass


class CheckoutShippingAddressUpdateGraphQLField(GraphQLField):
    pass


class CheckoutShippingMethodUpdateGraphQLField(GraphQLField):
    pass


class CheckoutDeliveryMethodUpdateGraphQLField(GraphQLField):
    pass


class CheckoutLanguageCodeUpdateGraphQLField(GraphQLField):
    pass


class OrderCreateFromCheckoutGraphQLField(GraphQLField):
    pass


class OrderCreateFromCheckoutErrorGraphQLField(GraphQLField):
    pass


class ChannelCreateGraphQLField(GraphQLField):
    pass


class ChannelErrorGraphQLField(GraphQLField):
    pass


class ChannelUpdateGraphQLField(GraphQLField):
    pass


class ChannelDeleteGraphQLField(GraphQLField):
    pass


class ChannelActivateGraphQLField(GraphQLField):
    pass


class ChannelDeactivateGraphQLField(GraphQLField):
    pass


class ChannelReorderWarehousesGraphQLField(GraphQLField):
    pass


class AttributeCreateGraphQLField(GraphQLField):
    pass


class AttributeErrorGraphQLField(GraphQLField):
    pass


class AttributeDeleteGraphQLField(GraphQLField):
    pass


class AttributeUpdateGraphQLField(GraphQLField):
    pass


class AttributeBulkCreateGraphQLField(GraphQLField):
    pass


class AttributeBulkCreateResultGraphQLField(GraphQLField):
    pass


class AttributeBulkCreateErrorGraphQLField(GraphQLField):
    pass


class AttributeBulkUpdateGraphQLField(GraphQLField):
    pass


class AttributeBulkUpdateResultGraphQLField(GraphQLField):
    pass


class AttributeBulkUpdateErrorGraphQLField(GraphQLField):
    pass


class AttributeTranslateGraphQLField(GraphQLField):
    pass


class AttributeBulkTranslateGraphQLField(GraphQLField):
    pass


class AttributeBulkTranslateResultGraphQLField(GraphQLField):
    pass


class AttributeBulkTranslateErrorGraphQLField(GraphQLField):
    pass


class AttributeBulkDeleteGraphQLField(GraphQLField):
    pass


class AttributeValueBulkDeleteGraphQLField(GraphQLField):
    pass


class AttributeValueCreateGraphQLField(GraphQLField):
    pass


class AttributeValueDeleteGraphQLField(GraphQLField):
    pass


class AttributeValueUpdateGraphQLField(GraphQLField):
    pass


class AttributeValueBulkTranslateGraphQLField(GraphQLField):
    pass


class AttributeValueBulkTranslateResultGraphQLField(GraphQLField):
    pass


class AttributeValueBulkTranslateErrorGraphQLField(GraphQLField):
    pass


class AttributeValueTranslateGraphQLField(GraphQLField):
    pass


class AttributeReorderValuesGraphQLField(GraphQLField):
    pass


class AppCreateGraphQLField(GraphQLField):
    pass


class AppErrorGraphQLField(GraphQLField):
    pass


class AppUpdateGraphQLField(GraphQLField):
    pass


class AppDeleteGraphQLField(GraphQLField):
    pass


class AppTokenCreateGraphQLField(GraphQLField):
    pass


class AppTokenDeleteGraphQLField(GraphQLField):
    pass


class AppTokenVerifyGraphQLField(GraphQLField):
    pass


class AppInstallGraphQLField(GraphQLField):
    pass


class AppRetryInstallGraphQLField(GraphQLField):
    pass


class AppDeleteFailedInstallationGraphQLField(GraphQLField):
    pass


class AppFetchManifestGraphQLField(GraphQLField):
    pass


class ManifestGraphQLField(GraphQLField):
    pass


class AppManifestExtensionGraphQLField(GraphQLField):
    pass


class AppManifestWebhookGraphQLField(GraphQLField):
    pass


class AppManifestRequiredSaleorVersionGraphQLField(GraphQLField):
    pass


class AppManifestBrandGraphQLField(GraphQLField):
    pass


class AppManifestBrandLogoGraphQLField(GraphQLField):
    pass


class AppActivateGraphQLField(GraphQLField):
    pass


class AppDeactivateGraphQLField(GraphQLField):
    pass


class CreateTokenGraphQLField(GraphQLField):
    pass


class AccountErrorGraphQLField(GraphQLField):
    pass


class RefreshTokenGraphQLField(GraphQLField):
    pass


class VerifyTokenGraphQLField(GraphQLField):
    pass


class DeactivateAllUserTokensGraphQLField(GraphQLField):
    pass


class ExternalAuthenticationUrlGraphQLField(GraphQLField):
    pass


class ExternalObtainAccessTokensGraphQLField(GraphQLField):
    pass


class ExternalRefreshGraphQLField(GraphQLField):
    pass


class ExternalLogoutGraphQLField(GraphQLField):
    pass


class ExternalVerifyGraphQLField(GraphQLField):
    pass


class RequestPasswordResetGraphQLField(GraphQLField):
    pass


class SendConfirmationEmailGraphQLField(GraphQLField):
    pass


class SendConfirmationEmailErrorGraphQLField(GraphQLField):
    pass


class ConfirmAccountGraphQLField(GraphQLField):
    pass


class SetPasswordGraphQLField(GraphQLField):
    pass


class PasswordChangeGraphQLField(GraphQLField):
    pass


class RequestEmailChangeGraphQLField(GraphQLField):
    pass


class ConfirmEmailChangeGraphQLField(GraphQLField):
    pass


class AccountAddressCreateGraphQLField(GraphQLField):
    pass


class AccountAddressUpdateGraphQLField(GraphQLField):
    pass


class AccountAddressDeleteGraphQLField(GraphQLField):
    pass


class AccountSetDefaultAddressGraphQLField(GraphQLField):
    pass


class AccountRegisterGraphQLField(GraphQLField):
    pass


class AccountUpdateGraphQLField(GraphQLField):
    pass


class AccountRequestDeletionGraphQLField(GraphQLField):
    pass


class AccountDeleteGraphQLField(GraphQLField):
    pass


class AddressCreateGraphQLField(GraphQLField):
    pass


class AddressUpdateGraphQLField(GraphQLField):
    pass


class AddressDeleteGraphQLField(GraphQLField):
    pass


class AddressSetDefaultGraphQLField(GraphQLField):
    pass


class CustomerCreateGraphQLField(GraphQLField):
    pass


class CustomerUpdateGraphQLField(GraphQLField):
    pass


class CustomerDeleteGraphQLField(GraphQLField):
    pass


class CustomerBulkDeleteGraphQLField(GraphQLField):
    pass


class CustomerBulkUpdateGraphQLField(GraphQLField):
    pass


class CustomerBulkResultGraphQLField(GraphQLField):
    pass


class CustomerBulkUpdateErrorGraphQLField(GraphQLField):
    pass


class StaffCreateGraphQLField(GraphQLField):
    pass


class StaffErrorGraphQLField(GraphQLField):
    pass


class StaffUpdateGraphQLField(GraphQLField):
    pass


class StaffDeleteGraphQLField(GraphQLField):
    pass


class StaffBulkDeleteGraphQLField(GraphQLField):
    pass


class UserAvatarUpdateGraphQLField(GraphQLField):
    pass


class UserAvatarDeleteGraphQLField(GraphQLField):
    pass


class UserBulkSetActiveGraphQLField(GraphQLField):
    pass


class PermissionGroupCreateGraphQLField(GraphQLField):
    pass


class PermissionGroupErrorGraphQLField(GraphQLField):
    pass


class PermissionGroupUpdateGraphQLField(GraphQLField):
    pass


class PermissionGroupDeleteGraphQLField(GraphQLField):
    pass


class EventInterface(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "EventInterface":
        self._inline_fragments[type_name] = subfields
        return self


class IssuingPrincipalUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "IssuingPrincipalUnion":
        self._inline_fragments[type_name] = subfields
        return self


class AccountConfirmationRequestedGraphQLField(GraphQLField):
    pass


class AccountChangeEmailRequestedGraphQLField(GraphQLField):
    pass


class AccountEmailChangedGraphQLField(GraphQLField):
    pass


class AccountSetPasswordRequestedGraphQLField(GraphQLField):
    pass


class AccountConfirmedGraphQLField(GraphQLField):
    pass


class AccountDeleteRequestedGraphQLField(GraphQLField):
    pass


class AccountDeletedGraphQLField(GraphQLField):
    pass


class AddressCreatedGraphQLField(GraphQLField):
    pass


class AddressUpdatedGraphQLField(GraphQLField):
    pass


class AddressDeletedGraphQLField(GraphQLField):
    pass


class AppInstalledGraphQLField(GraphQLField):
    pass


class AppUpdatedGraphQLField(GraphQLField):
    pass


class AppDeletedGraphQLField(GraphQLField):
    pass


class AppStatusChangedGraphQLField(GraphQLField):
    pass


class AttributeCreatedGraphQLField(GraphQLField):
    pass


class AttributeUpdatedGraphQLField(GraphQLField):
    pass


class AttributeDeletedGraphQLField(GraphQLField):
    pass


class AttributeValueCreatedGraphQLField(GraphQLField):
    pass


class AttributeValueUpdatedGraphQLField(GraphQLField):
    pass


class AttributeValueDeletedGraphQLField(GraphQLField):
    pass


class CategoryCreatedGraphQLField(GraphQLField):
    pass


class CategoryUpdatedGraphQLField(GraphQLField):
    pass


class CategoryDeletedGraphQLField(GraphQLField):
    pass


class ChannelCreatedGraphQLField(GraphQLField):
    pass


class ChannelUpdatedGraphQLField(GraphQLField):
    pass


class ChannelDeletedGraphQLField(GraphQLField):
    pass


class ChannelStatusChangedGraphQLField(GraphQLField):
    pass


class ChannelMetadataUpdatedGraphQLField(GraphQLField):
    pass


class GiftCardCreatedGraphQLField(GraphQLField):
    pass


class GiftCardUpdatedGraphQLField(GraphQLField):
    pass


class GiftCardDeletedGraphQLField(GraphQLField):
    pass


class GiftCardSentGraphQLField(GraphQLField):
    pass


class GiftCardStatusChangedGraphQLField(GraphQLField):
    pass


class GiftCardMetadataUpdatedGraphQLField(GraphQLField):
    pass


class GiftCardExportCompletedGraphQLField(GraphQLField):
    pass


class MenuCreatedGraphQLField(GraphQLField):
    pass


class MenuUpdatedGraphQLField(GraphQLField):
    pass


class MenuDeletedGraphQLField(GraphQLField):
    pass


class MenuItemCreatedGraphQLField(GraphQLField):
    pass


class MenuItemUpdatedGraphQLField(GraphQLField):
    pass


class MenuItemDeletedGraphQLField(GraphQLField):
    pass


class OrderCreatedGraphQLField(GraphQLField):
    pass


class OrderUpdatedGraphQLField(GraphQLField):
    pass


class OrderConfirmedGraphQLField(GraphQLField):
    pass


class OrderFullyPaidGraphQLField(GraphQLField):
    pass


class OrderPaidGraphQLField(GraphQLField):
    pass


class OrderRefundedGraphQLField(GraphQLField):
    pass


class OrderFullyRefundedGraphQLField(GraphQLField):
    pass


class OrderFulfilledGraphQLField(GraphQLField):
    pass


class OrderCancelledGraphQLField(GraphQLField):
    pass


class OrderExpiredGraphQLField(GraphQLField):
    pass


class OrderMetadataUpdatedGraphQLField(GraphQLField):
    pass


class OrderBulkCreatedGraphQLField(GraphQLField):
    pass


class DraftOrderCreatedGraphQLField(GraphQLField):
    pass


class DraftOrderUpdatedGraphQLField(GraphQLField):
    pass


class DraftOrderDeletedGraphQLField(GraphQLField):
    pass


class ProductCreatedGraphQLField(GraphQLField):
    pass


class ProductUpdatedGraphQLField(GraphQLField):
    pass


class ProductDeletedGraphQLField(GraphQLField):
    pass


class ProductMetadataUpdatedGraphQLField(GraphQLField):
    pass


class ProductExportCompletedGraphQLField(GraphQLField):
    pass


class ProductMediaCreatedGraphQLField(GraphQLField):
    pass


class ProductMediaUpdatedGraphQLField(GraphQLField):
    pass


class ProductMediaDeletedGraphQLField(GraphQLField):
    pass


class ProductVariantCreatedGraphQLField(GraphQLField):
    pass


class ProductVariantUpdatedGraphQLField(GraphQLField):
    pass


class ProductVariantOutOfStockGraphQLField(GraphQLField):
    pass


class ProductVariantBackInStockGraphQLField(GraphQLField):
    pass


class ProductVariantStockUpdatedGraphQLField(GraphQLField):
    pass


class ProductVariantDeletedGraphQLField(GraphQLField):
    pass


class ProductVariantMetadataUpdatedGraphQLField(GraphQLField):
    pass


class SaleCreatedGraphQLField(GraphQLField):
    pass


class SaleUpdatedGraphQLField(GraphQLField):
    pass


class SaleDeletedGraphQLField(GraphQLField):
    pass


class SaleToggleGraphQLField(GraphQLField):
    pass


class PromotionCreatedGraphQLField(GraphQLField):
    pass


class PromotionUpdatedGraphQLField(GraphQLField):
    pass


class PromotionDeletedGraphQLField(GraphQLField):
    pass


class PromotionStartedGraphQLField(GraphQLField):
    pass


class PromotionEndedGraphQLField(GraphQLField):
    pass


class PromotionRuleCreatedGraphQLField(GraphQLField):
    pass


class PromotionRuleUpdatedGraphQLField(GraphQLField):
    pass


class PromotionRuleDeletedGraphQLField(GraphQLField):
    pass


class InvoiceRequestedGraphQLField(GraphQLField):
    pass


class InvoiceDeletedGraphQLField(GraphQLField):
    pass


class InvoiceSentGraphQLField(GraphQLField):
    pass


class FulfillmentCreatedGraphQLField(GraphQLField):
    pass


class FulfillmentTrackingNumberUpdatedGraphQLField(GraphQLField):
    pass


class FulfillmentCanceledGraphQLField(GraphQLField):
    pass


class FulfillmentApprovedGraphQLField(GraphQLField):
    pass


class FulfillmentMetadataUpdatedGraphQLField(GraphQLField):
    pass


class CustomerCreatedGraphQLField(GraphQLField):
    pass


class CustomerUpdatedGraphQLField(GraphQLField):
    pass


class CustomerMetadataUpdatedGraphQLField(GraphQLField):
    pass


class CollectionCreatedGraphQLField(GraphQLField):
    pass


class CollectionUpdatedGraphQLField(GraphQLField):
    pass


class CollectionDeletedGraphQLField(GraphQLField):
    pass


class CollectionMetadataUpdatedGraphQLField(GraphQLField):
    pass


class CheckoutCreatedGraphQLField(GraphQLField):
    pass


class CheckoutUpdatedGraphQLField(GraphQLField):
    pass


class CheckoutFullyPaidGraphQLField(GraphQLField):
    pass


class CheckoutMetadataUpdatedGraphQLField(GraphQLField):
    pass


class PageCreatedGraphQLField(GraphQLField):
    pass


class PageUpdatedGraphQLField(GraphQLField):
    pass


class PageDeletedGraphQLField(GraphQLField):
    pass


class PageTypeCreatedGraphQLField(GraphQLField):
    pass


class PageTypeUpdatedGraphQLField(GraphQLField):
    pass


class PageTypeDeletedGraphQLField(GraphQLField):
    pass


class PermissionGroupCreatedGraphQLField(GraphQLField):
    pass


class PermissionGroupUpdatedGraphQLField(GraphQLField):
    pass


class PermissionGroupDeletedGraphQLField(GraphQLField):
    pass


class ShippingPriceCreatedGraphQLField(GraphQLField):
    pass


class ShippingPriceUpdatedGraphQLField(GraphQLField):
    pass


class ShippingPriceDeletedGraphQLField(GraphQLField):
    pass


class ShippingZoneCreatedGraphQLField(GraphQLField):
    pass


class ShippingZoneUpdatedGraphQLField(GraphQLField):
    pass


class ShippingZoneDeletedGraphQLField(GraphQLField):
    pass


class ShippingZoneMetadataUpdatedGraphQLField(GraphQLField):
    pass


class StaffCreatedGraphQLField(GraphQLField):
    pass


class StaffUpdatedGraphQLField(GraphQLField):
    pass


class StaffDeletedGraphQLField(GraphQLField):
    pass


class StaffSetPasswordRequestedGraphQLField(GraphQLField):
    pass


class TransactionItemMetadataUpdatedGraphQLField(GraphQLField):
    pass


class TranslationCreatedGraphQLField(GraphQLField):
    pass


class TranslationTypesUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "TranslationTypesUnion":
        self._inline_fragments[type_name] = subfields
        return self


class TranslationUpdatedGraphQLField(GraphQLField):
    pass


class VoucherCreatedGraphQLField(GraphQLField):
    pass


class VoucherUpdatedGraphQLField(GraphQLField):
    pass


class VoucherDeletedGraphQLField(GraphQLField):
    pass


class VoucherCodesCreatedGraphQLField(GraphQLField):
    pass


class VoucherCodesDeletedGraphQLField(GraphQLField):
    pass


class VoucherMetadataUpdatedGraphQLField(GraphQLField):
    pass


class VoucherCodeExportCompletedGraphQLField(GraphQLField):
    pass


class WarehouseCreatedGraphQLField(GraphQLField):
    pass


class WarehouseUpdatedGraphQLField(GraphQLField):
    pass


class WarehouseDeletedGraphQLField(GraphQLField):
    pass


class WarehouseMetadataUpdatedGraphQLField(GraphQLField):
    pass


class ThumbnailCreatedGraphQLField(GraphQLField):
    pass


class PaymentAuthorizeGraphQLField(GraphQLField):
    pass


class PaymentCaptureEventGraphQLField(GraphQLField):
    pass


class PaymentRefundEventGraphQLField(GraphQLField):
    pass


class PaymentVoidEventGraphQLField(GraphQLField):
    pass


class PaymentConfirmEventGraphQLField(GraphQLField):
    pass


class PaymentProcessEventGraphQLField(GraphQLField):
    pass


class PaymentListGatewaysGraphQLField(GraphQLField):
    pass


class TransactionCancelationRequestedGraphQLField(GraphQLField):
    pass


class TransactionActionGraphQLField(GraphQLField):
    pass


class TransactionChargeRequestedGraphQLField(GraphQLField):
    pass


class TransactionRefundRequestedGraphQLField(GraphQLField):
    pass


class OrderFilterShippingMethodsGraphQLField(GraphQLField):
    pass


class CheckoutFilterShippingMethodsGraphQLField(GraphQLField):
    pass


class ShippingListMethodsForCheckoutGraphQLField(GraphQLField):
    pass


class CalculateTaxesGraphQLField(GraphQLField):
    pass


class TaxableObjectGraphQLField(GraphQLField):
    pass


class TaxableObjectDiscountGraphQLField(GraphQLField):
    pass


class TaxableObjectLineGraphQLField(GraphQLField):
    pass


class TaxSourceLineUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "TaxSourceLineUnion":
        self._inline_fragments[type_name] = subfields
        return self


class PaymentGatewayInitializeSessionGraphQLField(GraphQLField):
    pass


class OrderOrCheckoutUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "OrderOrCheckoutUnion":
        self._inline_fragments[type_name] = subfields
        return self


class TransactionInitializeSessionGraphQLField(GraphQLField):
    pass


class TransactionProcessActionGraphQLField(GraphQLField):
    pass


class TransactionProcessSessionGraphQLField(GraphQLField):
    pass


class ShopMetadataUpdatedGraphQLField(GraphQLField):
    pass


class ListStoredPaymentMethodsGraphQLField(GraphQLField):
    pass


class StoredPaymentMethodDeleteRequestedGraphQLField(GraphQLField):
    pass


class PaymentGatewayInitializeTokenizationSessionGraphQLField(GraphQLField):
    pass


class PaymentMethodInitializeTokenizationSessionGraphQLField(GraphQLField):
    pass


class PaymentMethodProcessTokenizationSessionGraphQLField(GraphQLField):
    pass


class _EntityUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "_EntityUnion":
        self._inline_fragments[type_name] = subfields
        return self


class _ServiceGraphQLField(GraphQLField):
    pass

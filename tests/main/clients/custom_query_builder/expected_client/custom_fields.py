from typing import Optional, Union

from . import (
    AccountAddressCreateGraphQLField,
    AccountAddressDeleteGraphQLField,
    AccountAddressUpdateGraphQLField,
    AccountDeleteGraphQLField,
    AccountErrorGraphQLField,
    AccountRegisterGraphQLField,
    AccountRequestDeletionGraphQLField,
    AccountSetDefaultAddressGraphQLField,
    AccountUpdateGraphQLField,
    AddressCreateGraphQLField,
    AddressDeleteGraphQLField,
    AddressGraphQLField,
    AddressSetDefaultGraphQLField,
    AddressUpdateGraphQLField,
    AddressValidationDataGraphQLField,
    AllocationGraphQLField,
    AppActivateGraphQLField,
    AppBrandGraphQLField,
    AppBrandLogoGraphQLField,
    AppCountableConnectionGraphQLField,
    AppCountableEdgeGraphQLField,
    AppCreateGraphQLField,
    AppDeactivateGraphQLField,
    AppDeleteFailedInstallationGraphQLField,
    AppDeleteGraphQLField,
    AppErrorGraphQLField,
    AppExtensionCountableConnectionGraphQLField,
    AppExtensionCountableEdgeGraphQLField,
    AppExtensionGraphQLField,
    AppFetchManifestGraphQLField,
    AppGraphQLField,
    AppInstallationGraphQLField,
    AppInstallGraphQLField,
    AppManifestBrandGraphQLField,
    AppManifestBrandLogoGraphQLField,
    AppManifestExtensionGraphQLField,
    AppManifestRequiredSaleorVersionGraphQLField,
    AppManifestWebhookGraphQLField,
    AppRetryInstallGraphQLField,
    AppTokenCreateGraphQLField,
    AppTokenDeleteGraphQLField,
    AppTokenGraphQLField,
    AppTokenVerifyGraphQLField,
    AppUpdateGraphQLField,
    AssignedVariantAttributeGraphQLField,
    AssignNavigationGraphQLField,
    AttributeBulkCreateErrorGraphQLField,
    AttributeBulkCreateGraphQLField,
    AttributeBulkCreateResultGraphQLField,
    AttributeBulkDeleteGraphQLField,
    AttributeBulkTranslateErrorGraphQLField,
    AttributeBulkTranslateGraphQLField,
    AttributeBulkTranslateResultGraphQLField,
    AttributeBulkUpdateErrorGraphQLField,
    AttributeBulkUpdateGraphQLField,
    AttributeBulkUpdateResultGraphQLField,
    AttributeCountableConnectionGraphQLField,
    AttributeCountableEdgeGraphQLField,
    AttributeCreateGraphQLField,
    AttributeDeleteGraphQLField,
    AttributeErrorGraphQLField,
    AttributeGraphQLField,
    AttributeReorderValuesGraphQLField,
    AttributeTranslatableContentGraphQLField,
    AttributeTranslateGraphQLField,
    AttributeTranslationGraphQLField,
    AttributeUpdateGraphQLField,
    AttributeValueBulkDeleteGraphQLField,
    AttributeValueBulkTranslateErrorGraphQLField,
    AttributeValueBulkTranslateGraphQLField,
    AttributeValueBulkTranslateResultGraphQLField,
    AttributeValueCountableConnectionGraphQLField,
    AttributeValueCountableEdgeGraphQLField,
    AttributeValueCreateGraphQLField,
    AttributeValueDeleteGraphQLField,
    AttributeValueGraphQLField,
    AttributeValueTranslatableContentGraphQLField,
    AttributeValueTranslateGraphQLField,
    AttributeValueTranslationGraphQLField,
    AttributeValueUpdateGraphQLField,
    BulkProductErrorGraphQLField,
    BulkStockErrorGraphQLField,
    CategoryBulkDeleteGraphQLField,
    CategoryCountableConnectionGraphQLField,
    CategoryCountableEdgeGraphQLField,
    CategoryCreateGraphQLField,
    CategoryDeleteGraphQLField,
    CategoryGraphQLField,
    CategoryTranslatableContentGraphQLField,
    CategoryTranslateGraphQLField,
    CategoryTranslationGraphQLField,
    CategoryUpdateGraphQLField,
    ChannelActivateGraphQLField,
    ChannelCreateGraphQLField,
    ChannelDeactivateGraphQLField,
    ChannelDeleteGraphQLField,
    ChannelErrorGraphQLField,
    ChannelGraphQLField,
    ChannelReorderWarehousesGraphQLField,
    ChannelUpdateGraphQLField,
    CheckoutAddPromoCodeGraphQLField,
    CheckoutBillingAddressUpdateGraphQLField,
    CheckoutCompleteGraphQLField,
    CheckoutCountableConnectionGraphQLField,
    CheckoutCountableEdgeGraphQLField,
    CheckoutCreateFromOrderErrorGraphQLField,
    CheckoutCreateFromOrderGraphQLField,
    CheckoutCreateFromOrderUnavailableVariantGraphQLField,
    CheckoutCreateGraphQLField,
    CheckoutCustomerAttachGraphQLField,
    CheckoutCustomerDetachGraphQLField,
    CheckoutDeliveryMethodUpdateGraphQLField,
    CheckoutEmailUpdateGraphQLField,
    CheckoutErrorGraphQLField,
    CheckoutGraphQLField,
    CheckoutLanguageCodeUpdateGraphQLField,
    CheckoutLineCountableConnectionGraphQLField,
    CheckoutLineCountableEdgeGraphQLField,
    CheckoutLineDeleteGraphQLField,
    CheckoutLineGraphQLField,
    CheckoutLineProblemInsufficientStockGraphQLField,
    CheckoutLineProblemUnion,
    CheckoutLineProblemVariantNotAvailableGraphQLField,
    CheckoutLinesAddGraphQLField,
    CheckoutLinesDeleteGraphQLField,
    CheckoutLinesUpdateGraphQLField,
    CheckoutPaymentCreateGraphQLField,
    CheckoutProblemUnion,
    CheckoutRemovePromoCodeGraphQLField,
    CheckoutSettingsGraphQLField,
    CheckoutShippingAddressUpdateGraphQLField,
    CheckoutShippingMethodUpdateGraphQLField,
    ChoiceValueGraphQLField,
    CollectionAddProductsGraphQLField,
    CollectionBulkDeleteGraphQLField,
    CollectionChannelListingErrorGraphQLField,
    CollectionChannelListingGraphQLField,
    CollectionChannelListingUpdateGraphQLField,
    CollectionCountableConnectionGraphQLField,
    CollectionCountableEdgeGraphQLField,
    CollectionCreateGraphQLField,
    CollectionDeleteGraphQLField,
    CollectionErrorGraphQLField,
    CollectionGraphQLField,
    CollectionRemoveProductsGraphQLField,
    CollectionReorderProductsGraphQLField,
    CollectionTranslatableContentGraphQLField,
    CollectionTranslateGraphQLField,
    CollectionTranslationGraphQLField,
    CollectionUpdateGraphQLField,
    ConfigurationItemGraphQLField,
    ConfirmAccountGraphQLField,
    ConfirmEmailChangeGraphQLField,
    CountryDisplayGraphQLField,
    CreateTokenGraphQLField,
    CreditCardGraphQLField,
    CustomerBulkDeleteGraphQLField,
    CustomerBulkResultGraphQLField,
    CustomerBulkUpdateErrorGraphQLField,
    CustomerBulkUpdateGraphQLField,
    CustomerCreateGraphQLField,
    CustomerDeleteGraphQLField,
    CustomerEventGraphQLField,
    CustomerUpdateGraphQLField,
    DeactivateAllUserTokensGraphQLField,
    DeleteMetadataGraphQLField,
    DeletePrivateMetadataGraphQLField,
    DeliveryMethodUnion,
    DigitalContentCountableConnectionGraphQLField,
    DigitalContentCountableEdgeGraphQLField,
    DigitalContentCreateGraphQLField,
    DigitalContentDeleteGraphQLField,
    DigitalContentGraphQLField,
    DigitalContentUpdateGraphQLField,
    DigitalContentUrlCreateGraphQLField,
    DigitalContentUrlGraphQLField,
    DiscountErrorGraphQLField,
    DomainGraphQLField,
    DraftOrderBulkDeleteGraphQLField,
    DraftOrderCompleteGraphQLField,
    DraftOrderCreateGraphQLField,
    DraftOrderDeleteGraphQLField,
    DraftOrderLinesBulkDeleteGraphQLField,
    DraftOrderUpdateGraphQLField,
    EventDeliveryAttemptCountableConnectionGraphQLField,
    EventDeliveryAttemptCountableEdgeGraphQLField,
    EventDeliveryAttemptGraphQLField,
    EventDeliveryCountableConnectionGraphQLField,
    EventDeliveryCountableEdgeGraphQLField,
    EventDeliveryGraphQLField,
    EventDeliveryRetryGraphQLField,
    ExportErrorGraphQLField,
    ExportEventGraphQLField,
    ExportFileCountableConnectionGraphQLField,
    ExportFileCountableEdgeGraphQLField,
    ExportFileGraphQLField,
    ExportGiftCardsGraphQLField,
    ExportProductsGraphQLField,
    ExportVoucherCodesGraphQLField,
    ExternalAuthenticationGraphQLField,
    ExternalAuthenticationUrlGraphQLField,
    ExternalLogoutGraphQLField,
    ExternalNotificationErrorGraphQLField,
    ExternalNotificationTriggerGraphQLField,
    ExternalObtainAccessTokensGraphQLField,
    ExternalRefreshGraphQLField,
    ExternalVerifyGraphQLField,
    FileGraphQLField,
    FileUploadGraphQLField,
    FulfillmentApproveGraphQLField,
    FulfillmentCancelGraphQLField,
    FulfillmentGraphQLField,
    FulfillmentLineGraphQLField,
    FulfillmentRefundProductsGraphQLField,
    FulfillmentReturnProductsGraphQLField,
    FulfillmentUpdateTrackingGraphQLField,
    GatewayConfigLineGraphQLField,
    GiftCardActivateGraphQLField,
    GiftCardAddNoteGraphQLField,
    GiftCardBulkActivateGraphQLField,
    GiftCardBulkCreateGraphQLField,
    GiftCardBulkDeactivateGraphQLField,
    GiftCardBulkDeleteGraphQLField,
    GiftCardCountableConnectionGraphQLField,
    GiftCardCountableEdgeGraphQLField,
    GiftCardCreateGraphQLField,
    GiftCardDeactivateGraphQLField,
    GiftCardDeleteGraphQLField,
    GiftCardErrorGraphQLField,
    GiftCardEventBalanceGraphQLField,
    GiftCardEventGraphQLField,
    GiftCardGraphQLField,
    GiftCardResendGraphQLField,
    GiftCardSettingsErrorGraphQLField,
    GiftCardSettingsGraphQLField,
    GiftCardSettingsUpdateGraphQLField,
    GiftCardTagCountableConnectionGraphQLField,
    GiftCardTagCountableEdgeGraphQLField,
    GiftCardTagGraphQLField,
    GiftCardUpdateGraphQLField,
    GroupCountableConnectionGraphQLField,
    GroupCountableEdgeGraphQLField,
    GroupGraphQLField,
    ImageGraphQLField,
    InvoiceCreateGraphQLField,
    InvoiceDeleteGraphQLField,
    InvoiceErrorGraphQLField,
    InvoiceGraphQLField,
    InvoiceRequestDeleteGraphQLField,
    InvoiceRequestGraphQLField,
    InvoiceSendNotificationGraphQLField,
    InvoiceUpdateGraphQLField,
    LanguageDisplayGraphQLField,
    LimitInfoGraphQLField,
    LimitsGraphQLField,
    ManifestGraphQLField,
    MarginGraphQLField,
    MenuBulkDeleteGraphQLField,
    MenuCountableConnectionGraphQLField,
    MenuCountableEdgeGraphQLField,
    MenuCreateGraphQLField,
    MenuDeleteGraphQLField,
    MenuErrorGraphQLField,
    MenuGraphQLField,
    MenuItemBulkDeleteGraphQLField,
    MenuItemCountableConnectionGraphQLField,
    MenuItemCountableEdgeGraphQLField,
    MenuItemCreateGraphQLField,
    MenuItemDeleteGraphQLField,
    MenuItemGraphQLField,
    MenuItemMoveGraphQLField,
    MenuItemTranslatableContentGraphQLField,
    MenuItemTranslateGraphQLField,
    MenuItemTranslationGraphQLField,
    MenuItemUpdateGraphQLField,
    MenuUpdateGraphQLField,
    MetadataErrorGraphQLField,
    MetadataItemGraphQLField,
    MoneyGraphQLField,
    MoneyRangeGraphQLField,
    ObjectWithMetadataInterface,
    OrderAddNoteGraphQLField,
    OrderBulkCancelGraphQLField,
    OrderBulkCreateErrorGraphQLField,
    OrderBulkCreateGraphQLField,
    OrderBulkCreateResultGraphQLField,
    OrderCancelGraphQLField,
    OrderCaptureGraphQLField,
    OrderConfirmGraphQLField,
    OrderCountableConnectionGraphQLField,
    OrderCountableEdgeGraphQLField,
    OrderCreateFromCheckoutErrorGraphQLField,
    OrderCreateFromCheckoutGraphQLField,
    OrderDiscountAddGraphQLField,
    OrderDiscountDeleteGraphQLField,
    OrderDiscountGraphQLField,
    OrderDiscountUpdateGraphQLField,
    OrderErrorGraphQLField,
    OrderEventCountableConnectionGraphQLField,
    OrderEventCountableEdgeGraphQLField,
    OrderEventDiscountObjectGraphQLField,
    OrderEventGraphQLField,
    OrderEventOrderLineObjectGraphQLField,
    OrderFulfillGraphQLField,
    OrderGrantedRefundGraphQLField,
    OrderGrantedRefundLineGraphQLField,
    OrderGrantRefundCreateErrorGraphQLField,
    OrderGrantRefundCreateGraphQLField,
    OrderGrantRefundCreateLineErrorGraphQLField,
    OrderGrantRefundUpdateErrorGraphQLField,
    OrderGrantRefundUpdateGraphQLField,
    OrderGrantRefundUpdateLineErrorGraphQLField,
    OrderGraphQLField,
    OrderLineDeleteGraphQLField,
    OrderLineDiscountRemoveGraphQLField,
    OrderLineDiscountUpdateGraphQLField,
    OrderLineGraphQLField,
    OrderLinesCreateGraphQLField,
    OrderLineUpdateGraphQLField,
    OrderMarkAsPaidGraphQLField,
    OrderNoteAddErrorGraphQLField,
    OrderNoteAddGraphQLField,
    OrderNoteUpdateErrorGraphQLField,
    OrderNoteUpdateGraphQLField,
    OrderRefundGraphQLField,
    OrderSettingsErrorGraphQLField,
    OrderSettingsGraphQLField,
    OrderSettingsUpdateGraphQLField,
    OrderUpdateGraphQLField,
    OrderUpdateShippingGraphQLField,
    OrderVoidGraphQLField,
    PageAttributeAssignGraphQLField,
    PageAttributeUnassignGraphQLField,
    PageBulkDeleteGraphQLField,
    PageBulkPublishGraphQLField,
    PageCountableConnectionGraphQLField,
    PageCountableEdgeGraphQLField,
    PageCreateGraphQLField,
    PageDeleteGraphQLField,
    PageErrorGraphQLField,
    PageGraphQLField,
    PageInfoGraphQLField,
    PageReorderAttributeValuesGraphQLField,
    PageTranslatableContentGraphQLField,
    PageTranslateGraphQLField,
    PageTranslationGraphQLField,
    PageTypeBulkDeleteGraphQLField,
    PageTypeCountableConnectionGraphQLField,
    PageTypeCountableEdgeGraphQLField,
    PageTypeCreateGraphQLField,
    PageTypeDeleteGraphQLField,
    PageTypeGraphQLField,
    PageTypeReorderAttributesGraphQLField,
    PageTypeUpdateGraphQLField,
    PageUpdateGraphQLField,
    PasswordChangeGraphQLField,
    PaymentCaptureGraphQLField,
    PaymentCheckBalanceGraphQLField,
    PaymentCountableConnectionGraphQLField,
    PaymentCountableEdgeGraphQLField,
    PaymentErrorGraphQLField,
    PaymentGatewayConfigErrorGraphQLField,
    PaymentGatewayConfigGraphQLField,
    PaymentGatewayGraphQLField,
    PaymentGatewayInitializeErrorGraphQLField,
    PaymentGatewayInitializeGraphQLField,
    PaymentGatewayInitializeTokenizationErrorGraphQLField,
    PaymentGatewayInitializeTokenizationGraphQLField,
    PaymentGraphQLField,
    PaymentInitializedGraphQLField,
    PaymentInitializeGraphQLField,
    PaymentMethodInitializeTokenizationErrorGraphQLField,
    PaymentMethodInitializeTokenizationGraphQLField,
    PaymentMethodProcessTokenizationErrorGraphQLField,
    PaymentMethodProcessTokenizationGraphQLField,
    PaymentMethodRequestDeleteErrorGraphQLField,
    PaymentRefundGraphQLField,
    PaymentSettingsGraphQLField,
    PaymentSourceGraphQLField,
    PaymentVoidGraphQLField,
    PermissionGraphQLField,
    PermissionGroupCreateGraphQLField,
    PermissionGroupDeleteGraphQLField,
    PermissionGroupErrorGraphQLField,
    PermissionGroupUpdateGraphQLField,
    PluginConfigurationGraphQLField,
    PluginCountableConnectionGraphQLField,
    PluginCountableEdgeGraphQLField,
    PluginErrorGraphQLField,
    PluginGraphQLField,
    PluginUpdateGraphQLField,
    PreorderDataGraphQLField,
    PreorderThresholdGraphQLField,
    ProductAttributeAssignGraphQLField,
    ProductAttributeAssignmentUpdateGraphQLField,
    ProductAttributeUnassignGraphQLField,
    ProductBulkCreateErrorGraphQLField,
    ProductBulkCreateGraphQLField,
    ProductBulkDeleteGraphQLField,
    ProductBulkResultGraphQLField,
    ProductBulkTranslateErrorGraphQLField,
    ProductBulkTranslateGraphQLField,
    ProductBulkTranslateResultGraphQLField,
    ProductChannelListingErrorGraphQLField,
    ProductChannelListingGraphQLField,
    ProductChannelListingUpdateGraphQLField,
    ProductCountableConnectionGraphQLField,
    ProductCountableEdgeGraphQLField,
    ProductCreateGraphQLField,
    ProductDeleteGraphQLField,
    ProductErrorGraphQLField,
    ProductGraphQLField,
    ProductImageGraphQLField,
    ProductMediaBulkDeleteGraphQLField,
    ProductMediaCreateGraphQLField,
    ProductMediaDeleteGraphQLField,
    ProductMediaGraphQLField,
    ProductMediaReorderGraphQLField,
    ProductMediaUpdateGraphQLField,
    ProductPricingInfoGraphQLField,
    ProductReorderAttributeValuesGraphQLField,
    ProductTranslatableContentGraphQLField,
    ProductTranslateGraphQLField,
    ProductTranslationGraphQLField,
    ProductTypeBulkDeleteGraphQLField,
    ProductTypeCountableConnectionGraphQLField,
    ProductTypeCountableEdgeGraphQLField,
    ProductTypeCreateGraphQLField,
    ProductTypeDeleteGraphQLField,
    ProductTypeGraphQLField,
    ProductTypeReorderAttributesGraphQLField,
    ProductTypeUpdateGraphQLField,
    ProductUpdateGraphQLField,
    ProductVariantBulkCreateGraphQLField,
    ProductVariantBulkDeleteGraphQLField,
    ProductVariantBulkErrorGraphQLField,
    ProductVariantBulkResultGraphQLField,
    ProductVariantBulkTranslateErrorGraphQLField,
    ProductVariantBulkTranslateGraphQLField,
    ProductVariantBulkTranslateResultGraphQLField,
    ProductVariantBulkUpdateGraphQLField,
    ProductVariantChannelListingGraphQLField,
    ProductVariantChannelListingUpdateGraphQLField,
    ProductVariantCountableConnectionGraphQLField,
    ProductVariantCountableEdgeGraphQLField,
    ProductVariantCreateGraphQLField,
    ProductVariantDeleteGraphQLField,
    ProductVariantGraphQLField,
    ProductVariantPreorderDeactivateGraphQLField,
    ProductVariantReorderAttributeValuesGraphQLField,
    ProductVariantReorderGraphQLField,
    ProductVariantSetDefaultGraphQLField,
    ProductVariantStocksCreateGraphQLField,
    ProductVariantStocksDeleteGraphQLField,
    ProductVariantStocksUpdateGraphQLField,
    ProductVariantTranslatableContentGraphQLField,
    ProductVariantTranslateGraphQLField,
    ProductVariantTranslationGraphQLField,
    ProductVariantUpdateGraphQLField,
    PromotionBulkDeleteGraphQLField,
    PromotionCountableConnectionGraphQLField,
    PromotionCountableEdgeGraphQLField,
    PromotionCreatedEventGraphQLField,
    PromotionCreateErrorGraphQLField,
    PromotionCreateGraphQLField,
    PromotionDeleteErrorGraphQLField,
    PromotionDeleteGraphQLField,
    PromotionEndedEventGraphQLField,
    PromotionEventUnion,
    PromotionGraphQLField,
    PromotionRuleCreatedEventGraphQLField,
    PromotionRuleCreateErrorGraphQLField,
    PromotionRuleCreateGraphQLField,
    PromotionRuleDeletedEventGraphQLField,
    PromotionRuleDeleteErrorGraphQLField,
    PromotionRuleDeleteGraphQLField,
    PromotionRuleGraphQLField,
    PromotionRuleTranslatableContentGraphQLField,
    PromotionRuleTranslateGraphQLField,
    PromotionRuleTranslationGraphQLField,
    PromotionRuleUpdatedEventGraphQLField,
    PromotionRuleUpdateErrorGraphQLField,
    PromotionRuleUpdateGraphQLField,
    PromotionStartedEventGraphQLField,
    PromotionTranslatableContentGraphQLField,
    PromotionTranslateGraphQLField,
    PromotionTranslationGraphQLField,
    PromotionUpdatedEventGraphQLField,
    PromotionUpdateErrorGraphQLField,
    PromotionUpdateGraphQLField,
    ReducedRateGraphQLField,
    RefreshTokenGraphQLField,
    RequestEmailChangeGraphQLField,
    RequestPasswordResetGraphQLField,
    SaleAddCataloguesGraphQLField,
    SaleBulkDeleteGraphQLField,
    SaleChannelListingGraphQLField,
    SaleChannelListingUpdateGraphQLField,
    SaleCountableConnectionGraphQLField,
    SaleCountableEdgeGraphQLField,
    SaleCreateGraphQLField,
    SaleDeleteGraphQLField,
    SaleGraphQLField,
    SaleRemoveCataloguesGraphQLField,
    SaleTranslatableContentGraphQLField,
    SaleTranslateGraphQLField,
    SaleTranslationGraphQLField,
    SaleUpdateGraphQLField,
    SelectedAttributeGraphQLField,
    SendConfirmationEmailErrorGraphQLField,
    SendConfirmationEmailGraphQLField,
    SetPasswordGraphQLField,
    ShippingErrorGraphQLField,
    ShippingMethodChannelListingGraphQLField,
    ShippingMethodChannelListingUpdateGraphQLField,
    ShippingMethodGraphQLField,
    ShippingMethodPostalCodeRuleGraphQLField,
    ShippingMethodsPerCountryGraphQLField,
    ShippingMethodTranslatableContentGraphQLField,
    ShippingMethodTranslationGraphQLField,
    ShippingMethodTypeGraphQLField,
    ShippingPriceBulkDeleteGraphQLField,
    ShippingPriceCreateGraphQLField,
    ShippingPriceDeleteGraphQLField,
    ShippingPriceExcludeProductsGraphQLField,
    ShippingPriceRemoveProductFromExcludeGraphQLField,
    ShippingPriceTranslateGraphQLField,
    ShippingPriceUpdateGraphQLField,
    ShippingZoneBulkDeleteGraphQLField,
    ShippingZoneCountableConnectionGraphQLField,
    ShippingZoneCountableEdgeGraphQLField,
    ShippingZoneCreateGraphQLField,
    ShippingZoneDeleteGraphQLField,
    ShippingZoneGraphQLField,
    ShippingZoneUpdateGraphQLField,
    ShopAddressUpdateGraphQLField,
    ShopDomainUpdateGraphQLField,
    ShopErrorGraphQLField,
    ShopFetchTaxRatesGraphQLField,
    ShopGraphQLField,
    ShopSettingsTranslateGraphQLField,
    ShopSettingsUpdateGraphQLField,
    ShopTranslationGraphQLField,
    StaffBulkDeleteGraphQLField,
    StaffCreateGraphQLField,
    StaffDeleteGraphQLField,
    StaffErrorGraphQLField,
    StaffNotificationRecipientCreateGraphQLField,
    StaffNotificationRecipientDeleteGraphQLField,
    StaffNotificationRecipientGraphQLField,
    StaffNotificationRecipientUpdateGraphQLField,
    StaffUpdateGraphQLField,
    StockBulkResultGraphQLField,
    StockBulkUpdateErrorGraphQLField,
    StockBulkUpdateGraphQLField,
    StockCountableConnectionGraphQLField,
    StockCountableEdgeGraphQLField,
    StockErrorGraphQLField,
    StockGraphQLField,
    StockSettingsGraphQLField,
    StoredPaymentMethodGraphQLField,
    StoredPaymentMethodRequestDeleteGraphQLField,
    TaxClassCountableConnectionGraphQLField,
    TaxClassCountableEdgeGraphQLField,
    TaxClassCountryRateGraphQLField,
    TaxClassCreateErrorGraphQLField,
    TaxClassCreateGraphQLField,
    TaxClassDeleteErrorGraphQLField,
    TaxClassDeleteGraphQLField,
    TaxClassGraphQLField,
    TaxClassUpdateErrorGraphQLField,
    TaxClassUpdateGraphQLField,
    TaxConfigurationCountableConnectionGraphQLField,
    TaxConfigurationCountableEdgeGraphQLField,
    TaxConfigurationGraphQLField,
    TaxConfigurationPerCountryGraphQLField,
    TaxConfigurationUpdateErrorGraphQLField,
    TaxConfigurationUpdateGraphQLField,
    TaxCountryConfigurationDeleteErrorGraphQLField,
    TaxCountryConfigurationDeleteGraphQLField,
    TaxCountryConfigurationGraphQLField,
    TaxCountryConfigurationUpdateErrorGraphQLField,
    TaxCountryConfigurationUpdateGraphQLField,
    TaxedMoneyGraphQLField,
    TaxedMoneyRangeGraphQLField,
    TaxExemptionManageErrorGraphQLField,
    TaxExemptionManageGraphQLField,
    TaxSourceObjectUnion,
    TaxTypeGraphQLField,
    TimePeriodGraphQLField,
    TransactionCreateErrorGraphQLField,
    TransactionCreateGraphQLField,
    TransactionEventGraphQLField,
    TransactionEventReportErrorGraphQLField,
    TransactionEventReportGraphQLField,
    TransactionGraphQLField,
    TransactionInitializeErrorGraphQLField,
    TransactionInitializeGraphQLField,
    TransactionItemGraphQLField,
    TransactionProcessErrorGraphQLField,
    TransactionProcessGraphQLField,
    TransactionRequestActionErrorGraphQLField,
    TransactionRequestActionGraphQLField,
    TransactionRequestRefundForGrantedRefundErrorGraphQLField,
    TransactionRequestRefundForGrantedRefundGraphQLField,
    TransactionUpdateErrorGraphQLField,
    TransactionUpdateGraphQLField,
    TranslatableItemConnectionGraphQLField,
    TranslatableItemEdgeGraphQLField,
    TranslatableItemUnion,
    TranslationErrorGraphQLField,
    UpdateMetadataGraphQLField,
    UpdatePrivateMetadataGraphQLField,
    UploadErrorGraphQLField,
    UserAvatarDeleteGraphQLField,
    UserAvatarUpdateGraphQLField,
    UserBulkSetActiveGraphQLField,
    UserCountableConnectionGraphQLField,
    UserCountableEdgeGraphQLField,
    UserGraphQLField,
    UserOrAppUnion,
    UserPermissionGraphQLField,
    VariantMediaAssignGraphQLField,
    VariantMediaUnassignGraphQLField,
    VariantPricingInfoGraphQLField,
    VATGraphQLField,
    VerifyTokenGraphQLField,
    VoucherAddCataloguesGraphQLField,
    VoucherBulkDeleteGraphQLField,
    VoucherChannelListingGraphQLField,
    VoucherChannelListingUpdateGraphQLField,
    VoucherCodeBulkDeleteErrorGraphQLField,
    VoucherCodeBulkDeleteGraphQLField,
    VoucherCodeCountableConnectionGraphQLField,
    VoucherCodeCountableEdgeGraphQLField,
    VoucherCodeGraphQLField,
    VoucherCountableConnectionGraphQLField,
    VoucherCountableEdgeGraphQLField,
    VoucherCreateGraphQLField,
    VoucherDeleteGraphQLField,
    VoucherGraphQLField,
    VoucherRemoveCataloguesGraphQLField,
    VoucherTranslatableContentGraphQLField,
    VoucherTranslateGraphQLField,
    VoucherTranslationGraphQLField,
    VoucherUpdateGraphQLField,
    WarehouseCountableConnectionGraphQLField,
    WarehouseCountableEdgeGraphQLField,
    WarehouseCreateGraphQLField,
    WarehouseDeleteGraphQLField,
    WarehouseErrorGraphQLField,
    WarehouseGraphQLField,
    WarehouseShippingZoneAssignGraphQLField,
    WarehouseShippingZoneUnassignGraphQLField,
    WarehouseUpdateGraphQLField,
    WebhookCreateGraphQLField,
    WebhookDeleteGraphQLField,
    WebhookDryRunErrorGraphQLField,
    WebhookDryRunGraphQLField,
    WebhookErrorGraphQLField,
    WebhookEventAsyncGraphQLField,
    WebhookEventGraphQLField,
    WebhookEventSyncGraphQLField,
    WebhookGraphQLField,
    WebhookTriggerErrorGraphQLField,
    WebhookTriggerGraphQLField,
    WebhookUpdateGraphQLField,
    WeightGraphQLField,
    _ServiceGraphQLField,
)
from .base_operation import GraphQLField


class PromotionCreateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "PromotionCreateErrorFields":
        return PromotionCreateErrorFields("errors")

    @classmethod
    def promotion(cls) -> "PromotionFields":
        return PromotionFields("promotion")

    def fields(
        self,
        *subfields: Union[
            PromotionCreateGraphQLField, "PromotionFields", "PromotionCreateErrorFields"
        ]
    ) -> "PromotionCreateFields":
        self._subfields.extend(subfields)
        return self


class DomainFields(GraphQLField):
    host: DomainGraphQLField = DomainGraphQLField("host")
    ssl_enabled: DomainGraphQLField = DomainGraphQLField("sslEnabled")
    url: DomainGraphQLField = DomainGraphQLField("url")

    def fields(self, *subfields: DomainGraphQLField) -> "DomainFields":
        self._subfields.extend(subfields)
        return self


class PaymentRefundFields(GraphQLField):
    @classmethod
    def payment(cls) -> "PaymentFields":
        return PaymentFields("payment")

    @classmethod
    def payment_errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("payment_errors")

    @classmethod
    def errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentRefundGraphQLField, "PaymentFields", "PaymentErrorFields"
        ]
    ) -> "PaymentRefundFields":
        self._subfields.extend(subfields)
        return self


class TaxClassDeleteErrorFields(GraphQLField):
    field: TaxClassDeleteErrorGraphQLField = TaxClassDeleteErrorGraphQLField("field")
    message: TaxClassDeleteErrorGraphQLField = TaxClassDeleteErrorGraphQLField(
        "message"
    )
    code: TaxClassDeleteErrorGraphQLField = TaxClassDeleteErrorGraphQLField("code")

    def fields(
        self, *subfields: TaxClassDeleteErrorGraphQLField
    ) -> "TaxClassDeleteErrorFields":
        self._subfields.extend(subfields)
        return self


class PageFields(GraphQLField):
    id: PageGraphQLField = PageGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: PageGraphQLField = PageGraphQLField("privateMetafield")
    private_metafields: PageGraphQLField = PageGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: PageGraphQLField = PageGraphQLField("metafield")
    metafields: PageGraphQLField = PageGraphQLField("metafields")
    seo_title: PageGraphQLField = PageGraphQLField("seoTitle")
    seo_description: PageGraphQLField = PageGraphQLField("seoDescription")
    title: PageGraphQLField = PageGraphQLField("title")
    content: PageGraphQLField = PageGraphQLField("content")
    publication_date: PageGraphQLField = PageGraphQLField("publicationDate")
    published_at: PageGraphQLField = PageGraphQLField("publishedAt")
    is_published: PageGraphQLField = PageGraphQLField("isPublished")
    slug: PageGraphQLField = PageGraphQLField("slug")

    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    created: PageGraphQLField = PageGraphQLField("created")
    content_json: PageGraphQLField = PageGraphQLField("contentJson")

    @classmethod
    def translation(cls) -> "PageTranslationFields":
        return PageTranslationFields("translation")

    @classmethod
    def attributes(cls) -> "SelectedAttributeFields":
        return SelectedAttributeFields("attributes")

    def fields(
        self,
        *subfields: Union[
            PageGraphQLField,
            "PageTypeFields",
            "MetadataItemFields",
            "SelectedAttributeFields",
            "PageTranslationFields",
        ]
    ) -> "PageFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodFields(GraphQLField):
    id: ShippingMethodGraphQLField = ShippingMethodGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ShippingMethodGraphQLField = ShippingMethodGraphQLField(
        "privateMetafield"
    )
    private_metafields: ShippingMethodGraphQLField = ShippingMethodGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ShippingMethodGraphQLField = ShippingMethodGraphQLField("metafield")
    metafields: ShippingMethodGraphQLField = ShippingMethodGraphQLField("metafields")
    type: ShippingMethodGraphQLField = ShippingMethodGraphQLField("type")
    name: ShippingMethodGraphQLField = ShippingMethodGraphQLField("name")
    description: ShippingMethodGraphQLField = ShippingMethodGraphQLField("description")
    maximum_delivery_days: ShippingMethodGraphQLField = ShippingMethodGraphQLField(
        "maximumDeliveryDays"
    )
    minimum_delivery_days: ShippingMethodGraphQLField = ShippingMethodGraphQLField(
        "minimumDeliveryDays"
    )

    @classmethod
    def maximum_order_weight(cls) -> "WeightFields":
        return WeightFields("maximum_order_weight")

    @classmethod
    def minimum_order_weight(cls) -> "WeightFields":
        return WeightFields("minimum_order_weight")

    @classmethod
    def translation(cls) -> "ShippingMethodTranslationFields":
        return ShippingMethodTranslationFields("translation")

    @classmethod
    def price(cls) -> "MoneyFields":
        return MoneyFields("price")

    @classmethod
    def maximum_order_price(cls) -> "MoneyFields":
        return MoneyFields("maximum_order_price")

    @classmethod
    def minimum_order_price(cls) -> "MoneyFields":
        return MoneyFields("minimum_order_price")

    active: ShippingMethodGraphQLField = ShippingMethodGraphQLField("active")
    message: ShippingMethodGraphQLField = ShippingMethodGraphQLField("message")

    def fields(
        self,
        *subfields: Union[
            ShippingMethodGraphQLField,
            "WeightFields",
            "MetadataItemFields",
            "ShippingMethodTranslationFields",
            "MoneyFields",
        ]
    ) -> "ShippingMethodFields":
        self._subfields.extend(subfields)
        return self


class InvoiceUpdateFields(GraphQLField):
    @classmethod
    def invoice_errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("invoice_errors")

    @classmethod
    def errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("errors")

    @classmethod
    def invoice(cls) -> "InvoiceFields":
        return InvoiceFields("invoice")

    def fields(
        self,
        *subfields: Union[
            InvoiceUpdateGraphQLField, "InvoiceErrorFields", "InvoiceFields"
        ]
    ) -> "InvoiceUpdateFields":
        self._subfields.extend(subfields)
        return self


class OrderLineFields(GraphQLField):
    id: OrderLineGraphQLField = OrderLineGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: OrderLineGraphQLField = OrderLineGraphQLField("privateMetafield")
    private_metafields: OrderLineGraphQLField = OrderLineGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: OrderLineGraphQLField = OrderLineGraphQLField("metafield")
    metafields: OrderLineGraphQLField = OrderLineGraphQLField("metafields")
    product_name: OrderLineGraphQLField = OrderLineGraphQLField("productName")
    variant_name: OrderLineGraphQLField = OrderLineGraphQLField("variantName")
    product_sku: OrderLineGraphQLField = OrderLineGraphQLField("productSku")
    product_variant_id: OrderLineGraphQLField = OrderLineGraphQLField(
        "productVariantId"
    )
    is_shipping_required: OrderLineGraphQLField = OrderLineGraphQLField(
        "isShippingRequired"
    )
    quantity: OrderLineGraphQLField = OrderLineGraphQLField("quantity")
    quantity_fulfilled: OrderLineGraphQLField = OrderLineGraphQLField(
        "quantityFulfilled"
    )
    unit_discount_reason: OrderLineGraphQLField = OrderLineGraphQLField(
        "unitDiscountReason"
    )
    tax_rate: OrderLineGraphQLField = OrderLineGraphQLField("taxRate")

    @classmethod
    def digital_content_url(cls) -> "DigitalContentUrlFields":
        return DigitalContentUrlFields("digital_content_url")

    @classmethod
    def thumbnail(cls) -> "ImageFields":
        return ImageFields("thumbnail")

    @classmethod
    def unit_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("unit_price")

    @classmethod
    def undiscounted_unit_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("undiscounted_unit_price")

    @classmethod
    def unit_discount(cls) -> "MoneyFields":
        return MoneyFields("unit_discount")

    unit_discount_value: OrderLineGraphQLField = OrderLineGraphQLField(
        "unitDiscountValue"
    )

    @classmethod
    def total_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("total_price")

    @classmethod
    def undiscounted_total_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("undiscounted_total_price")

    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    translated_product_name: OrderLineGraphQLField = OrderLineGraphQLField(
        "translatedProductName"
    )
    translated_variant_name: OrderLineGraphQLField = OrderLineGraphQLField(
        "translatedVariantName"
    )

    @classmethod
    def allocations(cls) -> "AllocationFields":
        return AllocationFields("allocations")

    sale_id: OrderLineGraphQLField = OrderLineGraphQLField("saleId")
    quantity_to_fulfill: OrderLineGraphQLField = OrderLineGraphQLField(
        "quantityToFulfill"
    )
    unit_discount_type: OrderLineGraphQLField = OrderLineGraphQLField(
        "unitDiscountType"
    )

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    tax_class_name: OrderLineGraphQLField = OrderLineGraphQLField("taxClassName")

    @classmethod
    def tax_class_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("tax_class_metadata")

    @classmethod
    def tax_class_private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("tax_class_private_metadata")

    voucher_code: OrderLineGraphQLField = OrderLineGraphQLField("voucherCode")
    is_gift: OrderLineGraphQLField = OrderLineGraphQLField("isGift")

    def fields(
        self,
        *subfields: Union[
            OrderLineGraphQLField,
            "TaxedMoneyFields",
            "MetadataItemFields",
            "ProductVariantFields",
            "ImageFields",
            "MoneyFields",
            "TaxClassFields",
            "AllocationFields",
            "DigitalContentUrlFields",
        ]
    ) -> "OrderLineFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantTranslationFields(GraphQLField):
    id: ProductVariantTranslationGraphQLField = ProductVariantTranslationGraphQLField(
        "id"
    )

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: ProductVariantTranslationGraphQLField = ProductVariantTranslationGraphQLField(
        "name"
    )

    @classmethod
    def translatable_content(cls) -> "ProductVariantTranslatableContentFields":
        return ProductVariantTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            ProductVariantTranslationGraphQLField,
            "ProductVariantTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "ProductVariantTranslationFields":
        self._subfields.extend(subfields)
        return self


class WebhookTriggerErrorFields(GraphQLField):
    field: WebhookTriggerErrorGraphQLField = WebhookTriggerErrorGraphQLField("field")
    message: WebhookTriggerErrorGraphQLField = WebhookTriggerErrorGraphQLField(
        "message"
    )
    code: WebhookTriggerErrorGraphQLField = WebhookTriggerErrorGraphQLField("code")

    def fields(
        self, *subfields: WebhookTriggerErrorGraphQLField
    ) -> "WebhookTriggerErrorFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkTranslateFields(GraphQLField):
    count: AttributeBulkTranslateGraphQLField = AttributeBulkTranslateGraphQLField(
        "count"
    )

    @classmethod
    def results(cls) -> "AttributeBulkTranslateResultFields":
        return AttributeBulkTranslateResultFields("results")

    @classmethod
    def errors(cls) -> "AttributeBulkTranslateErrorFields":
        return AttributeBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeBulkTranslateGraphQLField,
            "AttributeBulkTranslateErrorFields",
            "AttributeBulkTranslateResultFields",
        ]
    ) -> "AttributeBulkTranslateFields":
        self._subfields.extend(subfields)
        return self


class SaleFields(GraphQLField):
    id: SaleGraphQLField = SaleGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: SaleGraphQLField = SaleGraphQLField("privateMetafield")
    private_metafields: SaleGraphQLField = SaleGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: SaleGraphQLField = SaleGraphQLField("metafield")
    metafields: SaleGraphQLField = SaleGraphQLField("metafields")
    name: SaleGraphQLField = SaleGraphQLField("name")
    type: SaleGraphQLField = SaleGraphQLField("type")
    start_date: SaleGraphQLField = SaleGraphQLField("startDate")
    end_date: SaleGraphQLField = SaleGraphQLField("endDate")
    created: SaleGraphQLField = SaleGraphQLField("created")
    updated_at: SaleGraphQLField = SaleGraphQLField("updatedAt")

    @classmethod
    def categories(cls) -> "CategoryCountableConnectionFields":
        return CategoryCountableConnectionFields("categories")

    @classmethod
    def collections(cls) -> "CollectionCountableConnectionFields":
        return CollectionCountableConnectionFields("collections")

    @classmethod
    def products(cls) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields("products")

    @classmethod
    def variants(cls) -> "ProductVariantCountableConnectionFields":
        return ProductVariantCountableConnectionFields("variants")

    @classmethod
    def translation(cls) -> "SaleTranslationFields":
        return SaleTranslationFields("translation")

    @classmethod
    def channel_listings(cls) -> "SaleChannelListingFields":
        return SaleChannelListingFields("channel_listings")

    discount_value: SaleGraphQLField = SaleGraphQLField("discountValue")
    currency: SaleGraphQLField = SaleGraphQLField("currency")

    def fields(
        self,
        *subfields: Union[
            SaleGraphQLField,
            "CollectionCountableConnectionFields",
            "MetadataItemFields",
            "ProductCountableConnectionFields",
            "SaleChannelListingFields",
            "CategoryCountableConnectionFields",
            "SaleTranslationFields",
            "ProductVariantCountableConnectionFields",
        ]
    ) -> "SaleFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ProductVariantFields":
        return ProductVariantFields("node")

    cursor: ProductVariantCountableEdgeGraphQLField = (
        ProductVariantCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[
            ProductVariantCountableEdgeGraphQLField, "ProductVariantFields"
        ]
    ) -> "ProductVariantCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class CheckoutEmailUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutEmailUpdateGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutEmailUpdateFields":
        self._subfields.extend(subfields)
        return self


class TaxClassDeleteFields(GraphQLField):
    @classmethod
    def errors(cls) -> "TaxClassDeleteErrorFields":
        return TaxClassDeleteErrorFields("errors")

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    def fields(
        self,
        *subfields: Union[
            TaxClassDeleteGraphQLField, "TaxClassDeleteErrorFields", "TaxClassFields"
        ]
    ) -> "TaxClassDeleteFields":
        self._subfields.extend(subfields)
        return self


class FileFields(GraphQLField):
    url: FileGraphQLField = FileGraphQLField("url")
    content_type: FileGraphQLField = FileGraphQLField("contentType")

    def fields(self, *subfields: FileGraphQLField) -> "FileFields":
        self._subfields.extend(subfields)
        return self


class CustomerBulkDeleteFields(GraphQLField):
    count: CustomerBulkDeleteGraphQLField = CustomerBulkDeleteGraphQLField("count")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self, *subfields: Union[CustomerBulkDeleteGraphQLField, "AccountErrorFields"]
    ) -> "CustomerBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class WebhookDryRunErrorFields(GraphQLField):
    field: WebhookDryRunErrorGraphQLField = WebhookDryRunErrorGraphQLField("field")
    message: WebhookDryRunErrorGraphQLField = WebhookDryRunErrorGraphQLField("message")
    code: WebhookDryRunErrorGraphQLField = WebhookDryRunErrorGraphQLField("code")

    def fields(
        self, *subfields: WebhookDryRunErrorGraphQLField
    ) -> "WebhookDryRunErrorFields":
        self._subfields.extend(subfields)
        return self


class GiftCardEventFields(GraphQLField):
    id: GiftCardEventGraphQLField = GiftCardEventGraphQLField("id")
    date: GiftCardEventGraphQLField = GiftCardEventGraphQLField("date")
    type: GiftCardEventGraphQLField = GiftCardEventGraphQLField("type")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    message: GiftCardEventGraphQLField = GiftCardEventGraphQLField("message")
    email: GiftCardEventGraphQLField = GiftCardEventGraphQLField("email")
    order_id: GiftCardEventGraphQLField = GiftCardEventGraphQLField("orderId")
    order_number: GiftCardEventGraphQLField = GiftCardEventGraphQLField("orderNumber")
    tags: GiftCardEventGraphQLField = GiftCardEventGraphQLField("tags")
    old_tags: GiftCardEventGraphQLField = GiftCardEventGraphQLField("oldTags")

    @classmethod
    def balance(cls) -> "GiftCardEventBalanceFields":
        return GiftCardEventBalanceFields("balance")

    expiry_date: GiftCardEventGraphQLField = GiftCardEventGraphQLField("expiryDate")
    old_expiry_date: GiftCardEventGraphQLField = GiftCardEventGraphQLField(
        "oldExpiryDate"
    )

    def fields(
        self,
        *subfields: Union[
            GiftCardEventGraphQLField,
            "GiftCardEventBalanceFields",
            "AppFields",
            "UserFields",
        ]
    ) -> "GiftCardEventFields":
        self._subfields.extend(subfields)
        return self


class AppExtensionCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "AppExtensionCountableEdgeFields":
        return AppExtensionCountableEdgeFields("edges")

    total_count: AppExtensionCountableConnectionGraphQLField = (
        AppExtensionCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            AppExtensionCountableConnectionGraphQLField,
            "AppExtensionCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "AppExtensionCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class AccountAddressDeleteFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    def fields(
        self,
        *subfields: Union[
            AccountAddressDeleteGraphQLField,
            "AccountErrorFields",
            "UserFields",
            "AddressFields",
        ]
    ) -> "AccountAddressDeleteFields":
        self._subfields.extend(subfields)
        return self


class UserCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "UserCountableEdgeFields":
        return UserCountableEdgeFields("edges")

    total_count: UserCountableConnectionGraphQLField = (
        UserCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            UserCountableConnectionGraphQLField,
            "PageInfoFields",
            "UserCountableEdgeFields",
        ]
    ) -> "UserCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class CollectionCreateFields(GraphQLField):
    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    def fields(
        self,
        *subfields: Union[
            CollectionCreateGraphQLField, "CollectionFields", "CollectionErrorFields"
        ]
    ) -> "CollectionCreateFields":
        self._subfields.extend(subfields)
        return self


class DraftOrderLinesBulkDeleteFields(GraphQLField):
    count: DraftOrderLinesBulkDeleteGraphQLField = (
        DraftOrderLinesBulkDeleteGraphQLField("count")
    )

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[DraftOrderLinesBulkDeleteGraphQLField, "OrderErrorFields"]
    ) -> "DraftOrderLinesBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class PromotionUpdateErrorFields(GraphQLField):
    field: PromotionUpdateErrorGraphQLField = PromotionUpdateErrorGraphQLField("field")
    message: PromotionUpdateErrorGraphQLField = PromotionUpdateErrorGraphQLField(
        "message"
    )
    code: PromotionUpdateErrorGraphQLField = PromotionUpdateErrorGraphQLField("code")

    def fields(
        self, *subfields: PromotionUpdateErrorGraphQLField
    ) -> "PromotionUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class AppUpdateFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    def fields(
        self, *subfields: Union[AppUpdateGraphQLField, "AppErrorFields", "AppFields"]
    ) -> "AppUpdateFields":
        self._subfields.extend(subfields)
        return self


class DeletePrivateMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadata_errors")

    @classmethod
    def errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("errors")

    item: ObjectWithMetadataInterface = ObjectWithMetadataInterface("item")

    def fields(
        self,
        *subfields: Union[
            DeletePrivateMetadataGraphQLField,
            "MetadataErrorFields",
            "ObjectWithMetadataInterface",
        ]
    ) -> "DeletePrivateMetadataFields":
        self._subfields.extend(subfields)
        return self


class OrderLineDeleteFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderLineDeleteGraphQLField,
            "OrderErrorFields",
            "OrderFields",
            "OrderLineFields",
        ]
    ) -> "OrderLineDeleteFields":
        self._subfields.extend(subfields)
        return self


class VoucherAddCataloguesFields(GraphQLField):
    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            VoucherAddCataloguesGraphQLField, "VoucherFields", "DiscountErrorFields"
        ]
    ) -> "VoucherAddCataloguesFields":
        self._subfields.extend(subfields)
        return self


class InvoiceErrorFields(GraphQLField):
    field: InvoiceErrorGraphQLField = InvoiceErrorGraphQLField("field")
    message: InvoiceErrorGraphQLField = InvoiceErrorGraphQLField("message")
    code: InvoiceErrorGraphQLField = InvoiceErrorGraphQLField("code")

    def fields(self, *subfields: InvoiceErrorGraphQLField) -> "InvoiceErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkTranslateErrorFields(GraphQLField):
    path: ProductVariantBulkTranslateErrorGraphQLField = (
        ProductVariantBulkTranslateErrorGraphQLField("path")
    )
    message: ProductVariantBulkTranslateErrorGraphQLField = (
        ProductVariantBulkTranslateErrorGraphQLField("message")
    )
    code: ProductVariantBulkTranslateErrorGraphQLField = (
        ProductVariantBulkTranslateErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: ProductVariantBulkTranslateErrorGraphQLField
    ) -> "ProductVariantBulkTranslateErrorFields":
        self._subfields.extend(subfields)
        return self


class PermissionFields(GraphQLField):
    code: PermissionGraphQLField = PermissionGraphQLField("code")
    name: PermissionGraphQLField = PermissionGraphQLField("name")

    def fields(self, *subfields: PermissionGraphQLField) -> "PermissionFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkUpdateFields(GraphQLField):
    count: AttributeBulkUpdateGraphQLField = AttributeBulkUpdateGraphQLField("count")

    @classmethod
    def results(cls) -> "AttributeBulkUpdateResultFields":
        return AttributeBulkUpdateResultFields("results")

    @classmethod
    def errors(cls) -> "AttributeBulkUpdateErrorFields":
        return AttributeBulkUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeBulkUpdateGraphQLField,
            "AttributeBulkUpdateResultFields",
            "AttributeBulkUpdateErrorFields",
        ]
    ) -> "AttributeBulkUpdateFields":
        self._subfields.extend(subfields)
        return self


class WebhookDeleteFields(GraphQLField):
    @classmethod
    def webhook_errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("webhook_errors")

    @classmethod
    def errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("errors")

    @classmethod
    def webhook(cls) -> "WebhookFields":
        return WebhookFields("webhook")

    def fields(
        self,
        *subfields: Union[
            WebhookDeleteGraphQLField, "WebhookErrorFields", "WebhookFields"
        ]
    ) -> "WebhookDeleteFields":
        self._subfields.extend(subfields)
        return self


class PageTypeBulkDeleteFields(GraphQLField):
    count: PageTypeBulkDeleteGraphQLField = PageTypeBulkDeleteGraphQLField("count")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self, *subfields: Union[PageTypeBulkDeleteGraphQLField, "PageErrorFields"]
    ) -> "PageTypeBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class PaymentMethodInitializeTokenizationFields(GraphQLField):
    result: PaymentMethodInitializeTokenizationGraphQLField = (
        PaymentMethodInitializeTokenizationGraphQLField("result")
    )
    id: PaymentMethodInitializeTokenizationGraphQLField = (
        PaymentMethodInitializeTokenizationGraphQLField("id")
    )
    data: PaymentMethodInitializeTokenizationGraphQLField = (
        PaymentMethodInitializeTokenizationGraphQLField("data")
    )

    @classmethod
    def errors(cls) -> "PaymentMethodInitializeTokenizationErrorFields":
        return PaymentMethodInitializeTokenizationErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentMethodInitializeTokenizationGraphQLField,
            "PaymentMethodInitializeTokenizationErrorFields",
        ]
    ) -> "PaymentMethodInitializeTokenizationFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleDeletedEventFields(GraphQLField):
    id: PromotionRuleDeletedEventGraphQLField = PromotionRuleDeletedEventGraphQLField(
        "id"
    )
    date: PromotionRuleDeletedEventGraphQLField = PromotionRuleDeletedEventGraphQLField(
        "date"
    )
    type: PromotionRuleDeletedEventGraphQLField = PromotionRuleDeletedEventGraphQLField(
        "type"
    )
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")
    rule_id: PromotionRuleDeletedEventGraphQLField = (
        PromotionRuleDeletedEventGraphQLField("ruleId")
    )

    def fields(
        self, *subfields: Union[PromotionRuleDeletedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionRuleDeletedEventFields":
        self._subfields.extend(subfields)
        return self


class AttributeErrorFields(GraphQLField):
    field: AttributeErrorGraphQLField = AttributeErrorGraphQLField("field")
    message: AttributeErrorGraphQLField = AttributeErrorGraphQLField("message")
    code: AttributeErrorGraphQLField = AttributeErrorGraphQLField("code")

    def fields(self, *subfields: AttributeErrorGraphQLField) -> "AttributeErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantDeleteFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    def fields(
        self,
        *subfields: Union[
            ProductVariantDeleteGraphQLField,
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "ProductVariantDeleteFields":
        self._subfields.extend(subfields)
        return self


class CheckoutRemovePromoCodeFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutRemovePromoCodeGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutRemovePromoCodeFields":
        self._subfields.extend(subfields)
        return self


class CategoryTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    def fields(
        self,
        *subfields: Union[
            CategoryTranslateGraphQLField, "TranslationErrorFields", "CategoryFields"
        ]
    ) -> "CategoryTranslateFields":
        self._subfields.extend(subfields)
        return self


class DiscountErrorFields(GraphQLField):
    field: DiscountErrorGraphQLField = DiscountErrorGraphQLField("field")
    message: DiscountErrorGraphQLField = DiscountErrorGraphQLField("message")
    products: DiscountErrorGraphQLField = DiscountErrorGraphQLField("products")
    code: DiscountErrorGraphQLField = DiscountErrorGraphQLField("code")
    channels: DiscountErrorGraphQLField = DiscountErrorGraphQLField("channels")
    voucher_codes: DiscountErrorGraphQLField = DiscountErrorGraphQLField("voucherCodes")

    def fields(self, *subfields: DiscountErrorGraphQLField) -> "DiscountErrorFields":
        self._subfields.extend(subfields)
        return self


class VoucherTranslatableContentFields(GraphQLField):
    id: VoucherTranslatableContentGraphQLField = VoucherTranslatableContentGraphQLField(
        "id"
    )
    voucher_id: VoucherTranslatableContentGraphQLField = (
        VoucherTranslatableContentGraphQLField("voucherId")
    )
    name: VoucherTranslatableContentGraphQLField = (
        VoucherTranslatableContentGraphQLField("name")
    )

    @classmethod
    def translation(cls) -> "VoucherTranslationFields":
        return VoucherTranslationFields("translation")

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    def fields(
        self,
        *subfields: Union[
            VoucherTranslatableContentGraphQLField,
            "VoucherFields",
            "VoucherTranslationFields",
        ]
    ) -> "VoucherTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class PaymentErrorFields(GraphQLField):
    field: PaymentErrorGraphQLField = PaymentErrorGraphQLField("field")
    message: PaymentErrorGraphQLField = PaymentErrorGraphQLField("message")
    code: PaymentErrorGraphQLField = PaymentErrorGraphQLField("code")
    variants: PaymentErrorGraphQLField = PaymentErrorGraphQLField("variants")

    def fields(self, *subfields: PaymentErrorGraphQLField) -> "PaymentErrorFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLineDeleteFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutLineDeleteGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutLineDeleteFields":
        self._subfields.extend(subfields)
        return self


class VoucherBulkDeleteFields(GraphQLField):
    count: VoucherBulkDeleteGraphQLField = VoucherBulkDeleteGraphQLField("count")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self, *subfields: Union[VoucherBulkDeleteGraphQLField, "DiscountErrorFields"]
    ) -> "VoucherBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class InvoiceCreateFields(GraphQLField):
    @classmethod
    def invoice_errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("invoice_errors")

    @classmethod
    def errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("errors")

    @classmethod
    def invoice(cls) -> "InvoiceFields":
        return InvoiceFields("invoice")

    def fields(
        self,
        *subfields: Union[
            InvoiceCreateGraphQLField, "InvoiceErrorFields", "InvoiceFields"
        ]
    ) -> "InvoiceCreateFields":
        self._subfields.extend(subfields)
        return self


class CategoryBulkDeleteFields(GraphQLField):
    count: CategoryBulkDeleteGraphQLField = CategoryBulkDeleteGraphQLField("count")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self, *subfields: Union[CategoryBulkDeleteGraphQLField, "ProductErrorFields"]
    ) -> "CategoryBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class MoneyFields(GraphQLField):
    currency: MoneyGraphQLField = MoneyGraphQLField("currency")
    amount: MoneyGraphQLField = MoneyGraphQLField("amount")

    def fields(self, *subfields: MoneyGraphQLField) -> "MoneyFields":
        self._subfields.extend(subfields)
        return self


class PaymentMethodProcessTokenizationErrorFields(GraphQLField):
    field: PaymentMethodProcessTokenizationErrorGraphQLField = (
        PaymentMethodProcessTokenizationErrorGraphQLField("field")
    )
    message: PaymentMethodProcessTokenizationErrorGraphQLField = (
        PaymentMethodProcessTokenizationErrorGraphQLField("message")
    )
    code: PaymentMethodProcessTokenizationErrorGraphQLField = (
        PaymentMethodProcessTokenizationErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: PaymentMethodProcessTokenizationErrorGraphQLField
    ) -> "PaymentMethodProcessTokenizationErrorFields":
        self._subfields.extend(subfields)
        return self


class CategoryCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "CategoryCountableEdgeFields":
        return CategoryCountableEdgeFields("edges")

    total_count: CategoryCountableConnectionGraphQLField = (
        CategoryCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            CategoryCountableConnectionGraphQLField,
            "CategoryCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "CategoryCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PromotionCreateErrorFields(GraphQLField):
    field: PromotionCreateErrorGraphQLField = PromotionCreateErrorGraphQLField("field")
    message: PromotionCreateErrorGraphQLField = PromotionCreateErrorGraphQLField(
        "message"
    )
    code: PromotionCreateErrorGraphQLField = PromotionCreateErrorGraphQLField("code")
    index: PromotionCreateErrorGraphQLField = PromotionCreateErrorGraphQLField("index")
    rules_limit: PromotionCreateErrorGraphQLField = PromotionCreateErrorGraphQLField(
        "rulesLimit"
    )
    rules_limit_exceed_by: PromotionCreateErrorGraphQLField = (
        PromotionCreateErrorGraphQLField("rulesLimitExceedBy")
    )
    gifts_limit: PromotionCreateErrorGraphQLField = PromotionCreateErrorGraphQLField(
        "giftsLimit"
    )
    gifts_limit_exceed_by: PromotionCreateErrorGraphQLField = (
        PromotionCreateErrorGraphQLField("giftsLimitExceedBy")
    )

    def fields(
        self, *subfields: PromotionCreateErrorGraphQLField
    ) -> "PromotionCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class VoucherUpdateFields(GraphQLField):
    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    def fields(
        self,
        *subfields: Union[
            VoucherUpdateGraphQLField, "VoucherFields", "DiscountErrorFields"
        ]
    ) -> "VoucherUpdateFields":
        self._subfields.extend(subfields)
        return self


class ShopAddressUpdateFields(GraphQLField):
    @classmethod
    def shop(cls) -> "ShopFields":
        return ShopFields("shop")

    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShopAddressUpdateGraphQLField, "ShopErrorFields", "ShopFields"
        ]
    ) -> "ShopAddressUpdateFields":
        self._subfields.extend(subfields)
        return self


class AppExtensionCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "AppExtensionFields":
        return AppExtensionFields("node")

    cursor: AppExtensionCountableEdgeGraphQLField = (
        AppExtensionCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[AppExtensionCountableEdgeGraphQLField, "AppExtensionFields"]
    ) -> "AppExtensionCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class InvoiceRequestFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def invoice_errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("invoice_errors")

    @classmethod
    def errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("errors")

    @classmethod
    def invoice(cls) -> "InvoiceFields":
        return InvoiceFields("invoice")

    def fields(
        self,
        *subfields: Union[
            InvoiceRequestGraphQLField,
            "InvoiceErrorFields",
            "InvoiceFields",
            "OrderFields",
        ]
    ) -> "InvoiceRequestFields":
        self._subfields.extend(subfields)
        return self


class GiftCardAddNoteFields(GraphQLField):
    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    @classmethod
    def event(cls) -> "GiftCardEventFields":
        return GiftCardEventFields("event")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            GiftCardAddNoteGraphQLField,
            "GiftCardErrorFields",
            "GiftCardEventFields",
            "GiftCardFields",
        ]
    ) -> "GiftCardAddNoteFields":
        self._subfields.extend(subfields)
        return self


class PaymentCheckBalanceFields(GraphQLField):
    data: PaymentCheckBalanceGraphQLField = PaymentCheckBalanceGraphQLField("data")

    @classmethod
    def payment_errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("payment_errors")

    @classmethod
    def errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("errors")

    def fields(
        self, *subfields: Union[PaymentCheckBalanceGraphQLField, "PaymentErrorFields"]
    ) -> "PaymentCheckBalanceFields":
        self._subfields.extend(subfields)
        return self


class OrderBulkCreateErrorFields(GraphQLField):
    path: OrderBulkCreateErrorGraphQLField = OrderBulkCreateErrorGraphQLField("path")
    message: OrderBulkCreateErrorGraphQLField = OrderBulkCreateErrorGraphQLField(
        "message"
    )
    code: OrderBulkCreateErrorGraphQLField = OrderBulkCreateErrorGraphQLField("code")

    def fields(
        self, *subfields: OrderBulkCreateErrorGraphQLField
    ) -> "OrderBulkCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleCreateErrorFields(GraphQLField):
    field: PromotionRuleCreateErrorGraphQLField = PromotionRuleCreateErrorGraphQLField(
        "field"
    )
    message: PromotionRuleCreateErrorGraphQLField = (
        PromotionRuleCreateErrorGraphQLField("message")
    )
    code: PromotionRuleCreateErrorGraphQLField = PromotionRuleCreateErrorGraphQLField(
        "code"
    )
    rules_limit: PromotionRuleCreateErrorGraphQLField = (
        PromotionRuleCreateErrorGraphQLField("rulesLimit")
    )
    rules_limit_exceed_by: PromotionRuleCreateErrorGraphQLField = (
        PromotionRuleCreateErrorGraphQLField("rulesLimitExceedBy")
    )
    gifts_limit: PromotionRuleCreateErrorGraphQLField = (
        PromotionRuleCreateErrorGraphQLField("giftsLimit")
    )
    gifts_limit_exceed_by: PromotionRuleCreateErrorGraphQLField = (
        PromotionRuleCreateErrorGraphQLField("giftsLimitExceedBy")
    )

    def fields(
        self, *subfields: PromotionRuleCreateErrorGraphQLField
    ) -> "PromotionRuleCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class PermissionGroupCreateFields(GraphQLField):
    @classmethod
    def permission_group_errors(cls) -> "PermissionGroupErrorFields":
        return PermissionGroupErrorFields("permission_group_errors")

    @classmethod
    def errors(cls) -> "PermissionGroupErrorFields":
        return PermissionGroupErrorFields("errors")

    @classmethod
    def group(cls) -> "GroupFields":
        return GroupFields("group")

    def fields(
        self,
        *subfields: Union[
            PermissionGroupCreateGraphQLField,
            "PermissionGroupErrorFields",
            "GroupFields",
        ]
    ) -> "PermissionGroupCreateFields":
        self._subfields.extend(subfields)
        return self


class BulkStockErrorFields(GraphQLField):
    field: BulkStockErrorGraphQLField = BulkStockErrorGraphQLField("field")
    message: BulkStockErrorGraphQLField = BulkStockErrorGraphQLField("message")
    code: BulkStockErrorGraphQLField = BulkStockErrorGraphQLField("code")
    attributes: BulkStockErrorGraphQLField = BulkStockErrorGraphQLField("attributes")
    values: BulkStockErrorGraphQLField = BulkStockErrorGraphQLField("values")
    index: BulkStockErrorGraphQLField = BulkStockErrorGraphQLField("index")

    def fields(self, *subfields: BulkStockErrorGraphQLField) -> "BulkStockErrorFields":
        self._subfields.extend(subfields)
        return self


class AppManifestWebhookFields(GraphQLField):
    name: AppManifestWebhookGraphQLField = AppManifestWebhookGraphQLField("name")
    async_events: AppManifestWebhookGraphQLField = AppManifestWebhookGraphQLField(
        "asyncEvents"
    )
    sync_events: AppManifestWebhookGraphQLField = AppManifestWebhookGraphQLField(
        "syncEvents"
    )
    query: AppManifestWebhookGraphQLField = AppManifestWebhookGraphQLField("query")
    target_url: AppManifestWebhookGraphQLField = AppManifestWebhookGraphQLField(
        "targetUrl"
    )

    def fields(
        self, *subfields: AppManifestWebhookGraphQLField
    ) -> "AppManifestWebhookFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueDeleteFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    @classmethod
    def attribute_value(cls) -> "AttributeValueFields":
        return AttributeValueFields("attribute_value")

    def fields(
        self,
        *subfields: Union[
            AttributeValueDeleteGraphQLField,
            "AttributeFields",
            "AttributeValueFields",
            "AttributeErrorFields",
        ]
    ) -> "AttributeValueDeleteFields":
        self._subfields.extend(subfields)
        return self


class ProductCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ProductFields":
        return ProductFields("node")

    cursor: ProductCountableEdgeGraphQLField = ProductCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[ProductCountableEdgeGraphQLField, "ProductFields"]
    ) -> "ProductCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class AddressDeleteFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    def fields(
        self,
        *subfields: Union[
            AddressDeleteGraphQLField,
            "AccountErrorFields",
            "UserFields",
            "AddressFields",
        ]
    ) -> "AddressDeleteFields":
        self._subfields.extend(subfields)
        return self


class AttributeFields(GraphQLField):
    id: AttributeGraphQLField = AttributeGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: AttributeGraphQLField = AttributeGraphQLField("privateMetafield")
    private_metafields: AttributeGraphQLField = AttributeGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: AttributeGraphQLField = AttributeGraphQLField("metafield")
    metafields: AttributeGraphQLField = AttributeGraphQLField("metafields")
    input_type: AttributeGraphQLField = AttributeGraphQLField("inputType")
    entity_type: AttributeGraphQLField = AttributeGraphQLField("entityType")
    name: AttributeGraphQLField = AttributeGraphQLField("name")
    slug: AttributeGraphQLField = AttributeGraphQLField("slug")
    type: AttributeGraphQLField = AttributeGraphQLField("type")
    unit: AttributeGraphQLField = AttributeGraphQLField("unit")

    @classmethod
    def choices(cls) -> "AttributeValueCountableConnectionFields":
        return AttributeValueCountableConnectionFields("choices")

    value_required: AttributeGraphQLField = AttributeGraphQLField("valueRequired")
    visible_in_storefront: AttributeGraphQLField = AttributeGraphQLField(
        "visibleInStorefront"
    )
    filterable_in_storefront: AttributeGraphQLField = AttributeGraphQLField(
        "filterableInStorefront"
    )
    filterable_in_dashboard: AttributeGraphQLField = AttributeGraphQLField(
        "filterableInDashboard"
    )
    available_in_grid: AttributeGraphQLField = AttributeGraphQLField("availableInGrid")
    storefront_search_position: AttributeGraphQLField = AttributeGraphQLField(
        "storefrontSearchPosition"
    )

    @classmethod
    def translation(cls) -> "AttributeTranslationFields":
        return AttributeTranslationFields("translation")

    with_choices: AttributeGraphQLField = AttributeGraphQLField("withChoices")

    @classmethod
    def product_types(cls) -> "ProductTypeCountableConnectionFields":
        return ProductTypeCountableConnectionFields("product_types")

    @classmethod
    def product_variant_types(cls) -> "ProductTypeCountableConnectionFields":
        return ProductTypeCountableConnectionFields("product_variant_types")

    external_reference: AttributeGraphQLField = AttributeGraphQLField(
        "externalReference"
    )

    def fields(
        self,
        *subfields: Union[
            AttributeGraphQLField,
            "AttributeValueCountableConnectionFields",
            "MetadataItemFields",
            "ProductTypeCountableConnectionFields",
            "AttributeTranslationFields",
        ]
    ) -> "AttributeFields":
        self._subfields.extend(subfields)
        return self


class PaymentMethodRequestDeleteErrorFields(GraphQLField):
    field: PaymentMethodRequestDeleteErrorGraphQLField = (
        PaymentMethodRequestDeleteErrorGraphQLField("field")
    )
    message: PaymentMethodRequestDeleteErrorGraphQLField = (
        PaymentMethodRequestDeleteErrorGraphQLField("message")
    )
    code: PaymentMethodRequestDeleteErrorGraphQLField = (
        PaymentMethodRequestDeleteErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: PaymentMethodRequestDeleteErrorGraphQLField
    ) -> "PaymentMethodRequestDeleteErrorFields":
        self._subfields.extend(subfields)
        return self


class AppBrandLogoFields(GraphQLField):
    default: AppBrandLogoGraphQLField = AppBrandLogoGraphQLField("default")

    def fields(self, *subfields: AppBrandLogoGraphQLField) -> "AppBrandLogoFields":
        self._subfields.extend(subfields)
        return self


class ExportEventFields(GraphQLField):
    id: ExportEventGraphQLField = ExportEventGraphQLField("id")
    date: ExportEventGraphQLField = ExportEventGraphQLField("date")
    type: ExportEventGraphQLField = ExportEventGraphQLField("type")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    message: ExportEventGraphQLField = ExportEventGraphQLField("message")

    def fields(
        self, *subfields: Union[ExportEventGraphQLField, "AppFields", "UserFields"]
    ) -> "ExportEventFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkTranslateResultFields(GraphQLField):
    @classmethod
    def translation(cls) -> "ProductTranslationFields":
        return ProductTranslationFields("translation")

    @classmethod
    def errors(cls) -> "ProductBulkTranslateErrorFields":
        return ProductBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductBulkTranslateResultGraphQLField,
            "ProductBulkTranslateErrorFields",
            "ProductTranslationFields",
        ]
    ) -> "ProductBulkTranslateResultFields":
        self._subfields.extend(subfields)
        return self


class BulkProductErrorFields(GraphQLField):
    field: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField("field")
    message: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField("message")
    code: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField("code")
    attributes: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField(
        "attributes"
    )
    values: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField("values")
    index: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField("index")
    warehouses: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField(
        "warehouses"
    )
    channels: BulkProductErrorGraphQLField = BulkProductErrorGraphQLField("channels")

    def fields(
        self, *subfields: BulkProductErrorGraphQLField
    ) -> "BulkProductErrorFields":
        self._subfields.extend(subfields)
        return self


class LanguageDisplayFields(GraphQLField):
    code: LanguageDisplayGraphQLField = LanguageDisplayGraphQLField("code")
    language: LanguageDisplayGraphQLField = LanguageDisplayGraphQLField("language")

    def fields(
        self, *subfields: LanguageDisplayGraphQLField
    ) -> "LanguageDisplayFields":
        self._subfields.extend(subfields)
        return self


class CollectionChannelListingFields(GraphQLField):
    id: CollectionChannelListingGraphQLField = CollectionChannelListingGraphQLField(
        "id"
    )
    publication_date: CollectionChannelListingGraphQLField = (
        CollectionChannelListingGraphQLField("publicationDate")
    )
    published_at: CollectionChannelListingGraphQLField = (
        CollectionChannelListingGraphQLField("publishedAt")
    )
    is_published: CollectionChannelListingGraphQLField = (
        CollectionChannelListingGraphQLField("isPublished")
    )

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    def fields(
        self, *subfields: Union[CollectionChannelListingGraphQLField, "ChannelFields"]
    ) -> "CollectionChannelListingFields":
        self._subfields.extend(subfields)
        return self


class GiftCardSettingsErrorFields(GraphQLField):
    field: GiftCardSettingsErrorGraphQLField = GiftCardSettingsErrorGraphQLField(
        "field"
    )
    message: GiftCardSettingsErrorGraphQLField = GiftCardSettingsErrorGraphQLField(
        "message"
    )
    code: GiftCardSettingsErrorGraphQLField = GiftCardSettingsErrorGraphQLField("code")

    def fields(
        self, *subfields: GiftCardSettingsErrorGraphQLField
    ) -> "GiftCardSettingsErrorFields":
        self._subfields.extend(subfields)
        return self


class PaymentCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "PaymentCountableEdgeFields":
        return PaymentCountableEdgeFields("edges")

    total_count: PaymentCountableConnectionGraphQLField = (
        PaymentCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            PaymentCountableConnectionGraphQLField,
            "PaymentCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "PaymentCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class ExportGiftCardsFields(GraphQLField):
    @classmethod
    def export_file(cls) -> "ExportFileFields":
        return ExportFileFields("export_file")

    @classmethod
    def errors(cls) -> "ExportErrorFields":
        return ExportErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExportGiftCardsGraphQLField, "ExportFileFields", "ExportErrorFields"
        ]
    ) -> "ExportGiftCardsFields":
        self._subfields.extend(subfields)
        return self


class VATFields(GraphQLField):
    country_code: VATGraphQLField = VATGraphQLField("countryCode")
    standard_rate: VATGraphQLField = VATGraphQLField("standardRate")

    @classmethod
    def reduced_rates(cls) -> "ReducedRateFields":
        return ReducedRateFields("reduced_rates")

    def fields(
        self, *subfields: Union[VATGraphQLField, "ReducedRateFields"]
    ) -> "VATFields":
        self._subfields.extend(subfields)
        return self


class TransactionInitializeFields(GraphQLField):
    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def transaction_event(cls) -> "TransactionEventFields":
        return TransactionEventFields("transaction_event")

    data: TransactionInitializeGraphQLField = TransactionInitializeGraphQLField("data")

    @classmethod
    def errors(cls) -> "TransactionInitializeErrorFields":
        return TransactionInitializeErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionInitializeGraphQLField,
            "TransactionItemFields",
            "TransactionInitializeErrorFields",
            "TransactionEventFields",
        ]
    ) -> "TransactionInitializeFields":
        self._subfields.extend(subfields)
        return self


class OrderBulkCancelFields(GraphQLField):
    count: OrderBulkCancelGraphQLField = OrderBulkCancelGraphQLField("count")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self, *subfields: Union[OrderBulkCancelGraphQLField, "OrderErrorFields"]
    ) -> "OrderBulkCancelFields":
        self._subfields.extend(subfields)
        return self


class ExternalObtainAccessTokensFields(GraphQLField):
    token: ExternalObtainAccessTokensGraphQLField = (
        ExternalObtainAccessTokensGraphQLField("token")
    )
    refresh_token: ExternalObtainAccessTokensGraphQLField = (
        ExternalObtainAccessTokensGraphQLField("refreshToken")
    )
    csrf_token: ExternalObtainAccessTokensGraphQLField = (
        ExternalObtainAccessTokensGraphQLField("csrfToken")
    )

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExternalObtainAccessTokensGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "ExternalObtainAccessTokensFields":
        self._subfields.extend(subfields)
        return self


class ConfigurationItemFields(GraphQLField):
    name: ConfigurationItemGraphQLField = ConfigurationItemGraphQLField("name")
    value: ConfigurationItemGraphQLField = ConfigurationItemGraphQLField("value")
    type: ConfigurationItemGraphQLField = ConfigurationItemGraphQLField("type")
    help_text: ConfigurationItemGraphQLField = ConfigurationItemGraphQLField("helpText")
    label: ConfigurationItemGraphQLField = ConfigurationItemGraphQLField("label")

    def fields(
        self, *subfields: ConfigurationItemGraphQLField
    ) -> "ConfigurationItemFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentUpdateFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    @classmethod
    def content(cls) -> "DigitalContentFields":
        return DigitalContentFields("content")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            DigitalContentUpdateGraphQLField,
            "DigitalContentFields",
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "DigitalContentUpdateFields":
        self._subfields.extend(subfields)
        return self


class DraftOrderCompleteFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            DraftOrderCompleteGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "DraftOrderCompleteFields":
        self._subfields.extend(subfields)
        return self


class VoucherCodeFields(GraphQLField):
    id: VoucherCodeGraphQLField = VoucherCodeGraphQLField("id")
    code: VoucherCodeGraphQLField = VoucherCodeGraphQLField("code")
    used: VoucherCodeGraphQLField = VoucherCodeGraphQLField("used")
    is_active: VoucherCodeGraphQLField = VoucherCodeGraphQLField("isActive")
    created_at: VoucherCodeGraphQLField = VoucherCodeGraphQLField("createdAt")

    def fields(self, *subfields: VoucherCodeGraphQLField) -> "VoucherCodeFields":
        self._subfields.extend(subfields)
        return self


class VoucherCodeCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "VoucherCodeCountableEdgeFields":
        return VoucherCodeCountableEdgeFields("edges")

    total_count: VoucherCodeCountableConnectionGraphQLField = (
        VoucherCodeCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            VoucherCodeCountableConnectionGraphQLField,
            "VoucherCodeCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "VoucherCodeCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class MenuItemUpdateFields(GraphQLField):
    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    @classmethod
    def menu_item(cls) -> "MenuItemFields":
        return MenuItemFields("menu_item")

    def fields(
        self,
        *subfields: Union[
            MenuItemUpdateGraphQLField, "MenuItemFields", "MenuErrorFields"
        ]
    ) -> "MenuItemUpdateFields":
        self._subfields.extend(subfields)
        return self


class ExternalLogoutFields(GraphQLField):
    logout_data: ExternalLogoutGraphQLField = ExternalLogoutGraphQLField("logoutData")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self, *subfields: Union[ExternalLogoutGraphQLField, "AccountErrorFields"]
    ) -> "ExternalLogoutFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueTranslationFields(GraphQLField):
    id: AttributeValueTranslationGraphQLField = AttributeValueTranslationGraphQLField(
        "id"
    )

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: AttributeValueTranslationGraphQLField = AttributeValueTranslationGraphQLField(
        "name"
    )
    rich_text: AttributeValueTranslationGraphQLField = (
        AttributeValueTranslationGraphQLField("richText")
    )
    plain_text: AttributeValueTranslationGraphQLField = (
        AttributeValueTranslationGraphQLField("plainText")
    )

    @classmethod
    def translatable_content(cls) -> "AttributeValueTranslatableContentFields":
        return AttributeValueTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            AttributeValueTranslationGraphQLField,
            "AttributeValueTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "AttributeValueTranslationFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkCreateResultFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def errors(cls) -> "AttributeBulkCreateErrorFields":
        return AttributeBulkCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeBulkCreateResultGraphQLField,
            "AttributeFields",
            "AttributeBulkCreateErrorFields",
        ]
    ) -> "AttributeBulkCreateResultFields":
        self._subfields.extend(subfields)
        return self


class OrderDiscountFields(GraphQLField):
    id: OrderDiscountGraphQLField = OrderDiscountGraphQLField("id")
    type: OrderDiscountGraphQLField = OrderDiscountGraphQLField("type")
    name: OrderDiscountGraphQLField = OrderDiscountGraphQLField("name")
    translated_name: OrderDiscountGraphQLField = OrderDiscountGraphQLField(
        "translatedName"
    )
    value_type: OrderDiscountGraphQLField = OrderDiscountGraphQLField("valueType")
    value: OrderDiscountGraphQLField = OrderDiscountGraphQLField("value")
    reason: OrderDiscountGraphQLField = OrderDiscountGraphQLField("reason")

    @classmethod
    def amount(cls) -> "MoneyFields":
        return MoneyFields("amount")

    def fields(
        self, *subfields: Union[OrderDiscountGraphQLField, "MoneyFields"]
    ) -> "OrderDiscountFields":
        self._subfields.extend(subfields)
        return self


class MenuCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "MenuCountableEdgeFields":
        return MenuCountableEdgeFields("edges")

    total_count: MenuCountableConnectionGraphQLField = (
        MenuCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            MenuCountableConnectionGraphQLField,
            "PageInfoFields",
            "MenuCountableEdgeFields",
        ]
    ) -> "MenuCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLinesAddFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutLinesAddGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutLinesAddFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantRefundCreateFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def granted_refund(cls) -> "OrderGrantedRefundFields":
        return OrderGrantedRefundFields("granted_refund")

    @classmethod
    def errors(cls) -> "OrderGrantRefundCreateErrorFields":
        return OrderGrantRefundCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderGrantRefundCreateGraphQLField,
            "OrderGrantRefundCreateErrorFields",
            "OrderGrantedRefundFields",
            "OrderFields",
        ]
    ) -> "OrderGrantRefundCreateFields":
        self._subfields.extend(subfields)
        return self


class VoucherChannelListingUpdateFields(GraphQLField):
    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            VoucherChannelListingUpdateGraphQLField,
            "VoucherFields",
            "DiscountErrorFields",
        ]
    ) -> "VoucherChannelListingUpdateFields":
        self._subfields.extend(subfields)
        return self


class CategoryCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "CategoryFields":
        return CategoryFields("node")

    cursor: CategoryCountableEdgeGraphQLField = CategoryCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[CategoryCountableEdgeGraphQLField, "CategoryFields"]
    ) -> "CategoryCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class TimePeriodFields(GraphQLField):
    amount: TimePeriodGraphQLField = TimePeriodGraphQLField("amount")
    type: TimePeriodGraphQLField = TimePeriodGraphQLField("type")

    def fields(self, *subfields: TimePeriodGraphQLField) -> "TimePeriodFields":
        self._subfields.extend(subfields)
        return self


class TransactionProcessErrorFields(GraphQLField):
    field: TransactionProcessErrorGraphQLField = TransactionProcessErrorGraphQLField(
        "field"
    )
    message: TransactionProcessErrorGraphQLField = TransactionProcessErrorGraphQLField(
        "message"
    )
    code: TransactionProcessErrorGraphQLField = TransactionProcessErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: TransactionProcessErrorGraphQLField
    ) -> "TransactionProcessErrorFields":
        self._subfields.extend(subfields)
        return self


class OrderCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "OrderCountableEdgeFields":
        return OrderCountableEdgeFields("edges")

    total_count: OrderCountableConnectionGraphQLField = (
        OrderCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            OrderCountableConnectionGraphQLField,
            "OrderCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "OrderCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class OrderNoteUpdateErrorFields(GraphQLField):
    field: OrderNoteUpdateErrorGraphQLField = OrderNoteUpdateErrorGraphQLField("field")
    message: OrderNoteUpdateErrorGraphQLField = OrderNoteUpdateErrorGraphQLField(
        "message"
    )
    code: OrderNoteUpdateErrorGraphQLField = OrderNoteUpdateErrorGraphQLField("code")

    def fields(
        self, *subfields: OrderNoteUpdateErrorGraphQLField
    ) -> "OrderNoteUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLineCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "CheckoutLineFields":
        return CheckoutLineFields("node")

    cursor: CheckoutLineCountableEdgeGraphQLField = (
        CheckoutLineCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[CheckoutLineCountableEdgeGraphQLField, "CheckoutLineFields"]
    ) -> "CheckoutLineCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ExportProductsFields(GraphQLField):
    @classmethod
    def export_file(cls) -> "ExportFileFields":
        return ExportFileFields("export_file")

    @classmethod
    def export_errors(cls) -> "ExportErrorFields":
        return ExportErrorFields("export_errors")

    @classmethod
    def errors(cls) -> "ExportErrorFields":
        return ExportErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExportProductsGraphQLField, "ExportFileFields", "ExportErrorFields"
        ]
    ) -> "ExportProductsFields":
        self._subfields.extend(subfields)
        return self


class ExportFileCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ExportFileFields":
        return ExportFileFields("node")

    cursor: ExportFileCountableEdgeGraphQLField = ExportFileCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[ExportFileCountableEdgeGraphQLField, "ExportFileFields"]
    ) -> "ExportFileCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class AddressValidationDataFields(GraphQLField):
    country_code: AddressValidationDataGraphQLField = AddressValidationDataGraphQLField(
        "countryCode"
    )
    country_name: AddressValidationDataGraphQLField = AddressValidationDataGraphQLField(
        "countryName"
    )
    address_format: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("addressFormat")
    )
    address_latin_format: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("addressLatinFormat")
    )
    allowed_fields: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("allowedFields")
    )
    required_fields: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("requiredFields")
    )
    upper_fields: AddressValidationDataGraphQLField = AddressValidationDataGraphQLField(
        "upperFields"
    )
    country_area_type: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("countryAreaType")
    )

    @classmethod
    def country_area_choices(cls) -> "ChoiceValueFields":
        return ChoiceValueFields("country_area_choices")

    city_type: AddressValidationDataGraphQLField = AddressValidationDataGraphQLField(
        "cityType"
    )

    @classmethod
    def city_choices(cls) -> "ChoiceValueFields":
        return ChoiceValueFields("city_choices")

    city_area_type: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("cityAreaType")
    )

    @classmethod
    def city_area_choices(cls) -> "ChoiceValueFields":
        return ChoiceValueFields("city_area_choices")

    postal_code_type: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("postalCodeType")
    )
    postal_code_matchers: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("postalCodeMatchers")
    )
    postal_code_examples: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("postalCodeExamples")
    )
    postal_code_prefix: AddressValidationDataGraphQLField = (
        AddressValidationDataGraphQLField("postalCodePrefix")
    )

    def fields(
        self, *subfields: Union[AddressValidationDataGraphQLField, "ChoiceValueFields"]
    ) -> "AddressValidationDataFields":
        self._subfields.extend(subfields)
        return self


class PaymentFields(GraphQLField):
    id: PaymentGraphQLField = PaymentGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: PaymentGraphQLField = PaymentGraphQLField("privateMetafield")
    private_metafields: PaymentGraphQLField = PaymentGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: PaymentGraphQLField = PaymentGraphQLField("metafield")
    metafields: PaymentGraphQLField = PaymentGraphQLField("metafields")
    gateway: PaymentGraphQLField = PaymentGraphQLField("gateway")
    is_active: PaymentGraphQLField = PaymentGraphQLField("isActive")
    created: PaymentGraphQLField = PaymentGraphQLField("created")
    modified: PaymentGraphQLField = PaymentGraphQLField("modified")
    token: PaymentGraphQLField = PaymentGraphQLField("token")

    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    payment_method_type: PaymentGraphQLField = PaymentGraphQLField("paymentMethodType")
    customer_ip_address: PaymentGraphQLField = PaymentGraphQLField("customerIpAddress")
    charge_status: PaymentGraphQLField = PaymentGraphQLField("chargeStatus")
    actions: PaymentGraphQLField = PaymentGraphQLField("actions")

    @classmethod
    def total(cls) -> "MoneyFields":
        return MoneyFields("total")

    @classmethod
    def captured_amount(cls) -> "MoneyFields":
        return MoneyFields("captured_amount")

    @classmethod
    def transactions(cls) -> "TransactionFields":
        return TransactionFields("transactions")

    @classmethod
    def available_capture_amount(cls) -> "MoneyFields":
        return MoneyFields("available_capture_amount")

    @classmethod
    def available_refund_amount(cls) -> "MoneyFields":
        return MoneyFields("available_refund_amount")

    @classmethod
    def credit_card(cls) -> "CreditCardFields":
        return CreditCardFields("credit_card")

    partial: PaymentGraphQLField = PaymentGraphQLField("partial")
    psp_reference: PaymentGraphQLField = PaymentGraphQLField("pspReference")

    def fields(
        self,
        *subfields: Union[
            PaymentGraphQLField,
            "OrderFields",
            "CheckoutFields",
            "MetadataItemFields",
            "CreditCardFields",
            "TransactionFields",
            "MoneyFields",
        ]
    ) -> "PaymentFields":
        self._subfields.extend(subfields)
        return self


class CollectionTranslationFields(GraphQLField):
    id: CollectionTranslationGraphQLField = CollectionTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    seo_title: CollectionTranslationGraphQLField = CollectionTranslationGraphQLField(
        "seoTitle"
    )
    seo_description: CollectionTranslationGraphQLField = (
        CollectionTranslationGraphQLField("seoDescription")
    )
    name: CollectionTranslationGraphQLField = CollectionTranslationGraphQLField("name")
    description: CollectionTranslationGraphQLField = CollectionTranslationGraphQLField(
        "description"
    )
    description_json: CollectionTranslationGraphQLField = (
        CollectionTranslationGraphQLField("descriptionJson")
    )

    @classmethod
    def translatable_content(cls) -> "CollectionTranslatableContentFields":
        return CollectionTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            CollectionTranslationGraphQLField,
            "CollectionTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "CollectionTranslationFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkTranslateErrorFields(GraphQLField):
    path: AttributeBulkTranslateErrorGraphQLField = (
        AttributeBulkTranslateErrorGraphQLField("path")
    )
    message: AttributeBulkTranslateErrorGraphQLField = (
        AttributeBulkTranslateErrorGraphQLField("message")
    )
    code: AttributeBulkTranslateErrorGraphQLField = (
        AttributeBulkTranslateErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: AttributeBulkTranslateErrorGraphQLField
    ) -> "AttributeBulkTranslateErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeCreateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    def fields(
        self,
        *subfields: Union[
            ProductTypeCreateGraphQLField, "ProductTypeFields", "ProductErrorFields"
        ]
    ) -> "ProductTypeCreateFields":
        self._subfields.extend(subfields)
        return self


class SaleRemoveCataloguesFields(GraphQLField):
    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            SaleRemoveCataloguesGraphQLField, "SaleFields", "DiscountErrorFields"
        ]
    ) -> "SaleRemoveCataloguesFields":
        self._subfields.extend(subfields)
        return self


class PageTranslatableContentFields(GraphQLField):
    id: PageTranslatableContentGraphQLField = PageTranslatableContentGraphQLField("id")
    page_id: PageTranslatableContentGraphQLField = PageTranslatableContentGraphQLField(
        "pageId"
    )
    seo_title: PageTranslatableContentGraphQLField = (
        PageTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: PageTranslatableContentGraphQLField = (
        PageTranslatableContentGraphQLField("seoDescription")
    )
    title: PageTranslatableContentGraphQLField = PageTranslatableContentGraphQLField(
        "title"
    )
    content: PageTranslatableContentGraphQLField = PageTranslatableContentGraphQLField(
        "content"
    )
    content_json: PageTranslatableContentGraphQLField = (
        PageTranslatableContentGraphQLField("contentJson")
    )

    @classmethod
    def translation(cls) -> "PageTranslationFields":
        return PageTranslationFields("translation")

    @classmethod
    def page(cls) -> "PageFields":
        return PageFields("page")

    @classmethod
    def attribute_values(cls) -> "AttributeValueTranslatableContentFields":
        return AttributeValueTranslatableContentFields("attribute_values")

    def fields(
        self,
        *subfields: Union[
            PageTranslatableContentGraphQLField,
            "AttributeValueTranslatableContentFields",
            "PageFields",
            "PageTranslationFields",
        ]
    ) -> "PageTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class AccountRequestDeletionFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[AccountRequestDeletionGraphQLField, "AccountErrorFields"]
    ) -> "AccountRequestDeletionFields":
        self._subfields.extend(subfields)
        return self


class AddressCreateFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    def fields(
        self,
        *subfields: Union[
            AddressCreateGraphQLField,
            "AccountErrorFields",
            "UserFields",
            "AddressFields",
        ]
    ) -> "AddressCreateFields":
        self._subfields.extend(subfields)
        return self


class MetadataErrorFields(GraphQLField):
    field: MetadataErrorGraphQLField = MetadataErrorGraphQLField("field")
    message: MetadataErrorGraphQLField = MetadataErrorGraphQLField("message")
    code: MetadataErrorGraphQLField = MetadataErrorGraphQLField("code")

    def fields(self, *subfields: MetadataErrorGraphQLField) -> "MetadataErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkResultFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def errors(cls) -> "ProductBulkCreateErrorFields":
        return ProductBulkCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductBulkResultGraphQLField,
            "ProductFields",
            "ProductBulkCreateErrorFields",
        ]
    ) -> "ProductBulkResultFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLineProblemVariantNotAvailableFields(GraphQLField):
    @classmethod
    def line(cls) -> "CheckoutLineFields":
        return CheckoutLineFields("line")

    def fields(
        self,
        *subfields: Union[
            CheckoutLineProblemVariantNotAvailableGraphQLField, "CheckoutLineFields"
        ]
    ) -> "CheckoutLineProblemVariantNotAvailableFields":
        self._subfields.extend(subfields)
        return self


class OrderCreateFromCheckoutErrorFields(GraphQLField):
    field: OrderCreateFromCheckoutErrorGraphQLField = (
        OrderCreateFromCheckoutErrorGraphQLField("field")
    )
    message: OrderCreateFromCheckoutErrorGraphQLField = (
        OrderCreateFromCheckoutErrorGraphQLField("message")
    )
    code: OrderCreateFromCheckoutErrorGraphQLField = (
        OrderCreateFromCheckoutErrorGraphQLField("code")
    )
    variants: OrderCreateFromCheckoutErrorGraphQLField = (
        OrderCreateFromCheckoutErrorGraphQLField("variants")
    )
    lines: OrderCreateFromCheckoutErrorGraphQLField = (
        OrderCreateFromCheckoutErrorGraphQLField("lines")
    )

    def fields(
        self, *subfields: OrderCreateFromCheckoutErrorGraphQLField
    ) -> "OrderCreateFromCheckoutErrorFields":
        self._subfields.extend(subfields)
        return self


class StaffNotificationRecipientUpdateFields(GraphQLField):
    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    @classmethod
    def staff_notification_recipient(cls) -> "StaffNotificationRecipientFields":
        return StaffNotificationRecipientFields("staff_notification_recipient")

    def fields(
        self,
        *subfields: Union[
            StaffNotificationRecipientUpdateGraphQLField,
            "StaffNotificationRecipientFields",
            "ShopErrorFields",
        ]
    ) -> "StaffNotificationRecipientUpdateFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkUpdateErrorFields(GraphQLField):
    path: AttributeBulkUpdateErrorGraphQLField = AttributeBulkUpdateErrorGraphQLField(
        "path"
    )
    message: AttributeBulkUpdateErrorGraphQLField = (
        AttributeBulkUpdateErrorGraphQLField("message")
    )
    code: AttributeBulkUpdateErrorGraphQLField = AttributeBulkUpdateErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: AttributeBulkUpdateErrorGraphQLField
    ) -> "AttributeBulkUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "CheckoutCountableEdgeFields":
        return CheckoutCountableEdgeFields("edges")

    total_count: CheckoutCountableConnectionGraphQLField = (
        CheckoutCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            CheckoutCountableConnectionGraphQLField,
            "CheckoutCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "CheckoutCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantUpdateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    def fields(
        self,
        *subfields: Union[
            ProductVariantUpdateGraphQLField,
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "ProductVariantUpdateFields":
        self._subfields.extend(subfields)
        return self


class ShopSettingsTranslateFields(GraphQLField):
    @classmethod
    def shop(cls) -> "ShopFields":
        return ShopFields("shop")

    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShopSettingsTranslateGraphQLField, "TranslationErrorFields", "ShopFields"
        ]
    ) -> "ShopSettingsTranslateFields":
        self._subfields.extend(subfields)
        return self


class PluginConfigurationFields(GraphQLField):
    active: PluginConfigurationGraphQLField = PluginConfigurationGraphQLField("active")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def configuration(cls) -> "ConfigurationItemFields":
        return ConfigurationItemFields("configuration")

    def fields(
        self,
        *subfields: Union[
            PluginConfigurationGraphQLField, "ChannelFields", "ConfigurationItemFields"
        ]
    ) -> "PluginConfigurationFields":
        self._subfields.extend(subfields)
        return self


class TransactionEventReportErrorFields(GraphQLField):
    field: TransactionEventReportErrorGraphQLField = (
        TransactionEventReportErrorGraphQLField("field")
    )
    message: TransactionEventReportErrorGraphQLField = (
        TransactionEventReportErrorGraphQLField("message")
    )
    code: TransactionEventReportErrorGraphQLField = (
        TransactionEventReportErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: TransactionEventReportErrorGraphQLField
    ) -> "TransactionEventReportErrorFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueTranslatableContentFields(GraphQLField):
    id: AttributeValueTranslatableContentGraphQLField = (
        AttributeValueTranslatableContentGraphQLField("id")
    )
    attribute_value_id: AttributeValueTranslatableContentGraphQLField = (
        AttributeValueTranslatableContentGraphQLField("attributeValueId")
    )
    name: AttributeValueTranslatableContentGraphQLField = (
        AttributeValueTranslatableContentGraphQLField("name")
    )
    rich_text: AttributeValueTranslatableContentGraphQLField = (
        AttributeValueTranslatableContentGraphQLField("richText")
    )
    plain_text: AttributeValueTranslatableContentGraphQLField = (
        AttributeValueTranslatableContentGraphQLField("plainText")
    )

    @classmethod
    def translation(cls) -> "AttributeValueTranslationFields":
        return AttributeValueTranslationFields("translation")

    @classmethod
    def attribute_value(cls) -> "AttributeValueFields":
        return AttributeValueFields("attribute_value")

    @classmethod
    def attribute(cls) -> "AttributeTranslatableContentFields":
        return AttributeTranslatableContentFields("attribute")

    def fields(
        self,
        *subfields: Union[
            AttributeValueTranslatableContentGraphQLField,
            "AttributeValueFields",
            "AttributeTranslatableContentFields",
            "AttributeValueTranslationFields",
        ]
    ) -> "AttributeValueTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueBulkTranslateResultFields(GraphQLField):
    @classmethod
    def translation(cls) -> "AttributeValueTranslationFields":
        return AttributeValueTranslationFields("translation")

    @classmethod
    def errors(cls) -> "AttributeValueBulkTranslateErrorFields":
        return AttributeValueBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeValueBulkTranslateResultGraphQLField,
            "AttributeValueTranslationFields",
            "AttributeValueBulkTranslateErrorFields",
        ]
    ) -> "AttributeValueBulkTranslateResultFields":
        self._subfields.extend(subfields)
        return self


class SaleTranslationFields(GraphQLField):
    id: SaleTranslationGraphQLField = SaleTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: SaleTranslationGraphQLField = SaleTranslationGraphQLField("name")

    @classmethod
    def translatable_content(cls) -> "SaleTranslatableContentFields":
        return SaleTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            SaleTranslationGraphQLField,
            "SaleTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "SaleTranslationFields":
        self._subfields.extend(subfields)
        return self


class ShopFields(GraphQLField):
    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ShopGraphQLField = ShopGraphQLField("privateMetafield")
    private_metafields: ShopGraphQLField = ShopGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ShopGraphQLField = ShopGraphQLField("metafield")
    metafields: ShopGraphQLField = ShopGraphQLField("metafields")
    id: ShopGraphQLField = ShopGraphQLField("id")

    @classmethod
    def available_payment_gateways(cls) -> "PaymentGatewayFields":
        return PaymentGatewayFields("available_payment_gateways")

    @classmethod
    def available_external_authentications(cls) -> "ExternalAuthenticationFields":
        return ExternalAuthenticationFields("available_external_authentications")

    @classmethod
    def available_shipping_methods(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("available_shipping_methods")

    channel_currencies: ShopGraphQLField = ShopGraphQLField("channelCurrencies")

    @classmethod
    def countries(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("countries")

    @classmethod
    def default_country(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("default_country")

    default_mail_sender_name: ShopGraphQLField = ShopGraphQLField(
        "defaultMailSenderName"
    )
    default_mail_sender_address: ShopGraphQLField = ShopGraphQLField(
        "defaultMailSenderAddress"
    )
    description: ShopGraphQLField = ShopGraphQLField("description")

    @classmethod
    def domain(cls) -> "DomainFields":
        return DomainFields("domain")

    @classmethod
    def languages(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("languages")

    name: ShopGraphQLField = ShopGraphQLField("name")

    @classmethod
    def permissions(cls) -> "PermissionFields":
        return PermissionFields("permissions")

    phone_prefixes: ShopGraphQLField = ShopGraphQLField("phonePrefixes")
    header_text: ShopGraphQLField = ShopGraphQLField("headerText")
    fulfillment_auto_approve: ShopGraphQLField = ShopGraphQLField(
        "fulfillmentAutoApprove"
    )
    fulfillment_allow_unpaid: ShopGraphQLField = ShopGraphQLField(
        "fulfillmentAllowUnpaid"
    )
    track_inventory_by_default: ShopGraphQLField = ShopGraphQLField(
        "trackInventoryByDefault"
    )
    default_weight_unit: ShopGraphQLField = ShopGraphQLField("defaultWeightUnit")

    @classmethod
    def translation(cls) -> "ShopTranslationFields":
        return ShopTranslationFields("translation")

    automatic_fulfillment_digital_products: ShopGraphQLField = ShopGraphQLField(
        "automaticFulfillmentDigitalProducts"
    )
    reserve_stock_duration_anonymous_user: ShopGraphQLField = ShopGraphQLField(
        "reserveStockDurationAnonymousUser"
    )
    reserve_stock_duration_authenticated_user: ShopGraphQLField = ShopGraphQLField(
        "reserveStockDurationAuthenticatedUser"
    )
    limit_quantity_per_checkout: ShopGraphQLField = ShopGraphQLField(
        "limitQuantityPerCheckout"
    )
    default_digital_max_downloads: ShopGraphQLField = ShopGraphQLField(
        "defaultDigitalMaxDownloads"
    )
    default_digital_url_valid_days: ShopGraphQLField = ShopGraphQLField(
        "defaultDigitalUrlValidDays"
    )

    @classmethod
    def company_address(cls) -> "AddressFields":
        return AddressFields("company_address")

    customer_set_password_url: ShopGraphQLField = ShopGraphQLField(
        "customerSetPasswordUrl"
    )

    @classmethod
    def staff_notification_recipients(cls) -> "StaffNotificationRecipientFields":
        return StaffNotificationRecipientFields("staff_notification_recipients")

    enable_account_confirmation_by_email: ShopGraphQLField = ShopGraphQLField(
        "enableAccountConfirmationByEmail"
    )
    allow_login_without_confirmation: ShopGraphQLField = ShopGraphQLField(
        "allowLoginWithoutConfirmation"
    )

    @classmethod
    def limits(cls) -> "LimitInfoFields":
        return LimitInfoFields("limits")

    version: ShopGraphQLField = ShopGraphQLField("version")
    schema_version: ShopGraphQLField = ShopGraphQLField("schemaVersion")

    @classmethod
    def available_tax_apps(cls) -> "AppFields":
        return AppFields("available_tax_apps")

    include_taxes_in_prices: ShopGraphQLField = ShopGraphQLField("includeTaxesInPrices")
    display_gross_prices: ShopGraphQLField = ShopGraphQLField("displayGrossPrices")
    charge_taxes_on_shipping: ShopGraphQLField = ShopGraphQLField(
        "chargeTaxesOnShipping"
    )

    def fields(
        self,
        *subfields: Union[
            ShopGraphQLField,
            "DomainFields",
            "LanguageDisplayFields",
            "MetadataItemFields",
            "AppFields",
            "PermissionFields",
            "ShippingMethodFields",
            "ShopTranslationFields",
            "StaffNotificationRecipientFields",
            "PaymentGatewayFields",
            "CountryDisplayFields",
            "ExternalAuthenticationFields",
            "AddressFields",
            "LimitInfoFields",
        ]
    ) -> "ShopFields":
        self._subfields.extend(subfields)
        return self


class AddressFields(GraphQLField):
    id: AddressGraphQLField = AddressGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: AddressGraphQLField = AddressGraphQLField("privateMetafield")
    private_metafields: AddressGraphQLField = AddressGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: AddressGraphQLField = AddressGraphQLField("metafield")
    metafields: AddressGraphQLField = AddressGraphQLField("metafields")
    first_name: AddressGraphQLField = AddressGraphQLField("firstName")
    last_name: AddressGraphQLField = AddressGraphQLField("lastName")
    company_name: AddressGraphQLField = AddressGraphQLField("companyName")
    street_address_1: AddressGraphQLField = AddressGraphQLField("streetAddress1")
    street_address_2: AddressGraphQLField = AddressGraphQLField("streetAddress2")
    city: AddressGraphQLField = AddressGraphQLField("city")
    city_area: AddressGraphQLField = AddressGraphQLField("cityArea")
    postal_code: AddressGraphQLField = AddressGraphQLField("postalCode")

    @classmethod
    def country(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("country")

    country_area: AddressGraphQLField = AddressGraphQLField("countryArea")
    phone: AddressGraphQLField = AddressGraphQLField("phone")
    is_default_shipping_address: AddressGraphQLField = AddressGraphQLField(
        "isDefaultShippingAddress"
    )
    is_default_billing_address: AddressGraphQLField = AddressGraphQLField(
        "isDefaultBillingAddress"
    )

    def fields(
        self,
        *subfields: Union[
            AddressGraphQLField, "MetadataItemFields", "CountryDisplayFields"
        ]
    ) -> "AddressFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryAttemptCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "EventDeliveryAttemptCountableEdgeFields":
        return EventDeliveryAttemptCountableEdgeFields("edges")

    total_count: EventDeliveryAttemptCountableConnectionGraphQLField = (
        EventDeliveryAttemptCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            EventDeliveryAttemptCountableConnectionGraphQLField,
            "EventDeliveryAttemptCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "EventDeliveryAttemptCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class ReducedRateFields(GraphQLField):
    rate: ReducedRateGraphQLField = ReducedRateGraphQLField("rate")
    rate_type: ReducedRateGraphQLField = ReducedRateGraphQLField("rateType")

    def fields(self, *subfields: ReducedRateGraphQLField) -> "ReducedRateFields":
        self._subfields.extend(subfields)
        return self


class MoneyRangeFields(GraphQLField):
    @classmethod
    def start(cls) -> "MoneyFields":
        return MoneyFields("start")

    @classmethod
    def stop(cls) -> "MoneyFields":
        return MoneyFields("stop")

    def fields(
        self, *subfields: Union[MoneyRangeGraphQLField, "MoneyFields"]
    ) -> "MoneyRangeFields":
        self._subfields.extend(subfields)
        return self


class WarehouseCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "WarehouseFields":
        return WarehouseFields("node")

    cursor: WarehouseCountableEdgeGraphQLField = WarehouseCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[WarehouseCountableEdgeGraphQLField, "WarehouseFields"]
    ) -> "WarehouseCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class MenuUpdateFields(GraphQLField):
    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    @classmethod
    def menu(cls) -> "MenuFields":
        return MenuFields("menu")

    def fields(
        self, *subfields: Union[MenuUpdateGraphQLField, "MenuFields", "MenuErrorFields"]
    ) -> "MenuUpdateFields":
        self._subfields.extend(subfields)
        return self


class ChannelActivateFields(GraphQLField):
    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def channel_errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("channel_errors")

    @classmethod
    def errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ChannelActivateGraphQLField, "ChannelFields", "ChannelErrorFields"
        ]
    ) -> "ChannelActivateFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLineProblemInsufficientStockFields(GraphQLField):
    available_quantity: CheckoutLineProblemInsufficientStockGraphQLField = (
        CheckoutLineProblemInsufficientStockGraphQLField("availableQuantity")
    )

    @classmethod
    def line(cls) -> "CheckoutLineFields":
        return CheckoutLineFields("line")

    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    def fields(
        self,
        *subfields: Union[
            CheckoutLineProblemInsufficientStockGraphQLField,
            "CheckoutLineFields",
            "ProductVariantFields",
        ]
    ) -> "CheckoutLineProblemInsufficientStockFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentUpdateTrackingFields(GraphQLField):
    @classmethod
    def fulfillment(cls) -> "FulfillmentFields":
        return FulfillmentFields("fulfillment")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            FulfillmentUpdateTrackingGraphQLField,
            "FulfillmentFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "FulfillmentUpdateTrackingFields":
        self._subfields.extend(subfields)
        return self


class GroupCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "GroupFields":
        return GroupFields("node")

    cursor: GroupCountableEdgeGraphQLField = GroupCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[GroupCountableEdgeGraphQLField, "GroupFields"]
    ) -> "GroupCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class MenuItemCreateFields(GraphQLField):
    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    @classmethod
    def menu_item(cls) -> "MenuItemFields":
        return MenuItemFields("menu_item")

    def fields(
        self,
        *subfields: Union[
            MenuItemCreateGraphQLField, "MenuItemFields", "MenuErrorFields"
        ]
    ) -> "MenuItemCreateFields":
        self._subfields.extend(subfields)
        return self


class UpdatePrivateMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadata_errors")

    @classmethod
    def errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("errors")

    item: ObjectWithMetadataInterface = ObjectWithMetadataInterface("item")

    def fields(
        self,
        *subfields: Union[
            UpdatePrivateMetadataGraphQLField,
            "MetadataErrorFields",
            "ObjectWithMetadataInterface",
        ]
    ) -> "UpdatePrivateMetadataFields":
        self._subfields.extend(subfields)
        return self


class AppDeleteFailedInstallationFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app_installation(cls) -> "AppInstallationFields":
        return AppInstallationFields("app_installation")

    def fields(
        self,
        *subfields: Union[
            AppDeleteFailedInstallationGraphQLField,
            "AppErrorFields",
            "AppInstallationFields",
        ]
    ) -> "AppDeleteFailedInstallationFields":
        self._subfields.extend(subfields)
        return self


class SelectedAttributeFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def values(cls) -> "AttributeValueFields":
        return AttributeValueFields("values")

    def fields(
        self,
        *subfields: Union[
            SelectedAttributeGraphQLField, "AttributeFields", "AttributeValueFields"
        ]
    ) -> "SelectedAttributeFields":
        self._subfields.extend(subfields)
        return self


class GiftCardEventBalanceFields(GraphQLField):
    @classmethod
    def initial_balance(cls) -> "MoneyFields":
        return MoneyFields("initial_balance")

    @classmethod
    def current_balance(cls) -> "MoneyFields":
        return MoneyFields("current_balance")

    @classmethod
    def old_initial_balance(cls) -> "MoneyFields":
        return MoneyFields("old_initial_balance")

    @classmethod
    def old_current_balance(cls) -> "MoneyFields":
        return MoneyFields("old_current_balance")

    def fields(
        self, *subfields: Union[GiftCardEventBalanceGraphQLField, "MoneyFields"]
    ) -> "GiftCardEventBalanceFields":
        self._subfields.extend(subfields)
        return self


class SendConfirmationEmailFields(GraphQLField):
    @classmethod
    def errors(cls) -> "SendConfirmationEmailErrorFields":
        return SendConfirmationEmailErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            SendConfirmationEmailGraphQLField, "SendConfirmationEmailErrorFields"
        ]
    ) -> "SendConfirmationEmailFields":
        self._subfields.extend(subfields)
        return self


class MenuCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "MenuFields":
        return MenuFields("node")

    cursor: MenuCountableEdgeGraphQLField = MenuCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[MenuCountableEdgeGraphQLField, "MenuFields"]
    ) -> "MenuCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceUpdateFields(GraphQLField):
    @classmethod
    def shipping_zone(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("shipping_zone")

    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShippingPriceUpdateGraphQLField,
            "ShippingZoneFields",
            "ShippingMethodTypeFields",
            "ShippingErrorFields",
        ]
    ) -> "ShippingPriceUpdateFields":
        self._subfields.extend(subfields)
        return self


class TaxClassCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "TaxClassCountableEdgeFields":
        return TaxClassCountableEdgeFields("edges")

    total_count: TaxClassCountableConnectionGraphQLField = (
        TaxClassCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            TaxClassCountableConnectionGraphQLField,
            "PageInfoFields",
            "TaxClassCountableEdgeFields",
        ]
    ) -> "TaxClassCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PromotionBulkDeleteFields(GraphQLField):
    count: PromotionBulkDeleteGraphQLField = PromotionBulkDeleteGraphQLField("count")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self, *subfields: Union[PromotionBulkDeleteGraphQLField, "DiscountErrorFields"]
    ) -> "PromotionBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueFields(GraphQLField):
    id: AttributeValueGraphQLField = AttributeValueGraphQLField("id")
    name: AttributeValueGraphQLField = AttributeValueGraphQLField("name")
    slug: AttributeValueGraphQLField = AttributeValueGraphQLField("slug")
    value: AttributeValueGraphQLField = AttributeValueGraphQLField("value")

    @classmethod
    def translation(cls) -> "AttributeValueTranslationFields":
        return AttributeValueTranslationFields("translation")

    input_type: AttributeValueGraphQLField = AttributeValueGraphQLField("inputType")
    reference: AttributeValueGraphQLField = AttributeValueGraphQLField("reference")

    @classmethod
    def file(cls) -> "FileFields":
        return FileFields("file")

    rich_text: AttributeValueGraphQLField = AttributeValueGraphQLField("richText")
    plain_text: AttributeValueGraphQLField = AttributeValueGraphQLField("plainText")
    boolean: AttributeValueGraphQLField = AttributeValueGraphQLField("boolean")
    date: AttributeValueGraphQLField = AttributeValueGraphQLField("date")
    date_time: AttributeValueGraphQLField = AttributeValueGraphQLField("dateTime")
    external_reference: AttributeValueGraphQLField = AttributeValueGraphQLField(
        "externalReference"
    )

    def fields(
        self,
        *subfields: Union[
            AttributeValueGraphQLField, "FileFields", "AttributeValueTranslationFields"
        ]
    ) -> "AttributeValueFields":
        self._subfields.extend(subfields)
        return self


class MenuItemTranslationFields(GraphQLField):
    id: MenuItemTranslationGraphQLField = MenuItemTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: MenuItemTranslationGraphQLField = MenuItemTranslationGraphQLField("name")

    @classmethod
    def translatable_content(cls) -> "MenuItemTranslatableContentFields":
        return MenuItemTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            MenuItemTranslationGraphQLField,
            "MenuItemTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "MenuItemTranslationFields":
        self._subfields.extend(subfields)
        return self


class ProductMediaUpdateFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductMediaUpdateGraphQLField,
            "ProductFields",
            "ProductErrorFields",
            "ProductMediaFields",
        ]
    ) -> "ProductMediaUpdateFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentUrlFields(GraphQLField):
    id: DigitalContentUrlGraphQLField = DigitalContentUrlGraphQLField("id")

    @classmethod
    def content(cls) -> "DigitalContentFields":
        return DigitalContentFields("content")

    created: DigitalContentUrlGraphQLField = DigitalContentUrlGraphQLField("created")
    download_num: DigitalContentUrlGraphQLField = DigitalContentUrlGraphQLField(
        "downloadNum"
    )
    url: DigitalContentUrlGraphQLField = DigitalContentUrlGraphQLField("url")
    token: DigitalContentUrlGraphQLField = DigitalContentUrlGraphQLField("token")

    def fields(
        self, *subfields: Union[DigitalContentUrlGraphQLField, "DigitalContentFields"]
    ) -> "DigitalContentUrlFields":
        self._subfields.extend(subfields)
        return self


class MenuItemDeleteFields(GraphQLField):
    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    @classmethod
    def menu_item(cls) -> "MenuItemFields":
        return MenuItemFields("menu_item")

    def fields(
        self,
        *subfields: Union[
            MenuItemDeleteGraphQLField, "MenuItemFields", "MenuErrorFields"
        ]
    ) -> "MenuItemDeleteFields":
        self._subfields.extend(subfields)
        return self


class OrderCreateFromCheckoutFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def errors(cls) -> "OrderCreateFromCheckoutErrorFields":
        return OrderCreateFromCheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderCreateFromCheckoutGraphQLField,
            "OrderCreateFromCheckoutErrorFields",
            "OrderFields",
        ]
    ) -> "OrderCreateFromCheckoutFields":
        self._subfields.extend(subfields)
        return self


class TaxConfigurationCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "TaxConfigurationFields":
        return TaxConfigurationFields("node")

    cursor: TaxConfigurationCountableEdgeGraphQLField = (
        TaxConfigurationCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[
            TaxConfigurationCountableEdgeGraphQLField, "TaxConfigurationFields"
        ]
    ) -> "TaxConfigurationCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class WarehouseCreateFields(GraphQLField):
    @classmethod
    def warehouse_errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("warehouse_errors")

    @classmethod
    def errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("errors")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    def fields(
        self,
        *subfields: Union[
            WarehouseCreateGraphQLField, "WarehouseFields", "WarehouseErrorFields"
        ]
    ) -> "WarehouseCreateFields":
        self._subfields.extend(subfields)
        return self


class ExternalAuthenticationUrlFields(GraphQLField):
    authentication_data: ExternalAuthenticationUrlGraphQLField = (
        ExternalAuthenticationUrlGraphQLField("authenticationData")
    )

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[ExternalAuthenticationUrlGraphQLField, "AccountErrorFields"]
    ) -> "ExternalAuthenticationUrlFields":
        self._subfields.extend(subfields)
        return self


class TranslatableItemConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "TranslatableItemEdgeFields":
        return TranslatableItemEdgeFields("edges")

    total_count: TranslatableItemConnectionGraphQLField = (
        TranslatableItemConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            TranslatableItemConnectionGraphQLField,
            "PageInfoFields",
            "TranslatableItemEdgeFields",
        ]
    ) -> "TranslatableItemConnectionFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueBulkTranslateErrorFields(GraphQLField):
    path: AttributeValueBulkTranslateErrorGraphQLField = (
        AttributeValueBulkTranslateErrorGraphQLField("path")
    )
    message: AttributeValueBulkTranslateErrorGraphQLField = (
        AttributeValueBulkTranslateErrorGraphQLField("message")
    )
    code: AttributeValueBulkTranslateErrorGraphQLField = (
        AttributeValueBulkTranslateErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: AttributeValueBulkTranslateErrorGraphQLField
    ) -> "AttributeValueBulkTranslateErrorFields":
        self._subfields.extend(subfields)
        return self


class TransactionRequestRefundForGrantedRefundErrorFields(GraphQLField):
    field: TransactionRequestRefundForGrantedRefundErrorGraphQLField = (
        TransactionRequestRefundForGrantedRefundErrorGraphQLField("field")
    )
    message: TransactionRequestRefundForGrantedRefundErrorGraphQLField = (
        TransactionRequestRefundForGrantedRefundErrorGraphQLField("message")
    )
    code: TransactionRequestRefundForGrantedRefundErrorGraphQLField = (
        TransactionRequestRefundForGrantedRefundErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: TransactionRequestRefundForGrantedRefundErrorGraphQLField
    ) -> "TransactionRequestRefundForGrantedRefundErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkErrorFields(GraphQLField):
    field: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "field"
    )
    message: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "message"
    )
    code: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "code"
    )
    path: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "path"
    )
    attributes: ProductVariantBulkErrorGraphQLField = (
        ProductVariantBulkErrorGraphQLField("attributes")
    )
    values: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "values"
    )
    warehouses: ProductVariantBulkErrorGraphQLField = (
        ProductVariantBulkErrorGraphQLField("warehouses")
    )
    stocks: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "stocks"
    )
    channels: ProductVariantBulkErrorGraphQLField = ProductVariantBulkErrorGraphQLField(
        "channels"
    )
    channel_listings: ProductVariantBulkErrorGraphQLField = (
        ProductVariantBulkErrorGraphQLField("channelListings")
    )

    def fields(
        self, *subfields: ProductVariantBulkErrorGraphQLField
    ) -> "ProductVariantBulkErrorFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleDeleteErrorFields(GraphQLField):
    field: PromotionRuleDeleteErrorGraphQLField = PromotionRuleDeleteErrorGraphQLField(
        "field"
    )
    message: PromotionRuleDeleteErrorGraphQLField = (
        PromotionRuleDeleteErrorGraphQLField("message")
    )
    code: PromotionRuleDeleteErrorGraphQLField = PromotionRuleDeleteErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: PromotionRuleDeleteErrorGraphQLField
    ) -> "PromotionRuleDeleteErrorFields":
        self._subfields.extend(subfields)
        return self


class TaxConfigurationFields(GraphQLField):
    id: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField(
        "privateMetafield"
    )
    private_metafields: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField("metafield")
    metafields: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField(
        "metafields"
    )

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    charge_taxes: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField(
        "chargeTaxes"
    )
    tax_calculation_strategy: TaxConfigurationGraphQLField = (
        TaxConfigurationGraphQLField("taxCalculationStrategy")
    )
    display_gross_prices: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField(
        "displayGrossPrices"
    )
    prices_entered_with_tax: TaxConfigurationGraphQLField = (
        TaxConfigurationGraphQLField("pricesEnteredWithTax")
    )

    @classmethod
    def countries(cls) -> "TaxConfigurationPerCountryFields":
        return TaxConfigurationPerCountryFields("countries")

    tax_app_id: TaxConfigurationGraphQLField = TaxConfigurationGraphQLField("taxAppId")

    def fields(
        self,
        *subfields: Union[
            TaxConfigurationGraphQLField,
            "MetadataItemFields",
            "TaxConfigurationPerCountryFields",
            "ChannelFields",
        ]
    ) -> "TaxConfigurationFields":
        self._subfields.extend(subfields)
        return self


class TaxConfigurationUpdateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "TaxConfigurationUpdateErrorFields":
        return TaxConfigurationUpdateErrorFields("errors")

    @classmethod
    def tax_configuration(cls) -> "TaxConfigurationFields":
        return TaxConfigurationFields("tax_configuration")

    def fields(
        self,
        *subfields: Union[
            TaxConfigurationUpdateGraphQLField,
            "TaxConfigurationUpdateErrorFields",
            "TaxConfigurationFields",
        ]
    ) -> "TaxConfigurationUpdateFields":
        self._subfields.extend(subfields)
        return self


class CollectionErrorFields(GraphQLField):
    field: CollectionErrorGraphQLField = CollectionErrorGraphQLField("field")
    message: CollectionErrorGraphQLField = CollectionErrorGraphQLField("message")
    products: CollectionErrorGraphQLField = CollectionErrorGraphQLField("products")
    code: CollectionErrorGraphQLField = CollectionErrorGraphQLField("code")

    def fields(
        self, *subfields: CollectionErrorGraphQLField
    ) -> "CollectionErrorFields":
        self._subfields.extend(subfields)
        return self


class AttributeReorderValuesFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeReorderValuesGraphQLField,
            "AttributeFields",
            "AttributeErrorFields",
        ]
    ) -> "AttributeReorderValuesFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCompleteFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    confirmation_needed: CheckoutCompleteGraphQLField = CheckoutCompleteGraphQLField(
        "confirmationNeeded"
    )
    confirmation_data: CheckoutCompleteGraphQLField = CheckoutCompleteGraphQLField(
        "confirmationData"
    )

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutCompleteGraphQLField, "CheckoutErrorFields", "OrderFields"
        ]
    ) -> "CheckoutCompleteFields":
        self._subfields.extend(subfields)
        return self


class VoucherDeleteFields(GraphQLField):
    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    def fields(
        self,
        *subfields: Union[
            VoucherDeleteGraphQLField, "VoucherFields", "DiscountErrorFields"
        ]
    ) -> "VoucherDeleteFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCustomerDetachFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutCustomerDetachGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutCustomerDetachFields":
        self._subfields.extend(subfields)
        return self


class ChannelErrorFields(GraphQLField):
    field: ChannelErrorGraphQLField = ChannelErrorGraphQLField("field")
    message: ChannelErrorGraphQLField = ChannelErrorGraphQLField("message")
    code: ChannelErrorGraphQLField = ChannelErrorGraphQLField("code")
    shipping_zones: ChannelErrorGraphQLField = ChannelErrorGraphQLField("shippingZones")
    warehouses: ChannelErrorGraphQLField = ChannelErrorGraphQLField("warehouses")

    def fields(self, *subfields: ChannelErrorGraphQLField) -> "ChannelErrorFields":
        self._subfields.extend(subfields)
        return self


class ConfirmAccountFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ConfirmAccountGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "ConfirmAccountFields":
        self._subfields.extend(subfields)
        return self


class AppCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "AppCountableEdgeFields":
        return AppCountableEdgeFields("edges")

    total_count: AppCountableConnectionGraphQLField = (
        AppCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            AppCountableConnectionGraphQLField,
            "AppCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "AppCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PageInfoFields(GraphQLField):
    has_next_page: PageInfoGraphQLField = PageInfoGraphQLField("hasNextPage")
    has_previous_page: PageInfoGraphQLField = PageInfoGraphQLField("hasPreviousPage")
    start_cursor: PageInfoGraphQLField = PageInfoGraphQLField("startCursor")
    end_cursor: PageInfoGraphQLField = PageInfoGraphQLField("endCursor")

    def fields(self, *subfields: PageInfoGraphQLField) -> "PageInfoFields":
        self._subfields.extend(subfields)
        return self


class PromotionStartedEventFields(GraphQLField):
    id: PromotionStartedEventGraphQLField = PromotionStartedEventGraphQLField("id")
    date: PromotionStartedEventGraphQLField = PromotionStartedEventGraphQLField("date")
    type: PromotionStartedEventGraphQLField = PromotionStartedEventGraphQLField("type")
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")

    def fields(
        self, *subfields: Union[PromotionStartedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionStartedEventFields":
        self._subfields.extend(subfields)
        return self


class PasswordChangeFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PasswordChangeGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "PasswordChangeFields":
        self._subfields.extend(subfields)
        return self


class ChannelDeleteFields(GraphQLField):
    @classmethod
    def channel_errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("channel_errors")

    @classmethod
    def errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("errors")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    def fields(
        self,
        *subfields: Union[
            ChannelDeleteGraphQLField, "ChannelFields", "ChannelErrorFields"
        ]
    ) -> "ChannelDeleteFields":
        self._subfields.extend(subfields)
        return self


class RefreshTokenFields(GraphQLField):
    token: RefreshTokenGraphQLField = RefreshTokenGraphQLField("token")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[RefreshTokenGraphQLField, "AccountErrorFields", "UserFields"]
    ) -> "RefreshTokenFields":
        self._subfields.extend(subfields)
        return self


class VoucherChannelListingFields(GraphQLField):
    id: VoucherChannelListingGraphQLField = VoucherChannelListingGraphQLField("id")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    discount_value: VoucherChannelListingGraphQLField = (
        VoucherChannelListingGraphQLField("discountValue")
    )
    currency: VoucherChannelListingGraphQLField = VoucherChannelListingGraphQLField(
        "currency"
    )

    @classmethod
    def min_spent(cls) -> "MoneyFields":
        return MoneyFields("min_spent")

    def fields(
        self,
        *subfields: Union[
            VoucherChannelListingGraphQLField, "ChannelFields", "MoneyFields"
        ]
    ) -> "VoucherChannelListingFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantSetDefaultFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantSetDefaultGraphQLField, "ProductFields", "ProductErrorFields"
        ]
    ) -> "ProductVariantSetDefaultFields":
        self._subfields.extend(subfields)
        return self


class AttributeDeleteFields(GraphQLField):
    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    def fields(
        self,
        *subfields: Union[
            AttributeDeleteGraphQLField, "AttributeErrorFields", "AttributeFields"
        ]
    ) -> "AttributeDeleteFields":
        self._subfields.extend(subfields)
        return self


class PaymentCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "PaymentFields":
        return PaymentFields("node")

    cursor: PaymentCountableEdgeGraphQLField = PaymentCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[PaymentCountableEdgeGraphQLField, "PaymentFields"]
    ) -> "PaymentCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class CollectionRemoveProductsFields(GraphQLField):
    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CollectionRemoveProductsGraphQLField,
            "CollectionFields",
            "CollectionErrorFields",
        ]
    ) -> "CollectionRemoveProductsFields":
        self._subfields.extend(subfields)
        return self


class CollectionAddProductsFields(GraphQLField):
    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CollectionAddProductsGraphQLField,
            "CollectionFields",
            "CollectionErrorFields",
        ]
    ) -> "CollectionAddProductsFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkTranslateResultFields(GraphQLField):
    @classmethod
    def translation(cls) -> "ProductVariantTranslationFields":
        return ProductVariantTranslationFields("translation")

    @classmethod
    def errors(cls) -> "ProductVariantBulkTranslateErrorFields":
        return ProductVariantBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantBulkTranslateResultGraphQLField,
            "ProductVariantTranslationFields",
            "ProductVariantBulkTranslateErrorFields",
        ]
    ) -> "ProductVariantBulkTranslateResultFields":
        self._subfields.extend(subfields)
        return self


class TaxClassUpdateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "TaxClassUpdateErrorFields":
        return TaxClassUpdateErrorFields("errors")

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    def fields(
        self,
        *subfields: Union[
            TaxClassUpdateGraphQLField, "TaxClassUpdateErrorFields", "TaxClassFields"
        ]
    ) -> "TaxClassUpdateFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLineFields(GraphQLField):
    id: CheckoutLineGraphQLField = CheckoutLineGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: CheckoutLineGraphQLField = CheckoutLineGraphQLField(
        "privateMetafield"
    )
    private_metafields: CheckoutLineGraphQLField = CheckoutLineGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: CheckoutLineGraphQLField = CheckoutLineGraphQLField("metafield")
    metafields: CheckoutLineGraphQLField = CheckoutLineGraphQLField("metafields")

    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    quantity: CheckoutLineGraphQLField = CheckoutLineGraphQLField("quantity")

    @classmethod
    def unit_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("unit_price")

    @classmethod
    def undiscounted_unit_price(cls) -> "MoneyFields":
        return MoneyFields("undiscounted_unit_price")

    @classmethod
    def total_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("total_price")

    @classmethod
    def undiscounted_total_price(cls) -> "MoneyFields":
        return MoneyFields("undiscounted_total_price")

    requires_shipping: CheckoutLineGraphQLField = CheckoutLineGraphQLField(
        "requiresShipping"
    )
    problems: CheckoutLineProblemUnion = CheckoutLineProblemUnion("problems")
    is_gift: CheckoutLineGraphQLField = CheckoutLineGraphQLField("isGift")

    def fields(
        self,
        *subfields: Union[
            CheckoutLineGraphQLField,
            "TaxedMoneyFields",
            "MetadataItemFields",
            "ProductVariantFields",
            "MoneyFields",
            "CheckoutLineProblemUnion",
        ]
    ) -> "CheckoutLineFields":
        self._subfields.extend(subfields)
        return self


class SaleUpdateFields(GraphQLField):
    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    def fields(
        self,
        *subfields: Union[SaleUpdateGraphQLField, "SaleFields", "DiscountErrorFields"]
    ) -> "SaleUpdateFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "DigitalContentFields":
        return DigitalContentFields("node")

    cursor: DigitalContentCountableEdgeGraphQLField = (
        DigitalContentCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[
            DigitalContentCountableEdgeGraphQLField, "DigitalContentFields"
        ]
    ) -> "DigitalContentCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class SaleTranslatableContentFields(GraphQLField):
    id: SaleTranslatableContentGraphQLField = SaleTranslatableContentGraphQLField("id")
    sale_id: SaleTranslatableContentGraphQLField = SaleTranslatableContentGraphQLField(
        "saleId"
    )
    name: SaleTranslatableContentGraphQLField = SaleTranslatableContentGraphQLField(
        "name"
    )

    @classmethod
    def translation(cls) -> "SaleTranslationFields":
        return SaleTranslationFields("translation")

    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    def fields(
        self,
        *subfields: Union[
            SaleTranslatableContentGraphQLField, "SaleTranslationFields", "SaleFields"
        ]
    ) -> "SaleTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueUpdateFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    @classmethod
    def attribute_value(cls) -> "AttributeValueFields":
        return AttributeValueFields("attribute_value")

    def fields(
        self,
        *subfields: Union[
            AttributeValueUpdateGraphQLField,
            "AttributeFields",
            "AttributeValueFields",
            "AttributeErrorFields",
        ]
    ) -> "AttributeValueUpdateFields":
        self._subfields.extend(subfields)
        return self


class OrderRefundFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[OrderRefundGraphQLField, "OrderErrorFields", "OrderFields"]
    ) -> "OrderRefundFields":
        self._subfields.extend(subfields)
        return self


class VoucherRemoveCataloguesFields(GraphQLField):
    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            VoucherRemoveCataloguesGraphQLField, "VoucherFields", "DiscountErrorFields"
        ]
    ) -> "VoucherRemoveCataloguesFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentLineFields(GraphQLField):
    id: FulfillmentLineGraphQLField = FulfillmentLineGraphQLField("id")
    quantity: FulfillmentLineGraphQLField = FulfillmentLineGraphQLField("quantity")

    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    def fields(
        self, *subfields: Union[FulfillmentLineGraphQLField, "OrderLineFields"]
    ) -> "FulfillmentLineFields":
        self._subfields.extend(subfields)
        return self


class ShopSettingsUpdateFields(GraphQLField):
    @classmethod
    def shop(cls) -> "ShopFields":
        return ShopFields("shop")

    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShopSettingsUpdateGraphQLField, "ShopErrorFields", "ShopFields"
        ]
    ) -> "ShopSettingsUpdateFields":
        self._subfields.extend(subfields)
        return self


class CollectionChannelListingUpdateFields(GraphQLField):
    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    @classmethod
    def collection_channel_listing_errors(cls) -> "CollectionChannelListingErrorFields":
        return CollectionChannelListingErrorFields("collection_channel_listing_errors")

    @classmethod
    def errors(cls) -> "CollectionChannelListingErrorFields":
        return CollectionChannelListingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CollectionChannelListingUpdateGraphQLField,
            "CollectionFields",
            "CollectionChannelListingErrorFields",
        ]
    ) -> "CollectionChannelListingUpdateFields":
        self._subfields.extend(subfields)
        return self


class ExternalNotificationErrorFields(GraphQLField):
    field: ExternalNotificationErrorGraphQLField = (
        ExternalNotificationErrorGraphQLField("field")
    )
    message: ExternalNotificationErrorGraphQLField = (
        ExternalNotificationErrorGraphQLField("message")
    )
    code: ExternalNotificationErrorGraphQLField = ExternalNotificationErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: ExternalNotificationErrorGraphQLField
    ) -> "ExternalNotificationErrorFields":
        self._subfields.extend(subfields)
        return self


class VoucherCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "VoucherCountableEdgeFields":
        return VoucherCountableEdgeFields("edges")

    total_count: VoucherCountableConnectionGraphQLField = (
        VoucherCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            VoucherCountableConnectionGraphQLField,
            "PageInfoFields",
            "VoucherCountableEdgeFields",
        ]
    ) -> "VoucherCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class ExternalRefreshFields(GraphQLField):
    token: ExternalRefreshGraphQLField = ExternalRefreshGraphQLField("token")
    refresh_token: ExternalRefreshGraphQLField = ExternalRefreshGraphQLField(
        "refreshToken"
    )
    csrf_token: ExternalRefreshGraphQLField = ExternalRefreshGraphQLField("csrfToken")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExternalRefreshGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "ExternalRefreshFields":
        self._subfields.extend(subfields)
        return self


class ProductMediaFields(GraphQLField):
    id: ProductMediaGraphQLField = ProductMediaGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ProductMediaGraphQLField = ProductMediaGraphQLField(
        "privateMetafield"
    )
    private_metafields: ProductMediaGraphQLField = ProductMediaGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ProductMediaGraphQLField = ProductMediaGraphQLField("metafield")
    metafields: ProductMediaGraphQLField = ProductMediaGraphQLField("metafields")
    sort_order: ProductMediaGraphQLField = ProductMediaGraphQLField("sortOrder")
    alt: ProductMediaGraphQLField = ProductMediaGraphQLField("alt")
    type: ProductMediaGraphQLField = ProductMediaGraphQLField("type")
    oembed_data: ProductMediaGraphQLField = ProductMediaGraphQLField("oembedData")
    url: ProductMediaGraphQLField = ProductMediaGraphQLField("url")
    product_id: ProductMediaGraphQLField = ProductMediaGraphQLField("productId")

    def fields(
        self, *subfields: Union[ProductMediaGraphQLField, "MetadataItemFields"]
    ) -> "ProductMediaFields":
        self._subfields.extend(subfields)
        return self


class CustomerUpdateFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[
            CustomerUpdateGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "CustomerUpdateFields":
        self._subfields.extend(subfields)
        return self


class PageTypeCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "PageTypeCountableEdgeFields":
        return PageTypeCountableEdgeFields("edges")

    total_count: PageTypeCountableConnectionGraphQLField = (
        PageTypeCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            PageTypeCountableConnectionGraphQLField,
            "PageInfoFields",
            "PageTypeCountableEdgeFields",
        ]
    ) -> "PageTypeCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class TransactionUpdateFields(GraphQLField):
    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def errors(cls) -> "TransactionUpdateErrorFields":
        return TransactionUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionUpdateGraphQLField,
            "TransactionItemFields",
            "TransactionUpdateErrorFields",
        ]
    ) -> "TransactionUpdateFields":
        self._subfields.extend(subfields)
        return self


class TaxConfigurationUpdateErrorFields(GraphQLField):
    field: TaxConfigurationUpdateErrorGraphQLField = (
        TaxConfigurationUpdateErrorGraphQLField("field")
    )
    message: TaxConfigurationUpdateErrorGraphQLField = (
        TaxConfigurationUpdateErrorGraphQLField("message")
    )
    code: TaxConfigurationUpdateErrorGraphQLField = (
        TaxConfigurationUpdateErrorGraphQLField("code")
    )
    country_codes: TaxConfigurationUpdateErrorGraphQLField = (
        TaxConfigurationUpdateErrorGraphQLField("countryCodes")
    )

    def fields(
        self, *subfields: TaxConfigurationUpdateErrorGraphQLField
    ) -> "TaxConfigurationUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class UserPermissionFields(GraphQLField):
    code: UserPermissionGraphQLField = UserPermissionGraphQLField("code")
    name: UserPermissionGraphQLField = UserPermissionGraphQLField("name")

    @classmethod
    def source_permission_groups(cls) -> "GroupFields":
        return GroupFields("source_permission_groups")

    def fields(
        self, *subfields: Union[UserPermissionGraphQLField, "GroupFields"]
    ) -> "UserPermissionFields":
        self._subfields.extend(subfields)
        return self


class AttributeTranslationFields(GraphQLField):
    id: AttributeTranslationGraphQLField = AttributeTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: AttributeTranslationGraphQLField = AttributeTranslationGraphQLField("name")

    @classmethod
    def translatable_content(cls) -> "AttributeTranslatableContentFields":
        return AttributeTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            AttributeTranslationGraphQLField,
            "AttributeTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "AttributeTranslationFields":
        self._subfields.extend(subfields)
        return self


class PluginFields(GraphQLField):
    id: PluginGraphQLField = PluginGraphQLField("id")
    name: PluginGraphQLField = PluginGraphQLField("name")
    description: PluginGraphQLField = PluginGraphQLField("description")

    @classmethod
    def global_configuration(cls) -> "PluginConfigurationFields":
        return PluginConfigurationFields("global_configuration")

    @classmethod
    def channel_configurations(cls) -> "PluginConfigurationFields":
        return PluginConfigurationFields("channel_configurations")

    def fields(
        self, *subfields: Union[PluginGraphQLField, "PluginConfigurationFields"]
    ) -> "PluginFields":
        self._subfields.extend(subfields)
        return self


class CollectionTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    def fields(
        self,
        *subfields: Union[
            CollectionTranslateGraphQLField,
            "CollectionFields",
            "TranslationErrorFields",
        ]
    ) -> "CollectionTranslateFields":
        self._subfields.extend(subfields)
        return self


class ProductErrorFields(GraphQLField):
    field: ProductErrorGraphQLField = ProductErrorGraphQLField("field")
    message: ProductErrorGraphQLField = ProductErrorGraphQLField("message")
    code: ProductErrorGraphQLField = ProductErrorGraphQLField("code")
    attributes: ProductErrorGraphQLField = ProductErrorGraphQLField("attributes")
    values: ProductErrorGraphQLField = ProductErrorGraphQLField("values")

    def fields(self, *subfields: ProductErrorGraphQLField) -> "ProductErrorFields":
        self._subfields.extend(subfields)
        return self


class GiftCardBulkActivateFields(GraphQLField):
    count: GiftCardBulkActivateGraphQLField = GiftCardBulkActivateGraphQLField("count")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self, *subfields: Union[GiftCardBulkActivateGraphQLField, "GiftCardErrorFields"]
    ) -> "GiftCardBulkActivateFields":
        self._subfields.extend(subfields)
        return self


class OrderCancelFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[OrderCancelGraphQLField, "OrderErrorFields", "OrderFields"]
    ) -> "OrderCancelFields":
        self._subfields.extend(subfields)
        return self


class TaxClassFields(GraphQLField):
    id: TaxClassGraphQLField = TaxClassGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: TaxClassGraphQLField = TaxClassGraphQLField("privateMetafield")
    private_metafields: TaxClassGraphQLField = TaxClassGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: TaxClassGraphQLField = TaxClassGraphQLField("metafield")
    metafields: TaxClassGraphQLField = TaxClassGraphQLField("metafields")
    name: TaxClassGraphQLField = TaxClassGraphQLField("name")

    @classmethod
    def countries(cls) -> "TaxClassCountryRateFields":
        return TaxClassCountryRateFields("countries")

    def fields(
        self,
        *subfields: Union[
            TaxClassGraphQLField, "MetadataItemFields", "TaxClassCountryRateFields"
        ]
    ) -> "TaxClassFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayInitializeFields(GraphQLField):
    @classmethod
    def gateway_configs(cls) -> "PaymentGatewayConfigFields":
        return PaymentGatewayConfigFields("gateway_configs")

    @classmethod
    def errors(cls) -> "PaymentGatewayInitializeErrorFields":
        return PaymentGatewayInitializeErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentGatewayInitializeGraphQLField,
            "PaymentGatewayConfigFields",
            "PaymentGatewayInitializeErrorFields",
        ]
    ) -> "PaymentGatewayInitializeFields":
        self._subfields.extend(subfields)
        return self


class GiftCardUpdateFields(GraphQLField):
    @classmethod
    def gift_card_errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("gift_card_errors")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    def fields(
        self,
        *subfields: Union[
            GiftCardUpdateGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardUpdateFields":
        self._subfields.extend(subfields)
        return self


class TaxExemptionManageErrorFields(GraphQLField):
    field: TaxExemptionManageErrorGraphQLField = TaxExemptionManageErrorGraphQLField(
        "field"
    )
    message: TaxExemptionManageErrorGraphQLField = TaxExemptionManageErrorGraphQLField(
        "message"
    )
    code: TaxExemptionManageErrorGraphQLField = TaxExemptionManageErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: TaxExemptionManageErrorGraphQLField
    ) -> "TaxExemptionManageErrorFields":
        self._subfields.extend(subfields)
        return self


class StockBulkUpdateErrorFields(GraphQLField):
    field: StockBulkUpdateErrorGraphQLField = StockBulkUpdateErrorGraphQLField("field")
    message: StockBulkUpdateErrorGraphQLField = StockBulkUpdateErrorGraphQLField(
        "message"
    )
    code: StockBulkUpdateErrorGraphQLField = StockBulkUpdateErrorGraphQLField("code")

    def fields(
        self, *subfields: StockBulkUpdateErrorGraphQLField
    ) -> "StockBulkUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductUpdateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    def fields(
        self,
        *subfields: Union[
            ProductUpdateGraphQLField, "ProductFields", "ProductErrorFields"
        ]
    ) -> "ProductUpdateFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeDeleteFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    def fields(
        self,
        *subfields: Union[
            ProductTypeDeleteGraphQLField, "ProductTypeFields", "ProductErrorFields"
        ]
    ) -> "ProductTypeDeleteFields":
        self._subfields.extend(subfields)
        return self


class TransactionRequestActionErrorFields(GraphQLField):
    field: TransactionRequestActionErrorGraphQLField = (
        TransactionRequestActionErrorGraphQLField("field")
    )
    message: TransactionRequestActionErrorGraphQLField = (
        TransactionRequestActionErrorGraphQLField("message")
    )
    code: TransactionRequestActionErrorGraphQLField = (
        TransactionRequestActionErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: TransactionRequestActionErrorGraphQLField
    ) -> "TransactionRequestActionErrorFields":
        self._subfields.extend(subfields)
        return self


class OrderAddNoteFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def event(cls) -> "OrderEventFields":
        return OrderEventFields("event")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderAddNoteGraphQLField,
            "OrderEventFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "OrderAddNoteFields":
        self._subfields.extend(subfields)
        return self


class StoredPaymentMethodFields(GraphQLField):
    id: StoredPaymentMethodGraphQLField = StoredPaymentMethodGraphQLField("id")

    @classmethod
    def gateway(cls) -> "PaymentGatewayFields":
        return PaymentGatewayFields("gateway")

    payment_method_id: StoredPaymentMethodGraphQLField = (
        StoredPaymentMethodGraphQLField("paymentMethodId")
    )

    @classmethod
    def credit_card_info(cls) -> "CreditCardFields":
        return CreditCardFields("credit_card_info")

    supported_payment_flows: StoredPaymentMethodGraphQLField = (
        StoredPaymentMethodGraphQLField("supportedPaymentFlows")
    )
    type: StoredPaymentMethodGraphQLField = StoredPaymentMethodGraphQLField("type")
    name: StoredPaymentMethodGraphQLField = StoredPaymentMethodGraphQLField("name")
    data: StoredPaymentMethodGraphQLField = StoredPaymentMethodGraphQLField("data")

    def fields(
        self,
        *subfields: Union[
            StoredPaymentMethodGraphQLField, "PaymentGatewayFields", "CreditCardFields"
        ]
    ) -> "StoredPaymentMethodFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantedRefundLineFields(GraphQLField):
    id: OrderGrantedRefundLineGraphQLField = OrderGrantedRefundLineGraphQLField("id")
    quantity: OrderGrantedRefundLineGraphQLField = OrderGrantedRefundLineGraphQLField(
        "quantity"
    )

    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    reason: OrderGrantedRefundLineGraphQLField = OrderGrantedRefundLineGraphQLField(
        "reason"
    )

    def fields(
        self, *subfields: Union[OrderGrantedRefundLineGraphQLField, "OrderLineFields"]
    ) -> "OrderGrantedRefundLineFields":
        self._subfields.extend(subfields)
        return self


class TaxCountryConfigurationDeleteFields(GraphQLField):
    @classmethod
    def tax_country_configuration(cls) -> "TaxCountryConfigurationFields":
        return TaxCountryConfigurationFields("tax_country_configuration")

    @classmethod
    def errors(cls) -> "TaxCountryConfigurationDeleteErrorFields":
        return TaxCountryConfigurationDeleteErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TaxCountryConfigurationDeleteGraphQLField,
            "TaxCountryConfigurationFields",
            "TaxCountryConfigurationDeleteErrorFields",
        ]
    ) -> "TaxCountryConfigurationDeleteFields":
        self._subfields.extend(subfields)
        return self


class AppManifestBrandFields(GraphQLField):
    @classmethod
    def logo(cls) -> "AppManifestBrandLogoFields":
        return AppManifestBrandLogoFields("logo")

    def fields(
        self,
        *subfields: Union[AppManifestBrandGraphQLField, "AppManifestBrandLogoFields"]
    ) -> "AppManifestBrandFields":
        self._subfields.extend(subfields)
        return self


class GiftCardDeleteFields(GraphQLField):
    @classmethod
    def gift_card_errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("gift_card_errors")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    def fields(
        self,
        *subfields: Union[
            GiftCardDeleteGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardDeleteFields":
        self._subfields.extend(subfields)
        return self


class WebhookErrorFields(GraphQLField):
    field: WebhookErrorGraphQLField = WebhookErrorGraphQLField("field")
    message: WebhookErrorGraphQLField = WebhookErrorGraphQLField("message")
    code: WebhookErrorGraphQLField = WebhookErrorGraphQLField("code")

    def fields(self, *subfields: WebhookErrorGraphQLField) -> "WebhookErrorFields":
        self._subfields.extend(subfields)
        return self


class MenuItemCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "MenuItemFields":
        return MenuItemFields("node")

    cursor: MenuItemCountableEdgeGraphQLField = MenuItemCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[MenuItemCountableEdgeGraphQLField, "MenuItemFields"]
    ) -> "MenuItemCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentCreateFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    @classmethod
    def content(cls) -> "DigitalContentFields":
        return DigitalContentFields("content")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            DigitalContentCreateGraphQLField,
            "DigitalContentFields",
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "DigitalContentCreateFields":
        self._subfields.extend(subfields)
        return self


class UpdateMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadata_errors")

    @classmethod
    def errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("errors")

    item: ObjectWithMetadataInterface = ObjectWithMetadataInterface("item")

    def fields(
        self,
        *subfields: Union[
            UpdateMetadataGraphQLField,
            "MetadataErrorFields",
            "ObjectWithMetadataInterface",
        ]
    ) -> "UpdateMetadataFields":
        self._subfields.extend(subfields)
        return self


class ProductMediaBulkDeleteFields(GraphQLField):
    count: ProductMediaBulkDeleteGraphQLField = ProductMediaBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[ProductMediaBulkDeleteGraphQLField, "ProductErrorFields"]
    ) -> "ProductMediaBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class TransactionCreateFields(GraphQLField):
    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def errors(cls) -> "TransactionCreateErrorFields":
        return TransactionCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionCreateGraphQLField,
            "TransactionItemFields",
            "TransactionCreateErrorFields",
        ]
    ) -> "TransactionCreateFields":
        self._subfields.extend(subfields)
        return self


class DraftOrderCreateFields(GraphQLField):
    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    def fields(
        self,
        *subfields: Union[
            DraftOrderCreateGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "DraftOrderCreateFields":
        self._subfields.extend(subfields)
        return self


class CategoryTranslatableContentFields(GraphQLField):
    id: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("id")
    )
    category_id: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("categoryId")
    )
    seo_title: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("seoDescription")
    )
    name: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("name")
    )
    description: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("description")
    )
    description_json: CategoryTranslatableContentGraphQLField = (
        CategoryTranslatableContentGraphQLField("descriptionJson")
    )

    @classmethod
    def translation(cls) -> "CategoryTranslationFields":
        return CategoryTranslationFields("translation")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    def fields(
        self,
        *subfields: Union[
            CategoryTranslatableContentGraphQLField,
            "CategoryTranslationFields",
            "CategoryFields",
        ]
    ) -> "CategoryTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class UserCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "UserFields":
        return UserFields("node")

    cursor: UserCountableEdgeGraphQLField = UserCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[UserCountableEdgeGraphQLField, "UserFields"]
    ) -> "UserCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkCreateFields(GraphQLField):
    count: ProductVariantBulkCreateGraphQLField = ProductVariantBulkCreateGraphQLField(
        "count"
    )

    @classmethod
    def product_variants(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variants")

    @classmethod
    def results(cls) -> "ProductVariantBulkResultFields":
        return ProductVariantBulkResultFields("results")

    @classmethod
    def bulk_product_errors(cls) -> "BulkProductErrorFields":
        return BulkProductErrorFields("bulk_product_errors")

    @classmethod
    def errors(cls) -> "BulkProductErrorFields":
        return BulkProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantBulkCreateGraphQLField,
            "BulkProductErrorFields",
            "ProductVariantFields",
            "ProductVariantBulkResultFields",
        ]
    ) -> "ProductVariantBulkCreateFields":
        self._subfields.extend(subfields)
        return self


class OrderFulfillFields(GraphQLField):
    @classmethod
    def fulfillments(cls) -> "FulfillmentFields":
        return FulfillmentFields("fulfillments")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderFulfillGraphQLField,
            "FulfillmentFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "OrderFulfillFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkUpdateFields(GraphQLField):
    count: ProductVariantBulkUpdateGraphQLField = ProductVariantBulkUpdateGraphQLField(
        "count"
    )

    @classmethod
    def results(cls) -> "ProductVariantBulkResultFields":
        return ProductVariantBulkResultFields("results")

    @classmethod
    def errors(cls) -> "ProductVariantBulkErrorFields":
        return ProductVariantBulkErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantBulkUpdateGraphQLField,
            "ProductVariantBulkErrorFields",
            "ProductVariantBulkResultFields",
        ]
    ) -> "ProductVariantBulkUpdateFields":
        self._subfields.extend(subfields)
        return self


class PageAttributeAssignFields(GraphQLField):
    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PageAttributeAssignGraphQLField, "PageTypeFields", "PageErrorFields"
        ]
    ) -> "PageAttributeAssignFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantTranslatableContentFields(GraphQLField):
    id: ProductVariantTranslatableContentGraphQLField = (
        ProductVariantTranslatableContentGraphQLField("id")
    )
    product_variant_id: ProductVariantTranslatableContentGraphQLField = (
        ProductVariantTranslatableContentGraphQLField("productVariantId")
    )
    name: ProductVariantTranslatableContentGraphQLField = (
        ProductVariantTranslatableContentGraphQLField("name")
    )

    @classmethod
    def translation(cls) -> "ProductVariantTranslationFields":
        return ProductVariantTranslationFields("translation")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def attribute_values(cls) -> "AttributeValueTranslatableContentFields":
        return AttributeValueTranslatableContentFields("attribute_values")

    def fields(
        self,
        *subfields: Union[
            ProductVariantTranslatableContentGraphQLField,
            "AttributeValueTranslatableContentFields",
            "ProductVariantTranslationFields",
            "ProductVariantFields",
        ]
    ) -> "ProductVariantTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkTranslateFields(GraphQLField):
    count: ProductBulkTranslateGraphQLField = ProductBulkTranslateGraphQLField("count")

    @classmethod
    def results(cls) -> "ProductBulkTranslateResultFields":
        return ProductBulkTranslateResultFields("results")

    @classmethod
    def errors(cls) -> "ProductBulkTranslateErrorFields":
        return ProductBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductBulkTranslateGraphQLField,
            "ProductBulkTranslateErrorFields",
            "ProductBulkTranslateResultFields",
        ]
    ) -> "ProductBulkTranslateFields":
        self._subfields.extend(subfields)
        return self


class GiftCardCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "GiftCardCountableEdgeFields":
        return GiftCardCountableEdgeFields("edges")

    total_count: GiftCardCountableConnectionGraphQLField = (
        GiftCardCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            GiftCardCountableConnectionGraphQLField,
            "GiftCardCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "GiftCardCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PageUpdateFields(GraphQLField):
    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    @classmethod
    def page(cls) -> "PageFields":
        return PageFields("page")

    def fields(
        self, *subfields: Union[PageUpdateGraphQLField, "PageErrorFields", "PageFields"]
    ) -> "PageUpdateFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkCreateErrorFields(GraphQLField):
    path: AttributeBulkCreateErrorGraphQLField = AttributeBulkCreateErrorGraphQLField(
        "path"
    )
    message: AttributeBulkCreateErrorGraphQLField = (
        AttributeBulkCreateErrorGraphQLField("message")
    )
    code: AttributeBulkCreateErrorGraphQLField = AttributeBulkCreateErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: AttributeBulkCreateErrorGraphQLField
    ) -> "AttributeBulkCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class WarehouseShippingZoneAssignFields(GraphQLField):
    @classmethod
    def warehouse_errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("warehouse_errors")

    @classmethod
    def errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("errors")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    def fields(
        self,
        *subfields: Union[
            WarehouseShippingZoneAssignGraphQLField,
            "WarehouseFields",
            "WarehouseErrorFields",
        ]
    ) -> "WarehouseShippingZoneAssignFields":
        self._subfields.extend(subfields)
        return self


class SendConfirmationEmailErrorFields(GraphQLField):
    field: SendConfirmationEmailErrorGraphQLField = (
        SendConfirmationEmailErrorGraphQLField("field")
    )
    message: SendConfirmationEmailErrorGraphQLField = (
        SendConfirmationEmailErrorGraphQLField("message")
    )
    code: SendConfirmationEmailErrorGraphQLField = (
        SendConfirmationEmailErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: SendConfirmationEmailErrorGraphQLField
    ) -> "SendConfirmationEmailErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductMediaReorderFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductMediaReorderGraphQLField,
            "ProductFields",
            "ProductErrorFields",
            "ProductMediaFields",
        ]
    ) -> "ProductMediaReorderFields":
        self._subfields.extend(subfields)
        return self


class WarehouseUpdateFields(GraphQLField):
    @classmethod
    def warehouse_errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("warehouse_errors")

    @classmethod
    def errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("errors")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    def fields(
        self,
        *subfields: Union[
            WarehouseUpdateGraphQLField, "WarehouseFields", "WarehouseErrorFields"
        ]
    ) -> "WarehouseUpdateFields":
        self._subfields.extend(subfields)
        return self


class InvoiceSendNotificationFields(GraphQLField):
    @classmethod
    def invoice_errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("invoice_errors")

    @classmethod
    def errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("errors")

    @classmethod
    def invoice(cls) -> "InvoiceFields":
        return InvoiceFields("invoice")

    def fields(
        self,
        *subfields: Union[
            InvoiceSendNotificationGraphQLField, "InvoiceErrorFields", "InvoiceFields"
        ]
    ) -> "InvoiceSendNotificationFields":
        self._subfields.extend(subfields)
        return self


class PageTypeDeleteFields(GraphQLField):
    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    def fields(
        self,
        *subfields: Union[
            PageTypeDeleteGraphQLField, "PageTypeFields", "PageErrorFields"
        ]
    ) -> "PageTypeDeleteFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLineCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "CheckoutLineCountableEdgeFields":
        return CheckoutLineCountableEdgeFields("edges")

    total_count: CheckoutLineCountableConnectionGraphQLField = (
        CheckoutLineCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            CheckoutLineCountableConnectionGraphQLField,
            "CheckoutLineCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "CheckoutLineCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class GiftCardBulkDeleteFields(GraphQLField):
    count: GiftCardBulkDeleteGraphQLField = GiftCardBulkDeleteGraphQLField("count")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self, *subfields: Union[GiftCardBulkDeleteGraphQLField, "GiftCardErrorFields"]
    ) -> "GiftCardBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class TransactionItemFields(GraphQLField):
    id: TransactionItemGraphQLField = TransactionItemGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: TransactionItemGraphQLField = TransactionItemGraphQLField(
        "privateMetafield"
    )
    private_metafields: TransactionItemGraphQLField = TransactionItemGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: TransactionItemGraphQLField = TransactionItemGraphQLField("metafield")
    metafields: TransactionItemGraphQLField = TransactionItemGraphQLField("metafields")
    token: TransactionItemGraphQLField = TransactionItemGraphQLField("token")
    created_at: TransactionItemGraphQLField = TransactionItemGraphQLField("createdAt")
    modified_at: TransactionItemGraphQLField = TransactionItemGraphQLField("modifiedAt")
    actions: TransactionItemGraphQLField = TransactionItemGraphQLField("actions")

    @classmethod
    def authorized_amount(cls) -> "MoneyFields":
        return MoneyFields("authorized_amount")

    @classmethod
    def authorize_pending_amount(cls) -> "MoneyFields":
        return MoneyFields("authorize_pending_amount")

    @classmethod
    def refunded_amount(cls) -> "MoneyFields":
        return MoneyFields("refunded_amount")

    @classmethod
    def refund_pending_amount(cls) -> "MoneyFields":
        return MoneyFields("refund_pending_amount")

    @classmethod
    def canceled_amount(cls) -> "MoneyFields":
        return MoneyFields("canceled_amount")

    @classmethod
    def cancel_pending_amount(cls) -> "MoneyFields":
        return MoneyFields("cancel_pending_amount")

    @classmethod
    def charged_amount(cls) -> "MoneyFields":
        return MoneyFields("charged_amount")

    @classmethod
    def charge_pending_amount(cls) -> "MoneyFields":
        return MoneyFields("charge_pending_amount")

    name: TransactionItemGraphQLField = TransactionItemGraphQLField("name")
    message: TransactionItemGraphQLField = TransactionItemGraphQLField("message")
    psp_reference: TransactionItemGraphQLField = TransactionItemGraphQLField(
        "pspReference"
    )

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def events(cls) -> "TransactionEventFields":
        return TransactionEventFields("events")

    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")
    external_url: TransactionItemGraphQLField = TransactionItemGraphQLField(
        "externalUrl"
    )

    def fields(
        self,
        *subfields: Union[
            TransactionItemGraphQLField,
            "OrderFields",
            "CheckoutFields",
            "UserOrAppUnion",
            "MetadataItemFields",
            "MoneyFields",
            "TransactionEventFields",
        ]
    ) -> "TransactionItemFields":
        self._subfields.extend(subfields)
        return self


class GroupFields(GraphQLField):
    id: GroupGraphQLField = GroupGraphQLField("id")
    name: GroupGraphQLField = GroupGraphQLField("name")

    @classmethod
    def users(cls) -> "UserFields":
        return UserFields("users")

    @classmethod
    def permissions(cls) -> "PermissionFields":
        return PermissionFields("permissions")

    user_can_manage: GroupGraphQLField = GroupGraphQLField("userCanManage")

    @classmethod
    def accessible_channels(cls) -> "ChannelFields":
        return ChannelFields("accessible_channels")

    restricted_access_to_channels: GroupGraphQLField = GroupGraphQLField(
        "restrictedAccessToChannels"
    )

    def fields(
        self,
        *subfields: Union[
            GroupGraphQLField, "ChannelFields", "PermissionFields", "UserFields"
        ]
    ) -> "GroupFields":
        self._subfields.extend(subfields)
        return self


class AppDeactivateFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    def fields(
        self,
        *subfields: Union[AppDeactivateGraphQLField, "AppErrorFields", "AppFields"]
    ) -> "AppDeactivateFields":
        self._subfields.extend(subfields)
        return self


class CustomerBulkUpdateErrorFields(GraphQLField):
    path: CustomerBulkUpdateErrorGraphQLField = CustomerBulkUpdateErrorGraphQLField(
        "path"
    )
    message: CustomerBulkUpdateErrorGraphQLField = CustomerBulkUpdateErrorGraphQLField(
        "message"
    )
    code: CustomerBulkUpdateErrorGraphQLField = CustomerBulkUpdateErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: CustomerBulkUpdateErrorGraphQLField
    ) -> "CustomerBulkUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueBulkDeleteFields(GraphQLField):
    count: AttributeValueBulkDeleteGraphQLField = AttributeValueBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    def fields(
        self,
        *subfields: Union[AttributeValueBulkDeleteGraphQLField, "AttributeErrorFields"]
    ) -> "AttributeValueBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class ProductDeleteFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    def fields(
        self,
        *subfields: Union[
            ProductDeleteGraphQLField, "ProductFields", "ProductErrorFields"
        ]
    ) -> "ProductDeleteFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueBulkTranslateFields(GraphQLField):
    count: AttributeValueBulkTranslateGraphQLField = (
        AttributeValueBulkTranslateGraphQLField("count")
    )

    @classmethod
    def results(cls) -> "AttributeValueBulkTranslateResultFields":
        return AttributeValueBulkTranslateResultFields("results")

    @classmethod
    def errors(cls) -> "AttributeValueBulkTranslateErrorFields":
        return AttributeValueBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeValueBulkTranslateGraphQLField,
            "AttributeValueBulkTranslateResultFields",
            "AttributeValueBulkTranslateErrorFields",
        ]
    ) -> "AttributeValueBulkTranslateFields":
        self._subfields.extend(subfields)
        return self


class CreateTokenFields(GraphQLField):
    token: CreateTokenGraphQLField = CreateTokenGraphQLField("token")
    refresh_token: CreateTokenGraphQLField = CreateTokenGraphQLField("refreshToken")
    csrf_token: CreateTokenGraphQLField = CreateTokenGraphQLField("csrfToken")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[CreateTokenGraphQLField, "AccountErrorFields", "UserFields"]
    ) -> "CreateTokenFields":
        self._subfields.extend(subfields)
        return self


class LimitInfoFields(GraphQLField):
    @classmethod
    def current_usage(cls) -> "LimitsFields":
        return LimitsFields("current_usage")

    @classmethod
    def allowed_usage(cls) -> "LimitsFields":
        return LimitsFields("allowed_usage")

    def fields(
        self, *subfields: Union[LimitInfoGraphQLField, "LimitsFields"]
    ) -> "LimitInfoFields":
        self._subfields.extend(subfields)
        return self


class TransactionEventFields(GraphQLField):
    id: TransactionEventGraphQLField = TransactionEventGraphQLField("id")
    created_at: TransactionEventGraphQLField = TransactionEventGraphQLField("createdAt")
    psp_reference: TransactionEventGraphQLField = TransactionEventGraphQLField(
        "pspReference"
    )
    message: TransactionEventGraphQLField = TransactionEventGraphQLField("message")
    external_url: TransactionEventGraphQLField = TransactionEventGraphQLField(
        "externalUrl"
    )

    @classmethod
    def amount(cls) -> "MoneyFields":
        return MoneyFields("amount")

    type: TransactionEventGraphQLField = TransactionEventGraphQLField("type")
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")
    idempotency_key: TransactionEventGraphQLField = TransactionEventGraphQLField(
        "idempotencyKey"
    )

    def fields(
        self,
        *subfields: Union[TransactionEventGraphQLField, "UserOrAppUnion", "MoneyFields"]
    ) -> "TransactionEventFields":
        self._subfields.extend(subfields)
        return self


class DraftOrderDeleteFields(GraphQLField):
    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    def fields(
        self,
        *subfields: Union[
            DraftOrderDeleteGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "DraftOrderDeleteFields":
        self._subfields.extend(subfields)
        return self


class OrderNoteUpdateFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def event(cls) -> "OrderEventFields":
        return OrderEventFields("event")

    @classmethod
    def errors(cls) -> "OrderNoteUpdateErrorFields":
        return OrderNoteUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderNoteUpdateGraphQLField,
            "OrderEventFields",
            "OrderFields",
            "OrderNoteUpdateErrorFields",
        ]
    ) -> "OrderNoteUpdateFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantChannelListingUpdateFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    @classmethod
    def product_channel_listing_errors(cls) -> "ProductChannelListingErrorFields":
        return ProductChannelListingErrorFields("product_channel_listing_errors")

    @classmethod
    def errors(cls) -> "ProductChannelListingErrorFields":
        return ProductChannelListingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantChannelListingUpdateGraphQLField,
            "ProductChannelListingErrorFields",
            "ProductVariantFields",
        ]
    ) -> "ProductVariantChannelListingUpdateFields":
        self._subfields.extend(subfields)
        return self


class AttributeCreateFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeCreateGraphQLField, "AttributeFields", "AttributeErrorFields"
        ]
    ) -> "AttributeCreateFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLinesDeleteFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutLinesDeleteGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutLinesDeleteFields":
        self._subfields.extend(subfields)
        return self


class OrderDiscountDeleteFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderDiscountDeleteGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "OrderDiscountDeleteFields":
        self._subfields.extend(subfields)
        return self


class ChannelUpdateFields(GraphQLField):
    @classmethod
    def channel_errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("channel_errors")

    @classmethod
    def errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("errors")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    def fields(
        self,
        *subfields: Union[
            ChannelUpdateGraphQLField, "ChannelFields", "ChannelErrorFields"
        ]
    ) -> "ChannelUpdateFields":
        self._subfields.extend(subfields)
        return self


class OrderEventFields(GraphQLField):
    id: OrderEventGraphQLField = OrderEventGraphQLField("id")
    date: OrderEventGraphQLField = OrderEventGraphQLField("date")
    type: OrderEventGraphQLField = OrderEventGraphQLField("type")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    message: OrderEventGraphQLField = OrderEventGraphQLField("message")
    email: OrderEventGraphQLField = OrderEventGraphQLField("email")
    email_type: OrderEventGraphQLField = OrderEventGraphQLField("emailType")
    amount: OrderEventGraphQLField = OrderEventGraphQLField("amount")
    payment_id: OrderEventGraphQLField = OrderEventGraphQLField("paymentId")
    payment_gateway: OrderEventGraphQLField = OrderEventGraphQLField("paymentGateway")
    quantity: OrderEventGraphQLField = OrderEventGraphQLField("quantity")
    composed_id: OrderEventGraphQLField = OrderEventGraphQLField("composedId")
    order_number: OrderEventGraphQLField = OrderEventGraphQLField("orderNumber")
    invoice_number: OrderEventGraphQLField = OrderEventGraphQLField("invoiceNumber")
    oversold_items: OrderEventGraphQLField = OrderEventGraphQLField("oversoldItems")

    @classmethod
    def lines(cls) -> "OrderEventOrderLineObjectFields":
        return OrderEventOrderLineObjectFields("lines")

    @classmethod
    def fulfilled_items(cls) -> "FulfillmentLineFields":
        return FulfillmentLineFields("fulfilled_items")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    transaction_reference: OrderEventGraphQLField = OrderEventGraphQLField(
        "transactionReference"
    )
    shipping_costs_included: OrderEventGraphQLField = OrderEventGraphQLField(
        "shippingCostsIncluded"
    )

    @classmethod
    def related_order(cls) -> "OrderFields":
        return OrderFields("related_order")

    @classmethod
    def related(cls) -> "OrderEventFields":
        return OrderEventFields("related")

    @classmethod
    def discount(cls) -> "OrderEventDiscountObjectFields":
        return OrderEventDiscountObjectFields("discount")

    reference: OrderEventGraphQLField = OrderEventGraphQLField("reference")

    def fields(
        self,
        *subfields: Union[
            OrderEventGraphQLField,
            "FulfillmentLineFields",
            "OrderEventDiscountObjectFields",
            "OrderEventOrderLineObjectFields",
            "UserFields",
            "OrderFields",
            "AppFields",
            "OrderEventFields",
            "WarehouseFields",
        ]
    ) -> "OrderEventFields":
        self._subfields.extend(subfields)
        return self


class AppRetryInstallFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app_installation(cls) -> "AppInstallationFields":
        return AppInstallationFields("app_installation")

    def fields(
        self,
        *subfields: Union[
            AppRetryInstallGraphQLField, "AppErrorFields", "AppInstallationFields"
        ]
    ) -> "AppRetryInstallFields":
        self._subfields.extend(subfields)
        return self


class ProductChannelListingErrorFields(GraphQLField):
    field: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("field")
    )
    message: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("message")
    )
    code: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("code")
    )
    attributes: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("attributes")
    )
    values: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("values")
    )
    channels: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("channels")
    )
    variants: ProductChannelListingErrorGraphQLField = (
        ProductChannelListingErrorGraphQLField("variants")
    )

    def fields(
        self, *subfields: ProductChannelListingErrorGraphQLField
    ) -> "ProductChannelListingErrorFields":
        self._subfields.extend(subfields)
        return self


class PromotionDeleteFields(GraphQLField):
    @classmethod
    def errors(cls) -> "PromotionDeleteErrorFields":
        return PromotionDeleteErrorFields("errors")

    @classmethod
    def promotion(cls) -> "PromotionFields":
        return PromotionFields("promotion")

    def fields(
        self,
        *subfields: Union[
            PromotionDeleteGraphQLField, "PromotionFields", "PromotionDeleteErrorFields"
        ]
    ) -> "PromotionDeleteFields":
        self._subfields.extend(subfields)
        return self


class AppCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "AppFields":
        return AppFields("node")

    cursor: AppCountableEdgeGraphQLField = AppCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[AppCountableEdgeGraphQLField, "AppFields"]
    ) -> "AppCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ChannelFields(GraphQLField):
    id: ChannelGraphQLField = ChannelGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ChannelGraphQLField = ChannelGraphQLField("privateMetafield")
    private_metafields: ChannelGraphQLField = ChannelGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ChannelGraphQLField = ChannelGraphQLField("metafield")
    metafields: ChannelGraphQLField = ChannelGraphQLField("metafields")
    slug: ChannelGraphQLField = ChannelGraphQLField("slug")
    name: ChannelGraphQLField = ChannelGraphQLField("name")
    is_active: ChannelGraphQLField = ChannelGraphQLField("isActive")
    currency_code: ChannelGraphQLField = ChannelGraphQLField("currencyCode")
    has_orders: ChannelGraphQLField = ChannelGraphQLField("hasOrders")

    @classmethod
    def default_country(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("default_country")

    @classmethod
    def warehouses(cls) -> "WarehouseFields":
        return WarehouseFields("warehouses")

    @classmethod
    def countries(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("countries")

    @classmethod
    def available_shipping_methods_per_country(
        cls,
    ) -> "ShippingMethodsPerCountryFields":
        return ShippingMethodsPerCountryFields("available_shipping_methods_per_country")

    @classmethod
    def stock_settings(cls) -> "StockSettingsFields":
        return StockSettingsFields("stock_settings")

    @classmethod
    def order_settings(cls) -> "OrderSettingsFields":
        return OrderSettingsFields("order_settings")

    @classmethod
    def checkout_settings(cls) -> "CheckoutSettingsFields":
        return CheckoutSettingsFields("checkout_settings")

    @classmethod
    def payment_settings(cls) -> "PaymentSettingsFields":
        return PaymentSettingsFields("payment_settings")

    @classmethod
    def tax_configuration(cls) -> "TaxConfigurationFields":
        return TaxConfigurationFields("tax_configuration")

    def fields(
        self,
        *subfields: Union[
            ChannelGraphQLField,
            "MetadataItemFields",
            "CheckoutSettingsFields",
            "TaxConfigurationFields",
            "PaymentSettingsFields",
            "CountryDisplayFields",
            "ShippingMethodsPerCountryFields",
            "StockSettingsFields",
            "OrderSettingsFields",
            "WarehouseFields",
        ]
    ) -> "ChannelFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCreateFromOrderUnavailableVariantFields(GraphQLField):
    message: CheckoutCreateFromOrderUnavailableVariantGraphQLField = (
        CheckoutCreateFromOrderUnavailableVariantGraphQLField("message")
    )
    code: CheckoutCreateFromOrderUnavailableVariantGraphQLField = (
        CheckoutCreateFromOrderUnavailableVariantGraphQLField("code")
    )
    variant_id: CheckoutCreateFromOrderUnavailableVariantGraphQLField = (
        CheckoutCreateFromOrderUnavailableVariantGraphQLField("variantId")
    )
    line_id: CheckoutCreateFromOrderUnavailableVariantGraphQLField = (
        CheckoutCreateFromOrderUnavailableVariantGraphQLField("lineId")
    )

    def fields(
        self, *subfields: CheckoutCreateFromOrderUnavailableVariantGraphQLField
    ) -> "CheckoutCreateFromOrderUnavailableVariantFields":
        self._subfields.extend(subfields)
        return self


class StaffCreateFields(GraphQLField):
    @classmethod
    def staff_errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("staff_errors")

    @classmethod
    def errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[StaffCreateGraphQLField, "UserFields", "StaffErrorFields"]
    ) -> "StaffCreateFields":
        self._subfields.extend(subfields)
        return self


class CollectionUpdateFields(GraphQLField):
    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    def fields(
        self,
        *subfields: Union[
            CollectionUpdateGraphQLField, "CollectionFields", "CollectionErrorFields"
        ]
    ) -> "CollectionUpdateFields":
        self._subfields.extend(subfields)
        return self


class AppInstallationFields(GraphQLField):
    id: AppInstallationGraphQLField = AppInstallationGraphQLField("id")
    status: AppInstallationGraphQLField = AppInstallationGraphQLField("status")
    created_at: AppInstallationGraphQLField = AppInstallationGraphQLField("createdAt")
    updated_at: AppInstallationGraphQLField = AppInstallationGraphQLField("updatedAt")
    message: AppInstallationGraphQLField = AppInstallationGraphQLField("message")
    app_name: AppInstallationGraphQLField = AppInstallationGraphQLField("appName")
    manifest_url: AppInstallationGraphQLField = AppInstallationGraphQLField(
        "manifestUrl"
    )

    @classmethod
    def brand(cls) -> "AppBrandFields":
        return AppBrandFields("brand")

    def fields(
        self, *subfields: Union[AppInstallationGraphQLField, "AppBrandFields"]
    ) -> "AppInstallationFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceDeleteFields(GraphQLField):
    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    @classmethod
    def shipping_zone(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("shipping_zone")

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShippingPriceDeleteGraphQLField,
            "ShippingZoneFields",
            "ShippingMethodTypeFields",
            "ShippingErrorFields",
        ]
    ) -> "ShippingPriceDeleteFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "ProductVariantCountableEdgeFields":
        return ProductVariantCountableEdgeFields("edges")

    total_count: ProductVariantCountableConnectionGraphQLField = (
        ProductVariantCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            ProductVariantCountableConnectionGraphQLField,
            "ProductVariantCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "ProductVariantCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class MenuErrorFields(GraphQLField):
    field: MenuErrorGraphQLField = MenuErrorGraphQLField("field")
    message: MenuErrorGraphQLField = MenuErrorGraphQLField("message")
    code: MenuErrorGraphQLField = MenuErrorGraphQLField("code")

    def fields(self, *subfields: MenuErrorGraphQLField) -> "MenuErrorFields":
        self._subfields.extend(subfields)
        return self


class PageTranslationFields(GraphQLField):
    id: PageTranslationGraphQLField = PageTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    seo_title: PageTranslationGraphQLField = PageTranslationGraphQLField("seoTitle")
    seo_description: PageTranslationGraphQLField = PageTranslationGraphQLField(
        "seoDescription"
    )
    title: PageTranslationGraphQLField = PageTranslationGraphQLField("title")
    content: PageTranslationGraphQLField = PageTranslationGraphQLField("content")
    content_json: PageTranslationGraphQLField = PageTranslationGraphQLField(
        "contentJson"
    )

    @classmethod
    def translatable_content(cls) -> "PageTranslatableContentFields":
        return PageTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            PageTranslationGraphQLField,
            "PageTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "PageTranslationFields":
        self._subfields.extend(subfields)
        return self


class WebhookDryRunFields(GraphQLField):
    payload: WebhookDryRunGraphQLField = WebhookDryRunGraphQLField("payload")

    @classmethod
    def errors(cls) -> "WebhookDryRunErrorFields":
        return WebhookDryRunErrorFields("errors")

    def fields(
        self, *subfields: Union[WebhookDryRunGraphQLField, "WebhookDryRunErrorFields"]
    ) -> "WebhookDryRunFields":
        self._subfields.extend(subfields)
        return self


class ChannelDeactivateFields(GraphQLField):
    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def channel_errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("channel_errors")

    @classmethod
    def errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ChannelDeactivateGraphQLField, "ChannelFields", "ChannelErrorFields"
        ]
    ) -> "ChannelDeactivateFields":
        self._subfields.extend(subfields)
        return self


class WebhookEventSyncFields(GraphQLField):
    name: WebhookEventSyncGraphQLField = WebhookEventSyncGraphQLField("name")
    event_type: WebhookEventSyncGraphQLField = WebhookEventSyncGraphQLField("eventType")

    def fields(
        self, *subfields: WebhookEventSyncGraphQLField
    ) -> "WebhookEventSyncFields":
        self._subfields.extend(subfields)
        return self


class TaxClassCountryRateFields(GraphQLField):
    @classmethod
    def country(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("country")

    rate: TaxClassCountryRateGraphQLField = TaxClassCountryRateGraphQLField("rate")

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    def fields(
        self,
        *subfields: Union[
            TaxClassCountryRateGraphQLField, "CountryDisplayFields", "TaxClassFields"
        ]
    ) -> "TaxClassCountryRateFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceRemoveProductFromExcludeFields(GraphQLField):
    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShippingPriceRemoveProductFromExcludeGraphQLField,
            "ShippingMethodTypeFields",
            "ShippingErrorFields",
        ]
    ) -> "ShippingPriceRemoveProductFromExcludeFields":
        self._subfields.extend(subfields)
        return self


class PageTypeFields(GraphQLField):
    id: PageTypeGraphQLField = PageTypeGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: PageTypeGraphQLField = PageTypeGraphQLField("privateMetafield")
    private_metafields: PageTypeGraphQLField = PageTypeGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: PageTypeGraphQLField = PageTypeGraphQLField("metafield")
    metafields: PageTypeGraphQLField = PageTypeGraphQLField("metafields")
    name: PageTypeGraphQLField = PageTypeGraphQLField("name")
    slug: PageTypeGraphQLField = PageTypeGraphQLField("slug")

    @classmethod
    def attributes(cls) -> "AttributeFields":
        return AttributeFields("attributes")

    @classmethod
    def available_attributes(cls) -> "AttributeCountableConnectionFields":
        return AttributeCountableConnectionFields("available_attributes")

    has_pages: PageTypeGraphQLField = PageTypeGraphQLField("hasPages")

    def fields(
        self,
        *subfields: Union[
            PageTypeGraphQLField,
            "MetadataItemFields",
            "AttributeFields",
            "AttributeCountableConnectionFields",
        ]
    ) -> "PageTypeFields":
        self._subfields.extend(subfields)
        return self


class CheckoutAddPromoCodeFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutAddPromoCodeGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutAddPromoCodeFields":
        self._subfields.extend(subfields)
        return self


class CheckoutShippingMethodUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutShippingMethodUpdateGraphQLField,
            "CheckoutErrorFields",
            "CheckoutFields",
        ]
    ) -> "CheckoutShippingMethodUpdateFields":
        self._subfields.extend(subfields)
        return self


class UserAvatarUpdateFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            UserAvatarUpdateGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "UserAvatarUpdateFields":
        self._subfields.extend(subfields)
        return self


class MenuDeleteFields(GraphQLField):
    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    @classmethod
    def menu(cls) -> "MenuFields":
        return MenuFields("menu")

    def fields(
        self, *subfields: Union[MenuDeleteGraphQLField, "MenuFields", "MenuErrorFields"]
    ) -> "MenuDeleteFields":
        self._subfields.extend(subfields)
        return self


class GiftCardTagCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "GiftCardTagFields":
        return GiftCardTagFields("node")

    cursor: GiftCardTagCountableEdgeGraphQLField = GiftCardTagCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self,
        *subfields: Union[GiftCardTagCountableEdgeGraphQLField, "GiftCardTagFields"]
    ) -> "GiftCardTagCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantRefundUpdateLineErrorFields(GraphQLField):
    field: OrderGrantRefundUpdateLineErrorGraphQLField = (
        OrderGrantRefundUpdateLineErrorGraphQLField("field")
    )
    message: OrderGrantRefundUpdateLineErrorGraphQLField = (
        OrderGrantRefundUpdateLineErrorGraphQLField("message")
    )
    code: OrderGrantRefundUpdateLineErrorGraphQLField = (
        OrderGrantRefundUpdateLineErrorGraphQLField("code")
    )
    line_id: OrderGrantRefundUpdateLineErrorGraphQLField = (
        OrderGrantRefundUpdateLineErrorGraphQLField("lineId")
    )

    def fields(
        self, *subfields: OrderGrantRefundUpdateLineErrorGraphQLField
    ) -> "OrderGrantRefundUpdateLineErrorFields":
        self._subfields.extend(subfields)
        return self


class StockSettingsFields(GraphQLField):
    allocation_strategy: StockSettingsGraphQLField = StockSettingsGraphQLField(
        "allocationStrategy"
    )

    def fields(self, *subfields: StockSettingsGraphQLField) -> "StockSettingsFields":
        self._subfields.extend(subfields)
        return self


class OrderUpdateFields(GraphQLField):
    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    def fields(
        self,
        *subfields: Union[OrderUpdateGraphQLField, "OrderErrorFields", "OrderFields"]
    ) -> "OrderUpdateFields":
        self._subfields.extend(subfields)
        return self


class PageTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def page(cls) -> "PageTranslatableContentFields":
        return PageTranslatableContentFields("page")

    def fields(
        self,
        *subfields: Union[
            PageTranslateGraphQLField,
            "PageTranslatableContentFields",
            "TranslationErrorFields",
        ]
    ) -> "PageTranslateFields":
        self._subfields.extend(subfields)
        return self


class CheckoutShippingAddressUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutShippingAddressUpdateGraphQLField,
            "CheckoutErrorFields",
            "CheckoutFields",
        ]
    ) -> "CheckoutShippingAddressUpdateFields":
        self._subfields.extend(subfields)
        return self


class TaxClassCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "TaxClassFields":
        return TaxClassFields("node")

    cursor: TaxClassCountableEdgeGraphQLField = TaxClassCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[TaxClassCountableEdgeGraphQLField, "TaxClassFields"]
    ) -> "TaxClassCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ShopFetchTaxRatesFields(GraphQLField):
    @classmethod
    def shop(cls) -> "ShopFields":
        return ShopFields("shop")

    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShopFetchTaxRatesGraphQLField, "ShopErrorFields", "ShopFields"
        ]
    ) -> "ShopFetchTaxRatesFields":
        self._subfields.extend(subfields)
        return self


class CheckoutErrorFields(GraphQLField):
    field: CheckoutErrorGraphQLField = CheckoutErrorGraphQLField("field")
    message: CheckoutErrorGraphQLField = CheckoutErrorGraphQLField("message")
    code: CheckoutErrorGraphQLField = CheckoutErrorGraphQLField("code")
    variants: CheckoutErrorGraphQLField = CheckoutErrorGraphQLField("variants")
    lines: CheckoutErrorGraphQLField = CheckoutErrorGraphQLField("lines")
    address_type: CheckoutErrorGraphQLField = CheckoutErrorGraphQLField("addressType")

    def fields(self, *subfields: CheckoutErrorGraphQLField) -> "CheckoutErrorFields":
        self._subfields.extend(subfields)
        return self


class StaffBulkDeleteFields(GraphQLField):
    count: StaffBulkDeleteGraphQLField = StaffBulkDeleteGraphQLField("count")

    @classmethod
    def staff_errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("staff_errors")

    @classmethod
    def errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("errors")

    def fields(
        self, *subfields: Union[StaffBulkDeleteGraphQLField, "StaffErrorFields"]
    ) -> "StaffBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "EventDeliveryFields":
        return EventDeliveryFields("node")

    cursor: EventDeliveryCountableEdgeGraphQLField = (
        EventDeliveryCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[EventDeliveryCountableEdgeGraphQLField, "EventDeliveryFields"]
    ) -> "EventDeliveryCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class CheckoutDeliveryMethodUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutDeliveryMethodUpdateGraphQLField,
            "CheckoutErrorFields",
            "CheckoutFields",
        ]
    ) -> "CheckoutDeliveryMethodUpdateFields":
        self._subfields.extend(subfields)
        return self


class MenuItemCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "MenuItemCountableEdgeFields":
        return MenuItemCountableEdgeFields("edges")

    total_count: MenuItemCountableConnectionGraphQLField = (
        MenuItemCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            MenuItemCountableConnectionGraphQLField,
            "MenuItemCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "MenuItemCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PluginCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "PluginFields":
        return PluginFields("node")

    cursor: PluginCountableEdgeGraphQLField = PluginCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[PluginCountableEdgeGraphQLField, "PluginFields"]
    ) -> "PluginCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ProductMediaCreateFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductMediaCreateGraphQLField,
            "ProductFields",
            "ProductErrorFields",
            "ProductMediaFields",
        ]
    ) -> "ProductMediaCreateFields":
        self._subfields.extend(subfields)
        return self


class OrderVoidFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[OrderVoidGraphQLField, "OrderErrorFields", "OrderFields"]
    ) -> "OrderVoidFields":
        self._subfields.extend(subfields)
        return self


class SaleBulkDeleteFields(GraphQLField):
    count: SaleBulkDeleteGraphQLField = SaleBulkDeleteGraphQLField("count")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self, *subfields: Union[SaleBulkDeleteGraphQLField, "DiscountErrorFields"]
    ) -> "SaleBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class SaleAddCataloguesFields(GraphQLField):
    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            SaleAddCataloguesGraphQLField, "SaleFields", "DiscountErrorFields"
        ]
    ) -> "SaleAddCataloguesFields":
        self._subfields.extend(subfields)
        return self


class GiftCardBulkDeactivateFields(GraphQLField):
    count: GiftCardBulkDeactivateGraphQLField = GiftCardBulkDeactivateGraphQLField(
        "count"
    )

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self,
        *subfields: Union[GiftCardBulkDeactivateGraphQLField, "GiftCardErrorFields"]
    ) -> "GiftCardBulkDeactivateFields":
        self._subfields.extend(subfields)
        return self


class AddressSetDefaultFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AddressSetDefaultGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "AddressSetDefaultFields":
        self._subfields.extend(subfields)
        return self


class ProductTranslatableContentFields(GraphQLField):
    id: ProductTranslatableContentGraphQLField = ProductTranslatableContentGraphQLField(
        "id"
    )
    product_id: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("productId")
    )
    seo_title: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("seoDescription")
    )
    name: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("name")
    )
    description: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("description")
    )
    description_json: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("descriptionJson")
    )

    @classmethod
    def translation(cls) -> "ProductTranslationFields":
        return ProductTranslationFields("translation")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def attribute_values(cls) -> "AttributeValueTranslatableContentFields":
        return AttributeValueTranslatableContentFields("attribute_values")

    def fields(
        self,
        *subfields: Union[
            ProductTranslatableContentGraphQLField,
            "AttributeValueTranslatableContentFields",
            "ProductFields",
            "ProductTranslationFields",
        ]
    ) -> "ProductTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class OrderUpdateShippingFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderUpdateShippingGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "OrderUpdateShippingFields":
        self._subfields.extend(subfields)
        return self


class GroupCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "GroupCountableEdgeFields":
        return GroupCountableEdgeFields("edges")

    total_count: GroupCountableConnectionGraphQLField = (
        GroupCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            GroupCountableConnectionGraphQLField,
            "PageInfoFields",
            "GroupCountableEdgeFields",
        ]
    ) -> "GroupCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class AppFetchManifestFields(GraphQLField):
    @classmethod
    def manifest(cls) -> "ManifestFields":
        return ManifestFields("manifest")

    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AppFetchManifestGraphQLField, "AppErrorFields", "ManifestFields"
        ]
    ) -> "AppFetchManifestFields":
        self._subfields.extend(subfields)
        return self


class AccountErrorFields(GraphQLField):
    field: AccountErrorGraphQLField = AccountErrorGraphQLField("field")
    message: AccountErrorGraphQLField = AccountErrorGraphQLField("message")
    code: AccountErrorGraphQLField = AccountErrorGraphQLField("code")
    address_type: AccountErrorGraphQLField = AccountErrorGraphQLField("addressType")

    def fields(self, *subfields: AccountErrorGraphQLField) -> "AccountErrorFields":
        self._subfields.extend(subfields)
        return self


class InvoiceFields(GraphQLField):
    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: InvoiceGraphQLField = InvoiceGraphQLField("privateMetafield")
    private_metafields: InvoiceGraphQLField = InvoiceGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: InvoiceGraphQLField = InvoiceGraphQLField("metafield")
    metafields: InvoiceGraphQLField = InvoiceGraphQLField("metafields")
    status: InvoiceGraphQLField = InvoiceGraphQLField("status")
    created_at: InvoiceGraphQLField = InvoiceGraphQLField("createdAt")
    updated_at: InvoiceGraphQLField = InvoiceGraphQLField("updatedAt")
    message: InvoiceGraphQLField = InvoiceGraphQLField("message")
    id: InvoiceGraphQLField = InvoiceGraphQLField("id")
    number: InvoiceGraphQLField = InvoiceGraphQLField("number")
    external_url: InvoiceGraphQLField = InvoiceGraphQLField("externalUrl")
    url: InvoiceGraphQLField = InvoiceGraphQLField("url")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    def fields(
        self,
        *subfields: Union[InvoiceGraphQLField, "MetadataItemFields", "OrderFields"]
    ) -> "InvoiceFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "CheckoutFields":
        return CheckoutFields("node")

    cursor: CheckoutCountableEdgeGraphQLField = CheckoutCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[CheckoutCountableEdgeGraphQLField, "CheckoutFields"]
    ) -> "CheckoutCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkCreateErrorFields(GraphQLField):
    path: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "path"
    )
    message: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "message"
    )
    code: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "code"
    )
    attributes: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "attributes"
    )
    values: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "values"
    )
    warehouses: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "warehouses"
    )
    channels: ProductBulkCreateErrorGraphQLField = ProductBulkCreateErrorGraphQLField(
        "channels"
    )

    def fields(
        self, *subfields: ProductBulkCreateErrorGraphQLField
    ) -> "ProductBulkCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class StaffUpdateFields(GraphQLField):
    @classmethod
    def staff_errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("staff_errors")

    @classmethod
    def errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[StaffUpdateGraphQLField, "UserFields", "StaffErrorFields"]
    ) -> "StaffUpdateFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantPreorderDeactivateFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantPreorderDeactivateGraphQLField,
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "ProductVariantPreorderDeactivateFields":
        self._subfields.extend(subfields)
        return self


class WebhookEventFields(GraphQLField):
    name: WebhookEventGraphQLField = WebhookEventGraphQLField("name")
    event_type: WebhookEventGraphQLField = WebhookEventGraphQLField("eventType")

    def fields(self, *subfields: WebhookEventGraphQLField) -> "WebhookEventFields":
        self._subfields.extend(subfields)
        return self


class ShopTranslationFields(GraphQLField):
    id: ShopTranslationGraphQLField = ShopTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    header_text: ShopTranslationGraphQLField = ShopTranslationGraphQLField("headerText")
    description: ShopTranslationGraphQLField = ShopTranslationGraphQLField(
        "description"
    )

    def fields(
        self, *subfields: Union[ShopTranslationGraphQLField, "LanguageDisplayFields"]
    ) -> "ShopTranslationFields":
        self._subfields.extend(subfields)
        return self


class RequestPasswordResetFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self, *subfields: Union[RequestPasswordResetGraphQLField, "AccountErrorFields"]
    ) -> "RequestPasswordResetFields":
        self._subfields.extend(subfields)
        return self


class OrderErrorFields(GraphQLField):
    field: OrderErrorGraphQLField = OrderErrorGraphQLField("field")
    message: OrderErrorGraphQLField = OrderErrorGraphQLField("message")
    code: OrderErrorGraphQLField = OrderErrorGraphQLField("code")
    warehouse: OrderErrorGraphQLField = OrderErrorGraphQLField("warehouse")
    order_lines: OrderErrorGraphQLField = OrderErrorGraphQLField("orderLines")
    variants: OrderErrorGraphQLField = OrderErrorGraphQLField("variants")
    address_type: OrderErrorGraphQLField = OrderErrorGraphQLField("addressType")

    def fields(self, *subfields: OrderErrorGraphQLField) -> "OrderErrorFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleCreateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "PromotionRuleCreateErrorFields":
        return PromotionRuleCreateErrorFields("errors")

    @classmethod
    def promotion_rule(cls) -> "PromotionRuleFields":
        return PromotionRuleFields("promotion_rule")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleCreateGraphQLField,
            "PromotionRuleCreateErrorFields",
            "PromotionRuleFields",
        ]
    ) -> "PromotionRuleCreateFields":
        self._subfields.extend(subfields)
        return self


class AppCreateFields(GraphQLField):
    auth_token: AppCreateGraphQLField = AppCreateGraphQLField("authToken")

    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    def fields(
        self, *subfields: Union[AppCreateGraphQLField, "AppErrorFields", "AppFields"]
    ) -> "AppCreateFields":
        self._subfields.extend(subfields)
        return self


class WarehouseFields(GraphQLField):
    id: WarehouseGraphQLField = WarehouseGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: WarehouseGraphQLField = WarehouseGraphQLField("privateMetafield")
    private_metafields: WarehouseGraphQLField = WarehouseGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: WarehouseGraphQLField = WarehouseGraphQLField("metafield")
    metafields: WarehouseGraphQLField = WarehouseGraphQLField("metafields")
    name: WarehouseGraphQLField = WarehouseGraphQLField("name")
    slug: WarehouseGraphQLField = WarehouseGraphQLField("slug")
    email: WarehouseGraphQLField = WarehouseGraphQLField("email")
    is_private: WarehouseGraphQLField = WarehouseGraphQLField("isPrivate")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    company_name: WarehouseGraphQLField = WarehouseGraphQLField("companyName")
    click_and_collect_option: WarehouseGraphQLField = WarehouseGraphQLField(
        "clickAndCollectOption"
    )

    @classmethod
    def shipping_zones(cls) -> "ShippingZoneCountableConnectionFields":
        return ShippingZoneCountableConnectionFields("shipping_zones")

    @classmethod
    def stocks(cls) -> "StockCountableConnectionFields":
        return StockCountableConnectionFields("stocks")

    external_reference: WarehouseGraphQLField = WarehouseGraphQLField(
        "externalReference"
    )

    def fields(
        self,
        *subfields: Union[
            WarehouseGraphQLField,
            "ShippingZoneCountableConnectionFields",
            "MetadataItemFields",
            "StockCountableConnectionFields",
            "AddressFields",
        ]
    ) -> "WarehouseFields":
        self._subfields.extend(subfields)
        return self


class TaxConfigurationPerCountryFields(GraphQLField):
    @classmethod
    def country(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("country")

    charge_taxes: TaxConfigurationPerCountryGraphQLField = (
        TaxConfigurationPerCountryGraphQLField("chargeTaxes")
    )
    tax_calculation_strategy: TaxConfigurationPerCountryGraphQLField = (
        TaxConfigurationPerCountryGraphQLField("taxCalculationStrategy")
    )
    display_gross_prices: TaxConfigurationPerCountryGraphQLField = (
        TaxConfigurationPerCountryGraphQLField("displayGrossPrices")
    )
    tax_app_id: TaxConfigurationPerCountryGraphQLField = (
        TaxConfigurationPerCountryGraphQLField("taxAppId")
    )

    def fields(
        self,
        *subfields: Union[
            TaxConfigurationPerCountryGraphQLField, "CountryDisplayFields"
        ]
    ) -> "TaxConfigurationPerCountryFields":
        self._subfields.extend(subfields)
        return self


class UserBulkSetActiveFields(GraphQLField):
    count: UserBulkSetActiveGraphQLField = UserBulkSetActiveGraphQLField("count")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self, *subfields: Union[UserBulkSetActiveGraphQLField, "AccountErrorFields"]
    ) -> "UserBulkSetActiveFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleUpdateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "PromotionRuleUpdateErrorFields":
        return PromotionRuleUpdateErrorFields("errors")

    @classmethod
    def promotion_rule(cls) -> "PromotionRuleFields":
        return PromotionRuleFields("promotion_rule")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleUpdateGraphQLField,
            "PromotionRuleUpdateErrorFields",
            "PromotionRuleFields",
        ]
    ) -> "PromotionRuleUpdateFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def attribute_value(cls) -> "AttributeValueFields":
        return AttributeValueFields("attribute_value")

    def fields(
        self,
        *subfields: Union[
            AttributeValueTranslateGraphQLField,
            "AttributeValueFields",
            "TranslationErrorFields",
        ]
    ) -> "AttributeValueTranslateFields":
        self._subfields.extend(subfields)
        return self


class VariantMediaAssignFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            VariantMediaAssignGraphQLField,
            "ProductMediaFields",
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "VariantMediaAssignFields":
        self._subfields.extend(subfields)
        return self


class UserFields(GraphQLField):
    id: UserGraphQLField = UserGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: UserGraphQLField = UserGraphQLField("privateMetafield")
    private_metafields: UserGraphQLField = UserGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: UserGraphQLField = UserGraphQLField("metafield")
    metafields: UserGraphQLField = UserGraphQLField("metafields")
    email: UserGraphQLField = UserGraphQLField("email")
    first_name: UserGraphQLField = UserGraphQLField("firstName")
    last_name: UserGraphQLField = UserGraphQLField("lastName")
    is_staff: UserGraphQLField = UserGraphQLField("isStaff")
    is_active: UserGraphQLField = UserGraphQLField("isActive")
    is_confirmed: UserGraphQLField = UserGraphQLField("isConfirmed")

    @classmethod
    def addresses(cls) -> "AddressFields":
        return AddressFields("addresses")

    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    checkout_tokens: UserGraphQLField = UserGraphQLField("checkoutTokens")
    checkout_ids: UserGraphQLField = UserGraphQLField("checkoutIds")

    @classmethod
    def checkouts(cls) -> "CheckoutCountableConnectionFields":
        return CheckoutCountableConnectionFields("checkouts")

    @classmethod
    def gift_cards(cls) -> "GiftCardCountableConnectionFields":
        return GiftCardCountableConnectionFields("gift_cards")

    note: UserGraphQLField = UserGraphQLField("note")

    @classmethod
    def orders(cls) -> "OrderCountableConnectionFields":
        return OrderCountableConnectionFields("orders")

    @classmethod
    def user_permissions(cls) -> "UserPermissionFields":
        return UserPermissionFields("user_permissions")

    @classmethod
    def permission_groups(cls) -> "GroupFields":
        return GroupFields("permission_groups")

    @classmethod
    def editable_groups(cls) -> "GroupFields":
        return GroupFields("editable_groups")

    @classmethod
    def accessible_channels(cls) -> "ChannelFields":
        return ChannelFields("accessible_channels")

    restricted_access_to_channels: UserGraphQLField = UserGraphQLField(
        "restrictedAccessToChannels"
    )

    @classmethod
    def avatar(cls) -> "ImageFields":
        return ImageFields("avatar")

    @classmethod
    def events(cls) -> "CustomerEventFields":
        return CustomerEventFields("events")

    @classmethod
    def stored_payment_sources(cls) -> "PaymentSourceFields":
        return PaymentSourceFields("stored_payment_sources")

    language_code: UserGraphQLField = UserGraphQLField("languageCode")

    @classmethod
    def default_shipping_address(cls) -> "AddressFields":
        return AddressFields("default_shipping_address")

    @classmethod
    def default_billing_address(cls) -> "AddressFields":
        return AddressFields("default_billing_address")

    external_reference: UserGraphQLField = UserGraphQLField("externalReference")
    last_login: UserGraphQLField = UserGraphQLField("lastLogin")
    date_joined: UserGraphQLField = UserGraphQLField("dateJoined")
    updated_at: UserGraphQLField = UserGraphQLField("updatedAt")

    @classmethod
    def stored_payment_methods(cls) -> "StoredPaymentMethodFields":
        return StoredPaymentMethodFields("stored_payment_methods")

    def fields(
        self,
        *subfields: Union[
            UserGraphQLField,
            "GroupFields",
            "GiftCardCountableConnectionFields",
            "OrderCountableConnectionFields",
            "CustomerEventFields",
            "CheckoutFields",
            "MetadataItemFields",
            "ImageFields",
            "ChannelFields",
            "StoredPaymentMethodFields",
            "PaymentSourceFields",
            "AddressFields",
            "UserPermissionFields",
            "CheckoutCountableConnectionFields",
        ]
    ) -> "UserFields":
        self._subfields.extend(subfields)
        return self


class InvoiceRequestDeleteFields(GraphQLField):
    @classmethod
    def invoice_errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("invoice_errors")

    @classmethod
    def errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("errors")

    @classmethod
    def invoice(cls) -> "InvoiceFields":
        return InvoiceFields("invoice")

    def fields(
        self,
        *subfields: Union[
            InvoiceRequestDeleteGraphQLField, "InvoiceErrorFields", "InvoiceFields"
        ]
    ) -> "InvoiceRequestDeleteFields":
        self._subfields.extend(subfields)
        return self


class ExportErrorFields(GraphQLField):
    field: ExportErrorGraphQLField = ExportErrorGraphQLField("field")
    message: ExportErrorGraphQLField = ExportErrorGraphQLField("message")
    code: ExportErrorGraphQLField = ExportErrorGraphQLField("code")

    def fields(self, *subfields: ExportErrorGraphQLField) -> "ExportErrorFields":
        self._subfields.extend(subfields)
        return self


class PageAttributeUnassignFields(GraphQLField):
    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PageAttributeUnassignGraphQLField, "PageTypeFields", "PageErrorFields"
        ]
    ) -> "PageAttributeUnassignFields":
        self._subfields.extend(subfields)
        return self


class CategoryFields(GraphQLField):
    id: CategoryGraphQLField = CategoryGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: CategoryGraphQLField = CategoryGraphQLField("privateMetafield")
    private_metafields: CategoryGraphQLField = CategoryGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: CategoryGraphQLField = CategoryGraphQLField("metafield")
    metafields: CategoryGraphQLField = CategoryGraphQLField("metafields")
    seo_title: CategoryGraphQLField = CategoryGraphQLField("seoTitle")
    seo_description: CategoryGraphQLField = CategoryGraphQLField("seoDescription")
    name: CategoryGraphQLField = CategoryGraphQLField("name")
    description: CategoryGraphQLField = CategoryGraphQLField("description")
    slug: CategoryGraphQLField = CategoryGraphQLField("slug")

    @classmethod
    def parent(cls) -> "CategoryFields":
        return CategoryFields("parent")

    level: CategoryGraphQLField = CategoryGraphQLField("level")
    description_json: CategoryGraphQLField = CategoryGraphQLField("descriptionJson")
    updated_at: CategoryGraphQLField = CategoryGraphQLField("updatedAt")

    @classmethod
    def ancestors(cls) -> "CategoryCountableConnectionFields":
        return CategoryCountableConnectionFields("ancestors")

    @classmethod
    def products(cls) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields("products")

    @classmethod
    def children(cls) -> "CategoryCountableConnectionFields":
        return CategoryCountableConnectionFields("children")

    @classmethod
    def background_image(cls) -> "ImageFields":
        return ImageFields("background_image")

    @classmethod
    def translation(cls) -> "CategoryTranslationFields":
        return CategoryTranslationFields("translation")

    def fields(
        self,
        *subfields: Union[
            CategoryGraphQLField,
            "MetadataItemFields",
            "ProductCountableConnectionFields",
            "ImageFields",
            "CategoryFields",
            "CategoryTranslationFields",
            "CategoryCountableConnectionFields",
        ]
    ) -> "CategoryFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantStocksDeleteFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def stock_errors(cls) -> "StockErrorFields":
        return StockErrorFields("stock_errors")

    @classmethod
    def errors(cls) -> "StockErrorFields":
        return StockErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantStocksDeleteGraphQLField,
            "StockErrorFields",
            "ProductVariantFields",
        ]
    ) -> "ProductVariantStocksDeleteFields":
        self._subfields.extend(subfields)
        return self


class PromotionTranslationFields(GraphQLField):
    id: PromotionTranslationGraphQLField = PromotionTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: PromotionTranslationGraphQLField = PromotionTranslationGraphQLField("name")
    description: PromotionTranslationGraphQLField = PromotionTranslationGraphQLField(
        "description"
    )

    @classmethod
    def translatable_content(cls) -> "PromotionTranslatableContentFields":
        return PromotionTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            PromotionTranslationGraphQLField,
            "PromotionTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "PromotionTranslationFields":
        self._subfields.extend(subfields)
        return self


class TaxClassCreateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "TaxClassCreateErrorFields":
        return TaxClassCreateErrorFields("errors")

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    def fields(
        self,
        *subfields: Union[
            TaxClassCreateGraphQLField, "TaxClassFields", "TaxClassCreateErrorFields"
        ]
    ) -> "TaxClassCreateFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceCreateFields(GraphQLField):
    @classmethod
    def shipping_zone(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("shipping_zone")

    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShippingPriceCreateGraphQLField,
            "ShippingZoneFields",
            "ShippingMethodTypeFields",
            "ShippingErrorFields",
        ]
    ) -> "ShippingPriceCreateFields":
        self._subfields.extend(subfields)
        return self


class CategoryDeleteFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    def fields(
        self,
        *subfields: Union[
            CategoryDeleteGraphQLField, "ProductErrorFields", "CategoryFields"
        ]
    ) -> "CategoryDeleteFields":
        self._subfields.extend(subfields)
        return self


class ProductMediaDeleteFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductMediaDeleteGraphQLField,
            "ProductFields",
            "ProductErrorFields",
            "ProductMediaFields",
        ]
    ) -> "ProductMediaDeleteFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeUpdateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    def fields(
        self,
        *subfields: Union[
            ProductTypeUpdateGraphQLField, "ProductTypeFields", "ProductErrorFields"
        ]
    ) -> "ProductTypeUpdateFields":
        self._subfields.extend(subfields)
        return self


class TransactionRequestActionFields(GraphQLField):
    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def errors(cls) -> "TransactionRequestActionErrorFields":
        return TransactionRequestActionErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionRequestActionGraphQLField,
            "TransactionItemFields",
            "TransactionRequestActionErrorFields",
        ]
    ) -> "TransactionRequestActionFields":
        self._subfields.extend(subfields)
        return self


class ExportFileCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "ExportFileCountableEdgeFields":
        return ExportFileCountableEdgeFields("edges")

    total_count: ExportFileCountableConnectionGraphQLField = (
        ExportFileCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            ExportFileCountableConnectionGraphQLField,
            "PageInfoFields",
            "ExportFileCountableEdgeFields",
        ]
    ) -> "ExportFileCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PromotionTranslatableContentFields(GraphQLField):
    id: PromotionTranslatableContentGraphQLField = (
        PromotionTranslatableContentGraphQLField("id")
    )
    promotion_id: PromotionTranslatableContentGraphQLField = (
        PromotionTranslatableContentGraphQLField("promotionId")
    )
    name: PromotionTranslatableContentGraphQLField = (
        PromotionTranslatableContentGraphQLField("name")
    )
    description: PromotionTranslatableContentGraphQLField = (
        PromotionTranslatableContentGraphQLField("description")
    )

    @classmethod
    def translation(cls) -> "PromotionTranslationFields":
        return PromotionTranslationFields("translation")

    def fields(
        self,
        *subfields: Union[
            PromotionTranslatableContentGraphQLField, "PromotionTranslationFields"
        ]
    ) -> "PromotionTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class CollectionTranslatableContentFields(GraphQLField):
    id: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("id")
    )
    collection_id: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("collectionId")
    )
    seo_title: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("seoDescription")
    )
    name: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("name")
    )
    description: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("description")
    )
    description_json: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("descriptionJson")
    )

    @classmethod
    def translation(cls) -> "CollectionTranslationFields":
        return CollectionTranslationFields("translation")

    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    def fields(
        self,
        *subfields: Union[
            CollectionTranslatableContentGraphQLField,
            "CollectionTranslationFields",
            "CollectionFields",
        ]
    ) -> "CollectionTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class CustomerEventFields(GraphQLField):
    id: CustomerEventGraphQLField = CustomerEventGraphQLField("id")
    date: CustomerEventGraphQLField = CustomerEventGraphQLField("date")
    type: CustomerEventGraphQLField = CustomerEventGraphQLField("type")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    message: CustomerEventGraphQLField = CustomerEventGraphQLField("message")
    count: CustomerEventGraphQLField = CustomerEventGraphQLField("count")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    def fields(
        self,
        *subfields: Union[
            CustomerEventGraphQLField,
            "OrderFields",
            "AppFields",
            "UserFields",
            "OrderLineFields",
        ]
    ) -> "CustomerEventFields":
        self._subfields.extend(subfields)
        return self


class CollectionCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "CollectionFields":
        return CollectionFields("node")

    cursor: CollectionCountableEdgeGraphQLField = CollectionCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[CollectionCountableEdgeGraphQLField, "CollectionFields"]
    ) -> "CollectionCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class PageCreateFields(GraphQLField):
    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    @classmethod
    def page(cls) -> "PageFields":
        return PageFields("page")

    def fields(
        self, *subfields: Union[PageCreateGraphQLField, "PageErrorFields", "PageFields"]
    ) -> "PageCreateFields":
        self._subfields.extend(subfields)
        return self


class PaymentMethodInitializeTokenizationErrorFields(GraphQLField):
    field: PaymentMethodInitializeTokenizationErrorGraphQLField = (
        PaymentMethodInitializeTokenizationErrorGraphQLField("field")
    )
    message: PaymentMethodInitializeTokenizationErrorGraphQLField = (
        PaymentMethodInitializeTokenizationErrorGraphQLField("message")
    )
    code: PaymentMethodInitializeTokenizationErrorGraphQLField = (
        PaymentMethodInitializeTokenizationErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: PaymentMethodInitializeTokenizationErrorGraphQLField
    ) -> "PaymentMethodInitializeTokenizationErrorFields":
        self._subfields.extend(subfields)
        return self


class StaffDeleteFields(GraphQLField):
    @classmethod
    def staff_errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("staff_errors")

    @classmethod
    def errors(cls) -> "StaffErrorFields":
        return StaffErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[StaffDeleteGraphQLField, "UserFields", "StaffErrorFields"]
    ) -> "StaffDeleteFields":
        self._subfields.extend(subfields)
        return self


class MarginFields(GraphQLField):
    start: MarginGraphQLField = MarginGraphQLField("start")
    stop: MarginGraphQLField = MarginGraphQLField("stop")

    def fields(self, *subfields: MarginGraphQLField) -> "MarginFields":
        self._subfields.extend(subfields)
        return self


class LimitsFields(GraphQLField):
    channels: LimitsGraphQLField = LimitsGraphQLField("channels")
    orders: LimitsGraphQLField = LimitsGraphQLField("orders")
    product_variants: LimitsGraphQLField = LimitsGraphQLField("productVariants")
    staff_users: LimitsGraphQLField = LimitsGraphQLField("staffUsers")
    warehouses: LimitsGraphQLField = LimitsGraphQLField("warehouses")

    def fields(self, *subfields: LimitsGraphQLField) -> "LimitsFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneDeleteFields(GraphQLField):
    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    @classmethod
    def shipping_zone(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("shipping_zone")

    def fields(
        self,
        *subfields: Union[
            ShippingZoneDeleteGraphQLField, "ShippingZoneFields", "ShippingErrorFields"
        ]
    ) -> "ShippingZoneDeleteFields":
        self._subfields.extend(subfields)
        return self


class MenuBulkDeleteFields(GraphQLField):
    count: MenuBulkDeleteGraphQLField = MenuBulkDeleteGraphQLField("count")

    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    def fields(
        self, *subfields: Union[MenuBulkDeleteGraphQLField, "MenuErrorFields"]
    ) -> "MenuBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class GiftCardFields(GraphQLField):
    id: GiftCardGraphQLField = GiftCardGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: GiftCardGraphQLField = GiftCardGraphQLField("privateMetafield")
    private_metafields: GiftCardGraphQLField = GiftCardGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: GiftCardGraphQLField = GiftCardGraphQLField("metafield")
    metafields: GiftCardGraphQLField = GiftCardGraphQLField("metafields")
    display_code: GiftCardGraphQLField = GiftCardGraphQLField("displayCode")
    last_4_code_chars: GiftCardGraphQLField = GiftCardGraphQLField("last4CodeChars")
    code: GiftCardGraphQLField = GiftCardGraphQLField("code")
    created: GiftCardGraphQLField = GiftCardGraphQLField("created")

    @classmethod
    def created_by(cls) -> "UserFields":
        return UserFields("created_by")

    @classmethod
    def used_by(cls) -> "UserFields":
        return UserFields("used_by")

    created_by_email: GiftCardGraphQLField = GiftCardGraphQLField("createdByEmail")
    used_by_email: GiftCardGraphQLField = GiftCardGraphQLField("usedByEmail")
    last_used_on: GiftCardGraphQLField = GiftCardGraphQLField("lastUsedOn")
    expiry_date: GiftCardGraphQLField = GiftCardGraphQLField("expiryDate")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def events(cls) -> "GiftCardEventFields":
        return GiftCardEventFields("events")

    @classmethod
    def tags(cls) -> "GiftCardTagFields":
        return GiftCardTagFields("tags")

    bought_in_channel: GiftCardGraphQLField = GiftCardGraphQLField("boughtInChannel")
    is_active: GiftCardGraphQLField = GiftCardGraphQLField("isActive")

    @classmethod
    def initial_balance(cls) -> "MoneyFields":
        return MoneyFields("initial_balance")

    @classmethod
    def current_balance(cls) -> "MoneyFields":
        return MoneyFields("current_balance")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    end_date: GiftCardGraphQLField = GiftCardGraphQLField("endDate")
    start_date: GiftCardGraphQLField = GiftCardGraphQLField("startDate")

    def fields(
        self,
        *subfields: Union[
            GiftCardGraphQLField,
            "UserFields",
            "MetadataItemFields",
            "AppFields",
            "GiftCardEventFields",
            "GiftCardTagFields",
            "MoneyFields",
            "ProductFields",
        ]
    ) -> "GiftCardFields":
        self._subfields.extend(subfields)
        return self


class CheckoutBillingAddressUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutBillingAddressUpdateGraphQLField,
            "CheckoutErrorFields",
            "CheckoutFields",
        ]
    ) -> "CheckoutBillingAddressUpdateFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "ShippingZoneCountableEdgeFields":
        return ShippingZoneCountableEdgeFields("edges")

    total_count: ShippingZoneCountableConnectionGraphQLField = (
        ShippingZoneCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            ShippingZoneCountableConnectionGraphQLField,
            "ShippingZoneCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "ShippingZoneCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodTypeFields(GraphQLField):
    id: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField(
        "privateMetafield"
    )
    private_metafields: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField(
        "metafield"
    )
    metafields: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField(
        "metafields"
    )
    name: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField("name")
    description: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField(
        "description"
    )
    type: ShippingMethodTypeGraphQLField = ShippingMethodTypeGraphQLField("type")

    @classmethod
    def translation(cls) -> "ShippingMethodTranslationFields":
        return ShippingMethodTranslationFields("translation")

    @classmethod
    def channel_listings(cls) -> "ShippingMethodChannelListingFields":
        return ShippingMethodChannelListingFields("channel_listings")

    @classmethod
    def maximum_order_price(cls) -> "MoneyFields":
        return MoneyFields("maximum_order_price")

    @classmethod
    def minimum_order_price(cls) -> "MoneyFields":
        return MoneyFields("minimum_order_price")

    @classmethod
    def postal_code_rules(cls) -> "ShippingMethodPostalCodeRuleFields":
        return ShippingMethodPostalCodeRuleFields("postal_code_rules")

    @classmethod
    def excluded_products(cls) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields("excluded_products")

    @classmethod
    def minimum_order_weight(cls) -> "WeightFields":
        return WeightFields("minimum_order_weight")

    @classmethod
    def maximum_order_weight(cls) -> "WeightFields":
        return WeightFields("maximum_order_weight")

    maximum_delivery_days: ShippingMethodTypeGraphQLField = (
        ShippingMethodTypeGraphQLField("maximumDeliveryDays")
    )
    minimum_delivery_days: ShippingMethodTypeGraphQLField = (
        ShippingMethodTypeGraphQLField("minimumDeliveryDays")
    )

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    def fields(
        self,
        *subfields: Union[
            ShippingMethodTypeGraphQLField,
            "ShippingMethodChannelListingFields",
            "WeightFields",
            "MetadataItemFields",
            "ShippingMethodTranslationFields",
            "ProductCountableConnectionFields",
            "ShippingMethodPostalCodeRuleFields",
            "MoneyFields",
            "TaxClassFields",
        ]
    ) -> "ShippingMethodTypeFields":
        self._subfields.extend(subfields)
        return self


class PageReorderAttributeValuesFields(GraphQLField):
    @classmethod
    def page(cls) -> "PageFields":
        return PageFields("page")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PageReorderAttributeValuesGraphQLField, "PageErrorFields", "PageFields"
        ]
    ) -> "PageReorderAttributeValuesFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneBulkDeleteFields(GraphQLField):
    count: ShippingZoneBulkDeleteGraphQLField = ShippingZoneBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[ShippingZoneBulkDeleteGraphQLField, "ShippingErrorFields"]
    ) -> "ShippingZoneBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class PreorderDataFields(GraphQLField):
    global_threshold: PreorderDataGraphQLField = PreorderDataGraphQLField(
        "globalThreshold"
    )
    global_sold_units: PreorderDataGraphQLField = PreorderDataGraphQLField(
        "globalSoldUnits"
    )
    end_date: PreorderDataGraphQLField = PreorderDataGraphQLField("endDate")

    def fields(self, *subfields: PreorderDataGraphQLField) -> "PreorderDataFields":
        self._subfields.extend(subfields)
        return self


class SaleCreateFields(GraphQLField):
    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    def fields(
        self,
        *subfields: Union[SaleCreateGraphQLField, "SaleFields", "DiscountErrorFields"]
    ) -> "SaleCreateFields":
        self._subfields.extend(subfields)
        return self


class SetPasswordFields(GraphQLField):
    token: SetPasswordGraphQLField = SetPasswordGraphQLField("token")
    refresh_token: SetPasswordGraphQLField = SetPasswordGraphQLField("refreshToken")
    csrf_token: SetPasswordGraphQLField = SetPasswordGraphQLField("csrfToken")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[SetPasswordGraphQLField, "AccountErrorFields", "UserFields"]
    ) -> "SetPasswordFields":
        self._subfields.extend(subfields)
        return self


class PaymentSettingsFields(GraphQLField):
    default_transaction_flow_strategy: PaymentSettingsGraphQLField = (
        PaymentSettingsGraphQLField("defaultTransactionFlowStrategy")
    )

    def fields(
        self, *subfields: PaymentSettingsGraphQLField
    ) -> "PaymentSettingsFields":
        self._subfields.extend(subfields)
        return self


class WarehouseShippingZoneUnassignFields(GraphQLField):
    @classmethod
    def warehouse_errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("warehouse_errors")

    @classmethod
    def errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("errors")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    def fields(
        self,
        *subfields: Union[
            WarehouseShippingZoneUnassignGraphQLField,
            "WarehouseFields",
            "WarehouseErrorFields",
        ]
    ) -> "WarehouseShippingZoneUnassignFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "AttributeValueFields":
        return AttributeValueFields("node")

    cursor: AttributeValueCountableEdgeGraphQLField = (
        AttributeValueCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[
            AttributeValueCountableEdgeGraphQLField, "AttributeValueFields"
        ]
    ) -> "AttributeValueCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class PromotionEndedEventFields(GraphQLField):
    id: PromotionEndedEventGraphQLField = PromotionEndedEventGraphQLField("id")
    date: PromotionEndedEventGraphQLField = PromotionEndedEventGraphQLField("date")
    type: PromotionEndedEventGraphQLField = PromotionEndedEventGraphQLField("type")
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")

    def fields(
        self, *subfields: Union[PromotionEndedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionEndedEventFields":
        self._subfields.extend(subfields)
        return self


class OrderCaptureFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[OrderCaptureGraphQLField, "OrderErrorFields", "OrderFields"]
    ) -> "OrderCaptureFields":
        self._subfields.extend(subfields)
        return self


class InvoiceDeleteFields(GraphQLField):
    @classmethod
    def invoice_errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("invoice_errors")

    @classmethod
    def errors(cls) -> "InvoiceErrorFields":
        return InvoiceErrorFields("errors")

    @classmethod
    def invoice(cls) -> "InvoiceFields":
        return InvoiceFields("invoice")

    def fields(
        self,
        *subfields: Union[
            InvoiceDeleteGraphQLField, "InvoiceErrorFields", "InvoiceFields"
        ]
    ) -> "InvoiceDeleteFields":
        self._subfields.extend(subfields)
        return self


class GatewayConfigLineFields(GraphQLField):
    field: GatewayConfigLineGraphQLField = GatewayConfigLineGraphQLField("field")
    value: GatewayConfigLineGraphQLField = GatewayConfigLineGraphQLField("value")

    def fields(
        self, *subfields: GatewayConfigLineGraphQLField
    ) -> "GatewayConfigLineFields":
        self._subfields.extend(subfields)
        return self


class AccountAddressCreateFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    def fields(
        self,
        *subfields: Union[
            AccountAddressCreateGraphQLField,
            "AccountErrorFields",
            "UserFields",
            "AddressFields",
        ]
    ) -> "AccountAddressCreateFields":
        self._subfields.extend(subfields)
        return self


class TaxCountryConfigurationFields(GraphQLField):
    @classmethod
    def country(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("country")

    @classmethod
    def tax_class_country_rates(cls) -> "TaxClassCountryRateFields":
        return TaxClassCountryRateFields("tax_class_country_rates")

    def fields(
        self,
        *subfields: Union[
            TaxCountryConfigurationGraphQLField,
            "CountryDisplayFields",
            "TaxClassCountryRateFields",
        ]
    ) -> "TaxCountryConfigurationFields":
        self._subfields.extend(subfields)
        return self


class PluginUpdateFields(GraphQLField):
    @classmethod
    def plugin(cls) -> "PluginFields":
        return PluginFields("plugin")

    @classmethod
    def plugins_errors(cls) -> "PluginErrorFields":
        return PluginErrorFields("plugins_errors")

    @classmethod
    def errors(cls) -> "PluginErrorFields":
        return PluginErrorFields("errors")

    def fields(
        self,
        *subfields: Union[PluginUpdateGraphQLField, "PluginFields", "PluginErrorFields"]
    ) -> "PluginUpdateFields":
        self._subfields.extend(subfields)
        return self


class ChoiceValueFields(GraphQLField):
    raw: ChoiceValueGraphQLField = ChoiceValueGraphQLField("raw")
    verbose: ChoiceValueGraphQLField = ChoiceValueGraphQLField("verbose")

    def fields(self, *subfields: ChoiceValueGraphQLField) -> "ChoiceValueFields":
        self._subfields.extend(subfields)
        return self


class StaffNotificationRecipientDeleteFields(GraphQLField):
    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    @classmethod
    def staff_notification_recipient(cls) -> "StaffNotificationRecipientFields":
        return StaffNotificationRecipientFields("staff_notification_recipient")

    def fields(
        self,
        *subfields: Union[
            StaffNotificationRecipientDeleteGraphQLField,
            "StaffNotificationRecipientFields",
            "ShopErrorFields",
        ]
    ) -> "StaffNotificationRecipientDeleteFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodTranslatableContentFields(GraphQLField):
    id: ShippingMethodTranslatableContentGraphQLField = (
        ShippingMethodTranslatableContentGraphQLField("id")
    )
    shipping_method_id: ShippingMethodTranslatableContentGraphQLField = (
        ShippingMethodTranslatableContentGraphQLField("shippingMethodId")
    )
    name: ShippingMethodTranslatableContentGraphQLField = (
        ShippingMethodTranslatableContentGraphQLField("name")
    )
    description: ShippingMethodTranslatableContentGraphQLField = (
        ShippingMethodTranslatableContentGraphQLField("description")
    )

    @classmethod
    def translation(cls) -> "ShippingMethodTranslationFields":
        return ShippingMethodTranslationFields("translation")

    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    def fields(
        self,
        *subfields: Union[
            ShippingMethodTranslatableContentGraphQLField,
            "ShippingMethodTranslationFields",
            "ShippingMethodTypeFields",
        ]
    ) -> "ShippingMethodTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class OrderBulkCreateResultFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def errors(cls) -> "OrderBulkCreateErrorFields":
        return OrderBulkCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderBulkCreateResultGraphQLField,
            "OrderBulkCreateErrorFields",
            "OrderFields",
        ]
    ) -> "OrderBulkCreateResultFields":
        self._subfields.extend(subfields)
        return self


class OrderMarkAsPaidFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderMarkAsPaidGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "OrderMarkAsPaidFields":
        self._subfields.extend(subfields)
        return self


class ProductFields(GraphQLField):
    id: ProductGraphQLField = ProductGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ProductGraphQLField = ProductGraphQLField("privateMetafield")
    private_metafields: ProductGraphQLField = ProductGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ProductGraphQLField = ProductGraphQLField("metafield")
    metafields: ProductGraphQLField = ProductGraphQLField("metafields")
    seo_title: ProductGraphQLField = ProductGraphQLField("seoTitle")
    seo_description: ProductGraphQLField = ProductGraphQLField("seoDescription")
    name: ProductGraphQLField = ProductGraphQLField("name")
    description: ProductGraphQLField = ProductGraphQLField("description")

    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    slug: ProductGraphQLField = ProductGraphQLField("slug")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    created: ProductGraphQLField = ProductGraphQLField("created")
    updated_at: ProductGraphQLField = ProductGraphQLField("updatedAt")
    charge_taxes: ProductGraphQLField = ProductGraphQLField("chargeTaxes")

    @classmethod
    def weight(cls) -> "WeightFields":
        return WeightFields("weight")

    @classmethod
    def default_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("default_variant")

    rating: ProductGraphQLField = ProductGraphQLField("rating")
    channel: ProductGraphQLField = ProductGraphQLField("channel")
    description_json: ProductGraphQLField = ProductGraphQLField("descriptionJson")

    @classmethod
    def thumbnail(cls) -> "ImageFields":
        return ImageFields("thumbnail")

    @classmethod
    def pricing(cls) -> "ProductPricingInfoFields":
        return ProductPricingInfoFields("pricing")

    is_available: ProductGraphQLField = ProductGraphQLField("isAvailable")

    @classmethod
    def tax_type(cls) -> "TaxTypeFields":
        return TaxTypeFields("tax_type")

    @classmethod
    def attribute(cls) -> "SelectedAttributeFields":
        return SelectedAttributeFields("attribute")

    @classmethod
    def attributes(cls) -> "SelectedAttributeFields":
        return SelectedAttributeFields("attributes")

    @classmethod
    def channel_listings(cls) -> "ProductChannelListingFields":
        return ProductChannelListingFields("channel_listings")

    @classmethod
    def media_by_id(cls) -> "ProductMediaFields":
        return ProductMediaFields("media_by_id")

    @classmethod
    def image_by_id(cls) -> "ProductImageFields":
        return ProductImageFields("image_by_id")

    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    @classmethod
    def variants(cls) -> "ProductVariantFields":
        return ProductVariantFields("variants")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def images(cls) -> "ProductImageFields":
        return ProductImageFields("images")

    @classmethod
    def collections(cls) -> "CollectionFields":
        return CollectionFields("collections")

    @classmethod
    def translation(cls) -> "ProductTranslationFields":
        return ProductTranslationFields("translation")

    available_for_purchase: ProductGraphQLField = ProductGraphQLField(
        "availableForPurchase"
    )
    available_for_purchase_at: ProductGraphQLField = ProductGraphQLField(
        "availableForPurchaseAt"
    )
    is_available_for_purchase: ProductGraphQLField = ProductGraphQLField(
        "isAvailableForPurchase"
    )

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    external_reference: ProductGraphQLField = ProductGraphQLField("externalReference")

    def fields(
        self,
        *subfields: Union[
            ProductGraphQLField,
            "SelectedAttributeFields",
            "WeightFields",
            "MetadataItemFields",
            "ProductPricingInfoFields",
            "ProductMediaFields",
            "CollectionFields",
            "ProductVariantFields",
            "CategoryFields",
            "ImageFields",
            "ProductImageFields",
            "TaxClassFields",
            "ProductTypeFields",
            "TaxTypeFields",
            "ProductChannelListingFields",
            "ProductTranslationFields",
        ]
    ) -> "ProductFields":
        self._subfields.extend(subfields)
        return self


class CollectionChannelListingErrorFields(GraphQLField):
    field: CollectionChannelListingErrorGraphQLField = (
        CollectionChannelListingErrorGraphQLField("field")
    )
    message: CollectionChannelListingErrorGraphQLField = (
        CollectionChannelListingErrorGraphQLField("message")
    )
    code: CollectionChannelListingErrorGraphQLField = (
        CollectionChannelListingErrorGraphQLField("code")
    )
    attributes: CollectionChannelListingErrorGraphQLField = (
        CollectionChannelListingErrorGraphQLField("attributes")
    )
    values: CollectionChannelListingErrorGraphQLField = (
        CollectionChannelListingErrorGraphQLField("values")
    )
    channels: CollectionChannelListingErrorGraphQLField = (
        CollectionChannelListingErrorGraphQLField("channels")
    )

    def fields(
        self, *subfields: CollectionChannelListingErrorGraphQLField
    ) -> "CollectionChannelListingErrorFields":
        self._subfields.extend(subfields)
        return self


class ExportFileFields(GraphQLField):
    id: ExportFileGraphQLField = ExportFileGraphQLField("id")
    status: ExportFileGraphQLField = ExportFileGraphQLField("status")
    created_at: ExportFileGraphQLField = ExportFileGraphQLField("createdAt")
    updated_at: ExportFileGraphQLField = ExportFileGraphQLField("updatedAt")
    message: ExportFileGraphQLField = ExportFileGraphQLField("message")
    url: ExportFileGraphQLField = ExportFileGraphQLField("url")

    @classmethod
    def events(cls) -> "ExportEventFields":
        return ExportEventFields("events")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    def fields(
        self,
        *subfields: Union[
            ExportFileGraphQLField, "ExportEventFields", "AppFields", "UserFields"
        ]
    ) -> "ExportFileFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleTranslationFields(GraphQLField):
    id: PromotionRuleTranslationGraphQLField = PromotionRuleTranslationGraphQLField(
        "id"
    )

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: PromotionRuleTranslationGraphQLField = PromotionRuleTranslationGraphQLField(
        "name"
    )
    description: PromotionRuleTranslationGraphQLField = (
        PromotionRuleTranslationGraphQLField("description")
    )

    @classmethod
    def translatable_content(cls) -> "PromotionRuleTranslatableContentFields":
        return PromotionRuleTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleTranslationGraphQLField,
            "PromotionRuleTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "PromotionRuleTranslationFields":
        self._subfields.extend(subfields)
        return self


class StaffNotificationRecipientCreateFields(GraphQLField):
    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    @classmethod
    def staff_notification_recipient(cls) -> "StaffNotificationRecipientFields":
        return StaffNotificationRecipientFields("staff_notification_recipient")

    def fields(
        self,
        *subfields: Union[
            StaffNotificationRecipientCreateGraphQLField,
            "StaffNotificationRecipientFields",
            "ShopErrorFields",
        ]
    ) -> "StaffNotificationRecipientCreateFields":
        self._subfields.extend(subfields)
        return self


class TaxCountryConfigurationUpdateErrorFields(GraphQLField):
    field: TaxCountryConfigurationUpdateErrorGraphQLField = (
        TaxCountryConfigurationUpdateErrorGraphQLField("field")
    )
    message: TaxCountryConfigurationUpdateErrorGraphQLField = (
        TaxCountryConfigurationUpdateErrorGraphQLField("message")
    )
    code: TaxCountryConfigurationUpdateErrorGraphQLField = (
        TaxCountryConfigurationUpdateErrorGraphQLField("code")
    )
    tax_class_ids: TaxCountryConfigurationUpdateErrorGraphQLField = (
        TaxCountryConfigurationUpdateErrorGraphQLField("taxClassIds")
    )

    def fields(
        self, *subfields: TaxCountryConfigurationUpdateErrorGraphQLField
    ) -> "TaxCountryConfigurationUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantFields(GraphQLField):
    id: ProductVariantGraphQLField = ProductVariantGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ProductVariantGraphQLField = ProductVariantGraphQLField(
        "privateMetafield"
    )
    private_metafields: ProductVariantGraphQLField = ProductVariantGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ProductVariantGraphQLField = ProductVariantGraphQLField("metafield")
    metafields: ProductVariantGraphQLField = ProductVariantGraphQLField("metafields")
    name: ProductVariantGraphQLField = ProductVariantGraphQLField("name")
    sku: ProductVariantGraphQLField = ProductVariantGraphQLField("sku")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    track_inventory: ProductVariantGraphQLField = ProductVariantGraphQLField(
        "trackInventory"
    )
    quantity_limit_per_customer: ProductVariantGraphQLField = (
        ProductVariantGraphQLField("quantityLimitPerCustomer")
    )

    @classmethod
    def weight(cls) -> "WeightFields":
        return WeightFields("weight")

    channel: ProductVariantGraphQLField = ProductVariantGraphQLField("channel")

    @classmethod
    def channel_listings(cls) -> "ProductVariantChannelListingFields":
        return ProductVariantChannelListingFields("channel_listings")

    @classmethod
    def pricing(cls) -> "VariantPricingInfoFields":
        return VariantPricingInfoFields("pricing")

    @classmethod
    def attributes(cls) -> "SelectedAttributeFields":
        return SelectedAttributeFields("attributes")

    margin: ProductVariantGraphQLField = ProductVariantGraphQLField("margin")
    quantity_ordered: ProductVariantGraphQLField = ProductVariantGraphQLField(
        "quantityOrdered"
    )

    @classmethod
    def revenue(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("revenue")

    @classmethod
    def images(cls) -> "ProductImageFields":
        return ProductImageFields("images")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def translation(cls) -> "ProductVariantTranslationFields":
        return ProductVariantTranslationFields("translation")

    @classmethod
    def digital_content(cls) -> "DigitalContentFields":
        return DigitalContentFields("digital_content")

    @classmethod
    def stocks(cls) -> "StockFields":
        return StockFields("stocks")

    quantity_available: ProductVariantGraphQLField = ProductVariantGraphQLField(
        "quantityAvailable"
    )

    @classmethod
    def preorder(cls) -> "PreorderDataFields":
        return PreorderDataFields("preorder")

    created: ProductVariantGraphQLField = ProductVariantGraphQLField("created")
    updated_at: ProductVariantGraphQLField = ProductVariantGraphQLField("updatedAt")
    external_reference: ProductVariantGraphQLField = ProductVariantGraphQLField(
        "externalReference"
    )

    def fields(
        self,
        *subfields: Union[
            ProductVariantGraphQLField,
            "ProductVariantChannelListingFields",
            "DigitalContentFields",
            "StockFields",
            "TaxedMoneyFields",
            "WeightFields",
            "MetadataItemFields",
            "ProductMediaFields",
            "ProductVariantTranslationFields",
            "ProductFields",
            "ProductImageFields",
            "VariantPricingInfoFields",
            "SelectedAttributeFields",
            "PreorderDataFields",
        ]
    ) -> "ProductVariantFields":
        self._subfields.extend(subfields)
        return self


class CountryDisplayFields(GraphQLField):
    code: CountryDisplayGraphQLField = CountryDisplayGraphQLField("code")
    country: CountryDisplayGraphQLField = CountryDisplayGraphQLField("country")

    @classmethod
    def vat(cls) -> "VATFields":
        return VATFields("vat")

    def fields(
        self, *subfields: Union[CountryDisplayGraphQLField, "VATFields"]
    ) -> "CountryDisplayFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayConfigFields(GraphQLField):
    id: PaymentGatewayConfigGraphQLField = PaymentGatewayConfigGraphQLField("id")
    data: PaymentGatewayConfigGraphQLField = PaymentGatewayConfigGraphQLField("data")

    @classmethod
    def errors(cls) -> "PaymentGatewayConfigErrorFields":
        return PaymentGatewayConfigErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentGatewayConfigGraphQLField, "PaymentGatewayConfigErrorFields"
        ]
    ) -> "PaymentGatewayConfigFields":
        self._subfields.extend(subfields)
        return self


class PromotionUpdatedEventFields(GraphQLField):
    id: PromotionUpdatedEventGraphQLField = PromotionUpdatedEventGraphQLField("id")
    date: PromotionUpdatedEventGraphQLField = PromotionUpdatedEventGraphQLField("date")
    type: PromotionUpdatedEventGraphQLField = PromotionUpdatedEventGraphQLField("type")
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")

    def fields(
        self, *subfields: Union[PromotionUpdatedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionUpdatedEventFields":
        self._subfields.extend(subfields)
        return self


class TaxedMoneyRangeFields(GraphQLField):
    @classmethod
    def start(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("start")

    @classmethod
    def stop(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("stop")

    def fields(
        self, *subfields: Union[TaxedMoneyRangeGraphQLField, "TaxedMoneyFields"]
    ) -> "TaxedMoneyRangeFields":
        self._subfields.extend(subfields)
        return self


class CustomerCreateFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[
            CustomerCreateGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "CustomerCreateFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantRefundCreateLineErrorFields(GraphQLField):
    field: OrderGrantRefundCreateLineErrorGraphQLField = (
        OrderGrantRefundCreateLineErrorGraphQLField("field")
    )
    message: OrderGrantRefundCreateLineErrorGraphQLField = (
        OrderGrantRefundCreateLineErrorGraphQLField("message")
    )
    code: OrderGrantRefundCreateLineErrorGraphQLField = (
        OrderGrantRefundCreateLineErrorGraphQLField("code")
    )
    line_id: OrderGrantRefundCreateLineErrorGraphQLField = (
        OrderGrantRefundCreateLineErrorGraphQLField("lineId")
    )

    def fields(
        self, *subfields: OrderGrantRefundCreateLineErrorGraphQLField
    ) -> "OrderGrantRefundCreateLineErrorFields":
        self._subfields.extend(subfields)
        return self


class ExternalNotificationTriggerFields(GraphQLField):
    @classmethod
    def errors(cls) -> "ExternalNotificationErrorFields":
        return ExternalNotificationErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExternalNotificationTriggerGraphQLField, "ExternalNotificationErrorFields"
        ]
    ) -> "ExternalNotificationTriggerFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryFields(GraphQLField):
    id: EventDeliveryGraphQLField = EventDeliveryGraphQLField("id")
    created_at: EventDeliveryGraphQLField = EventDeliveryGraphQLField("createdAt")
    status: EventDeliveryGraphQLField = EventDeliveryGraphQLField("status")
    event_type: EventDeliveryGraphQLField = EventDeliveryGraphQLField("eventType")

    @classmethod
    def attempts(cls) -> "EventDeliveryAttemptCountableConnectionFields":
        return EventDeliveryAttemptCountableConnectionFields("attempts")

    payload: EventDeliveryGraphQLField = EventDeliveryGraphQLField("payload")

    def fields(
        self,
        *subfields: Union[
            EventDeliveryGraphQLField, "EventDeliveryAttemptCountableConnectionFields"
        ]
    ) -> "EventDeliveryFields":
        self._subfields.extend(subfields)
        return self


class VoucherCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "VoucherFields":
        return VoucherFields("node")

    cursor: VoucherCountableEdgeGraphQLField = VoucherCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[VoucherCountableEdgeGraphQLField, "VoucherFields"]
    ) -> "VoucherCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class OrderLineDiscountUpdateFields(GraphQLField):
    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderLineDiscountUpdateGraphQLField,
            "OrderErrorFields",
            "OrderFields",
            "OrderLineFields",
        ]
    ) -> "OrderLineDiscountUpdateFields":
        self._subfields.extend(subfields)
        return self


class PageTypeReorderAttributesFields(GraphQLField):
    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PageTypeReorderAttributesGraphQLField, "PageTypeFields", "PageErrorFields"
        ]
    ) -> "PageTypeReorderAttributesFields":
        self._subfields.extend(subfields)
        return self


class ExportVoucherCodesFields(GraphQLField):
    @classmethod
    def export_file(cls) -> "ExportFileFields":
        return ExportFileFields("export_file")

    @classmethod
    def errors(cls) -> "ExportErrorFields":
        return ExportErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExportVoucherCodesGraphQLField, "ExportFileFields", "ExportErrorFields"
        ]
    ) -> "ExportVoucherCodesFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkDeleteFields(GraphQLField):
    count: ProductBulkDeleteGraphQLField = ProductBulkDeleteGraphQLField("count")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self, *subfields: Union[ProductBulkDeleteGraphQLField, "ProductErrorFields"]
    ) -> "ProductBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class TaxTypeFields(GraphQLField):
    description: TaxTypeGraphQLField = TaxTypeGraphQLField("description")
    tax_code: TaxTypeGraphQLField = TaxTypeGraphQLField("taxCode")

    def fields(self, *subfields: TaxTypeGraphQLField) -> "TaxTypeFields":
        self._subfields.extend(subfields)
        return self


class TransactionInitializeErrorFields(GraphQLField):
    field: TransactionInitializeErrorGraphQLField = (
        TransactionInitializeErrorGraphQLField("field")
    )
    message: TransactionInitializeErrorGraphQLField = (
        TransactionInitializeErrorGraphQLField("message")
    )
    code: TransactionInitializeErrorGraphQLField = (
        TransactionInitializeErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: TransactionInitializeErrorGraphQLField
    ) -> "TransactionInitializeErrorFields":
        self._subfields.extend(subfields)
        return self


class VariantPricingInfoFields(GraphQLField):
    on_sale: VariantPricingInfoGraphQLField = VariantPricingInfoGraphQLField("onSale")

    @classmethod
    def discount(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("discount")

    @classmethod
    def discount_local_currency(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("discount_local_currency")

    @classmethod
    def price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("price")

    @classmethod
    def price_undiscounted(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("price_undiscounted")

    @classmethod
    def price_local_currency(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("price_local_currency")

    def fields(
        self, *subfields: Union[VariantPricingInfoGraphQLField, "TaxedMoneyFields"]
    ) -> "VariantPricingInfoFields":
        self._subfields.extend(subfields)
        return self


class TransactionProcessFields(GraphQLField):
    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def transaction_event(cls) -> "TransactionEventFields":
        return TransactionEventFields("transaction_event")

    data: TransactionProcessGraphQLField = TransactionProcessGraphQLField("data")

    @classmethod
    def errors(cls) -> "TransactionProcessErrorFields":
        return TransactionProcessErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionProcessGraphQLField,
            "TransactionItemFields",
            "TransactionProcessErrorFields",
            "TransactionEventFields",
        ]
    ) -> "TransactionProcessFields":
        self._subfields.extend(subfields)
        return self


class AppTokenDeleteFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app_token(cls) -> "AppTokenFields":
        return AppTokenFields("app_token")

    def fields(
        self,
        *subfields: Union[
            AppTokenDeleteGraphQLField, "AppErrorFields", "AppTokenFields"
        ]
    ) -> "AppTokenDeleteFields":
        self._subfields.extend(subfields)
        return self


class VerifyTokenFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    is_valid: VerifyTokenGraphQLField = VerifyTokenGraphQLField("isValid")
    payload: VerifyTokenGraphQLField = VerifyTokenGraphQLField("payload")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[VerifyTokenGraphQLField, "AccountErrorFields", "UserFields"]
    ) -> "VerifyTokenFields":
        self._subfields.extend(subfields)
        return self


class OrderDiscountUpdateFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderDiscountUpdateGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "OrderDiscountUpdateFields":
        self._subfields.extend(subfields)
        return self


class CollectionBulkDeleteFields(GraphQLField):
    count: CollectionBulkDeleteGraphQLField = CollectionBulkDeleteGraphQLField("count")

    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    def fields(
        self,
        *subfields: Union[CollectionBulkDeleteGraphQLField, "CollectionErrorFields"]
    ) -> "CollectionBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class CollectionDeleteFields(GraphQLField):
    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    def fields(
        self,
        *subfields: Union[
            CollectionDeleteGraphQLField, "CollectionFields", "CollectionErrorFields"
        ]
    ) -> "CollectionDeleteFields":
        self._subfields.extend(subfields)
        return self


class PermissionGroupDeleteFields(GraphQLField):
    @classmethod
    def permission_group_errors(cls) -> "PermissionGroupErrorFields":
        return PermissionGroupErrorFields("permission_group_errors")

    @classmethod
    def errors(cls) -> "PermissionGroupErrorFields":
        return PermissionGroupErrorFields("errors")

    @classmethod
    def group(cls) -> "GroupFields":
        return GroupFields("group")

    def fields(
        self,
        *subfields: Union[
            PermissionGroupDeleteGraphQLField,
            "PermissionGroupErrorFields",
            "GroupFields",
        ]
    ) -> "PermissionGroupDeleteFields":
        self._subfields.extend(subfields)
        return self


class WarehouseDeleteFields(GraphQLField):
    @classmethod
    def warehouse_errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("warehouse_errors")

    @classmethod
    def errors(cls) -> "WarehouseErrorFields":
        return WarehouseErrorFields("errors")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    def fields(
        self,
        *subfields: Union[
            WarehouseDeleteGraphQLField, "WarehouseFields", "WarehouseErrorFields"
        ]
    ) -> "WarehouseDeleteFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLanguageCodeUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutLanguageCodeUpdateGraphQLField,
            "CheckoutErrorFields",
            "CheckoutFields",
        ]
    ) -> "CheckoutLanguageCodeUpdateFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayFields(GraphQLField):
    name: PaymentGatewayGraphQLField = PaymentGatewayGraphQLField("name")
    id: PaymentGatewayGraphQLField = PaymentGatewayGraphQLField("id")

    @classmethod
    def config(cls) -> "GatewayConfigLineFields":
        return GatewayConfigLineFields("config")

    currencies: PaymentGatewayGraphQLField = PaymentGatewayGraphQLField("currencies")

    def fields(
        self, *subfields: Union[PaymentGatewayGraphQLField, "GatewayConfigLineFields"]
    ) -> "PaymentGatewayFields":
        self._subfields.extend(subfields)
        return self


class ProductAttributeAssignFields(GraphQLField):
    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductAttributeAssignGraphQLField,
            "ProductTypeFields",
            "ProductErrorFields",
        ]
    ) -> "ProductAttributeAssignFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleUpdateErrorFields(GraphQLField):
    field: PromotionRuleUpdateErrorGraphQLField = PromotionRuleUpdateErrorGraphQLField(
        "field"
    )
    message: PromotionRuleUpdateErrorGraphQLField = (
        PromotionRuleUpdateErrorGraphQLField("message")
    )
    code: PromotionRuleUpdateErrorGraphQLField = PromotionRuleUpdateErrorGraphQLField(
        "code"
    )
    channels: PromotionRuleUpdateErrorGraphQLField = (
        PromotionRuleUpdateErrorGraphQLField("channels")
    )
    gifts_limit: PromotionRuleUpdateErrorGraphQLField = (
        PromotionRuleUpdateErrorGraphQLField("giftsLimit")
    )
    gifts_limit_exceed_by: PromotionRuleUpdateErrorGraphQLField = (
        PromotionRuleUpdateErrorGraphQLField("giftsLimitExceedBy")
    )

    def fields(
        self, *subfields: PromotionRuleUpdateErrorGraphQLField
    ) -> "PromotionRuleUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantRefundUpdateFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def granted_refund(cls) -> "OrderGrantedRefundFields":
        return OrderGrantedRefundFields("granted_refund")

    @classmethod
    def errors(cls) -> "OrderGrantRefundUpdateErrorFields":
        return OrderGrantRefundUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderGrantRefundUpdateGraphQLField,
            "OrderGrantRefundUpdateErrorFields",
            "OrderGrantedRefundFields",
            "OrderFields",
        ]
    ) -> "OrderGrantRefundUpdateFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleUpdatedEventFields(GraphQLField):
    id: PromotionRuleUpdatedEventGraphQLField = PromotionRuleUpdatedEventGraphQLField(
        "id"
    )
    date: PromotionRuleUpdatedEventGraphQLField = PromotionRuleUpdatedEventGraphQLField(
        "date"
    )
    type: PromotionRuleUpdatedEventGraphQLField = PromotionRuleUpdatedEventGraphQLField(
        "type"
    )
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")
    rule_id: PromotionRuleUpdatedEventGraphQLField = (
        PromotionRuleUpdatedEventGraphQLField("ruleId")
    )

    def fields(
        self, *subfields: Union[PromotionRuleUpdatedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionRuleUpdatedEventFields":
        self._subfields.extend(subfields)
        return self


class TransactionCreateErrorFields(GraphQLField):
    field: TransactionCreateErrorGraphQLField = TransactionCreateErrorGraphQLField(
        "field"
    )
    message: TransactionCreateErrorGraphQLField = TransactionCreateErrorGraphQLField(
        "message"
    )
    code: TransactionCreateErrorGraphQLField = TransactionCreateErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: TransactionCreateErrorGraphQLField
    ) -> "TransactionCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class StockCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "StockCountableEdgeFields":
        return StockCountableEdgeFields("edges")

    total_count: StockCountableConnectionGraphQLField = (
        StockCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            StockCountableConnectionGraphQLField,
            "StockCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "StockCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class GiftCardActivateFields(GraphQLField):
    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    @classmethod
    def gift_card_errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("gift_card_errors")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            GiftCardActivateGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardActivateFields":
        self._subfields.extend(subfields)
        return self


class CheckoutFields(GraphQLField):
    id: CheckoutGraphQLField = CheckoutGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: CheckoutGraphQLField = CheckoutGraphQLField("privateMetafield")
    private_metafields: CheckoutGraphQLField = CheckoutGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: CheckoutGraphQLField = CheckoutGraphQLField("metafield")
    metafields: CheckoutGraphQLField = CheckoutGraphQLField("metafields")
    created: CheckoutGraphQLField = CheckoutGraphQLField("created")
    updated_at: CheckoutGraphQLField = CheckoutGraphQLField("updatedAt")
    last_change: CheckoutGraphQLField = CheckoutGraphQLField("lastChange")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def billing_address(cls) -> "AddressFields":
        return AddressFields("billing_address")

    @classmethod
    def shipping_address(cls) -> "AddressFields":
        return AddressFields("shipping_address")

    note: CheckoutGraphQLField = CheckoutGraphQLField("note")

    @classmethod
    def discount(cls) -> "MoneyFields":
        return MoneyFields("discount")

    discount_name: CheckoutGraphQLField = CheckoutGraphQLField("discountName")
    translated_discount_name: CheckoutGraphQLField = CheckoutGraphQLField(
        "translatedDiscountName"
    )

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    voucher_code: CheckoutGraphQLField = CheckoutGraphQLField("voucherCode")

    @classmethod
    def available_shipping_methods(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("available_shipping_methods")

    @classmethod
    def shipping_methods(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("shipping_methods")

    @classmethod
    def available_collection_points(cls) -> "WarehouseFields":
        return WarehouseFields("available_collection_points")

    @classmethod
    def available_payment_gateways(cls) -> "PaymentGatewayFields":
        return PaymentGatewayFields("available_payment_gateways")

    email: CheckoutGraphQLField = CheckoutGraphQLField("email")

    @classmethod
    def gift_cards(cls) -> "GiftCardFields":
        return GiftCardFields("gift_cards")

    is_shipping_required: CheckoutGraphQLField = CheckoutGraphQLField(
        "isShippingRequired"
    )
    quantity: CheckoutGraphQLField = CheckoutGraphQLField("quantity")
    stock_reservation_expires: CheckoutGraphQLField = CheckoutGraphQLField(
        "stockReservationExpires"
    )

    @classmethod
    def lines(cls) -> "CheckoutLineFields":
        return CheckoutLineFields("lines")

    @classmethod
    def shipping_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("shipping_price")

    @classmethod
    def shipping_method(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("shipping_method")

    delivery_method: DeliveryMethodUnion = DeliveryMethodUnion("deliveryMethod")

    @classmethod
    def subtotal_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("subtotal_price")

    tax_exemption: CheckoutGraphQLField = CheckoutGraphQLField("taxExemption")
    token: CheckoutGraphQLField = CheckoutGraphQLField("token")

    @classmethod
    def total_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("total_price")

    @classmethod
    def total_balance(cls) -> "MoneyFields":
        return MoneyFields("total_balance")

    language_code: CheckoutGraphQLField = CheckoutGraphQLField("languageCode")

    @classmethod
    def transactions(cls) -> "TransactionItemFields":
        return TransactionItemFields("transactions")

    display_gross_prices: CheckoutGraphQLField = CheckoutGraphQLField(
        "displayGrossPrices"
    )
    authorize_status: CheckoutGraphQLField = CheckoutGraphQLField("authorizeStatus")
    charge_status: CheckoutGraphQLField = CheckoutGraphQLField("chargeStatus")

    @classmethod
    def stored_payment_methods(cls) -> "StoredPaymentMethodFields":
        return StoredPaymentMethodFields("stored_payment_methods")

    problems: CheckoutProblemUnion = CheckoutProblemUnion("problems")

    def fields(
        self,
        *subfields: Union[
            CheckoutGraphQLField,
            "CheckoutLineFields",
            "UserFields",
            "TaxedMoneyFields",
            "TransactionItemFields",
            "MetadataItemFields",
            "VoucherFields",
            "ShippingMethodFields",
            "DeliveryMethodUnion",
            "ChannelFields",
            "PaymentGatewayFields",
            "StoredPaymentMethodFields",
            "MoneyFields",
            "GiftCardFields",
            "AddressFields",
            "WarehouseFields",
            "CheckoutProblemUnion",
        ]
    ) -> "CheckoutFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "EventDeliveryCountableEdgeFields":
        return EventDeliveryCountableEdgeFields("edges")

    total_count: EventDeliveryCountableConnectionGraphQLField = (
        EventDeliveryCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            EventDeliveryCountableConnectionGraphQLField,
            "EventDeliveryCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "EventDeliveryCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PageDeleteFields(GraphQLField):
    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    @classmethod
    def page(cls) -> "PageFields":
        return PageFields("page")

    def fields(
        self, *subfields: Union[PageDeleteGraphQLField, "PageErrorFields", "PageFields"]
    ) -> "PageDeleteFields":
        self._subfields.extend(subfields)
        return self


class WarehouseCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "WarehouseCountableEdgeFields":
        return WarehouseCountableEdgeFields("edges")

    total_count: WarehouseCountableConnectionGraphQLField = (
        WarehouseCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            WarehouseCountableConnectionGraphQLField,
            "WarehouseCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "WarehouseCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class SaleChannelListingFields(GraphQLField):
    id: SaleChannelListingGraphQLField = SaleChannelListingGraphQLField("id")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    discount_value: SaleChannelListingGraphQLField = SaleChannelListingGraphQLField(
        "discountValue"
    )
    currency: SaleChannelListingGraphQLField = SaleChannelListingGraphQLField(
        "currency"
    )

    def fields(
        self, *subfields: Union[SaleChannelListingGraphQLField, "ChannelFields"]
    ) -> "SaleChannelListingFields":
        self._subfields.extend(subfields)
        return self


class OrderConfirmFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[OrderConfirmGraphQLField, "OrderErrorFields", "OrderFields"]
    ) -> "OrderConfirmFields":
        self._subfields.extend(subfields)
        return self


class PromotionUpdateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "PromotionUpdateErrorFields":
        return PromotionUpdateErrorFields("errors")

    @classmethod
    def promotion(cls) -> "PromotionFields":
        return PromotionFields("promotion")

    def fields(
        self,
        *subfields: Union[
            PromotionUpdateGraphQLField, "PromotionFields", "PromotionUpdateErrorFields"
        ]
    ) -> "PromotionUpdateFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeReorderAttributesFields(GraphQLField):
    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductTypeReorderAttributesGraphQLField,
            "ProductTypeFields",
            "ProductErrorFields",
        ]
    ) -> "ProductTypeReorderAttributesFields":
        self._subfields.extend(subfields)
        return self


class CategoryCreateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    def fields(
        self,
        *subfields: Union[
            CategoryCreateGraphQLField, "ProductErrorFields", "CategoryFields"
        ]
    ) -> "CategoryCreateFields":
        self._subfields.extend(subfields)
        return self


class WarehouseErrorFields(GraphQLField):
    field: WarehouseErrorGraphQLField = WarehouseErrorGraphQLField("field")
    message: WarehouseErrorGraphQLField = WarehouseErrorGraphQLField("message")
    code: WarehouseErrorGraphQLField = WarehouseErrorGraphQLField("code")
    shipping_zones: WarehouseErrorGraphQLField = WarehouseErrorGraphQLField(
        "shippingZones"
    )

    def fields(self, *subfields: WarehouseErrorGraphQLField) -> "WarehouseErrorFields":
        self._subfields.extend(subfields)
        return self


class OrderEventCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "OrderEventCountableEdgeFields":
        return OrderEventCountableEdgeFields("edges")

    total_count: OrderEventCountableConnectionGraphQLField = (
        OrderEventCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            OrderEventCountableConnectionGraphQLField,
            "OrderEventCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "OrderEventCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class TransactionUpdateErrorFields(GraphQLField):
    field: TransactionUpdateErrorGraphQLField = TransactionUpdateErrorGraphQLField(
        "field"
    )
    message: TransactionUpdateErrorGraphQLField = TransactionUpdateErrorGraphQLField(
        "message"
    )
    code: TransactionUpdateErrorGraphQLField = TransactionUpdateErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: TransactionUpdateErrorGraphQLField
    ) -> "TransactionUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class CategoryUpdateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    def fields(
        self,
        *subfields: Union[
            CategoryUpdateGraphQLField, "ProductErrorFields", "CategoryFields"
        ]
    ) -> "CategoryUpdateFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneFields(GraphQLField):
    id: ShippingZoneGraphQLField = ShippingZoneGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ShippingZoneGraphQLField = ShippingZoneGraphQLField(
        "privateMetafield"
    )
    private_metafields: ShippingZoneGraphQLField = ShippingZoneGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ShippingZoneGraphQLField = ShippingZoneGraphQLField("metafield")
    metafields: ShippingZoneGraphQLField = ShippingZoneGraphQLField("metafields")
    name: ShippingZoneGraphQLField = ShippingZoneGraphQLField("name")
    default: ShippingZoneGraphQLField = ShippingZoneGraphQLField("default")

    @classmethod
    def price_range(cls) -> "MoneyRangeFields":
        return MoneyRangeFields("price_range")

    @classmethod
    def countries(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("countries")

    @classmethod
    def shipping_methods(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_methods")

    @classmethod
    def warehouses(cls) -> "WarehouseFields":
        return WarehouseFields("warehouses")

    @classmethod
    def channels(cls) -> "ChannelFields":
        return ChannelFields("channels")

    description: ShippingZoneGraphQLField = ShippingZoneGraphQLField("description")

    def fields(
        self,
        *subfields: Union[
            ShippingZoneGraphQLField,
            "MoneyRangeFields",
            "ShippingMethodTypeFields",
            "MetadataItemFields",
            "ChannelFields",
            "CountryDisplayFields",
            "WarehouseFields",
        ]
    ) -> "ShippingZoneFields":
        self._subfields.extend(subfields)
        return self


class PageBulkDeleteFields(GraphQLField):
    count: PageBulkDeleteGraphQLField = PageBulkDeleteGraphQLField("count")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self, *subfields: Union[PageBulkDeleteGraphQLField, "PageErrorFields"]
    ) -> "PageBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentFields(GraphQLField):
    id: DigitalContentGraphQLField = DigitalContentGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: DigitalContentGraphQLField = DigitalContentGraphQLField(
        "privateMetafield"
    )
    private_metafields: DigitalContentGraphQLField = DigitalContentGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: DigitalContentGraphQLField = DigitalContentGraphQLField("metafield")
    metafields: DigitalContentGraphQLField = DigitalContentGraphQLField("metafields")
    use_default_settings: DigitalContentGraphQLField = DigitalContentGraphQLField(
        "useDefaultSettings"
    )
    automatic_fulfillment: DigitalContentGraphQLField = DigitalContentGraphQLField(
        "automaticFulfillment"
    )
    content_file: DigitalContentGraphQLField = DigitalContentGraphQLField("contentFile")
    max_downloads: DigitalContentGraphQLField = DigitalContentGraphQLField(
        "maxDownloads"
    )
    url_valid_days: DigitalContentGraphQLField = DigitalContentGraphQLField(
        "urlValidDays"
    )

    @classmethod
    def urls(cls) -> "DigitalContentUrlFields":
        return DigitalContentUrlFields("urls")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    def fields(
        self,
        *subfields: Union[
            DigitalContentGraphQLField,
            "MetadataItemFields",
            "ProductVariantFields",
            "DigitalContentUrlFields",
        ]
    ) -> "DigitalContentFields":
        self._subfields.extend(subfields)
        return self


class UserAvatarDeleteFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            UserAvatarDeleteGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "UserAvatarDeleteFields":
        self._subfields.extend(subfields)
        return self


class PaymentSourceFields(GraphQLField):
    gateway: PaymentSourceGraphQLField = PaymentSourceGraphQLField("gateway")
    payment_method_id: PaymentSourceGraphQLField = PaymentSourceGraphQLField(
        "paymentMethodId"
    )

    @classmethod
    def credit_card_info(cls) -> "CreditCardFields":
        return CreditCardFields("credit_card_info")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    def fields(
        self,
        *subfields: Union[
            PaymentSourceGraphQLField, "MetadataItemFields", "CreditCardFields"
        ]
    ) -> "PaymentSourceFields":
        self._subfields.extend(subfields)
        return self


class AssignNavigationFields(GraphQLField):
    @classmethod
    def menu(cls) -> "MenuFields":
        return MenuFields("menu")

    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    def fields(
        self,
        *subfields: Union[AssignNavigationGraphQLField, "MenuFields", "MenuErrorFields"]
    ) -> "AssignNavigationFields":
        self._subfields.extend(subfields)
        return self


class ProductImageFields(GraphQLField):
    id: ProductImageGraphQLField = ProductImageGraphQLField("id")
    alt: ProductImageGraphQLField = ProductImageGraphQLField("alt")
    sort_order: ProductImageGraphQLField = ProductImageGraphQLField("sortOrder")
    url: ProductImageGraphQLField = ProductImageGraphQLField("url")

    def fields(self, *subfields: ProductImageGraphQLField) -> "ProductImageFields":
        self._subfields.extend(subfields)
        return self


class WebhookCreateFields(GraphQLField):
    @classmethod
    def webhook_errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("webhook_errors")

    @classmethod
    def errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("errors")

    @classmethod
    def webhook(cls) -> "WebhookFields":
        return WebhookFields("webhook")

    def fields(
        self,
        *subfields: Union[
            WebhookCreateGraphQLField, "WebhookErrorFields", "WebhookFields"
        ]
    ) -> "WebhookCreateFields":
        self._subfields.extend(subfields)
        return self


class TaxConfigurationCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "TaxConfigurationCountableEdgeFields":
        return TaxConfigurationCountableEdgeFields("edges")

    total_count: TaxConfigurationCountableConnectionGraphQLField = (
        TaxConfigurationCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            TaxConfigurationCountableConnectionGraphQLField,
            "PageInfoFields",
            "TaxConfigurationCountableEdgeFields",
        ]
    ) -> "TaxConfigurationCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class CustomerBulkUpdateFields(GraphQLField):
    count: CustomerBulkUpdateGraphQLField = CustomerBulkUpdateGraphQLField("count")

    @classmethod
    def results(cls) -> "CustomerBulkResultFields":
        return CustomerBulkResultFields("results")

    @classmethod
    def errors(cls) -> "CustomerBulkUpdateErrorFields":
        return CustomerBulkUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CustomerBulkUpdateGraphQLField,
            "CustomerBulkResultFields",
            "CustomerBulkUpdateErrorFields",
        ]
    ) -> "CustomerBulkUpdateFields":
        self._subfields.extend(subfields)
        return self


class PaymentCaptureFields(GraphQLField):
    @classmethod
    def payment(cls) -> "PaymentFields":
        return PaymentFields("payment")

    @classmethod
    def payment_errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("payment_errors")

    @classmethod
    def errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentCaptureGraphQLField, "PaymentFields", "PaymentErrorFields"
        ]
    ) -> "PaymentCaptureFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantReorderFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantReorderGraphQLField, "ProductFields", "ProductErrorFields"
        ]
    ) -> "ProductVariantReorderFields":
        self._subfields.extend(subfields)
        return self


class VoucherCodeBulkDeleteFields(GraphQLField):
    count: VoucherCodeBulkDeleteGraphQLField = VoucherCodeBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def errors(cls) -> "VoucherCodeBulkDeleteErrorFields":
        return VoucherCodeBulkDeleteErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            VoucherCodeBulkDeleteGraphQLField, "VoucherCodeBulkDeleteErrorFields"
        ]
    ) -> "VoucherCodeBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class TransactionFields(GraphQLField):
    id: TransactionGraphQLField = TransactionGraphQLField("id")
    created: TransactionGraphQLField = TransactionGraphQLField("created")

    @classmethod
    def payment(cls) -> "PaymentFields":
        return PaymentFields("payment")

    token: TransactionGraphQLField = TransactionGraphQLField("token")
    kind: TransactionGraphQLField = TransactionGraphQLField("kind")
    is_success: TransactionGraphQLField = TransactionGraphQLField("isSuccess")
    error: TransactionGraphQLField = TransactionGraphQLField("error")
    gateway_response: TransactionGraphQLField = TransactionGraphQLField(
        "gatewayResponse"
    )

    @classmethod
    def amount(cls) -> "MoneyFields":
        return MoneyFields("amount")

    def fields(
        self, *subfields: Union[TransactionGraphQLField, "PaymentFields", "MoneyFields"]
    ) -> "TransactionFields":
        self._subfields.extend(subfields)
        return self


class PluginCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "PluginCountableEdgeFields":
        return PluginCountableEdgeFields("edges")

    total_count: PluginCountableConnectionGraphQLField = (
        PluginCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            PluginCountableConnectionGraphQLField,
            "PluginCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "PluginCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class AddressUpdateFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    def fields(
        self,
        *subfields: Union[
            AddressUpdateGraphQLField,
            "AccountErrorFields",
            "UserFields",
            "AddressFields",
        ]
    ) -> "AddressUpdateFields":
        self._subfields.extend(subfields)
        return self


class OrderSettingsUpdateFields(GraphQLField):
    @classmethod
    def order_settings(cls) -> "OrderSettingsFields":
        return OrderSettingsFields("order_settings")

    @classmethod
    def order_settings_errors(cls) -> "OrderSettingsErrorFields":
        return OrderSettingsErrorFields("order_settings_errors")

    @classmethod
    def errors(cls) -> "OrderSettingsErrorFields":
        return OrderSettingsErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderSettingsUpdateGraphQLField,
            "OrderSettingsErrorFields",
            "OrderSettingsFields",
        ]
    ) -> "OrderSettingsUpdateFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleDeleteFields(GraphQLField):
    @classmethod
    def errors(cls) -> "PromotionRuleDeleteErrorFields":
        return PromotionRuleDeleteErrorFields("errors")

    @classmethod
    def promotion_rule(cls) -> "PromotionRuleFields":
        return PromotionRuleFields("promotion_rule")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleDeleteGraphQLField,
            "PromotionRuleDeleteErrorFields",
            "PromotionRuleFields",
        ]
    ) -> "PromotionRuleDeleteFields":
        self._subfields.extend(subfields)
        return self


class OrderLineUpdateFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    def fields(
        self,
        *subfields: Union[
            OrderLineUpdateGraphQLField,
            "OrderErrorFields",
            "OrderFields",
            "OrderLineFields",
        ]
    ) -> "OrderLineUpdateFields":
        self._subfields.extend(subfields)
        return self


class DeleteMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadata_errors")

    @classmethod
    def errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("errors")

    item: ObjectWithMetadataInterface = ObjectWithMetadataInterface("item")

    def fields(
        self,
        *subfields: Union[
            DeleteMetadataGraphQLField,
            "MetadataErrorFields",
            "ObjectWithMetadataInterface",
        ]
    ) -> "DeleteMetadataFields":
        self._subfields.extend(subfields)
        return self


class MenuCreateFields(GraphQLField):
    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    @classmethod
    def menu(cls) -> "MenuFields":
        return MenuFields("menu")

    def fields(
        self, *subfields: Union[MenuCreateGraphQLField, "MenuFields", "MenuErrorFields"]
    ) -> "MenuCreateFields":
        self._subfields.extend(subfields)
        return self


class AccountSetDefaultAddressFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AccountSetDefaultAddressGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "AccountSetDefaultAddressFields":
        self._subfields.extend(subfields)
        return self


class WebhookEventAsyncFields(GraphQLField):
    name: WebhookEventAsyncGraphQLField = WebhookEventAsyncGraphQLField("name")
    event_type: WebhookEventAsyncGraphQLField = WebhookEventAsyncGraphQLField(
        "eventType"
    )

    def fields(
        self, *subfields: WebhookEventAsyncGraphQLField
    ) -> "WebhookEventAsyncFields":
        self._subfields.extend(subfields)
        return self


class OrderDiscountAddFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderDiscountAddGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "OrderDiscountAddFields":
        self._subfields.extend(subfields)
        return self


class AppActivateFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    def fields(
        self, *subfields: Union[AppActivateGraphQLField, "AppErrorFields", "AppFields"]
    ) -> "AppActivateFields":
        self._subfields.extend(subfields)
        return self


class AppManifestExtensionFields(GraphQLField):
    @classmethod
    def permissions(cls) -> "PermissionFields":
        return PermissionFields("permissions")

    label: AppManifestExtensionGraphQLField = AppManifestExtensionGraphQLField("label")
    url: AppManifestExtensionGraphQLField = AppManifestExtensionGraphQLField("url")
    mount: AppManifestExtensionGraphQLField = AppManifestExtensionGraphQLField("mount")
    target: AppManifestExtensionGraphQLField = AppManifestExtensionGraphQLField(
        "target"
    )

    def fields(
        self, *subfields: Union[AppManifestExtensionGraphQLField, "PermissionFields"]
    ) -> "AppManifestExtensionFields":
        self._subfields.extend(subfields)
        return self


class PaymentInitializeFields(GraphQLField):
    @classmethod
    def initialized_payment(cls) -> "PaymentInitializedFields":
        return PaymentInitializedFields("initialized_payment")

    @classmethod
    def payment_errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("payment_errors")

    @classmethod
    def errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentInitializeGraphQLField,
            "PaymentInitializedFields",
            "PaymentErrorFields",
        ]
    ) -> "PaymentInitializeFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCreateFromOrderErrorFields(GraphQLField):
    field: CheckoutCreateFromOrderErrorGraphQLField = (
        CheckoutCreateFromOrderErrorGraphQLField("field")
    )
    message: CheckoutCreateFromOrderErrorGraphQLField = (
        CheckoutCreateFromOrderErrorGraphQLField("message")
    )
    code: CheckoutCreateFromOrderErrorGraphQLField = (
        CheckoutCreateFromOrderErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: CheckoutCreateFromOrderErrorGraphQLField
    ) -> "CheckoutCreateFromOrderErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeBulkDeleteFields(GraphQLField):
    count: ProductTypeBulkDeleteGraphQLField = ProductTypeBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self, *subfields: Union[ProductTypeBulkDeleteGraphQLField, "ProductErrorFields"]
    ) -> "ProductTypeBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class PromotionCreatedEventFields(GraphQLField):
    id: PromotionCreatedEventGraphQLField = PromotionCreatedEventGraphQLField("id")
    date: PromotionCreatedEventGraphQLField = PromotionCreatedEventGraphQLField("date")
    type: PromotionCreatedEventGraphQLField = PromotionCreatedEventGraphQLField("type")
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")

    def fields(
        self, *subfields: Union[PromotionCreatedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionCreatedEventFields":
        self._subfields.extend(subfields)
        return self


class VoucherCodeBulkDeleteErrorFields(GraphQLField):
    path: VoucherCodeBulkDeleteErrorGraphQLField = (
        VoucherCodeBulkDeleteErrorGraphQLField("path")
    )
    message: VoucherCodeBulkDeleteErrorGraphQLField = (
        VoucherCodeBulkDeleteErrorGraphQLField("message")
    )
    code: VoucherCodeBulkDeleteErrorGraphQLField = (
        VoucherCodeBulkDeleteErrorGraphQLField("code")
    )
    voucher_codes: VoucherCodeBulkDeleteErrorGraphQLField = (
        VoucherCodeBulkDeleteErrorGraphQLField("voucherCodes")
    )

    def fields(
        self, *subfields: VoucherCodeBulkDeleteErrorGraphQLField
    ) -> "VoucherCodeBulkDeleteErrorFields":
        self._subfields.extend(subfields)
        return self


class PaymentMethodProcessTokenizationFields(GraphQLField):
    result: PaymentMethodProcessTokenizationGraphQLField = (
        PaymentMethodProcessTokenizationGraphQLField("result")
    )
    id: PaymentMethodProcessTokenizationGraphQLField = (
        PaymentMethodProcessTokenizationGraphQLField("id")
    )
    data: PaymentMethodProcessTokenizationGraphQLField = (
        PaymentMethodProcessTokenizationGraphQLField("data")
    )

    @classmethod
    def errors(cls) -> "PaymentMethodProcessTokenizationErrorFields":
        return PaymentMethodProcessTokenizationErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentMethodProcessTokenizationGraphQLField,
            "PaymentMethodProcessTokenizationErrorFields",
        ]
    ) -> "PaymentMethodProcessTokenizationFields":
        self._subfields.extend(subfields)
        return self


class OrderEventDiscountObjectFields(GraphQLField):
    value_type: OrderEventDiscountObjectGraphQLField = (
        OrderEventDiscountObjectGraphQLField("valueType")
    )
    value: OrderEventDiscountObjectGraphQLField = OrderEventDiscountObjectGraphQLField(
        "value"
    )
    reason: OrderEventDiscountObjectGraphQLField = OrderEventDiscountObjectGraphQLField(
        "reason"
    )

    @classmethod
    def amount(cls) -> "MoneyFields":
        return MoneyFields("amount")

    old_value_type: OrderEventDiscountObjectGraphQLField = (
        OrderEventDiscountObjectGraphQLField("oldValueType")
    )
    old_value: OrderEventDiscountObjectGraphQLField = (
        OrderEventDiscountObjectGraphQLField("oldValue")
    )

    @classmethod
    def old_amount(cls) -> "MoneyFields":
        return MoneyFields("old_amount")

    def fields(
        self, *subfields: Union[OrderEventDiscountObjectGraphQLField, "MoneyFields"]
    ) -> "OrderEventDiscountObjectFields":
        self._subfields.extend(subfields)
        return self


class PageTypeCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "PageTypeFields":
        return PageTypeFields("node")

    cursor: PageTypeCountableEdgeGraphQLField = PageTypeCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[PageTypeCountableEdgeGraphQLField, "PageTypeFields"]
    ) -> "PageTypeCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkDeleteFields(GraphQLField):
    count: ProductVariantBulkDeleteGraphQLField = ProductVariantBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[ProductVariantBulkDeleteGraphQLField, "ProductErrorFields"]
    ) -> "ProductVariantBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class StaffErrorFields(GraphQLField):
    field: StaffErrorGraphQLField = StaffErrorGraphQLField("field")
    message: StaffErrorGraphQLField = StaffErrorGraphQLField("message")
    code: StaffErrorGraphQLField = StaffErrorGraphQLField("code")
    address_type: StaffErrorGraphQLField = StaffErrorGraphQLField("addressType")
    permissions: StaffErrorGraphQLField = StaffErrorGraphQLField("permissions")
    groups: StaffErrorGraphQLField = StaffErrorGraphQLField("groups")
    users: StaffErrorGraphQLField = StaffErrorGraphQLField("users")

    def fields(self, *subfields: StaffErrorGraphQLField) -> "StaffErrorFields":
        self._subfields.extend(subfields)
        return self


class PluginErrorFields(GraphQLField):
    field: PluginErrorGraphQLField = PluginErrorGraphQLField("field")
    message: PluginErrorGraphQLField = PluginErrorGraphQLField("message")
    code: PluginErrorGraphQLField = PluginErrorGraphQLField("code")

    def fields(self, *subfields: PluginErrorGraphQLField) -> "PluginErrorFields":
        self._subfields.extend(subfields)
        return self


class UploadErrorFields(GraphQLField):
    field: UploadErrorGraphQLField = UploadErrorGraphQLField("field")
    message: UploadErrorGraphQLField = UploadErrorGraphQLField("message")
    code: UploadErrorGraphQLField = UploadErrorGraphQLField("code")

    def fields(self, *subfields: UploadErrorGraphQLField) -> "UploadErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantCreateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    def fields(
        self,
        *subfields: Union[
            ProductVariantCreateGraphQLField,
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "ProductVariantCreateFields":
        self._subfields.extend(subfields)
        return self


class MetadataItemFields(GraphQLField):
    key: MetadataItemGraphQLField = MetadataItemGraphQLField("key")
    value: MetadataItemGraphQLField = MetadataItemGraphQLField("value")

    def fields(self, *subfields: MetadataItemGraphQLField) -> "MetadataItemFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentUrlCreateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def digital_content_url(cls) -> "DigitalContentUrlFields":
        return DigitalContentUrlFields("digital_content_url")

    def fields(
        self,
        *subfields: Union[
            DigitalContentUrlCreateGraphQLField,
            "ProductErrorFields",
            "DigitalContentUrlFields",
        ]
    ) -> "DigitalContentUrlCreateFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeFields(GraphQLField):
    id: ProductTypeGraphQLField = ProductTypeGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ProductTypeGraphQLField = ProductTypeGraphQLField(
        "privateMetafield"
    )
    private_metafields: ProductTypeGraphQLField = ProductTypeGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ProductTypeGraphQLField = ProductTypeGraphQLField("metafield")
    metafields: ProductTypeGraphQLField = ProductTypeGraphQLField("metafields")
    name: ProductTypeGraphQLField = ProductTypeGraphQLField("name")
    slug: ProductTypeGraphQLField = ProductTypeGraphQLField("slug")
    has_variants: ProductTypeGraphQLField = ProductTypeGraphQLField("hasVariants")
    is_shipping_required: ProductTypeGraphQLField = ProductTypeGraphQLField(
        "isShippingRequired"
    )
    is_digital: ProductTypeGraphQLField = ProductTypeGraphQLField("isDigital")

    @classmethod
    def weight(cls) -> "WeightFields":
        return WeightFields("weight")

    kind: ProductTypeGraphQLField = ProductTypeGraphQLField("kind")

    @classmethod
    def products(cls) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields("products")

    @classmethod
    def tax_type(cls) -> "TaxTypeFields":
        return TaxTypeFields("tax_type")

    @classmethod
    def tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("tax_class")

    @classmethod
    def variant_attributes(cls) -> "AttributeFields":
        return AttributeFields("variant_attributes")

    @classmethod
    def assigned_variant_attributes(cls) -> "AssignedVariantAttributeFields":
        return AssignedVariantAttributeFields("assigned_variant_attributes")

    @classmethod
    def product_attributes(cls) -> "AttributeFields":
        return AttributeFields("product_attributes")

    @classmethod
    def available_attributes(cls) -> "AttributeCountableConnectionFields":
        return AttributeCountableConnectionFields("available_attributes")

    def fields(
        self,
        *subfields: Union[
            ProductTypeGraphQLField,
            "AssignedVariantAttributeFields",
            "WeightFields",
            "MetadataItemFields",
            "ProductCountableConnectionFields",
            "AttributeFields",
            "TaxClassFields",
            "AttributeCountableConnectionFields",
            "TaxTypeFields",
        ]
    ) -> "ProductTypeFields":
        self._subfields.extend(subfields)
        return self


class PromotionTranslateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def promotion(cls) -> "PromotionFields":
        return PromotionFields("promotion")

    def fields(
        self,
        *subfields: Union[
            PromotionTranslateGraphQLField, "PromotionFields", "TranslationErrorFields"
        ]
    ) -> "PromotionTranslateFields":
        self._subfields.extend(subfields)
        return self


class AttributeUpdateFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeUpdateGraphQLField, "AttributeFields", "AttributeErrorFields"
        ]
    ) -> "AttributeUpdateFields":
        self._subfields.extend(subfields)
        return self


class AppErrorFields(GraphQLField):
    field: AppErrorGraphQLField = AppErrorGraphQLField("field")
    message: AppErrorGraphQLField = AppErrorGraphQLField("message")
    code: AppErrorGraphQLField = AppErrorGraphQLField("code")
    permissions: AppErrorGraphQLField = AppErrorGraphQLField("permissions")

    def fields(self, *subfields: AppErrorGraphQLField) -> "AppErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkResultFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def errors(cls) -> "ProductVariantBulkErrorFields":
        return ProductVariantBulkErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantBulkResultGraphQLField,
            "ProductVariantFields",
            "ProductVariantBulkErrorFields",
        ]
    ) -> "ProductVariantBulkResultFields":
        self._subfields.extend(subfields)
        return self


class ProductPricingInfoFields(GraphQLField):
    on_sale: ProductPricingInfoGraphQLField = ProductPricingInfoGraphQLField("onSale")

    @classmethod
    def discount(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("discount")

    @classmethod
    def discount_local_currency(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("discount_local_currency")

    display_gross_prices: ProductPricingInfoGraphQLField = (
        ProductPricingInfoGraphQLField("displayGrossPrices")
    )

    @classmethod
    def price_range(cls) -> "TaxedMoneyRangeFields":
        return TaxedMoneyRangeFields("price_range")

    @classmethod
    def price_range_undiscounted(cls) -> "TaxedMoneyRangeFields":
        return TaxedMoneyRangeFields("price_range_undiscounted")

    @classmethod
    def price_range_local_currency(cls) -> "TaxedMoneyRangeFields":
        return TaxedMoneyRangeFields("price_range_local_currency")

    def fields(
        self,
        *subfields: Union[
            ProductPricingInfoGraphQLField, "TaxedMoneyRangeFields", "TaxedMoneyFields"
        ]
    ) -> "ProductPricingInfoFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantedRefundFields(GraphQLField):
    id: OrderGrantedRefundGraphQLField = OrderGrantedRefundGraphQLField("id")
    created_at: OrderGrantedRefundGraphQLField = OrderGrantedRefundGraphQLField(
        "createdAt"
    )
    updated_at: OrderGrantedRefundGraphQLField = OrderGrantedRefundGraphQLField(
        "updatedAt"
    )

    @classmethod
    def amount(cls) -> "MoneyFields":
        return MoneyFields("amount")

    reason: OrderGrantedRefundGraphQLField = OrderGrantedRefundGraphQLField("reason")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    shipping_costs_included: OrderGrantedRefundGraphQLField = (
        OrderGrantedRefundGraphQLField("shippingCostsIncluded")
    )

    @classmethod
    def lines(cls) -> "OrderGrantedRefundLineFields":
        return OrderGrantedRefundLineFields("lines")

    status: OrderGrantedRefundGraphQLField = OrderGrantedRefundGraphQLField("status")

    @classmethod
    def transaction_events(cls) -> "TransactionEventFields":
        return TransactionEventFields("transaction_events")

    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    def fields(
        self,
        *subfields: Union[
            OrderGrantedRefundGraphQLField,
            "OrderGrantedRefundLineFields",
            "UserFields",
            "TransactionItemFields",
            "AppFields",
            "MoneyFields",
            "TransactionEventFields",
        ]
    ) -> "OrderGrantedRefundFields":
        self._subfields.extend(subfields)
        return self


class TranslatableItemEdgeFields(GraphQLField):
    node: TranslatableItemUnion = TranslatableItemUnion("node")
    cursor: TranslatableItemEdgeGraphQLField = TranslatableItemEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self,
        *subfields: Union[TranslatableItemEdgeGraphQLField, "TranslatableItemUnion"]
    ) -> "TranslatableItemEdgeFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkTranslateErrorFields(GraphQLField):
    path: ProductBulkTranslateErrorGraphQLField = ProductBulkTranslateErrorGraphQLField(
        "path"
    )
    message: ProductBulkTranslateErrorGraphQLField = (
        ProductBulkTranslateErrorGraphQLField("message")
    )
    code: ProductBulkTranslateErrorGraphQLField = ProductBulkTranslateErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: ProductBulkTranslateErrorGraphQLField
    ) -> "ProductBulkTranslateErrorFields":
        self._subfields.extend(subfields)
        return self


class PromotionCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "PromotionCountableEdgeFields":
        return PromotionCountableEdgeFields("edges")

    total_count: PromotionCountableConnectionGraphQLField = (
        PromotionCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            PromotionCountableConnectionGraphQLField,
            "PromotionCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "PromotionCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayInitializeErrorFields(GraphQLField):
    field: PaymentGatewayInitializeErrorGraphQLField = (
        PaymentGatewayInitializeErrorGraphQLField("field")
    )
    message: PaymentGatewayInitializeErrorGraphQLField = (
        PaymentGatewayInitializeErrorGraphQLField("message")
    )
    code: PaymentGatewayInitializeErrorGraphQLField = (
        PaymentGatewayInitializeErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: PaymentGatewayInitializeErrorGraphQLField
    ) -> "PaymentGatewayInitializeErrorFields":
        self._subfields.extend(subfields)
        return self


class StockErrorFields(GraphQLField):
    field: StockErrorGraphQLField = StockErrorGraphQLField("field")
    message: StockErrorGraphQLField = StockErrorGraphQLField("message")
    code: StockErrorGraphQLField = StockErrorGraphQLField("code")

    def fields(self, *subfields: StockErrorGraphQLField) -> "StockErrorFields":
        self._subfields.extend(subfields)
        return self


class PreorderThresholdFields(GraphQLField):
    quantity: PreorderThresholdGraphQLField = PreorderThresholdGraphQLField("quantity")
    sold_units: PreorderThresholdGraphQLField = PreorderThresholdGraphQLField(
        "soldUnits"
    )

    def fields(
        self, *subfields: PreorderThresholdGraphQLField
    ) -> "PreorderThresholdFields":
        self._subfields.extend(subfields)
        return self


class AppManifestBrandLogoFields(GraphQLField):
    default: AppManifestBrandLogoGraphQLField = AppManifestBrandLogoGraphQLField(
        "default"
    )

    def fields(
        self, *subfields: AppManifestBrandLogoGraphQLField
    ) -> "AppManifestBrandLogoFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryAttemptFields(GraphQLField):
    id: EventDeliveryAttemptGraphQLField = EventDeliveryAttemptGraphQLField("id")
    created_at: EventDeliveryAttemptGraphQLField = EventDeliveryAttemptGraphQLField(
        "createdAt"
    )
    task_id: EventDeliveryAttemptGraphQLField = EventDeliveryAttemptGraphQLField(
        "taskId"
    )
    duration: EventDeliveryAttemptGraphQLField = EventDeliveryAttemptGraphQLField(
        "duration"
    )
    response: EventDeliveryAttemptGraphQLField = EventDeliveryAttemptGraphQLField(
        "response"
    )
    response_headers: EventDeliveryAttemptGraphQLField = (
        EventDeliveryAttemptGraphQLField("responseHeaders")
    )
    response_status_code: EventDeliveryAttemptGraphQLField = (
        EventDeliveryAttemptGraphQLField("responseStatusCode")
    )
    request_headers: EventDeliveryAttemptGraphQLField = (
        EventDeliveryAttemptGraphQLField("requestHeaders")
    )
    status: EventDeliveryAttemptGraphQLField = EventDeliveryAttemptGraphQLField(
        "status"
    )

    def fields(
        self, *subfields: EventDeliveryAttemptGraphQLField
    ) -> "EventDeliveryAttemptFields":
        self._subfields.extend(subfields)
        return self


class CategoryTranslationFields(GraphQLField):
    id: CategoryTranslationGraphQLField = CategoryTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    seo_title: CategoryTranslationGraphQLField = CategoryTranslationGraphQLField(
        "seoTitle"
    )
    seo_description: CategoryTranslationGraphQLField = CategoryTranslationGraphQLField(
        "seoDescription"
    )
    name: CategoryTranslationGraphQLField = CategoryTranslationGraphQLField("name")
    description: CategoryTranslationGraphQLField = CategoryTranslationGraphQLField(
        "description"
    )
    description_json: CategoryTranslationGraphQLField = CategoryTranslationGraphQLField(
        "descriptionJson"
    )

    @classmethod
    def translatable_content(cls) -> "CategoryTranslatableContentFields":
        return CategoryTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            CategoryTranslationGraphQLField,
            "CategoryTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "CategoryTranslationFields":
        self._subfields.extend(subfields)
        return self


class GiftCardDeactivateFields(GraphQLField):
    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    @classmethod
    def gift_card_errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("gift_card_errors")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            GiftCardDeactivateGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardDeactivateFields":
        self._subfields.extend(subfields)
        return self


class TaxedMoneyFields(GraphQLField):
    currency: TaxedMoneyGraphQLField = TaxedMoneyGraphQLField("currency")

    @classmethod
    def gross(cls) -> "MoneyFields":
        return MoneyFields("gross")

    @classmethod
    def net(cls) -> "MoneyFields":
        return MoneyFields("net")

    @classmethod
    def tax(cls) -> "MoneyFields":
        return MoneyFields("tax")

    def fields(
        self, *subfields: Union[TaxedMoneyGraphQLField, "MoneyFields"]
    ) -> "TaxedMoneyFields":
        self._subfields.extend(subfields)
        return self


class StockBulkResultFields(GraphQLField):
    @classmethod
    def stock(cls) -> "StockFields":
        return StockFields("stock")

    @classmethod
    def errors(cls) -> "StockBulkUpdateErrorFields":
        return StockBulkUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            StockBulkResultGraphQLField, "StockFields", "StockBulkUpdateErrorFields"
        ]
    ) -> "StockBulkResultFields":
        self._subfields.extend(subfields)
        return self


class ManifestFields(GraphQLField):
    identifier: ManifestGraphQLField = ManifestGraphQLField("identifier")
    version: ManifestGraphQLField = ManifestGraphQLField("version")
    name: ManifestGraphQLField = ManifestGraphQLField("name")
    about: ManifestGraphQLField = ManifestGraphQLField("about")

    @classmethod
    def permissions(cls) -> "PermissionFields":
        return PermissionFields("permissions")

    app_url: ManifestGraphQLField = ManifestGraphQLField("appUrl")
    configuration_url: ManifestGraphQLField = ManifestGraphQLField("configurationUrl")
    token_target_url: ManifestGraphQLField = ManifestGraphQLField("tokenTargetUrl")
    data_privacy: ManifestGraphQLField = ManifestGraphQLField("dataPrivacy")
    data_privacy_url: ManifestGraphQLField = ManifestGraphQLField("dataPrivacyUrl")
    homepage_url: ManifestGraphQLField = ManifestGraphQLField("homepageUrl")
    support_url: ManifestGraphQLField = ManifestGraphQLField("supportUrl")

    @classmethod
    def extensions(cls) -> "AppManifestExtensionFields":
        return AppManifestExtensionFields("extensions")

    @classmethod
    def webhooks(cls) -> "AppManifestWebhookFields":
        return AppManifestWebhookFields("webhooks")

    audience: ManifestGraphQLField = ManifestGraphQLField("audience")

    @classmethod
    def required_saleor_version(cls) -> "AppManifestRequiredSaleorVersionFields":
        return AppManifestRequiredSaleorVersionFields("required_saleor_version")

    author: ManifestGraphQLField = ManifestGraphQLField("author")

    @classmethod
    def brand(cls) -> "AppManifestBrandFields":
        return AppManifestBrandFields("brand")

    def fields(
        self,
        *subfields: Union[
            ManifestGraphQLField,
            "AppManifestRequiredSaleorVersionFields",
            "AppManifestExtensionFields",
            "PermissionFields",
            "AppManifestWebhookFields",
            "AppManifestBrandFields",
        ]
    ) -> "ManifestFields":
        self._subfields.extend(subfields)
        return self


class MenuFields(GraphQLField):
    id: MenuGraphQLField = MenuGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: MenuGraphQLField = MenuGraphQLField("privateMetafield")
    private_metafields: MenuGraphQLField = MenuGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: MenuGraphQLField = MenuGraphQLField("metafield")
    metafields: MenuGraphQLField = MenuGraphQLField("metafields")
    name: MenuGraphQLField = MenuGraphQLField("name")
    slug: MenuGraphQLField = MenuGraphQLField("slug")

    @classmethod
    def items(cls) -> "MenuItemFields":
        return MenuItemFields("items")

    def fields(
        self,
        *subfields: Union[MenuGraphQLField, "MetadataItemFields", "MenuItemFields"]
    ) -> "MenuFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneUpdateFields(GraphQLField):
    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    @classmethod
    def shipping_zone(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("shipping_zone")

    def fields(
        self,
        *subfields: Union[
            ShippingZoneUpdateGraphQLField, "ShippingZoneFields", "ShippingErrorFields"
        ]
    ) -> "ShippingZoneUpdateFields":
        self._subfields.extend(subfields)
        return self


class DraftOrderBulkDeleteFields(GraphQLField):
    count: DraftOrderBulkDeleteGraphQLField = DraftOrderBulkDeleteGraphQLField("count")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self, *subfields: Union[DraftOrderBulkDeleteGraphQLField, "OrderErrorFields"]
    ) -> "DraftOrderBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkTranslateResultFields(GraphQLField):
    @classmethod
    def translation(cls) -> "AttributeTranslationFields":
        return AttributeTranslationFields("translation")

    @classmethod
    def errors(cls) -> "AttributeBulkTranslateErrorFields":
        return AttributeBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeBulkTranslateResultGraphQLField,
            "AttributeBulkTranslateErrorFields",
            "AttributeTranslationFields",
        ]
    ) -> "AttributeBulkTranslateResultFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodTranslationFields(GraphQLField):
    id: ShippingMethodTranslationGraphQLField = ShippingMethodTranslationGraphQLField(
        "id"
    )

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: ShippingMethodTranslationGraphQLField = ShippingMethodTranslationGraphQLField(
        "name"
    )
    description: ShippingMethodTranslationGraphQLField = (
        ShippingMethodTranslationGraphQLField("description")
    )

    @classmethod
    def translatable_content(cls) -> "ShippingMethodTranslatableContentFields":
        return ShippingMethodTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            ShippingMethodTranslationGraphQLField,
            "ShippingMethodTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "ShippingMethodTranslationFields":
        self._subfields.extend(subfields)
        return self


class AttributeCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "AttributeCountableEdgeFields":
        return AttributeCountableEdgeFields("edges")

    total_count: AttributeCountableConnectionGraphQLField = (
        AttributeCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            AttributeCountableConnectionGraphQLField,
            "AttributeCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "AttributeCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class OrderCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "OrderFields":
        return OrderFields("node")

    cursor: OrderCountableEdgeGraphQLField = OrderCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[OrderCountableEdgeGraphQLField, "OrderFields"]
    ) -> "OrderCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class OrderFields(GraphQLField):
    id: OrderGraphQLField = OrderGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: OrderGraphQLField = OrderGraphQLField("privateMetafield")
    private_metafields: OrderGraphQLField = OrderGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: OrderGraphQLField = OrderGraphQLField("metafield")
    metafields: OrderGraphQLField = OrderGraphQLField("metafields")
    created: OrderGraphQLField = OrderGraphQLField("created")
    updated_at: OrderGraphQLField = OrderGraphQLField("updatedAt")
    status: OrderGraphQLField = OrderGraphQLField("status")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    tracking_client_id: OrderGraphQLField = OrderGraphQLField("trackingClientId")

    @classmethod
    def billing_address(cls) -> "AddressFields":
        return AddressFields("billing_address")

    @classmethod
    def shipping_address(cls) -> "AddressFields":
        return AddressFields("shipping_address")

    shipping_method_name: OrderGraphQLField = OrderGraphQLField("shippingMethodName")
    collection_point_name: OrderGraphQLField = OrderGraphQLField("collectionPointName")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def fulfillments(cls) -> "FulfillmentFields":
        return FulfillmentFields("fulfillments")

    @classmethod
    def lines(cls) -> "OrderLineFields":
        return OrderLineFields("lines")

    actions: OrderGraphQLField = OrderGraphQLField("actions")

    @classmethod
    def available_shipping_methods(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("available_shipping_methods")

    @classmethod
    def shipping_methods(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("shipping_methods")

    @classmethod
    def available_collection_points(cls) -> "WarehouseFields":
        return WarehouseFields("available_collection_points")

    @classmethod
    def invoices(cls) -> "InvoiceFields":
        return InvoiceFields("invoices")

    number: OrderGraphQLField = OrderGraphQLField("number")
    original: OrderGraphQLField = OrderGraphQLField("original")
    origin: OrderGraphQLField = OrderGraphQLField("origin")
    is_paid: OrderGraphQLField = OrderGraphQLField("isPaid")
    payment_status: OrderGraphQLField = OrderGraphQLField("paymentStatus")
    payment_status_display: OrderGraphQLField = OrderGraphQLField(
        "paymentStatusDisplay"
    )
    authorize_status: OrderGraphQLField = OrderGraphQLField("authorizeStatus")
    charge_status: OrderGraphQLField = OrderGraphQLField("chargeStatus")
    tax_exemption: OrderGraphQLField = OrderGraphQLField("taxExemption")

    @classmethod
    def transactions(cls) -> "TransactionItemFields":
        return TransactionItemFields("transactions")

    @classmethod
    def payments(cls) -> "PaymentFields":
        return PaymentFields("payments")

    @classmethod
    def total(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("total")

    @classmethod
    def undiscounted_total(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("undiscounted_total")

    @classmethod
    def shipping_method(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("shipping_method")

    @classmethod
    def shipping_price(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("shipping_price")

    shipping_tax_rate: OrderGraphQLField = OrderGraphQLField("shippingTaxRate")

    @classmethod
    def shipping_tax_class(cls) -> "TaxClassFields":
        return TaxClassFields("shipping_tax_class")

    shipping_tax_class_name: OrderGraphQLField = OrderGraphQLField(
        "shippingTaxClassName"
    )

    @classmethod
    def shipping_tax_class_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("shipping_tax_class_metadata")

    @classmethod
    def shipping_tax_class_private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("shipping_tax_class_private_metadata")

    token: OrderGraphQLField = OrderGraphQLField("token")

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    voucher_code: OrderGraphQLField = OrderGraphQLField("voucherCode")

    @classmethod
    def gift_cards(cls) -> "GiftCardFields":
        return GiftCardFields("gift_cards")

    customer_note: OrderGraphQLField = OrderGraphQLField("customerNote")

    @classmethod
    def weight(cls) -> "WeightFields":
        return WeightFields("weight")

    redirect_url: OrderGraphQLField = OrderGraphQLField("redirectUrl")

    @classmethod
    def subtotal(cls) -> "TaxedMoneyFields":
        return TaxedMoneyFields("subtotal")

    status_display: OrderGraphQLField = OrderGraphQLField("statusDisplay")
    can_finalize: OrderGraphQLField = OrderGraphQLField("canFinalize")

    @classmethod
    def total_authorized(cls) -> "MoneyFields":
        return MoneyFields("total_authorized")

    @classmethod
    def total_captured(cls) -> "MoneyFields":
        return MoneyFields("total_captured")

    @classmethod
    def total_charged(cls) -> "MoneyFields":
        return MoneyFields("total_charged")

    @classmethod
    def total_canceled(cls) -> "MoneyFields":
        return MoneyFields("total_canceled")

    @classmethod
    def events(cls) -> "OrderEventFields":
        return OrderEventFields("events")

    @classmethod
    def total_balance(cls) -> "MoneyFields":
        return MoneyFields("total_balance")

    user_email: OrderGraphQLField = OrderGraphQLField("userEmail")
    is_shipping_required: OrderGraphQLField = OrderGraphQLField("isShippingRequired")
    delivery_method: DeliveryMethodUnion = DeliveryMethodUnion("deliveryMethod")
    language_code: OrderGraphQLField = OrderGraphQLField("languageCode")
    language_code_enum: OrderGraphQLField = OrderGraphQLField("languageCodeEnum")

    @classmethod
    def discount(cls) -> "MoneyFields":
        return MoneyFields("discount")

    discount_name: OrderGraphQLField = OrderGraphQLField("discountName")
    translated_discount_name: OrderGraphQLField = OrderGraphQLField(
        "translatedDiscountName"
    )

    @classmethod
    def discounts(cls) -> "OrderDiscountFields":
        return OrderDiscountFields("discounts")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    display_gross_prices: OrderGraphQLField = OrderGraphQLField("displayGrossPrices")
    external_reference: OrderGraphQLField = OrderGraphQLField("externalReference")
    checkout_id: OrderGraphQLField = OrderGraphQLField("checkoutId")

    @classmethod
    def granted_refunds(cls) -> "OrderGrantedRefundFields":
        return OrderGrantedRefundFields("granted_refunds")

    @classmethod
    def total_granted_refund(cls) -> "MoneyFields":
        return MoneyFields("total_granted_refund")

    @classmethod
    def total_refunded(cls) -> "MoneyFields":
        return MoneyFields("total_refunded")

    @classmethod
    def total_refund_pending(cls) -> "MoneyFields":
        return MoneyFields("total_refund_pending")

    @classmethod
    def total_authorize_pending(cls) -> "MoneyFields":
        return MoneyFields("total_authorize_pending")

    @classmethod
    def total_charge_pending(cls) -> "MoneyFields":
        return MoneyFields("total_charge_pending")

    @classmethod
    def total_cancel_pending(cls) -> "MoneyFields":
        return MoneyFields("total_cancel_pending")

    @classmethod
    def total_remaining_grant(cls) -> "MoneyFields":
        return MoneyFields("total_remaining_grant")

    def fields(
        self,
        *subfields: Union[
            OrderGraphQLField,
            "OrderDiscountFields",
            "TaxedMoneyFields",
            "TransactionItemFields",
            "OrderErrorFields",
            "FulfillmentFields",
            "WarehouseFields",
            "UserFields",
            "WeightFields",
            "VoucherFields",
            "ChannelFields",
            "GiftCardFields",
            "OrderEventFields",
            "PaymentFields",
            "OrderGrantedRefundFields",
            "DeliveryMethodUnion",
            "InvoiceFields",
            "OrderLineFields",
            "MetadataItemFields",
            "ShippingMethodFields",
            "MoneyFields",
            "TaxClassFields",
            "AddressFields",
        ]
    ) -> "OrderFields":
        self._subfields.extend(subfields)
        return self


class PromotionCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "PromotionFields":
        return PromotionFields("node")

    cursor: PromotionCountableEdgeGraphQLField = PromotionCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[PromotionCountableEdgeGraphQLField, "PromotionFields"]
    ) -> "PromotionCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class SaleTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    def fields(
        self,
        *subfields: Union[
            SaleTranslateGraphQLField, "SaleFields", "TranslationErrorFields"
        ]
    ) -> "SaleTranslateFields":
        self._subfields.extend(subfields)
        return self


class ProductAttributeAssignmentUpdateFields(GraphQLField):
    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductAttributeAssignmentUpdateGraphQLField,
            "ProductTypeFields",
            "ProductErrorFields",
        ]
    ) -> "ProductAttributeAssignmentUpdateFields":
        self._subfields.extend(subfields)
        return self


class StockFields(GraphQLField):
    id: StockGraphQLField = StockGraphQLField("id")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    quantity: StockGraphQLField = StockGraphQLField("quantity")
    quantity_allocated: StockGraphQLField = StockGraphQLField("quantityAllocated")
    quantity_reserved: StockGraphQLField = StockGraphQLField("quantityReserved")

    def fields(
        self,
        *subfields: Union[StockGraphQLField, "WarehouseFields", "ProductVariantFields"]
    ) -> "StockFields":
        self._subfields.extend(subfields)
        return self


class _ServiceFields(GraphQLField):
    sdl: _ServiceGraphQLField = _ServiceGraphQLField("sdl")

    def fields(self, *subfields: _ServiceGraphQLField) -> "_ServiceFields":
        self._subfields.extend(subfields)
        return self


class OrderNoteAddFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def event(cls) -> "OrderEventFields":
        return OrderEventFields("event")

    @classmethod
    def errors(cls) -> "OrderNoteAddErrorFields":
        return OrderNoteAddErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderNoteAddGraphQLField,
            "OrderEventFields",
            "OrderNoteAddErrorFields",
            "OrderFields",
        ]
    ) -> "OrderNoteAddFields":
        self._subfields.extend(subfields)
        return self


class StockCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "StockFields":
        return StockFields("node")

    cursor: StockCountableEdgeGraphQLField = StockCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[StockCountableEdgeGraphQLField, "StockFields"]
    ) -> "StockCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class VoucherTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    def fields(
        self,
        *subfields: Union[
            VoucherTranslateGraphQLField, "VoucherFields", "TranslationErrorFields"
        ]
    ) -> "VoucherTranslateFields":
        self._subfields.extend(subfields)
        return self


class StaffNotificationRecipientFields(GraphQLField):
    id: StaffNotificationRecipientGraphQLField = StaffNotificationRecipientGraphQLField(
        "id"
    )

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    email: StaffNotificationRecipientGraphQLField = (
        StaffNotificationRecipientGraphQLField("email")
    )
    active: StaffNotificationRecipientGraphQLField = (
        StaffNotificationRecipientGraphQLField("active")
    )

    def fields(
        self, *subfields: Union[StaffNotificationRecipientGraphQLField, "UserFields"]
    ) -> "StaffNotificationRecipientFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodPostalCodeRuleFields(GraphQLField):
    id: ShippingMethodPostalCodeRuleGraphQLField = (
        ShippingMethodPostalCodeRuleGraphQLField("id")
    )
    start: ShippingMethodPostalCodeRuleGraphQLField = (
        ShippingMethodPostalCodeRuleGraphQLField("start")
    )
    end: ShippingMethodPostalCodeRuleGraphQLField = (
        ShippingMethodPostalCodeRuleGraphQLField("end")
    )
    inclusion_type: ShippingMethodPostalCodeRuleGraphQLField = (
        ShippingMethodPostalCodeRuleGraphQLField("inclusionType")
    )

    def fields(
        self, *subfields: ShippingMethodPostalCodeRuleGraphQLField
    ) -> "ShippingMethodPostalCodeRuleFields":
        self._subfields.extend(subfields)
        return self


class AppDeleteFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    def fields(
        self, *subfields: Union[AppDeleteGraphQLField, "AppErrorFields", "AppFields"]
    ) -> "AppDeleteFields":
        self._subfields.extend(subfields)
        return self


class GiftCardSettingsUpdateFields(GraphQLField):
    @classmethod
    def gift_card_settings(cls) -> "GiftCardSettingsFields":
        return GiftCardSettingsFields("gift_card_settings")

    @classmethod
    def errors(cls) -> "GiftCardSettingsErrorFields":
        return GiftCardSettingsErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            GiftCardSettingsUpdateGraphQLField,
            "GiftCardSettingsErrorFields",
            "GiftCardSettingsFields",
        ]
    ) -> "GiftCardSettingsUpdateFields":
        self._subfields.extend(subfields)
        return self


class TaxExemptionManageFields(GraphQLField):
    taxable_object: TaxSourceObjectUnion = TaxSourceObjectUnion("taxableObject")

    @classmethod
    def errors(cls) -> "TaxExemptionManageErrorFields":
        return TaxExemptionManageErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TaxExemptionManageGraphQLField,
            "TaxExemptionManageErrorFields",
            "TaxSourceObjectUnion",
        ]
    ) -> "TaxExemptionManageFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    def fields(
        self,
        *subfields: Union[
            ShippingPriceTranslateGraphQLField,
            "TranslationErrorFields",
            "ShippingMethodTypeFields",
        ]
    ) -> "ShippingPriceTranslateFields":
        self._subfields.extend(subfields)
        return self


class ProductChannelListingFields(GraphQLField):
    id: ProductChannelListingGraphQLField = ProductChannelListingGraphQLField("id")
    publication_date: ProductChannelListingGraphQLField = (
        ProductChannelListingGraphQLField("publicationDate")
    )
    published_at: ProductChannelListingGraphQLField = ProductChannelListingGraphQLField(
        "publishedAt"
    )
    is_published: ProductChannelListingGraphQLField = ProductChannelListingGraphQLField(
        "isPublished"
    )

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    visible_in_listings: ProductChannelListingGraphQLField = (
        ProductChannelListingGraphQLField("visibleInListings")
    )
    available_for_purchase: ProductChannelListingGraphQLField = (
        ProductChannelListingGraphQLField("availableForPurchase")
    )
    available_for_purchase_at: ProductChannelListingGraphQLField = (
        ProductChannelListingGraphQLField("availableForPurchaseAt")
    )

    @classmethod
    def discounted_price(cls) -> "MoneyFields":
        return MoneyFields("discounted_price")

    @classmethod
    def purchase_cost(cls) -> "MoneyRangeFields":
        return MoneyRangeFields("purchase_cost")

    @classmethod
    def margin(cls) -> "MarginFields":
        return MarginFields("margin")

    is_available_for_purchase: ProductChannelListingGraphQLField = (
        ProductChannelListingGraphQLField("isAvailableForPurchase")
    )

    @classmethod
    def pricing(cls) -> "ProductPricingInfoFields":
        return ProductPricingInfoFields("pricing")

    def fields(
        self,
        *subfields: Union[
            ProductChannelListingGraphQLField,
            "MoneyRangeFields",
            "ProductPricingInfoFields",
            "MarginFields",
            "ChannelFields",
            "MoneyFields",
        ]
    ) -> "ProductChannelListingFields":
        self._subfields.extend(subfields)
        return self


class ProductCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "ProductCountableEdgeFields":
        return ProductCountableEdgeFields("edges")

    total_count: ProductCountableConnectionGraphQLField = (
        ProductCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            ProductCountableConnectionGraphQLField,
            "ProductCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "ProductCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class TranslationErrorFields(GraphQLField):
    field: TranslationErrorGraphQLField = TranslationErrorGraphQLField("field")
    message: TranslationErrorGraphQLField = TranslationErrorGraphQLField("message")
    code: TranslationErrorGraphQLField = TranslationErrorGraphQLField("code")

    def fields(
        self, *subfields: TranslationErrorGraphQLField
    ) -> "TranslationErrorFields":
        self._subfields.extend(subfields)
        return self


class VoucherCreateFields(GraphQLField):
    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    @classmethod
    def voucher(cls) -> "VoucherFields":
        return VoucherFields("voucher")

    def fields(
        self,
        *subfields: Union[
            VoucherCreateGraphQLField, "VoucherFields", "DiscountErrorFields"
        ]
    ) -> "VoucherCreateFields":
        self._subfields.extend(subfields)
        return self


class PaymentInitializedFields(GraphQLField):
    gateway: PaymentInitializedGraphQLField = PaymentInitializedGraphQLField("gateway")
    name: PaymentInitializedGraphQLField = PaymentInitializedGraphQLField("name")
    data: PaymentInitializedGraphQLField = PaymentInitializedGraphQLField("data")

    def fields(
        self, *subfields: PaymentInitializedGraphQLField
    ) -> "PaymentInitializedFields":
        self._subfields.extend(subfields)
        return self


class ImageFields(GraphQLField):
    url: ImageGraphQLField = ImageGraphQLField("url")
    alt: ImageGraphQLField = ImageGraphQLField("alt")

    def fields(self, *subfields: ImageGraphQLField) -> "ImageFields":
        self._subfields.extend(subfields)
        return self


class ProductAttributeUnassignFields(GraphQLField):
    @classmethod
    def product_type(cls) -> "ProductTypeFields":
        return ProductTypeFields("product_type")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductAttributeUnassignGraphQLField,
            "ProductTypeFields",
            "ProductErrorFields",
        ]
    ) -> "ProductAttributeUnassignFields":
        self._subfields.extend(subfields)
        return self


class AttributeTranslatableContentFields(GraphQLField):
    id: AttributeTranslatableContentGraphQLField = (
        AttributeTranslatableContentGraphQLField("id")
    )
    attribute_id: AttributeTranslatableContentGraphQLField = (
        AttributeTranslatableContentGraphQLField("attributeId")
    )
    name: AttributeTranslatableContentGraphQLField = (
        AttributeTranslatableContentGraphQLField("name")
    )

    @classmethod
    def translation(cls) -> "AttributeTranslationFields":
        return AttributeTranslationFields("translation")

    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    def fields(
        self,
        *subfields: Union[
            AttributeTranslatableContentGraphQLField,
            "AttributeFields",
            "AttributeTranslationFields",
        ]
    ) -> "AttributeTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ProductTypeFields":
        return ProductTypeFields("node")

    cursor: ProductTypeCountableEdgeGraphQLField = ProductTypeCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self,
        *subfields: Union[ProductTypeCountableEdgeGraphQLField, "ProductTypeFields"]
    ) -> "ProductTypeCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class AccountUpdateFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[AccountUpdateGraphQLField, "AccountErrorFields", "UserFields"]
    ) -> "AccountUpdateFields":
        self._subfields.extend(subfields)
        return self


class PromotionDeleteErrorFields(GraphQLField):
    field: PromotionDeleteErrorGraphQLField = PromotionDeleteErrorGraphQLField("field")
    message: PromotionDeleteErrorGraphQLField = PromotionDeleteErrorGraphQLField(
        "message"
    )
    code: PromotionDeleteErrorGraphQLField = PromotionDeleteErrorGraphQLField("code")

    def fields(
        self, *subfields: PromotionDeleteErrorGraphQLField
    ) -> "PromotionDeleteErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantChannelListingFields(GraphQLField):
    id: ProductVariantChannelListingGraphQLField = (
        ProductVariantChannelListingGraphQLField("id")
    )

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def price(cls) -> "MoneyFields":
        return MoneyFields("price")

    @classmethod
    def cost_price(cls) -> "MoneyFields":
        return MoneyFields("cost_price")

    margin: ProductVariantChannelListingGraphQLField = (
        ProductVariantChannelListingGraphQLField("margin")
    )

    @classmethod
    def preorder_threshold(cls) -> "PreorderThresholdFields":
        return PreorderThresholdFields("preorder_threshold")

    def fields(
        self,
        *subfields: Union[
            ProductVariantChannelListingGraphQLField,
            "ChannelFields",
            "PreorderThresholdFields",
            "MoneyFields",
        ]
    ) -> "ProductVariantChannelListingFields":
        self._subfields.extend(subfields)
        return self


class CheckoutPaymentCreateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def payment(cls) -> "PaymentFields":
        return PaymentFields("payment")

    @classmethod
    def payment_errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("payment_errors")

    @classmethod
    def errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutPaymentCreateGraphQLField,
            "PaymentFields",
            "PaymentErrorFields",
            "CheckoutFields",
        ]
    ) -> "CheckoutPaymentCreateFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayInitializeTokenizationErrorFields(GraphQLField):
    field: PaymentGatewayInitializeTokenizationErrorGraphQLField = (
        PaymentGatewayInitializeTokenizationErrorGraphQLField("field")
    )
    message: PaymentGatewayInitializeTokenizationErrorGraphQLField = (
        PaymentGatewayInitializeTokenizationErrorGraphQLField("message")
    )
    code: PaymentGatewayInitializeTokenizationErrorGraphQLField = (
        PaymentGatewayInitializeTokenizationErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: PaymentGatewayInitializeTokenizationErrorGraphQLField
    ) -> "PaymentGatewayInitializeTokenizationErrorFields":
        self._subfields.extend(subfields)
        return self


class CheckoutLinesUpdateFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutLinesUpdateGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutLinesUpdateFields":
        self._subfields.extend(subfields)
        return self


class AttributeTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    def fields(
        self,
        *subfields: Union[
            AttributeTranslateGraphQLField, "AttributeFields", "TranslationErrorFields"
        ]
    ) -> "AttributeTranslateFields":
        self._subfields.extend(subfields)
        return self


class MenuItemTranslatableContentFields(GraphQLField):
    id: MenuItemTranslatableContentGraphQLField = (
        MenuItemTranslatableContentGraphQLField("id")
    )
    menu_item_id: MenuItemTranslatableContentGraphQLField = (
        MenuItemTranslatableContentGraphQLField("menuItemId")
    )
    name: MenuItemTranslatableContentGraphQLField = (
        MenuItemTranslatableContentGraphQLField("name")
    )

    @classmethod
    def translation(cls) -> "MenuItemTranslationFields":
        return MenuItemTranslationFields("translation")

    @classmethod
    def menu_item(cls) -> "MenuItemFields":
        return MenuItemFields("menu_item")

    def fields(
        self,
        *subfields: Union[
            MenuItemTranslatableContentGraphQLField,
            "MenuItemFields",
            "MenuItemTranslationFields",
        ]
    ) -> "MenuItemTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class VoucherFields(GraphQLField):
    id: VoucherGraphQLField = VoucherGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: VoucherGraphQLField = VoucherGraphQLField("privateMetafield")
    private_metafields: VoucherGraphQLField = VoucherGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: VoucherGraphQLField = VoucherGraphQLField("metafield")
    metafields: VoucherGraphQLField = VoucherGraphQLField("metafields")
    name: VoucherGraphQLField = VoucherGraphQLField("name")

    @classmethod
    def codes(cls) -> "VoucherCodeCountableConnectionFields":
        return VoucherCodeCountableConnectionFields("codes")

    code: VoucherGraphQLField = VoucherGraphQLField("code")
    usage_limit: VoucherGraphQLField = VoucherGraphQLField("usageLimit")
    used: VoucherGraphQLField = VoucherGraphQLField("used")
    start_date: VoucherGraphQLField = VoucherGraphQLField("startDate")
    end_date: VoucherGraphQLField = VoucherGraphQLField("endDate")
    apply_once_per_order: VoucherGraphQLField = VoucherGraphQLField("applyOncePerOrder")
    apply_once_per_customer: VoucherGraphQLField = VoucherGraphQLField(
        "applyOncePerCustomer"
    )
    single_use: VoucherGraphQLField = VoucherGraphQLField("singleUse")
    only_for_staff: VoucherGraphQLField = VoucherGraphQLField("onlyForStaff")
    min_checkout_items_quantity: VoucherGraphQLField = VoucherGraphQLField(
        "minCheckoutItemsQuantity"
    )

    @classmethod
    def categories(cls) -> "CategoryCountableConnectionFields":
        return CategoryCountableConnectionFields("categories")

    @classmethod
    def collections(cls) -> "CollectionCountableConnectionFields":
        return CollectionCountableConnectionFields("collections")

    @classmethod
    def products(cls) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields("products")

    @classmethod
    def variants(cls) -> "ProductVariantCountableConnectionFields":
        return ProductVariantCountableConnectionFields("variants")

    @classmethod
    def countries(cls) -> "CountryDisplayFields":
        return CountryDisplayFields("countries")

    @classmethod
    def translation(cls) -> "VoucherTranslationFields":
        return VoucherTranslationFields("translation")

    discount_value_type: VoucherGraphQLField = VoucherGraphQLField("discountValueType")
    discount_value: VoucherGraphQLField = VoucherGraphQLField("discountValue")
    currency: VoucherGraphQLField = VoucherGraphQLField("currency")

    @classmethod
    def min_spent(cls) -> "MoneyFields":
        return MoneyFields("min_spent")

    type: VoucherGraphQLField = VoucherGraphQLField("type")

    @classmethod
    def channel_listings(cls) -> "VoucherChannelListingFields":
        return VoucherChannelListingFields("channel_listings")

    def fields(
        self,
        *subfields: Union[
            VoucherGraphQLField,
            "VoucherChannelListingFields",
            "CollectionCountableConnectionFields",
            "MetadataItemFields",
            "ProductCountableConnectionFields",
            "VoucherCodeCountableConnectionFields",
            "CountryDisplayFields",
            "VoucherTranslationFields",
            "MoneyFields",
            "CategoryCountableConnectionFields",
            "ProductVariantCountableConnectionFields",
        ]
    ) -> "VoucherFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleCreatedEventFields(GraphQLField):
    id: PromotionRuleCreatedEventGraphQLField = PromotionRuleCreatedEventGraphQLField(
        "id"
    )
    date: PromotionRuleCreatedEventGraphQLField = PromotionRuleCreatedEventGraphQLField(
        "date"
    )
    type: PromotionRuleCreatedEventGraphQLField = PromotionRuleCreatedEventGraphQLField(
        "type"
    )
    created_by: UserOrAppUnion = UserOrAppUnion("createdBy")
    rule_id: PromotionRuleCreatedEventGraphQLField = (
        PromotionRuleCreatedEventGraphQLField("ruleId")
    )

    def fields(
        self, *subfields: Union[PromotionRuleCreatedEventGraphQLField, "UserOrAppUnion"]
    ) -> "PromotionRuleCreatedEventFields":
        self._subfields.extend(subfields)
        return self


class VoucherCodeCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "VoucherCodeFields":
        return VoucherCodeFields("node")

    cursor: VoucherCodeCountableEdgeGraphQLField = VoucherCodeCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self,
        *subfields: Union[VoucherCodeCountableEdgeGraphQLField, "VoucherCodeFields"]
    ) -> "VoucherCodeCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class AppTokenVerifyFields(GraphQLField):
    valid: AppTokenVerifyGraphQLField = AppTokenVerifyGraphQLField("valid")

    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    def fields(
        self, *subfields: Union[AppTokenVerifyGraphQLField, "AppErrorFields"]
    ) -> "AppTokenVerifyFields":
        self._subfields.extend(subfields)
        return self


class GiftCardTagFields(GraphQLField):
    id: GiftCardTagGraphQLField = GiftCardTagGraphQLField("id")
    name: GiftCardTagGraphQLField = GiftCardTagGraphQLField("name")

    def fields(self, *subfields: GiftCardTagGraphQLField) -> "GiftCardTagFields":
        self._subfields.extend(subfields)
        return self


class DraftOrderUpdateFields(GraphQLField):
    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    def fields(
        self,
        *subfields: Union[
            DraftOrderUpdateGraphQLField, "OrderErrorFields", "OrderFields"
        ]
    ) -> "DraftOrderUpdateFields":
        self._subfields.extend(subfields)
        return self


class ProductChannelListingUpdateFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def product_channel_listing_errors(cls) -> "ProductChannelListingErrorFields":
        return ProductChannelListingErrorFields("product_channel_listing_errors")

    @classmethod
    def errors(cls) -> "ProductChannelListingErrorFields":
        return ProductChannelListingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductChannelListingUpdateGraphQLField,
            "ProductFields",
            "ProductChannelListingErrorFields",
        ]
    ) -> "ProductChannelListingUpdateFields":
        self._subfields.extend(subfields)
        return self


class GiftCardTagCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "GiftCardTagCountableEdgeFields":
        return GiftCardTagCountableEdgeFields("edges")

    total_count: GiftCardTagCountableConnectionGraphQLField = (
        GiftCardTagCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            GiftCardTagCountableConnectionGraphQLField,
            "GiftCardTagCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "GiftCardTagCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkCreateFields(GraphQLField):
    count: AttributeBulkCreateGraphQLField = AttributeBulkCreateGraphQLField("count")

    @classmethod
    def results(cls) -> "AttributeBulkCreateResultFields":
        return AttributeBulkCreateResultFields("results")

    @classmethod
    def errors(cls) -> "AttributeBulkCreateErrorFields":
        return AttributeBulkCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeBulkCreateGraphQLField,
            "AttributeBulkCreateErrorFields",
            "AttributeBulkCreateResultFields",
        ]
    ) -> "AttributeBulkCreateFields":
        self._subfields.extend(subfields)
        return self


class AccountRegisterFields(GraphQLField):
    requires_confirmation: AccountRegisterGraphQLField = AccountRegisterGraphQLField(
        "requiresConfirmation"
    )

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[
            AccountRegisterGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "AccountRegisterFields":
        self._subfields.extend(subfields)
        return self


class AssignedVariantAttributeFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    variant_selection: AssignedVariantAttributeGraphQLField = (
        AssignedVariantAttributeGraphQLField("variantSelection")
    )

    def fields(
        self, *subfields: Union[AssignedVariantAttributeGraphQLField, "AttributeFields"]
    ) -> "AssignedVariantAttributeFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueCreateFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    @classmethod
    def attribute_value(cls) -> "AttributeValueFields":
        return AttributeValueFields("attribute_value")

    def fields(
        self,
        *subfields: Union[
            AttributeValueCreateGraphQLField,
            "AttributeFields",
            "AttributeValueFields",
            "AttributeErrorFields",
        ]
    ) -> "AttributeValueCreateFields":
        self._subfields.extend(subfields)
        return self


class OrderBulkCreateFields(GraphQLField):
    count: OrderBulkCreateGraphQLField = OrderBulkCreateGraphQLField("count")

    @classmethod
    def results(cls) -> "OrderBulkCreateResultFields":
        return OrderBulkCreateResultFields("results")

    @classmethod
    def errors(cls) -> "OrderBulkCreateErrorFields":
        return OrderBulkCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderBulkCreateGraphQLField,
            "OrderBulkCreateErrorFields",
            "OrderBulkCreateResultFields",
        ]
    ) -> "OrderBulkCreateFields":
        self._subfields.extend(subfields)
        return self


class MenuItemTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def menu_item(cls) -> "MenuItemFields":
        return MenuItemFields("menu_item")

    def fields(
        self,
        *subfields: Union[
            MenuItemTranslateGraphQLField, "TranslationErrorFields", "MenuItemFields"
        ]
    ) -> "MenuItemTranslateFields":
        self._subfields.extend(subfields)
        return self


class AttributeCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "AttributeFields":
        return AttributeFields("node")

    cursor: AttributeCountableEdgeGraphQLField = AttributeCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[AttributeCountableEdgeGraphQLField, "AttributeFields"]
    ) -> "AttributeCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class GiftCardCreateFields(GraphQLField):
    @classmethod
    def gift_card_errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("gift_card_errors")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    def fields(
        self,
        *subfields: Union[
            GiftCardCreateGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardCreateFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantStocksCreateFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def bulk_stock_errors(cls) -> "BulkStockErrorFields":
        return BulkStockErrorFields("bulk_stock_errors")

    @classmethod
    def errors(cls) -> "BulkStockErrorFields":
        return BulkStockErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantStocksCreateGraphQLField,
            "BulkStockErrorFields",
            "ProductVariantFields",
        ]
    ) -> "ProductVariantStocksCreateFields":
        self._subfields.extend(subfields)
        return self


class TaxCountryConfigurationDeleteErrorFields(GraphQLField):
    field: TaxCountryConfigurationDeleteErrorGraphQLField = (
        TaxCountryConfigurationDeleteErrorGraphQLField("field")
    )
    message: TaxCountryConfigurationDeleteErrorGraphQLField = (
        TaxCountryConfigurationDeleteErrorGraphQLField("message")
    )
    code: TaxCountryConfigurationDeleteErrorGraphQLField = (
        TaxCountryConfigurationDeleteErrorGraphQLField("code")
    )

    def fields(
        self, *subfields: TaxCountryConfigurationDeleteErrorGraphQLField
    ) -> "TaxCountryConfigurationDeleteErrorFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleTranslatableContentFields(GraphQLField):
    id: PromotionRuleTranslatableContentGraphQLField = (
        PromotionRuleTranslatableContentGraphQLField("id")
    )
    promotion_rule_id: PromotionRuleTranslatableContentGraphQLField = (
        PromotionRuleTranslatableContentGraphQLField("promotionRuleId")
    )
    name: PromotionRuleTranslatableContentGraphQLField = (
        PromotionRuleTranslatableContentGraphQLField("name")
    )
    description: PromotionRuleTranslatableContentGraphQLField = (
        PromotionRuleTranslatableContentGraphQLField("description")
    )

    @classmethod
    def translation(cls) -> "PromotionRuleTranslationFields":
        return PromotionRuleTranslationFields("translation")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleTranslatableContentGraphQLField,
            "PromotionRuleTranslationFields",
        ]
    ) -> "PromotionRuleTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class OrderNoteAddErrorFields(GraphQLField):
    field: OrderNoteAddErrorGraphQLField = OrderNoteAddErrorGraphQLField("field")
    message: OrderNoteAddErrorGraphQLField = OrderNoteAddErrorGraphQLField("message")
    code: OrderNoteAddErrorGraphQLField = OrderNoteAddErrorGraphQLField("code")

    def fields(
        self, *subfields: OrderNoteAddErrorGraphQLField
    ) -> "OrderNoteAddErrorFields":
        self._subfields.extend(subfields)
        return self


class AppInstallFields(GraphQLField):
    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app_installation(cls) -> "AppInstallationFields":
        return AppInstallationFields("app_installation")

    def fields(
        self,
        *subfields: Union[
            AppInstallGraphQLField, "AppErrorFields", "AppInstallationFields"
        ]
    ) -> "AppInstallFields":
        self._subfields.extend(subfields)
        return self


class PageTypeCreateFields(GraphQLField):
    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    def fields(
        self,
        *subfields: Union[
            PageTypeCreateGraphQLField, "PageTypeFields", "PageErrorFields"
        ]
    ) -> "PageTypeCreateFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkDeleteFields(GraphQLField):
    count: AttributeBulkDeleteGraphQLField = AttributeBulkDeleteGraphQLField("count")

    @classmethod
    def attribute_errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("attribute_errors")

    @classmethod
    def errors(cls) -> "AttributeErrorFields":
        return AttributeErrorFields("errors")

    def fields(
        self, *subfields: Union[AttributeBulkDeleteGraphQLField, "AttributeErrorFields"]
    ) -> "AttributeBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class MenuItemMoveFields(GraphQLField):
    @classmethod
    def menu(cls) -> "MenuFields":
        return MenuFields("menu")

    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    def fields(
        self,
        *subfields: Union[MenuItemMoveGraphQLField, "MenuFields", "MenuErrorFields"]
    ) -> "MenuItemMoveFields":
        self._subfields.extend(subfields)
        return self


class GiftCardResendFields(GraphQLField):
    @classmethod
    def gift_card(cls) -> "GiftCardFields":
        return GiftCardFields("gift_card")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            GiftCardResendGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardResendFields":
        self._subfields.extend(subfields)
        return self


class CollectionFields(GraphQLField):
    id: CollectionGraphQLField = CollectionGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: CollectionGraphQLField = CollectionGraphQLField(
        "privateMetafield"
    )
    private_metafields: CollectionGraphQLField = CollectionGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: CollectionGraphQLField = CollectionGraphQLField("metafield")
    metafields: CollectionGraphQLField = CollectionGraphQLField("metafields")
    seo_title: CollectionGraphQLField = CollectionGraphQLField("seoTitle")
    seo_description: CollectionGraphQLField = CollectionGraphQLField("seoDescription")
    name: CollectionGraphQLField = CollectionGraphQLField("name")
    description: CollectionGraphQLField = CollectionGraphQLField("description")
    slug: CollectionGraphQLField = CollectionGraphQLField("slug")
    channel: CollectionGraphQLField = CollectionGraphQLField("channel")
    description_json: CollectionGraphQLField = CollectionGraphQLField("descriptionJson")

    @classmethod
    def products(cls) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields("products")

    @classmethod
    def background_image(cls) -> "ImageFields":
        return ImageFields("background_image")

    @classmethod
    def translation(cls) -> "CollectionTranslationFields":
        return CollectionTranslationFields("translation")

    @classmethod
    def channel_listings(cls) -> "CollectionChannelListingFields":
        return CollectionChannelListingFields("channel_listings")

    def fields(
        self,
        *subfields: Union[
            CollectionGraphQLField,
            "MetadataItemFields",
            "ProductCountableConnectionFields",
            "CollectionChannelListingFields",
            "CollectionTranslationFields",
            "ImageFields",
        ]
    ) -> "CollectionFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentApproveFields(GraphQLField):
    @classmethod
    def fulfillment(cls) -> "FulfillmentFields":
        return FulfillmentFields("fulfillment")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            FulfillmentApproveGraphQLField,
            "FulfillmentFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "FulfillmentApproveFields":
        self._subfields.extend(subfields)
        return self


class TaxClassCreateErrorFields(GraphQLField):
    field: TaxClassCreateErrorGraphQLField = TaxClassCreateErrorGraphQLField("field")
    message: TaxClassCreateErrorGraphQLField = TaxClassCreateErrorGraphQLField(
        "message"
    )
    code: TaxClassCreateErrorGraphQLField = TaxClassCreateErrorGraphQLField("code")
    country_codes: TaxClassCreateErrorGraphQLField = TaxClassCreateErrorGraphQLField(
        "countryCodes"
    )

    def fields(
        self, *subfields: TaxClassCreateErrorGraphQLField
    ) -> "TaxClassCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class CustomerDeleteFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[
            CustomerDeleteGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "CustomerDeleteFields":
        self._subfields.extend(subfields)
        return self


class GiftCardErrorFields(GraphQLField):
    field: GiftCardErrorGraphQLField = GiftCardErrorGraphQLField("field")
    message: GiftCardErrorGraphQLField = GiftCardErrorGraphQLField("message")
    code: GiftCardErrorGraphQLField = GiftCardErrorGraphQLField("code")
    tags: GiftCardErrorGraphQLField = GiftCardErrorGraphQLField("tags")

    def fields(self, *subfields: GiftCardErrorGraphQLField) -> "GiftCardErrorFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentFields(GraphQLField):
    id: FulfillmentGraphQLField = FulfillmentGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: FulfillmentGraphQLField = FulfillmentGraphQLField(
        "privateMetafield"
    )
    private_metafields: FulfillmentGraphQLField = FulfillmentGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: FulfillmentGraphQLField = FulfillmentGraphQLField("metafield")
    metafields: FulfillmentGraphQLField = FulfillmentGraphQLField("metafields")
    fulfillment_order: FulfillmentGraphQLField = FulfillmentGraphQLField(
        "fulfillmentOrder"
    )
    status: FulfillmentGraphQLField = FulfillmentGraphQLField("status")
    tracking_number: FulfillmentGraphQLField = FulfillmentGraphQLField("trackingNumber")
    created: FulfillmentGraphQLField = FulfillmentGraphQLField("created")

    @classmethod
    def lines(cls) -> "FulfillmentLineFields":
        return FulfillmentLineFields("lines")

    status_display: FulfillmentGraphQLField = FulfillmentGraphQLField("statusDisplay")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    @classmethod
    def shipping_refunded_amount(cls) -> "MoneyFields":
        return MoneyFields("shipping_refunded_amount")

    @classmethod
    def total_refunded_amount(cls) -> "MoneyFields":
        return MoneyFields("total_refunded_amount")

    def fields(
        self,
        *subfields: Union[
            FulfillmentGraphQLField,
            "FulfillmentLineFields",
            "MetadataItemFields",
            "WarehouseFields",
            "MoneyFields",
        ]
    ) -> "FulfillmentFields":
        self._subfields.extend(subfields)
        return self


class PageErrorFields(GraphQLField):
    field: PageErrorGraphQLField = PageErrorGraphQLField("field")
    message: PageErrorGraphQLField = PageErrorGraphQLField("message")
    code: PageErrorGraphQLField = PageErrorGraphQLField("code")
    attributes: PageErrorGraphQLField = PageErrorGraphQLField("attributes")
    values: PageErrorGraphQLField = PageErrorGraphQLField("values")

    def fields(self, *subfields: PageErrorGraphQLField) -> "PageErrorFields":
        self._subfields.extend(subfields)
        return self


class DeactivateAllUserTokensFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[DeactivateAllUserTokensGraphQLField, "AccountErrorFields"]
    ) -> "DeactivateAllUserTokensFields":
        self._subfields.extend(subfields)
        return self


class ProductTypeCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "ProductTypeCountableEdgeFields":
        return ProductTypeCountableEdgeFields("edges")

    total_count: ProductTypeCountableConnectionGraphQLField = (
        ProductTypeCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            ProductTypeCountableConnectionGraphQLField,
            "ProductTypeCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "ProductTypeCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class AppTokenFields(GraphQLField):
    id: AppTokenGraphQLField = AppTokenGraphQLField("id")
    name: AppTokenGraphQLField = AppTokenGraphQLField("name")
    auth_token: AppTokenGraphQLField = AppTokenGraphQLField("authToken")

    def fields(self, *subfields: AppTokenGraphQLField) -> "AppTokenFields":
        self._subfields.extend(subfields)
        return self


class OrderSettingsFields(GraphQLField):
    automatically_confirm_all_new_orders: OrderSettingsGraphQLField = (
        OrderSettingsGraphQLField("automaticallyConfirmAllNewOrders")
    )
    automatically_fulfill_non_shippable_gift_card: OrderSettingsGraphQLField = (
        OrderSettingsGraphQLField("automaticallyFulfillNonShippableGiftCard")
    )
    expire_orders_after: OrderSettingsGraphQLField = OrderSettingsGraphQLField(
        "expireOrdersAfter"
    )
    mark_as_paid_strategy: OrderSettingsGraphQLField = OrderSettingsGraphQLField(
        "markAsPaidStrategy"
    )
    delete_expired_orders_after: OrderSettingsGraphQLField = OrderSettingsGraphQLField(
        "deleteExpiredOrdersAfter"
    )
    allow_unpaid_orders: OrderSettingsGraphQLField = OrderSettingsGraphQLField(
        "allowUnpaidOrders"
    )
    include_draft_order_in_voucher_usage: OrderSettingsGraphQLField = (
        OrderSettingsGraphQLField("includeDraftOrderInVoucherUsage")
    )

    def fields(self, *subfields: OrderSettingsGraphQLField) -> "OrderSettingsFields":
        self._subfields.extend(subfields)
        return self


class ProductTranslationFields(GraphQLField):
    id: ProductTranslationGraphQLField = ProductTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    seo_title: ProductTranslationGraphQLField = ProductTranslationGraphQLField(
        "seoTitle"
    )
    seo_description: ProductTranslationGraphQLField = ProductTranslationGraphQLField(
        "seoDescription"
    )
    name: ProductTranslationGraphQLField = ProductTranslationGraphQLField("name")
    description: ProductTranslationGraphQLField = ProductTranslationGraphQLField(
        "description"
    )
    description_json: ProductTranslationGraphQLField = ProductTranslationGraphQLField(
        "descriptionJson"
    )

    @classmethod
    def translatable_content(cls) -> "ProductTranslatableContentFields":
        return ProductTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            ProductTranslationGraphQLField,
            "ProductTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "ProductTranslationFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodsPerCountryFields(GraphQLField):
    country_code: ShippingMethodsPerCountryGraphQLField = (
        ShippingMethodsPerCountryGraphQLField("countryCode")
    )

    @classmethod
    def shipping_methods(cls) -> "ShippingMethodFields":
        return ShippingMethodFields("shipping_methods")

    def fields(
        self,
        *subfields: Union[ShippingMethodsPerCountryGraphQLField, "ShippingMethodFields"]
    ) -> "ShippingMethodsPerCountryFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodChannelListingFields(GraphQLField):
    id: ShippingMethodChannelListingGraphQLField = (
        ShippingMethodChannelListingGraphQLField("id")
    )

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def maximum_order_price(cls) -> "MoneyFields":
        return MoneyFields("maximum_order_price")

    @classmethod
    def minimum_order_price(cls) -> "MoneyFields":
        return MoneyFields("minimum_order_price")

    @classmethod
    def price(cls) -> "MoneyFields":
        return MoneyFields("price")

    def fields(
        self,
        *subfields: Union[
            ShippingMethodChannelListingGraphQLField, "ChannelFields", "MoneyFields"
        ]
    ) -> "ShippingMethodChannelListingFields":
        self._subfields.extend(subfields)
        return self


class SaleCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "SaleFields":
        return SaleFields("node")

    cursor: SaleCountableEdgeGraphQLField = SaleCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[SaleCountableEdgeGraphQLField, "SaleFields"]
    ) -> "SaleCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantStocksUpdateFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def bulk_stock_errors(cls) -> "BulkStockErrorFields":
        return BulkStockErrorFields("bulk_stock_errors")

    @classmethod
    def errors(cls) -> "BulkStockErrorFields":
        return BulkStockErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantStocksUpdateGraphQLField,
            "BulkStockErrorFields",
            "ProductVariantFields",
        ]
    ) -> "ProductVariantStocksUpdateFields":
        self._subfields.extend(subfields)
        return self


class ExternalAuthenticationFields(GraphQLField):
    id: ExternalAuthenticationGraphQLField = ExternalAuthenticationGraphQLField("id")
    name: ExternalAuthenticationGraphQLField = ExternalAuthenticationGraphQLField(
        "name"
    )

    def fields(
        self, *subfields: ExternalAuthenticationGraphQLField
    ) -> "ExternalAuthenticationFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantBulkTranslateFields(GraphQLField):
    count: ProductVariantBulkTranslateGraphQLField = (
        ProductVariantBulkTranslateGraphQLField("count")
    )

    @classmethod
    def results(cls) -> "ProductVariantBulkTranslateResultFields":
        return ProductVariantBulkTranslateResultFields("results")

    @classmethod
    def errors(cls) -> "ProductVariantBulkTranslateErrorFields":
        return ProductVariantBulkTranslateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantBulkTranslateGraphQLField,
            "ProductVariantBulkTranslateErrorFields",
            "ProductVariantBulkTranslateResultFields",
        ]
    ) -> "ProductVariantBulkTranslateFields":
        self._subfields.extend(subfields)
        return self


class ExternalVerifyFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    is_valid: ExternalVerifyGraphQLField = ExternalVerifyGraphQLField("isValid")
    verify_data: ExternalVerifyGraphQLField = ExternalVerifyGraphQLField("verifyData")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ExternalVerifyGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "ExternalVerifyFields":
        self._subfields.extend(subfields)
        return self


class CollectionCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "CollectionCountableEdgeFields":
        return CollectionCountableEdgeFields("edges")

    total_count: CollectionCountableConnectionGraphQLField = (
        CollectionCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            CollectionCountableConnectionGraphQLField,
            "CollectionCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "CollectionCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class ProductBulkCreateFields(GraphQLField):
    count: ProductBulkCreateGraphQLField = ProductBulkCreateGraphQLField("count")

    @classmethod
    def results(cls) -> "ProductBulkResultFields":
        return ProductBulkResultFields("results")

    @classmethod
    def errors(cls) -> "ProductBulkCreateErrorFields":
        return ProductBulkCreateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductBulkCreateGraphQLField,
            "ProductBulkResultFields",
            "ProductBulkCreateErrorFields",
        ]
    ) -> "ProductBulkCreateFields":
        self._subfields.extend(subfields)
        return self


class TransactionEventReportFields(GraphQLField):
    already_processed: TransactionEventReportGraphQLField = (
        TransactionEventReportGraphQLField("alreadyProcessed")
    )

    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def transaction_event(cls) -> "TransactionEventFields":
        return TransactionEventFields("transaction_event")

    @classmethod
    def errors(cls) -> "TransactionEventReportErrorFields":
        return TransactionEventReportErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionEventReportGraphQLField,
            "TransactionItemFields",
            "TransactionEventFields",
            "TransactionEventReportErrorFields",
        ]
    ) -> "TransactionEventReportFields":
        self._subfields.extend(subfields)
        return self


class RequestEmailChangeFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            RequestEmailChangeGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "RequestEmailChangeFields":
        self._subfields.extend(subfields)
        return self


class OrderEventOrderLineObjectFields(GraphQLField):
    quantity: OrderEventOrderLineObjectGraphQLField = (
        OrderEventOrderLineObjectGraphQLField("quantity")
    )

    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    item_name: OrderEventOrderLineObjectGraphQLField = (
        OrderEventOrderLineObjectGraphQLField("itemName")
    )

    @classmethod
    def discount(cls) -> "OrderEventDiscountObjectFields":
        return OrderEventDiscountObjectFields("discount")

    def fields(
        self,
        *subfields: Union[
            OrderEventOrderLineObjectGraphQLField,
            "OrderEventDiscountObjectFields",
            "OrderLineFields",
        ]
    ) -> "OrderEventOrderLineObjectFields":
        self._subfields.extend(subfields)
        return self


class TaxCountryConfigurationUpdateFields(GraphQLField):
    @classmethod
    def tax_country_configuration(cls) -> "TaxCountryConfigurationFields":
        return TaxCountryConfigurationFields("tax_country_configuration")

    @classmethod
    def errors(cls) -> "TaxCountryConfigurationUpdateErrorFields":
        return TaxCountryConfigurationUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TaxCountryConfigurationUpdateGraphQLField,
            "TaxCountryConfigurationUpdateErrorFields",
            "TaxCountryConfigurationFields",
        ]
    ) -> "TaxCountryConfigurationUpdateFields":
        self._subfields.extend(subfields)
        return self


class SaleChannelListingUpdateFields(GraphQLField):
    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            SaleChannelListingUpdateGraphQLField, "SaleFields", "DiscountErrorFields"
        ]
    ) -> "SaleChannelListingUpdateFields":
        self._subfields.extend(subfields)
        return self


class OrderLineDiscountRemoveFields(GraphQLField):
    @classmethod
    def order_line(cls) -> "OrderLineFields":
        return OrderLineFields("order_line")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderLineDiscountRemoveGraphQLField,
            "OrderErrorFields",
            "OrderFields",
            "OrderLineFields",
        ]
    ) -> "OrderLineDiscountRemoveFields":
        self._subfields.extend(subfields)
        return self


class StockBulkUpdateFields(GraphQLField):
    count: StockBulkUpdateGraphQLField = StockBulkUpdateGraphQLField("count")

    @classmethod
    def results(cls) -> "StockBulkResultFields":
        return StockBulkResultFields("results")

    @classmethod
    def errors(cls) -> "StockBulkUpdateErrorFields":
        return StockBulkUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            StockBulkUpdateGraphQLField,
            "StockBulkResultFields",
            "StockBulkUpdateErrorFields",
        ]
    ) -> "StockBulkUpdateFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentRefundProductsFields(GraphQLField):
    @classmethod
    def fulfillment(cls) -> "FulfillmentFields":
        return FulfillmentFields("fulfillment")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            FulfillmentRefundProductsGraphQLField,
            "FulfillmentFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "FulfillmentRefundProductsFields":
        self._subfields.extend(subfields)
        return self


class GiftCardCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "GiftCardFields":
        return GiftCardFields("node")

    cursor: GiftCardCountableEdgeGraphQLField = GiftCardCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[GiftCardCountableEdgeGraphQLField, "GiftCardFields"]
    ) -> "GiftCardCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class VariantMediaUnassignFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def media(cls) -> "ProductMediaFields":
        return ProductMediaFields("media")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            VariantMediaUnassignGraphQLField,
            "ProductMediaFields",
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "VariantMediaUnassignFields":
        self._subfields.extend(subfields)
        return self


class AccountDeleteFields(GraphQLField):
    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    def fields(
        self,
        *subfields: Union[AccountDeleteGraphQLField, "AccountErrorFields", "UserFields"]
    ) -> "AccountDeleteFields":
        self._subfields.extend(subfields)
        return self


class PageBulkPublishFields(GraphQLField):
    count: PageBulkPublishGraphQLField = PageBulkPublishGraphQLField("count")

    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    def fields(
        self, *subfields: Union[PageBulkPublishGraphQLField, "PageErrorFields"]
    ) -> "PageBulkPublishFields":
        self._subfields.extend(subfields)
        return self


class ShopErrorFields(GraphQLField):
    field: ShopErrorGraphQLField = ShopErrorGraphQLField("field")
    message: ShopErrorGraphQLField = ShopErrorGraphQLField("message")
    code: ShopErrorGraphQLField = ShopErrorGraphQLField("code")

    def fields(self, *subfields: ShopErrorGraphQLField) -> "ShopErrorFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentDeleteFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("variant")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            DigitalContentDeleteGraphQLField,
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "DigitalContentDeleteFields":
        self._subfields.extend(subfields)
        return self


class PromotionFields(GraphQLField):
    id: PromotionGraphQLField = PromotionGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: PromotionGraphQLField = PromotionGraphQLField("privateMetafield")
    private_metafields: PromotionGraphQLField = PromotionGraphQLField(
        "privateMetafields"
    )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: PromotionGraphQLField = PromotionGraphQLField("metafield")
    metafields: PromotionGraphQLField = PromotionGraphQLField("metafields")
    name: PromotionGraphQLField = PromotionGraphQLField("name")
    type: PromotionGraphQLField = PromotionGraphQLField("type")
    description: PromotionGraphQLField = PromotionGraphQLField("description")
    start_date: PromotionGraphQLField = PromotionGraphQLField("startDate")
    end_date: PromotionGraphQLField = PromotionGraphQLField("endDate")
    created_at: PromotionGraphQLField = PromotionGraphQLField("createdAt")
    updated_at: PromotionGraphQLField = PromotionGraphQLField("updatedAt")

    @classmethod
    def rules(cls) -> "PromotionRuleFields":
        return PromotionRuleFields("rules")

    @classmethod
    def translation(cls) -> "PromotionTranslationFields":
        return PromotionTranslationFields("translation")

    events: PromotionEventUnion = PromotionEventUnion("events")

    def fields(
        self,
        *subfields: Union[
            PromotionGraphQLField,
            "MetadataItemFields",
            "PromotionRuleFields",
            "PromotionTranslationFields",
            "PromotionEventUnion",
        ]
    ) -> "PromotionFields":
        self._subfields.extend(subfields)
        return self


class ShippingErrorFields(GraphQLField):
    field: ShippingErrorGraphQLField = ShippingErrorGraphQLField("field")
    message: ShippingErrorGraphQLField = ShippingErrorGraphQLField("message")
    code: ShippingErrorGraphQLField = ShippingErrorGraphQLField("code")
    warehouses: ShippingErrorGraphQLField = ShippingErrorGraphQLField("warehouses")
    channels: ShippingErrorGraphQLField = ShippingErrorGraphQLField("channels")

    def fields(self, *subfields: ShippingErrorGraphQLField) -> "ShippingErrorFields":
        self._subfields.extend(subfields)
        return self


class GiftCardSettingsFields(GraphQLField):
    expiry_type: GiftCardSettingsGraphQLField = GiftCardSettingsGraphQLField(
        "expiryType"
    )

    @classmethod
    def expiry_period(cls) -> "TimePeriodFields":
        return TimePeriodFields("expiry_period")

    def fields(
        self, *subfields: Union[GiftCardSettingsGraphQLField, "TimePeriodFields"]
    ) -> "GiftCardSettingsFields":
        self._subfields.extend(subfields)
        return self


class ConfirmEmailChangeFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ConfirmEmailChangeGraphQLField, "AccountErrorFields", "UserFields"
        ]
    ) -> "ConfirmEmailChangeFields":
        self._subfields.extend(subfields)
        return self


class PermissionGroupUpdateFields(GraphQLField):
    @classmethod
    def permission_group_errors(cls) -> "PermissionGroupErrorFields":
        return PermissionGroupErrorFields("permission_group_errors")

    @classmethod
    def errors(cls) -> "PermissionGroupErrorFields":
        return PermissionGroupErrorFields("errors")

    @classmethod
    def group(cls) -> "GroupFields":
        return GroupFields("group")

    def fields(
        self,
        *subfields: Union[
            PermissionGroupUpdateGraphQLField,
            "PermissionGroupErrorFields",
            "GroupFields",
        ]
    ) -> "PermissionGroupUpdateFields":
        self._subfields.extend(subfields)
        return self


class StoredPaymentMethodRequestDeleteFields(GraphQLField):
    result: StoredPaymentMethodRequestDeleteGraphQLField = (
        StoredPaymentMethodRequestDeleteGraphQLField("result")
    )

    @classmethod
    def errors(cls) -> "PaymentMethodRequestDeleteErrorFields":
        return PaymentMethodRequestDeleteErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            StoredPaymentMethodRequestDeleteGraphQLField,
            "PaymentMethodRequestDeleteErrorFields",
        ]
    ) -> "StoredPaymentMethodRequestDeleteFields":
        self._subfields.extend(subfields)
        return self


class ProductCreateFields(GraphQLField):
    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    def fields(
        self,
        *subfields: Union[
            ProductCreateGraphQLField, "ProductFields", "ProductErrorFields"
        ]
    ) -> "ProductCreateFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleFields(GraphQLField):
    id: PromotionRuleGraphQLField = PromotionRuleGraphQLField("id")
    name: PromotionRuleGraphQLField = PromotionRuleGraphQLField("name")
    description: PromotionRuleGraphQLField = PromotionRuleGraphQLField("description")

    @classmethod
    def promotion(cls) -> "PromotionFields":
        return PromotionFields("promotion")

    @classmethod
    def channels(cls) -> "ChannelFields":
        return ChannelFields("channels")

    reward_value: PromotionRuleGraphQLField = PromotionRuleGraphQLField("rewardValue")
    reward_value_type: PromotionRuleGraphQLField = PromotionRuleGraphQLField(
        "rewardValueType"
    )
    predicate_type: PromotionRuleGraphQLField = PromotionRuleGraphQLField(
        "predicateType"
    )
    catalogue_predicate: PromotionRuleGraphQLField = PromotionRuleGraphQLField(
        "cataloguePredicate"
    )
    order_predicate: PromotionRuleGraphQLField = PromotionRuleGraphQLField(
        "orderPredicate"
    )
    reward_type: PromotionRuleGraphQLField = PromotionRuleGraphQLField("rewardType")

    @classmethod
    def translation(cls) -> "PromotionRuleTranslationFields":
        return PromotionRuleTranslationFields("translation")

    gift_ids: PromotionRuleGraphQLField = PromotionRuleGraphQLField("giftIds")
    gifts_limit: PromotionRuleGraphQLField = PromotionRuleGraphQLField("giftsLimit")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleGraphQLField,
            "PromotionFields",
            "ChannelFields",
            "PromotionRuleTranslationFields",
        ]
    ) -> "PromotionRuleFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceExcludeProductsFields(GraphQLField):
    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShippingPriceExcludeProductsGraphQLField,
            "ShippingMethodTypeFields",
            "ShippingErrorFields",
        ]
    ) -> "ShippingPriceExcludeProductsFields":
        self._subfields.extend(subfields)
        return self


class PaymentVoidFields(GraphQLField):
    @classmethod
    def payment(cls) -> "PaymentFields":
        return PaymentFields("payment")

    @classmethod
    def payment_errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("payment_errors")

    @classmethod
    def errors(cls) -> "PaymentErrorFields":
        return PaymentErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentVoidGraphQLField, "PaymentFields", "PaymentErrorFields"
        ]
    ) -> "PaymentVoidFields":
        self._subfields.extend(subfields)
        return self


class FileUploadFields(GraphQLField):
    @classmethod
    def uploaded_file(cls) -> "FileFields":
        return FileFields("uploaded_file")

    @classmethod
    def upload_errors(cls) -> "UploadErrorFields":
        return UploadErrorFields("upload_errors")

    @classmethod
    def errors(cls) -> "UploadErrorFields":
        return UploadErrorFields("errors")

    def fields(
        self,
        *subfields: Union[FileUploadGraphQLField, "UploadErrorFields", "FileFields"]
    ) -> "FileUploadFields":
        self._subfields.extend(subfields)
        return self


class WebhookUpdateFields(GraphQLField):
    @classmethod
    def webhook_errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("webhook_errors")

    @classmethod
    def errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("errors")

    @classmethod
    def webhook(cls) -> "WebhookFields":
        return WebhookFields("webhook")

    def fields(
        self,
        *subfields: Union[
            WebhookUpdateGraphQLField, "WebhookErrorFields", "WebhookFields"
        ]
    ) -> "WebhookUpdateFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentCancelFields(GraphQLField):
    @classmethod
    def fulfillment(cls) -> "FulfillmentFields":
        return FulfillmentFields("fulfillment")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            FulfillmentCancelGraphQLField,
            "FulfillmentFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "FulfillmentCancelFields":
        self._subfields.extend(subfields)
        return self


class CustomerBulkResultFields(GraphQLField):
    @classmethod
    def customer(cls) -> "UserFields":
        return UserFields("customer")

    @classmethod
    def errors(cls) -> "CustomerBulkUpdateErrorFields":
        return CustomerBulkUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CustomerBulkResultGraphQLField,
            "CustomerBulkUpdateErrorFields",
            "UserFields",
        ]
    ) -> "CustomerBulkResultFields":
        self._subfields.extend(subfields)
        return self


class ProductTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    def fields(
        self,
        *subfields: Union[
            ProductTranslateGraphQLField, "ProductFields", "TranslationErrorFields"
        ]
    ) -> "ProductTranslateFields":
        self._subfields.extend(subfields)
        return self


class AttributeValueCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "AttributeValueCountableEdgeFields":
        return AttributeValueCountableEdgeFields("edges")

    total_count: AttributeValueCountableConnectionGraphQLField = (
        AttributeValueCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            AttributeValueCountableConnectionGraphQLField,
            "AttributeValueCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "AttributeValueCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PageCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "PageCountableEdgeFields":
        return PageCountableEdgeFields("edges")

    total_count: PageCountableConnectionGraphQLField = (
        PageCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            PageCountableConnectionGraphQLField,
            "PageCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "PageCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class MenuItemFields(GraphQLField):
    id: MenuItemGraphQLField = MenuItemGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: MenuItemGraphQLField = MenuItemGraphQLField("privateMetafield")
    private_metafields: MenuItemGraphQLField = MenuItemGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: MenuItemGraphQLField = MenuItemGraphQLField("metafield")
    metafields: MenuItemGraphQLField = MenuItemGraphQLField("metafields")
    name: MenuItemGraphQLField = MenuItemGraphQLField("name")

    @classmethod
    def menu(cls) -> "MenuFields":
        return MenuFields("menu")

    @classmethod
    def parent(cls) -> "MenuItemFields":
        return MenuItemFields("parent")

    @classmethod
    def category(cls) -> "CategoryFields":
        return CategoryFields("category")

    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    @classmethod
    def page(cls) -> "PageFields":
        return PageFields("page")

    level: MenuItemGraphQLField = MenuItemGraphQLField("level")

    @classmethod
    def children(cls) -> "MenuItemFields":
        return MenuItemFields("children")

    url: MenuItemGraphQLField = MenuItemGraphQLField("url")

    @classmethod
    def translation(cls) -> "MenuItemTranslationFields":
        return MenuItemTranslationFields("translation")

    def fields(
        self,
        *subfields: Union[
            MenuItemGraphQLField,
            "MetadataItemFields",
            "CollectionFields",
            "PageFields",
            "MenuFields",
            "MenuItemFields",
            "CategoryFields",
            "MenuItemTranslationFields",
        ]
    ) -> "MenuItemFields":
        self._subfields.extend(subfields)
        return self


class SaleDeleteFields(GraphQLField):
    @classmethod
    def discount_errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("discount_errors")

    @classmethod
    def errors(cls) -> "DiscountErrorFields":
        return DiscountErrorFields("errors")

    @classmethod
    def sale(cls) -> "SaleFields":
        return SaleFields("sale")

    def fields(
        self,
        *subfields: Union[SaleDeleteGraphQLField, "SaleFields", "DiscountErrorFields"]
    ) -> "SaleDeleteFields":
        self._subfields.extend(subfields)
        return self


class WeightFields(GraphQLField):
    unit: WeightGraphQLField = WeightGraphQLField("unit")
    value: WeightGraphQLField = WeightGraphQLField("value")

    def fields(self, *subfields: WeightGraphQLField) -> "WeightFields":
        self._subfields.extend(subfields)
        return self


class TransactionRequestRefundForGrantedRefundFields(GraphQLField):
    @classmethod
    def transaction(cls) -> "TransactionItemFields":
        return TransactionItemFields("transaction")

    @classmethod
    def errors(cls) -> "TransactionRequestRefundForGrantedRefundErrorFields":
        return TransactionRequestRefundForGrantedRefundErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            TransactionRequestRefundForGrantedRefundGraphQLField,
            "TransactionItemFields",
            "TransactionRequestRefundForGrantedRefundErrorFields",
        ]
    ) -> "TransactionRequestRefundForGrantedRefundFields":
        self._subfields.extend(subfields)
        return self


class ProductReorderAttributeValuesFields(GraphQLField):
    @classmethod
    def product(cls) -> "ProductFields":
        return ProductFields("product")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductReorderAttributeValuesGraphQLField,
            "ProductFields",
            "ProductErrorFields",
        ]
    ) -> "ProductReorderAttributeValuesFields":
        self._subfields.extend(subfields)
        return self


class CreditCardFields(GraphQLField):
    brand: CreditCardGraphQLField = CreditCardGraphQLField("brand")
    first_digits: CreditCardGraphQLField = CreditCardGraphQLField("firstDigits")
    last_digits: CreditCardGraphQLField = CreditCardGraphQLField("lastDigits")
    exp_month: CreditCardGraphQLField = CreditCardGraphQLField("expMonth")
    exp_year: CreditCardGraphQLField = CreditCardGraphQLField("expYear")

    def fields(self, *subfields: CreditCardGraphQLField) -> "CreditCardFields":
        self._subfields.extend(subfields)
        return self


class AppManifestRequiredSaleorVersionFields(GraphQLField):
    constraint: AppManifestRequiredSaleorVersionGraphQLField = (
        AppManifestRequiredSaleorVersionGraphQLField("constraint")
    )
    satisfied: AppManifestRequiredSaleorVersionGraphQLField = (
        AppManifestRequiredSaleorVersionGraphQLField("satisfied")
    )

    def fields(
        self, *subfields: AppManifestRequiredSaleorVersionGraphQLField
    ) -> "AppManifestRequiredSaleorVersionFields":
        self._subfields.extend(subfields)
        return self


class CheckoutSettingsFields(GraphQLField):
    use_legacy_error_flow: CheckoutSettingsGraphQLField = CheckoutSettingsGraphQLField(
        "useLegacyErrorFlow"
    )

    def fields(
        self, *subfields: CheckoutSettingsGraphQLField
    ) -> "CheckoutSettingsFields":
        self._subfields.extend(subfields)
        return self


class AppBrandFields(GraphQLField):
    @classmethod
    def logo(cls) -> "AppBrandLogoFields":
        return AppBrandLogoFields("logo")

    def fields(
        self, *subfields: Union[AppBrandGraphQLField, "AppBrandLogoFields"]
    ) -> "AppBrandFields":
        self._subfields.extend(subfields)
        return self


class FulfillmentReturnProductsFields(GraphQLField):
    @classmethod
    def return_fulfillment(cls) -> "FulfillmentFields":
        return FulfillmentFields("return_fulfillment")

    @classmethod
    def replace_fulfillment(cls) -> "FulfillmentFields":
        return FulfillmentFields("replace_fulfillment")

    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def replace_order(cls) -> "OrderFields":
        return OrderFields("replace_order")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            FulfillmentReturnProductsGraphQLField,
            "FulfillmentFields",
            "OrderErrorFields",
            "OrderFields",
        ]
    ) -> "FulfillmentReturnProductsFields":
        self._subfields.extend(subfields)
        return self


class PermissionGroupErrorFields(GraphQLField):
    field: PermissionGroupErrorGraphQLField = PermissionGroupErrorGraphQLField("field")
    message: PermissionGroupErrorGraphQLField = PermissionGroupErrorGraphQLField(
        "message"
    )
    code: PermissionGroupErrorGraphQLField = PermissionGroupErrorGraphQLField("code")
    permissions: PermissionGroupErrorGraphQLField = PermissionGroupErrorGraphQLField(
        "permissions"
    )
    users: PermissionGroupErrorGraphQLField = PermissionGroupErrorGraphQLField("users")
    channels: PermissionGroupErrorGraphQLField = PermissionGroupErrorGraphQLField(
        "channels"
    )

    def fields(
        self, *subfields: PermissionGroupErrorGraphQLField
    ) -> "PermissionGroupErrorFields":
        self._subfields.extend(subfields)
        return self


class ChannelCreateFields(GraphQLField):
    @classmethod
    def channel_errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("channel_errors")

    @classmethod
    def errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("errors")

    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    def fields(
        self,
        *subfields: Union[
            ChannelCreateGraphQLField, "ChannelFields", "ChannelErrorFields"
        ]
    ) -> "ChannelCreateFields":
        self._subfields.extend(subfields)
        return self


class CollectionReorderProductsFields(GraphQLField):
    @classmethod
    def collection(cls) -> "CollectionFields":
        return CollectionFields("collection")

    @classmethod
    def collection_errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("collection_errors")

    @classmethod
    def errors(cls) -> "CollectionErrorFields":
        return CollectionErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CollectionReorderProductsGraphQLField,
            "CollectionFields",
            "CollectionErrorFields",
        ]
    ) -> "CollectionReorderProductsFields":
        self._subfields.extend(subfields)
        return self


class OrderEventCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "OrderEventFields":
        return OrderEventFields("node")

    cursor: OrderEventCountableEdgeGraphQLField = OrderEventCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[OrderEventCountableEdgeGraphQLField, "OrderEventFields"]
    ) -> "OrderEventCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class WebhookTriggerFields(GraphQLField):
    @classmethod
    def delivery(cls) -> "EventDeliveryFields":
        return EventDeliveryFields("delivery")

    @classmethod
    def errors(cls) -> "WebhookTriggerErrorFields":
        return WebhookTriggerErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            WebhookTriggerGraphQLField,
            "EventDeliveryFields",
            "WebhookTriggerErrorFields",
        ]
    ) -> "WebhookTriggerFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantTranslateFields(GraphQLField):
    @classmethod
    def translation_errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("translation_errors")

    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    def fields(
        self,
        *subfields: Union[
            ProductVariantTranslateGraphQLField,
            "TranslationErrorFields",
            "ProductVariantFields",
        ]
    ) -> "ProductVariantTranslateFields":
        self._subfields.extend(subfields)
        return self


class GiftCardBulkCreateFields(GraphQLField):
    count: GiftCardBulkCreateGraphQLField = GiftCardBulkCreateGraphQLField("count")

    @classmethod
    def gift_cards(cls) -> "GiftCardFields":
        return GiftCardFields("gift_cards")

    @classmethod
    def errors(cls) -> "GiftCardErrorFields":
        return GiftCardErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            GiftCardBulkCreateGraphQLField, "GiftCardErrorFields", "GiftCardFields"
        ]
    ) -> "GiftCardBulkCreateFields":
        self._subfields.extend(subfields)
        return self


class ShippingMethodChannelListingUpdateFields(GraphQLField):
    @classmethod
    def shipping_method(cls) -> "ShippingMethodTypeFields":
        return ShippingMethodTypeFields("shipping_method")

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ShippingMethodChannelListingUpdateGraphQLField,
            "ShippingMethodTypeFields",
            "ShippingErrorFields",
        ]
    ) -> "ShippingMethodChannelListingUpdateFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayInitializeTokenizationFields(GraphQLField):
    result: PaymentGatewayInitializeTokenizationGraphQLField = (
        PaymentGatewayInitializeTokenizationGraphQLField("result")
    )
    data: PaymentGatewayInitializeTokenizationGraphQLField = (
        PaymentGatewayInitializeTokenizationGraphQLField("data")
    )

    @classmethod
    def errors(cls) -> "PaymentGatewayInitializeTokenizationErrorFields":
        return PaymentGatewayInitializeTokenizationErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            PaymentGatewayInitializeTokenizationGraphQLField,
            "PaymentGatewayInitializeTokenizationErrorFields",
        ]
    ) -> "PaymentGatewayInitializeTokenizationFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantRefundCreateErrorFields(GraphQLField):
    field: OrderGrantRefundCreateErrorGraphQLField = (
        OrderGrantRefundCreateErrorGraphQLField("field")
    )
    message: OrderGrantRefundCreateErrorGraphQLField = (
        OrderGrantRefundCreateErrorGraphQLField("message")
    )
    code: OrderGrantRefundCreateErrorGraphQLField = (
        OrderGrantRefundCreateErrorGraphQLField("code")
    )

    @classmethod
    def lines(cls) -> "OrderGrantRefundCreateLineErrorFields":
        return OrderGrantRefundCreateLineErrorFields("lines")

    def fields(
        self,
        *subfields: Union[
            OrderGrantRefundCreateErrorGraphQLField,
            "OrderGrantRefundCreateLineErrorFields",
        ]
    ) -> "OrderGrantRefundCreateErrorFields":
        self._subfields.extend(subfields)
        return self


class ProductVariantReorderAttributeValuesFields(GraphQLField):
    @classmethod
    def product_variant(cls) -> "ProductVariantFields":
        return ProductVariantFields("product_variant")

    @classmethod
    def product_errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("product_errors")

    @classmethod
    def errors(cls) -> "ProductErrorFields":
        return ProductErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ProductVariantReorderAttributeValuesGraphQLField,
            "ProductVariantFields",
            "ProductErrorFields",
        ]
    ) -> "ProductVariantReorderAttributeValuesFields":
        self._subfields.extend(subfields)
        return self


class PaymentGatewayConfigErrorFields(GraphQLField):
    field: PaymentGatewayConfigErrorGraphQLField = (
        PaymentGatewayConfigErrorGraphQLField("field")
    )
    message: PaymentGatewayConfigErrorGraphQLField = (
        PaymentGatewayConfigErrorGraphQLField("message")
    )
    code: PaymentGatewayConfigErrorGraphQLField = PaymentGatewayConfigErrorGraphQLField(
        "code"
    )

    def fields(
        self, *subfields: PaymentGatewayConfigErrorGraphQLField
    ) -> "PaymentGatewayConfigErrorFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCreateFields(GraphQLField):
    created: CheckoutCreateGraphQLField = CheckoutCreateGraphQLField("created")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    def fields(
        self,
        *subfields: Union[
            CheckoutCreateGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutCreateFields":
        self._subfields.extend(subfields)
        return self


class TaxClassUpdateErrorFields(GraphQLField):
    field: TaxClassUpdateErrorGraphQLField = TaxClassUpdateErrorGraphQLField("field")
    message: TaxClassUpdateErrorGraphQLField = TaxClassUpdateErrorGraphQLField(
        "message"
    )
    code: TaxClassUpdateErrorGraphQLField = TaxClassUpdateErrorGraphQLField("code")
    country_codes: TaxClassUpdateErrorGraphQLField = TaxClassUpdateErrorGraphQLField(
        "countryCodes"
    )

    def fields(
        self, *subfields: TaxClassUpdateErrorGraphQLField
    ) -> "TaxClassUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class OrderGrantRefundUpdateErrorFields(GraphQLField):
    field: OrderGrantRefundUpdateErrorGraphQLField = (
        OrderGrantRefundUpdateErrorGraphQLField("field")
    )
    message: OrderGrantRefundUpdateErrorGraphQLField = (
        OrderGrantRefundUpdateErrorGraphQLField("message")
    )
    code: OrderGrantRefundUpdateErrorGraphQLField = (
        OrderGrantRefundUpdateErrorGraphQLField("code")
    )

    @classmethod
    def add_lines(cls) -> "OrderGrantRefundUpdateLineErrorFields":
        return OrderGrantRefundUpdateLineErrorFields("add_lines")

    @classmethod
    def remove_lines(cls) -> "OrderGrantRefundUpdateLineErrorFields":
        return OrderGrantRefundUpdateLineErrorFields("remove_lines")

    def fields(
        self,
        *subfields: Union[
            OrderGrantRefundUpdateErrorGraphQLField,
            "OrderGrantRefundUpdateLineErrorFields",
        ]
    ) -> "OrderGrantRefundUpdateErrorFields":
        self._subfields.extend(subfields)
        return self


class ChannelReorderWarehousesFields(GraphQLField):
    @classmethod
    def channel(cls) -> "ChannelFields":
        return ChannelFields("channel")

    @classmethod
    def errors(cls) -> "ChannelErrorFields":
        return ChannelErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            ChannelReorderWarehousesGraphQLField, "ChannelFields", "ChannelErrorFields"
        ]
    ) -> "ChannelReorderWarehousesFields":
        self._subfields.extend(subfields)
        return self


class PageTypeUpdateFields(GraphQLField):
    @classmethod
    def page_errors(cls) -> "PageErrorFields":
        return PageErrorFields("page_errors")

    @classmethod
    def errors(cls) -> "PageErrorFields":
        return PageErrorFields("errors")

    @classmethod
    def page_type(cls) -> "PageTypeFields":
        return PageTypeFields("page_type")

    def fields(
        self,
        *subfields: Union[
            PageTypeUpdateGraphQLField, "PageTypeFields", "PageErrorFields"
        ]
    ) -> "PageTypeUpdateFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCustomerAttachFields(GraphQLField):
    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def checkout_errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("checkout_errors")

    @classmethod
    def errors(cls) -> "CheckoutErrorFields":
        return CheckoutErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutCustomerAttachGraphQLField, "CheckoutErrorFields", "CheckoutFields"
        ]
    ) -> "CheckoutCustomerAttachFields":
        self._subfields.extend(subfields)
        return self


class AccountAddressUpdateFields(GraphQLField):
    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def account_errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("account_errors")

    @classmethod
    def errors(cls) -> "AccountErrorFields":
        return AccountErrorFields("errors")

    @classmethod
    def address(cls) -> "AddressFields":
        return AddressFields("address")

    def fields(
        self,
        *subfields: Union[
            AccountAddressUpdateGraphQLField,
            "AccountErrorFields",
            "UserFields",
            "AddressFields",
        ]
    ) -> "AccountAddressUpdateFields":
        self._subfields.extend(subfields)
        return self


class OrderSettingsErrorFields(GraphQLField):
    field: OrderSettingsErrorGraphQLField = OrderSettingsErrorGraphQLField("field")
    message: OrderSettingsErrorGraphQLField = OrderSettingsErrorGraphQLField("message")
    code: OrderSettingsErrorGraphQLField = OrderSettingsErrorGraphQLField("code")

    def fields(
        self, *subfields: OrderSettingsErrorGraphQLField
    ) -> "OrderSettingsErrorFields":
        self._subfields.extend(subfields)
        return self


class AllocationFields(GraphQLField):
    id: AllocationGraphQLField = AllocationGraphQLField("id")
    quantity: AllocationGraphQLField = AllocationGraphQLField("quantity")

    @classmethod
    def warehouse(cls) -> "WarehouseFields":
        return WarehouseFields("warehouse")

    def fields(
        self, *subfields: Union[AllocationGraphQLField, "WarehouseFields"]
    ) -> "AllocationFields":
        self._subfields.extend(subfields)
        return self


class ShippingPriceBulkDeleteFields(GraphQLField):
    count: ShippingPriceBulkDeleteGraphQLField = ShippingPriceBulkDeleteGraphQLField(
        "count"
    )

    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    def fields(
        self,
        *subfields: Union[ShippingPriceBulkDeleteGraphQLField, "ShippingErrorFields"]
    ) -> "ShippingPriceBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneCreateFields(GraphQLField):
    @classmethod
    def shipping_errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("shipping_errors")

    @classmethod
    def errors(cls) -> "ShippingErrorFields":
        return ShippingErrorFields("errors")

    @classmethod
    def shipping_zone(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("shipping_zone")

    def fields(
        self,
        *subfields: Union[
            ShippingZoneCreateGraphQLField, "ShippingZoneFields", "ShippingErrorFields"
        ]
    ) -> "ShippingZoneCreateFields":
        self._subfields.extend(subfields)
        return self


class MenuItemBulkDeleteFields(GraphQLField):
    count: MenuItemBulkDeleteGraphQLField = MenuItemBulkDeleteGraphQLField("count")

    @classmethod
    def menu_errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("menu_errors")

    @classmethod
    def errors(cls) -> "MenuErrorFields":
        return MenuErrorFields("errors")

    def fields(
        self, *subfields: Union[MenuItemBulkDeleteGraphQLField, "MenuErrorFields"]
    ) -> "MenuItemBulkDeleteFields":
        self._subfields.extend(subfields)
        return self


class AppTokenCreateFields(GraphQLField):
    auth_token: AppTokenCreateGraphQLField = AppTokenCreateGraphQLField("authToken")

    @classmethod
    def app_errors(cls) -> "AppErrorFields":
        return AppErrorFields("app_errors")

    @classmethod
    def errors(cls) -> "AppErrorFields":
        return AppErrorFields("errors")

    @classmethod
    def app_token(cls) -> "AppTokenFields":
        return AppTokenFields("app_token")

    def fields(
        self,
        *subfields: Union[
            AppTokenCreateGraphQLField, "AppErrorFields", "AppTokenFields"
        ]
    ) -> "AppTokenCreateFields":
        self._subfields.extend(subfields)
        return self


class VoucherTranslationFields(GraphQLField):
    id: VoucherTranslationGraphQLField = VoucherTranslationGraphQLField("id")

    @classmethod
    def language(cls) -> "LanguageDisplayFields":
        return LanguageDisplayFields("language")

    name: VoucherTranslationGraphQLField = VoucherTranslationGraphQLField("name")

    @classmethod
    def translatable_content(cls) -> "VoucherTranslatableContentFields":
        return VoucherTranslatableContentFields("translatable_content")

    def fields(
        self,
        *subfields: Union[
            VoucherTranslationGraphQLField,
            "VoucherTranslatableContentFields",
            "LanguageDisplayFields",
        ]
    ) -> "VoucherTranslationFields":
        self._subfields.extend(subfields)
        return self


class WebhookFields(GraphQLField):
    id: WebhookGraphQLField = WebhookGraphQLField("id")
    name: WebhookGraphQLField = WebhookGraphQLField("name")

    @classmethod
    def events(cls) -> "WebhookEventFields":
        return WebhookEventFields("events")

    @classmethod
    def sync_events(cls) -> "WebhookEventSyncFields":
        return WebhookEventSyncFields("sync_events")

    @classmethod
    def async_events(cls) -> "WebhookEventAsyncFields":
        return WebhookEventAsyncFields("async_events")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    @classmethod
    def event_deliveries(cls) -> "EventDeliveryCountableConnectionFields":
        return EventDeliveryCountableConnectionFields("event_deliveries")

    target_url: WebhookGraphQLField = WebhookGraphQLField("targetUrl")
    is_active: WebhookGraphQLField = WebhookGraphQLField("isActive")
    secret_key: WebhookGraphQLField = WebhookGraphQLField("secretKey")
    subscription_query: WebhookGraphQLField = WebhookGraphQLField("subscriptionQuery")
    custom_headers: WebhookGraphQLField = WebhookGraphQLField("customHeaders")

    def fields(
        self,
        *subfields: Union[
            WebhookGraphQLField,
            "WebhookEventAsyncFields",
            "EventDeliveryCountableConnectionFields",
            "AppFields",
            "WebhookEventSyncFields",
            "WebhookEventFields",
        ]
    ) -> "WebhookFields":
        self._subfields.extend(subfields)
        return self


class SaleCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "SaleCountableEdgeFields":
        return SaleCountableEdgeFields("edges")

    total_count: SaleCountableConnectionGraphQLField = (
        SaleCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            SaleCountableConnectionGraphQLField,
            "SaleCountableEdgeFields",
            "PageInfoFields",
        ]
    ) -> "SaleCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class CheckoutCreateFromOrderFields(GraphQLField):
    @classmethod
    def unavailable_variants(cls) -> "CheckoutCreateFromOrderUnavailableVariantFields":
        return CheckoutCreateFromOrderUnavailableVariantFields("unavailable_variants")

    @classmethod
    def checkout(cls) -> "CheckoutFields":
        return CheckoutFields("checkout")

    @classmethod
    def errors(cls) -> "CheckoutCreateFromOrderErrorFields":
        return CheckoutCreateFromOrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            CheckoutCreateFromOrderGraphQLField,
            "CheckoutFields",
            "CheckoutCreateFromOrderErrorFields",
            "CheckoutCreateFromOrderUnavailableVariantFields",
        ]
    ) -> "CheckoutCreateFromOrderFields":
        self._subfields.extend(subfields)
        return self


class OrderLinesCreateFields(GraphQLField):
    @classmethod
    def order(cls) -> "OrderFields":
        return OrderFields("order")

    @classmethod
    def order_lines(cls) -> "OrderLineFields":
        return OrderLineFields("order_lines")

    @classmethod
    def order_errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("order_errors")

    @classmethod
    def errors(cls) -> "OrderErrorFields":
        return OrderErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            OrderLinesCreateGraphQLField,
            "OrderErrorFields",
            "OrderFields",
            "OrderLineFields",
        ]
    ) -> "OrderLinesCreateFields":
        self._subfields.extend(subfields)
        return self


class PageCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "PageFields":
        return PageFields("node")

    cursor: PageCountableEdgeGraphQLField = PageCountableEdgeGraphQLField("cursor")

    def fields(
        self, *subfields: Union[PageCountableEdgeGraphQLField, "PageFields"]
    ) -> "PageCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class ShippingZoneCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ShippingZoneFields":
        return ShippingZoneFields("node")

    cursor: ShippingZoneCountableEdgeGraphQLField = (
        ShippingZoneCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[ShippingZoneCountableEdgeGraphQLField, "ShippingZoneFields"]
    ) -> "ShippingZoneCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class AppFields(GraphQLField):
    id: AppGraphQLField = AppGraphQLField("id")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: AppGraphQLField = AppGraphQLField("privateMetafield")
    private_metafields: AppGraphQLField = AppGraphQLField("privateMetafields")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: AppGraphQLField = AppGraphQLField("metafield")
    metafields: AppGraphQLField = AppGraphQLField("metafields")
    identifier: AppGraphQLField = AppGraphQLField("identifier")

    @classmethod
    def permissions(cls) -> "PermissionFields":
        return PermissionFields("permissions")

    created: AppGraphQLField = AppGraphQLField("created")
    is_active: AppGraphQLField = AppGraphQLField("isActive")
    name: AppGraphQLField = AppGraphQLField("name")
    type: AppGraphQLField = AppGraphQLField("type")

    @classmethod
    def tokens(cls) -> "AppTokenFields":
        return AppTokenFields("tokens")

    @classmethod
    def webhooks(cls) -> "WebhookFields":
        return WebhookFields("webhooks")

    about_app: AppGraphQLField = AppGraphQLField("aboutApp")
    data_privacy: AppGraphQLField = AppGraphQLField("dataPrivacy")
    data_privacy_url: AppGraphQLField = AppGraphQLField("dataPrivacyUrl")
    homepage_url: AppGraphQLField = AppGraphQLField("homepageUrl")
    support_url: AppGraphQLField = AppGraphQLField("supportUrl")
    configuration_url: AppGraphQLField = AppGraphQLField("configurationUrl")
    app_url: AppGraphQLField = AppGraphQLField("appUrl")
    manifest_url: AppGraphQLField = AppGraphQLField("manifestUrl")
    version: AppGraphQLField = AppGraphQLField("version")
    access_token: AppGraphQLField = AppGraphQLField("accessToken")
    author: AppGraphQLField = AppGraphQLField("author")

    @classmethod
    def extensions(cls) -> "AppExtensionFields":
        return AppExtensionFields("extensions")

    @classmethod
    def brand(cls) -> "AppBrandFields":
        return AppBrandFields("brand")

    def fields(
        self,
        *subfields: Union[
            AppGraphQLField,
            "AppTokenFields",
            "MetadataItemFields",
            "PermissionFields",
            "AppExtensionFields",
            "WebhookFields",
            "AppBrandFields",
        ]
    ) -> "AppFields":
        self._subfields.extend(subfields)
        return self


class DigitalContentCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "DigitalContentCountableEdgeFields":
        return DigitalContentCountableEdgeFields("edges")

    total_count: DigitalContentCountableConnectionGraphQLField = (
        DigitalContentCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            DigitalContentCountableConnectionGraphQLField,
            "PageInfoFields",
            "DigitalContentCountableEdgeFields",
        ]
    ) -> "DigitalContentCountableConnectionFields":
        self._subfields.extend(subfields)
        return self


class PromotionRuleTranslateFields(GraphQLField):
    @classmethod
    def errors(cls) -> "TranslationErrorFields":
        return TranslationErrorFields("errors")

    @classmethod
    def promotion_rule(cls) -> "PromotionRuleFields":
        return PromotionRuleFields("promotion_rule")

    def fields(
        self,
        *subfields: Union[
            PromotionRuleTranslateGraphQLField,
            "TranslationErrorFields",
            "PromotionRuleFields",
        ]
    ) -> "PromotionRuleTranslateFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryAttemptCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "EventDeliveryAttemptFields":
        return EventDeliveryAttemptFields("node")

    cursor: EventDeliveryAttemptCountableEdgeGraphQLField = (
        EventDeliveryAttemptCountableEdgeGraphQLField("cursor")
    )

    def fields(
        self,
        *subfields: Union[
            EventDeliveryAttemptCountableEdgeGraphQLField, "EventDeliveryAttemptFields"
        ]
    ) -> "EventDeliveryAttemptCountableEdgeFields":
        self._subfields.extend(subfields)
        return self


class EventDeliveryRetryFields(GraphQLField):
    @classmethod
    def delivery(cls) -> "EventDeliveryFields":
        return EventDeliveryFields("delivery")

    @classmethod
    def errors(cls) -> "WebhookErrorFields":
        return WebhookErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            EventDeliveryRetryGraphQLField, "EventDeliveryFields", "WebhookErrorFields"
        ]
    ) -> "EventDeliveryRetryFields":
        self._subfields.extend(subfields)
        return self


class ShopDomainUpdateFields(GraphQLField):
    @classmethod
    def shop(cls) -> "ShopFields":
        return ShopFields("shop")

    @classmethod
    def shop_errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("shop_errors")

    @classmethod
    def errors(cls) -> "ShopErrorFields":
        return ShopErrorFields("errors")

    def fields(
        self,
        *subfields: Union[ShopDomainUpdateGraphQLField, "ShopErrorFields", "ShopFields"]
    ) -> "ShopDomainUpdateFields":
        self._subfields.extend(subfields)
        return self


class AttributeBulkUpdateResultFields(GraphQLField):
    @classmethod
    def attribute(cls) -> "AttributeFields":
        return AttributeFields("attribute")

    @classmethod
    def errors(cls) -> "AttributeBulkUpdateErrorFields":
        return AttributeBulkUpdateErrorFields("errors")

    def fields(
        self,
        *subfields: Union[
            AttributeBulkUpdateResultGraphQLField,
            "AttributeFields",
            "AttributeBulkUpdateErrorFields",
        ]
    ) -> "AttributeBulkUpdateResultFields":
        self._subfields.extend(subfields)
        return self


class AppExtensionFields(GraphQLField):
    id: AppExtensionGraphQLField = AppExtensionGraphQLField("id")

    @classmethod
    def permissions(cls) -> "PermissionFields":
        return PermissionFields("permissions")

    label: AppExtensionGraphQLField = AppExtensionGraphQLField("label")
    url: AppExtensionGraphQLField = AppExtensionGraphQLField("url")
    mount: AppExtensionGraphQLField = AppExtensionGraphQLField("mount")
    target: AppExtensionGraphQLField = AppExtensionGraphQLField("target")

    @classmethod
    def app(cls) -> "AppFields":
        return AppFields("app")

    access_token: AppExtensionGraphQLField = AppExtensionGraphQLField("accessToken")

    def fields(
        self,
        *subfields: Union[AppExtensionGraphQLField, "AppFields", "PermissionFields"]
    ) -> "AppExtensionFields":
        self._subfields.extend(subfields)
        return self

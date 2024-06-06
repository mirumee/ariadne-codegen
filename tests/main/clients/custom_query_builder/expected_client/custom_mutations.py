from typing import Any, Optional

from .base_model import Upload
from .custom_fields import (
    AccountAddressCreateFields,
    AccountAddressDeleteFields,
    AccountAddressUpdateFields,
    AccountDeleteFields,
    AccountRegisterFields,
    AccountRequestDeletionFields,
    AccountSetDefaultAddressFields,
    AccountUpdateFields,
    AddressCreateFields,
    AddressDeleteFields,
    AddressSetDefaultFields,
    AddressUpdateFields,
    AppActivateFields,
    AppCreateFields,
    AppDeactivateFields,
    AppDeleteFailedInstallationFields,
    AppDeleteFields,
    AppFetchManifestFields,
    AppInstallFields,
    AppRetryInstallFields,
    AppTokenCreateFields,
    AppTokenDeleteFields,
    AppTokenVerifyFields,
    AppUpdateFields,
    AssignNavigationFields,
    AttributeBulkCreateFields,
    AttributeBulkDeleteFields,
    AttributeBulkTranslateFields,
    AttributeBulkUpdateFields,
    AttributeCreateFields,
    AttributeDeleteFields,
    AttributeReorderValuesFields,
    AttributeTranslateFields,
    AttributeUpdateFields,
    AttributeValueBulkDeleteFields,
    AttributeValueBulkTranslateFields,
    AttributeValueCreateFields,
    AttributeValueDeleteFields,
    AttributeValueTranslateFields,
    AttributeValueUpdateFields,
    CategoryBulkDeleteFields,
    CategoryCreateFields,
    CategoryDeleteFields,
    CategoryTranslateFields,
    CategoryUpdateFields,
    ChannelActivateFields,
    ChannelCreateFields,
    ChannelDeactivateFields,
    ChannelDeleteFields,
    ChannelReorderWarehousesFields,
    ChannelUpdateFields,
    CheckoutAddPromoCodeFields,
    CheckoutBillingAddressUpdateFields,
    CheckoutCompleteFields,
    CheckoutCreateFields,
    CheckoutCreateFromOrderFields,
    CheckoutCustomerAttachFields,
    CheckoutCustomerDetachFields,
    CheckoutDeliveryMethodUpdateFields,
    CheckoutEmailUpdateFields,
    CheckoutLanguageCodeUpdateFields,
    CheckoutLineDeleteFields,
    CheckoutLinesAddFields,
    CheckoutLinesDeleteFields,
    CheckoutLinesUpdateFields,
    CheckoutPaymentCreateFields,
    CheckoutRemovePromoCodeFields,
    CheckoutShippingAddressUpdateFields,
    CheckoutShippingMethodUpdateFields,
    CollectionAddProductsFields,
    CollectionBulkDeleteFields,
    CollectionChannelListingUpdateFields,
    CollectionCreateFields,
    CollectionDeleteFields,
    CollectionRemoveProductsFields,
    CollectionReorderProductsFields,
    CollectionTranslateFields,
    CollectionUpdateFields,
    ConfirmAccountFields,
    ConfirmEmailChangeFields,
    CreateTokenFields,
    CustomerBulkDeleteFields,
    CustomerBulkUpdateFields,
    CustomerCreateFields,
    CustomerDeleteFields,
    CustomerUpdateFields,
    DeactivateAllUserTokensFields,
    DeleteMetadataFields,
    DeletePrivateMetadataFields,
    DigitalContentCreateFields,
    DigitalContentDeleteFields,
    DigitalContentUpdateFields,
    DigitalContentUrlCreateFields,
    DraftOrderBulkDeleteFields,
    DraftOrderCompleteFields,
    DraftOrderCreateFields,
    DraftOrderDeleteFields,
    DraftOrderLinesBulkDeleteFields,
    DraftOrderUpdateFields,
    EventDeliveryRetryFields,
    ExportGiftCardsFields,
    ExportProductsFields,
    ExportVoucherCodesFields,
    ExternalAuthenticationUrlFields,
    ExternalLogoutFields,
    ExternalNotificationTriggerFields,
    ExternalObtainAccessTokensFields,
    ExternalRefreshFields,
    ExternalVerifyFields,
    FileUploadFields,
    FulfillmentApproveFields,
    FulfillmentCancelFields,
    FulfillmentRefundProductsFields,
    FulfillmentReturnProductsFields,
    FulfillmentUpdateTrackingFields,
    GiftCardActivateFields,
    GiftCardAddNoteFields,
    GiftCardBulkActivateFields,
    GiftCardBulkCreateFields,
    GiftCardBulkDeactivateFields,
    GiftCardBulkDeleteFields,
    GiftCardCreateFields,
    GiftCardDeactivateFields,
    GiftCardDeleteFields,
    GiftCardResendFields,
    GiftCardSettingsUpdateFields,
    GiftCardUpdateFields,
    InvoiceCreateFields,
    InvoiceDeleteFields,
    InvoiceRequestDeleteFields,
    InvoiceRequestFields,
    InvoiceSendNotificationFields,
    InvoiceUpdateFields,
    MenuBulkDeleteFields,
    MenuCreateFields,
    MenuDeleteFields,
    MenuItemBulkDeleteFields,
    MenuItemCreateFields,
    MenuItemDeleteFields,
    MenuItemMoveFields,
    MenuItemTranslateFields,
    MenuItemUpdateFields,
    MenuUpdateFields,
    OrderAddNoteFields,
    OrderBulkCancelFields,
    OrderBulkCreateFields,
    OrderCancelFields,
    OrderCaptureFields,
    OrderConfirmFields,
    OrderCreateFromCheckoutFields,
    OrderDiscountAddFields,
    OrderDiscountDeleteFields,
    OrderDiscountUpdateFields,
    OrderFulfillFields,
    OrderGrantRefundCreateFields,
    OrderGrantRefundUpdateFields,
    OrderLineDeleteFields,
    OrderLineDiscountRemoveFields,
    OrderLineDiscountUpdateFields,
    OrderLinesCreateFields,
    OrderLineUpdateFields,
    OrderMarkAsPaidFields,
    OrderNoteAddFields,
    OrderNoteUpdateFields,
    OrderRefundFields,
    OrderSettingsUpdateFields,
    OrderUpdateFields,
    OrderUpdateShippingFields,
    OrderVoidFields,
    PageAttributeAssignFields,
    PageAttributeUnassignFields,
    PageBulkDeleteFields,
    PageBulkPublishFields,
    PageCreateFields,
    PageDeleteFields,
    PageReorderAttributeValuesFields,
    PageTranslateFields,
    PageTypeBulkDeleteFields,
    PageTypeCreateFields,
    PageTypeDeleteFields,
    PageTypeReorderAttributesFields,
    PageTypeUpdateFields,
    PageUpdateFields,
    PasswordChangeFields,
    PaymentCaptureFields,
    PaymentCheckBalanceFields,
    PaymentGatewayInitializeFields,
    PaymentGatewayInitializeTokenizationFields,
    PaymentInitializeFields,
    PaymentMethodInitializeTokenizationFields,
    PaymentMethodProcessTokenizationFields,
    PaymentRefundFields,
    PaymentVoidFields,
    PermissionGroupCreateFields,
    PermissionGroupDeleteFields,
    PermissionGroupUpdateFields,
    PluginUpdateFields,
    ProductAttributeAssignFields,
    ProductAttributeAssignmentUpdateFields,
    ProductAttributeUnassignFields,
    ProductBulkCreateFields,
    ProductBulkDeleteFields,
    ProductBulkTranslateFields,
    ProductChannelListingUpdateFields,
    ProductCreateFields,
    ProductDeleteFields,
    ProductMediaBulkDeleteFields,
    ProductMediaCreateFields,
    ProductMediaDeleteFields,
    ProductMediaReorderFields,
    ProductMediaUpdateFields,
    ProductReorderAttributeValuesFields,
    ProductTranslateFields,
    ProductTypeBulkDeleteFields,
    ProductTypeCreateFields,
    ProductTypeDeleteFields,
    ProductTypeReorderAttributesFields,
    ProductTypeUpdateFields,
    ProductUpdateFields,
    ProductVariantBulkCreateFields,
    ProductVariantBulkDeleteFields,
    ProductVariantBulkTranslateFields,
    ProductVariantBulkUpdateFields,
    ProductVariantChannelListingUpdateFields,
    ProductVariantCreateFields,
    ProductVariantDeleteFields,
    ProductVariantPreorderDeactivateFields,
    ProductVariantReorderAttributeValuesFields,
    ProductVariantReorderFields,
    ProductVariantSetDefaultFields,
    ProductVariantStocksCreateFields,
    ProductVariantStocksDeleteFields,
    ProductVariantStocksUpdateFields,
    ProductVariantTranslateFields,
    ProductVariantUpdateFields,
    PromotionBulkDeleteFields,
    PromotionCreateFields,
    PromotionDeleteFields,
    PromotionRuleCreateFields,
    PromotionRuleDeleteFields,
    PromotionRuleTranslateFields,
    PromotionRuleUpdateFields,
    PromotionTranslateFields,
    PromotionUpdateFields,
    RefreshTokenFields,
    RequestEmailChangeFields,
    RequestPasswordResetFields,
    SaleAddCataloguesFields,
    SaleBulkDeleteFields,
    SaleChannelListingUpdateFields,
    SaleCreateFields,
    SaleDeleteFields,
    SaleRemoveCataloguesFields,
    SaleTranslateFields,
    SaleUpdateFields,
    SendConfirmationEmailFields,
    SetPasswordFields,
    ShippingMethodChannelListingUpdateFields,
    ShippingPriceBulkDeleteFields,
    ShippingPriceCreateFields,
    ShippingPriceDeleteFields,
    ShippingPriceExcludeProductsFields,
    ShippingPriceRemoveProductFromExcludeFields,
    ShippingPriceTranslateFields,
    ShippingPriceUpdateFields,
    ShippingZoneBulkDeleteFields,
    ShippingZoneCreateFields,
    ShippingZoneDeleteFields,
    ShippingZoneUpdateFields,
    ShopAddressUpdateFields,
    ShopDomainUpdateFields,
    ShopFetchTaxRatesFields,
    ShopSettingsTranslateFields,
    ShopSettingsUpdateFields,
    StaffBulkDeleteFields,
    StaffCreateFields,
    StaffDeleteFields,
    StaffNotificationRecipientCreateFields,
    StaffNotificationRecipientDeleteFields,
    StaffNotificationRecipientUpdateFields,
    StaffUpdateFields,
    StockBulkUpdateFields,
    StoredPaymentMethodRequestDeleteFields,
    TaxClassCreateFields,
    TaxClassDeleteFields,
    TaxClassUpdateFields,
    TaxConfigurationUpdateFields,
    TaxCountryConfigurationDeleteFields,
    TaxCountryConfigurationUpdateFields,
    TaxExemptionManageFields,
    TransactionCreateFields,
    TransactionEventReportFields,
    TransactionInitializeFields,
    TransactionProcessFields,
    TransactionRequestActionFields,
    TransactionRequestRefundForGrantedRefundFields,
    TransactionUpdateFields,
    UpdateMetadataFields,
    UpdatePrivateMetadataFields,
    UserAvatarDeleteFields,
    UserAvatarUpdateFields,
    UserBulkSetActiveFields,
    VariantMediaAssignFields,
    VariantMediaUnassignFields,
    VerifyTokenFields,
    VoucherAddCataloguesFields,
    VoucherBulkDeleteFields,
    VoucherChannelListingUpdateFields,
    VoucherCodeBulkDeleteFields,
    VoucherCreateFields,
    VoucherDeleteFields,
    VoucherRemoveCataloguesFields,
    VoucherTranslateFields,
    VoucherUpdateFields,
    WarehouseCreateFields,
    WarehouseDeleteFields,
    WarehouseShippingZoneAssignFields,
    WarehouseShippingZoneUnassignFields,
    WarehouseUpdateFields,
    WebhookCreateFields,
    WebhookDeleteFields,
    WebhookDryRunFields,
    WebhookTriggerFields,
    WebhookUpdateFields,
)
from .enums import (
    AddressTypeEnum,
    CountryCode,
    ErrorPolicyEnum,
    LanguageCodeEnum,
    NavigationType,
    ProductAttributeType,
    StockUpdatePolicyEnum,
    TokenizedPaymentFlowEnum,
    TransactionActionEnum,
    TransactionEventTypeEnum,
    TransactionFlowStrategyEnum,
)
from .input_types import (
    AccountInput,
    AccountRegisterInput,
    AddressInput,
    AppInput,
    AppInstallInput,
    AppTokenInput,
    AttributeBulkTranslateInput,
    AttributeBulkUpdateInput,
    AttributeCreateInput,
    AttributeUpdateInput,
    AttributeValueBulkTranslateInput,
    AttributeValueCreateInput,
    AttributeValueTranslationInput,
    AttributeValueUpdateInput,
    CatalogueInput,
    CategoryInput,
    ChannelCreateInput,
    ChannelDeleteInput,
    ChannelUpdateInput,
    CheckoutAddressValidationRules,
    CheckoutCreateInput,
    CheckoutLineInput,
    CheckoutLineUpdateInput,
    CollectionChannelListingUpdateInput,
    CollectionCreateInput,
    CollectionInput,
    CustomerBulkUpdateInput,
    CustomerInput,
    DigitalContentInput,
    DigitalContentUploadInput,
    DigitalContentUrlCreateInput,
    DraftOrderCreateInput,
    DraftOrderInput,
    ExportGiftCardsInput,
    ExportProductsInput,
    ExportVoucherCodesInput,
    ExternalNotificationTriggerInput,
    FulfillmentCancelInput,
    FulfillmentUpdateTrackingInput,
    GiftCardAddNoteInput,
    GiftCardBulkCreateInput,
    GiftCardCreateInput,
    GiftCardResendInput,
    GiftCardSettingsUpdateInput,
    GiftCardUpdateInput,
    InvoiceCreateInput,
    MenuCreateInput,
    MenuInput,
    MenuItemCreateInput,
    MenuItemInput,
    MenuItemMoveInput,
    MetadataInput,
    MoveProductInput,
    NameTranslationInput,
    OrderAddNoteInput,
    OrderBulkCreateInput,
    OrderDiscountCommonInput,
    OrderFulfillInput,
    OrderGrantRefundCreateInput,
    OrderGrantRefundUpdateInput,
    OrderLineCreateInput,
    OrderLineInput,
    OrderNoteInput,
    OrderRefundProductsInput,
    OrderReturnProductsInput,
    OrderSettingsUpdateInput,
    OrderUpdateInput,
    OrderUpdateShippingInput,
    PageCreateInput,
    PageInput,
    PageTranslationInput,
    PageTypeCreateInput,
    PageTypeUpdateInput,
    PaymentCheckBalanceInput,
    PaymentGatewayToInitialize,
    PaymentInput,
    PermissionGroupCreateInput,
    PermissionGroupUpdateInput,
    PluginUpdateInput,
    ProductAttributeAssignInput,
    ProductAttributeAssignmentUpdateInput,
    ProductBulkCreateInput,
    ProductBulkTranslateInput,
    ProductChannelListingUpdateInput,
    ProductCreateInput,
    ProductInput,
    ProductMediaCreateInput,
    ProductMediaUpdateInput,
    ProductTypeInput,
    ProductVariantBulkCreateInput,
    ProductVariantBulkTranslateInput,
    ProductVariantBulkUpdateInput,
    ProductVariantChannelListingAddInput,
    ProductVariantCreateInput,
    ProductVariantInput,
    PromotionCreateInput,
    PromotionRuleCreateInput,
    PromotionRuleTranslationInput,
    PromotionRuleUpdateInput,
    PromotionTranslationInput,
    PromotionUpdateInput,
    ReorderInput,
    SaleChannelListingInput,
    SaleInput,
    ShippingMethodChannelListingInput,
    ShippingPriceExcludeProductsInput,
    ShippingPriceInput,
    ShippingPriceTranslationInput,
    ShippingZoneCreateInput,
    ShippingZoneUpdateInput,
    ShopSettingsInput,
    ShopSettingsTranslationInput,
    SiteDomainInput,
    StaffCreateInput,
    StaffNotificationRecipientInput,
    StaffUpdateInput,
    StockBulkUpdateInput,
    StockInput,
    TaxClassCreateInput,
    TaxClassRateInput,
    TaxClassUpdateInput,
    TaxConfigurationUpdateInput,
    TransactionCreateInput,
    TransactionEventInput,
    TransactionUpdateInput,
    TranslationInput,
    UpdateInvoiceInput,
    UserCreateInput,
    VoucherChannelListingInput,
    VoucherInput,
    WarehouseCreateInput,
    WarehouseUpdateInput,
    WebhookCreateInput,
    WebhookUpdateInput,
)


class Mutation:
    @classmethod
    def webhook_create(
        cls, *, input: Optional[WebhookCreateInput] = None
    ) -> WebhookCreateFields:
        return WebhookCreateFields(field_name="webhookCreate", input=input)

    @classmethod
    def webhook_delete(cls, *, id: Optional[str] = None) -> WebhookDeleteFields:
        return WebhookDeleteFields(field_name="webhookDelete", id=id)

    @classmethod
    def webhook_update(
        cls, *, id: Optional[str] = None, input: Optional[WebhookUpdateInput] = None
    ) -> WebhookUpdateFields:
        return WebhookUpdateFields(field_name="webhookUpdate", id=id, input=input)

    @classmethod
    def event_delivery_retry(
        cls, *, id: Optional[str] = None
    ) -> EventDeliveryRetryFields:
        return EventDeliveryRetryFields(field_name="eventDeliveryRetry", id=id)

    @classmethod
    def webhook_dry_run(
        cls, *, objectId: Optional[str] = None, query: Optional[str] = None
    ) -> WebhookDryRunFields:
        return WebhookDryRunFields(
            field_name="webhookDryRun", objectId=objectId, query=query
        )

    @classmethod
    def webhook_trigger(
        cls, *, objectId: Optional[str] = None, webhookId: Optional[str] = None
    ) -> WebhookTriggerFields:
        return WebhookTriggerFields(
            field_name="webhookTrigger", objectId=objectId, webhookId=webhookId
        )

    @classmethod
    def create_warehouse(
        cls, *, input: Optional[WarehouseCreateInput] = None
    ) -> WarehouseCreateFields:
        return WarehouseCreateFields(field_name="createWarehouse", input=input)

    @classmethod
    def update_warehouse(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[WarehouseUpdateInput] = None
    ) -> WarehouseUpdateFields:
        return WarehouseUpdateFields(
            field_name="updateWarehouse",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def delete_warehouse(cls, *, id: Optional[str] = None) -> WarehouseDeleteFields:
        return WarehouseDeleteFields(field_name="deleteWarehouse", id=id)

    @classmethod
    def assign_warehouse_shipping_zone(
        cls, *, id: Optional[str] = None, shippingZoneIds: Optional[str] = None
    ) -> WarehouseShippingZoneAssignFields:
        return WarehouseShippingZoneAssignFields(
            field_name="assignWarehouseShippingZone",
            id=id,
            shippingZoneIds=shippingZoneIds,
        )

    @classmethod
    def unassign_warehouse_shipping_zone(
        cls, *, id: Optional[str] = None, shippingZoneIds: Optional[str] = None
    ) -> WarehouseShippingZoneUnassignFields:
        return WarehouseShippingZoneUnassignFields(
            field_name="unassignWarehouseShippingZone",
            id=id,
            shippingZoneIds=shippingZoneIds,
        )

    @classmethod
    def tax_class_create(
        cls, *, input: Optional[TaxClassCreateInput] = None
    ) -> TaxClassCreateFields:
        return TaxClassCreateFields(field_name="taxClassCreate", input=input)

    @classmethod
    def tax_class_delete(cls, *, id: Optional[str] = None) -> TaxClassDeleteFields:
        return TaxClassDeleteFields(field_name="taxClassDelete", id=id)

    @classmethod
    def tax_class_update(
        cls, *, id: Optional[str] = None, input: Optional[TaxClassUpdateInput] = None
    ) -> TaxClassUpdateFields:
        return TaxClassUpdateFields(field_name="taxClassUpdate", id=id, input=input)

    @classmethod
    def tax_configuration_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[TaxConfigurationUpdateInput] = None
    ) -> TaxConfigurationUpdateFields:
        return TaxConfigurationUpdateFields(
            field_name="taxConfigurationUpdate", id=id, input=input
        )

    @classmethod
    def tax_country_configuration_update(
        cls,
        *,
        countryCode: Optional[CountryCode] = None,
        updateTaxClassRates: Optional[TaxClassRateInput] = None
    ) -> TaxCountryConfigurationUpdateFields:
        return TaxCountryConfigurationUpdateFields(
            field_name="taxCountryConfigurationUpdate",
            countryCode=countryCode,
            updateTaxClassRates=updateTaxClassRates,
        )

    @classmethod
    def tax_country_configuration_delete(
        cls, *, countryCode: Optional[CountryCode] = None
    ) -> TaxCountryConfigurationDeleteFields:
        return TaxCountryConfigurationDeleteFields(
            field_name="taxCountryConfigurationDelete", countryCode=countryCode
        )

    @classmethod
    def tax_exemption_manage(
        cls, *, id: Optional[str] = None, taxExemption: Optional[bool] = None
    ) -> TaxExemptionManageFields:
        return TaxExemptionManageFields(
            field_name="taxExemptionManage", id=id, taxExemption=taxExemption
        )

    @classmethod
    def stock_bulk_update(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        stocks: Optional[StockBulkUpdateInput] = None
    ) -> StockBulkUpdateFields:
        return StockBulkUpdateFields(
            field_name="stockBulkUpdate", errorPolicy=errorPolicy, stocks=stocks
        )

    @classmethod
    def staff_notification_recipient_create(
        cls, *, input: Optional[StaffNotificationRecipientInput] = None
    ) -> StaffNotificationRecipientCreateFields:
        return StaffNotificationRecipientCreateFields(
            field_name="staffNotificationRecipientCreate", input=input
        )

    @classmethod
    def staff_notification_recipient_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[StaffNotificationRecipientInput] = None
    ) -> StaffNotificationRecipientUpdateFields:
        return StaffNotificationRecipientUpdateFields(
            field_name="staffNotificationRecipientUpdate", id=id, input=input
        )

    @classmethod
    def staff_notification_recipient_delete(
        cls, *, id: Optional[str] = None
    ) -> StaffNotificationRecipientDeleteFields:
        return StaffNotificationRecipientDeleteFields(
            field_name="staffNotificationRecipientDelete", id=id
        )

    @classmethod
    def shop_domain_update(
        cls, *, input: Optional[SiteDomainInput] = None
    ) -> ShopDomainUpdateFields:
        return ShopDomainUpdateFields(field_name="shopDomainUpdate", input=input)

    @classmethod
    def shop_settings_update(
        cls, *, input: Optional[ShopSettingsInput] = None
    ) -> ShopSettingsUpdateFields:
        return ShopSettingsUpdateFields(field_name="shopSettingsUpdate", input=input)

    @classmethod
    def shop_fetch_tax_rates(cls) -> ShopFetchTaxRatesFields:
        return ShopFetchTaxRatesFields(field_name="shopFetchTaxRates")

    @classmethod
    def shop_settings_translate(
        cls,
        *,
        input: Optional[ShopSettingsTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> ShopSettingsTranslateFields:
        return ShopSettingsTranslateFields(
            field_name="shopSettingsTranslate", input=input, languageCode=languageCode
        )

    @classmethod
    def shop_address_update(
        cls, *, input: Optional[AddressInput] = None
    ) -> ShopAddressUpdateFields:
        return ShopAddressUpdateFields(field_name="shopAddressUpdate", input=input)

    @classmethod
    def order_settings_update(
        cls, *, input: Optional[OrderSettingsUpdateInput] = None
    ) -> OrderSettingsUpdateFields:
        return OrderSettingsUpdateFields(field_name="orderSettingsUpdate", input=input)

    @classmethod
    def gift_card_settings_update(
        cls, *, input: Optional[GiftCardSettingsUpdateInput] = None
    ) -> GiftCardSettingsUpdateFields:
        return GiftCardSettingsUpdateFields(
            field_name="giftCardSettingsUpdate", input=input
        )

    @classmethod
    def shipping_method_channel_listing_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ShippingMethodChannelListingInput] = None
    ) -> ShippingMethodChannelListingUpdateFields:
        return ShippingMethodChannelListingUpdateFields(
            field_name="shippingMethodChannelListingUpdate", id=id, input=input
        )

    @classmethod
    def shipping_price_create(
        cls, *, input: Optional[ShippingPriceInput] = None
    ) -> ShippingPriceCreateFields:
        return ShippingPriceCreateFields(field_name="shippingPriceCreate", input=input)

    @classmethod
    def shipping_price_delete(
        cls, *, id: Optional[str] = None
    ) -> ShippingPriceDeleteFields:
        return ShippingPriceDeleteFields(field_name="shippingPriceDelete", id=id)

    @classmethod
    def shipping_price_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> ShippingPriceBulkDeleteFields:
        return ShippingPriceBulkDeleteFields(
            field_name="shippingPriceBulkDelete", ids=ids
        )

    @classmethod
    def shipping_price_update(
        cls, *, id: Optional[str] = None, input: Optional[ShippingPriceInput] = None
    ) -> ShippingPriceUpdateFields:
        return ShippingPriceUpdateFields(
            field_name="shippingPriceUpdate", id=id, input=input
        )

    @classmethod
    def shipping_price_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ShippingPriceTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> ShippingPriceTranslateFields:
        return ShippingPriceTranslateFields(
            field_name="shippingPriceTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def shipping_price_exclude_products(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ShippingPriceExcludeProductsInput] = None
    ) -> ShippingPriceExcludeProductsFields:
        return ShippingPriceExcludeProductsFields(
            field_name="shippingPriceExcludeProducts", id=id, input=input
        )

    @classmethod
    def shipping_price_remove_product_from_exclude(
        cls, *, id: Optional[str] = None, products: Optional[str] = None
    ) -> ShippingPriceRemoveProductFromExcludeFields:
        return ShippingPriceRemoveProductFromExcludeFields(
            field_name="shippingPriceRemoveProductFromExclude", id=id, products=products
        )

    @classmethod
    def shipping_zone_create(
        cls, *, input: Optional[ShippingZoneCreateInput] = None
    ) -> ShippingZoneCreateFields:
        return ShippingZoneCreateFields(field_name="shippingZoneCreate", input=input)

    @classmethod
    def shipping_zone_delete(
        cls, *, id: Optional[str] = None
    ) -> ShippingZoneDeleteFields:
        return ShippingZoneDeleteFields(field_name="shippingZoneDelete", id=id)

    @classmethod
    def shipping_zone_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> ShippingZoneBulkDeleteFields:
        return ShippingZoneBulkDeleteFields(
            field_name="shippingZoneBulkDelete", ids=ids
        )

    @classmethod
    def shipping_zone_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ShippingZoneUpdateInput] = None
    ) -> ShippingZoneUpdateFields:
        return ShippingZoneUpdateFields(
            field_name="shippingZoneUpdate", id=id, input=input
        )

    @classmethod
    def product_attribute_assign(
        cls,
        *,
        operations: Optional[ProductAttributeAssignInput] = None,
        productTypeId: Optional[str] = None
    ) -> ProductAttributeAssignFields:
        return ProductAttributeAssignFields(
            field_name="productAttributeAssign",
            operations=operations,
            productTypeId=productTypeId,
        )

    @classmethod
    def product_attribute_assignment_update(
        cls,
        *,
        operations: Optional[ProductAttributeAssignmentUpdateInput] = None,
        productTypeId: Optional[str] = None
    ) -> ProductAttributeAssignmentUpdateFields:
        return ProductAttributeAssignmentUpdateFields(
            field_name="productAttributeAssignmentUpdate",
            operations=operations,
            productTypeId=productTypeId,
        )

    @classmethod
    def product_attribute_unassign(
        cls, *, attributeIds: Optional[str] = None, productTypeId: Optional[str] = None
    ) -> ProductAttributeUnassignFields:
        return ProductAttributeUnassignFields(
            field_name="productAttributeUnassign",
            attributeIds=attributeIds,
            productTypeId=productTypeId,
        )

    @classmethod
    def category_create(
        cls, *, input: Optional[CategoryInput] = None, parent: Optional[str] = None
    ) -> CategoryCreateFields:
        return CategoryCreateFields(
            field_name="categoryCreate", input=input, parent=parent
        )

    @classmethod
    def category_delete(cls, *, id: Optional[str] = None) -> CategoryDeleteFields:
        return CategoryDeleteFields(field_name="categoryDelete", id=id)

    @classmethod
    def category_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> CategoryBulkDeleteFields:
        return CategoryBulkDeleteFields(field_name="categoryBulkDelete", ids=ids)

    @classmethod
    def category_update(
        cls, *, id: Optional[str] = None, input: Optional[CategoryInput] = None
    ) -> CategoryUpdateFields:
        return CategoryUpdateFields(field_name="categoryUpdate", id=id, input=input)

    @classmethod
    def category_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[TranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> CategoryTranslateFields:
        return CategoryTranslateFields(
            field_name="categoryTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def collection_add_products(
        cls, *, collectionId: Optional[str] = None, products: Optional[str] = None
    ) -> CollectionAddProductsFields:
        return CollectionAddProductsFields(
            field_name="collectionAddProducts",
            collectionId=collectionId,
            products=products,
        )

    @classmethod
    def collection_create(
        cls, *, input: Optional[CollectionCreateInput] = None
    ) -> CollectionCreateFields:
        return CollectionCreateFields(field_name="collectionCreate", input=input)

    @classmethod
    def collection_delete(cls, *, id: Optional[str] = None) -> CollectionDeleteFields:
        return CollectionDeleteFields(field_name="collectionDelete", id=id)

    @classmethod
    def collection_reorder_products(
        cls,
        *,
        collectionId: Optional[str] = None,
        moves: Optional[MoveProductInput] = None
    ) -> CollectionReorderProductsFields:
        return CollectionReorderProductsFields(
            field_name="collectionReorderProducts",
            collectionId=collectionId,
            moves=moves,
        )

    @classmethod
    def collection_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> CollectionBulkDeleteFields:
        return CollectionBulkDeleteFields(field_name="collectionBulkDelete", ids=ids)

    @classmethod
    def collection_remove_products(
        cls, *, collectionId: Optional[str] = None, products: Optional[str] = None
    ) -> CollectionRemoveProductsFields:
        return CollectionRemoveProductsFields(
            field_name="collectionRemoveProducts",
            collectionId=collectionId,
            products=products,
        )

    @classmethod
    def collection_update(
        cls, *, id: Optional[str] = None, input: Optional[CollectionInput] = None
    ) -> CollectionUpdateFields:
        return CollectionUpdateFields(field_name="collectionUpdate", id=id, input=input)

    @classmethod
    def collection_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[TranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> CollectionTranslateFields:
        return CollectionTranslateFields(
            field_name="collectionTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def collection_channel_listing_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[CollectionChannelListingUpdateInput] = None
    ) -> CollectionChannelListingUpdateFields:
        return CollectionChannelListingUpdateFields(
            field_name="collectionChannelListingUpdate", id=id, input=input
        )

    @classmethod
    def product_create(
        cls, *, input: Optional[ProductCreateInput] = None
    ) -> ProductCreateFields:
        return ProductCreateFields(field_name="productCreate", input=input)

    @classmethod
    def product_delete(
        cls, *, externalReference: Optional[str] = None, id: Optional[str] = None
    ) -> ProductDeleteFields:
        return ProductDeleteFields(
            field_name="productDelete", externalReference=externalReference, id=id
        )

    @classmethod
    def product_bulk_create(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        products: Optional[ProductBulkCreateInput] = None
    ) -> ProductBulkCreateFields:
        return ProductBulkCreateFields(
            field_name="productBulkCreate", errorPolicy=errorPolicy, products=products
        )

    @classmethod
    def product_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> ProductBulkDeleteFields:
        return ProductBulkDeleteFields(field_name="productBulkDelete", ids=ids)

    @classmethod
    def product_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[ProductInput] = None
    ) -> ProductUpdateFields:
        return ProductUpdateFields(
            field_name="productUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def product_bulk_translate(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        translations: Optional[ProductBulkTranslateInput] = None
    ) -> ProductBulkTranslateFields:
        return ProductBulkTranslateFields(
            field_name="productBulkTranslate",
            errorPolicy=errorPolicy,
            translations=translations,
        )

    @classmethod
    def product_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[TranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> ProductTranslateFields:
        return ProductTranslateFields(
            field_name="productTranslate", id=id, input=input, languageCode=languageCode
        )

    @classmethod
    def product_channel_listing_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ProductChannelListingUpdateInput] = None
    ) -> ProductChannelListingUpdateFields:
        return ProductChannelListingUpdateFields(
            field_name="productChannelListingUpdate", id=id, input=input
        )

    @classmethod
    def product_media_create(
        cls, *, input: Optional[ProductMediaCreateInput] = None
    ) -> ProductMediaCreateFields:
        return ProductMediaCreateFields(field_name="productMediaCreate", input=input)

    @classmethod
    def product_variant_reorder(
        cls, *, moves: Optional[ReorderInput] = None, productId: Optional[str] = None
    ) -> ProductVariantReorderFields:
        return ProductVariantReorderFields(
            field_name="productVariantReorder", moves=moves, productId=productId
        )

    @classmethod
    def product_media_delete(
        cls, *, id: Optional[str] = None
    ) -> ProductMediaDeleteFields:
        return ProductMediaDeleteFields(field_name="productMediaDelete", id=id)

    @classmethod
    def product_media_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> ProductMediaBulkDeleteFields:
        return ProductMediaBulkDeleteFields(
            field_name="productMediaBulkDelete", ids=ids
        )

    @classmethod
    def product_media_reorder(
        cls, *, mediaIds: Optional[str] = None, productId: Optional[str] = None
    ) -> ProductMediaReorderFields:
        return ProductMediaReorderFields(
            field_name="productMediaReorder", mediaIds=mediaIds, productId=productId
        )

    @classmethod
    def product_media_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ProductMediaUpdateInput] = None
    ) -> ProductMediaUpdateFields:
        return ProductMediaUpdateFields(
            field_name="productMediaUpdate", id=id, input=input
        )

    @classmethod
    def product_type_create(
        cls, *, input: Optional[ProductTypeInput] = None
    ) -> ProductTypeCreateFields:
        return ProductTypeCreateFields(field_name="productTypeCreate", input=input)

    @classmethod
    def product_type_delete(
        cls, *, id: Optional[str] = None
    ) -> ProductTypeDeleteFields:
        return ProductTypeDeleteFields(field_name="productTypeDelete", id=id)

    @classmethod
    def product_type_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> ProductTypeBulkDeleteFields:
        return ProductTypeBulkDeleteFields(field_name="productTypeBulkDelete", ids=ids)

    @classmethod
    def product_type_update(
        cls, *, id: Optional[str] = None, input: Optional[ProductTypeInput] = None
    ) -> ProductTypeUpdateFields:
        return ProductTypeUpdateFields(
            field_name="productTypeUpdate", id=id, input=input
        )

    @classmethod
    def product_type_reorder_attributes(
        cls,
        *,
        moves: Optional[ReorderInput] = None,
        productTypeId: Optional[str] = None,
        type: Optional[ProductAttributeType] = None
    ) -> ProductTypeReorderAttributesFields:
        return ProductTypeReorderAttributesFields(
            field_name="productTypeReorderAttributes",
            moves=moves,
            productTypeId=productTypeId,
            type=type,
        )

    @classmethod
    def product_reorder_attribute_values(
        cls,
        *,
        attributeId: Optional[str] = None,
        moves: Optional[ReorderInput] = None,
        productId: Optional[str] = None
    ) -> ProductReorderAttributeValuesFields:
        return ProductReorderAttributeValuesFields(
            field_name="productReorderAttributeValues",
            attributeId=attributeId,
            moves=moves,
            productId=productId,
        )

    @classmethod
    def digital_content_create(
        cls,
        *,
        input: Optional[DigitalContentUploadInput] = None,
        variantId: Optional[str] = None
    ) -> DigitalContentCreateFields:
        return DigitalContentCreateFields(
            field_name="digitalContentCreate", input=input, variantId=variantId
        )

    @classmethod
    def digital_content_delete(
        cls, *, variantId: Optional[str] = None
    ) -> DigitalContentDeleteFields:
        return DigitalContentDeleteFields(
            field_name="digitalContentDelete", variantId=variantId
        )

    @classmethod
    def digital_content_update(
        cls,
        *,
        input: Optional[DigitalContentInput] = None,
        variantId: Optional[str] = None
    ) -> DigitalContentUpdateFields:
        return DigitalContentUpdateFields(
            field_name="digitalContentUpdate", input=input, variantId=variantId
        )

    @classmethod
    def digital_content_url_create(
        cls, *, input: Optional[DigitalContentUrlCreateInput] = None
    ) -> DigitalContentUrlCreateFields:
        return DigitalContentUrlCreateFields(
            field_name="digitalContentUrlCreate", input=input
        )

    @classmethod
    def product_variant_create(
        cls, *, input: Optional[ProductVariantCreateInput] = None
    ) -> ProductVariantCreateFields:
        return ProductVariantCreateFields(
            field_name="productVariantCreate", input=input
        )

    @classmethod
    def product_variant_delete(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        sku: Optional[str] = None
    ) -> ProductVariantDeleteFields:
        return ProductVariantDeleteFields(
            field_name="productVariantDelete",
            externalReference=externalReference,
            id=id,
            sku=sku,
        )

    @classmethod
    def product_variant_bulk_create(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        product: Optional[str] = None,
        variants: Optional[ProductVariantBulkCreateInput] = None
    ) -> ProductVariantBulkCreateFields:
        return ProductVariantBulkCreateFields(
            field_name="productVariantBulkCreate",
            errorPolicy=errorPolicy,
            product=product,
            variants=variants,
        )

    @classmethod
    def product_variant_bulk_update(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        product: Optional[str] = None,
        variants: Optional[ProductVariantBulkUpdateInput] = None
    ) -> ProductVariantBulkUpdateFields:
        return ProductVariantBulkUpdateFields(
            field_name="productVariantBulkUpdate",
            errorPolicy=errorPolicy,
            product=product,
            variants=variants,
        )

    @classmethod
    def product_variant_bulk_delete(
        cls, *, ids: Optional[str] = None, skus: Optional[str] = None
    ) -> ProductVariantBulkDeleteFields:
        return ProductVariantBulkDeleteFields(
            field_name="productVariantBulkDelete", ids=ids, skus=skus
        )

    @classmethod
    def product_variant_stocks_create(
        cls, *, stocks: Optional[StockInput] = None, variantId: Optional[str] = None
    ) -> ProductVariantStocksCreateFields:
        return ProductVariantStocksCreateFields(
            field_name="productVariantStocksCreate", stocks=stocks, variantId=variantId
        )

    @classmethod
    def product_variant_stocks_delete(
        cls,
        *,
        sku: Optional[str] = None,
        variantId: Optional[str] = None,
        warehouseIds: Optional[str] = None
    ) -> ProductVariantStocksDeleteFields:
        return ProductVariantStocksDeleteFields(
            field_name="productVariantStocksDelete",
            sku=sku,
            variantId=variantId,
            warehouseIds=warehouseIds,
        )

    @classmethod
    def product_variant_stocks_update(
        cls,
        *,
        sku: Optional[str] = None,
        stocks: Optional[StockInput] = None,
        variantId: Optional[str] = None
    ) -> ProductVariantStocksUpdateFields:
        return ProductVariantStocksUpdateFields(
            field_name="productVariantStocksUpdate",
            sku=sku,
            stocks=stocks,
            variantId=variantId,
        )

    @classmethod
    def product_variant_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[ProductVariantInput] = None,
        sku: Optional[str] = None
    ) -> ProductVariantUpdateFields:
        return ProductVariantUpdateFields(
            field_name="productVariantUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
            sku=sku,
        )

    @classmethod
    def product_variant_set_default(
        cls, *, productId: Optional[str] = None, variantId: Optional[str] = None
    ) -> ProductVariantSetDefaultFields:
        return ProductVariantSetDefaultFields(
            field_name="productVariantSetDefault",
            productId=productId,
            variantId=variantId,
        )

    @classmethod
    def product_variant_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[NameTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> ProductVariantTranslateFields:
        return ProductVariantTranslateFields(
            field_name="productVariantTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def product_variant_bulk_translate(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        translations: Optional[ProductVariantBulkTranslateInput] = None
    ) -> ProductVariantBulkTranslateFields:
        return ProductVariantBulkTranslateFields(
            field_name="productVariantBulkTranslate",
            errorPolicy=errorPolicy,
            translations=translations,
        )

    @classmethod
    def product_variant_channel_listing_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[ProductVariantChannelListingAddInput] = None,
        sku: Optional[str] = None
    ) -> ProductVariantChannelListingUpdateFields:
        return ProductVariantChannelListingUpdateFields(
            field_name="productVariantChannelListingUpdate", id=id, input=input, sku=sku
        )

    @classmethod
    def product_variant_reorder_attribute_values(
        cls,
        *,
        attributeId: Optional[str] = None,
        moves: Optional[ReorderInput] = None,
        variantId: Optional[str] = None
    ) -> ProductVariantReorderAttributeValuesFields:
        return ProductVariantReorderAttributeValuesFields(
            field_name="productVariantReorderAttributeValues",
            attributeId=attributeId,
            moves=moves,
            variantId=variantId,
        )

    @classmethod
    def product_variant_preorder_deactivate(
        cls, *, id: Optional[str] = None
    ) -> ProductVariantPreorderDeactivateFields:
        return ProductVariantPreorderDeactivateFields(
            field_name="productVariantPreorderDeactivate", id=id
        )

    @classmethod
    def variant_media_assign(
        cls, *, mediaId: Optional[str] = None, variantId: Optional[str] = None
    ) -> VariantMediaAssignFields:
        return VariantMediaAssignFields(
            field_name="variantMediaAssign", mediaId=mediaId, variantId=variantId
        )

    @classmethod
    def variant_media_unassign(
        cls, *, mediaId: Optional[str] = None, variantId: Optional[str] = None
    ) -> VariantMediaUnassignFields:
        return VariantMediaUnassignFields(
            field_name="variantMediaUnassign", mediaId=mediaId, variantId=variantId
        )

    @classmethod
    def payment_capture(
        cls, *, amount: Optional[Any] = None, paymentId: Optional[str] = None
    ) -> PaymentCaptureFields:
        return PaymentCaptureFields(
            field_name="paymentCapture", amount=amount, paymentId=paymentId
        )

    @classmethod
    def payment_refund(
        cls, *, amount: Optional[Any] = None, paymentId: Optional[str] = None
    ) -> PaymentRefundFields:
        return PaymentRefundFields(
            field_name="paymentRefund", amount=amount, paymentId=paymentId
        )

    @classmethod
    def payment_void(cls, *, paymentId: Optional[str] = None) -> PaymentVoidFields:
        return PaymentVoidFields(field_name="paymentVoid", paymentId=paymentId)

    @classmethod
    def payment_initialize(
        cls,
        *,
        channel: Optional[str] = None,
        gateway: Optional[str] = None,
        paymentData: Optional[Any] = None
    ) -> PaymentInitializeFields:
        return PaymentInitializeFields(
            field_name="paymentInitialize",
            channel=channel,
            gateway=gateway,
            paymentData=paymentData,
        )

    @classmethod
    def payment_check_balance(
        cls, *, input: Optional[PaymentCheckBalanceInput] = None
    ) -> PaymentCheckBalanceFields:
        return PaymentCheckBalanceFields(field_name="paymentCheckBalance", input=input)

    @classmethod
    def transaction_create(
        cls,
        *,
        id: Optional[str] = None,
        transaction: Optional[TransactionCreateInput] = None,
        transactionEvent: Optional[TransactionEventInput] = None
    ) -> TransactionCreateFields:
        return TransactionCreateFields(
            field_name="transactionCreate",
            id=id,
            transaction=transaction,
            transactionEvent=transactionEvent,
        )

    @classmethod
    def transaction_update(
        cls,
        *,
        id: Optional[str] = None,
        token: Optional[Any] = None,
        transaction: Optional[TransactionUpdateInput] = None,
        transactionEvent: Optional[TransactionEventInput] = None
    ) -> TransactionUpdateFields:
        return TransactionUpdateFields(
            field_name="transactionUpdate",
            id=id,
            token=token,
            transaction=transaction,
            transactionEvent=transactionEvent,
        )

    @classmethod
    def transaction_request_action(
        cls,
        *,
        actionType: Optional[TransactionActionEnum] = None,
        amount: Optional[Any] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> TransactionRequestActionFields:
        return TransactionRequestActionFields(
            field_name="transactionRequestAction",
            actionType=actionType,
            amount=amount,
            id=id,
            token=token,
        )

    @classmethod
    def transaction_request_refund_for_granted_refund(
        cls,
        *,
        grantedRefundId: Optional[str] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> TransactionRequestRefundForGrantedRefundFields:
        return TransactionRequestRefundForGrantedRefundFields(
            field_name="transactionRequestRefundForGrantedRefund",
            grantedRefundId=grantedRefundId,
            id=id,
            token=token,
        )

    @classmethod
    def transaction_event_report(
        cls,
        *,
        amount: Optional[Any] = None,
        availableActions: Optional[TransactionActionEnum] = None,
        externalUrl: Optional[str] = None,
        id: Optional[str] = None,
        message: Optional[str] = None,
        pspReference: Optional[str] = None,
        time: Optional[Any] = None,
        token: Optional[Any] = None,
        type: Optional[TransactionEventTypeEnum] = None
    ) -> TransactionEventReportFields:
        return TransactionEventReportFields(
            field_name="transactionEventReport",
            amount=amount,
            availableActions=availableActions,
            externalUrl=externalUrl,
            id=id,
            message=message,
            pspReference=pspReference,
            time=time,
            token=token,
            type=type,
        )

    @classmethod
    def payment_gateway_initialize(
        cls,
        *,
        amount: Optional[Any] = None,
        id: Optional[str] = None,
        paymentGateways: Optional[PaymentGatewayToInitialize] = None
    ) -> PaymentGatewayInitializeFields:
        return PaymentGatewayInitializeFields(
            field_name="paymentGatewayInitialize",
            amount=amount,
            id=id,
            paymentGateways=paymentGateways,
        )

    @classmethod
    def transaction_initialize(
        cls,
        *,
        action: Optional[TransactionFlowStrategyEnum] = None,
        amount: Optional[Any] = None,
        customerIpAddress: Optional[str] = None,
        id: Optional[str] = None,
        idempotencyKey: Optional[str] = None,
        paymentGateway: Optional[PaymentGatewayToInitialize] = None
    ) -> TransactionInitializeFields:
        return TransactionInitializeFields(
            field_name="transactionInitialize",
            action=action,
            amount=amount,
            customerIpAddress=customerIpAddress,
            id=id,
            idempotencyKey=idempotencyKey,
            paymentGateway=paymentGateway,
        )

    @classmethod
    def transaction_process(
        cls,
        *,
        customerIpAddress: Optional[str] = None,
        data: Optional[Any] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> TransactionProcessFields:
        return TransactionProcessFields(
            field_name="transactionProcess",
            customerIpAddress=customerIpAddress,
            data=data,
            id=id,
            token=token,
        )

    @classmethod
    def stored_payment_method_request_delete(
        cls, *, channel: Optional[str] = None, id: Optional[str] = None
    ) -> StoredPaymentMethodRequestDeleteFields:
        return StoredPaymentMethodRequestDeleteFields(
            field_name="storedPaymentMethodRequestDelete", channel=channel, id=id
        )

    @classmethod
    def payment_gateway_initialize_tokenization(
        cls,
        *,
        channel: Optional[str] = None,
        data: Optional[Any] = None,
        id: Optional[str] = None
    ) -> PaymentGatewayInitializeTokenizationFields:
        return PaymentGatewayInitializeTokenizationFields(
            field_name="paymentGatewayInitializeTokenization",
            channel=channel,
            data=data,
            id=id,
        )

    @classmethod
    def payment_method_initialize_tokenization(
        cls,
        *,
        channel: Optional[str] = None,
        data: Optional[Any] = None,
        id: Optional[str] = None,
        paymentFlowToSupport: Optional[TokenizedPaymentFlowEnum] = None
    ) -> PaymentMethodInitializeTokenizationFields:
        return PaymentMethodInitializeTokenizationFields(
            field_name="paymentMethodInitializeTokenization",
            channel=channel,
            data=data,
            id=id,
            paymentFlowToSupport=paymentFlowToSupport,
        )

    @classmethod
    def payment_method_process_tokenization(
        cls,
        *,
        channel: Optional[str] = None,
        data: Optional[Any] = None,
        id: Optional[str] = None
    ) -> PaymentMethodProcessTokenizationFields:
        return PaymentMethodProcessTokenizationFields(
            field_name="paymentMethodProcessTokenization",
            channel=channel,
            data=data,
            id=id,
        )

    @classmethod
    def page_create(
        cls, *, input: Optional[PageCreateInput] = None
    ) -> PageCreateFields:
        return PageCreateFields(field_name="pageCreate", input=input)

    @classmethod
    def page_delete(cls, *, id: Optional[str] = None) -> PageDeleteFields:
        return PageDeleteFields(field_name="pageDelete", id=id)

    @classmethod
    def page_bulk_delete(cls, *, ids: Optional[str] = None) -> PageBulkDeleteFields:
        return PageBulkDeleteFields(field_name="pageBulkDelete", ids=ids)

    @classmethod
    def page_bulk_publish(
        cls, *, ids: Optional[str] = None, isPublished: Optional[bool] = None
    ) -> PageBulkPublishFields:
        return PageBulkPublishFields(
            field_name="pageBulkPublish", ids=ids, isPublished=isPublished
        )

    @classmethod
    def page_update(
        cls, *, id: Optional[str] = None, input: Optional[PageInput] = None
    ) -> PageUpdateFields:
        return PageUpdateFields(field_name="pageUpdate", id=id, input=input)

    @classmethod
    def page_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[PageTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> PageTranslateFields:
        return PageTranslateFields(
            field_name="pageTranslate", id=id, input=input, languageCode=languageCode
        )

    @classmethod
    def page_type_create(
        cls, *, input: Optional[PageTypeCreateInput] = None
    ) -> PageTypeCreateFields:
        return PageTypeCreateFields(field_name="pageTypeCreate", input=input)

    @classmethod
    def page_type_update(
        cls, *, id: Optional[str] = None, input: Optional[PageTypeUpdateInput] = None
    ) -> PageTypeUpdateFields:
        return PageTypeUpdateFields(field_name="pageTypeUpdate", id=id, input=input)

    @classmethod
    def page_type_delete(cls, *, id: Optional[str] = None) -> PageTypeDeleteFields:
        return PageTypeDeleteFields(field_name="pageTypeDelete", id=id)

    @classmethod
    def page_type_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> PageTypeBulkDeleteFields:
        return PageTypeBulkDeleteFields(field_name="pageTypeBulkDelete", ids=ids)

    @classmethod
    def page_attribute_assign(
        cls, *, attributeIds: Optional[str] = None, pageTypeId: Optional[str] = None
    ) -> PageAttributeAssignFields:
        return PageAttributeAssignFields(
            field_name="pageAttributeAssign",
            attributeIds=attributeIds,
            pageTypeId=pageTypeId,
        )

    @classmethod
    def page_attribute_unassign(
        cls, *, attributeIds: Optional[str] = None, pageTypeId: Optional[str] = None
    ) -> PageAttributeUnassignFields:
        return PageAttributeUnassignFields(
            field_name="pageAttributeUnassign",
            attributeIds=attributeIds,
            pageTypeId=pageTypeId,
        )

    @classmethod
    def page_type_reorder_attributes(
        cls, *, moves: Optional[ReorderInput] = None, pageTypeId: Optional[str] = None
    ) -> PageTypeReorderAttributesFields:
        return PageTypeReorderAttributesFields(
            field_name="pageTypeReorderAttributes", moves=moves, pageTypeId=pageTypeId
        )

    @classmethod
    def page_reorder_attribute_values(
        cls,
        *,
        attributeId: Optional[str] = None,
        moves: Optional[ReorderInput] = None,
        pageId: Optional[str] = None
    ) -> PageReorderAttributeValuesFields:
        return PageReorderAttributeValuesFields(
            field_name="pageReorderAttributeValues",
            attributeId=attributeId,
            moves=moves,
            pageId=pageId,
        )

    @classmethod
    def draft_order_complete(
        cls, *, id: Optional[str] = None
    ) -> DraftOrderCompleteFields:
        return DraftOrderCompleteFields(field_name="draftOrderComplete", id=id)

    @classmethod
    def draft_order_create(
        cls, *, input: Optional[DraftOrderCreateInput] = None
    ) -> DraftOrderCreateFields:
        return DraftOrderCreateFields(field_name="draftOrderCreate", input=input)

    @classmethod
    def draft_order_delete(
        cls, *, externalReference: Optional[str] = None, id: Optional[str] = None
    ) -> DraftOrderDeleteFields:
        return DraftOrderDeleteFields(
            field_name="draftOrderDelete", externalReference=externalReference, id=id
        )

    @classmethod
    def draft_order_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> DraftOrderBulkDeleteFields:
        return DraftOrderBulkDeleteFields(field_name="draftOrderBulkDelete", ids=ids)

    @classmethod
    def draft_order_lines_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> DraftOrderLinesBulkDeleteFields:
        return DraftOrderLinesBulkDeleteFields(
            field_name="draftOrderLinesBulkDelete", ids=ids
        )

    @classmethod
    def draft_order_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[DraftOrderInput] = None
    ) -> DraftOrderUpdateFields:
        return DraftOrderUpdateFields(
            field_name="draftOrderUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def order_add_note(
        cls, *, order: Optional[str] = None, input: Optional[OrderAddNoteInput] = None
    ) -> OrderAddNoteFields:
        return OrderAddNoteFields(field_name="orderAddNote", order=order, input=input)

    @classmethod
    def order_cancel(cls, *, id: Optional[str] = None) -> OrderCancelFields:
        return OrderCancelFields(field_name="orderCancel", id=id)

    @classmethod
    def order_capture(
        cls, *, amount: Optional[Any] = None, id: Optional[str] = None
    ) -> OrderCaptureFields:
        return OrderCaptureFields(field_name="orderCapture", amount=amount, id=id)

    @classmethod
    def order_confirm(cls, *, id: Optional[str] = None) -> OrderConfirmFields:
        return OrderConfirmFields(field_name="orderConfirm", id=id)

    @classmethod
    def order_fulfill(
        cls, *, input: Optional[OrderFulfillInput] = None, order: Optional[str] = None
    ) -> OrderFulfillFields:
        return OrderFulfillFields(field_name="orderFulfill", input=input, order=order)

    @classmethod
    def order_fulfillment_cancel(
        cls, *, id: Optional[str] = None, input: Optional[FulfillmentCancelInput] = None
    ) -> FulfillmentCancelFields:
        return FulfillmentCancelFields(
            field_name="orderFulfillmentCancel", id=id, input=input
        )

    @classmethod
    def order_fulfillment_approve(
        cls,
        *,
        allowStockToBeExceeded: Optional[bool] = None,
        id: Optional[str] = None,
        notifyCustomer: Optional[bool] = None
    ) -> FulfillmentApproveFields:
        return FulfillmentApproveFields(
            field_name="orderFulfillmentApprove",
            allowStockToBeExceeded=allowStockToBeExceeded,
            id=id,
            notifyCustomer=notifyCustomer,
        )

    @classmethod
    def order_fulfillment_update_tracking(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[FulfillmentUpdateTrackingInput] = None
    ) -> FulfillmentUpdateTrackingFields:
        return FulfillmentUpdateTrackingFields(
            field_name="orderFulfillmentUpdateTracking", id=id, input=input
        )

    @classmethod
    def order_fulfillment_refund_products(
        cls,
        *,
        input: Optional[OrderRefundProductsInput] = None,
        order: Optional[str] = None
    ) -> FulfillmentRefundProductsFields:
        return FulfillmentRefundProductsFields(
            field_name="orderFulfillmentRefundProducts", input=input, order=order
        )

    @classmethod
    def order_fulfillment_return_products(
        cls,
        *,
        input: Optional[OrderReturnProductsInput] = None,
        order: Optional[str] = None
    ) -> FulfillmentReturnProductsFields:
        return FulfillmentReturnProductsFields(
            field_name="orderFulfillmentReturnProducts", input=input, order=order
        )

    @classmethod
    def order_grant_refund_create(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[OrderGrantRefundCreateInput] = None
    ) -> OrderGrantRefundCreateFields:
        return OrderGrantRefundCreateFields(
            field_name="orderGrantRefundCreate", id=id, input=input
        )

    @classmethod
    def order_grant_refund_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[OrderGrantRefundUpdateInput] = None
    ) -> OrderGrantRefundUpdateFields:
        return OrderGrantRefundUpdateFields(
            field_name="orderGrantRefundUpdate", id=id, input=input
        )

    @classmethod
    def order_lines_create(
        cls, *, id: Optional[str] = None, input: Optional[OrderLineCreateInput] = None
    ) -> OrderLinesCreateFields:
        return OrderLinesCreateFields(field_name="orderLinesCreate", id=id, input=input)

    @classmethod
    def order_line_delete(cls, *, id: Optional[str] = None) -> OrderLineDeleteFields:
        return OrderLineDeleteFields(field_name="orderLineDelete", id=id)

    @classmethod
    def order_line_update(
        cls, *, id: Optional[str] = None, input: Optional[OrderLineInput] = None
    ) -> OrderLineUpdateFields:
        return OrderLineUpdateFields(field_name="orderLineUpdate", id=id, input=input)

    @classmethod
    def order_discount_add(
        cls,
        *,
        input: Optional[OrderDiscountCommonInput] = None,
        orderId: Optional[str] = None
    ) -> OrderDiscountAddFields:
        return OrderDiscountAddFields(
            field_name="orderDiscountAdd", input=input, orderId=orderId
        )

    @classmethod
    def order_discount_update(
        cls,
        *,
        discountId: Optional[str] = None,
        input: Optional[OrderDiscountCommonInput] = None
    ) -> OrderDiscountUpdateFields:
        return OrderDiscountUpdateFields(
            field_name="orderDiscountUpdate", discountId=discountId, input=input
        )

    @classmethod
    def order_discount_delete(
        cls, *, discountId: Optional[str] = None
    ) -> OrderDiscountDeleteFields:
        return OrderDiscountDeleteFields(
            field_name="orderDiscountDelete", discountId=discountId
        )

    @classmethod
    def order_line_discount_update(
        cls,
        *,
        input: Optional[OrderDiscountCommonInput] = None,
        orderLineId: Optional[str] = None
    ) -> OrderLineDiscountUpdateFields:
        return OrderLineDiscountUpdateFields(
            field_name="orderLineDiscountUpdate", input=input, orderLineId=orderLineId
        )

    @classmethod
    def order_line_discount_remove(
        cls, *, orderLineId: Optional[str] = None
    ) -> OrderLineDiscountRemoveFields:
        return OrderLineDiscountRemoveFields(
            field_name="orderLineDiscountRemove", orderLineId=orderLineId
        )

    @classmethod
    def order_note_add(
        cls, *, order: Optional[str] = None, input: Optional[OrderNoteInput] = None
    ) -> OrderNoteAddFields:
        return OrderNoteAddFields(field_name="orderNoteAdd", order=order, input=input)

    @classmethod
    def order_note_update(
        cls, *, note: Optional[str] = None, input: Optional[OrderNoteInput] = None
    ) -> OrderNoteUpdateFields:
        return OrderNoteUpdateFields(
            field_name="orderNoteUpdate", note=note, input=input
        )

    @classmethod
    def order_mark_as_paid(
        cls, *, id: Optional[str] = None, transactionReference: Optional[str] = None
    ) -> OrderMarkAsPaidFields:
        return OrderMarkAsPaidFields(
            field_name="orderMarkAsPaid",
            id=id,
            transactionReference=transactionReference,
        )

    @classmethod
    def order_refund(
        cls, *, amount: Optional[Any] = None, id: Optional[str] = None
    ) -> OrderRefundFields:
        return OrderRefundFields(field_name="orderRefund", amount=amount, id=id)

    @classmethod
    def order_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[OrderUpdateInput] = None
    ) -> OrderUpdateFields:
        return OrderUpdateFields(
            field_name="orderUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def order_update_shipping(
        cls,
        *,
        order: Optional[str] = None,
        input: Optional[OrderUpdateShippingInput] = None
    ) -> OrderUpdateShippingFields:
        return OrderUpdateShippingFields(
            field_name="orderUpdateShipping", order=order, input=input
        )

    @classmethod
    def order_void(cls, *, id: Optional[str] = None) -> OrderVoidFields:
        return OrderVoidFields(field_name="orderVoid", id=id)

    @classmethod
    def order_bulk_cancel(cls, *, ids: Optional[str] = None) -> OrderBulkCancelFields:
        return OrderBulkCancelFields(field_name="orderBulkCancel", ids=ids)

    @classmethod
    def order_bulk_create(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        orders: Optional[OrderBulkCreateInput] = None,
        stockUpdatePolicy: Optional[StockUpdatePolicyEnum] = None
    ) -> OrderBulkCreateFields:
        return OrderBulkCreateFields(
            field_name="orderBulkCreate",
            errorPolicy=errorPolicy,
            orders=orders,
            stockUpdatePolicy=stockUpdatePolicy,
        )

    @classmethod
    def delete_metadata(
        cls, *, id: Optional[str] = None, keys: Optional[str] = None
    ) -> DeleteMetadataFields:
        return DeleteMetadataFields(field_name="deleteMetadata", id=id, keys=keys)

    @classmethod
    def delete_private_metadata(
        cls, *, id: Optional[str] = None, keys: Optional[str] = None
    ) -> DeletePrivateMetadataFields:
        return DeletePrivateMetadataFields(
            field_name="deletePrivateMetadata", id=id, keys=keys
        )

    @classmethod
    def update_metadata(
        cls, *, id: Optional[str] = None, input: Optional[MetadataInput] = None
    ) -> UpdateMetadataFields:
        return UpdateMetadataFields(field_name="updateMetadata", id=id, input=input)

    @classmethod
    def update_private_metadata(
        cls, *, id: Optional[str] = None, input: Optional[MetadataInput] = None
    ) -> UpdatePrivateMetadataFields:
        return UpdatePrivateMetadataFields(
            field_name="updatePrivateMetadata", id=id, input=input
        )

    @classmethod
    def assign_navigation(
        cls,
        *,
        menu: Optional[str] = None,
        navigationType: Optional[NavigationType] = None
    ) -> AssignNavigationFields:
        return AssignNavigationFields(
            field_name="assignNavigation", menu=menu, navigationType=navigationType
        )

    @classmethod
    def menu_create(
        cls, *, input: Optional[MenuCreateInput] = None
    ) -> MenuCreateFields:
        return MenuCreateFields(field_name="menuCreate", input=input)

    @classmethod
    def menu_delete(cls, *, id: Optional[str] = None) -> MenuDeleteFields:
        return MenuDeleteFields(field_name="menuDelete", id=id)

    @classmethod
    def menu_bulk_delete(cls, *, ids: Optional[str] = None) -> MenuBulkDeleteFields:
        return MenuBulkDeleteFields(field_name="menuBulkDelete", ids=ids)

    @classmethod
    def menu_update(
        cls, *, id: Optional[str] = None, input: Optional[MenuInput] = None
    ) -> MenuUpdateFields:
        return MenuUpdateFields(field_name="menuUpdate", id=id, input=input)

    @classmethod
    def menu_item_create(
        cls, *, input: Optional[MenuItemCreateInput] = None
    ) -> MenuItemCreateFields:
        return MenuItemCreateFields(field_name="menuItemCreate", input=input)

    @classmethod
    def menu_item_delete(cls, *, id: Optional[str] = None) -> MenuItemDeleteFields:
        return MenuItemDeleteFields(field_name="menuItemDelete", id=id)

    @classmethod
    def menu_item_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> MenuItemBulkDeleteFields:
        return MenuItemBulkDeleteFields(field_name="menuItemBulkDelete", ids=ids)

    @classmethod
    def menu_item_update(
        cls, *, id: Optional[str] = None, input: Optional[MenuItemInput] = None
    ) -> MenuItemUpdateFields:
        return MenuItemUpdateFields(field_name="menuItemUpdate", id=id, input=input)

    @classmethod
    def menu_item_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[NameTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> MenuItemTranslateFields:
        return MenuItemTranslateFields(
            field_name="menuItemTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def menu_item_move(
        cls, *, menu: Optional[str] = None, moves: Optional[MenuItemMoveInput] = None
    ) -> MenuItemMoveFields:
        return MenuItemMoveFields(field_name="menuItemMove", menu=menu, moves=moves)

    @classmethod
    def invoice_request(
        cls, *, number: Optional[str] = None, orderId: Optional[str] = None
    ) -> InvoiceRequestFields:
        return InvoiceRequestFields(
            field_name="invoiceRequest", number=number, orderId=orderId
        )

    @classmethod
    def invoice_request_delete(
        cls, *, id: Optional[str] = None
    ) -> InvoiceRequestDeleteFields:
        return InvoiceRequestDeleteFields(field_name="invoiceRequestDelete", id=id)

    @classmethod
    def invoice_create(
        cls,
        *,
        input: Optional[InvoiceCreateInput] = None,
        orderId: Optional[str] = None
    ) -> InvoiceCreateFields:
        return InvoiceCreateFields(
            field_name="invoiceCreate", input=input, orderId=orderId
        )

    @classmethod
    def invoice_delete(cls, *, id: Optional[str] = None) -> InvoiceDeleteFields:
        return InvoiceDeleteFields(field_name="invoiceDelete", id=id)

    @classmethod
    def invoice_update(
        cls, *, id: Optional[str] = None, input: Optional[UpdateInvoiceInput] = None
    ) -> InvoiceUpdateFields:
        return InvoiceUpdateFields(field_name="invoiceUpdate", id=id, input=input)

    @classmethod
    def invoice_send_notification(
        cls, *, id: Optional[str] = None
    ) -> InvoiceSendNotificationFields:
        return InvoiceSendNotificationFields(
            field_name="invoiceSendNotification", id=id
        )

    @classmethod
    def gift_card_activate(cls, *, id: Optional[str] = None) -> GiftCardActivateFields:
        return GiftCardActivateFields(field_name="giftCardActivate", id=id)

    @classmethod
    def gift_card_create(
        cls, *, input: Optional[GiftCardCreateInput] = None
    ) -> GiftCardCreateFields:
        return GiftCardCreateFields(field_name="giftCardCreate", input=input)

    @classmethod
    def gift_card_delete(cls, *, id: Optional[str] = None) -> GiftCardDeleteFields:
        return GiftCardDeleteFields(field_name="giftCardDelete", id=id)

    @classmethod
    def gift_card_deactivate(
        cls, *, id: Optional[str] = None
    ) -> GiftCardDeactivateFields:
        return GiftCardDeactivateFields(field_name="giftCardDeactivate", id=id)

    @classmethod
    def gift_card_update(
        cls, *, id: Optional[str] = None, input: Optional[GiftCardUpdateInput] = None
    ) -> GiftCardUpdateFields:
        return GiftCardUpdateFields(field_name="giftCardUpdate", id=id, input=input)

    @classmethod
    def gift_card_resend(
        cls, *, input: Optional[GiftCardResendInput] = None
    ) -> GiftCardResendFields:
        return GiftCardResendFields(field_name="giftCardResend", input=input)

    @classmethod
    def gift_card_add_note(
        cls, *, id: Optional[str] = None, input: Optional[GiftCardAddNoteInput] = None
    ) -> GiftCardAddNoteFields:
        return GiftCardAddNoteFields(field_name="giftCardAddNote", id=id, input=input)

    @classmethod
    def gift_card_bulk_create(
        cls, *, input: Optional[GiftCardBulkCreateInput] = None
    ) -> GiftCardBulkCreateFields:
        return GiftCardBulkCreateFields(field_name="giftCardBulkCreate", input=input)

    @classmethod
    def gift_card_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> GiftCardBulkDeleteFields:
        return GiftCardBulkDeleteFields(field_name="giftCardBulkDelete", ids=ids)

    @classmethod
    def gift_card_bulk_activate(
        cls, *, ids: Optional[str] = None
    ) -> GiftCardBulkActivateFields:
        return GiftCardBulkActivateFields(field_name="giftCardBulkActivate", ids=ids)

    @classmethod
    def gift_card_bulk_deactivate(
        cls, *, ids: Optional[str] = None
    ) -> GiftCardBulkDeactivateFields:
        return GiftCardBulkDeactivateFields(
            field_name="giftCardBulkDeactivate", ids=ids
        )

    @classmethod
    def plugin_update(
        cls,
        *,
        channelId: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[PluginUpdateInput] = None
    ) -> PluginUpdateFields:
        return PluginUpdateFields(
            field_name="pluginUpdate", channelId=channelId, id=id, input=input
        )

    @classmethod
    def external_notification_trigger(
        cls,
        *,
        channel: Optional[str] = None,
        input: Optional[ExternalNotificationTriggerInput] = None,
        pluginId: Optional[str] = None
    ) -> ExternalNotificationTriggerFields:
        return ExternalNotificationTriggerFields(
            field_name="externalNotificationTrigger",
            channel=channel,
            input=input,
            pluginId=pluginId,
        )

    @classmethod
    def promotion_create(
        cls, *, input: Optional[PromotionCreateInput] = None
    ) -> PromotionCreateFields:
        return PromotionCreateFields(field_name="promotionCreate", input=input)

    @classmethod
    def promotion_update(
        cls, *, id: Optional[str] = None, input: Optional[PromotionUpdateInput] = None
    ) -> PromotionUpdateFields:
        return PromotionUpdateFields(field_name="promotionUpdate", id=id, input=input)

    @classmethod
    def promotion_delete(cls, *, id: Optional[str] = None) -> PromotionDeleteFields:
        return PromotionDeleteFields(field_name="promotionDelete", id=id)

    @classmethod
    def promotion_rule_create(
        cls, *, input: Optional[PromotionRuleCreateInput] = None
    ) -> PromotionRuleCreateFields:
        return PromotionRuleCreateFields(field_name="promotionRuleCreate", input=input)

    @classmethod
    def promotion_rule_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[PromotionRuleUpdateInput] = None
    ) -> PromotionRuleUpdateFields:
        return PromotionRuleUpdateFields(
            field_name="promotionRuleUpdate", id=id, input=input
        )

    @classmethod
    def promotion_rule_delete(
        cls, *, id: Optional[str] = None
    ) -> PromotionRuleDeleteFields:
        return PromotionRuleDeleteFields(field_name="promotionRuleDelete", id=id)

    @classmethod
    def promotion_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[PromotionTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> PromotionTranslateFields:
        return PromotionTranslateFields(
            field_name="promotionTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def promotion_rule_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[PromotionRuleTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> PromotionRuleTranslateFields:
        return PromotionRuleTranslateFields(
            field_name="promotionRuleTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def promotion_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> PromotionBulkDeleteFields:
        return PromotionBulkDeleteFields(field_name="promotionBulkDelete", ids=ids)

    @classmethod
    def sale_create(cls, *, input: Optional[SaleInput] = None) -> SaleCreateFields:
        return SaleCreateFields(field_name="saleCreate", input=input)

    @classmethod
    def sale_delete(cls, *, id: Optional[str] = None) -> SaleDeleteFields:
        return SaleDeleteFields(field_name="saleDelete", id=id)

    @classmethod
    def sale_bulk_delete(cls, *, ids: Optional[str] = None) -> SaleBulkDeleteFields:
        return SaleBulkDeleteFields(field_name="saleBulkDelete", ids=ids)

    @classmethod
    def sale_update(
        cls, *, id: Optional[str] = None, input: Optional[SaleInput] = None
    ) -> SaleUpdateFields:
        return SaleUpdateFields(field_name="saleUpdate", id=id, input=input)

    @classmethod
    def sale_catalogues_add(
        cls, *, id: Optional[str] = None, input: Optional[CatalogueInput] = None
    ) -> SaleAddCataloguesFields:
        return SaleAddCataloguesFields(
            field_name="saleCataloguesAdd", id=id, input=input
        )

    @classmethod
    def sale_catalogues_remove(
        cls, *, id: Optional[str] = None, input: Optional[CatalogueInput] = None
    ) -> SaleRemoveCataloguesFields:
        return SaleRemoveCataloguesFields(
            field_name="saleCataloguesRemove", id=id, input=input
        )

    @classmethod
    def sale_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[NameTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> SaleTranslateFields:
        return SaleTranslateFields(
            field_name="saleTranslate", id=id, input=input, languageCode=languageCode
        )

    @classmethod
    def sale_channel_listing_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[SaleChannelListingInput] = None
    ) -> SaleChannelListingUpdateFields:
        return SaleChannelListingUpdateFields(
            field_name="saleChannelListingUpdate", id=id, input=input
        )

    @classmethod
    def voucher_create(
        cls, *, input: Optional[VoucherInput] = None
    ) -> VoucherCreateFields:
        return VoucherCreateFields(field_name="voucherCreate", input=input)

    @classmethod
    def voucher_delete(cls, *, id: Optional[str] = None) -> VoucherDeleteFields:
        return VoucherDeleteFields(field_name="voucherDelete", id=id)

    @classmethod
    def voucher_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> VoucherBulkDeleteFields:
        return VoucherBulkDeleteFields(field_name="voucherBulkDelete", ids=ids)

    @classmethod
    def voucher_update(
        cls, *, id: Optional[str] = None, input: Optional[VoucherInput] = None
    ) -> VoucherUpdateFields:
        return VoucherUpdateFields(field_name="voucherUpdate", id=id, input=input)

    @classmethod
    def voucher_catalogues_add(
        cls, *, id: Optional[str] = None, input: Optional[CatalogueInput] = None
    ) -> VoucherAddCataloguesFields:
        return VoucherAddCataloguesFields(
            field_name="voucherCataloguesAdd", id=id, input=input
        )

    @classmethod
    def voucher_catalogues_remove(
        cls, *, id: Optional[str] = None, input: Optional[CatalogueInput] = None
    ) -> VoucherRemoveCataloguesFields:
        return VoucherRemoveCataloguesFields(
            field_name="voucherCataloguesRemove", id=id, input=input
        )

    @classmethod
    def voucher_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[NameTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> VoucherTranslateFields:
        return VoucherTranslateFields(
            field_name="voucherTranslate", id=id, input=input, languageCode=languageCode
        )

    @classmethod
    def voucher_channel_listing_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[VoucherChannelListingInput] = None
    ) -> VoucherChannelListingUpdateFields:
        return VoucherChannelListingUpdateFields(
            field_name="voucherChannelListingUpdate", id=id, input=input
        )

    @classmethod
    def voucher_code_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> VoucherCodeBulkDeleteFields:
        return VoucherCodeBulkDeleteFields(field_name="voucherCodeBulkDelete", ids=ids)

    @classmethod
    def export_products(
        cls, *, input: Optional[ExportProductsInput] = None
    ) -> ExportProductsFields:
        return ExportProductsFields(field_name="exportProducts", input=input)

    @classmethod
    def export_gift_cards(
        cls, *, input: Optional[ExportGiftCardsInput] = None
    ) -> ExportGiftCardsFields:
        return ExportGiftCardsFields(field_name="exportGiftCards", input=input)

    @classmethod
    def export_voucher_codes(
        cls, *, input: Optional[ExportVoucherCodesInput] = None
    ) -> ExportVoucherCodesFields:
        return ExportVoucherCodesFields(field_name="exportVoucherCodes", input=input)

    @classmethod
    def file_upload(cls, *, file: Optional[Upload] = None) -> FileUploadFields:
        return FileUploadFields(field_name="fileUpload", file=file)

    @classmethod
    def checkout_add_promo_code(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        promoCode: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutAddPromoCodeFields:
        return CheckoutAddPromoCodeFields(
            field_name="checkoutAddPromoCode",
            checkoutId=checkoutId,
            id=id,
            promoCode=promoCode,
            token=token,
        )

    @classmethod
    def checkout_billing_address_update(
        cls,
        *,
        billingAddress: Optional[AddressInput] = None,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None,
        validationRules: Optional[CheckoutAddressValidationRules] = None
    ) -> CheckoutBillingAddressUpdateFields:
        return CheckoutBillingAddressUpdateFields(
            field_name="checkoutBillingAddressUpdate",
            billingAddress=billingAddress,
            checkoutId=checkoutId,
            id=id,
            token=token,
            validationRules=validationRules,
        )

    @classmethod
    def checkout_complete(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        metadata: Optional[MetadataInput] = None,
        paymentData: Optional[Any] = None,
        redirectUrl: Optional[str] = None,
        storeSource: Optional[bool] = None,
        token: Optional[Any] = None
    ) -> CheckoutCompleteFields:
        return CheckoutCompleteFields(
            field_name="checkoutComplete",
            checkoutId=checkoutId,
            id=id,
            metadata=metadata,
            paymentData=paymentData,
            redirectUrl=redirectUrl,
            storeSource=storeSource,
            token=token,
        )

    @classmethod
    def checkout_create(
        cls, *, input: Optional[CheckoutCreateInput] = None
    ) -> CheckoutCreateFields:
        return CheckoutCreateFields(field_name="checkoutCreate", input=input)

    @classmethod
    def checkout_create_from_order(
        cls, *, id: Optional[str] = None
    ) -> CheckoutCreateFromOrderFields:
        return CheckoutCreateFromOrderFields(
            field_name="checkoutCreateFromOrder", id=id
        )

    @classmethod
    def checkout_customer_attach(
        cls,
        *,
        checkoutId: Optional[str] = None,
        customerId: Optional[str] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutCustomerAttachFields:
        return CheckoutCustomerAttachFields(
            field_name="checkoutCustomerAttach",
            checkoutId=checkoutId,
            customerId=customerId,
            id=id,
            token=token,
        )

    @classmethod
    def checkout_customer_detach(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutCustomerDetachFields:
        return CheckoutCustomerDetachFields(
            field_name="checkoutCustomerDetach",
            checkoutId=checkoutId,
            id=id,
            token=token,
        )

    @classmethod
    def checkout_email_update(
        cls,
        *,
        checkoutId: Optional[str] = None,
        email: Optional[str] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutEmailUpdateFields:
        return CheckoutEmailUpdateFields(
            field_name="checkoutEmailUpdate",
            checkoutId=checkoutId,
            email=email,
            id=id,
            token=token,
        )

    @classmethod
    def checkout_line_delete(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        lineId: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutLineDeleteFields:
        return CheckoutLineDeleteFields(
            field_name="checkoutLineDelete",
            checkoutId=checkoutId,
            id=id,
            lineId=lineId,
            token=token,
        )

    @classmethod
    def checkout_lines_delete(
        cls,
        *,
        id: Optional[str] = None,
        linesIds: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutLinesDeleteFields:
        return CheckoutLinesDeleteFields(
            field_name="checkoutLinesDelete", id=id, linesIds=linesIds, token=token
        )

    @classmethod
    def checkout_lines_add(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        lines: Optional[CheckoutLineInput] = None,
        token: Optional[Any] = None
    ) -> CheckoutLinesAddFields:
        return CheckoutLinesAddFields(
            field_name="checkoutLinesAdd",
            checkoutId=checkoutId,
            id=id,
            lines=lines,
            token=token,
        )

    @classmethod
    def checkout_lines_update(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        lines: Optional[CheckoutLineUpdateInput] = None,
        token: Optional[Any] = None
    ) -> CheckoutLinesUpdateFields:
        return CheckoutLinesUpdateFields(
            field_name="checkoutLinesUpdate",
            checkoutId=checkoutId,
            id=id,
            lines=lines,
            token=token,
        )

    @classmethod
    def checkout_remove_promo_code(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        promoCode: Optional[str] = None,
        promoCodeId: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutRemovePromoCodeFields:
        return CheckoutRemovePromoCodeFields(
            field_name="checkoutRemovePromoCode",
            checkoutId=checkoutId,
            id=id,
            promoCode=promoCode,
            promoCodeId=promoCodeId,
            token=token,
        )

    @classmethod
    def checkout_payment_create(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[PaymentInput] = None,
        token: Optional[Any] = None
    ) -> CheckoutPaymentCreateFields:
        return CheckoutPaymentCreateFields(
            field_name="checkoutPaymentCreate",
            checkoutId=checkoutId,
            id=id,
            input=input,
            token=token,
        )

    @classmethod
    def checkout_shipping_address_update(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        shippingAddress: Optional[AddressInput] = None,
        token: Optional[Any] = None,
        validationRules: Optional[CheckoutAddressValidationRules] = None
    ) -> CheckoutShippingAddressUpdateFields:
        return CheckoutShippingAddressUpdateFields(
            field_name="checkoutShippingAddressUpdate",
            checkoutId=checkoutId,
            id=id,
            shippingAddress=shippingAddress,
            token=token,
            validationRules=validationRules,
        )

    @classmethod
    def checkout_shipping_method_update(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        shippingMethodId: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutShippingMethodUpdateFields:
        return CheckoutShippingMethodUpdateFields(
            field_name="checkoutShippingMethodUpdate",
            checkoutId=checkoutId,
            id=id,
            shippingMethodId=shippingMethodId,
            token=token,
        )

    @classmethod
    def checkout_delivery_method_update(
        cls,
        *,
        deliveryMethodId: Optional[str] = None,
        id: Optional[str] = None,
        token: Optional[Any] = None
    ) -> CheckoutDeliveryMethodUpdateFields:
        return CheckoutDeliveryMethodUpdateFields(
            field_name="checkoutDeliveryMethodUpdate",
            deliveryMethodId=deliveryMethodId,
            id=id,
            token=token,
        )

    @classmethod
    def checkout_language_code_update(
        cls,
        *,
        checkoutId: Optional[str] = None,
        id: Optional[str] = None,
        languageCode: Optional[LanguageCodeEnum] = None,
        token: Optional[Any] = None
    ) -> CheckoutLanguageCodeUpdateFields:
        return CheckoutLanguageCodeUpdateFields(
            field_name="checkoutLanguageCodeUpdate",
            checkoutId=checkoutId,
            id=id,
            languageCode=languageCode,
            token=token,
        )

    @classmethod
    def order_create_from_checkout(
        cls,
        *,
        id: Optional[str] = None,
        metadata: Optional[MetadataInput] = None,
        privateMetadata: Optional[MetadataInput] = None,
        removeCheckout: Optional[bool] = None
    ) -> OrderCreateFromCheckoutFields:
        return OrderCreateFromCheckoutFields(
            field_name="orderCreateFromCheckout",
            id=id,
            metadata=metadata,
            privateMetadata=privateMetadata,
            removeCheckout=removeCheckout,
        )

    @classmethod
    def channel_create(
        cls, *, input: Optional[ChannelCreateInput] = None
    ) -> ChannelCreateFields:
        return ChannelCreateFields(field_name="channelCreate", input=input)

    @classmethod
    def channel_update(
        cls, *, id: Optional[str] = None, input: Optional[ChannelUpdateInput] = None
    ) -> ChannelUpdateFields:
        return ChannelUpdateFields(field_name="channelUpdate", id=id, input=input)

    @classmethod
    def channel_delete(
        cls, *, id: Optional[str] = None, input: Optional[ChannelDeleteInput] = None
    ) -> ChannelDeleteFields:
        return ChannelDeleteFields(field_name="channelDelete", id=id, input=input)

    @classmethod
    def channel_activate(cls, *, id: Optional[str] = None) -> ChannelActivateFields:
        return ChannelActivateFields(field_name="channelActivate", id=id)

    @classmethod
    def channel_deactivate(cls, *, id: Optional[str] = None) -> ChannelDeactivateFields:
        return ChannelDeactivateFields(field_name="channelDeactivate", id=id)

    @classmethod
    def channel_reorder_warehouses(
        cls, *, channelId: Optional[str] = None, moves: Optional[ReorderInput] = None
    ) -> ChannelReorderWarehousesFields:
        return ChannelReorderWarehousesFields(
            field_name="channelReorderWarehouses", channelId=channelId, moves=moves
        )

    @classmethod
    def attribute_create(
        cls, *, input: Optional[AttributeCreateInput] = None
    ) -> AttributeCreateFields:
        return AttributeCreateFields(field_name="attributeCreate", input=input)

    @classmethod
    def attribute_delete(
        cls, *, externalReference: Optional[str] = None, id: Optional[str] = None
    ) -> AttributeDeleteFields:
        return AttributeDeleteFields(
            field_name="attributeDelete", externalReference=externalReference, id=id
        )

    @classmethod
    def attribute_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[AttributeUpdateInput] = None
    ) -> AttributeUpdateFields:
        return AttributeUpdateFields(
            field_name="attributeUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def attribute_bulk_create(
        cls,
        *,
        attributes: Optional[AttributeCreateInput] = None,
        errorPolicy: Optional[ErrorPolicyEnum] = None
    ) -> AttributeBulkCreateFields:
        return AttributeBulkCreateFields(
            field_name="attributeBulkCreate",
            attributes=attributes,
            errorPolicy=errorPolicy,
        )

    @classmethod
    def attribute_bulk_update(
        cls,
        *,
        attributes: Optional[AttributeBulkUpdateInput] = None,
        errorPolicy: Optional[ErrorPolicyEnum] = None
    ) -> AttributeBulkUpdateFields:
        return AttributeBulkUpdateFields(
            field_name="attributeBulkUpdate",
            attributes=attributes,
            errorPolicy=errorPolicy,
        )

    @classmethod
    def attribute_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[NameTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> AttributeTranslateFields:
        return AttributeTranslateFields(
            field_name="attributeTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def attribute_bulk_translate(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        translations: Optional[AttributeBulkTranslateInput] = None
    ) -> AttributeBulkTranslateFields:
        return AttributeBulkTranslateFields(
            field_name="attributeBulkTranslate",
            errorPolicy=errorPolicy,
            translations=translations,
        )

    @classmethod
    def attribute_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> AttributeBulkDeleteFields:
        return AttributeBulkDeleteFields(field_name="attributeBulkDelete", ids=ids)

    @classmethod
    def attribute_value_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> AttributeValueBulkDeleteFields:
        return AttributeValueBulkDeleteFields(
            field_name="attributeValueBulkDelete", ids=ids
        )

    @classmethod
    def attribute_value_create(
        cls,
        *,
        attribute: Optional[str] = None,
        input: Optional[AttributeValueCreateInput] = None
    ) -> AttributeValueCreateFields:
        return AttributeValueCreateFields(
            field_name="attributeValueCreate", attribute=attribute, input=input
        )

    @classmethod
    def attribute_value_delete(
        cls, *, externalReference: Optional[str] = None, id: Optional[str] = None
    ) -> AttributeValueDeleteFields:
        return AttributeValueDeleteFields(
            field_name="attributeValueDelete",
            externalReference=externalReference,
            id=id,
        )

    @classmethod
    def attribute_value_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[AttributeValueUpdateInput] = None
    ) -> AttributeValueUpdateFields:
        return AttributeValueUpdateFields(
            field_name="attributeValueUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def attribute_value_bulk_translate(
        cls,
        *,
        errorPolicy: Optional[ErrorPolicyEnum] = None,
        translations: Optional[AttributeValueBulkTranslateInput] = None
    ) -> AttributeValueBulkTranslateFields:
        return AttributeValueBulkTranslateFields(
            field_name="attributeValueBulkTranslate",
            errorPolicy=errorPolicy,
            translations=translations,
        )

    @classmethod
    def attribute_value_translate(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[AttributeValueTranslationInput] = None,
        languageCode: Optional[LanguageCodeEnum] = None
    ) -> AttributeValueTranslateFields:
        return AttributeValueTranslateFields(
            field_name="attributeValueTranslate",
            id=id,
            input=input,
            languageCode=languageCode,
        )

    @classmethod
    def attribute_reorder_values(
        cls, *, attributeId: Optional[str] = None, moves: Optional[ReorderInput] = None
    ) -> AttributeReorderValuesFields:
        return AttributeReorderValuesFields(
            field_name="attributeReorderValues", attributeId=attributeId, moves=moves
        )

    @classmethod
    def app_create(cls, *, input: Optional[AppInput] = None) -> AppCreateFields:
        return AppCreateFields(field_name="appCreate", input=input)

    @classmethod
    def app_update(
        cls, *, id: Optional[str] = None, input: Optional[AppInput] = None
    ) -> AppUpdateFields:
        return AppUpdateFields(field_name="appUpdate", id=id, input=input)

    @classmethod
    def app_delete(cls, *, id: Optional[str] = None) -> AppDeleteFields:
        return AppDeleteFields(field_name="appDelete", id=id)

    @classmethod
    def app_token_create(
        cls, *, input: Optional[AppTokenInput] = None
    ) -> AppTokenCreateFields:
        return AppTokenCreateFields(field_name="appTokenCreate", input=input)

    @classmethod
    def app_token_delete(cls, *, id: Optional[str] = None) -> AppTokenDeleteFields:
        return AppTokenDeleteFields(field_name="appTokenDelete", id=id)

    @classmethod
    def app_token_verify(cls, *, token: Optional[str] = None) -> AppTokenVerifyFields:
        return AppTokenVerifyFields(field_name="appTokenVerify", token=token)

    @classmethod
    def app_install(
        cls, *, input: Optional[AppInstallInput] = None
    ) -> AppInstallFields:
        return AppInstallFields(field_name="appInstall", input=input)

    @classmethod
    def app_retry_install(
        cls,
        *,
        activateAfterInstallation: Optional[bool] = None,
        id: Optional[str] = None
    ) -> AppRetryInstallFields:
        return AppRetryInstallFields(
            field_name="appRetryInstall",
            activateAfterInstallation=activateAfterInstallation,
            id=id,
        )

    @classmethod
    def app_delete_failed_installation(
        cls, *, id: Optional[str] = None
    ) -> AppDeleteFailedInstallationFields:
        return AppDeleteFailedInstallationFields(
            field_name="appDeleteFailedInstallation", id=id
        )

    @classmethod
    def app_fetch_manifest(
        cls, *, manifestUrl: Optional[str] = None
    ) -> AppFetchManifestFields:
        return AppFetchManifestFields(
            field_name="appFetchManifest", manifestUrl=manifestUrl
        )

    @classmethod
    def app_activate(cls, *, id: Optional[str] = None) -> AppActivateFields:
        return AppActivateFields(field_name="appActivate", id=id)

    @classmethod
    def app_deactivate(cls, *, id: Optional[str] = None) -> AppDeactivateFields:
        return AppDeactivateFields(field_name="appDeactivate", id=id)

    @classmethod
    def token_create(
        cls,
        *,
        audience: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None
    ) -> CreateTokenFields:
        return CreateTokenFields(
            field_name="tokenCreate", audience=audience, email=email, password=password
        )

    @classmethod
    def token_refresh(
        cls, *, csrfToken: Optional[str] = None, refreshToken: Optional[str] = None
    ) -> RefreshTokenFields:
        return RefreshTokenFields(
            field_name="tokenRefresh", csrfToken=csrfToken, refreshToken=refreshToken
        )

    @classmethod
    def token_verify(cls, *, token: Optional[str] = None) -> VerifyTokenFields:
        return VerifyTokenFields(field_name="tokenVerify", token=token)

    @classmethod
    def tokens_deactivate_all(cls) -> DeactivateAllUserTokensFields:
        return DeactivateAllUserTokensFields(field_name="tokensDeactivateAll")

    @classmethod
    def external_authentication_url(
        cls, *, input: Optional[Any] = None, pluginId: Optional[str] = None
    ) -> ExternalAuthenticationUrlFields:
        return ExternalAuthenticationUrlFields(
            field_name="externalAuthenticationUrl", input=input, pluginId=pluginId
        )

    @classmethod
    def external_obtain_access_tokens(
        cls, *, input: Optional[Any] = None, pluginId: Optional[str] = None
    ) -> ExternalObtainAccessTokensFields:
        return ExternalObtainAccessTokensFields(
            field_name="externalObtainAccessTokens", input=input, pluginId=pluginId
        )

    @classmethod
    def external_refresh(
        cls, *, input: Optional[Any] = None, pluginId: Optional[str] = None
    ) -> ExternalRefreshFields:
        return ExternalRefreshFields(
            field_name="externalRefresh", input=input, pluginId=pluginId
        )

    @classmethod
    def external_logout(
        cls, *, input: Optional[Any] = None, pluginId: Optional[str] = None
    ) -> ExternalLogoutFields:
        return ExternalLogoutFields(
            field_name="externalLogout", input=input, pluginId=pluginId
        )

    @classmethod
    def external_verify(
        cls, *, input: Optional[Any] = None, pluginId: Optional[str] = None
    ) -> ExternalVerifyFields:
        return ExternalVerifyFields(
            field_name="externalVerify", input=input, pluginId=pluginId
        )

    @classmethod
    def request_password_reset(
        cls,
        *,
        channel: Optional[str] = None,
        email: Optional[str] = None,
        redirectUrl: Optional[str] = None
    ) -> RequestPasswordResetFields:
        return RequestPasswordResetFields(
            field_name="requestPasswordReset",
            channel=channel,
            email=email,
            redirectUrl=redirectUrl,
        )

    @classmethod
    def send_confirmation_email(
        cls, *, channel: Optional[str] = None, redirectUrl: Optional[str] = None
    ) -> SendConfirmationEmailFields:
        return SendConfirmationEmailFields(
            field_name="sendConfirmationEmail", channel=channel, redirectUrl=redirectUrl
        )

    @classmethod
    def confirm_account(
        cls, *, email: Optional[str] = None, token: Optional[str] = None
    ) -> ConfirmAccountFields:
        return ConfirmAccountFields(
            field_name="confirmAccount", email=email, token=token
        )

    @classmethod
    def set_password(
        cls,
        *,
        email: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None
    ) -> SetPasswordFields:
        return SetPasswordFields(
            field_name="setPassword", email=email, password=password, token=token
        )

    @classmethod
    def password_change(
        cls, *, newPassword: Optional[str] = None, oldPassword: Optional[str] = None
    ) -> PasswordChangeFields:
        return PasswordChangeFields(
            field_name="passwordChange",
            newPassword=newPassword,
            oldPassword=oldPassword,
        )

    @classmethod
    def request_email_change(
        cls,
        *,
        channel: Optional[str] = None,
        newEmail: Optional[str] = None,
        password: Optional[str] = None,
        redirectUrl: Optional[str] = None
    ) -> RequestEmailChangeFields:
        return RequestEmailChangeFields(
            field_name="requestEmailChange",
            channel=channel,
            newEmail=newEmail,
            password=password,
            redirectUrl=redirectUrl,
        )

    @classmethod
    def confirm_email_change(
        cls, *, channel: Optional[str] = None, token: Optional[str] = None
    ) -> ConfirmEmailChangeFields:
        return ConfirmEmailChangeFields(
            field_name="confirmEmailChange", channel=channel, token=token
        )

    @classmethod
    def account_address_create(
        cls,
        *,
        input: Optional[AddressInput] = None,
        type: Optional[AddressTypeEnum] = None
    ) -> AccountAddressCreateFields:
        return AccountAddressCreateFields(
            field_name="accountAddressCreate", input=input, type=type
        )

    @classmethod
    def account_address_update(
        cls, *, id: Optional[str] = None, input: Optional[AddressInput] = None
    ) -> AccountAddressUpdateFields:
        return AccountAddressUpdateFields(
            field_name="accountAddressUpdate", id=id, input=input
        )

    @classmethod
    def account_address_delete(
        cls, *, id: Optional[str] = None
    ) -> AccountAddressDeleteFields:
        return AccountAddressDeleteFields(field_name="accountAddressDelete", id=id)

    @classmethod
    def account_set_default_address(
        cls, *, id: Optional[str] = None, type: Optional[AddressTypeEnum] = None
    ) -> AccountSetDefaultAddressFields:
        return AccountSetDefaultAddressFields(
            field_name="accountSetDefaultAddress", id=id, type=type
        )

    @classmethod
    def account_register(
        cls, *, input: Optional[AccountRegisterInput] = None
    ) -> AccountRegisterFields:
        return AccountRegisterFields(field_name="accountRegister", input=input)

    @classmethod
    def account_update(
        cls, *, input: Optional[AccountInput] = None
    ) -> AccountUpdateFields:
        return AccountUpdateFields(field_name="accountUpdate", input=input)

    @classmethod
    def account_request_deletion(
        cls, *, channel: Optional[str] = None, redirectUrl: Optional[str] = None
    ) -> AccountRequestDeletionFields:
        return AccountRequestDeletionFields(
            field_name="accountRequestDeletion",
            channel=channel,
            redirectUrl=redirectUrl,
        )

    @classmethod
    def account_delete(cls, *, token: Optional[str] = None) -> AccountDeleteFields:
        return AccountDeleteFields(field_name="accountDelete", token=token)

    @classmethod
    def address_create(
        cls, *, input: Optional[AddressInput] = None, userId: Optional[str] = None
    ) -> AddressCreateFields:
        return AddressCreateFields(
            field_name="addressCreate", input=input, userId=userId
        )

    @classmethod
    def address_update(
        cls, *, id: Optional[str] = None, input: Optional[AddressInput] = None
    ) -> AddressUpdateFields:
        return AddressUpdateFields(field_name="addressUpdate", id=id, input=input)

    @classmethod
    def address_delete(cls, *, id: Optional[str] = None) -> AddressDeleteFields:
        return AddressDeleteFields(field_name="addressDelete", id=id)

    @classmethod
    def address_set_default(
        cls,
        *,
        addressId: Optional[str] = None,
        type: Optional[AddressTypeEnum] = None,
        userId: Optional[str] = None
    ) -> AddressSetDefaultFields:
        return AddressSetDefaultFields(
            field_name="addressSetDefault",
            addressId=addressId,
            type=type,
            userId=userId,
        )

    @classmethod
    def customer_create(
        cls, *, input: Optional[UserCreateInput] = None
    ) -> CustomerCreateFields:
        return CustomerCreateFields(field_name="customerCreate", input=input)

    @classmethod
    def customer_update(
        cls,
        *,
        externalReference: Optional[str] = None,
        id: Optional[str] = None,
        input: Optional[CustomerInput] = None
    ) -> CustomerUpdateFields:
        return CustomerUpdateFields(
            field_name="customerUpdate",
            externalReference=externalReference,
            id=id,
            input=input,
        )

    @classmethod
    def customer_delete(
        cls, *, externalReference: Optional[str] = None, id: Optional[str] = None
    ) -> CustomerDeleteFields:
        return CustomerDeleteFields(
            field_name="customerDelete", externalReference=externalReference, id=id
        )

    @classmethod
    def customer_bulk_delete(
        cls, *, ids: Optional[str] = None
    ) -> CustomerBulkDeleteFields:
        return CustomerBulkDeleteFields(field_name="customerBulkDelete", ids=ids)

    @classmethod
    def customer_bulk_update(
        cls,
        *,
        customers: Optional[CustomerBulkUpdateInput] = None,
        errorPolicy: Optional[ErrorPolicyEnum] = None
    ) -> CustomerBulkUpdateFields:
        return CustomerBulkUpdateFields(
            field_name="customerBulkUpdate",
            customers=customers,
            errorPolicy=errorPolicy,
        )

    @classmethod
    def staff_create(
        cls, *, input: Optional[StaffCreateInput] = None
    ) -> StaffCreateFields:
        return StaffCreateFields(field_name="staffCreate", input=input)

    @classmethod
    def staff_update(
        cls, *, id: Optional[str] = None, input: Optional[StaffUpdateInput] = None
    ) -> StaffUpdateFields:
        return StaffUpdateFields(field_name="staffUpdate", id=id, input=input)

    @classmethod
    def staff_delete(cls, *, id: Optional[str] = None) -> StaffDeleteFields:
        return StaffDeleteFields(field_name="staffDelete", id=id)

    @classmethod
    def staff_bulk_delete(cls, *, ids: Optional[str] = None) -> StaffBulkDeleteFields:
        return StaffBulkDeleteFields(field_name="staffBulkDelete", ids=ids)

    @classmethod
    def user_avatar_update(
        cls, *, image: Optional[Upload] = None
    ) -> UserAvatarUpdateFields:
        return UserAvatarUpdateFields(field_name="userAvatarUpdate", image=image)

    @classmethod
    def user_avatar_delete(cls) -> UserAvatarDeleteFields:
        return UserAvatarDeleteFields(field_name="userAvatarDelete")

    @classmethod
    def user_bulk_set_active(
        cls, *, ids: Optional[str] = None, isActive: Optional[bool] = None
    ) -> UserBulkSetActiveFields:
        return UserBulkSetActiveFields(
            field_name="userBulkSetActive", ids=ids, isActive=isActive
        )

    @classmethod
    def permission_group_create(
        cls, *, input: Optional[PermissionGroupCreateInput] = None
    ) -> PermissionGroupCreateFields:
        return PermissionGroupCreateFields(
            field_name="permissionGroupCreate", input=input
        )

    @classmethod
    def permission_group_update(
        cls,
        *,
        id: Optional[str] = None,
        input: Optional[PermissionGroupUpdateInput] = None
    ) -> PermissionGroupUpdateFields:
        return PermissionGroupUpdateFields(
            field_name="permissionGroupUpdate", id=id, input=input
        )

    @classmethod
    def permission_group_delete(
        cls, *, id: Optional[str] = None
    ) -> PermissionGroupDeleteFields:
        return PermissionGroupDeleteFields(field_name="permissionGroupDelete", id=id)

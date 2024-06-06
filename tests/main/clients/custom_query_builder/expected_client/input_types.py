from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel, Upload
from .enums import (
    AllocationStrategyEnum,
    AppExtensionMountEnum,
    AppExtensionTargetEnum,
    AppSortField,
    AppTypeEnum,
    AttributeChoicesSortField,
    AttributeEntityTypeEnum,
    AttributeInputTypeEnum,
    AttributeSortField,
    AttributeTypeEnum,
    CategorySortField,
    CheckoutAuthorizeStatusEnum,
    CheckoutChargeStatusEnum,
    CheckoutSortField,
    CollectionPublished,
    CollectionSortField,
    CountryCode,
    DiscountStatusEnum,
    DiscountValueTypeEnum,
    EventDeliveryAttemptSortField,
    EventDeliverySortField,
    EventDeliveryStatusEnum,
    ExportFileSortField,
    ExportScope,
    FileTypesEnum,
    GiftCardEventsEnum,
    GiftCardSettingsExpiryTypeEnum,
    GiftCardSortField,
    JobStatusEnum,
    LanguageCodeEnum,
    MarkAsPaidStrategyEnum,
    MeasurementUnitsEnum,
    MediaChoicesSortField,
    MenuItemsSortField,
    MenuSortField,
    OrderAuthorizeStatusEnum,
    OrderChargeStatusEnum,
    OrderDirection,
    OrderSortField,
    OrderStatus,
    OrderStatusFilter,
    PageSortField,
    PageTypeSortField,
    PaymentChargeStatusEnum,
    PermissionEnum,
    PermissionGroupSortField,
    PluginConfigurationType,
    PluginSortField,
    PostalCodeRuleInclusionTypeEnum,
    ProductAttributeType,
    ProductFieldEnum,
    ProductOrderField,
    ProductTypeConfigurable,
    ProductTypeEnum,
    ProductTypeKindEnum,
    ProductTypeSortField,
    ProductVariantSortField,
    PromotionSortField,
    PromotionTypeEnum,
    RewardTypeEnum,
    RewardValueTypeEnum,
    SaleSortField,
    ShippingMethodTypeEnum,
    StaffMemberStatus,
    StockAvailability,
    StorePaymentMethodEnum,
    TaxCalculationStrategy,
    TaxClassSortField,
    TimePeriodTypeEnum,
    TransactionActionEnum,
    TransactionFlowStrategyEnum,
    UserSortField,
    VoucherDiscountType,
    VoucherSortField,
    VoucherTypeEnum,
    WarehouseClickAndCollectOptionEnum,
    WarehouseSortField,
    WebhookEventTypeAsyncEnum,
    WebhookEventTypeEnum,
    WebhookEventTypeSyncEnum,
    WeightUnitsEnum,
)


class EventDeliveryAttemptSortingInput(BaseModel):
    direction: OrderDirection
    field: EventDeliveryAttemptSortField


class EventDeliverySortingInput(BaseModel):
    direction: OrderDirection
    field: EventDeliverySortField


class EventDeliveryFilterInput(BaseModel):
    status: Optional[EventDeliveryStatusEnum] = None
    event_type: Optional[WebhookEventTypeEnum] = Field(alias="eventType", default=None)


class AttributeChoicesSortingInput(BaseModel):
    direction: OrderDirection
    field: AttributeChoicesSortField


class AttributeValueFilterInput(BaseModel):
    search: Optional[str] = None
    ids: Optional[List[str]] = None
    slugs: Optional[List[str]] = None


class AttributeFilterInput(BaseModel):
    value_required: Optional[bool] = Field(alias="valueRequired", default=None)
    is_variant_only: Optional[bool] = Field(alias="isVariantOnly", default=None)
    visible_in_storefront: Optional[bool] = Field(
        alias="visibleInStorefront", default=None
    )
    filterable_in_storefront: Optional[bool] = Field(
        alias="filterableInStorefront", default=None
    )
    filterable_in_dashboard: Optional[bool] = Field(
        alias="filterableInDashboard", default=None
    )
    available_in_grid: Optional[bool] = Field(alias="availableInGrid", default=None)
    metadata: Optional[List["MetadataFilter"]] = None
    search: Optional[str] = None
    ids: Optional[List[str]] = None
    type: Optional[AttributeTypeEnum] = None
    in_collection: Optional[str] = Field(alias="inCollection", default=None)
    in_category: Optional[str] = Field(alias="inCategory", default=None)
    slugs: Optional[List[str]] = None
    channel: Optional[str] = None


class MetadataFilter(BaseModel):
    key: str
    value: Optional[str] = None


class AttributeWhereInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    name: Optional["StringFilterInput"] = None
    slug: Optional["StringFilterInput"] = None
    with_choices: Optional[bool] = Field(alias="withChoices", default=None)
    input_type: Optional["AttributeInputTypeEnumFilterInput"] = Field(
        alias="inputType", default=None
    )
    entity_type: Optional["AttributeEntityTypeEnumFilterInput"] = Field(
        alias="entityType", default=None
    )
    type: Optional["AttributeTypeEnumFilterInput"] = None
    unit: Optional["MeasurementUnitsEnumFilterInput"] = None
    in_collection: Optional[str] = Field(alias="inCollection", default=None)
    in_category: Optional[str] = Field(alias="inCategory", default=None)
    value_required: Optional[bool] = Field(alias="valueRequired", default=None)
    visible_in_storefront: Optional[bool] = Field(
        alias="visibleInStorefront", default=None
    )
    filterable_in_dashboard: Optional[bool] = Field(
        alias="filterableInDashboard", default=None
    )
    and_: Optional[List["AttributeWhereInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["AttributeWhereInput"]] = Field(alias="OR", default=None)


class StringFilterInput(BaseModel):
    eq: Optional[str] = None
    one_of: Optional[List[str]] = Field(alias="oneOf", default=None)


class AttributeInputTypeEnumFilterInput(BaseModel):
    eq: Optional[AttributeInputTypeEnum] = None
    one_of: Optional[List[AttributeInputTypeEnum]] = Field(alias="oneOf", default=None)


class AttributeEntityTypeEnumFilterInput(BaseModel):
    eq: Optional[AttributeEntityTypeEnum] = None
    one_of: Optional[List[AttributeEntityTypeEnum]] = Field(alias="oneOf", default=None)


class AttributeTypeEnumFilterInput(BaseModel):
    eq: Optional[AttributeTypeEnum] = None
    one_of: Optional[List[AttributeTypeEnum]] = Field(alias="oneOf", default=None)


class MeasurementUnitsEnumFilterInput(BaseModel):
    eq: Optional[MeasurementUnitsEnum] = None
    one_of: Optional[List[MeasurementUnitsEnum]] = Field(alias="oneOf", default=None)


class ProductFilterInput(BaseModel):
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    collections: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    has_category: Optional[bool] = Field(alias="hasCategory", default=None)
    attributes: Optional[List["AttributeInput"]] = None
    stock_availability: Optional[StockAvailability] = Field(
        alias="stockAvailability", default=None
    )
    stocks: Optional["ProductStockFilterInput"] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    published_from: Optional[Any] = Field(alias="publishedFrom", default=None)
    is_available: Optional[bool] = Field(alias="isAvailable", default=None)
    available_from: Optional[Any] = Field(alias="availableFrom", default=None)
    is_visible_in_listing: Optional[bool] = Field(
        alias="isVisibleInListing", default=None
    )
    price: Optional["PriceRangeInput"] = None
    minimal_price: Optional["PriceRangeInput"] = Field(
        alias="minimalPrice", default=None
    )
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)
    product_types: Optional[List[str]] = Field(alias="productTypes", default=None)
    gift_card: Optional[bool] = Field(alias="giftCard", default=None)
    ids: Optional[List[str]] = None
    has_preordered_variants: Optional[bool] = Field(
        alias="hasPreorderedVariants", default=None
    )
    slugs: Optional[List[str]] = None
    channel: Optional[str] = None


class AttributeInput(BaseModel):
    slug: str
    values: Optional[List[str]] = None
    values_range: Optional["IntRangeInput"] = Field(alias="valuesRange", default=None)
    date_time: Optional["DateTimeRangeInput"] = Field(alias="dateTime", default=None)
    date: Optional["DateRangeInput"] = None
    boolean: Optional[bool] = None


class IntRangeInput(BaseModel):
    gte: Optional[int] = None
    lte: Optional[int] = None


class DateTimeRangeInput(BaseModel):
    gte: Optional[Any] = None
    lte: Optional[Any] = None


class DateRangeInput(BaseModel):
    gte: Optional[Any] = None
    lte: Optional[Any] = None


class ProductStockFilterInput(BaseModel):
    warehouse_ids: Optional[List[str]] = Field(alias="warehouseIds", default=None)
    quantity: Optional["IntRangeInput"] = None


class PriceRangeInput(BaseModel):
    gte: Optional[float] = None
    lte: Optional[float] = None


class ProductWhereInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    name: Optional["StringFilterInput"] = None
    slug: Optional["StringFilterInput"] = None
    product_type: Optional["GlobalIDFilterInput"] = Field(
        alias="productType", default=None
    )
    category: Optional["GlobalIDFilterInput"] = None
    collection: Optional["GlobalIDFilterInput"] = None
    is_available: Optional[bool] = Field(alias="isAvailable", default=None)
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    is_visible_in_listing: Optional[bool] = Field(
        alias="isVisibleInListing", default=None
    )
    published_from: Optional[Any] = Field(alias="publishedFrom", default=None)
    available_from: Optional[Any] = Field(alias="availableFrom", default=None)
    has_category: Optional[bool] = Field(alias="hasCategory", default=None)
    price: Optional["DecimalFilterInput"] = None
    minimal_price: Optional["DecimalFilterInput"] = Field(
        alias="minimalPrice", default=None
    )
    attributes: Optional[List["AttributeInput"]] = None
    stock_availability: Optional[StockAvailability] = Field(
        alias="stockAvailability", default=None
    )
    stocks: Optional["ProductStockFilterInput"] = None
    gift_card: Optional[bool] = Field(alias="giftCard", default=None)
    has_preordered_variants: Optional[bool] = Field(
        alias="hasPreorderedVariants", default=None
    )
    updated_at: Optional["DateTimeFilterInput"] = Field(alias="updatedAt", default=None)
    and_: Optional[List["ProductWhereInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["ProductWhereInput"]] = Field(alias="OR", default=None)


class GlobalIDFilterInput(BaseModel):
    eq: Optional[str] = None
    one_of: Optional[List[str]] = Field(alias="oneOf", default=None)


class DecimalFilterInput(BaseModel):
    eq: Optional[Any] = None
    one_of: Optional[List[Any]] = Field(alias="oneOf", default=None)
    range: Optional["DecimalRangeInput"] = None


class DecimalRangeInput(BaseModel):
    gte: Optional[Any] = None
    lte: Optional[Any] = None


class DateTimeFilterInput(BaseModel):
    eq: Optional[Any] = None
    one_of: Optional[List[Any]] = Field(alias="oneOf", default=None)
    range: Optional["DateTimeRangeInput"] = None


class ProductOrder(BaseModel):
    direction: OrderDirection
    channel: Optional[str] = None
    attribute_id: Optional[str] = Field(alias="attributeId", default=None)
    field: Optional[ProductOrderField] = None


class AddressInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    company_name: Optional[str] = Field(alias="companyName", default=None)
    street_address_1: Optional[str] = Field(alias="streetAddress1", default=None)
    street_address_2: Optional[str] = Field(alias="streetAddress2", default=None)
    city: Optional[str] = None
    city_area: Optional[str] = Field(alias="cityArea", default=None)
    postal_code: Optional[str] = Field(alias="postalCode", default=None)
    country: Optional[CountryCode] = None
    country_area: Optional[str] = Field(alias="countryArea", default=None)
    phone: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None


class MetadataInput(BaseModel):
    key: str
    value: str


class MediaSortingInput(BaseModel):
    direction: OrderDirection
    field: MediaChoicesSortField


class WarehouseFilterInput(BaseModel):
    click_and_collect_option: Optional[WarehouseClickAndCollectOptionEnum] = Field(
        alias="clickAndCollectOption", default=None
    )
    metadata: Optional[List["MetadataFilter"]] = None
    search: Optional[str] = None
    ids: Optional[List[str]] = None
    is_private: Optional[bool] = Field(alias="isPrivate", default=None)
    channels: Optional[List[str]] = None
    slugs: Optional[List[str]] = None


class WarehouseSortingInput(BaseModel):
    direction: OrderDirection
    field: WarehouseSortField


class TaxConfigurationFilterInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None


class TaxClassSortingInput(BaseModel):
    direction: OrderDirection
    field: TaxClassSortField


class TaxClassFilterInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    countries: Optional[List[CountryCode]] = None


class StockFilterInput(BaseModel):
    quantity: Optional[float] = None
    search: Optional[str] = None


class CountryFilterInput(BaseModel):
    attached_to_shipping_zones: Optional[bool] = Field(
        alias="attachedToShippingZones", default=None
    )


class GiftCardEventFilterInput(BaseModel):
    type: Optional[GiftCardEventsEnum] = None
    orders: Optional[List[str]] = None


class ShippingZoneFilterInput(BaseModel):
    search: Optional[str] = None
    channels: Optional[List[str]] = None


class CategoryFilterInput(BaseModel):
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    slugs: Optional[List[str]] = None
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)


class CategoryWhereInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    and_: Optional[List["CategoryWhereInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["CategoryWhereInput"]] = Field(alias="OR", default=None)


class CategorySortingInput(BaseModel):
    direction: OrderDirection
    channel: Optional[str] = None
    field: CategorySortField


class CollectionFilterInput(BaseModel):
    published: Optional[CollectionPublished] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    slugs: Optional[List[str]] = None
    channel: Optional[str] = None


class CollectionWhereInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    and_: Optional[List["CollectionWhereInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["CollectionWhereInput"]] = Field(alias="OR", default=None)


class CollectionSortingInput(BaseModel):
    direction: OrderDirection
    channel: Optional[str] = None
    field: CollectionSortField


class ProductTypeFilterInput(BaseModel):
    search: Optional[str] = None
    configurable: Optional[ProductTypeConfigurable] = None
    product_type: Optional[ProductTypeEnum] = Field(alias="productType", default=None)
    metadata: Optional[List["MetadataFilter"]] = None
    kind: Optional[ProductTypeKindEnum] = None
    ids: Optional[List[str]] = None
    slugs: Optional[List[str]] = None


class ProductTypeSortingInput(BaseModel):
    direction: OrderDirection
    field: ProductTypeSortField


class ProductVariantFilterInput(BaseModel):
    search: Optional[str] = None
    sku: Optional[List[str]] = None
    metadata: Optional[List["MetadataFilter"]] = None
    is_preorder: Optional[bool] = Field(alias="isPreorder", default=None)
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)


class ProductVariantWhereInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    and_: Optional[List["ProductVariantWhereInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["ProductVariantWhereInput"]] = Field(alias="OR", default=None)


class ProductVariantSortingInput(BaseModel):
    direction: OrderDirection
    field: ProductVariantSortField


class PaymentFilterInput(BaseModel):
    ids: Optional[List[str]] = None
    checkouts: Optional[List[str]] = None


class PageSortingInput(BaseModel):
    direction: OrderDirection
    field: PageSortField


class PageFilterInput(BaseModel):
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    page_types: Optional[List[str]] = Field(alias="pageTypes", default=None)
    ids: Optional[List[str]] = None
    slugs: Optional[List[str]] = None


class PageTypeSortingInput(BaseModel):
    direction: OrderDirection
    field: PageTypeSortField


class PageTypeFilterInput(BaseModel):
    search: Optional[str] = None
    slugs: Optional[List[str]] = None


class OrderSortingInput(BaseModel):
    direction: OrderDirection
    field: OrderSortField


class OrderFilterInput(BaseModel):
    payment_status: Optional[List[PaymentChargeStatusEnum]] = Field(
        alias="paymentStatus", default=None
    )
    status: Optional[List[OrderStatusFilter]] = None
    customer: Optional[str] = None
    created: Optional["DateRangeInput"] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    channels: Optional[List[str]] = None
    authorize_status: Optional[List[OrderAuthorizeStatusEnum]] = Field(
        alias="authorizeStatus", default=None
    )
    charge_status: Optional[List[OrderChargeStatusEnum]] = Field(
        alias="chargeStatus", default=None
    )
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)
    is_click_and_collect: Optional[bool] = Field(
        alias="isClickAndCollect", default=None
    )
    is_preorder: Optional[bool] = Field(alias="isPreorder", default=None)
    ids: Optional[List[str]] = None
    gift_card_used: Optional[bool] = Field(alias="giftCardUsed", default=None)
    gift_card_bought: Optional[bool] = Field(alias="giftCardBought", default=None)
    numbers: Optional[List[str]] = None
    checkout_ids: Optional[List[str]] = Field(alias="checkoutIds", default=None)


class OrderDraftFilterInput(BaseModel):
    customer: Optional[str] = None
    created: Optional["DateRangeInput"] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    channels: Optional[List[str]] = None


class MenuSortingInput(BaseModel):
    direction: OrderDirection
    field: MenuSortField


class MenuFilterInput(BaseModel):
    search: Optional[str] = None
    slug: Optional[List[str]] = None
    metadata: Optional[List["MetadataFilter"]] = None
    slugs: Optional[List[str]] = None


class MenuItemSortingInput(BaseModel):
    direction: OrderDirection
    field: MenuItemsSortField


class MenuItemFilterInput(BaseModel):
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None


class GiftCardSortingInput(BaseModel):
    direction: OrderDirection
    field: GiftCardSortField


class GiftCardFilterInput(BaseModel):
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    metadata: Optional[List["MetadataFilter"]] = None
    tags: Optional[List[str]] = None
    products: Optional[List[str]] = None
    used_by: Optional[List[str]] = Field(alias="usedBy", default=None)
    used: Optional[bool] = None
    currency: Optional[str] = None
    current_balance: Optional["PriceRangeInput"] = Field(
        alias="currentBalance", default=None
    )
    initial_balance: Optional["PriceRangeInput"] = Field(
        alias="initialBalance", default=None
    )
    code: Optional[str] = None
    created_by_email: Optional[str] = Field(alias="createdByEmail", default=None)


class GiftCardTagFilterInput(BaseModel):
    search: Optional[str] = None


class PluginFilterInput(BaseModel):
    status_in_channels: Optional["PluginStatusInChannelsInput"] = Field(
        alias="statusInChannels", default=None
    )
    search: Optional[str] = None
    type: Optional[PluginConfigurationType] = None


class PluginStatusInChannelsInput(BaseModel):
    active: bool
    channels: List[str]


class PluginSortingInput(BaseModel):
    direction: OrderDirection
    field: PluginSortField


class SaleFilterInput(BaseModel):
    status: Optional[List[DiscountStatusEnum]] = None
    sale_type: Optional[DiscountValueTypeEnum] = Field(alias="saleType", default=None)
    started: Optional["DateTimeRangeInput"] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)


class SaleSortingInput(BaseModel):
    direction: OrderDirection
    channel: Optional[str] = None
    field: SaleSortField


class VoucherFilterInput(BaseModel):
    status: Optional[List[DiscountStatusEnum]] = None
    times_used: Optional["IntRangeInput"] = Field(alias="timesUsed", default=None)
    discount_type: Optional[List[VoucherDiscountType]] = Field(
        alias="discountType", default=None
    )
    started: Optional["DateTimeRangeInput"] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None


class VoucherSortingInput(BaseModel):
    direction: OrderDirection
    channel: Optional[str] = None
    field: VoucherSortField


class PromotionWhereInput(BaseModel):
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    name: Optional["StringFilterInput"] = None
    end_date: Optional["DateTimeFilterInput"] = Field(alias="endDate", default=None)
    start_date: Optional["DateTimeFilterInput"] = Field(alias="startDate", default=None)
    is_old_sale: Optional[bool] = Field(alias="isOldSale", default=None)
    type: Optional["PromotionTypeEnumFilterInput"] = None
    and_: Optional[List["PromotionWhereInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["PromotionWhereInput"]] = Field(alias="OR", default=None)


class PromotionTypeEnumFilterInput(BaseModel):
    eq: Optional[PromotionTypeEnum] = None
    one_of: Optional[List[PromotionTypeEnum]] = Field(alias="oneOf", default=None)


class PromotionSortingInput(BaseModel):
    direction: OrderDirection
    field: PromotionSortField


class ExportFileFilterInput(BaseModel):
    created_at: Optional["DateTimeRangeInput"] = Field(alias="createdAt", default=None)
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)
    status: Optional[JobStatusEnum] = None
    user: Optional[str] = None
    app: Optional[str] = None


class ExportFileSortingInput(BaseModel):
    direction: OrderDirection
    field: ExportFileSortField


class CheckoutSortingInput(BaseModel):
    direction: OrderDirection
    field: CheckoutSortField


class CheckoutFilterInput(BaseModel):
    customer: Optional[str] = None
    created: Optional["DateRangeInput"] = None
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    channels: Optional[List[str]] = None
    updated_at: Optional["DateRangeInput"] = Field(alias="updatedAt", default=None)
    authorize_status: Optional[List[CheckoutAuthorizeStatusEnum]] = Field(
        alias="authorizeStatus", default=None
    )
    charge_status: Optional[List[CheckoutChargeStatusEnum]] = Field(
        alias="chargeStatus", default=None
    )


class AttributeSortingInput(BaseModel):
    direction: OrderDirection
    field: AttributeSortField


class AppFilterInput(BaseModel):
    search: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    type: Optional[AppTypeEnum] = None


class AppSortingInput(BaseModel):
    direction: OrderDirection
    field: AppSortField


class AppExtensionFilterInput(BaseModel):
    mount: Optional[List[AppExtensionMountEnum]] = None
    target: Optional[AppExtensionTargetEnum] = None


class CustomerFilterInput(BaseModel):
    date_joined: Optional["DateRangeInput"] = Field(alias="dateJoined", default=None)
    number_of_orders: Optional["IntRangeInput"] = Field(
        alias="numberOfOrders", default=None
    )
    placed_orders: Optional["DateRangeInput"] = Field(
        alias="placedOrders", default=None
    )
    search: Optional[str] = None
    metadata: Optional[List["MetadataFilter"]] = None
    ids: Optional[List[str]] = None
    updated_at: Optional["DateTimeRangeInput"] = Field(alias="updatedAt", default=None)


class UserSortingInput(BaseModel):
    direction: OrderDirection
    field: UserSortField


class PermissionGroupFilterInput(BaseModel):
    search: Optional[str] = None
    ids: Optional[List[str]] = None


class PermissionGroupSortingInput(BaseModel):
    direction: OrderDirection
    field: PermissionGroupSortField


class StaffUserInput(BaseModel):
    status: Optional[StaffMemberStatus] = None
    search: Optional[str] = None
    ids: Optional[List[str]] = None


class WebhookCreateInput(BaseModel):
    name: Optional[str] = None
    target_url: Optional[str] = Field(alias="targetUrl", default=None)
    events: Optional[List[WebhookEventTypeEnum]] = None
    async_events: Optional[List[WebhookEventTypeAsyncEnum]] = Field(
        alias="asyncEvents", default=None
    )
    sync_events: Optional[List[WebhookEventTypeSyncEnum]] = Field(
        alias="syncEvents", default=None
    )
    app: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    secret_key: Optional[str] = Field(alias="secretKey", default=None)
    query: Optional[str] = None
    custom_headers: Optional[Any] = Field(alias="customHeaders", default=None)


class WebhookUpdateInput(BaseModel):
    name: Optional[str] = None
    target_url: Optional[str] = Field(alias="targetUrl", default=None)
    events: Optional[List[WebhookEventTypeEnum]] = None
    async_events: Optional[List[WebhookEventTypeAsyncEnum]] = Field(
        alias="asyncEvents", default=None
    )
    sync_events: Optional[List[WebhookEventTypeSyncEnum]] = Field(
        alias="syncEvents", default=None
    )
    app: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    secret_key: Optional[str] = Field(alias="secretKey", default=None)
    query: Optional[str] = None
    custom_headers: Optional[Any] = Field(alias="customHeaders", default=None)


class WarehouseCreateInput(BaseModel):
    slug: Optional[str] = None
    email: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    name: str
    address: "AddressInput"
    shipping_zones: Optional[List[str]] = Field(alias="shippingZones", default=None)


class WarehouseUpdateInput(BaseModel):
    slug: Optional[str] = None
    email: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    name: Optional[str] = None
    address: Optional["AddressInput"] = None
    click_and_collect_option: Optional[WarehouseClickAndCollectOptionEnum] = Field(
        alias="clickAndCollectOption", default=None
    )
    is_private: Optional[bool] = Field(alias="isPrivate", default=None)


class TaxClassCreateInput(BaseModel):
    name: str
    create_country_rates: Optional[List["CountryRateInput"]] = Field(
        alias="createCountryRates", default=None
    )


class CountryRateInput(BaseModel):
    country_code: CountryCode = Field(alias="countryCode")
    rate: float


class TaxClassUpdateInput(BaseModel):
    name: Optional[str] = None
    update_country_rates: Optional[List["CountryRateUpdateInput"]] = Field(
        alias="updateCountryRates", default=None
    )
    remove_country_rates: Optional[List[CountryCode]] = Field(
        alias="removeCountryRates", default=None
    )


class CountryRateUpdateInput(BaseModel):
    country_code: CountryCode = Field(alias="countryCode")
    rate: Optional[float] = None


class TaxConfigurationUpdateInput(BaseModel):
    charge_taxes: Optional[bool] = Field(alias="chargeTaxes", default=None)
    tax_calculation_strategy: Optional[TaxCalculationStrategy] = Field(
        alias="taxCalculationStrategy", default=None
    )
    display_gross_prices: Optional[bool] = Field(
        alias="displayGrossPrices", default=None
    )
    prices_entered_with_tax: Optional[bool] = Field(
        alias="pricesEnteredWithTax", default=None
    )
    update_countries_configuration: Optional[
        List["TaxConfigurationPerCountryInput"]
    ] = Field(alias="updateCountriesConfiguration", default=None)
    remove_countries_configuration: Optional[List[CountryCode]] = Field(
        alias="removeCountriesConfiguration", default=None
    )
    tax_app_id: Optional[str] = Field(alias="taxAppId", default=None)


class TaxConfigurationPerCountryInput(BaseModel):
    country_code: CountryCode = Field(alias="countryCode")
    charge_taxes: bool = Field(alias="chargeTaxes")
    tax_calculation_strategy: Optional[TaxCalculationStrategy] = Field(
        alias="taxCalculationStrategy", default=None
    )
    display_gross_prices: bool = Field(alias="displayGrossPrices")
    tax_app_id: Optional[str] = Field(alias="taxAppId", default=None)


class TaxClassRateInput(BaseModel):
    tax_class_id: Optional[str] = Field(alias="taxClassId", default=None)
    rate: Optional[float] = None


class StockBulkUpdateInput(BaseModel):
    variant_id: Optional[str] = Field(alias="variantId", default=None)
    variant_external_reference: Optional[str] = Field(
        alias="variantExternalReference", default=None
    )
    warehouse_id: Optional[str] = Field(alias="warehouseId", default=None)
    warehouse_external_reference: Optional[str] = Field(
        alias="warehouseExternalReference", default=None
    )
    quantity: int


class StaffNotificationRecipientInput(BaseModel):
    user: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None


class SiteDomainInput(BaseModel):
    domain: Optional[str] = None
    name: Optional[str] = None


class ShopSettingsInput(BaseModel):
    header_text: Optional[str] = Field(alias="headerText", default=None)
    description: Optional[str] = None
    track_inventory_by_default: Optional[bool] = Field(
        alias="trackInventoryByDefault", default=None
    )
    default_weight_unit: Optional[WeightUnitsEnum] = Field(
        alias="defaultWeightUnit", default=None
    )
    automatic_fulfillment_digital_products: Optional[bool] = Field(
        alias="automaticFulfillmentDigitalProducts", default=None
    )
    fulfillment_auto_approve: Optional[bool] = Field(
        alias="fulfillmentAutoApprove", default=None
    )
    fulfillment_allow_unpaid: Optional[bool] = Field(
        alias="fulfillmentAllowUnpaid", default=None
    )
    default_digital_max_downloads: Optional[int] = Field(
        alias="defaultDigitalMaxDownloads", default=None
    )
    default_digital_url_valid_days: Optional[int] = Field(
        alias="defaultDigitalUrlValidDays", default=None
    )
    default_mail_sender_name: Optional[str] = Field(
        alias="defaultMailSenderName", default=None
    )
    default_mail_sender_address: Optional[str] = Field(
        alias="defaultMailSenderAddress", default=None
    )
    customer_set_password_url: Optional[str] = Field(
        alias="customerSetPasswordUrl", default=None
    )
    reserve_stock_duration_anonymous_user: Optional[int] = Field(
        alias="reserveStockDurationAnonymousUser", default=None
    )
    reserve_stock_duration_authenticated_user: Optional[int] = Field(
        alias="reserveStockDurationAuthenticatedUser", default=None
    )
    limit_quantity_per_checkout: Optional[int] = Field(
        alias="limitQuantityPerCheckout", default=None
    )
    enable_account_confirmation_by_email: Optional[bool] = Field(
        alias="enableAccountConfirmationByEmail", default=None
    )
    allow_login_without_confirmation: Optional[bool] = Field(
        alias="allowLoginWithoutConfirmation", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    include_taxes_in_prices: Optional[bool] = Field(
        alias="includeTaxesInPrices", default=None
    )
    display_gross_prices: Optional[bool] = Field(
        alias="displayGrossPrices", default=None
    )
    charge_taxes_on_shipping: Optional[bool] = Field(
        alias="chargeTaxesOnShipping", default=None
    )


class ShopSettingsTranslationInput(BaseModel):
    header_text: Optional[str] = Field(alias="headerText", default=None)
    description: Optional[str] = None


class OrderSettingsUpdateInput(BaseModel):
    automatically_confirm_all_new_orders: Optional[bool] = Field(
        alias="automaticallyConfirmAllNewOrders", default=None
    )
    automatically_fulfill_non_shippable_gift_card: Optional[bool] = Field(
        alias="automaticallyFulfillNonShippableGiftCard", default=None
    )


class GiftCardSettingsUpdateInput(BaseModel):
    expiry_type: Optional[GiftCardSettingsExpiryTypeEnum] = Field(
        alias="expiryType", default=None
    )
    expiry_period: Optional["TimePeriodInputType"] = Field(
        alias="expiryPeriod", default=None
    )


class TimePeriodInputType(BaseModel):
    amount: int
    type: TimePeriodTypeEnum


class ShippingMethodChannelListingInput(BaseModel):
    add_channels: Optional[List["ShippingMethodChannelListingAddInput"]] = Field(
        alias="addChannels", default=None
    )
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)


class ShippingMethodChannelListingAddInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    price: Optional[Any] = None
    minimum_order_price: Optional[Any] = Field(alias="minimumOrderPrice", default=None)
    maximum_order_price: Optional[Any] = Field(alias="maximumOrderPrice", default=None)


class ShippingPriceInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None
    minimum_order_weight: Optional[Any] = Field(
        alias="minimumOrderWeight", default=None
    )
    maximum_order_weight: Optional[Any] = Field(
        alias="maximumOrderWeight", default=None
    )
    maximum_delivery_days: Optional[int] = Field(
        alias="maximumDeliveryDays", default=None
    )
    minimum_delivery_days: Optional[int] = Field(
        alias="minimumDeliveryDays", default=None
    )
    type: Optional[ShippingMethodTypeEnum] = None
    shipping_zone: Optional[str] = Field(alias="shippingZone", default=None)
    add_postal_code_rules: Optional[List["ShippingPostalCodeRulesCreateInputRange"]] = (
        Field(alias="addPostalCodeRules", default=None)
    )
    delete_postal_code_rules: Optional[List[str]] = Field(
        alias="deletePostalCodeRules", default=None
    )
    inclusion_type: Optional[PostalCodeRuleInclusionTypeEnum] = Field(
        alias="inclusionType", default=None
    )
    tax_class: Optional[str] = Field(alias="taxClass", default=None)


class ShippingPostalCodeRulesCreateInputRange(BaseModel):
    start: str
    end: Optional[str] = None


class ShippingPriceTranslationInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None


class ShippingPriceExcludeProductsInput(BaseModel):
    products: List[str]


class ShippingZoneCreateInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    countries: Optional[List[str]] = None
    default: Optional[bool] = None
    add_warehouses: Optional[List[str]] = Field(alias="addWarehouses", default=None)
    add_channels: Optional[List[str]] = Field(alias="addChannels", default=None)


class ShippingZoneUpdateInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    countries: Optional[List[str]] = None
    default: Optional[bool] = None
    add_warehouses: Optional[List[str]] = Field(alias="addWarehouses", default=None)
    add_channels: Optional[List[str]] = Field(alias="addChannels", default=None)
    remove_warehouses: Optional[List[str]] = Field(
        alias="removeWarehouses", default=None
    )
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)


class ProductAttributeAssignInput(BaseModel):
    id: str
    type: ProductAttributeType
    variant_selection: Optional[bool] = Field(alias="variantSelection", default=None)


class ProductAttributeAssignmentUpdateInput(BaseModel):
    id: str
    variant_selection: bool = Field(alias="variantSelection")


class CategoryInput(BaseModel):
    description: Optional[Any] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    seo: Optional["SeoInput"] = None
    background_image: Optional[Upload] = Field(alias="backgroundImage", default=None)
    background_image_alt: Optional[str] = Field(
        alias="backgroundImageAlt", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )


class SeoInput(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TranslationInput(BaseModel):
    seo_title: Optional[str] = Field(alias="seoTitle", default=None)
    seo_description: Optional[str] = Field(alias="seoDescription", default=None)
    name: Optional[str] = None
    description: Optional[Any] = None


class CollectionCreateInput(BaseModel):
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[Any] = None
    background_image: Optional[Upload] = Field(alias="backgroundImage", default=None)
    background_image_alt: Optional[str] = Field(
        alias="backgroundImageAlt", default=None
    )
    seo: Optional["SeoInput"] = None
    publication_date: Optional[Any] = Field(alias="publicationDate", default=None)
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    products: Optional[List[str]] = None


class MoveProductInput(BaseModel):
    product_id: str = Field(alias="productId")
    sort_order: Optional[int] = Field(alias="sortOrder", default=None)


class CollectionInput(BaseModel):
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[Any] = None
    background_image: Optional[Upload] = Field(alias="backgroundImage", default=None)
    background_image_alt: Optional[str] = Field(
        alias="backgroundImageAlt", default=None
    )
    seo: Optional["SeoInput"] = None
    publication_date: Optional[Any] = Field(alias="publicationDate", default=None)
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )


class CollectionChannelListingUpdateInput(BaseModel):
    add_channels: Optional[List["PublishableChannelListingInput"]] = Field(
        alias="addChannels", default=None
    )
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)


class PublishableChannelListingInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    publication_date: Optional[Any] = Field(alias="publicationDate", default=None)
    published_at: Optional[Any] = Field(alias="publishedAt", default=None)


class ProductCreateInput(BaseModel):
    attributes: Optional[List["AttributeValueInput"]] = None
    category: Optional[str] = None
    charge_taxes: Optional[bool] = Field(alias="chargeTaxes", default=None)
    collections: Optional[List[str]] = None
    description: Optional[Any] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    tax_class: Optional[str] = Field(alias="taxClass", default=None)
    tax_code: Optional[str] = Field(alias="taxCode", default=None)
    seo: Optional["SeoInput"] = None
    weight: Optional[Any] = None
    rating: Optional[float] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    product_type: str = Field(alias="productType")


class AttributeValueInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    values: Optional[List[str]] = None
    dropdown: Optional["AttributeValueSelectableTypeInput"] = None
    swatch: Optional["AttributeValueSelectableTypeInput"] = None
    multiselect: Optional[List["AttributeValueSelectableTypeInput"]] = None
    numeric: Optional[str] = None
    file: Optional[str] = None
    content_type: Optional[str] = Field(alias="contentType", default=None)
    references: Optional[List[str]] = None
    rich_text: Optional[Any] = Field(alias="richText", default=None)
    plain_text: Optional[str] = Field(alias="plainText", default=None)
    boolean: Optional[bool] = None
    date: Optional[Any] = None
    date_time: Optional[Any] = Field(alias="dateTime", default=None)


class AttributeValueSelectableTypeInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    value: Optional[str] = None


class ProductBulkCreateInput(BaseModel):
    attributes: Optional[List["AttributeValueInput"]] = None
    category: Optional[str] = None
    charge_taxes: Optional[bool] = Field(alias="chargeTaxes", default=None)
    collections: Optional[List[str]] = None
    description: Optional[Any] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    tax_class: Optional[str] = Field(alias="taxClass", default=None)
    tax_code: Optional[str] = Field(alias="taxCode", default=None)
    seo: Optional["SeoInput"] = None
    weight: Optional[Any] = None
    rating: Optional[float] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    product_type: str = Field(alias="productType")
    media: Optional[List["MediaInput"]] = None
    channel_listings: Optional[List["ProductChannelListingCreateInput"]] = Field(
        alias="channelListings", default=None
    )
    variants: Optional[List["ProductVariantBulkCreateInput"]] = None


class MediaInput(BaseModel):
    alt: Optional[str] = None
    image: Optional[Upload] = None
    media_url: Optional[str] = Field(alias="mediaUrl", default=None)


class ProductChannelListingCreateInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    published_at: Optional[Any] = Field(alias="publishedAt", default=None)
    visible_in_listings: Optional[bool] = Field(alias="visibleInListings", default=None)
    is_available_for_purchase: Optional[bool] = Field(
        alias="isAvailableForPurchase", default=None
    )
    available_for_purchase_at: Optional[Any] = Field(
        alias="availableForPurchaseAt", default=None
    )


class ProductVariantBulkCreateInput(BaseModel):
    attributes: List["BulkAttributeValueInput"]
    sku: Optional[str] = None
    name: Optional[str] = None
    track_inventory: Optional[bool] = Field(alias="trackInventory", default=None)
    weight: Optional[Any] = None
    preorder: Optional["PreorderSettingsInput"] = None
    quantity_limit_per_customer: Optional[int] = Field(
        alias="quantityLimitPerCustomer", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    stocks: Optional[List["StockInput"]] = None
    channel_listings: Optional[List["ProductVariantChannelListingAddInput"]] = Field(
        alias="channelListings", default=None
    )


class BulkAttributeValueInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    values: Optional[List[str]] = None
    dropdown: Optional["AttributeValueSelectableTypeInput"] = None
    swatch: Optional["AttributeValueSelectableTypeInput"] = None
    multiselect: Optional[List["AttributeValueSelectableTypeInput"]] = None
    numeric: Optional[str] = None
    file: Optional[str] = None
    content_type: Optional[str] = Field(alias="contentType", default=None)
    references: Optional[List[str]] = None
    rich_text: Optional[Any] = Field(alias="richText", default=None)
    plain_text: Optional[str] = Field(alias="plainText", default=None)
    boolean: Optional[bool] = None
    date: Optional[Any] = None
    date_time: Optional[Any] = Field(alias="dateTime", default=None)


class PreorderSettingsInput(BaseModel):
    global_threshold: Optional[int] = Field(alias="globalThreshold", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)


class StockInput(BaseModel):
    warehouse: str
    quantity: int


class ProductVariantChannelListingAddInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    price: Any
    cost_price: Optional[Any] = Field(alias="costPrice", default=None)
    preorder_threshold: Optional[int] = Field(alias="preorderThreshold", default=None)


class ProductInput(BaseModel):
    attributes: Optional[List["AttributeValueInput"]] = None
    category: Optional[str] = None
    charge_taxes: Optional[bool] = Field(alias="chargeTaxes", default=None)
    collections: Optional[List[str]] = None
    description: Optional[Any] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    tax_class: Optional[str] = Field(alias="taxClass", default=None)
    tax_code: Optional[str] = Field(alias="taxCode", default=None)
    seo: Optional["SeoInput"] = None
    weight: Optional[Any] = None
    rating: Optional[float] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class ProductBulkTranslateInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    translation_fields: "TranslationInput" = Field(alias="translationFields")


class ProductChannelListingUpdateInput(BaseModel):
    update_channels: Optional[List["ProductChannelListingAddInput"]] = Field(
        alias="updateChannels", default=None
    )
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)


class ProductChannelListingAddInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    publication_date: Optional[Any] = Field(alias="publicationDate", default=None)
    published_at: Optional[Any] = Field(alias="publishedAt", default=None)
    visible_in_listings: Optional[bool] = Field(alias="visibleInListings", default=None)
    is_available_for_purchase: Optional[bool] = Field(
        alias="isAvailableForPurchase", default=None
    )
    available_for_purchase_date: Optional[Any] = Field(
        alias="availableForPurchaseDate", default=None
    )
    available_for_purchase_at: Optional[Any] = Field(
        alias="availableForPurchaseAt", default=None
    )
    add_variants: Optional[List[str]] = Field(alias="addVariants", default=None)
    remove_variants: Optional[List[str]] = Field(alias="removeVariants", default=None)


class ProductMediaCreateInput(BaseModel):
    alt: Optional[str] = None
    image: Optional[Upload] = None
    product: str
    media_url: Optional[str] = Field(alias="mediaUrl", default=None)


class ReorderInput(BaseModel):
    id: str
    sort_order: Optional[int] = Field(alias="sortOrder", default=None)


class ProductMediaUpdateInput(BaseModel):
    alt: Optional[str] = None


class ProductTypeInput(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    kind: Optional[ProductTypeKindEnum] = None
    has_variants: Optional[bool] = Field(alias="hasVariants", default=None)
    product_attributes: Optional[List[str]] = Field(
        alias="productAttributes", default=None
    )
    variant_attributes: Optional[List[str]] = Field(
        alias="variantAttributes", default=None
    )
    is_shipping_required: Optional[bool] = Field(
        alias="isShippingRequired", default=None
    )
    is_digital: Optional[bool] = Field(alias="isDigital", default=None)
    weight: Optional[Any] = None
    tax_code: Optional[str] = Field(alias="taxCode", default=None)
    tax_class: Optional[str] = Field(alias="taxClass", default=None)


class DigitalContentUploadInput(BaseModel):
    use_default_settings: bool = Field(alias="useDefaultSettings")
    max_downloads: Optional[int] = Field(alias="maxDownloads", default=None)
    url_valid_days: Optional[int] = Field(alias="urlValidDays", default=None)
    automatic_fulfillment: Optional[bool] = Field(
        alias="automaticFulfillment", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    content_file: Upload = Field(alias="contentFile")


class DigitalContentInput(BaseModel):
    use_default_settings: bool = Field(alias="useDefaultSettings")
    max_downloads: Optional[int] = Field(alias="maxDownloads", default=None)
    url_valid_days: Optional[int] = Field(alias="urlValidDays", default=None)
    automatic_fulfillment: Optional[bool] = Field(
        alias="automaticFulfillment", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )


class DigitalContentUrlCreateInput(BaseModel):
    content: str


class ProductVariantCreateInput(BaseModel):
    attributes: List["AttributeValueInput"]
    sku: Optional[str] = None
    name: Optional[str] = None
    track_inventory: Optional[bool] = Field(alias="trackInventory", default=None)
    weight: Optional[Any] = None
    preorder: Optional["PreorderSettingsInput"] = None
    quantity_limit_per_customer: Optional[int] = Field(
        alias="quantityLimitPerCustomer", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    product: str
    stocks: Optional[List["StockInput"]] = None


class ProductVariantBulkUpdateInput(BaseModel):
    attributes: Optional[List["BulkAttributeValueInput"]] = None
    sku: Optional[str] = None
    name: Optional[str] = None
    track_inventory: Optional[bool] = Field(alias="trackInventory", default=None)
    weight: Optional[Any] = None
    preorder: Optional["PreorderSettingsInput"] = None
    quantity_limit_per_customer: Optional[int] = Field(
        alias="quantityLimitPerCustomer", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    stocks: Optional["ProductVariantStocksUpdateInput"] = None
    channel_listings: Optional["ProductVariantChannelListingUpdateInput"] = Field(
        alias="channelListings", default=None
    )
    id: str


class ProductVariantStocksUpdateInput(BaseModel):
    create: Optional[List["StockInput"]] = None
    update: Optional[List["StockUpdateInput"]] = None
    remove: Optional[List[str]] = None


class StockUpdateInput(BaseModel):
    stock: str
    quantity: int


class ProductVariantChannelListingUpdateInput(BaseModel):
    create: Optional[List["ProductVariantChannelListingAddInput"]] = None
    update: Optional[List["ChannelListingUpdateInput"]] = None
    remove: Optional[List[str]] = None


class ChannelListingUpdateInput(BaseModel):
    channel_listing: str = Field(alias="channelListing")
    price: Optional[Any] = None
    cost_price: Optional[Any] = Field(alias="costPrice", default=None)
    preorder_threshold: Optional[int] = Field(alias="preorderThreshold", default=None)


class ProductVariantInput(BaseModel):
    attributes: Optional[List["AttributeValueInput"]] = None
    sku: Optional[str] = None
    name: Optional[str] = None
    track_inventory: Optional[bool] = Field(alias="trackInventory", default=None)
    weight: Optional[Any] = None
    preorder: Optional["PreorderSettingsInput"] = None
    quantity_limit_per_customer: Optional[int] = Field(
        alias="quantityLimitPerCustomer", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class NameTranslationInput(BaseModel):
    name: Optional[str] = None


class ProductVariantBulkTranslateInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    translation_fields: "NameTranslationInput" = Field(alias="translationFields")


class PaymentCheckBalanceInput(BaseModel):
    gateway_id: str = Field(alias="gatewayId")
    method: str
    channel: str
    card: "CardInput"


class CardInput(BaseModel):
    code: str
    cvc: Optional[str] = None
    money: "MoneyInput"


class MoneyInput(BaseModel):
    currency: str
    amount: Any


class TransactionCreateInput(BaseModel):
    name: Optional[str] = None
    message: Optional[str] = None
    psp_reference: Optional[str] = Field(alias="pspReference", default=None)
    available_actions: Optional[List[TransactionActionEnum]] = Field(
        alias="availableActions", default=None
    )
    amount_authorized: Optional["MoneyInput"] = Field(
        alias="amountAuthorized", default=None
    )
    amount_charged: Optional["MoneyInput"] = Field(alias="amountCharged", default=None)
    amount_refunded: Optional["MoneyInput"] = Field(
        alias="amountRefunded", default=None
    )
    amount_canceled: Optional["MoneyInput"] = Field(
        alias="amountCanceled", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_url: Optional[str] = Field(alias="externalUrl", default=None)


class TransactionEventInput(BaseModel):
    psp_reference: Optional[str] = Field(alias="pspReference", default=None)
    message: Optional[str] = None


class TransactionUpdateInput(BaseModel):
    name: Optional[str] = None
    message: Optional[str] = None
    psp_reference: Optional[str] = Field(alias="pspReference", default=None)
    available_actions: Optional[List[TransactionActionEnum]] = Field(
        alias="availableActions", default=None
    )
    amount_authorized: Optional["MoneyInput"] = Field(
        alias="amountAuthorized", default=None
    )
    amount_charged: Optional["MoneyInput"] = Field(alias="amountCharged", default=None)
    amount_refunded: Optional["MoneyInput"] = Field(
        alias="amountRefunded", default=None
    )
    amount_canceled: Optional["MoneyInput"] = Field(
        alias="amountCanceled", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    external_url: Optional[str] = Field(alias="externalUrl", default=None)


class PaymentGatewayToInitialize(BaseModel):
    id: str
    data: Optional[Any] = None


class PageCreateInput(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    content: Optional[Any] = None
    attributes: Optional[List["AttributeValueInput"]] = None
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    publication_date: Optional[str] = Field(alias="publicationDate", default=None)
    published_at: Optional[Any] = Field(alias="publishedAt", default=None)
    seo: Optional["SeoInput"] = None
    page_type: str = Field(alias="pageType")


class PageInput(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    content: Optional[Any] = None
    attributes: Optional[List["AttributeValueInput"]] = None
    is_published: Optional[bool] = Field(alias="isPublished", default=None)
    publication_date: Optional[str] = Field(alias="publicationDate", default=None)
    published_at: Optional[Any] = Field(alias="publishedAt", default=None)
    seo: Optional["SeoInput"] = None


class PageTranslationInput(BaseModel):
    seo_title: Optional[str] = Field(alias="seoTitle", default=None)
    seo_description: Optional[str] = Field(alias="seoDescription", default=None)
    title: Optional[str] = None
    content: Optional[Any] = None


class PageTypeCreateInput(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    add_attributes: Optional[List[str]] = Field(alias="addAttributes", default=None)


class PageTypeUpdateInput(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    add_attributes: Optional[List[str]] = Field(alias="addAttributes", default=None)
    remove_attributes: Optional[List[str]] = Field(
        alias="removeAttributes", default=None
    )


class DraftOrderCreateInput(BaseModel):
    billing_address: Optional["AddressInput"] = Field(
        alias="billingAddress", default=None
    )
    user: Optional[str] = None
    user_email: Optional[str] = Field(alias="userEmail", default=None)
    discount: Optional[Any] = None
    shipping_address: Optional["AddressInput"] = Field(
        alias="shippingAddress", default=None
    )
    shipping_method: Optional[str] = Field(alias="shippingMethod", default=None)
    voucher: Optional[str] = None
    voucher_code: Optional[str] = Field(alias="voucherCode", default=None)
    customer_note: Optional[str] = Field(alias="customerNote", default=None)
    channel_id: Optional[str] = Field(alias="channelId", default=None)
    redirect_url: Optional[str] = Field(alias="redirectUrl", default=None)
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    lines: Optional[List["OrderLineCreateInput"]] = None


class OrderLineCreateInput(BaseModel):
    quantity: int
    variant_id: str = Field(alias="variantId")
    force_new_line: Optional[bool] = Field(alias="forceNewLine", default=False)
    price: Optional[Any] = None


class DraftOrderInput(BaseModel):
    billing_address: Optional["AddressInput"] = Field(
        alias="billingAddress", default=None
    )
    user: Optional[str] = None
    user_email: Optional[str] = Field(alias="userEmail", default=None)
    discount: Optional[Any] = None
    shipping_address: Optional["AddressInput"] = Field(
        alias="shippingAddress", default=None
    )
    shipping_method: Optional[str] = Field(alias="shippingMethod", default=None)
    voucher: Optional[str] = None
    voucher_code: Optional[str] = Field(alias="voucherCode", default=None)
    customer_note: Optional[str] = Field(alias="customerNote", default=None)
    channel_id: Optional[str] = Field(alias="channelId", default=None)
    redirect_url: Optional[str] = Field(alias="redirectUrl", default=None)
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class OrderAddNoteInput(BaseModel):
    message: str


class OrderFulfillInput(BaseModel):
    lines: List["OrderFulfillLineInput"]
    notify_customer: Optional[bool] = Field(alias="notifyCustomer", default=None)
    allow_stock_to_be_exceeded: Optional[bool] = Field(
        alias="allowStockToBeExceeded", default=False
    )
    tracking_number: Optional[str] = Field(alias="trackingNumber", default=None)


class OrderFulfillLineInput(BaseModel):
    order_line_id: Optional[str] = Field(alias="orderLineId", default=None)
    stocks: List["OrderFulfillStockInput"]


class OrderFulfillStockInput(BaseModel):
    quantity: int
    warehouse: str


class FulfillmentCancelInput(BaseModel):
    warehouse_id: Optional[str] = Field(alias="warehouseId", default=None)


class FulfillmentUpdateTrackingInput(BaseModel):
    tracking_number: Optional[str] = Field(alias="trackingNumber", default=None)
    notify_customer: Optional[bool] = Field(alias="notifyCustomer", default=False)


class OrderRefundProductsInput(BaseModel):
    order_lines: Optional[List["OrderRefundLineInput"]] = Field(
        alias="orderLines", default=None
    )
    fulfillment_lines: Optional[List["OrderRefundFulfillmentLineInput"]] = Field(
        alias="fulfillmentLines", default=None
    )
    amount_to_refund: Optional[Any] = Field(alias="amountToRefund", default=None)
    include_shipping_costs: Optional[bool] = Field(
        alias="includeShippingCosts", default=False
    )


class OrderRefundLineInput(BaseModel):
    order_line_id: str = Field(alias="orderLineId")
    quantity: int


class OrderRefundFulfillmentLineInput(BaseModel):
    fulfillment_line_id: str = Field(alias="fulfillmentLineId")
    quantity: int


class OrderReturnProductsInput(BaseModel):
    order_lines: Optional[List["OrderReturnLineInput"]] = Field(
        alias="orderLines", default=None
    )
    fulfillment_lines: Optional[List["OrderReturnFulfillmentLineInput"]] = Field(
        alias="fulfillmentLines", default=None
    )
    amount_to_refund: Optional[Any] = Field(alias="amountToRefund", default=None)
    include_shipping_costs: Optional[bool] = Field(
        alias="includeShippingCosts", default=False
    )
    refund: Optional[bool] = False


class OrderReturnLineInput(BaseModel):
    order_line_id: str = Field(alias="orderLineId")
    quantity: int
    replace: Optional[bool] = False


class OrderReturnFulfillmentLineInput(BaseModel):
    fulfillment_line_id: str = Field(alias="fulfillmentLineId")
    quantity: int
    replace: Optional[bool] = False


class OrderGrantRefundCreateInput(BaseModel):
    amount: Optional[Any] = None
    reason: Optional[str] = None
    lines: Optional[List["OrderGrantRefundCreateLineInput"]] = None
    grant_refund_for_shipping: Optional[bool] = Field(
        alias="grantRefundForShipping", default=None
    )
    transaction_id: Optional[str] = Field(alias="transactionId", default=None)


class OrderGrantRefundCreateLineInput(BaseModel):
    id: str
    quantity: int
    reason: Optional[str] = None


class OrderGrantRefundUpdateInput(BaseModel):
    amount: Optional[Any] = None
    reason: Optional[str] = None
    add_lines: Optional[List["OrderGrantRefundUpdateLineAddInput"]] = Field(
        alias="addLines", default=None
    )
    remove_lines: Optional[List[str]] = Field(alias="removeLines", default=None)
    grant_refund_for_shipping: Optional[bool] = Field(
        alias="grantRefundForShipping", default=None
    )
    transaction_id: Optional[str] = Field(alias="transactionId", default=None)


class OrderGrantRefundUpdateLineAddInput(BaseModel):
    id: str
    quantity: int
    reason: Optional[str] = None


class OrderLineInput(BaseModel):
    quantity: int


class OrderDiscountCommonInput(BaseModel):
    value_type: DiscountValueTypeEnum = Field(alias="valueType")
    value: Any
    reason: Optional[str] = None


class OrderNoteInput(BaseModel):
    message: str


class OrderUpdateInput(BaseModel):
    billing_address: Optional["AddressInput"] = Field(
        alias="billingAddress", default=None
    )
    user_email: Optional[str] = Field(alias="userEmail", default=None)
    shipping_address: Optional["AddressInput"] = Field(
        alias="shippingAddress", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class OrderUpdateShippingInput(BaseModel):
    shipping_method: Optional[str] = Field(alias="shippingMethod", default=None)


class OrderBulkCreateInput(BaseModel):
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    channel: str
    created_at: Any = Field(alias="createdAt")
    status: Optional[OrderStatus] = None
    user: "OrderBulkCreateUserInput"
    billing_address: "AddressInput" = Field(alias="billingAddress")
    shipping_address: Optional["AddressInput"] = Field(
        alias="shippingAddress", default=None
    )
    currency: str
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    customer_note: Optional[str] = Field(alias="customerNote", default=None)
    notes: Optional[List["OrderBulkCreateNoteInput"]] = None
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    display_gross_prices: Optional[bool] = Field(
        alias="displayGrossPrices", default=None
    )
    weight: Optional[Any] = None
    redirect_url: Optional[str] = Field(alias="redirectUrl", default=None)
    lines: List["OrderBulkCreateOrderLineInput"]
    delivery_method: Optional["OrderBulkCreateDeliveryMethodInput"] = Field(
        alias="deliveryMethod", default=None
    )
    gift_cards: Optional[List[str]] = Field(alias="giftCards", default=None)
    voucher_code: Optional[str] = Field(alias="voucherCode", default=None)
    discounts: Optional[List["OrderDiscountCommonInput"]] = None
    fulfillments: Optional[List["OrderBulkCreateFulfillmentInput"]] = None
    transactions: Optional[List["TransactionCreateInput"]] = None
    invoices: Optional[List["OrderBulkCreateInvoiceInput"]] = None


class OrderBulkCreateUserInput(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class OrderBulkCreateNoteInput(BaseModel):
    message: str
    date: Optional[Any] = None
    user_id: Optional[str] = Field(alias="userId", default=None)
    user_email: Optional[str] = Field(alias="userEmail", default=None)
    user_external_reference: Optional[str] = Field(
        alias="userExternalReference", default=None
    )
    app_id: Optional[str] = Field(alias="appId", default=None)


class OrderBulkCreateOrderLineInput(BaseModel):
    variant_id: Optional[str] = Field(alias="variantId", default=None)
    variant_sku: Optional[str] = Field(alias="variantSku", default=None)
    variant_external_reference: Optional[str] = Field(
        alias="variantExternalReference", default=None
    )
    variant_name: Optional[str] = Field(alias="variantName", default=None)
    product_name: Optional[str] = Field(alias="productName", default=None)
    translated_variant_name: Optional[str] = Field(
        alias="translatedVariantName", default=None
    )
    translated_product_name: Optional[str] = Field(
        alias="translatedProductName", default=None
    )
    created_at: Any = Field(alias="createdAt")
    is_shipping_required: bool = Field(alias="isShippingRequired")
    is_gift_card: bool = Field(alias="isGiftCard")
    quantity: int
    total_price: "TaxedMoneyInput" = Field(alias="totalPrice")
    undiscounted_total_price: "TaxedMoneyInput" = Field(alias="undiscountedTotalPrice")
    warehouse: str
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    tax_rate: Optional[Any] = Field(alias="taxRate", default=None)
    tax_class_id: Optional[str] = Field(alias="taxClassId", default=None)
    tax_class_name: Optional[str] = Field(alias="taxClassName", default=None)
    tax_class_metadata: Optional[List["MetadataInput"]] = Field(
        alias="taxClassMetadata", default=None
    )
    tax_class_private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="taxClassPrivateMetadata", default=None
    )


class TaxedMoneyInput(BaseModel):
    gross: Any
    net: Any


class OrderBulkCreateDeliveryMethodInput(BaseModel):
    warehouse_id: Optional[str] = Field(alias="warehouseId", default=None)
    warehouse_name: Optional[str] = Field(alias="warehouseName", default=None)
    shipping_method_id: Optional[str] = Field(alias="shippingMethodId", default=None)
    shipping_method_name: Optional[str] = Field(
        alias="shippingMethodName", default=None
    )
    shipping_price: Optional["TaxedMoneyInput"] = Field(
        alias="shippingPrice", default=None
    )
    shipping_tax_rate: Optional[Any] = Field(alias="shippingTaxRate", default=None)
    shipping_tax_class_id: Optional[str] = Field(
        alias="shippingTaxClassId", default=None
    )
    shipping_tax_class_name: Optional[str] = Field(
        alias="shippingTaxClassName", default=None
    )
    shipping_tax_class_metadata: Optional[List["MetadataInput"]] = Field(
        alias="shippingTaxClassMetadata", default=None
    )
    shipping_tax_class_private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="shippingTaxClassPrivateMetadata", default=None
    )


class OrderBulkCreateFulfillmentInput(BaseModel):
    tracking_code: Optional[str] = Field(alias="trackingCode", default=None)
    lines: Optional[List["OrderBulkCreateFulfillmentLineInput"]] = None


class OrderBulkCreateFulfillmentLineInput(BaseModel):
    variant_id: Optional[str] = Field(alias="variantId", default=None)
    variant_sku: Optional[str] = Field(alias="variantSku", default=None)
    variant_external_reference: Optional[str] = Field(
        alias="variantExternalReference", default=None
    )
    quantity: int
    warehouse: str
    order_line_index: int = Field(alias="orderLineIndex")


class OrderBulkCreateInvoiceInput(BaseModel):
    created_at: Any = Field(alias="createdAt")
    number: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )


class MenuCreateInput(BaseModel):
    name: str
    slug: Optional[str] = None
    items: Optional[List["MenuItemInput"]] = None


class MenuItemInput(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    collection: Optional[str] = None
    page: Optional[str] = None


class MenuInput(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


class MenuItemCreateInput(BaseModel):
    name: str
    url: Optional[str] = None
    category: Optional[str] = None
    collection: Optional[str] = None
    page: Optional[str] = None
    menu: str
    parent: Optional[str] = None


class MenuItemMoveInput(BaseModel):
    item_id: str = Field(alias="itemId")
    parent_id: Optional[str] = Field(alias="parentId", default=None)
    sort_order: Optional[int] = Field(alias="sortOrder", default=None)


class InvoiceCreateInput(BaseModel):
    number: str
    url: str
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )


class UpdateInvoiceInput(BaseModel):
    number: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )


class GiftCardCreateInput(BaseModel):
    add_tags: Optional[List[str]] = Field(alias="addTags", default=None)
    expiry_date: Optional[Any] = Field(alias="expiryDate", default=None)
    start_date: Optional[Any] = Field(alias="startDate", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)
    balance: "PriceInput"
    user_email: Optional[str] = Field(alias="userEmail", default=None)
    channel: Optional[str] = None
    is_active: bool = Field(alias="isActive")
    code: Optional[str] = None
    note: Optional[str] = None


class PriceInput(BaseModel):
    currency: str
    amount: Any


class GiftCardUpdateInput(BaseModel):
    add_tags: Optional[List[str]] = Field(alias="addTags", default=None)
    expiry_date: Optional[Any] = Field(alias="expiryDate", default=None)
    start_date: Optional[Any] = Field(alias="startDate", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)
    remove_tags: Optional[List[str]] = Field(alias="removeTags", default=None)
    balance_amount: Optional[Any] = Field(alias="balanceAmount", default=None)


class GiftCardResendInput(BaseModel):
    id: str
    email: Optional[str] = None
    channel: str


class GiftCardAddNoteInput(BaseModel):
    message: str


class GiftCardBulkCreateInput(BaseModel):
    count: int
    balance: "PriceInput"
    tags: Optional[List[str]] = None
    expiry_date: Optional[Any] = Field(alias="expiryDate", default=None)
    is_active: bool = Field(alias="isActive")


class PluginUpdateInput(BaseModel):
    active: Optional[bool] = None
    configuration: Optional[List["ConfigurationItemInput"]] = None


class ConfigurationItemInput(BaseModel):
    name: str
    value: Optional[str] = None


class ExternalNotificationTriggerInput(BaseModel):
    ids: List[str]
    extra_payload: Optional[Any] = Field(alias="extraPayload", default=None)
    external_event_type: str = Field(alias="externalEventType")


class PromotionCreateInput(BaseModel):
    description: Optional[Any] = None
    start_date: Optional[Any] = Field(alias="startDate", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)
    name: str
    type: Optional[PromotionTypeEnum] = None
    rules: Optional[List["PromotionRuleInput"]] = None


class PromotionRuleInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None
    catalogue_predicate: Optional["CataloguePredicateInput"] = Field(
        alias="cataloguePredicate", default=None
    )
    order_predicate: Optional["OrderPredicateInput"] = Field(
        alias="orderPredicate", default=None
    )
    reward_value_type: Optional[RewardValueTypeEnum] = Field(
        alias="rewardValueType", default=None
    )
    reward_value: Optional[Any] = Field(alias="rewardValue", default=None)
    reward_type: Optional[RewardTypeEnum] = Field(alias="rewardType", default=None)
    channels: Optional[List[str]] = None
    gifts: Optional[List[str]] = None


class CataloguePredicateInput(BaseModel):
    variant_predicate: Optional["ProductVariantWhereInput"] = Field(
        alias="variantPredicate", default=None
    )
    product_predicate: Optional["ProductWhereInput"] = Field(
        alias="productPredicate", default=None
    )
    category_predicate: Optional["CategoryWhereInput"] = Field(
        alias="categoryPredicate", default=None
    )
    collection_predicate: Optional["CollectionWhereInput"] = Field(
        alias="collectionPredicate", default=None
    )
    and_: Optional[List["CataloguePredicateInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["CataloguePredicateInput"]] = Field(alias="OR", default=None)


class OrderPredicateInput(BaseModel):
    discounted_object_predicate: Optional["DiscountedObjectWhereInput"] = Field(
        alias="discountedObjectPredicate", default=None
    )
    and_: Optional[List["OrderPredicateInput"]] = Field(alias="AND", default=None)
    or_: Optional[List["OrderPredicateInput"]] = Field(alias="OR", default=None)


class DiscountedObjectWhereInput(BaseModel):
    base_subtotal_price: Optional["DecimalFilterInput"] = Field(
        alias="baseSubtotalPrice", default=None
    )
    base_total_price: Optional["DecimalFilterInput"] = Field(
        alias="baseTotalPrice", default=None
    )
    and_: Optional[List["DiscountedObjectWhereInput"]] = Field(
        alias="AND", default=None
    )
    or_: Optional[List["DiscountedObjectWhereInput"]] = Field(alias="OR", default=None)


class PromotionUpdateInput(BaseModel):
    description: Optional[Any] = None
    start_date: Optional[Any] = Field(alias="startDate", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)
    name: Optional[str] = None


class PromotionRuleCreateInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None
    catalogue_predicate: Optional["CataloguePredicateInput"] = Field(
        alias="cataloguePredicate", default=None
    )
    order_predicate: Optional["OrderPredicateInput"] = Field(
        alias="orderPredicate", default=None
    )
    reward_value_type: Optional[RewardValueTypeEnum] = Field(
        alias="rewardValueType", default=None
    )
    reward_value: Optional[Any] = Field(alias="rewardValue", default=None)
    reward_type: Optional[RewardTypeEnum] = Field(alias="rewardType", default=None)
    channels: Optional[List[str]] = None
    gifts: Optional[List[str]] = None
    promotion: str


class PromotionRuleUpdateInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None
    catalogue_predicate: Optional["CataloguePredicateInput"] = Field(
        alias="cataloguePredicate", default=None
    )
    order_predicate: Optional["OrderPredicateInput"] = Field(
        alias="orderPredicate", default=None
    )
    reward_value_type: Optional[RewardValueTypeEnum] = Field(
        alias="rewardValueType", default=None
    )
    reward_value: Optional[Any] = Field(alias="rewardValue", default=None)
    reward_type: Optional[RewardTypeEnum] = Field(alias="rewardType", default=None)
    add_channels: Optional[List[str]] = Field(alias="addChannels", default=None)
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)
    add_gifts: Optional[List[str]] = Field(alias="addGifts", default=None)
    remove_gifts: Optional[List[str]] = Field(alias="removeGifts", default=None)


class PromotionTranslationInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None


class PromotionRuleTranslationInput(BaseModel):
    name: Optional[str] = None
    description: Optional[Any] = None


class SaleInput(BaseModel):
    name: Optional[str] = None
    type: Optional[DiscountValueTypeEnum] = None
    value: Optional[Any] = None
    products: Optional[List[str]] = None
    variants: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    start_date: Optional[Any] = Field(alias="startDate", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)


class CatalogueInput(BaseModel):
    products: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    variants: Optional[List[str]] = None


class SaleChannelListingInput(BaseModel):
    add_channels: Optional[List["SaleChannelListingAddInput"]] = Field(
        alias="addChannels", default=None
    )
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)


class SaleChannelListingAddInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    discount_value: Any = Field(alias="discountValue")


class VoucherInput(BaseModel):
    type: Optional[VoucherTypeEnum] = None
    name: Optional[str] = None
    code: Optional[str] = None
    add_codes: Optional[List[str]] = Field(alias="addCodes", default=None)
    start_date: Optional[Any] = Field(alias="startDate", default=None)
    end_date: Optional[Any] = Field(alias="endDate", default=None)
    discount_value_type: Optional[DiscountValueTypeEnum] = Field(
        alias="discountValueType", default=None
    )
    products: Optional[List[str]] = None
    variants: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    min_checkout_items_quantity: Optional[int] = Field(
        alias="minCheckoutItemsQuantity", default=None
    )
    countries: Optional[List[str]] = None
    apply_once_per_order: Optional[bool] = Field(
        alias="applyOncePerOrder", default=None
    )
    apply_once_per_customer: Optional[bool] = Field(
        alias="applyOncePerCustomer", default=None
    )
    only_for_staff: Optional[bool] = Field(alias="onlyForStaff", default=None)
    single_use: Optional[bool] = Field(alias="singleUse", default=None)
    usage_limit: Optional[int] = Field(alias="usageLimit", default=None)


class VoucherChannelListingInput(BaseModel):
    add_channels: Optional[List["VoucherChannelListingAddInput"]] = Field(
        alias="addChannels", default=None
    )
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)


class VoucherChannelListingAddInput(BaseModel):
    channel_id: str = Field(alias="channelId")
    discount_value: Optional[Any] = Field(alias="discountValue", default=None)
    min_amount_spent: Optional[Any] = Field(alias="minAmountSpent", default=None)


class ExportProductsInput(BaseModel):
    scope: ExportScope
    filter: Optional["ProductFilterInput"] = None
    ids: Optional[List[str]] = None
    export_info: Optional["ExportInfoInput"] = Field(alias="exportInfo", default=None)
    file_type: FileTypesEnum = Field(alias="fileType")


class ExportInfoInput(BaseModel):
    attributes: Optional[List[str]] = None
    warehouses: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    fields: Optional[List[ProductFieldEnum]] = None


class ExportGiftCardsInput(BaseModel):
    scope: ExportScope
    filter: Optional["GiftCardFilterInput"] = None
    ids: Optional[List[str]] = None
    file_type: FileTypesEnum = Field(alias="fileType")


class ExportVoucherCodesInput(BaseModel):
    voucher_id: Optional[str] = Field(alias="voucherId", default=None)
    ids: Optional[List[str]] = None
    file_type: FileTypesEnum = Field(alias="fileType")


class CheckoutAddressValidationRules(BaseModel):
    check_required_fields: Optional[bool] = Field(
        alias="checkRequiredFields", default=True
    )
    check_fields_format: Optional[bool] = Field(alias="checkFieldsFormat", default=True)
    enable_fields_normalization: Optional[bool] = Field(
        alias="enableFieldsNormalization", default=True
    )


class CheckoutCreateInput(BaseModel):
    channel: Optional[str] = None
    lines: List["CheckoutLineInput"]
    email: Optional[str] = None
    shipping_address: Optional["AddressInput"] = Field(
        alias="shippingAddress", default=None
    )
    billing_address: Optional["AddressInput"] = Field(
        alias="billingAddress", default=None
    )
    language_code: Optional[LanguageCodeEnum] = Field(
        alias="languageCode", default=None
    )
    validation_rules: Optional["CheckoutValidationRules"] = Field(
        alias="validationRules", default=None
    )


class CheckoutLineInput(BaseModel):
    quantity: int
    variant_id: str = Field(alias="variantId")
    price: Optional[Any] = None
    force_new_line: Optional[bool] = Field(alias="forceNewLine", default=False)
    metadata: Optional[List["MetadataInput"]] = None


class CheckoutValidationRules(BaseModel):
    shipping_address: Optional["CheckoutAddressValidationRules"] = Field(
        alias="shippingAddress", default=None
    )
    billing_address: Optional["CheckoutAddressValidationRules"] = Field(
        alias="billingAddress", default=None
    )


class CheckoutLineUpdateInput(BaseModel):
    variant_id: Optional[str] = Field(alias="variantId", default=None)
    quantity: Optional[int] = None
    price: Optional[Any] = None
    line_id: Optional[str] = Field(alias="lineId", default=None)


class PaymentInput(BaseModel):
    gateway: str
    token: Optional[str] = None
    amount: Optional[Any] = None
    return_url: Optional[str] = Field(alias="returnUrl", default=None)
    store_payment_method: Optional[StorePaymentMethodEnum] = Field(
        alias="storePaymentMethod", default=StorePaymentMethodEnum.NONE
    )
    metadata: Optional[List["MetadataInput"]] = None


class ChannelCreateInput(BaseModel):
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    stock_settings: Optional["StockSettingsInput"] = Field(
        alias="stockSettings", default=None
    )
    add_shipping_zones: Optional[List[str]] = Field(
        alias="addShippingZones", default=None
    )
    add_warehouses: Optional[List[str]] = Field(alias="addWarehouses", default=None)
    order_settings: Optional["OrderSettingsInput"] = Field(
        alias="orderSettings", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    checkout_settings: Optional["CheckoutSettingsInput"] = Field(
        alias="checkoutSettings", default=None
    )
    payment_settings: Optional["PaymentSettingsInput"] = Field(
        alias="paymentSettings", default=None
    )
    name: str
    slug: str
    currency_code: str = Field(alias="currencyCode")
    default_country: CountryCode = Field(alias="defaultCountry")


class StockSettingsInput(BaseModel):
    allocation_strategy: AllocationStrategyEnum = Field(alias="allocationStrategy")


class OrderSettingsInput(BaseModel):
    automatically_confirm_all_new_orders: Optional[bool] = Field(
        alias="automaticallyConfirmAllNewOrders", default=None
    )
    automatically_fulfill_non_shippable_gift_card: Optional[bool] = Field(
        alias="automaticallyFulfillNonShippableGiftCard", default=None
    )
    expire_orders_after: Optional[Any] = Field(alias="expireOrdersAfter", default=None)
    delete_expired_orders_after: Optional[Any] = Field(
        alias="deleteExpiredOrdersAfter", default=None
    )
    mark_as_paid_strategy: Optional[MarkAsPaidStrategyEnum] = Field(
        alias="markAsPaidStrategy", default=None
    )
    allow_unpaid_orders: Optional[bool] = Field(alias="allowUnpaidOrders", default=None)
    include_draft_order_in_voucher_usage: Optional[bool] = Field(
        alias="includeDraftOrderInVoucherUsage", default=None
    )


class CheckoutSettingsInput(BaseModel):
    use_legacy_error_flow: Optional[bool] = Field(
        alias="useLegacyErrorFlow", default=None
    )


class PaymentSettingsInput(BaseModel):
    default_transaction_flow_strategy: Optional[TransactionFlowStrategyEnum] = Field(
        alias="defaultTransactionFlowStrategy", default=None
    )


class ChannelUpdateInput(BaseModel):
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    stock_settings: Optional["StockSettingsInput"] = Field(
        alias="stockSettings", default=None
    )
    add_shipping_zones: Optional[List[str]] = Field(
        alias="addShippingZones", default=None
    )
    add_warehouses: Optional[List[str]] = Field(alias="addWarehouses", default=None)
    order_settings: Optional["OrderSettingsInput"] = Field(
        alias="orderSettings", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    checkout_settings: Optional["CheckoutSettingsInput"] = Field(
        alias="checkoutSettings", default=None
    )
    payment_settings: Optional["PaymentSettingsInput"] = Field(
        alias="paymentSettings", default=None
    )
    name: Optional[str] = None
    slug: Optional[str] = None
    default_country: Optional[CountryCode] = Field(alias="defaultCountry", default=None)
    remove_shipping_zones: Optional[List[str]] = Field(
        alias="removeShippingZones", default=None
    )
    remove_warehouses: Optional[List[str]] = Field(
        alias="removeWarehouses", default=None
    )


class ChannelDeleteInput(BaseModel):
    channel_id: str = Field(alias="channelId")


class AttributeCreateInput(BaseModel):
    input_type: Optional[AttributeInputTypeEnum] = Field(
        alias="inputType", default=None
    )
    entity_type: Optional[AttributeEntityTypeEnum] = Field(
        alias="entityType", default=None
    )
    name: str
    slug: Optional[str] = None
    type: AttributeTypeEnum
    unit: Optional[MeasurementUnitsEnum] = None
    values: Optional[List["AttributeValueCreateInput"]] = None
    value_required: Optional[bool] = Field(alias="valueRequired", default=None)
    is_variant_only: Optional[bool] = Field(alias="isVariantOnly", default=None)
    visible_in_storefront: Optional[bool] = Field(
        alias="visibleInStorefront", default=None
    )
    filterable_in_storefront: Optional[bool] = Field(
        alias="filterableInStorefront", default=None
    )
    filterable_in_dashboard: Optional[bool] = Field(
        alias="filterableInDashboard", default=None
    )
    storefront_search_position: Optional[int] = Field(
        alias="storefrontSearchPosition", default=None
    )
    available_in_grid: Optional[bool] = Field(alias="availableInGrid", default=None)
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class AttributeValueCreateInput(BaseModel):
    value: Optional[str] = None
    rich_text: Optional[Any] = Field(alias="richText", default=None)
    plain_text: Optional[str] = Field(alias="plainText", default=None)
    file_url: Optional[str] = Field(alias="fileUrl", default=None)
    content_type: Optional[str] = Field(alias="contentType", default=None)
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    name: str


class AttributeUpdateInput(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    unit: Optional[MeasurementUnitsEnum] = None
    remove_values: Optional[List[str]] = Field(alias="removeValues", default=None)
    add_values: Optional[List["AttributeValueUpdateInput"]] = Field(
        alias="addValues", default=None
    )
    value_required: Optional[bool] = Field(alias="valueRequired", default=None)
    is_variant_only: Optional[bool] = Field(alias="isVariantOnly", default=None)
    visible_in_storefront: Optional[bool] = Field(
        alias="visibleInStorefront", default=None
    )
    filterable_in_storefront: Optional[bool] = Field(
        alias="filterableInStorefront", default=None
    )
    filterable_in_dashboard: Optional[bool] = Field(
        alias="filterableInDashboard", default=None
    )
    storefront_search_position: Optional[int] = Field(
        alias="storefrontSearchPosition", default=None
    )
    available_in_grid: Optional[bool] = Field(alias="availableInGrid", default=None)
    external_reference: Optional[str] = Field(alias="externalReference", default=None)


class AttributeValueUpdateInput(BaseModel):
    value: Optional[str] = None
    rich_text: Optional[Any] = Field(alias="richText", default=None)
    plain_text: Optional[str] = Field(alias="plainText", default=None)
    file_url: Optional[str] = Field(alias="fileUrl", default=None)
    content_type: Optional[str] = Field(alias="contentType", default=None)
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    name: Optional[str] = None


class AttributeBulkUpdateInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    fields: "AttributeUpdateInput"


class AttributeBulkTranslateInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    translation_fields: "NameTranslationInput" = Field(alias="translationFields")


class AttributeValueBulkTranslateInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    translation_fields: "AttributeValueTranslationInput" = Field(
        alias="translationFields"
    )


class AttributeValueTranslationInput(BaseModel):
    name: Optional[str] = None
    rich_text: Optional[Any] = Field(alias="richText", default=None)
    plain_text: Optional[str] = Field(alias="plainText", default=None)


class AppInput(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    permissions: Optional[List[PermissionEnum]] = None


class AppTokenInput(BaseModel):
    name: Optional[str] = None
    app: str


class AppInstallInput(BaseModel):
    app_name: Optional[str] = Field(alias="appName", default=None)
    manifest_url: Optional[str] = Field(alias="manifestUrl", default=None)
    activate_after_installation: Optional[bool] = Field(
        alias="activateAfterInstallation", default=True
    )
    permissions: Optional[List[PermissionEnum]] = None


class AccountRegisterInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    language_code: Optional[LanguageCodeEnum] = Field(
        alias="languageCode", default=None
    )
    email: str
    password: str
    redirect_url: Optional[str] = Field(alias="redirectUrl", default=None)
    metadata: Optional[List["MetadataInput"]] = None
    channel: Optional[str] = None


class AccountInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    language_code: Optional[LanguageCodeEnum] = Field(
        alias="languageCode", default=None
    )
    default_billing_address: Optional["AddressInput"] = Field(
        alias="defaultBillingAddress", default=None
    )
    default_shipping_address: Optional["AddressInput"] = Field(
        alias="defaultShippingAddress", default=None
    )
    metadata: Optional[List["MetadataInput"]] = None


class UserCreateInput(BaseModel):
    default_billing_address: Optional["AddressInput"] = Field(
        alias="defaultBillingAddress", default=None
    )
    default_shipping_address: Optional["AddressInput"] = Field(
        alias="defaultShippingAddress", default=None
    )
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    note: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    language_code: Optional[LanguageCodeEnum] = Field(
        alias="languageCode", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    is_confirmed: Optional[bool] = Field(alias="isConfirmed", default=None)
    redirect_url: Optional[str] = Field(alias="redirectUrl", default=None)
    channel: Optional[str] = None


class CustomerInput(BaseModel):
    default_billing_address: Optional["AddressInput"] = Field(
        alias="defaultBillingAddress", default=None
    )
    default_shipping_address: Optional["AddressInput"] = Field(
        alias="defaultShippingAddress", default=None
    )
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    note: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    language_code: Optional[LanguageCodeEnum] = Field(
        alias="languageCode", default=None
    )
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    is_confirmed: Optional[bool] = Field(alias="isConfirmed", default=None)


class CustomerBulkUpdateInput(BaseModel):
    id: Optional[str] = None
    external_reference: Optional[str] = Field(alias="externalReference", default=None)
    input: "CustomerInput"


class StaffCreateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    note: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    add_groups: Optional[List[str]] = Field(alias="addGroups", default=None)
    redirect_url: Optional[str] = Field(alias="redirectUrl", default=None)


class StaffUpdateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: Optional[str] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)
    note: Optional[str] = None
    metadata: Optional[List["MetadataInput"]] = None
    private_metadata: Optional[List["MetadataInput"]] = Field(
        alias="privateMetadata", default=None
    )
    add_groups: Optional[List[str]] = Field(alias="addGroups", default=None)
    remove_groups: Optional[List[str]] = Field(alias="removeGroups", default=None)


class PermissionGroupCreateInput(BaseModel):
    add_permissions: Optional[List[PermissionEnum]] = Field(
        alias="addPermissions", default=None
    )
    add_users: Optional[List[str]] = Field(alias="addUsers", default=None)
    add_channels: Optional[List[str]] = Field(alias="addChannels", default=None)
    name: str
    restricted_access_to_channels: Optional[bool] = Field(
        alias="restrictedAccessToChannels", default=False
    )


class PermissionGroupUpdateInput(BaseModel):
    add_permissions: Optional[List[PermissionEnum]] = Field(
        alias="addPermissions", default=None
    )
    add_users: Optional[List[str]] = Field(alias="addUsers", default=None)
    add_channels: Optional[List[str]] = Field(alias="addChannels", default=None)
    name: Optional[str] = None
    remove_permissions: Optional[List[PermissionEnum]] = Field(
        alias="removePermissions", default=None
    )
    remove_users: Optional[List[str]] = Field(alias="removeUsers", default=None)
    remove_channels: Optional[List[str]] = Field(alias="removeChannels", default=None)
    restricted_access_to_channels: Optional[bool] = Field(
        alias="restrictedAccessToChannels", default=None
    )


AttributeFilterInput.model_rebuild()
AttributeWhereInput.model_rebuild()
ProductFilterInput.model_rebuild()
AttributeInput.model_rebuild()
ProductStockFilterInput.model_rebuild()
ProductWhereInput.model_rebuild()
DecimalFilterInput.model_rebuild()
DateTimeFilterInput.model_rebuild()
AddressInput.model_rebuild()
WarehouseFilterInput.model_rebuild()
TaxConfigurationFilterInput.model_rebuild()
TaxClassFilterInput.model_rebuild()
CategoryFilterInput.model_rebuild()
CategoryWhereInput.model_rebuild()
CollectionFilterInput.model_rebuild()
CollectionWhereInput.model_rebuild()
ProductTypeFilterInput.model_rebuild()
ProductVariantFilterInput.model_rebuild()
ProductVariantWhereInput.model_rebuild()
PageFilterInput.model_rebuild()
OrderFilterInput.model_rebuild()
OrderDraftFilterInput.model_rebuild()
MenuFilterInput.model_rebuild()
MenuItemFilterInput.model_rebuild()
GiftCardFilterInput.model_rebuild()
PluginFilterInput.model_rebuild()
SaleFilterInput.model_rebuild()
VoucherFilterInput.model_rebuild()
PromotionWhereInput.model_rebuild()
ExportFileFilterInput.model_rebuild()
CheckoutFilterInput.model_rebuild()
CustomerFilterInput.model_rebuild()
WarehouseCreateInput.model_rebuild()
WarehouseUpdateInput.model_rebuild()
TaxClassCreateInput.model_rebuild()
TaxClassUpdateInput.model_rebuild()
TaxConfigurationUpdateInput.model_rebuild()
ShopSettingsInput.model_rebuild()
GiftCardSettingsUpdateInput.model_rebuild()
ShippingMethodChannelListingInput.model_rebuild()
ShippingPriceInput.model_rebuild()
CategoryInput.model_rebuild()
CollectionCreateInput.model_rebuild()
CollectionInput.model_rebuild()
CollectionChannelListingUpdateInput.model_rebuild()
ProductCreateInput.model_rebuild()
AttributeValueInput.model_rebuild()
ProductBulkCreateInput.model_rebuild()
ProductVariantBulkCreateInput.model_rebuild()
BulkAttributeValueInput.model_rebuild()
ProductInput.model_rebuild()
ProductBulkTranslateInput.model_rebuild()
ProductChannelListingUpdateInput.model_rebuild()
DigitalContentUploadInput.model_rebuild()
DigitalContentInput.model_rebuild()
ProductVariantCreateInput.model_rebuild()
ProductVariantBulkUpdateInput.model_rebuild()
ProductVariantStocksUpdateInput.model_rebuild()
ProductVariantChannelListingUpdateInput.model_rebuild()
ProductVariantInput.model_rebuild()
ProductVariantBulkTranslateInput.model_rebuild()
PaymentCheckBalanceInput.model_rebuild()
CardInput.model_rebuild()
TransactionCreateInput.model_rebuild()
TransactionUpdateInput.model_rebuild()
PageCreateInput.model_rebuild()
PageInput.model_rebuild()
DraftOrderCreateInput.model_rebuild()
DraftOrderInput.model_rebuild()
OrderFulfillInput.model_rebuild()
OrderFulfillLineInput.model_rebuild()
OrderRefundProductsInput.model_rebuild()
OrderReturnProductsInput.model_rebuild()
OrderGrantRefundCreateInput.model_rebuild()
OrderGrantRefundUpdateInput.model_rebuild()
OrderUpdateInput.model_rebuild()
OrderBulkCreateInput.model_rebuild()
OrderBulkCreateOrderLineInput.model_rebuild()
OrderBulkCreateDeliveryMethodInput.model_rebuild()
OrderBulkCreateFulfillmentInput.model_rebuild()
OrderBulkCreateInvoiceInput.model_rebuild()
MenuCreateInput.model_rebuild()
InvoiceCreateInput.model_rebuild()
UpdateInvoiceInput.model_rebuild()
GiftCardCreateInput.model_rebuild()
GiftCardBulkCreateInput.model_rebuild()
PluginUpdateInput.model_rebuild()
PromotionCreateInput.model_rebuild()
PromotionRuleInput.model_rebuild()
CataloguePredicateInput.model_rebuild()
OrderPredicateInput.model_rebuild()
DiscountedObjectWhereInput.model_rebuild()
PromotionRuleCreateInput.model_rebuild()
PromotionRuleUpdateInput.model_rebuild()
SaleChannelListingInput.model_rebuild()
VoucherChannelListingInput.model_rebuild()
ExportProductsInput.model_rebuild()
ExportGiftCardsInput.model_rebuild()
CheckoutCreateInput.model_rebuild()
CheckoutLineInput.model_rebuild()
CheckoutValidationRules.model_rebuild()
PaymentInput.model_rebuild()
ChannelCreateInput.model_rebuild()
ChannelUpdateInput.model_rebuild()
AttributeCreateInput.model_rebuild()
AttributeUpdateInput.model_rebuild()
AttributeBulkUpdateInput.model_rebuild()
AttributeBulkTranslateInput.model_rebuild()
AttributeValueBulkTranslateInput.model_rebuild()
AccountRegisterInput.model_rebuild()
AccountInput.model_rebuild()
UserCreateInput.model_rebuild()
CustomerInput.model_rebuild()
CustomerBulkUpdateInput.model_rebuild()
StaffCreateInput.model_rebuild()
StaffUpdateInput.model_rebuild()

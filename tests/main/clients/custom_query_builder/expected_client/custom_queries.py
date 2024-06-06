from typing import Any, Optional

from .custom_fields import (
    AddressFields,
    AddressValidationDataFields,
    AppCountableConnectionFields,
    AppExtensionCountableConnectionFields,
    AppExtensionFields,
    AppFields,
    AppInstallationFields,
    AttributeCountableConnectionFields,
    AttributeFields,
    CategoryCountableConnectionFields,
    CategoryFields,
    ChannelFields,
    CheckoutCountableConnectionFields,
    CheckoutFields,
    CheckoutLineCountableConnectionFields,
    CollectionCountableConnectionFields,
    CollectionFields,
    DigitalContentCountableConnectionFields,
    DigitalContentFields,
    ExportFileCountableConnectionFields,
    ExportFileFields,
    GiftCardCountableConnectionFields,
    GiftCardFields,
    GiftCardSettingsFields,
    GiftCardTagCountableConnectionFields,
    GroupCountableConnectionFields,
    GroupFields,
    MenuCountableConnectionFields,
    MenuFields,
    MenuItemCountableConnectionFields,
    MenuItemFields,
    OrderCountableConnectionFields,
    OrderEventCountableConnectionFields,
    OrderFields,
    OrderSettingsFields,
    PageCountableConnectionFields,
    PageFields,
    PageTypeCountableConnectionFields,
    PageTypeFields,
    PaymentCountableConnectionFields,
    PaymentFields,
    PluginCountableConnectionFields,
    PluginFields,
    ProductCountableConnectionFields,
    ProductFields,
    ProductTypeCountableConnectionFields,
    ProductTypeFields,
    ProductVariantCountableConnectionFields,
    ProductVariantFields,
    PromotionCountableConnectionFields,
    PromotionFields,
    SaleCountableConnectionFields,
    SaleFields,
    ShippingZoneCountableConnectionFields,
    ShippingZoneFields,
    ShopFields,
    StockCountableConnectionFields,
    StockFields,
    TaxClassCountableConnectionFields,
    TaxClassFields,
    TaxConfigurationCountableConnectionFields,
    TaxConfigurationFields,
    TaxCountryConfigurationFields,
    TaxedMoneyFields,
    TaxTypeFields,
    TransactionItemFields,
    TranslatableItemConnectionFields,
    UserCountableConnectionFields,
    UserFields,
    VoucherCountableConnectionFields,
    VoucherFields,
    WarehouseCountableConnectionFields,
    WarehouseFields,
    WebhookEventFields,
    WebhookFields,
    _ServiceFields,
)
from .enums import CountryCode, ReportingPeriod, TranslatableKinds
from .input_types import (
    AppExtensionFilterInput,
    AppFilterInput,
    AppSortingInput,
    AttributeFilterInput,
    AttributeSortingInput,
    AttributeWhereInput,
    CategoryFilterInput,
    CategorySortingInput,
    CategoryWhereInput,
    CheckoutFilterInput,
    CheckoutSortingInput,
    CollectionFilterInput,
    CollectionSortingInput,
    CollectionWhereInput,
    CustomerFilterInput,
    ExportFileFilterInput,
    ExportFileSortingInput,
    GiftCardFilterInput,
    GiftCardSortingInput,
    GiftCardTagFilterInput,
    MenuFilterInput,
    MenuItemFilterInput,
    MenuItemSortingInput,
    MenuSortingInput,
    OrderDraftFilterInput,
    OrderFilterInput,
    OrderSortingInput,
    PageFilterInput,
    PageSortingInput,
    PageTypeFilterInput,
    PageTypeSortingInput,
    PaymentFilterInput,
    PermissionGroupFilterInput,
    PermissionGroupSortingInput,
    PluginFilterInput,
    PluginSortingInput,
    ProductFilterInput,
    ProductOrder,
    ProductTypeFilterInput,
    ProductTypeSortingInput,
    ProductVariantFilterInput,
    ProductVariantSortingInput,
    ProductVariantWhereInput,
    ProductWhereInput,
    PromotionSortingInput,
    PromotionWhereInput,
    SaleFilterInput,
    SaleSortingInput,
    ShippingZoneFilterInput,
    StaffUserInput,
    StockFilterInput,
    TaxClassFilterInput,
    TaxClassSortingInput,
    TaxConfigurationFilterInput,
    UserSortingInput,
    VoucherFilterInput,
    VoucherSortingInput,
    WarehouseFilterInput,
    WarehouseSortingInput,
)


class Query:
    @classmethod
    def webhook(cls, *, id: Optional[str] = None) -> WebhookFields:
        return WebhookFields(field_name="webhook", id=id)

    @classmethod
    def webhook_events(cls) -> WebhookEventFields:
        return WebhookEventFields(field_name="webhookEvents")

    @classmethod
    def warehouse(
        cls, *, id: Optional[str] = None, externalReference: Optional[str] = None
    ) -> WarehouseFields:
        return WarehouseFields(
            field_name="warehouse", id=id, externalReference=externalReference
        )

    @classmethod
    def warehouses(
        cls,
        *,
        filter: Optional[WarehouseFilterInput] = None,
        sortBy: Optional[WarehouseSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> WarehouseCountableConnectionFields:
        return WarehouseCountableConnectionFields(
            field_name="warehouses",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def translations(
        cls,
        *,
        kind: Optional[TranslatableKinds] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> TranslatableItemConnectionFields:
        return TranslatableItemConnectionFields(
            field_name="translations",
            kind=kind,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def tax_configuration(cls, *, id: Optional[str] = None) -> TaxConfigurationFields:
        return TaxConfigurationFields(field_name="taxConfiguration", id=id)

    @classmethod
    def tax_configurations(
        cls,
        *,
        filter: Optional[TaxConfigurationFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> TaxConfigurationCountableConnectionFields:
        return TaxConfigurationCountableConnectionFields(
            field_name="taxConfigurations",
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def tax_class(cls, *, id: Optional[str] = None) -> TaxClassFields:
        return TaxClassFields(field_name="taxClass", id=id)

    @classmethod
    def tax_classes(
        cls,
        *,
        sortBy: Optional[TaxClassSortingInput] = None,
        filter: Optional[TaxClassFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> TaxClassCountableConnectionFields:
        return TaxClassCountableConnectionFields(
            field_name="taxClasses",
            sortBy=sortBy,
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def tax_country_configuration(
        cls, *, countryCode: Optional[CountryCode] = None
    ) -> TaxCountryConfigurationFields:
        return TaxCountryConfigurationFields(
            field_name="taxCountryConfiguration", countryCode=countryCode
        )

    @classmethod
    def tax_country_configurations(cls) -> TaxCountryConfigurationFields:
        return TaxCountryConfigurationFields(field_name="taxCountryConfigurations")

    @classmethod
    def stock(cls, *, id: Optional[str] = None) -> StockFields:
        return StockFields(field_name="stock", id=id)

    @classmethod
    def stocks(
        cls,
        *,
        filter: Optional[StockFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> StockCountableConnectionFields:
        return StockCountableConnectionFields(
            field_name="stocks",
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def shop(cls) -> ShopFields:
        return ShopFields(field_name="shop")

    @classmethod
    def order_settings(cls) -> OrderSettingsFields:
        return OrderSettingsFields(field_name="orderSettings")

    @classmethod
    def gift_card_settings(cls) -> GiftCardSettingsFields:
        return GiftCardSettingsFields(field_name="giftCardSettings")

    @classmethod
    def shipping_zone(
        cls, *, id: Optional[str] = None, channel: Optional[str] = None
    ) -> ShippingZoneFields:
        return ShippingZoneFields(field_name="shippingZone", id=id, channel=channel)

    @classmethod
    def shipping_zones(
        cls,
        *,
        filter: Optional[ShippingZoneFilterInput] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> ShippingZoneCountableConnectionFields:
        return ShippingZoneCountableConnectionFields(
            field_name="shippingZones",
            filter=filter,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def digital_content(cls, *, id: Optional[str] = None) -> DigitalContentFields:
        return DigitalContentFields(field_name="digitalContent", id=id)

    @classmethod
    def digital_contents(
        cls,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> DigitalContentCountableConnectionFields:
        return DigitalContentCountableConnectionFields(
            field_name="digitalContents",
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def categories(
        cls,
        *,
        filter: Optional[CategoryFilterInput] = None,
        where: Optional[CategoryWhereInput] = None,
        sortBy: Optional[CategorySortingInput] = None,
        level: Optional[int] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> CategoryCountableConnectionFields:
        return CategoryCountableConnectionFields(
            field_name="categories",
            filter=filter,
            where=where,
            sortBy=sortBy,
            level=level,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def category(
        cls, *, id: Optional[str] = None, slug: Optional[str] = None
    ) -> CategoryFields:
        return CategoryFields(field_name="category", id=id, slug=slug)

    @classmethod
    def collection(
        cls,
        *,
        id: Optional[str] = None,
        slug: Optional[str] = None,
        channel: Optional[str] = None
    ) -> CollectionFields:
        return CollectionFields(
            field_name="collection", id=id, slug=slug, channel=channel
        )

    @classmethod
    def collections(
        cls,
        *,
        filter: Optional[CollectionFilterInput] = None,
        where: Optional[CollectionWhereInput] = None,
        sortBy: Optional[CollectionSortingInput] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> CollectionCountableConnectionFields:
        return CollectionCountableConnectionFields(
            field_name="collections",
            filter=filter,
            where=where,
            sortBy=sortBy,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def product(
        cls,
        *,
        id: Optional[str] = None,
        slug: Optional[str] = None,
        externalReference: Optional[str] = None,
        channel: Optional[str] = None
    ) -> ProductFields:
        return ProductFields(
            field_name="product",
            id=id,
            slug=slug,
            externalReference=externalReference,
            channel=channel,
        )

    @classmethod
    def products(
        cls,
        *,
        filter: Optional[ProductFilterInput] = None,
        where: Optional[ProductWhereInput] = None,
        sortBy: Optional[ProductOrder] = None,
        search: Optional[str] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> ProductCountableConnectionFields:
        return ProductCountableConnectionFields(
            field_name="products",
            filter=filter,
            where=where,
            sortBy=sortBy,
            search=search,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def product_type(cls, *, id: Optional[str] = None) -> ProductTypeFields:
        return ProductTypeFields(field_name="productType", id=id)

    @classmethod
    def product_types(
        cls,
        *,
        filter: Optional[ProductTypeFilterInput] = None,
        sortBy: Optional[ProductTypeSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> ProductTypeCountableConnectionFields:
        return ProductTypeCountableConnectionFields(
            field_name="productTypes",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def product_variant(
        cls,
        *,
        id: Optional[str] = None,
        sku: Optional[str] = None,
        externalReference: Optional[str] = None,
        channel: Optional[str] = None
    ) -> ProductVariantFields:
        return ProductVariantFields(
            field_name="productVariant",
            id=id,
            sku=sku,
            externalReference=externalReference,
            channel=channel,
        )

    @classmethod
    def product_variants(
        cls,
        *,
        ids: Optional[str] = None,
        channel: Optional[str] = None,
        filter: Optional[ProductVariantFilterInput] = None,
        where: Optional[ProductVariantWhereInput] = None,
        sortBy: Optional[ProductVariantSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> ProductVariantCountableConnectionFields:
        return ProductVariantCountableConnectionFields(
            field_name="productVariants",
            ids=ids,
            channel=channel,
            filter=filter,
            where=where,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def report_product_sales(
        cls,
        *,
        period: Optional[ReportingPeriod] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> ProductVariantCountableConnectionFields:
        return ProductVariantCountableConnectionFields(
            field_name="reportProductSales",
            period=period,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def payment(cls, *, id: Optional[str] = None) -> PaymentFields:
        return PaymentFields(field_name="payment", id=id)

    @classmethod
    def payments(
        cls,
        *,
        filter: Optional[PaymentFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> PaymentCountableConnectionFields:
        return PaymentCountableConnectionFields(
            field_name="payments",
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def transaction(
        cls, *, id: Optional[str] = None, token: Optional[Any] = None
    ) -> TransactionItemFields:
        return TransactionItemFields(field_name="transaction", id=id, token=token)

    @classmethod
    def page(
        cls, *, id: Optional[str] = None, slug: Optional[str] = None
    ) -> PageFields:
        return PageFields(field_name="page", id=id, slug=slug)

    @classmethod
    def pages(
        cls,
        *,
        sortBy: Optional[PageSortingInput] = None,
        filter: Optional[PageFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> PageCountableConnectionFields:
        return PageCountableConnectionFields(
            field_name="pages",
            sortBy=sortBy,
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def page_type(cls, *, id: Optional[str] = None) -> PageTypeFields:
        return PageTypeFields(field_name="pageType", id=id)

    @classmethod
    def page_types(
        cls,
        *,
        sortBy: Optional[PageTypeSortingInput] = None,
        filter: Optional[PageTypeFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> PageTypeCountableConnectionFields:
        return PageTypeCountableConnectionFields(
            field_name="pageTypes",
            sortBy=sortBy,
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def homepage_events(
        cls,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> OrderEventCountableConnectionFields:
        return OrderEventCountableConnectionFields(
            field_name="homepageEvents",
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def order(
        cls, *, id: Optional[str] = None, externalReference: Optional[str] = None
    ) -> OrderFields:
        return OrderFields(
            field_name="order", id=id, externalReference=externalReference
        )

    @classmethod
    def orders(
        cls,
        *,
        sortBy: Optional[OrderSortingInput] = None,
        filter: Optional[OrderFilterInput] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> OrderCountableConnectionFields:
        return OrderCountableConnectionFields(
            field_name="orders",
            sortBy=sortBy,
            filter=filter,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def draft_orders(
        cls,
        *,
        sortBy: Optional[OrderSortingInput] = None,
        filter: Optional[OrderDraftFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> OrderCountableConnectionFields:
        return OrderCountableConnectionFields(
            field_name="draftOrders",
            sortBy=sortBy,
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def orders_total(
        cls, *, period: Optional[ReportingPeriod] = None, channel: Optional[str] = None
    ) -> TaxedMoneyFields:
        return TaxedMoneyFields(
            field_name="ordersTotal", period=period, channel=channel
        )

    @classmethod
    def order_by_token(cls, *, token: Optional[Any] = None) -> OrderFields:
        return OrderFields(field_name="orderByToken", token=token)

    @classmethod
    def menu(
        cls,
        *,
        channel: Optional[str] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        slug: Optional[str] = None
    ) -> MenuFields:
        return MenuFields(
            field_name="menu", channel=channel, id=id, name=name, slug=slug
        )

    @classmethod
    def menus(
        cls,
        *,
        channel: Optional[str] = None,
        sortBy: Optional[MenuSortingInput] = None,
        filter: Optional[MenuFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> MenuCountableConnectionFields:
        return MenuCountableConnectionFields(
            field_name="menus",
            channel=channel,
            sortBy=sortBy,
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def menu_item(
        cls, *, id: Optional[str] = None, channel: Optional[str] = None
    ) -> MenuItemFields:
        return MenuItemFields(field_name="menuItem", id=id, channel=channel)

    @classmethod
    def menu_items(
        cls,
        *,
        channel: Optional[str] = None,
        sortBy: Optional[MenuItemSortingInput] = None,
        filter: Optional[MenuItemFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> MenuItemCountableConnectionFields:
        return MenuItemCountableConnectionFields(
            field_name="menuItems",
            channel=channel,
            sortBy=sortBy,
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def gift_card(cls, *, id: Optional[str] = None) -> GiftCardFields:
        return GiftCardFields(field_name="giftCard", id=id)

    @classmethod
    def gift_cards(
        cls,
        *,
        sortBy: Optional[GiftCardSortingInput] = None,
        filter: Optional[GiftCardFilterInput] = None,
        search: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> GiftCardCountableConnectionFields:
        return GiftCardCountableConnectionFields(
            field_name="giftCards",
            sortBy=sortBy,
            filter=filter,
            search=search,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def gift_card_tags(
        cls,
        *,
        filter: Optional[GiftCardTagFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> GiftCardTagCountableConnectionFields:
        return GiftCardTagCountableConnectionFields(
            field_name="giftCardTags",
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def plugin(cls, *, id: Optional[str] = None) -> PluginFields:
        return PluginFields(field_name="plugin", id=id)

    @classmethod
    def plugins(
        cls,
        *,
        filter: Optional[PluginFilterInput] = None,
        sortBy: Optional[PluginSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> PluginCountableConnectionFields:
        return PluginCountableConnectionFields(
            field_name="plugins",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def sale(
        cls, *, id: Optional[str] = None, channel: Optional[str] = None
    ) -> SaleFields:
        return SaleFields(field_name="sale", id=id, channel=channel)

    @classmethod
    def sales(
        cls,
        *,
        filter: Optional[SaleFilterInput] = None,
        sortBy: Optional[SaleSortingInput] = None,
        query: Optional[str] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> SaleCountableConnectionFields:
        return SaleCountableConnectionFields(
            field_name="sales",
            filter=filter,
            sortBy=sortBy,
            query=query,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def voucher(
        cls, *, id: Optional[str] = None, channel: Optional[str] = None
    ) -> VoucherFields:
        return VoucherFields(field_name="voucher", id=id, channel=channel)

    @classmethod
    def vouchers(
        cls,
        *,
        filter: Optional[VoucherFilterInput] = None,
        sortBy: Optional[VoucherSortingInput] = None,
        query: Optional[str] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> VoucherCountableConnectionFields:
        return VoucherCountableConnectionFields(
            field_name="vouchers",
            filter=filter,
            sortBy=sortBy,
            query=query,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def promotion(cls, *, id: Optional[str] = None) -> PromotionFields:
        return PromotionFields(field_name="promotion", id=id)

    @classmethod
    def promotions(
        cls,
        *,
        where: Optional[PromotionWhereInput] = None,
        sortBy: Optional[PromotionSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> PromotionCountableConnectionFields:
        return PromotionCountableConnectionFields(
            field_name="promotions",
            where=where,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def export_file(cls, *, id: Optional[str] = None) -> ExportFileFields:
        return ExportFileFields(field_name="exportFile", id=id)

    @classmethod
    def export_files(
        cls,
        *,
        filter: Optional[ExportFileFilterInput] = None,
        sortBy: Optional[ExportFileSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> ExportFileCountableConnectionFields:
        return ExportFileCountableConnectionFields(
            field_name="exportFiles",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def tax_types(cls) -> TaxTypeFields:
        return TaxTypeFields(field_name="taxTypes")

    @classmethod
    def checkout(
        cls, *, id: Optional[str] = None, token: Optional[Any] = None
    ) -> CheckoutFields:
        return CheckoutFields(field_name="checkout", id=id, token=token)

    @classmethod
    def checkouts(
        cls,
        *,
        sortBy: Optional[CheckoutSortingInput] = None,
        filter: Optional[CheckoutFilterInput] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> CheckoutCountableConnectionFields:
        return CheckoutCountableConnectionFields(
            field_name="checkouts",
            sortBy=sortBy,
            filter=filter,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def checkout_lines(
        cls,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> CheckoutLineCountableConnectionFields:
        return CheckoutLineCountableConnectionFields(
            field_name="checkoutLines",
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def channel(
        cls, *, id: Optional[str] = None, slug: Optional[str] = None
    ) -> ChannelFields:
        return ChannelFields(field_name="channel", id=id, slug=slug)

    @classmethod
    def channels(cls) -> ChannelFields:
        return ChannelFields(field_name="channels")

    @classmethod
    def attributes(
        cls,
        *,
        filter: Optional[AttributeFilterInput] = None,
        where: Optional[AttributeWhereInput] = None,
        search: Optional[str] = None,
        sortBy: Optional[AttributeSortingInput] = None,
        channel: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> AttributeCountableConnectionFields:
        return AttributeCountableConnectionFields(
            field_name="attributes",
            filter=filter,
            where=where,
            search=search,
            sortBy=sortBy,
            channel=channel,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def attribute(
        cls,
        *,
        id: Optional[str] = None,
        slug: Optional[str] = None,
        externalReference: Optional[str] = None
    ) -> AttributeFields:
        return AttributeFields(
            field_name="attribute",
            id=id,
            slug=slug,
            externalReference=externalReference,
        )

    @classmethod
    def apps_installations(cls) -> AppInstallationFields:
        return AppInstallationFields(field_name="appsInstallations")

    @classmethod
    def apps(
        cls,
        *,
        filter: Optional[AppFilterInput] = None,
        sortBy: Optional[AppSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> AppCountableConnectionFields:
        return AppCountableConnectionFields(
            field_name="apps",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def app(cls, *, id: Optional[str] = None) -> AppFields:
        return AppFields(field_name="app", id=id)

    @classmethod
    def app_extensions(
        cls,
        *,
        filter: Optional[AppExtensionFilterInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> AppExtensionCountableConnectionFields:
        return AppExtensionCountableConnectionFields(
            field_name="appExtensions",
            filter=filter,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def app_extension(cls, *, id: Optional[str] = None) -> AppExtensionFields:
        return AppExtensionFields(field_name="appExtension", id=id)

    @classmethod
    def address_validation_rules(
        cls,
        *,
        countryCode: Optional[CountryCode] = None,
        countryArea: Optional[str] = None,
        city: Optional[str] = None,
        cityArea: Optional[str] = None
    ) -> AddressValidationDataFields:
        return AddressValidationDataFields(
            field_name="addressValidationRules",
            countryCode=countryCode,
            countryArea=countryArea,
            city=city,
            cityArea=cityArea,
        )

    @classmethod
    def address(cls, *, id: Optional[str] = None) -> AddressFields:
        return AddressFields(field_name="address", id=id)

    @classmethod
    def customers(
        cls,
        *,
        filter: Optional[CustomerFilterInput] = None,
        sortBy: Optional[UserSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> UserCountableConnectionFields:
        return UserCountableConnectionFields(
            field_name="customers",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def permission_groups(
        cls,
        *,
        filter: Optional[PermissionGroupFilterInput] = None,
        sortBy: Optional[PermissionGroupSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> GroupCountableConnectionFields:
        return GroupCountableConnectionFields(
            field_name="permissionGroups",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def permission_group(cls, *, id: Optional[str] = None) -> GroupFields:
        return GroupFields(field_name="permissionGroup", id=id)

    @classmethod
    def me(cls) -> UserFields:
        return UserFields(field_name="me")

    @classmethod
    def staff_users(
        cls,
        *,
        filter: Optional[StaffUserInput] = None,
        sortBy: Optional[UserSortingInput] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> UserCountableConnectionFields:
        return UserCountableConnectionFields(
            field_name="staffUsers",
            filter=filter,
            sortBy=sortBy,
            before=before,
            after=after,
            first=first,
            last=last,
        )

    @classmethod
    def user(
        cls,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        externalReference: Optional[str] = None
    ) -> UserFields:
        return UserFields(
            field_name="user", id=id, email=email, externalReference=externalReference
        )

    @classmethod
    def service(cls) -> _ServiceFields:
        return _ServiceFields(field_name="_service")

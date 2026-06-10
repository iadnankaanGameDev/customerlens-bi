import re

import numpy as np
import pandas as pd


CUSTOMER_FEATURE_FIELDS = [
    "customer_id",
    "recency",
    "frequency",
    "monetary",
    "avg_order_value",
    "unique_products",
    "total_quantity",
    "customer_lifetime_days",
]

REQUIRED_CLUSTERING_FEATURES = [
    "recency",
    "frequency",
    "monetary",
    "avg_order_value",
    "unique_products",
    "total_quantity",
    "customer_lifetime_days",
]

TRANSACTION_FIELDS = [
    "customer_id",
    "order_id",
    "order_date",
    "quantity",
    "unit_price",
    "total_amount",
    "product_id",
    "country",
]

PROFILE_FIELDS = CUSTOMER_FEATURE_FIELDS.copy()


# ============================================================
# Extended column aliases
# ============================================================

COLUMN_ALIASES = {
    "customer_id": [
        # Direct customer identifiers
        "customer_id",
        "customerid",
        "customer id",
        "customer_no",
        "customerno",
        "customer no",
        "customer_number",
        "customernumber",
        "customer number",
        "customer_code",
        "customercode",
        "customer code",

        # Client identifiers
        "client_id",
        "clientid",
        "client id",
        "client_no",
        "clientno",
        "client no",
        "client_number",
        "clientnumber",
        "client number",
        "client_code",
        "clientcode",
        "client code",

        # User identifiers
        "user_id",
        "userid",
        "user id",
        "user_no",
        "userno",
        "user no",
        "user_number",
        "usernumber",
        "user number",
        "user_code",
        "usercode",
        "user code",

        # Member identifiers
        "member_id",
        "memberid",
        "member id",
        "member_no",
        "memberno",
        "member no",
        "member_number",
        "membernumber",
        "member number",
        "member_code",
        "membercode",
        "member code",

        # Account identifiers
        "account_id",
        "accountid",
        "account id",
        "account_no",
        "accountno",
        "account no",
        "account_number",
        "accountnumber",
        "account number",
        "account_code",
        "accountcode",
        "account code",

        # Buyer / shopper identifiers
        "buyer_id",
        "buyerid",
        "buyer id",
        "buyer_no",
        "buyerno",
        "buyer no",
        "buyer_number",
        "buyernumber",
        "buyer number",
        "shopper_id",
        "shopperid",
        "shopper id",
        "shopper_no",
        "shopperno",
        "shopper no",
        "shopper_number",
        "shoppernumber",
        "shopper number",

        # Subscriber / visitor identifiers
        "subscriber_id",
        "subscriberid",
        "subscriber id",
        "visitor_id",
        "visitorid",
        "visitor id",
        "session_user_id",
        "sessionuserid",
        "session user id",

        # Names used as stable identifiers in some public datasets
        "customer_name",
        "customername",
        "customer name",
        "client_name",
        "clientname",
        "client name",
        "user_name",
        "username",
        "user name",
        "account_name",
        "accountname",
        "account name",
        "member_name",
        "membername",
        "member name",
        "buyer_name",
        "buyername",
        "buyer name",
        "shopper_name",
        "shoppername",
        "shopper name",

        # Email/contact identifiers
        "customer_email",
        "customeremail",
        "customer email",
        "client_email",
        "clientemail",
        "client email",
        "user_email",
        "useremail",
        "user email",
        "member_email",
        "memberemail",
        "member email",
        "buyer_email",
        "buyeremail",
        "buyer email",
        "email",
        "email_address",
        "emailaddress",
        "email address",

        # Generic fallback identifiers
        # Keep these near the end because they can be ambiguous.
        "id",
        "identifier",
        "record_id",
        "recordid",
        "record id",
        "entity_id",
        "entityid",
        "entity id",
        "name",
    ],

    "order_id": [
        # Order identifiers
        "order_id",
        "orderid",
        "order id",
        "order_no",
        "orderno",
        "order no",
        "order_number",
        "ordernumber",
        "order number",
        "order_code",
        "ordercode",
        "order code",

        # Transaction identifiers
        "transaction_id",
        "transactionid",
        "transaction id",
        "transaction_no",
        "transactionno",
        "transaction no",
        "transaction_number",
        "transactionnumber",
        "transaction number",
        "transaction_code",
        "transactioncode",
        "transaction code",

        # Invoice identifiers
        "invoice_no",
        "invoiceno",
        "invoice no",
        "invoice_number",
        "invoicenumber",
        "invoice number",
        "invoice_id",
        "invoiceid",
        "invoice id",
        "invoice",

        # Purchase / receipt identifiers
        "purchase_id",
        "purchaseid",
        "purchase id",
        "purchase_no",
        "purchaseno",
        "purchase no",
        "purchase_number",
        "purchasenumber",
        "purchase number",
        "receipt_id",
        "receiptid",
        "receipt id",
        "receipt_no",
        "receiptno",
        "receipt no",
        "receipt_number",
        "receiptnumber",
        "receipt number",

        # Generic fallback
        "sales_id",
        "salesid",
        "sales id",
        "sale_id",
        "saleid",
        "sale id",
        "id",
    ],

    "order_date": [
        # Order dates
        "order_date",
        "orderdate",
        "order date",
        "order_datetime",
        "orderdatetime",
        "order datetime",
        "order_time",
        "ordertime",
        "order time",

        # Transaction dates
        "transaction_date",
        "transactiondate",
        "transaction date",
        "transaction_datetime",
        "transactiondatetime",
        "transaction datetime",
        "transaction_time",
        "transactiontime",
        "transaction time",

        # Purchase dates
        "purchase_date",
        "purchasedate",
        "purchase date",
        "purchase_datetime",
        "purchasedatetime",
        "purchase datetime",
        "purchase_time",
        "purchasetime",
        "purchase time",

        # Invoice dates
        "invoice_date",
        "invoicedate",
        "invoice date",
        "invoice_datetime",
        "invoicedatetime",
        "invoice datetime",

        # Generic dates
        "date",
        "datetime",
        "timestamp",
        "time",
        "created_at",
        "createdat",
        "created at",
        "created_date",
        "createddate",
        "created date",
        "event_date",
        "eventdate",
        "event date",
    ],

    "quantity": [
        "quantity",
        "qty",
        "units",
        "unit_count",
        "unitcount",
        "unit count",
        "items",
        "item_count",
        "itemcount",
        "item count",
        "number_of_items",
        "numberofitems",
        "number of items",
        "num_items",
        "numitems",
        "num items",
        "count",
        "product_quantity",
        "productquantity",
        "product quantity",
        "purchase_quantity",
        "purchasequantity",
        "purchase quantity",
        "order_quantity",
        "orderquantity",
        "order quantity",
    ],

    "unit_price": [
        "unit_price",
        "unitprice",
        "unit price",
        "price",
        "price_per_unit",
        "priceperunit",
        "price per unit",
        "product_price",
        "productprice",
        "product price",
        "item_price",
        "itemprice",
        "item price",
        "unit_cost",
        "unitcost",
        "unit cost",
        "cost_per_unit",
        "costperunit",
        "cost per unit",
        "sales_price",
        "salesprice",
        "sales price",
        "selling_price",
        "sellingprice",
        "selling price",
        "purchase_price",
        "purchaseprice",
        "purchase price",
    ],

    "total_amount": [
        # Generic amount / revenue
        "total_amount",
        "totalamount",
        "total amount",
        "amount",
        "sales",
        "revenue",
        "value",
        "total_value",
        "totalvalue",
        "total value",
        "total_price",
        "totalprice",
        "total price",

        # Spend / purchase amount
        "total_spend",
        "totalspend",
        "total spend",
        "spend",
        "spending",
        "purchase_amount",
        "purchaseamount",
        "purchase amount",
        "purchase_amount_usd",
        "purchaseamountusd",
        "purchase amount usd",
        "total_purchase_amount",
        "totalpurchaseamount",
        "total purchase amount",

        # Transaction amount
        "transaction_amount",
        "transactionamount",
        "transaction amount",
        "transaction_value",
        "transactionvalue",
        "transaction value",

        # Order / basket amount
        "order_value",
        "ordervalue",
        "order value",
        "order_amount",
        "orderamount",
        "order amount",
        "basket_value",
        "basketvalue",
        "basket value",
        "basket_amount",
        "basketamount",
        "basket amount",
        "cart_value",
        "cartvalue",
        "cart value",
        "cart_amount",
        "cartamount",
        "cart amount",

        # Financial alternatives
        "gross_sales",
        "grosssales",
        "gross sales",
        "net_sales",
        "netsales",
        "net sales",
        "subtotal",
        "grand_total",
        "grandtotal",
        "grand total",
        "payment_amount",
        "paymentamount",
        "payment amount",
        "paid_amount",
        "paidamount",
        "paid amount",
    ],

    "product_id": [
        # Product identifiers
        "product_id",
        "productid",
        "product id",
        "product_code",
        "productcode",
        "product code",
        "product_no",
        "productno",
        "product no",
        "product_number",
        "productnumber",
        "product number",

        # Product names / information
        "product",
        "product_name",
        "productname",
        "product name",
        "productinformation",
        "product_information",
        "product information",

        # SKU / item identifiers
        "sku",
        "stock_code",
        "stockcode",
        "stock code",
        "item_id",
        "itemid",
        "item id",
        "item_code",
        "itemcode",
        "item code",
        "item_name",
        "itemname",
        "item name",
        "item_purchased",
        "itempurchased",
        "item purchased",

        # Category identifiers
        "category",
        "product_category",
        "productcategory",
        "product category",
        "item_category",
        "itemcategory",
        "item category",
        "department",
        "department_name",
        "departmentname",
        "department name",
        "subcategory",
        "sub_category",
        "subcategory",
        "sub category",
    ],

    "country": [
        # Country/location
        "country",
        "country_name",
        "countryname",
        "country name",
        "location",
        "customer_location",
        "customerlocation",
        "customer location",
        "shipping_country",
        "shippingcountry",
        "shipping country",
        "billing_country",
        "billingcountry",
        "billing country",

        # City/region/state
        "city",
        "town",
        "region",
        "state",
        "province",
        "area",
        "market",
        "territory",
        "zone",

        # Address-like generic fields
        "address_country",
        "addresscountry",
        "address country",
        "geo",
        "geography",
        "locale",
    ],
}


PROFILE_ALIASES = {
    "customer_id": COLUMN_ALIASES["customer_id"],

    "recency": [
        "recency",
        "recency_days",
        "recencydays",
        "recency days",
        "days_since_last_purchase",
        "dayssincelastpurchase",
        "days since last purchase",
        "days_since_last_order",
        "dayssincelastorder",
        "days since last order",
        "days_since_last_transaction",
        "dayssincelasttransaction",
        "days since last transaction",
        "days_since_last",
        "dayssincelast",
        "days since last",
        "last_purchase_days",
        "lastpurchasedays",
        "last purchase days",
        "last_order_days",
        "lastorderdays",
        "last order days",
        "last_transaction_days",
        "lasttransactiondays",
        "last transaction days",
        "inactive_days",
        "inactivedays",
        "inactive days",
    ],

    "frequency": [
        "frequency",
        "purchase_frequency",
        "purchasefrequency",
        "purchase frequency",
        "order_frequency",
        "orderfrequency",
        "order frequency",
        "transaction_frequency",
        "transactionfrequency",
        "transaction frequency",
        "items_purchased",
        "itemspurchased",
        "items purchased",
        "previous_purchases",
        "previouspurchases",
        "previous purchases",
        "number_of_orders",
        "numberoforders",
        "number of orders",
        "orders",
        "order_count",
        "ordercount",
        "order count",
        "purchase_count",
        "purchasecount",
        "purchase count",
        "transaction_count",
        "transactioncount",
        "transaction count",
        "transactions",
        "visits",
        "visit_count",
        "visitcount",
        "visit count",
    ],

    "monetary": COLUMN_ALIASES["total_amount"],

    "avg_order_value": [
        "avg_order_value",
        "avgordervalue",
        "avg order value",
        "average_order_value",
        "averageordervalue",
        "average order value",
        "aov",
        "avg_purchase_value",
        "avgpurchasevalue",
        "avg purchase value",
        "average_purchase_value",
        "averagepurchasevalue",
        "average purchase value",
        "avg_transaction_value",
        "avgtransactionvalue",
        "avg transaction value",
        "average_transaction_value",
        "averagetransactionvalue",
        "average transaction value",
        "avg_basket_value",
        "avgbasketvalue",
        "avg basket value",
    ],

    "unique_products": [
        "unique_products",
        "uniqueproducts",
        "unique products",
        "unique_items",
        "uniqueitems",
        "unique items",
        "unique_product_count",
        "uniqueproductcount",
        "unique product count",
        "product_count",
        "productcount",
        "product count",
        "item_count",
        "itemcount",
        "item count",
        "category_count",
        "categorycount",
        "category count",
        "categories_count",
        "categoriescount",
        "categories count",
        "distinct_products",
        "distinctproducts",
        "distinct products",
        "distinct_items",
        "distinctitems",
        "distinct items",
        "items_purchased",
        "itemspurchased",
        "items purchased",
    ],

    "total_quantity": [
        "total_quantity",
        "totalquantity",
        "total quantity",
        "quantity",
        "qty",
        "units",
        "total_units",
        "totalunits",
        "total units",
        "total_items",
        "totalitems",
        "total items",
        "items_purchased",
        "itemspurchased",
        "items purchased",
        "previous_purchases",
        "previouspurchases",
        "previous purchases",
        "quantity_sum",
        "quantitysum",
        "quantity sum",
        "units_sum",
        "unitssum",
        "units sum",
    ],

    "customer_lifetime_days": [
        "customer_lifetime_days",
        "customerlifetimedays",
        "customer lifetime days",
        "lifetime_days",
        "lifetimedays",
        "lifetime days",
        "tenure_days",
        "tenuredays",
        "tenure days",
        "tenure",
        "customer_age_days",
        "customeragedays",
        "customer age days",
        "days_as_customer",
        "daysascustomer",
        "days as customer",
        "membership_days",
        "membershipdays",
        "membership days",
        "account_age_days",
        "accountagedays",
        "account age days",
    ],
}
# ============================================================
# Normalization / mapping helpers
# ============================================================

def normalize_column_name(col):
    normalized = str(col).strip().lower()
    normalized = re.sub(r"[\s-]+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.strip("_")


def _normalized_column_lookup(df):
    lookup = {}
    for col in df.columns:
        normalized = normalize_column_name(col)
        if normalized not in lookup:
            lookup[normalized] = col
    return lookup


def _suggest_mapping(df, aliases):
    normalized_columns = _normalized_column_lookup(df)
    mapping = {}

    for field, field_aliases in aliases.items():
        mapping[field] = None

        for alias in field_aliases:
            normalized_alias = normalize_column_name(alias)

            if normalized_alias in normalized_columns:
                mapping[field] = normalized_columns[normalized_alias]
                break

    return mapping


def suggest_column_mapping(df):
    return _suggest_mapping(df, COLUMN_ALIASES)


def suggest_profile_mapping(df):
    return _suggest_mapping(df, PROFILE_ALIASES)


def _clean_mapping(mapping):
    return {
        field: (column if column and column != "Not selected" else None)
        for field, column in mapping.items()
    }


def _has_customer_features(df, required_features):
    normalized_columns = set(normalize_column_name(col) for col in df.columns)
    return all(normalize_column_name(col) in normalized_columns for col in required_features)


# ============================================================
# Upload type detection
# ============================================================

def detect_upload_type(df, required_features):
    if _has_customer_features(df, required_features):
        return "customer_features"

    transaction_mapping = suggest_column_mapping(df)

    has_transaction_core = bool(
        transaction_mapping.get("customer_id") and transaction_mapping.get("order_date")
    )

    has_transaction_revenue = bool(transaction_mapping.get("total_amount")) or bool(
        transaction_mapping.get("quantity") and transaction_mapping.get("unit_price")
    )

    if has_transaction_core and has_transaction_revenue:
        return "transaction_data"

    profile_mapping = suggest_profile_mapping(df)

    if profile_mapping.get("customer_id") and profile_mapping.get("monetary"):
        return "customer_profile"

    return "unknown"


# ============================================================
# Transaction feature generation
# ============================================================

def prepare_transaction_mapping_and_df(uploaded_df, mapping):
    mapping = _clean_mapping(mapping)
    work_df = uploaded_df.copy()

    if not mapping.get("order_id"):
        generated_col = "__generated_order_id__"
        work_df[generated_col] = range(1, len(work_df) + 1)
        mapping["order_id"] = generated_col

    return work_df, mapping


def _validate_transaction_mapping(mapping):
    missing_core = [
        field for field in ["customer_id", "order_date"] if not mapping.get(field)
    ]

    has_revenue = bool(mapping.get("total_amount")) or bool(
        mapping.get("quantity") and mapping.get("unit_price")
    )

    if missing_core or not has_revenue:
        raise ValueError(
            "Please map customer_id, order_date, and either total_amount "
            "or quantity + unit_price. If your dataset does not have a numeric "
            "customer ID, you can use a stable identifier such as user name, email, "
            "account name, or customer name."
        )


def build_customer_features_from_transactions(df, mapping):
    mapping = _clean_mapping(mapping)
    _validate_transaction_mapping(mapping)

    work_df = pd.DataFrame()

    for field in TRANSACTION_FIELDS:
        source_col = mapping.get(field)
        if source_col:
            work_df[field] = df[source_col]

    normalized_columns = _normalized_column_lookup(df)

    for optional_col in ["location", "source"]:
        source_col = normalized_columns.get(optional_col)
        if source_col and optional_col not in work_df.columns:
            work_df[optional_col] = df[source_col]

    work_df = work_df.dropna(subset=["customer_id", "order_date"]).copy()
    work_df["customer_id"] = work_df["customer_id"].astype(str).str.strip()
    work_df = work_df[work_df["customer_id"] != ""]

    if "order_id" not in work_df.columns:
        work_df["order_id"] = range(1, len(work_df) + 1)
    else:
        work_df["order_id"] = work_df["order_id"].astype(str).str.strip()
        work_df = work_df[work_df["order_id"] != ""]

        # Online Retail style cancellation invoices often start with C.
        work_df = work_df[~work_df["order_id"].str.upper().str.startswith("C")]

    work_df["order_date"] = pd.to_datetime(work_df["order_date"], errors="coerce")
    work_df = work_df.dropna(subset=["order_date"])

    if "quantity" in work_df.columns:
        work_df["quantity"] = pd.to_numeric(work_df["quantity"], errors="coerce")
        work_df = work_df[work_df["quantity"] > 0]

    if "unit_price" in work_df.columns:
        work_df["unit_price"] = pd.to_numeric(work_df["unit_price"], errors="coerce")
        work_df = work_df[work_df["unit_price"] > 0]

    if "total_amount" in work_df.columns:
        work_df["transaction_amount"] = pd.to_numeric(
            work_df["total_amount"], errors="coerce"
        )
    else:
        work_df["transaction_amount"] = work_df["quantity"] * work_df["unit_price"]

    work_df = work_df[work_df["transaction_amount"] > 0]

    if work_df.empty:
        raise ValueError("No valid transaction rows found after cleaning.")

    reference_date = work_df["order_date"].max() + pd.Timedelta(days=1)

    aggregations = {
        "order_date": ["min", "max"],
        "order_id": pd.Series.nunique,
        "transaction_amount": "sum",
    }

    if "product_id" in work_df.columns:
        aggregations["product_id"] = pd.Series.nunique

    if "quantity" in work_df.columns:
        aggregations["quantity"] = "sum"

    customer_features = work_df.groupby("customer_id").agg(aggregations)

    customer_features.columns = [
        "_".join(col).strip("_") for col in customer_features.columns.to_flat_index()
    ]

    customer_features = customer_features.reset_index()

    customer_features["recency"] = (
        reference_date - customer_features["order_date_max"]
    ).dt.days

    customer_features["frequency"] = customer_features["order_id_nunique"]
    customer_features["monetary"] = customer_features["transaction_amount_sum"]
    customer_features["avg_order_value"] = (
        customer_features["monetary"] / customer_features["frequency"]
    )

    customer_features["unique_products"] = customer_features.get("product_id_nunique", 1)

    customer_features["total_quantity"] = customer_features.get(
        "quantity_sum",
        customer_features["frequency"],
    )

    customer_features["customer_lifetime_days"] = (
        customer_features["order_date_max"] - customer_features["order_date_min"]
    ).dt.days

    result_df = customer_features[CUSTOMER_FEATURE_FIELDS].copy()

    result_df["__recency_is_default"] = False

    for optional_col in ["country", "location", "source"]:
        if optional_col in work_df.columns:
            values = (
                work_df.groupby("customer_id")[optional_col]
                .agg(
                    lambda items: (
                        items.mode().iloc[0]
                        if not items.mode().empty
                        else items.iloc[0]
                    )
                )
                .reset_index()
            )

            result_df = result_df.merge(values, on="customer_id", how="left")

    return validate_customer_features(result_df, REQUIRED_CLUSTERING_FEATURES)


# ============================================================
# Profile feature generation
# ============================================================

def build_customer_features_from_profile(df, mapping):
    mapping = _clean_mapping(mapping)

    if not mapping.get("customer_id"):
        raise ValueError(
            "Please map customer_id. If your dataset does not have a numeric customer ID, "
            "you can use a stable identifier such as user name, email, account name, "
            "or customer name."
        )

    if not mapping.get("monetary"):
        raise ValueError("Please map monetary / total spend / purchase amount.")

    result_df = pd.DataFrame()
    result_df["customer_id"] = df[mapping["customer_id"]].astype(str).str.strip()

    result_df["recency"] = _numeric_or_default(df, mapping.get("recency"), 0)
    result_df["__recency_is_default"] = not bool(mapping.get("recency"))
    result_df["frequency"] = _numeric_or_default(df, mapping.get("frequency"), 1)
    result_df["monetary"] = pd.to_numeric(df[mapping["monetary"]], errors="coerce")

    result_df["frequency"] = result_df["frequency"].fillna(1)
    result_df.loc[result_df["frequency"] <= 0, "frequency"] = 1

    result_df["avg_order_value"] = _numeric_or_default(
        df,
        mapping.get("avg_order_value"),
        result_df["monetary"] / result_df["frequency"],
    )

    result_df["unique_products"] = _numeric_or_default(
        df,
        mapping.get("unique_products"),
        1,
    )

    result_df["total_quantity"] = _numeric_or_default(
        df,
        mapping.get("total_quantity"),
        result_df["frequency"],
    )

    result_df["customer_lifetime_days"] = _numeric_or_default(
        df,
        mapping.get("customer_lifetime_days"),
        0,
    )

    normalized_columns = _normalized_column_lookup(df)

    for optional_col in ["country", "location", "source"]:
        source_col = normalized_columns.get(optional_col)
        if source_col:
            result_df[optional_col] = df[source_col]

    return validate_customer_features(result_df, REQUIRED_CLUSTERING_FEATURES)


def _numeric_or_default(df, source_col, default):
    if source_col:
        return pd.to_numeric(df[source_col], errors="coerce")

    return default


# ============================================================
# Final validation
# ============================================================

def validate_customer_features(feature_df, required_features):
    result_df = feature_df.copy()
    normalized_columns = _normalized_column_lookup(result_df)

    for feature in required_features:
        if feature not in result_df.columns:
            source_col = normalized_columns.get(normalize_column_name(feature))
            if source_col:
                result_df[feature] = result_df[source_col]

    missing_columns = [col for col in required_features if col not in result_df.columns]

    if missing_columns:
        raise ValueError(
            "Missing required customer feature columns: "
            + ", ".join(missing_columns)
        )

    if "customer_id" not in result_df.columns:
        result_df.insert(
            0,
            "customer_id",
            [f"Customer {i + 1}" for i in range(len(result_df))],
        )

    result_df["customer_id"] = result_df["customer_id"].astype(str).str.strip()
    result_df = result_df[result_df["customer_id"] != ""]

    for col in required_features:
        result_df[col] = pd.to_numeric(result_df[col], errors="coerce")

    result_df = result_df.replace([np.inf, -np.inf], np.nan)
    result_df = result_df.dropna(subset=["customer_id", *required_features])

    for col in required_features:
        result_df[col] = result_df[col].clip(lower=0)

    if result_df.empty:
        raise ValueError("No valid customer feature rows found after cleaning.")

    if "__recency_is_default" not in result_df.columns:
        result_df["__recency_is_default"] = False

    ordered_columns = CUSTOMER_FEATURE_FIELDS + [
        col
        for col in ["country", "location", "source"]
        if col in result_df.columns and col not in CUSTOMER_FEATURE_FIELDS
    ]

    other_columns = [col for col in result_df.columns if col not in ordered_columns]

    return result_df[ordered_columns + other_columns].copy()
import html
import io
import re
import zipfile

import plotly.express as px
import streamlit as st

from translations import get_text


PREMIUM_BLUE = "#2563eb"
PREMIUM_TEAL = "#0f766e"
PREMIUM_PALETTE = [
    "#38bdf8",
    "#22c55e",
    "#818cf8",
    "#f59e0b",
    "#14b8a6",
    "#a78bfa",
    "#f97316",
    "#94a3b8",
]


# ============================================================
# Small helpers
# ============================================================

def _t(t):
    return t if t is not None else get_text("en")


def _format_cell(value):
    if value is None:
        return ""

    text = str(value)

    if len(text) > 80:
        text = text[:77] + "..."

    return html.escape(text)

def _safe_filename(text):
    text = str(text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "_", text)
    return text[:80] or "segment"


def render_dark_table(df, max_height=520):
    safe_df = df.copy()

    table_html = [f'<div class="dark-table-wrap" style="max-height: {max_height}px;">']
    table_html.append('<table class="dark-table">')

    table_html.append("<thead><tr>")
    for col in safe_df.columns:
        table_html.append(f"<th>{html.escape(str(col))}</th>")
    table_html.append("</tr></thead>")

    table_html.append("<tbody>")
    for _, row in safe_df.iterrows():
        table_html.append("<tr>")
        for value in row:
            table_html.append(f"<td>{_format_cell(value)}</td>")
        table_html.append("</tr>")
    table_html.append("</tbody>")

    table_html.append("</table></div>")

    st.markdown("".join(table_html), unsafe_allow_html=True)


def render_column_pills(columns):
    pills = "".join(
        f'<span class="column-pill">{html.escape(str(col))}</span>'
        for col in columns
    )

    st.markdown(
        f"""
<div class="column-pill-wrap">
  {pills}
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# Global UI Blocks
# ============================================================

def render_hero(t=None):
    t = _t(t)

    st.markdown(
        f"""
<div class="hero-card">
  <div class="hero-eyebrow">{t["hero_badge"]}</div>
  <h1 class="hero-title">{t["hero_title"]}</h1>
  <p class="hero-subtitle">
    {t["hero_subtitle"]}
  </p>

  <div class="hero-grid">
    <div class="hero-mini-card">
      <div class="hero-mini-label">{t["hero_input_label"]}</div>
      <div class="hero-mini-value">{t["hero_input_value"]}</div>
    </div>
    <div class="hero-mini-card">
      <div class="hero-mini-label">{t["hero_model_label"]}</div>
      <div class="hero-mini-value">{t["hero_model_value"]}</div>
    </div>
    <div class="hero-mini-card">
      <div class="hero-mini-label">{t["hero_output_label"]}</div>
      <div class="hero-mini-value">{t["hero_output_value"]}</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_workflow_steps(t=None):
    t = _t(t)

    st.markdown(
        f"""
<div class="step-grid">
  <div class="step-card">
    <div class="step-number">STEP 01</div>
    <div class="step-title">{t["step_01_title"]}</div>
    <div class="step-copy">{t["step_01_copy"]}</div>
  </div>
  <div class="step-card">
    <div class="step-number">STEP 02</div>
    <div class="step-title">{t["step_02_title"]}</div>
    <div class="step-copy">{t["step_02_copy"]}</div>
  </div>
  <div class="step-card">
    <div class="step-number">STEP 03</div>
    <div class="step-title">{t["step_03_title"]}</div>
    <div class="step-copy">{t["step_03_copy"]}</div>
  </div>
  <div class="step-card">
    <div class="step-number">STEP 04</div>
    <div class="step-title">{t["step_04_title"]}</div>
    <div class="step-copy">{t["step_04_copy"]}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_section_header(title, caption=None, icon=""):
    icon_text = f"{icon} " if icon else ""
    caption_html = f'<div class="section-caption">{caption}</div>' if caption else ""

    st.markdown(
        f"""
<div class="section-card">
  <div class="section-title">{icon_text}{title}</div>
  {caption_html}
</div>
""",
        unsafe_allow_html=True,
    )


def render_supported_formats_expander(location=st, expanded=False, t=None):
    t = _t(t)

    with location.expander("Supported upload formats", expanded=expanded) as expander:
        if t["language"] == "Dil":
            expander.markdown(
                """
### 1. Demo veri seti

Uygulamayı kendi dosyanı yüklemeden önce örnek veriyle incelemek için kullan.

### 2. Müşteri özellikleri CSV

Her satır zaten bir müşteriyi temsil ediyorsa ve şu kolonları içeriyorsa kullan:

- `recency`
- `frequency`
- `monetary`
- `avg_order_value`
- `unique_products`
- `total_quantity`
- `customer_lifetime_days`

### 3. İşlem / sipariş CSV

Her satır bir sipariş, fatura veya ürün satırıysa kullan.

Gerekli alanlar:

- müşteri kolonu
- tarih kolonu
- toplam tutar **veya** quantity + unit price

Order ID önerilir ama zorunlu değildir. Yoksa her satır bir işlem gibi değerlendirilebilir.

### 4. Müşteri profil CSV

Her satır zaten tek bir müşteriyi temsil ediyorsa kullan.

Faydalı kolonlar:

- toplam harcama
- satın alınan ürün sayısı
- son satın almadan geçen gün
- önceki satın alma sayısı

Eksik opsiyonel alanlar güvenli varsayılanlarla tamamlanabilir.
"""
            )
        else:
            expander.markdown(
                """
### 1. Demo dataset

Use the built-in example data to preview the app before uploading your own file.

### 2. Customer feature CSV

Use this when each row already represents one customer and includes:

- `recency`
- `frequency`
- `monetary`
- `avg_order_value`
- `unique_products`
- `total_quantity`
- `customer_lifetime_days`

### 3. Transaction / order CSV

Use this when each row is an order, invoice, or purchase line.

Required:

- customer column
- date column
- total amount **or** quantity + unit price

Order ID is recommended but optional. If missing, each row can be treated as one transaction.

### 4. Customer profile CSV

Use this only if each row already represents one customer.

Useful columns:

- total spend
- items purchased
- days since last purchase
- previous purchases

Missing optional features can be estimated with safe defaults.
"""
            )


# ============================================================
# Upload / Mapping UI
# ============================================================

def render_upload_preview(uploaded_df, t=None):
    t = _t(t)

    with st.expander(t["preview_uploaded_data"], expanded=False):
        max_rows = min(len(uploaded_df), 200)

        if max_rows >= 5:
            preview_rows = st.slider(
                t["preview_rows"],
                min_value=5,
                max_value=max_rows,
                value=min(20, max_rows),
                step=5,
                help=(
                    "Önizleme tablosunda kaç satır gösterileceğini değiştir."
                    if t["language"] == "Dil"
                    else "Change how many uploaded rows are shown in the preview table."
                ),
            )
        else:
            preview_rows = max_rows

        render_dark_table(uploaded_df.head(preview_rows), max_height=420)

        with st.expander(t["column_list"], expanded=False):
            render_column_pills(uploaded_df.columns)


def render_detection_message(upload_type_label, t=None):
    t = _t(t)

    if t["language"] == "Dil":
        body = (
            "Devam etmeden önce algılamayı kontrol et. Eğer dosya yapısı yanlış görünüyorsa, "
            "aşağıdaki eşleştirme alanlarıyla uygulamayı yönlendirebilirsin."
        )
    else:
        body = (
            "Review this detection before continuing. If the structure looks wrong, "
            "use the mapping controls below to guide the app."
        )

    st.markdown(
        f"""
<div class="section-card">
  <div class="section-title">{t["detected_upload_type"]}</div>
  <div class="section-caption">
    <strong>{html.escape(str(upload_type_label))}</strong><br>
    {body}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_mapping_selectboxes(fields, suggested_mapping, uploaded_df, key_prefix):
    mapping = {}
    options = ["Not selected"] + list(uploaded_df.columns)

    left, right = st.columns(2)

    for idx, field in enumerate(fields):
        container = left if idx % 2 == 0 else right

        with container:
            suggested_column = suggested_mapping.get(field)
            default_index = options.index(suggested_column) if suggested_column in options else 0

            mapping[field] = st.selectbox(
                field,
                options=options,
                index=default_index,
                key=f"{key_prefix}_{field}",
                help=f"Select the uploaded CSV column that should be used as {field}.",
            )

    return mapping


def render_transaction_guidance(t=None):
    t = _t(t)
    st.info(t["transaction_guidance"])


def render_profile_guidance(t=None):
    t = _t(t)
    st.info(t["profile_guidance"])


# ============================================================
# Metrics / Tables / Charts
# ============================================================

def render_kpi_cards(df, t=None):
    t = _t(t)

    total_customers = df["customer_id"].nunique() if "customer_id" in df.columns else len(df)
    total_revenue = df["monetary"].sum()
    avg_monetary = df["monetary"].mean()
    avg_recency = df["recency"].mean()

    if t["language"] == "Dil":
        values = [
            ("Toplam müşteri", f"{total_customers:,}"),
            ("Toplam gelir", f"${total_revenue:,.0f}"),
            ("Ortalama monetary", f"${avg_monetary:,.0f}"),
            ("Ortalama recency", f"{avg_recency:.0f} gün"),
        ]
    else:
        values = [
            ("Total Customers", f"{total_customers:,}"),
            ("Total Revenue", f"${total_revenue:,.0f}"),
            ("Avg Monetary", f"${avg_monetary:,.0f}"),
            ("Avg Recency", f"{avg_recency:.0f} days"),
        ]

    cols = st.columns(4)

    for col, (label, value) in zip(cols, values):
        col.markdown(
            f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_cluster_setup(scores_df, recommendation, t=None):
    t = _t(t)

    render_section_header(
        t["clustering_setup"],
        t["clustering_setup_caption"],
        icon="🧭",
    )

    min_k = int(scores_df["k"].min())
    max_k = int(scores_df["k"].max())
    default_k = int(recommendation["business_recommended_k"])

    selected_k = st.slider(
        t["selected_clusters"],
        min_value=min_k,
        max_value=max_k,
        value=default_k,
        step=1,
        key="selected_cluster_count",
        help=(
            "Daha genel veya daha detaylı müşteri grupları istiyorsan öneriyi değiştirebilirsin."
            if t["language"] == "Dil"
            else "You can override the recommendation if you want broader or more detailed customer groups."
        ),
    )

    active_k_label = t["active_selected_k"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t["technical_best_k"], recommendation["technical_best_k"])
    col2.metric(t["business_friendly_k"], recommendation["business_recommended_k"])
    col3.metric(active_k_label, selected_k)
    col4.metric(t["best_silhouette"], f"{recommendation['best_score']:.3f}")

    if selected_k != int(recommendation["business_recommended_k"]):
        st.info(
            t["active_k_info"].format(
                recommended_k=recommendation["business_recommended_k"],
                selected_k=selected_k,
            )
        )

    return selected_k


def render_silhouette_table(scores_df, t=None):
    t = _t(t)

    with st.expander(t["silhouette_details"], expanded=False):
        st.caption(t["silhouette_caption"])

        display_df = scores_df.copy()

        visible_columns = [
            "k",
            "inertia",
            "silhouette_score",
            "min_cluster_size",
            "min_cluster_share",
        ]

        display_df = display_df[[col for col in visible_columns if col in display_df.columns]]

        display_df["inertia"] = display_df["inertia"].map(lambda x: f"{x:,.2f}")
        display_df["silhouette_score"] = display_df["silhouette_score"].map(lambda x: f"{x:.3f}")

        if "min_cluster_share" in display_df.columns:
            display_df["min_cluster_share"] = display_df["min_cluster_share"].map(lambda x: f"{x:.1%}")

        render_dark_table(display_df, max_height=360)


def render_cluster_profile(cluster_profile, title=None, t=None):
    t = _t(t)

    if title is None:
        title = t["cluster_profile_before"]

    st.subheader(title)
    st.caption(t["cluster_profile_caption"])

    display_df = cluster_profile.copy()

    money_cols = ["avg_monetary", "avg_order_value", "total_revenue"]
    pct_cols = ["customer_share_pct", "revenue_share_pct"]

    for col in money_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].map(lambda x: f"${x:,.0f}")

    for col in pct_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].map(lambda x: f"{x:.1f}%")

    for col in [
        "avg_recency",
        "avg_frequency",
        "avg_unique_products",
        "avg_total_quantity",
        "avg_lifetime_days",
    ]:
        if col in display_df.columns:
            display_df[col] = display_df[col].map(lambda x: f"{x:.2f}")

    render_dark_table(display_df, max_height=360)

def render_segment_size_warnings(cluster_profile, t=None):
    t = _t(t)

    if "size_warning_level" not in cluster_profile.columns:
        return

    warning_rows = cluster_profile[
        cluster_profile["size_warning_level"].isin(
            ["very_small", "small", "dominant"]
        )
    ]

    if warning_rows.empty:
        return

    st.warning(t["segment_size_warning_title"])

    for _, row in warning_rows.sort_values("ml_cluster").iterrows():
        cluster_id = int(row["ml_cluster"])
        share = float(row["customer_share_pct"])
        warning_level = row["size_warning_level"]

        if warning_level == "very_small":
            message_template = t["segment_size_very_small"]
        elif warning_level == "small":
            message_template = t["segment_size_small"]
        else:
            message_template = t["segment_size_dominant"]

        st.caption(
            message_template.format(
                cluster_id=cluster_id,
                share=share,
            )
        )

def render_segment_insight_cards(cluster_profile, t=None):
    t = _t(t)

    if "segment_drivers" not in cluster_profile.columns:
        return

    render_section_header(
        t["segment_insights_title"],
        t["segment_insights_caption"],
        icon="💡",
    )

    for _, row in cluster_profile.sort_values("ml_cluster").iterrows():
        cluster_id = int(row["ml_cluster"])
        segment_name = row.get("suggested_segment", f"Cluster {cluster_id}")
        drivers = row.get("segment_drivers", [])

        if not isinstance(drivers, list):
            drivers = []

        driver_items = ""

        for driver in drivers:
            explanation = driver.get("explanation", "")
            pct_diff = float(driver.get("pct_diff", 0))

            if pct_diff > 0:
                direction_symbol = "▲"
            elif pct_diff < 0:
                direction_symbol = "▼"
            else:
                direction_symbol = "●"

            driver_items += f"""
<li>
  <span class="insight-driver-symbol">{direction_symbol}</span>
  <span>{html.escape(str(explanation))}</span>
</li>
"""

        if not driver_items:
            driver_items = """
<li>
  <span class="insight-driver-symbol">●</span>
  <span>No strong segment driver was detected.</span>
</li>
"""

        recency_note = ""

        if bool(row.get("recency_is_default", False)):
            recency_note = f"""
<div class="insight-note">
  {html.escape(str(t["recency_not_available_note"]))}
</div>
"""

        recommended_action = row.get("recommended_action", "")

        action_html = ""

        if recommended_action:
            action_html = (
                '<div class="insight-action-box">'
                f'<div class="insight-action-label">{html.escape(str(t["recommended_action_label"]))}</div>'
                f'<div class="insight-action-text">{html.escape(str(recommended_action))}</div>'
                '</div>'
            )

        st.markdown(
            f"""
<div class="segment-insight-card">
  <div class="segment-insight-header">
    <div class="segment-insight-kicker">Cluster {cluster_id}</div>
    <div class="segment-insight-title">{html.escape(str(segment_name))}</div>
  </div>

  <div class="segment-insight-label">{html.escape(str(t["segment_drivers_label"]))}</div>

  <ul class="segment-insight-list">
    {driver_items}
  </ul>

  {recency_note}
  {action_html}
</div>
""",
            unsafe_allow_html=True,
        )

def render_segment_charts(cluster_profile, t=None):
    t = _t(t)

    if cluster_profile.empty:
        return

    render_section_header(
        t["segment_charts_title"],
        t["segment_charts_caption"],
        icon="📊",
    )

    chart_df = cluster_profile.copy()

    # Prefer final user-facing segment names if available.
    if "ml_segment" in chart_df.columns:
        chart_df["segment_name"] = chart_df["ml_segment"]
    elif "suggested_segment" in chart_df.columns:
        chart_df["segment_name"] = chart_df["suggested_segment"]
    else:
        chart_df["segment_name"] = chart_df["ml_cluster"].map(
            lambda cluster_id: f"Cluster {int(cluster_id)}"
        )
    # Safety fallback:
    # If two clusters have the same visible segment name, make chart labels unique.
    if chart_df["segment_name"].duplicated().any():
        chart_df["segment_name"] = chart_df.apply(
            lambda row: f"{row['segment_name']} · Cluster {int(row['ml_cluster'])}",
            axis=1,
        )

    chart_df = chart_df.sort_values("customers", ascending=False).copy()

    color_map = {
        segment_name: SEGMENT_CHART_COLOR_SEQUENCE[i % len(SEGMENT_CHART_COLOR_SEQUENCE)]
        for i, segment_name in enumerate(chart_df["segment_name"].tolist())
    }

    col_left, col_right = st.columns(2)

    with col_left:
        fig_customers = px.bar(
            chart_df,
            x="customers",
            y="segment_name",
            orientation="h",
            title=t["chart_customers_by_segment"],
            text="customers",
            color="segment_name",
            color_discrete_map=color_map,
        )

        fig_customers.update_traces(
            textposition="auto",
            insidetextanchor="end",
            textfont=dict(color="#f8fafc", size=12),
            marker_line_width=0,
        )

        fig_customers.update_layout(
            height=390,
            title_font=dict(color="#f8fafc", size=16),
            yaxis_title="",
            xaxis_title=t["chart_customers_axis"],
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(2,6,23,0.32)",
            font_color="#e5e7eb",
            margin=dict(l=20, r=70, t=60, b=20),
        )

        fig_customers.update_xaxes(gridcolor="rgba(148, 163, 184, 0.16)")
        fig_customers.update_yaxes(gridcolor="rgba(148, 163, 184, 0.16)")

        st.plotly_chart(fig_customers, use_container_width=True)

    with col_right:
        revenue_df = chart_df.sort_values("revenue_share_pct", ascending=False).copy()

        fig_revenue = px.bar(
            revenue_df,
            x="segment_name",
            y="revenue_share_pct",
            title=t["chart_revenue_share_by_segment"],
            text=revenue_df["revenue_share_pct"].map(lambda value: f"{value:.1f}%"),
            color="segment_name",
            color_discrete_map=color_map,
        )

        fig_revenue.update_traces(
            textposition="outside",
            marker_line_width=0,
        )

        fig_revenue.update_layout(
            height=390,
            title_font=dict(color="#f8fafc", size=16),
            xaxis_title="",
            yaxis_title=t["chart_revenue_share_axis"],
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(2,6,23,0.32)",
            font_color="#e5e7eb",
            margin=dict(l=20, r=20, t=60, b=80),
        )

        fig_revenue.update_xaxes(
            gridcolor="rgba(148, 163, 184, 0.16)",
            tickangle=-20,
        )
        fig_revenue.update_yaxes(
            gridcolor="rgba(148, 163, 184, 0.16)",
            ticksuffix="%",
        )

        st.plotly_chart(fig_revenue, use_container_width=True)

    monetary_df = chart_df.sort_values("avg_monetary", ascending=False).copy()

    fig_monetary = px.bar(
        monetary_df,
        x="segment_name",
        y="avg_monetary",
        title=t["chart_avg_monetary_by_segment"],
        text=monetary_df["avg_monetary"].map(lambda value: f"${value:,.0f}"),
        color="segment_name",
        color_discrete_map=color_map,
    )

    fig_monetary.update_traces(
        textposition="outside",
        marker_line_width=0,
    )

    fig_monetary.update_layout(
        height=420,
        title_font=dict(color="#f8fafc", size=16),
        xaxis_title="",
        yaxis_title=t["chart_avg_monetary_axis"],
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2,6,23,0.32)",
        font_color="#e5e7eb",
        margin=dict(l=20, r=20, t=60, b=90),
    )

    fig_monetary.update_xaxes(
        gridcolor="rgba(148, 163, 184, 0.16)",
        tickangle=-20,
    )
    fig_monetary.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.16)",
    )

    st.plotly_chart(fig_monetary, use_container_width=True)


def render_cluster_label_inputs(cluster_profile, t=None):
    t = _t(t)

    st.subheader(t["name_clusters"])
    st.caption(t["name_clusters_caption"])

    label_mapping = {}

    for _, row in cluster_profile.sort_values("ml_cluster").iterrows():
        cluster_id = int(row["ml_cluster"])

        customers_label = "müşteri" if t["language"] == "Dil" else "customers"
        avg_monetary_label = "Ort. monetary" if t["language"] == "Dil" else "Avg monetary"
        avg_frequency_label = "Ort. frequency" if t["language"] == "Dil" else "Avg frequency"
        avg_recency_label = "Ort. recency" if t["language"] == "Dil" else "Avg recency"
        revenue_share_label = "Gelir payı" if t["language"] == "Dil" else "Revenue share"

        st.markdown(
            f"""
    <div class="cluster-name-card">
      <div class="cluster-name-title">Cluster {cluster_id}</div>
      <div class="cluster-name-meta">
        {int(row["customers"]):,} {customers_label} ·
        {avg_monetary_label} ${row["avg_monetary"]:,.0f} ·
        {avg_frequency_label} {row["avg_frequency"]:.2f} ·
        {avg_recency_label} {row["avg_recency"]:.1f} ·
        {revenue_share_label} {row["revenue_share_pct"]:.1f}%
      </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

        suggested_segment = row.get("suggested_segment", f"Cluster {cluster_id}")

        st.markdown(
            f"""
    <div class="cluster-name-card">
      <div class="cluster-name-title">
        {html.escape(str(t["suggested_segment_label"]))}: {html.escape(str(suggested_segment))}
      </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

        label_mapping[cluster_id] = st.text_input(
            f"{t['label_for_cluster']} {cluster_id}",
            value=str(suggested_segment),
            key=f"cluster_label_{cluster_id}",
        )

    st.success(t["custom_labels_success"])
    return label_mapping


CLUSTER_COLOR_SEQUENCE = [
    "#1D4ED8",  # deep blue
    "#0F766E",  # deep teal
    "#D97706",  # burnt amber
    "#7C3AED",  # deep violet
    "#0369A1",  # ocean blue
    "#BE123C",  # deep rose
    "#A16207",  # muted gold
    "#475569",  # slate
]
SEGMENT_CHART_COLOR_SEQUENCE = [
    "#1D4ED8",  # deep blue
    "#0F766E",  # deep teal
    "#D97706",  # burnt amber
    "#7C3AED",  # deep violet
    "#0369A1",  # ocean blue
    "#BE123C",  # deep rose
    "#A16207",  # muted gold
    "#475569",  # slate
]


def render_pca_scatter(pca_df, t=None, selected_k=None):
    if t is None:
        t = {}

    title_base = t.get("pca_title", "Customer clusters PCA view")
    title = title_base if selected_k is None else f"{title_base} · aktif k = {selected_k}"

    subtitle = t.get(
        "pca_caption",
        "This 2D projection is directional only; cluster separation should be interpreted comparatively."
    )

    st.subheader(title)
    st.caption(subtitle)

    cluster_values = sorted(pca_df["ml_segment"].dropna().unique().tolist())

    color_map = {
        cluster_name: CLUSTER_COLOR_SEQUENCE[i % len(CLUSTER_COLOR_SEQUENCE)]
        for i, cluster_name in enumerate(cluster_values)
    }

    fig = px.scatter(
        pca_df,
        x="pca_1",
        y="pca_2",
        color="ml_segment",
        color_discrete_map=color_map,
        hover_data=[
            col for col in ["customer_id", "monetary", "frequency", "recency"]
            if col in pca_df.columns
        ],
        opacity=0.88,
    )

    fig.update_traces(
        marker=dict(
            size=7,
            line=dict(width=0.6, color="rgba(255,255,255,0.18)")
        )
    )

    fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#081225",
        font=dict(color="#E6EEF8"),
        legend_title_text=t.get("segment_legend", "Segment"),
        legend=dict(
            bgcolor="rgba(8,18,37,0.72)",
            bordercolor="rgba(148,163,184,0.20)",
            borderwidth=1,
            font=dict(color="#E6EEF8", size=12),
            orientation="v",
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            title="pca_1",
            gridcolor="rgba(148,163,184,0.12)",
            zerolinecolor="rgba(148,163,184,0.18)",
        ),
        yaxis=dict(
            title="pca_2",
            gridcolor="rgba(148,163,184,0.12)",
            zerolinecolor="rgba(148,163,184,0.18)",
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_segmented_customer_table(df, t=None):
    t = _t(t)

    st.subheader(t["segmented_customer_data"])
    st.caption(t["segmented_customer_caption"])

    segment_options = sorted(df["ml_segment"].dropna().unique())

    selected_segments = st.multiselect(
        t["filter_by_segment"],
        options=segment_options,
        default=segment_options,
    )

    filtered_df = df[df["ml_segment"].isin(selected_segments)]

    max_rows = min(len(filtered_df), 500)

    if max_rows >= 5:
        preview_rows = st.slider(
            t["rows_shown"],
            min_value=5,
            max_value=max_rows,
            value=min(50, max_rows),
            step=5,
            key="segmented_table_rows",
        )
        render_dark_table(filtered_df.head(preview_rows), max_height=520)
    else:
        render_dark_table(filtered_df, max_height=520)

    return filtered_df


def render_download_button(df, t=None):
    t = _t(t)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=t["download_csv"],
        data=csv,
        file_name="segmented_customers.csv",
        mime="text/csv",
        use_container_width=True,
    )

def render_segment_zip_download_button(df, t=None):
    t = _t(t)

    if "ml_segment" not in df.columns:
        return

    export_df = df.drop(
        columns=["__recency_is_default"],
        errors="ignore",
    )

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for segment_name, segment_df in export_df.groupby("ml_segment"):
            cluster_id = (
                int(segment_df["ml_cluster"].iloc[0])
                if "ml_cluster" in segment_df.columns
                else 0
            )

            safe_segment_name = _safe_filename(segment_name)
            file_name = f"cluster_{cluster_id}_{safe_segment_name}.csv"

            csv_bytes = segment_df.to_csv(index=False).encode("utf-8")
            zip_file.writestr(file_name, csv_bytes)

    st.download_button(
        label=t["download_segments_zip"],
        data=zip_buffer.getvalue(),
        file_name="customer_segments_by_group.zip",
        mime="application/zip",
        use_container_width=True,
    )

# ============================================================
# Demo Mode UI
# ============================================================

def render_demo_summary(df, t=None):
    t = _t(t)

    st.subheader(t["demo_segment_summary"])

    customer_count_column = "customer_id" if "customer_id" in df.columns else "ml_cluster"

    summary = (
        df.groupby("ml_segment")
        .agg(
            customers=(customer_count_column, "count"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
            avg_order_value=("avg_order_value", "mean"),
            avg_unique_products=("unique_products", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("avg_monetary", ascending=False)
    )

    st.caption(t["demo_segment_caption"])
    render_dark_table(summary, max_height=360)

    return summary


def render_demo_charts(segment_summary, t=None):
    t = _t(t)

    customers_title = "Segmente göre müşteri sayısı" if t["language"] == "Dil" else "Customers by segment"
    monetary_title = "Segmente göre ortalama monetary" if t["language"] == "Dil" else "Average monetary by segment"
    customers_axis = "Müşteri sayısı" if t["language"] == "Dil" else "Customers"
    monetary_axis = "Ortalama monetary" if t["language"] == "Dil" else "Average monetary"

    col_left, col_right = st.columns(2)

    with col_left:
        fig = px.bar(
            segment_summary,
            x="customers",
            y="ml_segment",
            orientation="h",
            title=customers_title,
            text="customers",
            color_discrete_sequence=[PREMIUM_BLUE],
        )

        fig.update_layout(
            height=420,
            yaxis_title="",
            xaxis_title=customers_axis,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(2,6,23,0.32)",
            font_color="#e5e7eb",
            margin=dict(l=20, r=20, t=60, b=20),
        )

        fig.update_xaxes(gridcolor="rgba(148, 163, 184, 0.16)")
        fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.16)")

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        fig = px.bar(
            segment_summary,
            x="avg_monetary",
            y="ml_segment",
            orientation="h",
            title=monetary_title,
            text="avg_monetary",
            color_discrete_sequence=[PREMIUM_TEAL],
        )

        fig.update_layout(
            height=420,
            yaxis_title="",
            xaxis_title=monetary_axis,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(2,6,23,0.32)",
            font_color="#e5e7eb",
            margin=dict(l=20, r=20, t=60, b=20),
        )

        fig.update_xaxes(gridcolor="rgba(148, 163, 184, 0.16)")
        fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.16)")

        st.plotly_chart(fig, use_container_width=True)
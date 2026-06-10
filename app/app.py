import pandas as pd
import streamlit as st

from clustering_utils import (
    apply_custom_cluster_labels,
    build_cluster_profile,
    cluster_uploaded_customer_features,
    compute_pca_projection,
    make_suggested_segment_labels_unique,
    evaluate_k_range,
    prepare_clustering_matrix,
    recommend_business_friendly_k,
    cluster_prepared_matrix,
    add_suggested_segment_labels,
    add_segment_size_warnings,
    add_segment_drivers,
    add_recommended_actions,
)
from data_utils import (
    PROFILE_FIELDS,
    TRANSACTION_FIELDS,
    build_customer_features_from_profile,
    build_customer_features_from_transactions,
    detect_upload_type,
    prepare_transaction_mapping_and_df,
    suggest_column_mapping,
    suggest_profile_mapping,
    validate_customer_features,
)
from model_utils import load_demo_data, load_feature_names
from style import apply_custom_css
from translations import get_text
from ui_utils import (
    render_cluster_label_inputs,
    render_cluster_profile,
    render_cluster_setup,
    render_demo_charts,
    render_demo_summary,
    render_detection_message,
    render_download_button,
    render_hero,
    render_kpi_cards,
    render_mapping_selectboxes,
    render_pca_scatter,
    render_profile_guidance,
    render_section_header,
    render_segmented_customer_table,
    render_silhouette_table,
    render_supported_formats_expander,
    render_transaction_guidance,
    render_upload_preview,
    render_workflow_steps,
    render_dark_table,
    render_segment_size_warnings,
    render_segment_insight_cards,
    render_segment_charts,
    render_segment_zip_download_button,
)


# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="CustomerLens BI",
    page_icon="📊",
    layout="wide",
)

apply_custom_css()


# ============================================================
# App State / Sidebar
# ============================================================

def reset_app():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.clear()
    st.rerun()


def save_uploaded_features(feature_df):
    st.session_state["uploaded_feature_df"] = feature_df.copy()
    st.session_state["has_uploaded_features"] = True


def clear_uploaded_features():
    st.session_state.pop("uploaded_feature_df", None)
    st.session_state["has_uploaded_features"] = False
    st.session_state.pop("selected_k_for_labels", None)

    keys_to_remove = [
        key for key in st.session_state.keys()
        if key.startswith("cluster_label_")
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)


def render_sidebar():
    st.sidebar.title("CustomerLens BI")

    language_label = st.sidebar.radio(
        "Language / Dil",
        options=["English", "Türkçe"],
        index=1,
        horizontal=False,
    )

    language_code = "tr" if language_label == "Türkçe" else "en"
    t = get_text(language_code)

    st.sidebar.caption(t["app_subtitle"])

    data_mode = st.sidebar.radio(
        t["choose_data_source"],
        [t["use_demo"], t["upload_csv"]],
        index=0,
    )

    if st.sidebar.button(t["reset_app"], use_container_width=True):
        reset_app()

    st.sidebar.markdown("---")
    render_supported_formats_expander(st.sidebar, expanded=False, t=t)

    return data_mode, t


# ============================================================
# Upload Handling
# ============================================================

def get_upload_type_label(upload_type, t):
    upload_type_labels = {
        "customer_features": t["customer_feature_csv"],
        "transaction_data": t["transaction_csv"],
        "customer_profile": t["customer_profile_csv"],
        "unknown": t["unknown_csv"],
    }

    return upload_type_labels.get(upload_type, upload_type)


def get_feature_df_from_upload(uploaded_df, upload_type, features, t):
    upload_type_label = get_upload_type_label(upload_type, t)

    render_detection_message(upload_type_label, t=t)
    render_upload_preview(uploaded_df, t=t)

    if upload_type == "unknown":
        st.warning(t["unknown_mapping_warning"])

        mapping_mode = st.radio(
            t["mapping_mode_question"],
            [t["transaction_mode"], t["profile_mode"]],
            horizontal=True,
        )

    elif upload_type == "transaction_data":
        mapping_mode = t["transaction_mode"]

    elif upload_type == "customer_profile":
        mapping_mode = t["profile_mode"]

    else:
        st.success(t["customer_feature_detected"])
        feature_df = validate_customer_features(uploaded_df, features)
        save_uploaded_features(feature_df)
        return feature_df

    if mapping_mode == t["transaction_mode"]:
        return get_transaction_feature_df(uploaded_df, t)

    return get_profile_feature_df(uploaded_df, t)


def get_transaction_feature_df(uploaded_df, t):
    suggested_mapping = suggest_column_mapping(uploaded_df)

    render_section_header(
        t["transaction_mapping"],
        t["transaction_mapping_caption"],
        icon="🧾",
    )

    render_transaction_guidance(t=t)

    mapping = render_mapping_selectboxes(
        TRANSACTION_FIELDS,
        suggested_mapping,
        uploaded_df,
        key_prefix="transaction_mapping",
    )

    if not st.button(t["generate_features"], type="primary"):
        st.stop()

    transaction_df, transaction_mapping = prepare_transaction_mapping_and_df(
        uploaded_df,
        mapping,
    )

    with st.spinner(t["clustering_running"]):
        feature_df = build_customer_features_from_transactions(
            transaction_df,
            transaction_mapping,
        )

    save_uploaded_features(feature_df)
    return feature_df


def get_profile_feature_df(uploaded_df, t):
    suggested_mapping = suggest_profile_mapping(uploaded_df)

    render_section_header(
        t["profile_mapping"],
        t["profile_mapping_caption"],
        icon="👤",
    )

    render_profile_guidance(t=t)

    profile_mapping = render_mapping_selectboxes(
        PROFILE_FIELDS,
        suggested_mapping,
        uploaded_df,
        key_prefix="profile_mapping",
    )

    recency_missing_message = t.get(
        "profile_recency_missing_warning",
        (
            "Recency kolonu seçilmedi. Uygulama güvenli varsayılan olarak 0 kullanacak; "
            "ancak veri setinde son satın almadan geçen gün veya son aktivite kolonu varsa "
            "segmentasyon kalitesi artabilir."
        ),
    )

    if (
        not profile_mapping.get("recency")
        or profile_mapping.get("recency") == "Not selected"
    ):
        st.warning(recency_missing_message)

    if not st.button(t["generate_features"], type="primary"):
        st.stop()

    with st.spinner(t["clustering_running"]):
        feature_df = build_customer_features_from_profile(uploaded_df, profile_mapping)

    save_uploaded_features(feature_df)
    return feature_df


# ============================================================
# Uploaded Clustering Flow
# ============================================================

def get_feature_signature(feature_df, features):
    return (
        len(feature_df),
        tuple(features),
        tuple(feature_df.columns),
        float(feature_df[features].sum(numeric_only=True).sum()),
    )


def clear_clustering_cache():
    keys_to_remove = [
        "clustering_signature",
        "X_scaled",
        "clean_feature_df",
        "scores_df",
        "recommendation",
        "clustered_df",
        "cluster_model",
        "cluster_profile",
        "pca_base_df",
        "pca_selected_k",
        "selected_k_for_model",
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)


def render_uploaded_clustering(feature_df, features, t):
    st.markdown("---")

    render_section_header(
        t["uploaded_clustering"],
        t["uploaded_clustering_caption"],
        icon="🧠",
    )
    language_code = "tr" if t["language"] == "Dil" else "en"

    current_signature = get_feature_signature(feature_df, features)

    if st.session_state.get("clustering_signature") != current_signature:
        clear_clustering_cache()
        st.session_state["clustering_signature"] = current_signature

    # ------------------------------------------------------------
    # 1) Matrix + scaler only once per uploaded/generated feature_df
    # ------------------------------------------------------------
    if "X_scaled" not in st.session_state or "clean_feature_df" not in st.session_state:
        with st.spinner(t["preparing_matrix"]):
            X_scaled, clean_feature_df, _ = prepare_clustering_matrix(
                feature_df,
                features,
            )

        st.session_state["X_scaled"] = X_scaled
        st.session_state["clean_feature_df"] = clean_feature_df
    else:
        X_scaled = st.session_state["X_scaled"]
        clean_feature_df = st.session_state["clean_feature_df"]

    # ------------------------------------------------------------
    # 2) Silhouette only once per uploaded/generated feature_df
    # ------------------------------------------------------------
    if "scores_df" not in st.session_state:
        with st.spinner(t["evaluating_k"]):
            scores_df = evaluate_k_range(
                X_scaled,
                min_k=2,
                max_k=8,
                max_sample_rows=5000,
            )

        recommendation = recommend_business_friendly_k(scores_df)

        st.session_state["scores_df"] = scores_df
        st.session_state["recommendation"] = recommendation
    else:
        scores_df = st.session_state["scores_df"]
        recommendation = st.session_state["recommendation"]

    # ------------------------------------------------------------
    # Show sampling info if silhouette was calculated on a sample
    # ------------------------------------------------------------
    if "used_sample" in scores_df.columns and bool(scores_df["used_sample"].iloc[0]):
        evaluated_rows = int(scores_df["evaluated_rows"].iloc[0])
        total_rows = int(scores_df["total_rows"].iloc[0])

        st.info(
            t["silhouette_sampling_info"].format(
                evaluated_rows=evaluated_rows,
                total_rows=total_rows,
            )
        )

    selected_k = render_cluster_setup(scores_df, recommendation, t=t)
    render_silhouette_table(scores_df, t=t)

    # ------------------------------------------------------------
    # 3) If k changes, clear old cluster label inputs
    # ------------------------------------------------------------
    previous_k = st.session_state.get("selected_k_for_labels")

    if previous_k is not None and previous_k != selected_k:
        keys_to_remove = [
            key for key in st.session_state.keys()
            if key.startswith("cluster_label_")
        ]

        for key in keys_to_remove:
            st.session_state.pop(key, None)

    st.session_state["selected_k_for_labels"] = selected_k

    # ------------------------------------------------------------
    # 4) KMeans only when selected_k changes
    # ------------------------------------------------------------
    if (
        "clustered_df" not in st.session_state
        or st.session_state.get("selected_k_for_model") != selected_k
    ):
        with st.spinner(t["running_kmeans"]):
            clustered_df, model = cluster_prepared_matrix(
                clean_feature_df,
                X_scaled,
                selected_k,
            )

        cluster_profile = build_cluster_profile(clustered_df)

        cluster_profile = add_segment_size_warnings(cluster_profile)

        cluster_profile = add_suggested_segment_labels(
            cluster_profile,
            language_code=language_code,
        )

        cluster_profile = make_suggested_segment_labels_unique(
            cluster_profile,
            language_code=language_code,
        )

        cluster_profile = add_segment_drivers(
            cluster_profile,
            clustered_df,
            language_code=language_code,
        )

        cluster_profile = add_recommended_actions(
            cluster_profile,
            language_code=language_code,
        )

        st.session_state["clustered_df"] = clustered_df
        st.session_state["cluster_model"] = model
        st.session_state["cluster_profile"] = cluster_profile
        st.session_state["selected_k_for_model"] = selected_k

        # k değişince PCA label'ları da değişeceği için temizle
        st.session_state.pop("pca_base_df", None)
        st.session_state.pop("pca_selected_k", None)
    else:
        clustered_df = st.session_state["clustered_df"]
        cluster_profile = st.session_state["cluster_profile"]

    st.markdown("---")
    render_cluster_profile(
        cluster_profile,
        title=t["cluster_profile_before"],
        t=t,
    )
    # st.write(
    #     cluster_profile[
    #         [
    #             "ml_cluster",
    #             "suggested_segment",
    #             "segment_drivers",
    #             "recency_is_default",
    #         ]
    #     ]
    # )

    render_segment_size_warnings(cluster_profile, t=t)

    label_mapping = render_cluster_label_inputs(cluster_profile, t=t)

    insight_profile = cluster_profile.copy()
    insight_profile["suggested_segment"] = insight_profile["ml_cluster"].map(
        lambda cluster_id: label_mapping.get(
            int(cluster_id),
            f"Cluster {int(cluster_id)}",
        )
    )

    render_segment_insight_cards(insight_profile, t=t)

    labeled_df = apply_custom_cluster_labels(clustered_df, label_mapping)

    labeled_df["customer_segment"] = labeled_df["ml_segment"]
    labeled_df["cluster_id"] = labeled_df["ml_cluster"]

    labeled_profile = build_cluster_profile(labeled_df)

    segment_name_lookup = (
        labeled_df[["ml_cluster", "ml_segment"]]
        .drop_duplicates()
        .set_index("ml_cluster")["ml_segment"]
        .to_dict()
    )

    labeled_profile["ml_segment"] = labeled_profile["ml_cluster"].map(
        segment_name_lookup
    )

    # ------------------------------------------------------------
    # 5) PCA only when selected_k changes
    # Not when user only edits cluster names
    # ------------------------------------------------------------
    if (
            "pca_base_df" not in st.session_state
            or st.session_state.get("pca_selected_k") != selected_k
    ):
        pca_df = compute_pca_projection(
            X_scaled,
            clustered_df,
            max_sample_rows=10000,
        )

        st.session_state["pca_base_df"] = pca_df
        st.session_state["pca_selected_k"] = selected_k
    else:
        pca_df = st.session_state["pca_base_df"].copy()

    # Kullanıcı cluster isimlerini değiştirirse PCA'daki segment isimleri güncellensin
    pca_df["ml_segment"] = pca_df["ml_cluster"].map(
        lambda cluster_id: label_mapping.get(cluster_id, f"Cluster {cluster_id}")
    )
    if (
            "pca_used_sample" in pca_df.columns
            and bool(pca_df["pca_used_sample"].iloc[0])
    ):
        evaluated_rows = int(pca_df["pca_evaluated_rows"].iloc[0])
        total_rows = int(pca_df["pca_total_rows"].iloc[0])

        st.info(
            t["pca_sampling_info"].format(
                evaluated_rows=evaluated_rows,
                total_rows=total_rows,
            )
        )

    st.markdown("---")
    render_section_header(
        t["segmentation_results"],
        t["segmentation_results_caption"],
        icon="📌",
    )

    render_kpi_cards(labeled_df, t=t)

    st.markdown("---")
    render_cluster_profile(
        labeled_profile,
        title=t["final_cluster_profile"],
        t=t,
    )

    render_segment_charts(labeled_profile, t=t)

    render_pca_scatter(pca_df, t=t, selected_k=selected_k)

    filtered_df = render_segmented_customer_table(labeled_df, t=t)

    if "customer_segment" not in filtered_df.columns:
        filtered_df = filtered_df.copy()
        filtered_df["customer_segment"] = filtered_df["ml_segment"]

    if "cluster_id" not in filtered_df.columns:
        filtered_df = filtered_df.copy()
        filtered_df["cluster_id"] = filtered_df["ml_cluster"]

    # Internal metadata columns should not be exported.
    export_df = filtered_df.drop(
        columns=["__recency_is_default"],
        errors="ignore",
    )

    render_download_button(export_df, t=t)
    render_segment_zip_download_button(export_df, t=t)


# ============================================================
# Demo / Upload Modes
# ============================================================

def render_demo_mode(t):
    df = load_demo_data()

    st.success(t["demo_loaded"])

    render_kpi_cards(df, t=t)

    st.markdown("---")
    render_section_header(
        t["demo_overview"],
        t["demo_overview_caption"],
        icon="📊",
    )

    segment_summary = render_demo_summary(df, t=t)
    render_demo_charts(segment_summary, t=t)

    if "business_segment" in df.columns:
        st.markdown("---")
        st.subheader(t["business_vs_ml"])
        st.caption(t["business_vs_ml_caption"])

        comparison = pd.crosstab(df["business_segment"], df["ml_segment"])
        render_dark_table(comparison.reset_index(), max_height=360)

    st.markdown("---")
    filtered_df = render_segmented_customer_table(df, t=t)
    render_download_button(filtered_df, t=t)


def render_upload_mode(features, t):
    render_section_header(
        t["upload_title"],
        t["upload_caption"],
        icon="⬆️",
    )

    st.info(t["large_file_warning"])

    uploaded_file = st.file_uploader(
        t["upload_label"],
        type=["csv"],
        key="customer_csv_upload",
    )

    if uploaded_file is None:
        clear_uploaded_features()
        st.warning(t["file_waiting_warning"])
        st.stop()

    uploaded_df = pd.read_csv(uploaded_file)
    upload_type = detect_upload_type(uploaded_df, features)

    try:
        # If customer-level features were already generated, keep using them.
        # This prevents sliders/text inputs from sending the user back to mapping.
        if (
            st.session_state.get("has_uploaded_features")
            and "uploaded_feature_df" in st.session_state
        ):
            if st.button("Eşleştirmeyi yeniden yap / Remap uploaded CSV"):
                clear_uploaded_features()
                st.rerun()

            feature_df = st.session_state["uploaded_feature_df"]
            render_uploaded_clustering(feature_df, features, t)
            return

        feature_df = get_feature_df_from_upload(
            uploaded_df,
            upload_type,
            features,
            t,
        )

        render_uploaded_clustering(feature_df, features, t)

    except ValueError as exc:
        st.error(str(exc))
        st.stop()


# ============================================================
# Main App
# ============================================================

features = load_feature_names()
data_mode, t = render_sidebar()

render_hero(t=t)
render_workflow_steps(t=t)

if data_mode == t["use_demo"]:
    render_demo_mode(t)
else:
    render_upload_mode(features, t)
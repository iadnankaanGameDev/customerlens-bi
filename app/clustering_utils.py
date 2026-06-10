import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.utils import check_random_state

from data_utils import validate_customer_features


LOG_FEATURES = [
    "frequency",
    "monetary",
    "avg_order_value",
    "unique_products",
    "total_quantity",
    "customer_lifetime_days",
]


def prepare_clustering_matrix(feature_df, features):
    clean_df = validate_customer_features(feature_df, features)
    X = clean_df[features].copy()

    for col in features:
        X[col] = pd.to_numeric(X[col], errors="coerce")

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    available_log_features = [col for col in LOG_FEATURES if col in X.columns]
    X[available_log_features] = np.log1p(X[available_log_features].clip(lower=0))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, clean_df, scaler


def evaluate_k_range(
    X_scaled,
    min_k=2,
    max_k=8,
    max_sample_rows=5000,
    random_state=42,
):
    n_total_samples = len(X_scaled)

    if n_total_samples < 3:
        raise ValueError("At least 3 customers are needed for clustering.")

    X_eval, sample_indices, used_sample = sample_scaled_matrix(
        X_scaled,
        max_rows=max_sample_rows,
        random_state=random_state,
    )

    n_eval_samples = len(X_eval)

    max_k = min(max_k, n_eval_samples - 1)

    if min_k > max_k:
        raise ValueError("Not enough customers to evaluate the requested cluster range.")

    rows = []

    for k in range(min_k, max_k + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = model.fit_predict(X_eval)

        cluster_counts = pd.Series(labels).value_counts()
        min_cluster_size = int(cluster_counts.min())
        min_cluster_share = float(min_cluster_size / n_eval_samples)

        rows.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette_score": silhouette_score(X_eval, labels),
                "min_cluster_size": min_cluster_size,
                "min_cluster_share": min_cluster_share,
                "evaluated_rows": n_eval_samples,
                "total_rows": n_total_samples,
                "used_sample": used_sample,
            }
        )

    return pd.DataFrame(rows)


def recommend_business_friendly_k(scores_df):
    if scores_df.empty:
        raise ValueError("No silhouette scores available.")

    scores_df = scores_df.copy()

    best_row = scores_df.sort_values("silhouette_score", ascending=False).iloc[0]
    technical_best_k = int(best_row["k"])
    best_score = float(best_row["silhouette_score"])

    # Business-friendly recommendation:
    # - Technical best k maximizes silhouette.
    # - Business-friendly k prefers simpler/readable segmentation
    #   when its silhouette score is close enough to the best score.
    # - Avoids tiny clusters where possible.
    readable_candidates = scores_df[
        (scores_df["k"].between(3, 6))
        & (scores_df["silhouette_score"] >= best_score * 0.92)
        & (scores_df["min_cluster_share"] >= 0.03)
    ].copy()

    if not readable_candidates.empty:
        business_k = int(readable_candidates.sort_values("k").iloc[0]["k"])
    else:
        relaxed_candidates = scores_df[
            (scores_df["k"].between(3, 6))
            & (scores_df["silhouette_score"] >= best_score * 0.88)
        ].copy()

        if not relaxed_candidates.empty:
            business_k = int(
                relaxed_candidates.sort_values(
                    ["silhouette_score", "k"],
                    ascending=[False, True],
                ).iloc[0]["k"]
            )
        else:
            business_k = technical_best_k

    return {
        "technical_best_k": technical_best_k,
        "business_recommended_k": business_k,
        "best_score": best_score,
    }


def cluster_uploaded_customer_features(feature_df, features, n_clusters):
    X_scaled, clean_df, scaler = prepare_clustering_matrix(feature_df, features)

    if len(clean_df) < 3:
        raise ValueError("At least 3 customers are needed for clustering.")

    if n_clusters < 2 or n_clusters >= len(clean_df):
        raise ValueError("Selected cluster count must be between 2 and customer count - 1.")

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    result_df = clean_df.copy()
    result_df["ml_cluster"] = model.fit_predict(X_scaled)
    result_df["ml_segment"] = result_df["ml_cluster"].map(
        lambda cluster_id: f"Cluster {cluster_id}"
    )

    return result_df, X_scaled, model, scaler


def build_cluster_profile(clustered_df):
    total_customers = len(clustered_df)
    total_revenue = clustered_df["monetary"].sum()

    profile = (
        clustered_df.groupby("ml_cluster")
        .agg(
            customers=("customer_id", "count"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
            avg_order_value=("avg_order_value", "mean"),
            avg_unique_products=("unique_products", "mean"),
            avg_total_quantity=("total_quantity", "mean"),
            avg_lifetime_days=("customer_lifetime_days", "mean"),
            total_revenue=("monetary", "sum"),
        )
        .reset_index()
    )

    profile["customer_share_pct"] = profile["customers"] / total_customers * 100

    profile["revenue_share_pct"] = np.where(
        total_revenue > 0,
        profile["total_revenue"] / total_revenue * 100,
        0,
    )

    columns = [
        "ml_cluster",
        "customers",
        "customer_share_pct",
        "avg_recency",
        "avg_frequency",
        "avg_monetary",
        "avg_order_value",
        "avg_unique_products",
        "avg_total_quantity",
        "avg_lifetime_days",
        "total_revenue",
        "revenue_share_pct",
    ]

    return profile[columns].round(2)

def add_segment_size_warnings(
    cluster_profile,
    very_small_threshold=5.0,
    small_threshold=10.0,
    dominant_threshold=60.0,
):
    profile = cluster_profile.copy()

    def get_warning_level(customer_share_pct):
        if customer_share_pct < very_small_threshold:
            return "very_small"

        if customer_share_pct < small_threshold:
            return "small"

        if customer_share_pct > dominant_threshold:
            return "dominant"

        return "normal"

    profile["size_warning_level"] = profile["customer_share_pct"].apply(
        get_warning_level
    )

    return profile

def _safe_pct_diff(value, average):
    if average is None or average == 0 or pd.isna(average):
        return 0.0

    return float((value - average) / average * 100)


def _format_driver_direction(feature_name, pct_diff, language_code="en"):
    abs_diff = abs(pct_diff)

    if language_code == "tr":
        if feature_name == "avg_recency":
            if pct_diff < 0:
                return (
                    f"Recency ortalamanın %{abs_diff:.1f} altında; "
                    "bu grup daha yakın zamanda aktif görünüyor."
                )
            if pct_diff > 0:
                return (
                    f"Recency ortalamanın %{abs_diff:.1f} üzerinde; "
                    "bu grup daha uzun süredir pasif görünüyor."
                )
            return "Recency genel ortalamaya yakın; aktivite zamanı açısından belirgin bir fark yok."

        if feature_name == "avg_monetary":
            if pct_diff > 0:
                return (
                    f"Monetary ortalamanın %{abs_diff:.1f} üzerinde; "
                    "bu grup daha yüksek harcama eğilimi gösteriyor."
                )
            if pct_diff < 0:
                return (
                    f"Monetary ortalamanın %{abs_diff:.1f} altında; "
                    "bu grup daha düşük harcama eğilimi gösteriyor."
                )
            return "Monetary genel ortalamaya yakın; harcama düzeyi belirgin şekilde ayrışmıyor."

        if feature_name == "avg_frequency":
            if pct_diff > 0:
                return (
                    f"Frequency ortalamanın %{abs_diff:.1f} üzerinde; "
                    "bu grup daha sık alışveriş yapıyor."
                )
            if pct_diff < 0:
                return (
                    f"Frequency ortalamanın %{abs_diff:.1f} altında; "
                    "bu grup daha seyrek alışveriş yapıyor."
                )
            return "Frequency genel ortalamaya yakın; alışveriş sıklığı belirgin şekilde ayrışmıyor."

        label_map = {
            "avg_order_value": "Average order value",
            "avg_unique_products": "Unique products",
            "avg_total_quantity": "Total quantity",
            "avg_lifetime_days": "Customer lifetime",
        }

        label = label_map.get(feature_name, feature_name)

        if pct_diff > 0:
            return f"{label} ortalamanın %{abs_diff:.1f} üzerinde."
        if pct_diff < 0:
            return f"{label} ortalamanın %{abs_diff:.1f} altında."
        return f"{label} genel ortalamaya yakın."

    # English
    if feature_name == "avg_recency":
        if pct_diff < 0:
            return (
                f"Recency is {abs_diff:.1f}% below average, "
                "suggesting more recent customer activity."
            )
        if pct_diff > 0:
            return (
                f"Recency is {abs_diff:.1f}% above average, "
                "suggesting longer inactivity."
            )
        return "Recency is close to the dataset average, so activity timing does not clearly separate this segment."

    if feature_name == "avg_monetary":
        if pct_diff > 0:
            return (
                f"Monetary is {abs_diff:.1f}% above average, "
                "suggesting stronger spending behavior."
            )
        if pct_diff < 0:
            return (
                f"Monetary is {abs_diff:.1f}% below average, "
                "suggesting lower spending behavior."
            )
        return "Monetary is close to the dataset average, so spending does not clearly separate this segment."

    if feature_name == "avg_frequency":
        if pct_diff > 0:
            return (
                f"Frequency is {abs_diff:.1f}% above average, "
                "suggesting more frequent purchasing."
            )
        if pct_diff < 0:
            return (
                f"Frequency is {abs_diff:.1f}% below average, "
                "suggesting less frequent purchasing."
            )
        return "Frequency is close to the dataset average, so purchase frequency does not clearly separate this segment."

    label_map = {
        "avg_order_value": "Average order value",
        "avg_unique_products": "Unique products",
        "avg_total_quantity": "Total quantity",
        "avg_lifetime_days": "Customer lifetime",
    }

    label = label_map.get(feature_name, feature_name)

    if pct_diff > 0:
        return f"{label} is {abs_diff:.1f}% above average."
    if pct_diff < 0:
        return f"{label} is {abs_diff:.1f}% below average."
    return f"{label} is close to the dataset average."


def add_segment_drivers(
    cluster_profile,
    clustered_df,
    language_code="en",
    top_n=3,
):
    profile = cluster_profile.copy()

    recency_is_default = False
    if "__recency_is_default" in clustered_df.columns:
        recency_is_default = bool(clustered_df["__recency_is_default"].all())

    driver_features = [
        "avg_monetary",
        "avg_frequency",
        "avg_recency",
    ]

    if recency_is_default:
        driver_features = [
            feature for feature in driver_features
            if feature != "avg_recency"
        ]

    dataset_averages = {
        feature: profile[feature].mean()
        for feature in driver_features
        if feature in profile.columns
    }

    driver_rows = []

    for _, row in profile.iterrows():
        cluster_id = int(row["ml_cluster"])

        cluster_drivers = []

        for feature in driver_features:
            if feature not in profile.columns:
                continue

            pct_diff = _safe_pct_diff(row[feature], dataset_averages.get(feature))
            explanation = _format_driver_direction(
                feature,
                pct_diff,
                language_code=language_code,
            )

            cluster_drivers.append(
                {
                    "feature": feature,
                    "pct_diff": pct_diff,
                    "abs_pct_diff": abs(pct_diff),
                    "explanation": explanation,
                }
            )

        cluster_drivers = sorted(
            cluster_drivers,
            key=lambda item: item["abs_pct_diff"],
            reverse=True,
        )[:top_n]

        driver_rows.append(
            {
                "ml_cluster": cluster_id,
                "segment_drivers": cluster_drivers,
                "recency_is_default": recency_is_default,
            }
        )

    drivers_df = pd.DataFrame(driver_rows)

    return profile.merge(drivers_df, on="ml_cluster", how="left")

def _get_action_templates(language_code="en"):
    if language_code == "tr":
        return {
            "high_value_loyal": (
                "VIP sadakat teklifleri, erken erişim kampanyaları ve kişiselleştirilmiş avantajlarla "
                "bu segmentin bağlılığını koru."
            ),
            "valuable_at_risk": (
                "Bu segment değerli ama pasifleşme riski taşıyor. Geri kazanım kampanyaları, özel indirimler "
                "ve hatırlatma mesajlarıyla yeniden aktivasyon dene."
            ),
            "premium_occasional": (
                "Daha sık alışverişe teşvik etmek için premium ürün önerileri, sınırlı süreli teklifler "
                "ve çapraz satış kampanyaları kullan."
            ),
            "frequent_low_spend": (
                "Sepet tutarını artırmak için bundle teklifleri, tamamlayıcı ürün önerileri ve minimum sepet kampanyaları dene."
            ),
            "dormant_low_value": (
                "Düşük maliyetli yeniden aktivasyon kampanyalarıyla test et; yüksek bütçeli kampanyaları bu segmente sınırlı uygula."
            ),
            "recent_low_engagement": (
                "Onboarding mesajları, ilk/sonraki alışveriş teşvikleri ve ürün keşif önerileriyle ilişkiyi güçlendir."
            ),
            "dormant_customers": (
                "Win-back kampanyaları, zaman sınırlı teklifler ve yeniden ilgi uyandıracak iletişimlerle geri kazanım dene."
            ),
            "loyal_regulars": (
                "Sadakat programları, düzenli alışveriş ödülleri ve kişiselleştirilmiş önerilerle bu müşterileri elde tut."
            ),
            "high_value_customers": (
                "Kişiselleştirilmiş premium teklifler, özel kampanyalar ve yüksek değerli ürün önerileriyle gelir potansiyelini koru."
            ),
            "standard_customers": (
                "Bu segment için genel kampanyalar, ürün önerileri ve davranışa göre test edilecek küçük promosyonlar uygundur."
            ),
        }

    return {
        "high_value_loyal": (
            "Protect this segment with VIP loyalty offers, early access campaigns, and personalized benefits."
        ),
        "valuable_at_risk": (
            "This segment is valuable but may be drifting away. Use win-back campaigns, special offers, "
            "and reminder messaging to reactivate them."
        ),
        "premium_occasional": (
            "Encourage more frequent purchases with premium product recommendations, limited-time offers, "
            "and cross-sell campaigns."
        ),
        "frequent_low_spend": (
            "Increase basket value with bundles, complementary product recommendations, and minimum-spend incentives."
        ),
        "dormant_low_value": (
            "Use low-cost reactivation tests for this group; avoid allocating heavy campaign budget too early."
        ),
        "recent_low_engagement": (
            "Strengthen the relationship with onboarding messages, next-purchase incentives, and product discovery prompts."
        ),
        "dormant_customers": (
            "Try win-back campaigns, time-limited offers, and re-engagement messaging."
        ),
        "loyal_regulars": (
            "Retain these customers with loyalty programs, repeat-purchase rewards, and personalized recommendations."
        ),
        "high_value_customers": (
            "Preserve revenue potential with personalized premium offers, exclusive campaigns, and high-value recommendations."
        ),
        "standard_customers": (
            "Use general campaigns, product recommendations, and small promotional tests based on observed behavior."
        ),
    }


def infer_segment_action_key(row):
    suggested_segment = str(row.get("suggested_segment", "")).lower()

    # Label-based fallback. Works for both EN/TR suggested labels.
    if "sadık yüksek" in suggested_segment or "high-value loyal" in suggested_segment:
        return "high_value_loyal"

    if "risk" in suggested_segment or "at risk" in suggested_segment:
        return "valuable_at_risk"

    if "premium" in suggested_segment or "ara sıra" in suggested_segment or "occasional" in suggested_segment:
        return "premium_occasional"

    if "sık alışveriş" in suggested_segment or "frequent low" in suggested_segment:
        return "frequent_low_spend"

    if "uykuda düşük" in suggested_segment or "dormant low" in suggested_segment:
        return "dormant_low_value"

    if "yeni" in suggested_segment or "low-engagement" in suggested_segment:
        return "recent_low_engagement"

    if "uykuda" in suggested_segment or "dormant" in suggested_segment:
        return "dormant_customers"

    if "sadık düzenli" in suggested_segment or "loyal regular" in suggested_segment:
        return "loyal_regulars"

    if "yüksek değer" in suggested_segment or "high-value" in suggested_segment:
        return "high_value_customers"

    return "standard_customers"


def add_recommended_actions(cluster_profile, language_code="en"):
    profile = cluster_profile.copy()
    action_templates = _get_action_templates(language_code)

    profile["recommended_action"] = profile.apply(
        lambda row: action_templates.get(
            infer_segment_action_key(row),
            action_templates["standard_customers"],
        ),
        axis=1,
    )

    return profile

def _relative_level(value, average, low_threshold=0.75, high_threshold=1.25):
    if average is None or average <= 0:
        return "middle"

    ratio = value / average

    if ratio >= high_threshold:
        return "high"

    if ratio <= low_threshold:
        return "low"

    return "middle"


def _get_segment_label_templates(language_code="en"):
    if language_code == "tr":
        return {
            "high_value_loyal": "Sadık Yüksek Değerli Müşteriler",
            "valuable_at_risk": "Risk Altındaki Değerli Müşteriler",
            "premium_occasional": "Ara Sıra Alışveriş Yapan Premium Müşteriler",
            "frequent_low_spend": "Sık Alışveriş Yapan Düşük Harcamalı Müşteriler",
            "dormant_low_value": "Uykuda Düşük Değerli Müşteriler",
            "recent_low_engagement": "Yeni veya Düşük Etkileşimli Aktif Müşteriler",
            "dormant_customers": "Uykuda Müşteriler",
            "loyal_regulars": "Sadık Düzenli Müşteriler",
            "high_value_customers": "Yüksek Değerli Müşteriler",
            "standard_customers": "Standart Müşteriler",
        }

    return {
        "high_value_loyal": "High-Value Loyal Customers",
        "valuable_at_risk": "Valuable Customers at Risk",
        "premium_occasional": "Premium Occasional Buyers",
        "frequent_low_spend": "Frequent Low-Spend Customers",
        "dormant_low_value": "Dormant Low-Value Customers",
        "recent_low_engagement": "New or Low-Engagement Active Customers",
        "dormant_customers": "Dormant Customers",
        "loyal_regulars": "Loyal Regulars",
        "high_value_customers": "High-Value Customers",
        "standard_customers": "Standard Customers",
    }


def suggest_segment_label(row, dataset_averages, language_code="en"):
    labels = _get_segment_label_templates(language_code)

    monetary_level = _relative_level(
        row["avg_monetary"],
        dataset_averages["avg_monetary"],
    )

    frequency_level = _relative_level(
        row["avg_frequency"],
        dataset_averages["avg_frequency"],
    )

    # Recency is inverse:
    # lower recency means more recently active, higher recency means less active.
    recency_level = _relative_level(
        row["avg_recency"],
        dataset_averages["avg_recency"],
    )

    is_high_monetary = monetary_level == "high"
    is_low_monetary = monetary_level == "low"

    is_high_frequency = frequency_level == "high"
    is_low_frequency = frequency_level == "low"

    is_recent = recency_level == "low"
    is_dormant = recency_level == "high"

    if is_high_monetary and is_high_frequency and is_recent:
        return labels["high_value_loyal"]

    if is_high_monetary and is_high_frequency and is_dormant:
        return labels["valuable_at_risk"]

    if is_high_monetary and is_low_frequency:
        return labels["premium_occasional"]

    if is_low_monetary and is_high_frequency:
        return labels["frequent_low_spend"]

    if is_low_monetary and is_low_frequency and is_dormant:
        return labels["dormant_low_value"]

    if is_recent and is_low_frequency:
        return labels["recent_low_engagement"]

    if is_dormant:
        return labels["dormant_customers"]

    if is_high_frequency:
        return labels["loyal_regulars"]

    if is_high_monetary:
        return labels["high_value_customers"]

    return labels["standard_customers"]


def add_suggested_segment_labels(cluster_profile, language_code="en"):
    profile = cluster_profile.copy()

    dataset_averages = {
        "avg_recency": profile["avg_recency"].mean(),
        "avg_frequency": profile["avg_frequency"].mean(),
        "avg_monetary": profile["avg_monetary"].mean(),
    }

    profile["suggested_segment"] = profile.apply(
        lambda row: suggest_segment_label(
            row,
            dataset_averages,
            language_code=language_code,
        ),
        axis=1,
    )

    return profile

def _get_duplicate_segment_suffix(row, dataset_averages, language_code="en"):
    monetary_diff = _safe_pct_diff(
        row.get("avg_monetary", 0),
        dataset_averages.get("avg_monetary", 0),
    )

    frequency_diff = _safe_pct_diff(
        row.get("avg_frequency", 0),
        dataset_averages.get("avg_frequency", 0),
    )

    recency_diff = _safe_pct_diff(
        row.get("avg_recency", 0),
        dataset_averages.get("avg_recency", 0),
    )

    candidates = [
        ("monetary", monetary_diff),
        ("frequency", frequency_diff),
        ("recency", recency_diff),
    ]

    strongest_feature, strongest_diff = max(
        candidates,
        key=lambda item: abs(item[1]),
    )

    if language_code == "tr":
        if strongest_feature == "monetary":
            return "Daha yüksek harcama" if strongest_diff > 0 else "Daha düşük harcama"

        if strongest_feature == "frequency":
            return "Daha sık alışveriş" if strongest_diff > 0 else "Daha seyrek alışveriş"

        if strongest_feature == "recency":
            return "Daha pasif" if strongest_diff > 0 else "Daha aktif"

        return "Alt grup"

    if strongest_feature == "monetary":
        return "Higher spend" if strongest_diff > 0 else "Lower spend"

    if strongest_feature == "frequency":
        return "More frequent" if strongest_diff > 0 else "Less frequent"

    if strongest_feature == "recency":
        return "Less active" if strongest_diff > 0 else "More active"

    return "Subgroup"


def make_suggested_segment_labels_unique(cluster_profile, language_code="en"):
    profile = cluster_profile.copy()

    if "suggested_segment" not in profile.columns:
        return profile

    duplicate_mask = profile["suggested_segment"].duplicated(keep=False)

    if not duplicate_mask.any():
        return profile

    dataset_averages = {
        "avg_recency": profile["avg_recency"].mean(),
        "avg_frequency": profile["avg_frequency"].mean(),
        "avg_monetary": profile["avg_monetary"].mean(),
    }

    used_labels = set()

    for idx, row in profile.iterrows():
        base_label = row["suggested_segment"]

        if not duplicate_mask.loc[idx]:
            used_labels.add(base_label)
            continue

        suffix = _get_duplicate_segment_suffix(
            row,
            dataset_averages,
            language_code=language_code,
        )

        candidate_label = f"{base_label} · {suffix}"

        # Fallback if two duplicate clusters still get the same suffix.
        if candidate_label in used_labels:
            cluster_id = int(row["ml_cluster"])
            candidate_label = f"{base_label} · Cluster {cluster_id}"

        profile.at[idx, "suggested_segment"] = candidate_label
        used_labels.add(candidate_label)

    return profile


def compute_pca_projection(
    X_scaled,
    clustered_df,
    max_sample_rows=10000,
    random_state=42,
):
    n_total_samples = len(X_scaled)

    X_pca, sample_indices, used_sample = sample_scaled_matrix(
        X_scaled,
        max_rows=max_sample_rows,
        random_state=random_state,
    )

    pca = PCA(n_components=2, random_state=random_state)
    projection = pca.fit_transform(X_pca)

    sampled_clustered_df = clustered_df.iloc[sample_indices].copy()

    pca_df = sampled_clustered_df[
        ["customer_id", "ml_cluster", "ml_segment", "monetary", "frequency", "recency"]
    ].copy()

    pca_df["pca_1"] = projection[:, 0]
    pca_df["pca_2"] = projection[:, 1]
    pca_df["pca_used_sample"] = used_sample
    pca_df["pca_evaluated_rows"] = len(X_pca)
    pca_df["pca_total_rows"] = n_total_samples

    return pca_df[
        [
            "pca_1",
            "pca_2",
            "ml_cluster",
            "ml_segment",
            "customer_id",
            "monetary",
            "frequency",
            "recency",
            "pca_used_sample",
            "pca_evaluated_rows",
            "pca_total_rows",
        ]
    ]

def sample_scaled_matrix(X_scaled, max_rows=5000, random_state=42):
    n_samples = len(X_scaled)

    if n_samples <= max_rows:
        return X_scaled, np.arange(n_samples), False

    rng = check_random_state(random_state)
    sample_indices = rng.choice(n_samples, size=max_rows, replace=False)

    return X_scaled[sample_indices], sample_indices, True


def apply_custom_cluster_labels(df, label_mapping):
    result_df = df.copy()

    result_df["ml_segment"] = result_df["ml_cluster"].map(
        lambda cluster_id: label_mapping.get(cluster_id, f"Cluster {cluster_id}")
    )

    return result_df

def cluster_prepared_matrix(clean_df, X_scaled, n_clusters):
    if len(clean_df) < 3:
        raise ValueError("At least 3 customers are needed for clustering.")

    if n_clusters < 2 or n_clusters >= len(clean_df):
        raise ValueError("Selected cluster count must be between 2 and customer count - 1.")

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    result_df = clean_df.copy()
    result_df["ml_cluster"] = model.fit_predict(X_scaled)
    result_df["ml_segment"] = result_df["ml_cluster"].map(
        lambda cluster_id: f"Cluster {cluster_id}"
    )

    return result_df, model


TEXT = {
    "en": {
        # Sidebar
        "language": "Language",
        "app_subtitle": "Interactive customer segmentation workspace",
        "choose_data_source": "Choose data source",
        "use_demo": "Use demo dataset",
        "upload_csv": "Upload your own CSV",
        "reset_app": "Reset App",

        # Hero
        "hero_badge": "Upload-specific clustering workspace",
        "hero_title": "CustomerLens BI",
        "hero_subtitle": (
            "Convert customer, profile, or transaction CSV files into customer-level features, "
            "explore clustering options, inspect cluster profiles, name your own segments, "
            "and export a segmented customer dataset."
        ),
        "hero_input_label": "Input",
        "hero_input_value": "Feature / profile / transaction CSV",
        "hero_model_label": "Model",
        "hero_model_value": "Fresh KMeans per uploaded dataset",
        "hero_output_label": "Output",
        "hero_output_value": "Clustered customers + downloadable CSV",

        # Workflow
        "step_01_title": "Upload CSV",
        "step_01_copy": "Use the demo data or upload your own customer, profile, or transaction file.",
        "step_02_title": "Map columns",
        "step_02_copy": "Review detected columns and fix mappings if the file structure is different.",
        "step_03_title": "Choose clusters",
        "step_03_copy": "Use silhouette guidance, then override k if business segmentation needs more detail.",
        "step_04_title": "Name & export",
        "step_04_copy": "Inspect cluster profiles, rename segments, and download the final segmented CSV.",

        # Upload
        "upload_title": "Upload your CSV",
        "upload_caption": (
            "Start with any customer-level, profile-level, or transaction-level CSV. "
            "The app will guide you through mapping if needed."
        ),
        "upload_label": "Upload customer, profile, or transaction CSV",
        "file_waiting_warning": "Please upload a CSV file to continue.",
        "large_file_warning": (
            "Large files may take longer to process. Column mapping is usually fast, "
            "but customer feature generation, silhouette analysis, and KMeans clustering "
            "can take additional time depending on file size and row count."
        ),

        # Upload detection / preview
        "detected_upload_type": "Detected upload type",
        "customer_feature_csv": "Customer feature CSV",
        "transaction_csv": "Transaction-level CSV",
        "customer_profile_csv": "Customer profile CSV",
        "unknown_csv": "Unknown / manual mapping needed",
        "preview_uploaded_data": "Preview uploaded data",
        "preview_rows": "Preview rows",
        "column_list": "Column list",

        # Mapping mode
        "unknown_mapping_warning": (
            "The app could not fully detect your CSV structure. Choose the mapping mode "
            "that best describes your file."
        ),
        "mapping_mode_question": "How should this CSV be interpreted?",
        "transaction_mode": "Transaction/order data",
        "profile_mode": "Customer profile data",

        # Transaction mapping
        "transaction_mapping": "Transaction column mapping",
        "transaction_mapping_caption": (
            "Use this when each row is an order, invoice, product line, or purchase event."
        ),
        "transaction_guidance": (
            "Transaction mode is best when each row is an order, invoice, product line, "
            "or purchase event. If there is no order_id column, leave it as Not selected. "
            "If there is no customer_id column, choose a stable customer identifier such as "
            "username, email, account name, or customer name."
        ),

        # Profile mapping
        "profile_mapping": "Customer profile column mapping",
        "profile_mapping_caption": "Use this only if each row already represents one customer.",
        "profile_guidance": (
            "Profile mode is best when each row already represents one customer. "
            "If optional fields are missing, the app will estimate them with safe defaults."
        ),
        "profile_recency_missing_warning": (
            "Recency column is not selected. The app will use 0 as a safe default, "
            "but segmentation quality may improve if your dataset contains a days-since-last-purchase "
            "or last activity column."
        ),

        "segment_size_warning_title": "Segment size warning",
        "segment_size_very_small": (
            "Cluster {cluster_id} contains only {share:.1f}% of customers. "
            "This may be a niche or outlier-like segment, so interpret it carefully."
        ),
        "segment_size_small": (
            "Cluster {cluster_id} contains {share:.1f}% of customers. "
            "This is a small segment; it may still be useful, but should be interpreted with care."
        ),
        "segment_size_dominant": (
            "Cluster {cluster_id} contains {share:.1f}% of customers. "
            "This is a dominant segment; the selected k may be too low or the features may not separate customers strongly."
        ),

        # Feature generation
        "generate_features": "Generate customer features",
        "customer_feature_detected": (
            "Customer-level feature CSV detected. The uploaded file will be clustered "
            "using its own customer distribution."
        ),

        # Clustering
        "uploaded_clustering": "Uploaded data clustering",
        "uploaded_clustering_caption": (
            "The uploaded file is clustered independently. The built-in demo model is not forced "
            "onto your custom dataset."
        ),
        "clustering_setup": "Clustering setup",
        "clustering_setup_caption": (
            "Technical best k is the cluster count with the highest silhouette score. "
            "Business-friendly k prefers a simpler, readable segmentation when the score difference is small. "
            "You can always override the recommendation."
        ),
        "technical_best_k": "Technical best k",
        "business_friendly_k": "Business-friendly k",
        "best_silhouette": "Best silhouette",
        "selected_clusters": "Selected number of clusters",
        "silhouette_details": "Show silhouette details",
        "silhouette_caption": (
            "Use this table to compare candidate k values. Technical best k maximizes silhouette. "
            "Business-friendly k prefers simpler groups when scores are close."
        ),
        "active_selected_k": "Active selected k",
        "active_k_info": (
            "Recommended k = {recommended_k}, but clustering is currently running "
            "with active k = {selected_k}."
        ),
        "silhouette_sampling_info": (
            "For faster performance, silhouette analysis was calculated on a representative "
            "sample of {evaluated_rows:,} customers out of {total_rows:,}. "
            "Final segment assignment is still applied to all customers."
        ),

        # Cluster profiles
        "cluster_profile_before": "Cluster profile before naming",
        "cluster_profile_caption": (
            "Use this table to understand each cluster before naming segments. "
            "Look at recency, frequency, monetary value, customer share, and revenue share together."
        ),
        "name_clusters": "Name your clusters",
        "name_clusters_caption": (
            "Default labels are neutral. Rename them only after reviewing the cluster profile. "
            "These labels will be applied to the downloadable CSV."
        ),
        "label_for_cluster": "Label for Cluster",
        "custom_labels_success": "Custom labels will be applied to charts, tables, and the downloaded CSV.",

        # Results
        "segmentation_results": "Segmentation results",
        "segmentation_results_caption": (
            "Review the final customer-level segmentation. Custom labels are reflected in the charts, "
            "table, and downloadable CSV."
        ),
        "final_cluster_profile": "Final cluster profile",
        "pca_view": "Customer clusters PCA view",
        "pca_caption": (
            "This 2D projection is a visual check, not the clustering algorithm itself. "
            "It helps you see whether the customer groups separate clearly or overlap."
        ),
        "segmented_customer_data": "Segmented customer data",
        "segmented_customer_caption": "Filter segments and inspect the final customer-level output before downloading.",
        "filter_by_segment": "Filter by segment",
        "rows_shown": "Rows shown in table",
        "download_csv": "Download segmented CSV",

        "pca_sampling_info": (
            "For faster chart rendering, the PCA visualization is shown on a representative "
            "sample of {evaluated_rows:,} customers out of {total_rows:,}. "
            "Final clustering, KPIs, profiles, and CSV export still use all customers."
        ),
        "segment_insights_title": "Segment insights",
        "segment_insights_caption": (
            "These cards explain why each segment received its suggested label. "
            "Drivers compare each cluster average against the dataset-wide average."
        ),
        "segment_drivers_label": "Key segment drivers",
        "recency_not_available_note": (
            "Recency was not available in this dataset and was filled with a safe default, "
            "so activity timing is not used in this interpretation."
        ),

        # Demo
        "demo_loaded": (
            "Demo customer segmentation dataset loaded. Upload mode will re-cluster your own data separately."
        ),
        "demo_overview": "Demo overview",
        "demo_overview_caption": "This built-in dataset shows the kind of output CustomerLens BI can produce.",
        "demo_segment_summary": "Demo segment summary",
        "demo_segment_caption": (
            "This demo uses the built-in CustomerLens sample data. Uploaded files are clustered separately."
        ),
        "business_vs_ml": "Business segment vs ML segment",
        "business_vs_ml_caption": (
            "This comparison exists only for the demo data because it already has predefined business labels."
        ),
        "profile_recency_missing_warning": (
            "Recency column is not selected. The app will use 0 as a safe default, "
            "but segmentation quality may improve if your dataset contains a days-since-last-purchase "
            "or last activity column."
        ),
        "suggested_segment_label": "Suggested segment label",

        "recommended_action_label": "Recommended action",

        "segment_charts_title": "Segment charts",
        "segment_charts_caption": (
            "Visual summary of segment size, revenue contribution, and average monetary value."
        ),
        "download_segments_zip": "Download segments as separate CSV files",

        "chart_customers_by_segment": "Customers by segment",
        "chart_revenue_share_by_segment": "Revenue share by segment",
        "chart_avg_monetary_by_segment": "Average monetary by segment",
        "chart_customers_axis": "Customers",
        "chart_revenue_share_axis": "Revenue share",
        "chart_avg_monetary_axis": "Average monetary",

        # Spinners
        "clustering_running": "Clustering is running. Large files may take a while...",
        "preparing_matrix": "Preparing clustering matrix...",
        "evaluating_k": "Evaluating cluster counts with silhouette score...",
        "running_kmeans": "Running final KMeans clustering...",
    },

    "tr": {
        # Sidebar
        "language": "Dil",
        "app_subtitle": "Etkileşimli müşteri segmentasyonu çalışma alanı",
        "choose_data_source": "Veri kaynağı seç",
        "use_demo": "Demo veri setini kullan",
        "upload_csv": "Kendi CSV dosyanı yükle",
        "reset_app": "Uygulamayı sıfırla",

        # Hero
        "hero_badge": "Yüklenen veriye özel kümeleme alanı",
        "hero_title": "CustomerLens BI",
        "hero_subtitle": (
            "Müşteri, profil veya işlem CSV dosyalarını müşteri bazlı özelliklere dönüştür; "
            "kümeleme seçeneklerini incele, küme profillerini yorumla, segmentleri kendin isimlendir "
            "ve segmentlenmiş müşteri verisini dışa aktar."
        ),
        "hero_input_label": "Girdi",
        "hero_input_value": "Özellik / profil / işlem CSV",
        "hero_model_label": "Model",
        "hero_model_value": "Yüklenen veriye özel yeni KMeans",
        "hero_output_label": "Çıktı",
        "hero_output_value": "Kümelenmiş müşteriler + indirilebilir CSV",

        # Workflow
        "step_01_title": "CSV yükle",
        "step_01_copy": "Demo veriyi kullan veya kendi müşteri/profil/işlem dosyanı yükle.",
        "step_02_title": "Kolonları eşleştir",
        "step_02_copy": "Algılanan kolonları kontrol et; dosya yapısı farklıysa eşleştirmeyi düzelt.",
        "step_03_title": "Küme sayısını seç",
        "step_03_copy": "Silhouette önerisini incele; iş yorumu için gerekirse k değerini değiştir.",
        "step_04_title": "İsimlendir ve indir",
        "step_04_copy": "Küme profillerini incele, segmentleri isimlendir ve final CSV’yi indir.",

        # Upload
        "upload_title": "CSV dosyanı yükle",
        "upload_caption": (
            "Müşteri bazlı, profil bazlı veya işlem/sipariş bazlı CSV ile başlayabilirsin. "
            "Gerekirse uygulama kolon eşleştirme adımlarında seni yönlendirir."
        ),
        "upload_label": "Müşteri, profil veya işlem CSV dosyası yükle",
        "file_waiting_warning": "Devam etmek için bir CSV dosyası yükle.",
        "large_file_warning": (
            "Büyük dosyaların işlenmesi daha uzun sürebilir. Kolon eşleştirme genelde hızlıdır; "
            "ancak müşteri özellikleri üretme, silhouette analizi ve KMeans kümeleme "
            "dosya boyutuna ve satır sayısına göre zaman alabilir."
        ),

        # Upload detection / preview
        "detected_upload_type": "Algılanan veri tipi",
        "customer_feature_csv": "Müşteri özellikleri CSV",
        "transaction_csv": "İşlem/sipariş bazlı CSV",
        "customer_profile_csv": "Müşteri profili CSV",
        "unknown_csv": "Bilinmeyen / manuel eşleştirme gerekli",
        "preview_uploaded_data": "Yüklenen veriyi önizle",
        "preview_rows": "Önizleme satır sayısı",
        "column_list": "Kolon listesi",

        # Mapping mode
        "unknown_mapping_warning": (
            "Uygulama CSV yapısını tam olarak algılayamadı. Dosyanı en iyi tarif eden eşleştirme modunu seç."
        ),
        "mapping_mode_question": "Bu CSV nasıl yorumlansın?",
        "transaction_mode": "İşlem/sipariş verisi",
        "profile_mode": "Müşteri profil verisi",

        # Transaction mapping
        "transaction_mapping": "İşlem/sipariş kolon eşleştirme",
        "transaction_mapping_caption": (
            "Her satır bir sipariş, fatura, ürün satırı veya satın alma olayıysa bunu kullan."
        ),
        "transaction_guidance": (
            "İşlem modu, her satır bir sipariş, fatura, ürün satırı veya satın alma olayı olduğunda uygundur. "
            "order_id kolonu yoksa Not selected bırakabilirsin. customer_id kolonu yoksa kullanıcı adı, e-posta, "
            "hesap adı veya müşteri adı gibi sabit bir müşteri tanımlayıcı kolon seçebilirsin."
        ),

        # Profile mapping
        "profile_mapping": "Müşteri profili kolon eşleştirme",
        "profile_mapping_caption": "Her satır zaten tek bir müşteriyi temsil ediyorsa bunu kullan.",
        "profile_guidance": (
            "Profil modu, her satır zaten müşteri özeti olduğunda uygundur. "
            "Eksik opsiyonel alanlar güvenli varsayılanlarla tamamlanır."
        ),
        "profile_recency_missing_warning": (
            "Recency kolonu seçilmedi. Uygulama güvenli varsayılan olarak 0 kullanacak; "
            "ancak veri setinde son satın almadan geçen gün veya son aktivite kolonu varsa "
            "segmentasyon kalitesi artabilir."
        ),

        "segment_size_warning_title": "Segment boyutu uyarısı",
        "segment_size_very_small": (
            "Cluster {cluster_id} müşterilerin yalnızca %{share:.1f}’ini içeriyor. "
            "Bu niş veya aykırı değere benzeyen bir segment olabilir; dikkatli yorumlanmalıdır."
        ),
        "segment_size_small": (
            "Cluster {cluster_id} müşterilerin %{share:.1f}’ini içeriyor. "
            "Bu küçük bir segmenttir; yine de faydalı olabilir ama dikkatli yorumlanmalıdır."
        ),
        "segment_size_dominant": (
            "Cluster {cluster_id} müşterilerin %{share:.1f}’ini içeriyor. "
            "Bu baskın bir segmenttir; seçilen k düşük olabilir veya özellikler müşterileri güçlü şekilde ayırmıyor olabilir."
        ),


        # Feature generation
        "generate_features": "Müşteri özelliklerini üret",
        "customer_feature_detected": (
            "Müşteri seviyesinde özellik CSV’si algılandı. Yüklenen dosya kendi müşteri dağılımına göre kümelenecek."
        ),

        # Clustering
        "uploaded_clustering": "Yüklenen veriyle kümeleme",
        "uploaded_clustering_caption": (
            "Yüklenen dosya kendi içinde kümelenir. Demo model, özel veri setine zorla uygulanmaz."
        ),
        "clustering_setup": "Kümeleme ayarları",
        "clustering_setup_caption": (
            "Teknik olarak en iyi k, silhouette skoru en yüksek olan küme sayısıdır. "
            "İş yorumu için önerilen k ise skor farkı küçükse daha sade ve okunabilir bir segmentasyonu tercih eder. "
            "İstersen bu öneriyi değiştirebilirsin."
        ),
        "technical_best_k": "Teknik olarak en iyi k",
        "business_friendly_k": "İş yorumu için önerilen k",
        "best_silhouette": "En iyi silhouette",
        "selected_clusters": "Seçilen küme sayısı",
        "silhouette_details": "Silhouette detaylarını göster",
        "silhouette_caption": (
            "Bu tablo aday k değerlerini karşılaştırmak için kullanılır. Teknik en iyi k, silhouette skorunu maksimize eder. "
            "İş yorumu için önerilen k, skorlar yakın olduğunda daha sade grupları tercih eder."
        ),
        "active_selected_k": "Aktif seçilen k",
        "active_k_info": (
            "Önerilen k = {recommended_k}, ancak şu anda aktif olarak "
            "k = {selected_k} ile kümeleme yapılıyor."
        ),
        "silhouette_sampling_info": (
            "Silhouette analizi hız için {total_rows:,} müşterinin "
            "{evaluated_rows:,} satırlık temsili örneklemi üzerinde hesaplandı. "
            "Final segment ataması tüm müşterilere uygulanır."
        ),

        # Cluster profiles
        "cluster_profile_before": "İsimlendirme öncesi küme profili",
        "cluster_profile_caption": (
            "Segmentleri isimlendirmeden önce bu tabloyu incele. Recency, frequency, monetary, "
            "müşteri payı ve gelir payını birlikte değerlendir."
        ),
        "name_clusters": "Kümeleri isimlendir",
        "name_clusters_caption": (
            "Varsayılan isimler nötrdür. Küme profilini inceledikten sonra segment isimlerini değiştirebilirsin. "
            "Bu isimler indirilecek CSV’ye uygulanır."
        ),
        "label_for_cluster": "Küme etiketi",
        "custom_labels_success": "Özel segment isimleri grafiklere, tablolara ve indirilecek CSV’ye uygulanır.",

        # Results
        "segmentation_results": "Segmentasyon sonuçları",
        "segmentation_results_caption": (
            "Final müşteri segmentasyonunu incele. Özel segment isimleri grafiklere, tabloya ve indirilecek CSV’ye yansır."
        ),
        "final_cluster_profile": "Final küme profili",
        "pca_view": "Müşteri kümeleri PCA görünümü",
        "pca_caption": (
            "Bu 2D görünüm görsel kontrol içindir; kümeleme algoritmasının kendisi değildir. "
            "Müşteri gruplarının ne kadar ayrıştığını veya örtüştüğünü anlamaya yardım eder."
        ),
        "segmented_customer_data": "Segmentlenmiş müşteri verisi",
        "segmented_customer_caption": "Final müşteri çıktısını indirmeden önce segmentlere göre filtreleyip incele.",
        "filter_by_segment": "Segmente göre filtrele",
        "rows_shown": "Tabloda gösterilen satır sayısı",
        "download_csv": "Segmentlenmiş CSV indir",

        "pca_sampling_info": (
            "Grafiğin daha hızlı çizilmesi için PCA görünümü {total_rows:,} müşterinin "
            "{evaluated_rows:,} satırlık temsili örneklemiyle gösteriliyor. "
            "Final kümeleme, KPI’lar, küme profilleri ve CSV çıktısı tüm müşteriler üzerinden hesaplanır."
        ),

        "segment_insights_title": "Segment yorumları",
        "segment_insights_caption": (
            "Bu kartlar her segmentin önerilen ismini neden aldığını açıklar. "
            "Gösterilen farklar, her kümenin ortalamasını veri seti genel ortalamasıyla karşılaştırır."
        ),
        "segment_drivers_label": "Öne çıkan segment farkları",
        "recency_not_available_note": (
            "Bu veri setinde recency bilgisi gerçek bir kolon olarak gelmediği ve güvenli varsayılanla doldurulduğu için "
            "aktivite zamanı yoruma dahil edilmedi."
        ),

        # Demo
        "demo_loaded": (
            "Demo müşteri segmentasyonu veri seti yüklendi. Upload modu kendi verini ayrıca yeniden kümeleyecek."
        ),
        "demo_overview": "Demo genel bakış",
        "demo_overview_caption": "Bu yerleşik veri seti, CustomerLens BI’ın üretebileceği çıktıyı gösterir.",
        "demo_segment_summary": "Demo segment özeti",
        "demo_segment_caption": (
            "Bu demo yerleşik CustomerLens örnek verisini kullanır. Yüklenen dosyalar ayrıca kümelenir."
        ),
        "business_vs_ml": "İş segmenti vs ML segmenti",
        "business_vs_ml_caption": (
            "Bu karşılaştırma yalnızca demo verisinde vardır; çünkü demo verisi önceden tanımlanmış iş etiketleri içerir."
        ),
        "suggested_segment_label": "Önerilen segment adı",

        "recommended_action_label": "Önerilen aksiyon",

        "segment_charts_title": "Segment grafikleri",
        "segment_charts_caption": (
            "Segment büyüklüğü, gelir katkısı ve ortalama monetary değerini görsel olarak özetler."
        ),
        "download_segments_zip": "Segmentleri ayrı CSV dosyaları olarak indir",

        "chart_customers_by_segment": "Segmente göre müşteri sayısı",
        "chart_revenue_share_by_segment": "Segmente göre gelir payı",
        "chart_avg_monetary_by_segment": "Segmente göre ortalama monetary",
        "chart_customers_axis": "Müşteri sayısı",
        "chart_revenue_share_axis": "Gelir payı",
        "chart_avg_monetary_axis": "Ortalama monetary",

        # Spinners
        "clustering_running": "Kümeleme çalışıyor. Büyük dosyalar biraz zaman alabilir...",
        "preparing_matrix": "Kümeleme matrisi hazırlanıyor...",
        "evaluating_k": "Silhouette skorlarıyla küme sayıları değerlendiriliyor...",
        "running_kmeans": "Final KMeans kümelemesi çalıştırılıyor...",
    },
}


def get_text(language_code):
    return TEXT.get(language_code, TEXT["en"])
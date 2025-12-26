# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np
# from datetime import datetime, timedelta
# from collections import Counter
# import re
# import base64
# from io import StringIO, BytesIO

# # Konfigurasi Halaman
# st.set_page_config(
#     page_title="Analisis Klien Parthaistic",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # CSS Kustom
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #2E86AB;
#         text-align: center;
#         margin-bottom: 2rem;
#         font-weight: bold;
#     }
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         margin: 0.5rem 0;
#         text-align: center;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#     }
#     .insight-box {
#         background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
#         border-left: 5px solid #2E86AB;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .client-card {
#         background: white;
#         border-radius: 15px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#         border-left: 5px solid #2E86AB;
#         transition: transform 0.2s;
#     }
#     .client-card:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
#     }
#     .need-indicator {
#         background: #28a745;
#         color: white;
#         padding: 0.3rem 0.8rem;
#         border-radius: 20px;
#         font-size: 0.8rem;
#         margin: 0.2rem;
#         display: inline-block;
#     }
#     .hashtag-indicator {
#         background: #007bff;
#         color: white;
#         padding: 0.2rem 0.6rem;
#         border-radius: 15px;
#         font-size: 0.75rem;
#         margin: 0.1rem;
#         display: inline-block;
#     }
#     .post-content {
#         background: #f8f9fa;
#         border-radius: 10px;
#         padding: 1rem;
#         margin: 0.5rem 0;
#         border-left: 3px solid #007bff;
#         font-style: italic;
#         max-height: 150px;
#         overflow-y: auto;
#     }
#     .score-high { color: #28a745; font-weight: bold; }
#     .score-medium { color: #ffc107; font-weight: bold; }
#     .score-low { color: #dc3545; font-weight: bold; }
#     .search-box {
#         background: white;
#         border: 2px solid #e9ecef;
#         border-radius: 15px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .download-section {
#         background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
#         border: 2px solid #2196f3;
#         border-radius: 15px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         text-align: center;
#     }
#     .target-client-card {
#         background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
#         border: 2px solid #2196f3;
#         border-radius: 15px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#     }
#     .similar-client-card {
#         background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
#         border: 1px solid #ff9800;
#         border-radius: 15px;
#         padding: 1rem;
#         margin: 0.5rem 0;
#         transition: all 0.3s ease;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .similar-client-card:hover {
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
#         transform: translateY(-2px);
#     }
#     .similarity-score {
#         background: linear-gradient(135deg, #ff9800, #f57c00);
#         color: white;
#         padding: 0.4rem 1rem;
#         border-radius: 25px;
#         font-weight: bold;
#         font-size: 0.9rem;
#         display: inline-block;
#         margin-bottom: 0.5rem;
#     }
#     .client-info-row {
#         display: flex;
#         justify-content: space-between;
#         margin: 0.3rem 0;
#         font-size: 0.9rem;
#     }
#     .client-info-label {
#         font-weight: 600;
#         color: #555;
#     }
#     .client-info-value {
#         color: #333;
#     }
#     .profiling-section {
#         background: #f8f9fa;
#         border-radius: 15px;
#         padding: 2rem;
#         margin: 1rem 0;
#     }
#     .youtube-link {
#         color: #ff0000;
#         text-decoration: none;
#         font-weight: bold;
#         transition: color 0.3s ease;
#     }
#     .youtube-link:hover {
#         color: #cc0000;
#         text-decoration: underline;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Fungsi untuk membuat sample CSV lengkap berdasarkan data Excel
# def create_complete_csv_template():
#     template_data = """Name,Year,Type,Service 1,Service 2,Service 3,Regular End Period,Link Youtube
# Youtubers Depok,2020,Community,Custom Video Production,,,,
# LDK Senada STT NF,2021,Community,Project Musikal Pemuda Indonesia,Video Editor,,,
# Jakarta Youth Choir,2021,Community,Project Musikal Pemuda Indonesia,,,,
# Depok Bercerita,2021,Community,All In Regular,,,2023,https://youtu.be/PBrwimauGUk?si=ODTaGksvck3DdGLz
# PKS Muda,2021,Community,All In Regular,,,2022,
# BIGREDS Depok,2022,Community,Event Documentation,,,,https://youtu.be/06Xk4dQfgts?si=l-bjTagh0lqvLkaV
# PPI UK,2023,Community,Short Video,,,,
# Ikatan Ibu Brantas Abipraya,2023,Community,Event Documentation,,,,
# FSLDK Jadebek,2023,Community,Video Editor,,,,
# Nafkah Community,2023,Community,All In Regular,,,2024,https://youtu.be/-a5iVf8KNkE?si=x-XWtPRNnjHLRD94
# Singing Engineers,2024,Community,Event Documentation,,,,
# Dancing Engineers,2024,Community,Event Documentation,,,,
# Youth Talent Alliance,2024,Community,Video Editor,,,,
# International Madani Association,2025,Community,Video Editor,,,,
# Pulang Production,2020,Corporate,Custom Video Production,,,,
# Rumah Kepemimpinan,2020,Corporate,All In Regular,,,2020,
# Putra Daerah Membangun,2020,Corporate,Video Editor,,,,
# C4Change,2021,Corporate,Video Editor,,,,
# Pahlawan Music School,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
# Duta Futsal,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
# Rabbani,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
# Adhiputro Konsultan Internasional,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
# Mi Studio,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
# Dompet Dhuafa Sumsel,2021,Corporate,Video Editor,,,,https://youtu.be/JSgUUdmGa5Q?si=zp07v_owv9U1FKa8
# Themefood,2021,Corporate,Commercial Video Production,,,,
# Muslimbox,2021,Corporate,Commercial Video Production,,,,
# Indekstat,2021,Corporate,Event Documentation,,,,
# STT NF,2021,Corporate,Company Profile,,,,https://youtu.be/8C_hmTagJc4?si=XH5Qe1VH7wf2neDV
# Magister Manajemen UI,2022,Corporate,E-Learning Video,,,,
# MI Taufiqurrahman 2,2022,Corporate,Event Documentation,Photographer,,,
# Penerbit Luxima,2022,Corporate,Commercial Video Production,,,,
# Top Karir Indonesia,2022,Corporate,Video Editor,,,,
# SMKN 51 Jakarta,2022,Corporate,Workshop,,,,
# Harrington Official Store,2023,Corporate,Commercial Video Production,,,,
# Modernvet,2023,Corporate,Company Profile,,,,
# Teh AI,2023,Corporate,Commercial Video Production,,,,
# OFFO Living,2023,Corporate,Short Video,,,,
# Yayasan Jantung Indonesia,2023,Corporate,Custom Video Production,,,,
# Safia Natural,2023,Corporate,Event Documentation,,,,
# PTQ Griya Quran,2024,Corporate,Company Profile,Event Documentation,,,https://youtu.be/FLxgj5k-MxA?si=R9jSGawS_TaVuoa4
# Konservasi Indonesia,2024,Corporate,Event Documentation,,,,
# Lingkar Keluarga Matahati,2024,Corporate,Custom Video Production,,,,
# Kurita Indonesia,2024,Corporate,Video Editor,,,,
# Klinik Soragan 100 C,2024,Corporate,Video Editor,,,,
# Coway,2024,Corporate,Commercial Video Production,,,,
# SMP Muhammadiyah 2,2024,Corporate,Photographer,,,,
# Yayasan Muda Cemerlang,2025,Corporate,Workshop,,,,
# Rizky Yudo,2020,Figure,All In Regular,,,2026,https://youtu.be/snuAJQ6gFDk?si=Buh0DgIRJprzlW7o
# Oni Sahroni,2020,Figure,All In Regular,,,2020,https://youtu.be/KXRzrjmaJ-8?si=Srl_nYfRaj0MxlzN
# Ibnu Wardani,2021,Figure,Video Editor,,,,https://youtu.be/PqqmHz6pPPQ?si=qdiuq77fbydzk-VO
# Ongky Uktolseja,2021,Figure,Project Musikal Pemuda Indonesia,Video Editor,Videographer,
# Anton,2021,Figure,Video Editor,,,,
# Rizky Januardi,2021,Figure,Video Editor,,,,
# Ash Shiddiq,2021,Figure,Video Editor,,,,
# Imam Budi Hartono,2021,Figure,Short Video,,,,
# The Winfields,2021,Figure,All In Regular,,,2022,https://youtu.be/_CWZxrOrm38?si=W5DtRt4iEYmEW3pl
# The Vanderheydes,2022,Figure,All In Regular,,,2023,https://youtu.be/ehNX8_v-5Qw?si=Xtny4q-N3thEifkH
# Shenina Cinnamon,2022,Figure,Short Video,,,,
# Aqeela Calista,2022,Figure,Short Video,,,,https://youtu.be/beO6JUtri7E?si=Mo7bmdSbDnbW9xvb
# Hanafiah Muhammad,2022,Figure,Video Editor Regular,,,2023,
# Valerie-Veronika TWNS,2022,Figure,All In Regular,,,2022,https://youtu.be/rUX44bQdxYY?si=VtyntCAwypd58Xxz
# Raisa Chairunnisa,2022,Figure,Short Film,,,,
# SRAH,2022,Figure,All In Regular,,,2023,https://youtu.be/zHU8qR18x6g?si=mKF-U9875mDif-vV
# Hanggini,2022,Figure,Short Video,,,,
# Doula Alia,2022,Figure,All In Regular,,,2023,https://youtu.be/USTRbIR-_sA?si=pdhZ4S2HLQOWcmzB
# Jelita,2022,Figure,All In Regular,,,2022,
# Ranty Maria,2022,Figure,Video Editor,,,,
# Michin Family,2022,Figure,Video Editor,Videographer,,
# Nanda Arsyinta,2022,Figure,All In Regular,,,2023,https://youtu.be/85Z12y6b2rk?si=O7VwLpd3etZ-36N-
# Dr. Yuliani Chandranata,2023,Figure,All In Regular,,,2023, https://youtu.be/WD_2ttqJYjE?si=HTvY_9RVIXbFcGkt
# Broto Laras Family,2023,Figure,Custom Video Production,,,,
# Sarah Tumiwa,2023,Figure,All In Regular,,,2023,https://youtu.be/avhjB5mDSeg?si=F9mTogU9aZqEfavx
# Sabrina Anggraini,2023,Figure,Video Editor,,,2023,https://youtu.be/GZYCgCL8GIw?si=BqvesLjtkN6B5Io1
# Jefan Nathanio,2023,Figure,All In Regular,,,2024,https://youtu.be/UIm71CmByzY?si=Hv4324aqA02EGJUc
# Handika Pratama,2023,Figure,Video Editor,Videographer,,
# Zhafira Aqyla,2023,Figure,Event Documentation,Video Editor,,
# DJ Freya,2023,Figure,All In Regular,,,2024,https://youtube.com/@dj_freya?si=hzW60V6H1upKwD2j
# Agatha Chelsea,2023,Figure,Video Editor,,,,https://youtu.be/de0JlcTOOU8?si=QBNNNXI8zGuq9I54
# Luthfi Aulia,2023,Figure,Creative Writer,,,,
# Sabrina Najwa Aulia,2024,Figure,Video Editor,,,,
# Rahmad Junaidi,2024,Figure,All In Regular,,,2024,
# Bang Ghozi,2024,Figure,All In Regular,,,2026,https://youtu.be/bxU9CyNoCxI?si=Mi1sxHcXxPzYrP1P
# BKPM RI,2021,Government,Event Documentation,,,,https://youtu.be/TeHW9ZTC0Qk?si=MOKmOUbi5Kui6Kl4
# Pemkot Depok,2021,Government,All In Regular,Workshop,,2024,
# BPI Kemdikbud RI,2023,Government,Short Video,,,,
# Brantas Abipraya,2023,Government,Event Documentation,,,,
# KKP RI,2024,Government,Event Documentation,,,,
# USAID,2024,Government,Event Documentation,,,,
# WWF Indonesia,2024,Government,Event Documentation,,,,
# Investabook,2024,Government,All In Regular,,,2024,
# DAMRI,2021,SOE,Video Editor,,,,https://youtu.be/hHvHNqwoIbo?si=8qzYQ5Oh52H-O0rU
# TMII,2021,SOE,Project Musikal Pemuda Indonesia,,,,
# BRI,2022,SOE,E-Learning Video,,,,
# Indra Karya,2022,SOE,Video Editor,,,,https://youtu.be/5FLHbEUjSt0?si=leMWatcQ2KrudQ1-
# RSUD ASA Depok,2024,SOE,Company Profile,,,,
# Gag Nikel,2024,SOE,Company Profile,Short Film,Photographer,2025,https://youtu.be/vn5QbfX0iBU?si=QgUxcvK0-mZrMmxG"""
#     return template_data

# # Fungsi untuk mencari klien serupa
# def find_similar_clients(target_client, df, top_n=5):
#     """Mencari klien dengan profil serupa berdasarkan berbagai faktor"""
#     if target_client not in df['Name'].values:
#         return None
    
#     target_row = df[df['Name'] == target_client].iloc[0]
#     similarities = []
    
#     for idx, row in df.iterrows():
#         if row['Name'] == target_client:
#             continue
            
#         similarity_score = 0
        
#         # 1. Kesamaan Tipe Klien (bobot: 30%)
#         if row['Type'] == target_row['Type']:
#             similarity_score += 30
        
#         # 2. Kedekatan Tahun (bobot: 20%)
#         year_diff = abs(row['Year'] - target_row['Year'])
#         if year_diff == 0:
#             similarity_score += 20
#         elif year_diff <= 1:
#             similarity_score += 15
#         elif year_diff <= 2:
#             similarity_score += 10
#         elif year_diff <= 3:
#             similarity_score += 5
        
#         # 3. Kesamaan Layanan (bobot: 30%)
#         target_services = set(target_row['Services'])
#         row_services = set(row['Services'])
        
#         if target_services and row_services:
#             # Jaccard similarity untuk layanan
#             intersection = len(target_services.intersection(row_services))
#             union = len(target_services.union(row_services))
#             if union > 0:
#                 jaccard_similarity = intersection / union
#                 similarity_score += jaccard_similarity * 30
        
#         # 4. Kesamaan Status Loyalitas (bobot: 15%)
#         if row['Is_Loyal'] == target_row['Is_Loyal']:
#             similarity_score += 15
        
#         # 5. Kesamaan Jumlah Layanan (bobot: 5%)
#         service_count_diff = abs(row['Service_Count'] - target_row['Service_Count'])
#         if service_count_diff == 0:
#             similarity_score += 5
#         elif service_count_diff <= 1:
#             similarity_score += 3
        
#         similarities.append({
#             'Name': row['Name'],
#             'Similarity_Score': similarity_score,
#             'Type': row['Type'],
#             'Year': row['Year'],
#             'Services': row['Services'],
#             'Is_Loyal': row['Is_Loyal'],
#             'Link_Youtube': row.get('Link_Youtube', ''),
#             'Service_Count': row['Service_Count']
#         })
    
#     similarities_df = pd.DataFrame(similarities)
#     return similarities_df.nlargest(top_n, 'Similarity_Score')

# # Header utama
# st.markdown('<h1 class="main-header">🎬 Dasbor Analisis Klien Parthaistic</h1>', unsafe_allow_html=True)

# # Load data existing clients
# @st.cache_data
# def load_and_process_data(uploaded_file=None):
#     if uploaded_file is not None:
#         try:
#             # Cek apakah file Excel atau CSV
#             if uploaded_file.name.endswith('.xlsx'):
#                 df = pd.read_excel(uploaded_file)
#             else:
#                 df = pd.read_csv(uploaded_file)
#             st.success("✅ Data berhasil dimuat!")
#         except Exception as e:
#             st.error(f"❌ Error membaca file: {e}")
#             return None
#     else:
#         # Data default - menggunakan data lengkap
#         data = create_complete_csv_template()
#         df = pd.read_csv(StringIO(data))
#         st.info("📄 Menggunakan data default. Upload file CSV/Excel untuk menggunakan data Anda sendiri.")
    
#     # Proses data
#     df['Regular End Period'] = pd.to_numeric(df['Regular End Period'], errors='coerce')
    
#     services = []
#     service_columns = [col for col in df.columns if col.startswith('Service')]
    
#     for _, row in df.iterrows():
#         client_services = []
#         for col in service_columns:
#             if pd.notna(row[col]) and str(row[col]).strip():
#                 client_services.append(str(row[col]).strip())
#         services.append(client_services)
    
#     df['Services'] = services
#     df['Service_Count'] = df['Services'].apply(len)
#     df['Is_Loyal'] = df['Regular End Period'].notna()
#     df['Loyalty_Duration'] = df['Regular End Period'] - df['Year']
#     df['Loyalty_Duration'] = df['Loyalty_Duration'].fillna(0)
    
#     # Rename kolom Link Youtube untuk konsistensi
#     if 'Link Youtube' in df.columns:
#         df = df.rename(columns={'Link Youtube': 'Link_Youtube'})
    
#     return df

# # Area upload file dengan template download
# st.subheader("📁 Upload Data CSV/Excel")

# # Section download template
# st.markdown("""
# <div class="download-section">
#     <h4>📋 Template CSV Format</h4>
#     <p>Download template CSV lengkap dengan semua data klien Parthaistic untuk melihat format yang benar</p>
# </div>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns([1, 1])

# with col1:
#     # Tombol download template CSV lengkap
#     template_csv_data = create_complete_csv_template()
#     st.download_button(
#         label="📥 Download Template CSV Lengkap",
#         data=template_csv_data,
#         file_name="template_klien_parthaistic_lengkap.csv",
#         mime="text/csv",
#         help="Download template dengan semua data klien untuk melihat format yang benar",
#         use_container_width=True
#     )

# with col2:
#     # Informasi format
#     st.info("""
#     **📋 Format Kolom CSV/Excel:**
#     - **Name**: Nama klien/perusahaan
#     - **Year**: Tahun mulai (2020-2025)
#     - **Type**: Corporate/Figure/Community/Government/SOE
#     - **Service 1-3**: Layanan yang digunakan
#     - **Regular End Period**: Tahun berakhir (jika loyal)
#     - **Link Youtube**: Link video YouTube hasil kerja sama
#     """)

# # Upload file
# uploaded_file = st.file_uploader(
#     "Pilih file CSV atau Excel Anda", 
#     type=['csv', 'xlsx'],
#     help="Upload file CSV atau Excel dengan format sesuai template yang dapat didownload di atas"
# )

# # Muat data
# df = load_and_process_data(uploaded_file)

# if df is not None:
#     # Tab Dasbor Utama
#     tab1, tab2, tab3, tab4 = st.tabs([
#         "📊 Gambaran Umum", 
#         "🎯 Profiling Klien", 
#         "🔍 Analisis Klien Loyal", 
#         "💡 Wawasan Bisnis"
#     ])

#     with tab1:
#         st.header("📊 Gambaran Umum Bisnis")
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>{len(df)}</h3>
#                 <p>Total Klien</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             loyal_clients = len(df[df['Is_Loyal']])
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>{loyal_clients}</h3>
#                 <p>Klien Loyal</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col3:
#             loyalty_rate = (loyal_clients / len(df) * 100) if len(df) > 0 else 0
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>{loyalty_rate:.1f}%</h3>
#                 <p>Tingkat Loyalitas</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col4:
#             avg_services = df['Service_Count'].mean()
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>{avg_services:.1f}</h3>
#                 <p>Rata-rata Layanan/Klien</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Grafik distribusi klien
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("📈 Klien berdasarkan Tahun & Tipe")
#             year_type_data = df.groupby(['Year', 'Type']).size().reset_index(name='Count')
#             fig = px.bar(year_type_data, x='Year', y='Count', color='Type',
#                         title="Distribusi Klien berdasarkan Tahun dan Tipe")
#             fig.update_layout(height=400)
#             st.plotly_chart(fig, use_container_width=True)
        
#         with col2:
#             st.subheader("🥧 Distribusi Tipe Klien")
#             type_counts = df['Type'].value_counts()
#             fig = px.pie(values=type_counts.values, names=type_counts.index,
#                         title="Distribusi Tipe Klien")
#             fig.update_layout(height=400)
#             st.plotly_chart(fig, use_container_width=True)

#     with tab2:
#         st.header("🎯 Profiling Klien Tingkat Lanjut")
        
#         # Container untuk profiling
#         st.markdown('<div class="profiling-section">', unsafe_allow_html=True)
        
#         # Bagian pencarian klien serupa
#         st.subheader("🔍 Temukan Klien Serupa")
#         st.markdown("Pilih klien untuk menemukan profil serupa berdasarkan tipe, layanan, tahun, dan status loyalitas:")
        
#         selected_client = st.selectbox(
#             "Pilih klien untuk analisis kesamaan:", 
#             [""] + sorted(df['Name'].tolist()),
#             key="client_similarity_selector"
#         )
        
#         if selected_client:
#             similar_clients = find_similar_clients(selected_client, df, top_n=5)
            
#             if similar_clients is not None and len(similar_clients) > 0:
#                 col1, col2 = st.columns([1, 2])
                
#                 with col1:
#                     # Target client card
#                     target_info = df[df['Name'] == selected_client].iloc[0]
#                     loyalty_status = "Loyal" if target_info['Is_Loyal'] else "Non-loyal"
#                     youtube_link = target_info.get('Link_Youtube', '')
                    
#                     # Membuat link YouTube yang bisa diklik dengan markdown
#                     youtube_display = "Tidak ada"
#                     if youtube_link and str(youtube_link).strip() and str(youtube_link).strip() != 'nan':
#                         youtube_display = f'<a href="{youtube_link}" target="_blank" class="youtube-link">🎬 Tonton Video di YouTube</a>'
                    
#                     st.markdown(f"""
#                     <div class="target-client-card">
#                         <h4>📋 Klien Target</h4>
#                         <h3 style="color: #1976d2; margin: 0.5rem 0;">{selected_client}</h3>
#                         <div class="client-info-row">
#                             <span class="client-info-label">Tipe:</span>
#                             <span class="client-info-value">{target_info['Type']}</span>
#                         </div>
#                         <div class="client-info-row">
#                             <span class="client-info-label">Tahun:</span>
#                             <span class="client-info-value">{target_info['Year']}</span>
#                         </div>
#                         <div class="client-info-row">
#                             <span class="client-info-label">Status:</span>
#                             <span class="client-info-value">{loyalty_status}</span>
#                         </div>
#                         <div class="client-info-row">
#                             <span class="client-info-label">YouTube:</span>
#                             <span class="client-info-value">{youtube_display}</span>
#                         </div>
#                         <div style="margin-top: 1rem;">
#                             <span class="client-info-label">Layanan ({target_info['Service_Count']}):</span><br>
#                             <span class="client-info-value">{', '.join(target_info['Services'])}</span>
#                         </div>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#                 with col2:
#                     # Similar clients
#                     st.markdown("### 🤝 Klien Paling Serupa")
                    
#                     for idx, client in similar_clients.iterrows():
#                         similarity_pct = client['Similarity_Score']
#                         loyalty_status = "Loyal" if client['Is_Loyal'] else "Non-loyal"
#                         youtube_link = client.get('Link_Youtube', '')
                        
#                         # Membuat link YouTube yang bisa diklik
#                         youtube_display = "Tidak ada"
#                         if youtube_link and str(youtube_link).strip() and str(youtube_link).strip() != 'nan':
#                             youtube_display = f'<a href="{youtube_link}" target="_blank" class="youtube-link">🎬 Tonton Video</a>'
                        
#                         # Determine similarity level
#                         if similarity_pct >= 70:
#                             similarity_level = "🔥 Sangat Mirip"
#                             card_style = "background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%); border-color: #4caf50;"
#                         elif similarity_pct >= 50:
#                             similarity_level = "⭐ Cukup Mirip"
#                             card_style = "background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-color: #ff9800;"
#                         else:
#                             similarity_level = "💡 Sedikit Mirip"
#                             card_style = "background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-color: #9c27b0;"
                        
#                         st.markdown(f"""
#                         <div class="similar-client-card" style="{card_style}">
#                             <div class="similarity-score">Kesamaan: {similarity_pct:.1f}% - {similarity_level}</div>
#                             <h4 style="margin: 0.5rem 0; color: #e65100;">{client['Name']}</h4>
#                             <div class="client-info-row">
#                                 <span class="client-info-label">Tipe:</span>
#                                 <span class="client-info-value">{client['Type']}</span>
#                             </div>
#                             <div class="client-info-row">
#                                 <span class="client-info-label">Tahun:</span>
#                                 <span class="client-info-value">{client['Year']}</span>
#                             </div>
#                             <div class="client-info-row">
#                                 <span class="client-info-label">Status:</span>
#                                 <span class="client-info-value">{loyalty_status}</span>
#                             </div>
#                             <div class="client-info-row">
#                                 <span class="client-info-label">YouTube:</span>
#                                 <span class="client-info-value">{youtube_display}</span>
#                             </div>
#                             <div style="margin-top: 0.5rem;">
#                                 <span class="client-info-label">Layanan ({client['Service_Count']}):</span><br>
#                                 <span class="client-info-value">{', '.join(client['Services'])}</span>
#                             </div>
#                         </div>
#                         """, unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Analisis layanan populer
#         st.subheader("🎬 Analisis Popularitas Layanan")
#         all_services = []
#         for services_list in df['Services']:
#             all_services.extend(services_list)
        
#         if all_services:
#             service_counts = pd.Series(all_services).value_counts().head(10)
#             fig = px.bar(x=service_counts.values, y=service_counts.index, orientation='h',
#                         title="10 Layanan Paling Populer")
#             fig.update_layout(height=500)
#             st.plotly_chart(fig, use_container_width=True)

#     with tab3:
#         st.header("🔍 Analisis Klien Loyal")
        
#         loyal_df = df[df['Is_Loyal']].copy()
        
#         if len(loyal_df) > 0:
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("👑 Karakteristik Klien Loyal")
#                 loyal_types = loyal_df['Type'].value_counts()
#                 fig = px.pie(values=loyal_types.values, names=loyal_types.index,
#                             title="Klien Loyal berdasarkan Tipe")
#                 st.plotly_chart(fig, use_container_width=True)
            
#             with col2:
#                 st.subheader("🎬 Layanan Populer Klien Loyal")
#                 loyal_services = []
#                 for services in loyal_df['Services']:
#                     loyal_services.extend(services)
                
#                 if loyal_services:
#                     loyal_service_counts = pd.Series(loyal_services).value_counts().head(8)
#                     fig = px.bar(x=loyal_service_counts.values, y=loyal_service_counts.index, 
#                                 orientation='h', title="Layanan Teratas di Kalangan Klien Loyal")
#                     fig.update_layout(height=400)
#                     st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning("Tidak ada klien loyal yang ditemukan.")

#     with tab4:
#         st.header("💡 Wawasan Bisnis")
        
#         # Generate insights
#         insights = []
        
#         # Analisis tren pertumbuhan
#         yearly_growth = df.groupby('Year').size()
#         if len(yearly_growth) > 1:
#             latest_growth = yearly_growth.iloc[-1] - yearly_growth.iloc[-2]
#             growth_rate = (latest_growth / yearly_growth.iloc[-2]) * 100 if yearly_growth.iloc[-2] > 0 else 0
#             insights.append(f"📈 **Tren Pertumbuhan**: Pertumbuhan klien {growth_rate:+.1f}% dari {yearly_growth.index[-2]} ke {yearly_growth.index[-1]}")
        
#         # Wawasan loyalitas
#         if len(df[df['Is_Loyal']]) > 0:
#             loyalty_rate = len(df[df['Is_Loyal']]) / len(df) * 100
#             insights.append(f"👑 **Tingkat Loyalitas**: {loyalty_rate:.1f}% klien menjadi pelanggan setia")
        
#         # Layanan paling populer
#         if all_services:
#             most_popular_service = pd.Series(all_services).value_counts().index[0]
#             insights.append(f"🌟 **Layanan Paling Populer**: {most_popular_service} adalah layanan yang paling banyak diminta")
        
#         # Analisis klien dengan video YouTube
#         youtube_clients = df[df['Link_Youtube'].notna() & (df['Link_Youtube'] != '')]
#         if len(youtube_clients) > 0:
#             youtube_percentage = len(youtube_clients) / len(df) * 100
#             insights.append(f"🎬 **Portofolio Video**: {len(youtube_clients)} klien ({youtube_percentage:.1f}%) memiliki video YouTube yang dapat ditampilkan")
        
#         # Tampilkan wawasan
#         for insight in insights:
#             st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

# else:
#     st.warning("⚠️ Tidak dapat memuat data. Periksa file CSV/Excel Anda.")

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; color: #666;">
#     <p>🎬 Dasbor Analisis Klien Parthaistic | Client Analytics Dashboard</p>
# </div>
# """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import random
import time
from io import StringIO

# Konfigurasi Halaman
st.set_page_config(
    page_title="Parthaistic - Dashboard Rekomendasi Calon Klien",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom yang lebih menarik dengan animasi
st.markdown("""
<style>
    /* Animasi utama */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink {
        50% { border-color: transparent }
    }
    
    /* Styles utama dengan animasi */
    .main-header {
        font-size: 3.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
        animation: fadeIn 1s ease-out, float 6s ease-in-out infinite;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #4A5568;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
        animation: fadeIn 1.5s ease-out;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: fadeIn 2s ease-out, glow 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 50%,
            transparent 70%
        );
        animation: shimmer 8s infinite linear;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .recommendation-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.5s ease-out;
    }
    
    .recommendation-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        animation: pulse 0.5s ease-out;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #E4405F, #C13584);
        animation: shimmer 2s infinite linear;
    }
    
    .username-badge {
        background: linear-gradient(135deg, #E4405F, #C13584);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(228, 64, 95, 0.2);
        animation: pulse 2s infinite;
    }
    
    .stats-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #2E86AB;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-out;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }
    
    .search-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        margin: 1rem auto;
        animation: glow 2s infinite, pulse 2s infinite;
    }
    
    .search-button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        animation: none;
    }
    
    /* Advanced Loading Animation */
    .loading-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin: 3rem 0;
        padding: 3rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .loading-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(102, 126, 234, 0.1) 50%,
            transparent 70%
        );
        animation: shimmer 3s infinite linear;
    }
    
    .loading-title {
        font-size: 2rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        animation: float 3s ease-in-out infinite;
    }
    
    .loading-subtitle {
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        overflow: hidden;
        white-space: nowrap;
        animation: typing 3.5s steps(40, end), blink .75s step-end infinite;
        border-right: 3px solid #667eea;
    }
    
    .particles {
        display: flex;
        gap: 8px;
    }
    
    .particle {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        animation: bounce 1s infinite ease-in-out;
    }
    
    .particle:nth-child(1) { animation-delay: -0.32s; }
    .particle:nth-child(2) { animation-delay: -0.16s; }
    .particle:nth-child(3) { animation-delay: 0s; }
    .particle:nth-child(4) { animation-delay: 0.16s; }
    .particle:nth-child(5) { animation-delay: 0.32s; }
    
    @keyframes bounce {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.5;
        }
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .progress-bar {
        width: 100%;
        height: 10px;
        background: #e9ecef;
        border-radius: 5px;
        overflow: hidden;
        margin-top: 20px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        width: 0%;
        animation: progress 10s linear forwards;
        border-radius: 5px;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    .loading-stats {
        display: flex;
        gap: 30px;
        margin-top: 20px;
    }
    
    .loading-stat {
        text-align: center;
        animation: fadeIn 2s ease-out;
    }
    
    .loading-stat-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 1s infinite;
    }
    
    .loading-stat-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    /* Floating elements */
    .floating-element {
        position: absolute;
        font-size: 2rem;
        opacity: 0.1;
        animation: float 20s infinite linear;
    }
    
    .floating-1 { top: 10%; left: 5%; animation-delay: 0s; }
    .floating-2 { top: 20%; right: 10%; animation-delay: -5s; }
    .floating-3 { bottom: 30%; left: 15%; animation-delay: -10s; }
    .floating-4 { bottom: 20%; right: 5%; animation-delay: -15s; }
    
    /* Result animations */
    .result-count {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-size: 1.2rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        animation: fadeIn 1s ease-out, pulse 2s infinite;
    }
    
    .refresh-button {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        animation: fadeIn 1s ease-out;
    }
    
    .refresh-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 25px rgba(255, 152, 0, 0.3);
    }
    
    /* Success animation */
    @keyframes success {
        0% { transform: scale(0); opacity: 0; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-animation {
        animation: success 1s ease-out;
    }
    
    /* Empty state with animation */
    .empty-state {
        text-align: center;
        padding: 4rem;
        color: #6c757d;
        animation: fadeIn 1s ease-out;
    }
    
    .empty-state-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        color: #dee2e6;
        animation: float 4s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Data Instagram lengkap (sama seperti sebelumnya)
INSTAGRAM_DATA = """Link Instagram,Username
https://www.instagram.com/mimi.peri/,mimi.peri
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/hanaabas92/,hanaabas92
https://www.instagram.com/kiesha.alvaro/,kiesha.alvaro
https://www.instagram.com/its_lauramoane2/,its_lauramoane2
https://www.instagram.com/elleonora.rika/,elleonora.rika
https://www.instagram.com/aldosinarta/,aldosinarta
https://www.instagram.com/salshabillaadr/,salshabillaadr
https://www.instagram.com/fransiscawdya/,fransiscawdya
https://www.instagram.com/garemcapsoang/,garemcapsoang
https://www.instagram.com/adisurantha/,adisurantha
https://www.instagram.com/zidan.trisnanto/,zidan.trisnanto
https://www.instagram.com/seeforcare/,seeforcare
https://www.instagram.com/snap.nuel/,snap.nuel
https://www.instagram.com/liyanzef/,liyanzef
https://www.instagram.com/claygribble/,claygribble
https://www.instagram.com/converse_id/,converse_id
https://www.instagram.com/deevadep_/,deevadep_
https://www.instagram.com/nicole_rossi_/,nicole_rossi_
https://www.instagram.com/zayyansakha/,zayyansakha
https://www.instagram.com/sinetron.sctv/,sinetron.sctv
https://www.instagram.com/real.hanummegaa/,real.hanummegaa
https://www.instagram.com/saaihalilintar/,saaihalilintar
https://www.instagram.com/opa.jahja/,opa.jahja
https://www.instagram.com/r_marrwt/,r_marrwt
https://www.instagram.com/samudra.taylor/,samudra.taylor
https://www.instagram.com/na1ma._/,na1ma._
https://www.instagram.com/shint_ta/,shint_ta
https://www.instagram.com/arellaraina/,arellaraina
https://www.instagram.com/yasminnapper/,yasminnapper
https://www.instagram.com/randymartinnn/,randymartinnn
https://www.instagram.com/biandanadia/,biandanadia
https://www.instagram.com/danjyohiyoji/,danjyohiyoji
https://www.instagram.com/aisyahaqilahh/,aisyahaqilahh
https://www.instagram.com/naymirdad/,naymirdad
https://www.instagram.com/yndlaurens/,yndlaurens
https://www.instagram.com/keisyalevronka/,keisyalevronka
https://www.instagram.com/andi_nopianto00/,andi_nopianto00
https://www.instagram.com/dindakirana.s/,dindakirana.s
https://www.instagram.com/jeartofa/,jeartofa
https://www.instagram.com/nayo_chio/,nayo_chio
https://www.instagram.com/prencong_jakarta/,prencong_jakarta
https://www.instagram.com/fariz_irawan/,fariz_irawan
https://www.instagram.com/gde_karya69/,gde_karya69
https://www.instagram.com/indridimassinggih/,indridimassinggih
https://www.instagram.com/intan_ahmad/,intan_ahmad
https://www.instagram.com/mulanisanjay/,mulanisanjay
https://www.instagram.com/artistinc.id/,artistinc.id
https://www.instagram.com/santa_paris_jakarta/,santa_paris_jakarta
https://www.instagram.com/av9zs/,av9zs
https://www.instagram.com/stephaniepoetri/,stephaniepoetri
https://www.instagram.com/wildawidy/,wildawidy
https://www.instagram.com/inpower.id/,inpower.id
https://www.instagram.com/farell.akbar11/,farell.akbar11
https://www.instagram.com/saridano/,saridano
https://www.instagram.com/zulfasyamlan/,zulfasyamlan
https://www.instagram.com/rinijuarsa/,rinijuarsa
https://www.instagram.com/chechewe_22/,chechewe_22
https://www.instagram.com/rgy_f/,rgy_f
https://www.instagram.com/fanadnt/,fanadnt
https://www.instagram.com/gadismagz/,gadismagz
https://www.instagram.com/latte_jkt/,latte_jkt
https://www.instagram.com/vita_ngangas/,vita_ngangas
https://www.instagram.com/delanodaniel/,delanodaniel
https://www.instagram.com/babby_key_nahd/,babby_key_nahd
https://www.instagram.com/cantik_shalzabillah/,cantik_shalzabillah
https://www.instagram.com/m.husnanhabib/,m.husnanhabib
https://www.instagram.com/pm_photoworks/,pm_photoworks
https://www.instagram.com/nadafikalopurba/,nadafikalopurba
https://www.instagram.com/zahralarafi/,zahralarafi
https://www.instagram.com/patriciagouw/,patriciagouw
https://www.instagram.com/faul.gayo19/,faul.gayo19
https://www.instagram.com/aliffarrasya21/,aliffarrasya21
https://www.instagram.com/gabriellacawley2/,gabriellacawley2
https://www.instagram.com/queenvalishaa/,queenvalishaa
https://www.instagram.com/ramzialmuzaki_/,ramzialmuzaki_
https://www.instagram.com/amesharianty_/,amesharianty_
https://www.instagram.com/winstongomez/,winstongomez
https://www.instagram.com/mumtaz.raffy/,mumtaz.raffy
https://www.instagram.com/wulanpurwanti89/,wulanpurwanti89
https://www.instagram.com/yourminbite/,yourminbite
https://www.instagram.com/audymaulidyna/,audymaulidyna
https://www.instagram.com/byputy/,byputy
https://www.instagram.com/jessavanathan/,jessavanathan
https://www.instagram.com/arasha.skater/,arasha.skater
https://www.instagram.com/viansfn/,viansfn
https://www.instagram.com/zzieie/,zzieie
https://www.instagram.com/ktriana10/,ktriana10
https://www.instagram.com/nevytaania/,nevytaania
https://www.instagram.com/ryanpitna/,ryanpitna
https://www.instagram.com/syanaalha/,syanaalha
https://www.instagram.com/asha.assuncao/,asha.assuncao
https://www.instagram.com/gemavya__/,gemavya__
https://www.instagram.com/ridho.firmansyahhh/,ridho.firmansyahhh
https://www.instagram.com/novriinayati/,novriinayati
https://www.instagram.com/bremagintings/,bremagintings
https://www.instagram.com/citrazein/,citrazein
https://www.instagram.com/radhsvi/,radhsvi
https://www.instagram.com/patricia_angelie_tan/,patricia_angelie_tan
https://www.instagram.com/davidsuwarto/,davidsuwarto
https://www.instagram.com/endri_sano/,endri_sano
https://www.instagram.com/bapack2pesonk/,bapack2pesonk
https://www.instagram.com/gloowandbe/,gloowandbe
https://www.instagram.com/salwastwti/,salwastwti
https://www.instagram.com/queency.alycia/,queency.alycia
https://www.instagram.com/ersa_puspa/,ersa_puspa
https://www.instagram.com/isabel.azhari/,isabel.azhari
https://www.instagram.com/aryamohan7/,aryamohan7
https://www.instagram.com/almer_vicko/,almer_vicko
https://www.instagram.com/azizi.althaf/,azizi.althaf
https://www.instagram.com/dndabrlyn09/,dndabrlyn09
https://www.instagram.com/_dimasputt/,_dimasputt
https://www.instagram.com/allyciasyllm/,allyciasyllm
https://www.instagram.com/naldyf/,naldyf
https://www.instagram.com/aimanameeraa/,aimanameeraa
https://www.instagram.com/mikha_hernan/,mikha_hernan
https://www.instagram.com/aya.mazayaa/,aya.mazayaa
https://www.instagram.com/aliefindr/,aliefindr
https://www.instagram.com/papabearwisnu/,papabearwisnu
https://www.instagram.com/dimas.agsa/,dimas.agsa
https://www.instagram.com/jrocks.official/,jrocks.official
https://www.instagram.com/ranieroo/,ranieroo
https://www.instagram.com/reginafransissca/,reginafransissca
https://www.instagram.com/gabrihella_/,gabrihella_
https://www.instagram.com/ramlihursan/,ramlihursan
https://www.instagram.com/azzurabisyir/,azzurabisyir
https://www.instagram.com/sandro_karamoy/,sandro_karamoy
https://www.instagram.com/paca.sweetandsavory/,paca.sweetandsavory
https://www.instagram.com/shennyra/,shennyra
https://www.instagram.com/juliastv2015/,juliastv2015
https://www.instagram.com/mrizkyra_/,mrizkyra_
https://www.instagram.com/eddy_mm/,eddy_mm
https://www.instagram.com/andreriva77/,andreriva77
https://www.instagram.com/anggaharyono_/,anggaharyono_
https://www.instagram.com/suciasabrina/,suciasabrina
https://www.instagram.com/mia_kalipancur/,mia_kalipancur
https://www.instagram.com/sutisnaagus523/,sutisnaagus523
https://www.instagram.com/bindusamtani/,bindusamtani
https://www.instagram.com/razanzu/,razanzu
https://www.instagram.com/raniabisyir/,raniabisyir
https://www.instagram.com/masnanda___/,masnanda___
https://www.instagram.com/windyhartanto/,windyhartanto
https://www.instagram.com/kaktyann/,kaktyann
https://www.instagram.com/mikhayla_rezky/,mikhayla_rezky
https://www.instagram.com/sitiwiryani/,sitiwiryani
https://www.instagram.com/zaza_seca/,zaza_seca
https://www.instagram.com/m_ara1950/,m_ara1950
https://www.instagram.com/karissa_meme/,karissa_meme
https://www.instagram.com/bintangsci/,bintangsci
https://www.instagram.com/michellechrlt_/,michellechrlt_
https://www.instagram.com/raniasalsabilaazzahra/,raniasalsabilaazzahra
https://www.instagram.com/hanzhp/,hanzhp
https://www.instagram.com/azaclothing.co/,azaclothing.co
https://www.instagram.com/zavieraa.co/,zavieraa.co
https://www.instagram.com/shahnazbsyr/,shahnazbsyr
https://www.instagram.com/izzatassegaf/,izzatassegaf
https://www.instagram.com/meytariarosalina/,meytariarosalina
https://www.instagram.com/jadenbahtera/,jadenbahtera
https://www.instagram.com/antokaunang/,antokaunang
https://www.instagram.com/yogidarmawansyah96/,yogidarmawansyah96
https://www.instagram.com/magejibril/,magejibril
https://www.instagram.com/bazaarin.id/,bazaarin.id
https://www.instagram.com/fattsyach/,fattsyach
https://www.instagram.com/vaniapriscilla.real/,vaniapriscilla.real
https://www.instagram.com/tennyaininnisa/,tennyaininnisa
https://www.instagram.com/ammar.mahija.razzaq/,ammar.mahija.razzaq
https://www.instagram.com/alejandro.cool/,alejandro.cool
https://www.instagram.com/xavieraalanna/,xavieraalanna
https://www.instagram.com/sintadella.real/,sintadella.real
https://www.instagram.com/alejandromarianoo/,alejandromarianoo
https://www.instagram.com/nenarosier/,nenarosier
https://www.instagram.com/dickymakeup/,dickymakeup
https://www.instagram.com/wasrinita/,wasrinita
https://www.instagram.com/ikrarsr/,ikrarsr
https://www.instagram.com/gitapanhar/,gitapanhar
https://www.instagram.com/melodyamanda_25/,melodyamanda_25
https://www.instagram.com/gwella.id/,gwella.id
https://www.instagram.com/auleenn/,auleenn
https://www.instagram.com/elissa_haddadxx/,elissa_haddadxx
https://www.instagram.com/jokonugroho2115/,jokonugroho2115
https://www.instagram.com/jihanrnt1/,jihanrnt1
https://www.instagram.com/asmaragt/,asmaragt
https://www.instagram.com/matthewkenevan/,matthewkenevan
https://www.instagram.com/dayangida_instyle/,dayangida_instyle
https://www.instagram.com/dafauguciano/,dafauguciano
https://www.instagram.com/hilgadoui/,hilgadoui
https://www.instagram.com/keeamacleod/,keeamacleod
https://www.instagram.com/aqeeverss_1406/,aqeeverss_1406
https://www.instagram.com/andilagii/,andilagii
https://www.instagram.com/alanamusicofficial/,alanamusicofficial
https://www.instagram.com/agustia_nursiti/,agustia_nursiti
https://www.instagram.com/zafiraadelia/,zafiraadelia
https://www.instagram.com/aldyqullriz/,aldyqullriz
https://www.instagram.com/arumakhadijah/,arumakhadijah
https://www.instagram.com/firmannnf/,firmannnf
https://www.instagram.com/nadya.yusuf/,nadya.yusuf
https://www.instagram.com/itsichey/,itsichey
https://www.instagram.com/houseofdimassinggih/,houseofdimassinggih
https://www.instagram.com/ammarmahijarazzaq/,ammarmahijarazzaq
https://www.instagram.com/neysachandria/,neysachandria
https://www.instagram.com/xxayukar_/,xxayukar_
https://www.instagram.com/dinda.ghaniaa/,dinda.ghaniaa
https://www.instagram.com/gitapilar/,gitapilar
https://www.instagram.com/jojoohalim/,jojoohalim
https://www.instagram.com/felix.hasibuan/,felix.hasibuan
https://www.instagram.com/audreyralinka/,audreyralinka
https://www.instagram.com/fauzanharish/,fauzanharish
https://www.instagram.com/therealfidiany/,therealfidiany
https://www.instagram.com/asyaroh.98/,asyaroh.98
https://www.instagram.com/evifebriyantii/,evifebriyantii
https://www.instagram.com/faruxruxli/,faruxruxli
https://www.instagram.com/srnentertainment_official/,srnentertainment_official
https://www.instagram.com/megarymnd/,megarymnd
https://www.instagram.com/edwinstevenl/,edwinstevenl
https://www.instagram.com/andyw24_/,andyw24_
https://www.instagram.com/idahaddad/,idahaddad
https://www.instagram.com/valdyp_s7ven/,valdyp_s7ven
https://www.instagram.com/blackantgamestation/,blackantgamestation
https://www.instagram.com/ratuurafa/,ratuurafa
https://www.instagram.com/braynlim/,braynlim
https://www.instagram.com/polinviona/,polinviona
https://www.instagram.com/rbananto/,rbananto
https://www.instagram.com/aridanik76/,aridanik76
https://www.instagram.com/riskaftriaa_/,riskaftriaa_
https://www.instagram.com/syifakamaliaa_/,syifakamaliaa_
https://www.instagram.com/drina07/,drina07
https://www.instagram.com/alunarizk/,alunarizk
https://www.instagram.com/reyromy98/,reyromy98
https://www.instagram.com/putrigitaaaa___/,putrigitaaaa___
https://www.instagram.com/raisamariee_/,raisamariee_
https://www.instagram.com/citraa1121/,citraa1121
https://www.instagram.com/aa_ahmad/,aa_ahmad
https://www.instagram.com/khosyi_aidillana/,khosyi_aidillana
https://www.instagram.com/nopekkk/,nopekkk
https://www.instagram.com/androtrinanda/,androtrinanda
https://www.instagram.com/nanang_khan/,nanang_khan
https://www.instagram.com/yusufyudo/,yusufyudo
https://www.instagram.com/dapoermaemun/,dapoermaemun
https://www.instagram.com/candra_ngan/,candra_ngan
https://www.instagram.com/avhiedop/,avhiedop
https://www.instagram.com/silvansaputra/,silvansaputra
https://www.instagram.com/jameshartono/,jameshartono
https://www.instagram.com/jisunkang_/,jisunkang_
https://www.instagram.com/richelprabarini/,richelprabarini
https://www.instagram.com/youmnald/,youmnald
https://www.instagram.com/angga_sastro/,angga_sastro
https://www.instagram.com/harry.vghn/,harry.vghn
https://www.instagram.com/lovelysilvia_/,lovelysilvia_
https://www.instagram.com/rhyawilko/,rhyawilko
https://www.instagram.com/f.talithaa/,f.talithaa
https://www.instagram.com/taufik.t7/,taufik.t7
https://www.instagram.com/ditodarmawan__/,ditodarmawan__
https://www.instagram.com/nduthspears/,nduthspears
https://www.instagram.com/revimasyitaaa/,revimasyitaaa
https://www.instagram.com/aqueneazizdjorghi/,aqueneazizdjorghi
https://www.instagram.com/ichsanrindengan/,ichsanrindengan
https://www.instagram.com/susan_rossi_/,susan_rossi_
https://www.instagram.com/hayu_pangastuti/,hayu_pangastuti
https://www.instagram.com/ammarsyahdi/,ammarsyahdi
https://www.instagram.com/mickomentari/,mickomentari
https://www.instagram.com/bertram_beryl/,bertram_beryl
https://www.instagram.com/sanyandsusanti/,sanyandsusanti
https://www.instagram.com/kickmanagement.id/,kickmanagement.id
https://www.instagram.com/oneshotonekill.camera/,oneshotonekill.camera
https://www.instagram.com/sinemart_ph/,sinemart_ph
https://www.instagram.com/falconpictures_/,falconpictures_
https://www.instagram.com/rassyahidayahreal/,rassyahidayahreal
https://www.instagram.com/andrewxbarrett/,andrewxbarrett
https://www.instagram.com/syaradivaazima/,syaradivaazima
https://www.instagram.com/deankhalil/,deankhalil
https://www.instagram.com/denyssimon/,denyssimon
https://www.instagram.com/adriankhalif/,adriankhalif
https://www.instagram.com/_william_xu/,_william_xu
https://www.instagram.com/siscamagdalena_/,siscamagdalena_
https://www.instagram.com/diandraich/,diandraich
https://www.instagram.com/anggayoya/,anggayoya
https://www.instagram.com/putrirahay/,putrirahay
https://www.instagram.com/pratiwinurel/,pratiwinurel
https://www.instagram.com/sulaimanbsyr/,sulaimanbsyr
https://www.instagram.com/sastra.silalahii/,sastra.silalahii
https://www.instagram.com/rahmaniarrusnan/,rahmaniarrusnan
https://www.instagram.com/nuradatau/,nuradatau
https://www.instagram.com/narulita_maharani/,narulita_maharani
https://www.instagram.com/tristan_alif_naufal/,tristan_alif_naufal
https://www.instagram.com/mrs.rani_tdj/,mrs.rani_tdj
https://www.instagram.com/yuriwa_0811/,yuriwa_0811
https://www.instagram.com/baselxendra/,baselxendra
https://www.instagram.com/shalby08/,shalby08
https://www.instagram.com/tasyacarlla27/,tasyacarlla27
https://www.instagram.com/rendiputrasetiawan/,rendiputrasetiawan
https://www.instagram.com/ricky_zakno/,ricky_zakno
https://www.instagram.com/iduradewijaya/,iduradewijaya
https://www.instagram.com/dewisaputra83/,dewisaputra83
https://www.instagram.com/ziziezidane/,ziziezidane
https://www.instagram.com/naufala2/,naufala2
https://www.instagram.com/meliza_hutasoit/,meliza_hutasoit
https://www.instagram.com/alfaris_1818/,alfaris_1818
https://www.instagram.com/official.aqeevers/,official.aqeevers
https://www.instagram.com/antonjrocks.kelces/,antonjrocks.kelces
https://www.instagram.com/sabrinabisyirr/,sabrinabisyirr
https://www.instagram.com/ghinarai/,ghinarai
https://www.instagram.com/xandrahardian/,xandrahardian
https://www.instagram.com/upie_samsimar/,upie_samsimar
https://www.instagram.com/putrasiregarr17/,putrasiregarr17
https://www.instagram.com/yoongimenez/,yoongimenez
https://www.instagram.com/prialangga_/,prialangga_
https://www.instagram.com/bimasenaprisai_/,bimasenaprisai_
https://www.instagram.com/imelda_lubis9/,imelda_lubis9
https://www.instagram.com/ney_neo/,ney_neo
https://www.instagram.com/ranggayusuf/,ranggayusuf
https://www.instagram.com/sheilakusnadi_/,sheilakusnadi_
https://www.instagram.com/willyjn15/,willyjn15
https://www.instagram.com/kanmogroup.fashion/,kanmogroup.fashion
https://www.instagram.com/sheemar_rahman/,sheemar_rahman
https://www.instagram.com/rafidahalatas/,rafidahalatas
https://www.instagram.com/adli_umar/,adli_umar
https://www.instagram.com/dude2harlino/,dude2harlino
https://www.instagram.com/nabilazaviraa_/,nabilazaviraa_
https://www.instagram.com/flaviozavieraa/,flaviozavieraa
https://www.instagram.com/azxtha/,azxtha
https://www.instagram.com/washeudee/,washeudee
https://www.instagram.com/cantikaaputrikirana/,cantikaaputrikirana
https://www.instagram.com/danieltito13/,danieltito13
https://www.instagram.com/bnhimawan/,bnhimawan
https://www.instagram.com/tha2_nez/,tha2_nez
https://www.instagram.com/diansidik_/,diansidik_
https://www.instagram.com/chairul.giano/,chairul.giano
https://www.instagram.com/irien_heriyanto/,irien_heriyanto
https://www.instagram.com/ratusfy_/,ratusfy_
https://www.instagram.com/sabrinasoetomo/,sabrinasoetomo
https://www.instagram.com/rezadpy/,rezadpy
https://www.instagram.com/diva.mn/,diva.mn
https://www.instagram.com/umamap2/,umamap2
https://www.instagram.com/moedjenan/,moedjenan
https://www.instagram.com/oki.hartanto/,oki.hartanto
https://www.instagram.com/zolada_mum/,zolada_mum
https://www.instagram.com/madeardanaofficial/,madeardanaofficial
https://www.instagram.com/kimmyyyyy.kim/,kimmyyyyy.kim
https://www.instagram.com/delon_mercy_/,delon_mercy_
https://www.instagram.com/mike.lucock/,mike.lucock
https://www.instagram.com/yudetraaj/,yudetraaj
https://www.instagram.com/shendykarunia_/,shendykarunia_
https://www.instagram.com/zheyamada_/,zheyamada_
https://www.instagram.com/tamarasyarief/,tamarasyarief
https://www.instagram.com/hauralathifarz/,hauralathifarz
https://www.instagram.com/andrewchriz/,andrewchriz
https://www.instagram.com/nonaeurny/,nonaeurny
https://www.instagram.com/diraamel/,diraamel
https://www.instagram.com/roymagny/,roymagny
https://www.instagram.com/ikkedspt/,ikkedspt
https://www.instagram.com/lindasaibi/,lindasaibi
https://www.instagram.com/nadiaraysa/,nadiaraysa
https://www.instagram.com/devhianrhasan/,devhianrhasan
https://www.instagram.com/chelseaconcheta/,chelseaconcheta
https://www.instagram.com/albielatief/,albielatief
https://www.instagram.com/kartikaputr/,kartikaputr
https://www.instagram.com/wetvindonesia/,wetvindonesia
https://www.instagram.com/ibamadr/,ibamadr
https://www.instagram.com/riizkkaaay/,riizkkaaay
https://www.instagram.com/kimora_razi/,kimora_razi
https://www.instagram.com/ebasheba/,ebasheba
https://www.instagram.com/sriwadebarrett/,sriwadebarrett
https://www.instagram.com/nadialaydrus/,nadialaydrus
https://www.instagram.com/dyah_gayatri/,dyah_gayatri
https://www.instagram.com/shofia_shireen/,shofia_shireen
https://www.instagram.com/mayangwulansantoso/,mayangwulansantoso
https://www.instagram.com/ms.pipit_puspitawardhaniadjie/,ms.pipit_puspitawardhaniadjie
https://www.instagram.com/_darimatakemata/,_darimatakemata
https://www.instagram.com/jscamandy/,jscamandy
https://www.instagram.com/qheylazv/,qheylazv
https://www.instagram.com/nadhifbasalamah/,nadhifbasalamah
https://www.instagram.com/rhiofaldo/,rhiofaldo
https://www.instagram.com/nafisahnjlaa/,nafisahnjlaa
https://www.instagram.com/baetzmanagement/,baetzmanagement
https://www.instagram.com/zorayaudri/,zorayaudri
https://www.instagram.com/deniirawan1981/,deniirawan1981
https://www.instagram.com/rennov3011/,rennov3011
https://www.instagram.com/ebel_cobra/,ebel_cobra
https://www.instagram.com/falconmusic/,falconmusic
https://www.instagram.com/dienz_36/,dienz_36
https://www.instagram.com/lesleyvs/,lesleyvs
https://www.instagram.com/leciel.design/,leciel.design
https://www.instagram.com/alineefziah/,alineefziah
https://www.instagram.com/haedy_dot/,haedy_dot
https://www.instagram.com/joe_chandra28/,joe_chandra28
https://www.instagram.com/nowayisthataki/,nowayisthataki
https://www.instagram.com/angelinacortizo/,angelinacortizo
https://www.instagram.com/naylayuu/,naylayuu
https://www.instagram.com/ichanvirgo_new/,ichanvirgo_new
https://www.instagram.com/yudhahehehe/,yudhahehehe
https://www.instagram.com/diniajah12/,diniajah12
https://www.instagram.com/jay82sandy/,jay82sandy
https://www.instagram.com/williamroberts08/,williamroberts08
https://www.instagram.com/almanuraaa/,almanuraaa
https://www.instagram.com/lutfihasby/,lutfihasby
https://www.instagram.com/mryogiepratama/,mryogiepratama
https://www.instagram.com/harunempenk/,harunempenk
https://www.instagram.com/reza.ekas/,reza.ekas
https://www.instagram.com/rurypadwa/,rurypadwa
https://www.instagram.com/yehuda.gilbert/,yehuda.gilbert
https://www.instagram.com/dindaaaaa.17/,dindaaaaa.17
https://www.instagram.com/kiaramckenna/,kiaramckenna
https://www.instagram.com/feliciablancomua/,feliciablancomua
https://www.instagram.com/kamilrff/,kamilrff
https://www.instagram.com/arry_dharyanto/,arry_dharyanto
https://www.instagram.com/andikapangestu19/,andikapangestu19
https://www.instagram.com/viecawley/,viecawley
https://www.instagram.com/kangadetalco/,kangadetalco
https://www.instagram.com/jinan.safaa/,jinan.safaa
https://www.instagram.com/svastiari/,svastiari
https://www.instagram.com/kenyolw/,kenyolw
https://www.instagram.com/ajeng_faradita/,ajeng_faradita
https://www.instagram.com/lintangamel/,lintangamel
https://www.instagram.com/medigerdiandi/,medigerdiandi
https://www.instagram.com/teukuanwar/,teukuanwar
https://www.instagram.com/keanurne/,keanurne
https://www.instagram.com/brideseries/,brideseries
https://www.instagram.com/riz.basey/,riz.basey
https://www.instagram.com/hiitstheoo/,hiitstheoo
https://www.instagram.com/un1ty_official/,un1ty_official
https://www.instagram.com/ariksyach/,ariksyach
https://www.instagram.com/ronny_irawan/,ronny_irawan
https://www.instagram.com/hairbyranggayusuf/,hairbyranggayusuf
https://www.instagram.com/bungafathia06/,bungafathia06
https://www.instagram.com/silvyprajogo/,silvyprajogo
https://www.instagram.com/bunda.latinas/,bunda.latinas
https://www.instagram.com/thecataracs/,thecataracs
https://www.instagram.com/bravyson.vconk/,bravyson.vconk
https://www.instagram.com/acidlineave/,acidlineave
https://www.instagram.com/kaay.raw/,kaay.raw
https://www.instagram.com/richardricardoo/,richardricardoo
https://www.instagram.com/titipdongkak_reborn/,titipdongkak_reborn
https://www.instagram.com/okintph/,okintph
https://www.instagram.com/snap.nuel/,snap.nuel
https://www.instagram.com/adlianesa/,adlianesa
https://www.instagram.com/nickyromero/,nickyromero
https://www.instagram.com/greg11n/,greg11n
https://www.instagram.com/revelation.stage/,revelation.stage
https://www.instagram.com/wowshack/,wowshack
https://www.instagram.com/aldosinarta/,aldosinarta
https://www.instagram.com/warkop.rinjani/,warkop.rinjani
https://www.instagram.com/the.atami/,the.atami
https://www.instagram.com/seiru0711/,seiru0711
https://www.instagram.com/audien/,audien
https://www.instagram.com/yuliabaltschun/,yuliabaltschun
https://www.instagram.com/noizemafia/,noizemafia
https://www.instagram.com/adindapuri/,adindapuri
https://www.instagram.com/lunpharrin/,lunpharrin
https://www.instagram.com/tchindaeliza/,tchindaeliza
https://www.instagram.com/vercit/,vercit
https://www.instagram.com/nareend/,nareend
https://www.instagram.com/yoshehairdo/,yoshehairdo
https://www.instagram.com/sabrinasameh/,sabrinasameh
https://www.instagram.com/bossybabe.id/,bossybabe.id
https://www.instagram.com/prettycia.official/,prettycia.official
https://www.instagram.com/kodkushi/,kodkushi
https://www.instagram.com/alyafrcn/,alyafrcn
https://www.instagram.com/thelist.bali/,thelist.bali
https://www.instagram.com/maria.ishida/,maria.ishida
https://www.instagram.com/kshmr/,kshmr
https://www.instagram.com/zai_cafe/,zai_cafe
https://www.instagram.com/__star101__/,__star101__
https://www.instagram.com/supirdieropa/,supirdieropa
https://www.instagram.com/christamcqueen.mua/,christamcqueen.mua
https://www.instagram.com/riskylaskyyy/,riskylaskyyy
https://www.instagram.com/ridho.ghonim/,ridho.ghonim
https://www.instagram.com/irliewijanarko/,irliewijanarko
https://www.instagram.com/vilotisss/,vilotisss
https://www.instagram.com/iniadzwaaurell/,iniadzwaaurell
https://www.instagram.com/eby.adinata/,eby.adinata
https://www.instagram.com/uncle.yama/,uncle.yama
https://www.instagram.com/medidecil/,medidecil
https://www.instagram.com/micellehalim/,micellehalim
https://www.instagram.com/life.ofgie/,life.ofgie
https://www.instagram.com/yaya_loves_youuu/,yaya_loves_youuu
https://www.instagram.com/anastasia_audreysc/,anastasia_audreysc
https://www.instagram.com/squillliams/,squillliams
https://www.instagram.com/indraparuga/,indraparuga
https://www.instagram.com/emmamadan/,emmamadan
https://www.instagram.com/creafein/,creafein
https://www.instagram.com/jorenzojonathan/,jorenzojonathan
https://www.instagram.com/viggyvino/,viggyvino
https://www.instagram.com/polina.a/,polina.a
https://www.instagram.com/javaphile96/,javaphile96
https://www.instagram.com/thaliaandini/,thaliaandini
https://www.instagram.com/pipigawww/,pipigawww
https://www.instagram.com/missgrandindonesiaofficial/,missgrandindonesiaofficial
https://www.instagram.com/rellkeyy/,rellkeyy
https://www.instagram.com/stampcase.bali/,stampcase.bali
https://www.instagram.com/ayy_andriana/,ayy_andriana
https://www.instagram.com/eizamaghfira/,eizamaghfira
https://www.instagram.com/umaisoumaima/,umaisoumaima
https://www.instagram.com/vtapritia/,vtapritia
https://www.instagram.com/mtriamustika/,mtriamustika
https://www.instagram.com/_sammaxx_/,_sammaxx_
https://www.instagram.com/ariefayip_/,ariefayip_
https://www.instagram.com/nurafarhanaaa/,nurafarhanaaa
https://www.instagram.com/_lukichova_/,_lukichova_
https://www.instagram.com/fathirbahanan/,fathirbahanan
https://www.instagram.com/harishfadhil/,harishfadhil
https://www.instagram.com/fatimahshirin._/,fatimahshirin._
https://www.instagram.com/_forrise/,_forrise
https://www.instagram.com/_haziqj/,_haziqj
https://www.instagram.com/bams_pattikawa/,bams_pattikawa
https://www.instagram.com/wonderbluefreedive/,wonderbluefreedive
https://www.instagram.com/fadithya01/,fadithya01
https://www.instagram.com/diphabarus/,diphabarus
https://www.instagram.com/dimasbestari/,dimasbestari
https://www.instagram.com/reksanalendra/,reksanalendra
https://www.instagram.com/iara.music_/,iara.music_
https://www.instagram.com/iamsararena/,iamsararena
https://www.instagram.com/kumalaambar/,kumalaambar
https://www.instagram.com/frkhayla/,frkhayla
https://www.instagram.com/louisreyner6/,louisreyner6
https://www.instagram.com/_nugeeee/,_nugeeee
https://www.instagram.com/tim_aditya/,tim_aditya
https://www.instagram.com/dv_chivu/,dv_chivu
https://www.instagram.com/edurinaldy/,edurinaldy
https://www.instagram.com/keanu.js/,keanu.js
https://www.instagram.com/lilchindoboi/,lilchindoboi
https://www.instagram.com/dj.fanya/,dj.fanya
https://www.instagram.com/wirsarrr/,wirsarrr
https://www.instagram.com/ghinageriz/,ghinageriz
https://www.instagram.com/rezzarizr/,rezzarizr
https://www.instagram.com/rukes/,rukes
https://www.instagram.com/andryesetiawan/,andryesetiawan
https://www.instagram.com/zicoazi/,zicoazi
https://www.instagram.com/ivana.dusarduyn/,ivana.dusarduyn
https://www.instagram.com/mitchslorach/,mitchslorach
https://www.instagram.com/jelitajee/,jelitajee
https://www.instagram.com/dudutdj/,dudutdj
https://www.instagram.com/nntysxmusic/,nntysxmusic
https://www.instagram.com/nissaoktora/,nissaoktora
https://www.instagram.com/joodakota/,joodakota
https://www.instagram.com/stephenwira/,stephenwira
https://www.instagram.com/kikodwk/,kikodwk
https://www.instagram.com/vifalksatria/,vifalksatria
https://www.instagram.com/cannyclaudya/,cannyclaudya
https://www.instagram.com/kimm.id/,kimm.id
https://www.instagram.com/juliakristie/,juliakristie
https://www.instagram.com/errikirre/,errikirre
https://www.instagram.com/matsumotong/,matsumotong
https://www.instagram.com/joelbanget/,joelbanget
https://www.instagram.com/mhdalfrzl/,mhdalfrzl
https://www.instagram.com/aydra/,aydra
https://www.instagram.com/haryotejo/,haryotejo
https://www.instagram.com/robstee_/,robstee_
https://www.instagram.com/michellejesicaa/,michellejesicaa
https://www.instagram.com/hi.gab/,hi.gab
https://www.instagram.com/damabdz/,damabdz
https://www.instagram.com/sarasabila/,sarasabila
https://www.instagram.com/raramispawanti/,raramispawanti
https://www.instagram.com/sundaysundaemusic/,sundaysundaemusic
https://www.instagram.com/sayhitojesse/,sayhitojesse
https://www.instagram.com/m0r3nd/,m0r3nd
https://www.instagram.com/ivonnemadlenec/,ivonnemadlenec
https://www.instagram.com/dhenadf/,dhenadf
https://www.instagram.com/jirosamin/,jirosamin
https://www.instagram.com/irfiorent/,irfiorent
https://www.instagram.com/nadia.vecchi/,nadia.vecchi
https://www.instagram.com/adstrwn/,adstrwn
https://www.instagram.com/findmevilla/,findmevilla
https://www.instagram.com/yakobuz1/,yakobuz1
https://www.instagram.com/windy_lazuardi/,windy_lazuardi
https://www.instagram.com/tanamur.jpeg/,tanamur.jpeg
https://www.instagram.com/brianrmadhann/,brianrmadhann
https://www.instagram.com/djumcollect/,djumcollect
https://www.instagram.com/deyn.al/,deyn.al
https://www.instagram.com/suedeshots/,suedeshots
https://www.instagram.com/er_erlangga/,er_erlangga
https://www.instagram.com/dhioadhinugra/,dhioadhinugra
https://www.instagram.com/dancesignal/,dancesignal
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/abilrie/,abilrie
https://www.instagram.com/jeep_wranglers/,jeep_wranglers
https://www.instagram.com/timothyronaldd/,timothyronaldd
https://www.instagram.com/suliantoindriaputra/,suliantoindriaputra
https://www.instagram.com/rizkyudo/,rizkyudo
https://www.instagram.com/kiesha.alvaro/,kiesha.alvaro
https://www.instagram.com/milesfilms/,milesfilms
https://www.instagram.com/sundarpichai/,sundarpichai
https://www.instagram.com/mariokassarofficial/,mariokassarofficial
https://www.instagram.com/herbert.situmorang.7/,herbert.situmorang.7
https://www.instagram.com/nyfanewyork/,nyfanewyork
https://www.instagram.com/newyorkfilmacademy/,newyorkfilmacademy
https://www.instagram.com/jeep/,jeep
https://www.instagram.com/societyawards/,societyawards
https://www.instagram.com/jeffbezos/,jeffbezos
https://www.instagram.com/babecabiita/,babecabiita
https://www.instagram.com/thisisbillgates/,thisisbillgates
https://www.instagram.com/honda/,honda
https://www.instagram.com/neildegrassetyson/,neildegrassetyson
https://www.instagram.com/grantgust/,grantgust
https://www.instagram.com/jejesoekarno/,jejesoekarno
https://www.instagram.com/nike/,nike
https://www.instagram.com/holidayswap/,holidayswap
https://www.instagram.com/venesia_ari/,venesia_ari
https://www.instagram.com/hightyid/,hightyid
https://www.instagram.com/_adamrajwa/,_adamrajwa
https://www.instagram.com/gwynethgnv/,gwynethgnv
https://www.instagram.com/dodit_mul/,dodit_mul
https://www.instagram.com/its_lauramoane2/,its_lauramoane2
https://www.instagram.com/the_rosemaryy/,the_rosemaryy
https://www.instagram.com/sdambarwati/,sdambarwati
https://www.instagram.com/officialpilarez/,officialpilarez
https://www.instagram.com/arnoldpo/,arnoldpo
https://www.instagram.com/alexpreview/,alexpreview
https://www.instagram.com/samuelchrist/,samuelchrist
https://www.instagram.com/nataliezenn24/,nataliezenn24
https://www.instagram.com/budyceka_bucek/,budyceka_bucek
https://www.instagram.com/afifsalmanalfarisi/,afifsalmanalfarisi
https://www.instagram.com/nthniazefanya/,nthniazefanya
https://www.instagram.com/cahyaidputra/,cahyaidputra
https://www.instagram.com/cristianodslv_/,cristianodslv_
https://www.instagram.com/hendrajunior2022/,hendrajunior2022
https://www.instagram.com/swr_carwash/,swr_carwash
https://www.instagram.com/debrugge_/,debrugge_
https://www.instagram.com/hafiz_husni/,hafiz_husni
https://www.instagram.com/matthew.parulian/,matthew.parulian
https://www.instagram.com/karinasalim/,karinasalim
https://www.instagram.com/asheladz/,asheladz
https://www.instagram.com/graciemgdln/,graciemgdln
https://www.instagram.com/teppanku/,teppanku
https://www.instagram.com/celloszxz/,celloszxz
https://www.instagram.com/astridasuryatenggara/,astridasuryatenggara
https://www.instagram.com/putrimarino/,putrimarino
https://www.instagram.com/zh4vira/,zh4vira
https://www.instagram.com/lyasxh_/,lyasxh_
https://www.instagram.com/aknesalua0904/,aknesalua0904
https://www.instagram.com/wingsgroupsurabaya/,wingsgroupsurabaya
https://www.instagram.com/abunsungkar/,abunsungkar
https://www.instagram.com/muhammadzahirubaydillah/,muhammadzahirubaydillah
https://www.instagram.com/virakoban8302/,virakoban8302
https://www.instagram.com/mculangtahun_arif/,mculangtahun_arif
https://www.instagram.com/da7_robi/,da7_robi
https://www.instagram.com/yoona__lim/,yoona__lim
https://www.instagram.com/mellyleeofficial/,mellyleeofficial
https://www.instagram.com/zaskiadyamecca/,zaskiadyamecca
https://www.instagram.com/azizahsalsha_/,azizahsalsha_
https://www.instagram.com/gadiiing/,gadiiing
https://www.instagram.com/leshclinic/,leshclinic
https://www.instagram.com/levianbillar/,levianbillar
https://www.instagram.com/streamentertainment_/,streamentertainment_
https://www.instagram.com/da5_ebyrizta14/,da5_ebyrizta14
https://www.instagram.com/kyo1122/,kyo1122
https://www.instagram.com/flowirtz/,flowirtz
https://www.instagram.com/leslaragency/,leslaragency
https://www.instagram.com/ryanjiro_/,ryanjiro_
https://www.instagram.com/conorbradley.03/,conorbradley.03
https://www.instagram.com/cuerpoid/,cuerpoid
https://www.instagram.com/fyifact/,fyifact
https://www.instagram.com/dedimulyadi71/,dedimulyadi71
https://www.instagram.com/jck_desaratu/,jck_desaratu
https://www.instagram.com/lida_selfi07/,lida_selfi07
https://www.instagram.com/miloskerkezofficial/,miloskerkezofficial
https://www.instagram.com/mybalqiss/,mybalqiss
https://www.instagram.com/citraciki/,citraciki
https://www.instagram.com/curtisjones/,curtisjones
https://www.instagram.com/kareenakapoorkhan/,kareenakapoorkhan
https://www.instagram.com/da7_sastra08/,da7_sastra08
https://www.instagram.com/flaviozavieraa/,flaviozavieraa
https://www.instagram.com/sridev1206/,sridev1206
https://www.instagram.com/ataliapr/,ataliapr
https://www.instagram.com/leslar_entertainment/,leslar_entertainment
https://www.instagram.com/juliaprt7/,juliaprt7
https://www.instagram.com/prabowo/,prabowo
https://www.instagram.com/duniapunyacerita/,duniapunyacerita
https://www.instagram.com/dinanfajrina/,dinanfajrina
https://www.instagram.com/hidahpratama/,hidahpratama
https://www.instagram.com/leshiativana/,leshiativana
https://www.instagram.com/official_lestilovers_indonesia/,official_lestilovers_indonesia
https://www.instagram.com/muhammadnuzuldzikri/,muhammadnuzuldzikri
https://www.instagram.com/kampunghalamanofficial/,kampunghalamanofficial
https://www.instagram.com/harsiwiachmad/,harsiwiachmad
https://www.instagram.com/ibrahimakonate/,ibrahimakonate
https://www.instagram.com/esterlita_alexander/,esterlita_alexander
https://www.instagram.com/indosiar/,indosiar
https://www.instagram.com/davidsuwarto/,davidsuwarto
https://www.instagram.com/iwanfals/,iwanfals
https://www.instagram.com/amiawards/,amiawards
https://www.instagram.com/bulebarbie_official/,bulebarbie_official
https://www.instagram.com/___aryan___/,___aryan___
https://www.instagram.com/ask.malika/,ask.malika
https://www.instagram.com/hananiagroup.id/,hananiagroup.id
https://www.instagram.com/szoboszlaidominik/,szoboszlaidominik
https://www.instagram.com/kitabisacom/,kitabisacom
https://www.instagram.com/calamaryshop/,calamaryshop
https://www.instagram.com/nitavior/,nitavior
https://www.instagram.com/kajol/,kajol
https://www.instagram.com/adebae.77/,adebae.77
https://www.instagram.com/diana_sastra/,diana_sastra
https://www.instagram.com/melodylaksani92/,melodylaksani92
https://www.instagram.com/leslarrecords/,leslarrecords
https://www.instagram.com/yasminnapper/,yasminnapper
https://www.instagram.com/alex_isak/,alex_isak
https://www.instagram.com/tomcruise/,tomcruise
https://www.instagram.com/pablogavi/,pablogavi
https://www.instagram.com/ustadzabdulsomad_official/,ustadzabdulsomad_official
https://www.instagram.com/dr.iqhbal/,dr.iqhbal
https://www.instagram.com/itsnaufalsamudra/,itsnaufalsamudra
https://www.instagram.com/fakhru_ans_official/,fakhru_ans_official
https://www.instagram.com/endowataru/,endowataru
https://www.instagram.com/callistarum/,callistarum
https://www.instagram.com/marshaz/,marshaz
https://www.instagram.com/plesbol.inc/,plesbol.inc
https://www.instagram.com/aqeelacalista/,aqeelacalista
https://www.instagram.com/shabrina_leonita/,shabrina_leonita
https://www.instagram.com/itsaulia17/,itsaulia17
https://www.instagram.com/arianinismaputri/,arianinismaputri
https://www.instagram.com/alnassr/,alnassr
https://www.instagram.com/nasariastri/,nasariastri
https://www.instagram.com/gyaps/,gyaps
https://www.instagram.com/dinda.ghaniaa/,dinda.ghaniaa
https://www.instagram.com/waodeofficial/,waodeofficial
https://www.instagram.com/ajaib_investasi/,ajaib_investasi
https://www.instagram.com/bellabonita_r.a/,bellabonita_r.a
https://www.instagram.com/syahamimishahri/,syahamimishahri
https://www.instagram.com/noparpradipta_/,noparpradipta_
https://www.instagram.com/vidiodotcom/,vidiodotcom
https://www.instagram.com/bouttier_maxime/,bouttier_maxime
https://www.instagram.com/sanayairani/,sanayairani
https://www.instagram.com/iamdevano/,iamdevano
https://www.instagram.com/dokterfeliani/,dokterfeliani
https://www.instagram.com/da4_fildan/,da4_fildan
https://www.instagram.com/valtifanka/,valtifanka
https://www.instagram.com/itadyahpurnamasari/,itadyahpurnamasari
https://www.instagram.com/thebathaholic/,thebathaholic
https://www.instagram.com/ratuisyellnrzr/,ratuisyellnrzr
https://www.instagram.com/cut.intannabila/,cut.intannabila
https://www.instagram.com/radhikkamadan/,radhikkamadan
https://www.instagram.com/primarasaresto/,primarasaresto
https://www.instagram.com/virgilvandijk/,virgilvandijk
https://www.instagram.com/aaliyah.massaid/,aaliyah.massaid
https://www.instagram.com/24evercoffee/,24evercoffee
https://www.instagram.com/handy.bonny/,handy.bonny
https://www.instagram.com/lyodraofficial/,lyodraofficial
https://www.instagram.com/mulanjameela1/,mulanjameela1
https://www.instagram.com/hrithikroshan/,hrithikroshan
https://www.instagram.com/jajanan.djalu/,jajanan.djalu
https://www.instagram.com/trinityoptima/,trinityoptima
https://www.instagram.com/septiasiregar17/,septiasiregar17
https://www.instagram.com/byayudyahandari/,byayudyahandari
https://www.instagram.com/beingsalmankhan/,beingsalmankhan
https://www.instagram.com/sheiladaisha/,sheiladaisha
https://www.instagram.com/dewiperssik9/,dewiperssik9
https://www.instagram.com/putrasiregarr17/,putrasiregarr17
https://www.instagram.com/lida_ridwan17/,lida_ridwan17
https://www.instagram.com/sherlyannavita/,sherlyannavita
https://www.instagram.com/nandaarsynt/,nandaarsynt
https://www.instagram.com/elsaajapasal/,elsaajapasal
https://www.instagram.com/bellyiverzon/,bellyiverzon
https://www.instagram.com/fadiljaidi/,fadiljaidi
https://www.instagram.com/gia_manek/,gia_manek
https://www.instagram.com/ibuhajat123/,ibuhajat123
https://www.instagram.com/ustadz.pantun/,ustadz.pantun
https://www.instagram.com/anna.mci10/,anna.mci10
https://www.instagram.com/fg_icha/,fg_icha
https://www.instagram.com/ranveersingh/,ranveersingh
https://www.instagram.com/zara_leola_official/,zara_leola_official
https://www.instagram.com/smindrawati/,smindrawati
https://www.instagram.com/amitabhbachchan/,amitabhbachchan
https://www.instagram.com/adele/,adele
https://www.instagram.com/ponijanliaw/,ponijanliaw
https://www.instagram.com/gadiscsadiqah/,gadiscsadiqah
https://www.instagram.com/nehakakkar/,nehakakkar
https://www.instagram.com/ucie_sucita/,ucie_sucita
https://www.instagram.com/dwina_drm/,dwina_drm
https://www.instagram.com/ildivo/,ildivo
https://www.instagram.com/claudiaudie/,claudiaudie
https://www.instagram.com/jokowi/,jokowi
https://www.instagram.com/atykimmorahnew/,atykimmorahnew
https://www.instagram.com/gibran_rakabuming/,gibran_rakabuming
https://www.instagram.com/iranndha/,iranndha
https://www.instagram.com/dinihanipahm/,dinihanipahm
https://www.instagram.com/jennheryanto/,jennheryanto
https://www.instagram.com/hanggini/,hanggini
https://www.instagram.com/alemacallister/,alemacallister
https://www.instagram.com/akshaykumar/,akshaykumar
https://www.instagram.com/celinedion/,celinedion
https://www.instagram.com/harshaalimalhotra_03/,harshaalimalhotra_03
https://www.instagram.com/lyia_tm/,lyia_tm
https://www.instagram.com/3dent_id/,3dent_id
https://www.instagram.com/kayla.nadira/,kayla.nadira
https://www.instagram.com/ginaaayoubi/,ginaaayoubi
https://www.instagram.com/lilyjcollins/,lilyjcollins
https://www.instagram.com/klinikdermaprojakarta/,klinikdermaprojakarta
https://www.instagram.com/7sainaljassmi/,7sainaljassmi
https://www.instagram.com/yellowfitkitchen/,yellowfitkitchen
https://www.instagram.com/kaktyann/,kaktyann
https://www.instagram.com/marlenehariman/,marlenehariman
https://www.instagram.com/mdtv/,mdtv
https://www.instagram.com/sigitwardana/,sigitwardana
https://www.instagram.com/deepikapadukone/,deepikapadukone
https://www.instagram.com/fannysabilaofficial/,fannysabilaofficial
https://www.instagram.com/mimi.peri/,mimi.peri
https://www.instagram.com/elv.label/,elv.label
https://www.instagram.com/daidermawann/,daidermawann
https://www.instagram.com/nonaculinary/,nonaculinary
https://www.instagram.com/sithamarino/,sithamarino
https://www.instagram.com/handemiyy/,handemiyy
https://www.instagram.com/drgdevya/,drgdevya
https://www.instagram.com/fachrulhadid/,fachrulhadid
https://www.instagram.com/nattaama_/,nattaama_
https://www.instagram.com/aruanmarsha/,aruanmarsha
https://www.instagram.com/mawrellous/,mawrellous
https://www.instagram.com/shabrinaaluna/,shabrinaaluna
https://www.instagram.com/elelrumi/,elelrumi
https://www.instagram.com/michan_91/,michan_91
https://www.instagram.com/ikhsanpirdaus1/,ikhsanpirdaus1
https://www.instagram.com/daarulquranindonesia/,daarulquranindonesia
https://www.instagram.com/mahirahkhan/,mahirahkhan
https://www.instagram.com/oliviasumargo/,oliviasumargo
https://www.instagram.com/kana.sybilla/,kana.sybilla
https://www.instagram.com/officialpilarez/,officialpilarez
https://www.instagram.com/aishakeem15/,aishakeem15
https://www.instagram.com/realpz/,realpz
https://www.instagram.com/alifalubis/,alifalubis
https://www.instagram.com/moell.id/,moell.id
https://www.instagram.com/hke57/,hke57
https://www.instagram.com/shafaharris/,shafaharris
https://www.instagram.com/cutputrims/,cutputrims
https://www.instagram.com/priyankachopra/,priyankachopra
https://www.instagram.com/anisarahmaan/,anisarahmaan
https://www.instagram.com/lida_rara06/,lida_rara06
https://www.instagram.com/dwihandaanda/,dwihandaanda
https://www.instagram.com/shraddhakapoor/,shraddhakapoor
https://www.instagram.com/randpunk/,randpunk
https://www.instagram.com/buttonscarves/,buttonscarves
https://www.instagram.com/thariqhalilintar/,thariqhalilintar
https://www.instagram.com/lida_alifaulia02/,lida_alifaulia02
https://www.instagram.com/aliaabhatt/,aliaabhatt
https://www.instagram.com/vidialdiano/,vidialdiano
https://www.instagram.com/rizkinanazarr/,rizkinanazarr
https://www.instagram.com/alexanderbarackel/,alexanderbarackel
https://www.instagram.com/adysky99/,adysky99
https://www.instagram.com/shaniaindryn/,shaniaindryn
https://www.instagram.com/zivamagnolya/,zivamagnolya
https://www.instagram.com/dianamputri/,dianamputri
https://www.instagram.com/vienstasman/,vienstasman
https://www.instagram.com/susansameeh/,susansameeh
https://www.instagram.com/kiranadevina/,kiranadevina
https://www.instagram.com/ferrysal1m/,ferrysal1m
https://www.instagram.com/novitamochamad/,novitamochamad
https://www.instagram.com/tasyafarasya/,tasyafarasya
https://www.instagram.com/sinisukanthony/,sinisukanthony
https://www.instagram.com/gebysrikandii/,gebysrikandii
https://www.instagram.com/bintangemon/,bintangemon
https://www.instagram.com/eriesuzan/,eriesuzan
https://www.instagram.com/okidatanglagi/,okidatanglagi
https://www.instagram.com/bellinamer/,bellinamer
https://www.instagram.com/shaktiarora/,shaktiarora
https://www.instagram.com/shreyaghoshal/,shreyaghoshal
https://www.instagram.com/fahrulrochman_/,fahrulrochman_
https://www.instagram.com/varundvn/,varundvn
https://www.instagram.com/ferry_fernandez83/,ferry_fernandez83
https://www.instagram.com/benkasyafani/,benkasyafani
https://www.instagram.com/amingisback/,amingisback
https://www.instagram.com/rizalakbarazhari/,rizalakbarazhari
https://www.instagram.com/adelia_finsani/,adelia_finsani
https://www.instagram.com/mayshajhu/,mayshajhu
https://www.instagram.com/ayungberinda/,ayungberinda
https://www.instagram.com/shellasaukiaofficial/,shellasaukiaofficial
https://www.instagram.com/femilasinukaban/,femilasinukaban
https://www.instagram.com/arafahrianti/,arafahrianti
https://www.instagram.com/angkringan.tehita/,angkringan.tehita
https://www.instagram.com/hijabchic/,hijabchic
https://www.instagram.com/nisaf__/,nisaf__
https://www.instagram.com/mamah_kejora/,mamah_kejora
https://www.instagram.com/tasya_ratu_gopo/,tasya_ratu_gopo
https://www.instagram.com/bamed.id/,bamed.id
https://www.instagram.com/andyrobertson94/,andyrobertson94
https://www.instagram.com/manutd/,manutd
https://www.instagram.com/ayra.zahra.nursyifa/,ayra.zahra.nursyifa
https://www.instagram.com/kierking8/,kierking8
https://www.instagram.com/findriliasanvira/,findriliasanvira
https://www.instagram.com/chocochipsboutique/,chocochipsboutique
https://www.instagram.com/adindanegara/,adindanegara
https://www.instagram.com/fabioasher/,fabioasher
https://www.instagram.com/afnaalliya_/,afnaalliya_
https://www.instagram.com/sintyamarisca/,sintyamarisca
https://www.instagram.com/sevinc_sevil/,sevinc_sevil
https://www.instagram.com/fraulila/,fraulila
https://www.instagram.com/philipekarunia/,philipekarunia
https://www.instagram.com/siviazizah/,siviazizah
https://www.instagram.com/arie_kriting/,arie_kriting
https://www.instagram.com/anushkasharma/,anushkasharma
https://www.instagram.com/anwar_bab/,anwar_bab
https://www.instagram.com/sherine/,sherine
https://www.instagram.com/putriisnari3/,putriisnari3
https://www.instagram.com/betariayu22/,betariayu22
https://www.instagram.com/dindazani/,dindazani
https://www.instagram.com/mulanisanjay/,mulanisanjay
https://www.instagram.com/alyaaputri/,alyaaputri
https://www.instagram.com/shandyaulia/,shandyaulia
https://www.instagram.com/umar_syarief/,umar_syarief
https://www.instagram.com/ayudyahandari/,ayudyahandari
https://www.instagram.com/drellendr/,drellendr
https://www.instagram.com/natasharizkynew/,natasharizkynew
https://www.instagram.com/luqmanoktaviana_mc/,luqmanoktaviana_mc
https://www.instagram.com/zayn/,zayn
https://www.instagram.com/lida2020_aco1/,lida2020_aco1
https://www.instagram.com/baraa_masoud/,baraa_masoud
https://www.instagram.com/mawaddatulhaq/,mawaddatulhaq
https://www.instagram.com/halobandung/,halobandung
https://www.instagram.com/marshanatika/,marshanatika
https://www.instagram.com/h.hermansuherman/,h.hermansuherman
https://www.instagram.com/eva_ellococg10/,eva_ellococg10
https://www.instagram.com/andirianto_official/,andirianto_official
https://www.instagram.com/mahaliniraharja/,mahaliniraharja
https://www.instagram.com/mariana__putri/,mariana__putri
https://www.instagram.com/abdillah.sholeh/,abdillah.sholeh
https://www.instagram.com/jharnabhagwani/,jharnabhagwani
https://www.instagram.com/dr.najmahnurislami/,dr.najmahnurislami
https://www.instagram.com/laurabbasjackson/,laurabbasjackson
https://www.instagram.com/rey_mbayang/,rey_mbayang
https://www.instagram.com/kesharatuliu05/,kesharatuliu05
https://www.instagram.com/js.collection_official/,js.collection_official
https://www.instagram.com/enazirashf_/,enazirashf_
https://www.instagram.com/patriciagouw/,patriciagouw
https://www.instagram.com/kdi2020_wina/,kdi2020_wina
https://www.instagram.com/riafinola/,riafinola
https://www.instagram.com/revinavt/,revinavt
https://www.instagram.com/tokoleslar/,tokoleslar
https://www.instagram.com/fajarnugrs/,fajarnugrs
https://www.instagram.com/jennifercoppenreal20/,jennifercoppenreal20
https://www.instagram.com/nadiaraysa/,nadiaraysa
https://www.instagram.com/lilymhe/,lilymhe
https://www.instagram.com/lestikejora/,lestikejora
https://www.instagram.com/adiba.knza/,adiba.knza
https://www.instagram.com/sridev1206/,sridev1206
https://www.instagram.com/ndf.s/,ndf.s
https://www.instagram.com/tapia/,tapia
https://www.instagram.com/nasyamarcella/,nasyamarcella
https://www.instagram.com/kitabisacom/,kitabisacom
https://www.instagram.com/emmaraducanu/,emmaraducanu
https://www.instagram.com/dewaopentournament/,dewaopentournament
https://www.instagram.com/nishabasrewan/,nishabasrewan
https://www.instagram.com/kingryan/,kingryan
https://www.instagram.com/jasminmeijers/,jasminmeijers
https://www.instagram.com/bailafauri/,bailafauri
https://www.instagram.com/desta80s/,desta80s
https://www.instagram.com/regina.tanyaa/,regina.tanyaa
https://www.instagram.com/andre_rosiade/,andre_rosiade
https://www.instagram.com/whisnusantika/,whisnusantika
https://www.instagram.com/gyaps/,gyaps
https://www.instagram.com/justjared/,justjared
https://www.instagram.com/jessicashainaa/,jessicashainaa
https://www.instagram.com/eri.carl/,eri.carl
https://www.instagram.com/valtifanka/,valtifanka
https://www.instagram.com/carlitosalcarazz/,carlitosalcarazz
https://www.instagram.com/welber07official/,welber07official
https://www.instagram.com/charles_leclerc/,charles_leclerc
https://www.instagram.com/mariatheodoree/,mariatheodoree
https://www.instagram.com/chelsea.veronnia/,chelsea.veronnia
https://www.instagram.com/aaliyah.massaid/,aaliyah.massaid
https://www.instagram.com/fuji_an/,fuji_an
https://www.instagram.com/zahmuz12/,zahmuz12
https://www.instagram.com/zaraadhsty/,zaraadhsty
https://www.instagram.com/iniadzwaaurell/,iniadzwaaurell
https://www.instagram.com/sultansapta/,sultansapta
https://www.instagram.com/alyssadaguise/,alyssadaguise
https://www.instagram.com/zarworldpadel.id/,zarworldpadel.id
https://www.instagram.com/wimbledon/,wimbledon
https://www.instagram.com/xolovelyayana/,xolovelyayana
https://www.instagram.com/davinaakaramoy/,davinaakaramoy
https://www.instagram.com/adrianarmanasco/,adrianarmanasco
https://www.instagram.com/firdaaindiraa/,firdaaindiraa
https://www.instagram.com/putrasiregarr17/,putrasiregarr17
https://www.instagram.com/gabriellaekaputri/,gabriellaekaputri
https://www.instagram.com/kezialetheia/,kezialetheia
https://www.instagram.com/raissanggiani/,raissanggiani
https://www.instagram.com/fadiljaidi/,fadiljaidi
https://www.instagram.com/leonardmalikiii/,leonardmalikiii
https://www.instagram.com/maudyeffrosina/,maudyeffrosina
https://www.instagram.com/mikha_hernan/,mikha_hernan
https://www.instagram.com/danniasalsabilla/,danniasalsabilla
https://www.instagram.com/karinasalim/,karinasalim
https://www.instagram.com/denise.hoefer.3005/,denise.hoefer.3005
https://www.instagram.com/asnawi_bhr/,asnawi_bhr
https://www.instagram.com/ybrap/,ybrap
https://www.instagram.com/dwina_drm/,dwina_drm
https://www.instagram.com/c.eendy/,c.eendy
https://www.instagram.com/annyaerica/,annyaerica
https://www.instagram.com/nicoleparham_/,nicoleparham_
https://www.instagram.com/paparich666/,paparich666
https://www.instagram.com/alecyavebyy/,alecyavebyy
https://www.instagram.com/alegalan96/,alegalan96
https://www.instagram.com/thomascgibson/,thomascgibson
https://www.instagram.com/gladysvctry/,gladysvctry
https://www.instagram.com/grigordimitrov/,grigordimitrov
https://www.instagram.com/gilangsamiadji/,gilangsamiadji
https://www.instagram.com/rd.ayuregita/,rd.ayuregita
https://www.instagram.com/niloverjudge/,niloverjudge
https://www.instagram.com/fatehhalilintar/,fatehhalilintar
https://www.instagram.com/taufikwahyuda/,taufikwahyuda
https://www.instagram.com/rklopperr/,rklopperr
https://www.instagram.com/ddaffariqq/,ddaffariqq
https://www.instagram.com/angiemstwn/,angiemstwn
https://www.instagram.com/adeleeta/,adeleeta
https://www.instagram.com/marlenehariman/,marlenehariman
https://www.instagram.com/lulalahfah/,lulalahfah
https://www.instagram.com/afniyulindah/,afniyulindah
https://www.instagram.com/malaikha/,malaikha
https://www.instagram.com/racheltheresia/,racheltheresia
https://www.instagram.com/witansulaiman_/,witansulaiman_
https://www.instagram.com/bellaclrs/,bellaclrs
https://www.instagram.com/adipati/,adipati
https://www.instagram.com/mufli_ananda/,mufli_ananda
https://www.instagram.com/just.yumi/,just.yumi
https://www.instagram.com/shela_lala96/,shela_lala96
https://www.instagram.com/harashta/,harashta
https://www.instagram.com/theresaefrata/,theresaefrata
https://www.instagram.com/thariqhalilintar/,thariqhalilintar
https://www.instagram.com/adysky99/,adysky99
https://www.instagram.com/zivamagnolya/,zivamagnolya
https://www.instagram.com/doshzn/,doshzn
https://www.instagram.com/munggaran6/,munggaran6
https://www.instagram.com/aurelialourdes/,aurelialourdes
https://www.instagram.com/rifqiftr/,rifqiftr
https://www.instagram.com/darrelmichelin/,darrelmichelin
https://www.instagram.com/key24bingss/,key24bingss
https://www.instagram.com/milajmlaa/,milajmlaa
https://www.instagram.com/vlrieval/,vlrieval
https://www.instagram.com/desrapercaya/,desrapercaya
https://www.instagram.com/iluminen/,iluminen
https://www.instagram.com/raisyah/,raisyah
https://www.instagram.com/iamdevano/,iamdevano
https://www.instagram.com/egymaulanavikri/,egymaulanavikri
https://www.instagram.com/indiarosebrownn/,indiarosebrownn
https://www.instagram.com/nuffal/,nuffal
https://www.instagram.com/kharimaocha/,kharimaocha
https://www.instagram.com/evarinjanii/,evarinjanii
https://www.instagram.com/aditiyadaffaa_/,aditiyadaffaa_
https://www.instagram.com/ojmo_/,ojmo_
https://www.instagram.com/aqsaaswar/,aqsaaswar
https://www.instagram.com/ney_neo/,ney_neo
https://www.instagram.com/pratamaarhan8/,pratamaarhan8
https://www.instagram.com/mauragbrll/,mauragbrll
https://www.instagram.com/anissaaziza/,anissaaziza
https://www.instagram.com/jonisaputra09/,jonisaputra09
https://www.instagram.com/ekaceluller/,ekaceluller
https://www.instagram.com/zahirahandifaa/,zahirahandifaa
https://www.instagram.com/ragahdo/,ragahdo
https://www.instagram.com/nicholasandrsn/,nicholasandrsn
https://www.instagram.com/joleneemarie/,joleneemarie
https://www.instagram.com/aruanmarsha/,aruanmarsha
https://www.instagram.com/celloszxz/,celloszxz
https://www.instagram.com/bebytsabina/,bebytsabina
https://www.instagram.com/aeroaswar/,aeroaswar
https://www.instagram.com/ataliabunga/,ataliabunga
https://www.instagram.com/zayn/,zayn
https://www.instagram.com/neymarjr/,neymarjr
https://www.instagram.com/shazhaniaa/,shazhaniaa
https://www.instagram.com/medinadinaaa/,medinadinaaa
https://www.instagram.com/vanessaegas/,vanessaegas
https://www.instagram.com/babelrizki/,babelrizki
https://www.instagram.com/ansellmaputri/,ansellmaputri
https://www.instagram.com/dennisgustiputra/,dennisgustiputra
https://www.instagram.com/drgdevya/,drgdevya
https://www.instagram.com/scarlettofficial/,scarlettofficial
https://www.instagram.com/elnandautomo/,elnandautomo
https://www.instagram.com/raissarmdhn/,raissarmdhn
https://www.instagram.com/rizkybillar/,rizkybillar
https://www.instagram.com/ilimaaa_/,ilimaaa_
https://www.instagram.com/andiannsyah/,andiannsyah
https://www.instagram.com/sabreenadressler/,sabreenadressler
https://www.instagram.com/okintph/,okintph
https://www.instagram.com/rifkiantariksa_/,rifkiantariksa_
https://www.instagram.com/naura.ayu/,naura.ayu
https://www.instagram.com/mailmayo_syahputra89/,mailmayo_syahputra89
https://www.instagram.com/maydinahnfh/,maydinahnfh
https://www.instagram.com/ialzimarker/,ialzimarker
https://www.instagram.com/yorikooangln_/,yorikooangln_
https://www.instagram.com/doctorsiska/,doctorsiska
https://www.instagram.com/maswahibb/,maswahibb
https://www.instagram.com/jelitatf/,jelitatf
https://www.instagram.com/timotiusmul/,timotiusmul
https://www.instagram.com/antogriezmann/,antogriezmann
https://www.instagram.com/revashion/,revashion
https://www.instagram.com/kikysaputrii/,kikysaputrii
https://www.instagram.com/kayra.miendra/,kayra.miendra
https://www.instagram.com/sooyon_texture/,sooyon_texture
https://www.instagram.com/rorymcilroy/,rorymcilroy
https://www.instagram.com/ayusarasw/,ayusarasw
https://www.instagram.com/ayunghadid/,ayunghadid
https://www.instagram.com/lorenzoabraham/,lorenzoabraham
https://www.instagram.com/ratu.namira/,ratu.namira
https://www.instagram.com/daraarafah/,daraarafah
https://www.instagram.com/ranggazlaksmana/,ranggazlaksmana
https://www.instagram.com/roxannemorgann/,roxannemorgann
https://www.instagram.com/sabilavirajatii/,sabilavirajatii
https://www.instagram.com/adinda.latieff/,adinda.latieff
https://www.instagram.com/cintaindraa/,cintaindraa
https://www.instagram.com/keanucampora/,keanucampora
https://www.instagram.com/imamjunaaa/,imamjunaaa
https://www.instagram.com/vladimirama/,vladimirama
https://www.instagram.com/tashyanaraysha/,tashyanaraysha
https://www.instagram.com/angiieewilliams/,angiieewilliams
https://www.instagram.com/alvianarrrr/,alvianarrrr
https://www.instagram.com/sharazaaa/,sharazaaa
https://www.instagram.com/coco3_ame9/,coco3_ame9
https://www.instagram.com/giorgino_abraham/,giorgino_abraham
https://www.instagram.com/ningayu_/,ningayu_
https://www.instagram.com/sajidahhalilintar/,sajidahhalilintar
https://www.instagram.com/ariee7/,ariee7
https://www.instagram.com/tommyteja/,tommyteja
https://www.instagram.com/nadhifbasalamah/,nadhifbasalamah
https://www.instagram.com/tercipungcipung/,tercipungcipung
https://www.instagram.com/tissabiani/,tissabiani
https://www.instagram.com/sintyamarisca/,sintyamarisca
https://www.instagram.com/jovitakaren/,jovitakaren
https://www.instagram.com/emilmari0/,emilmari0
https://www.instagram.com/dikta/,dikta
https://www.instagram.com/steffizamoraaa/,steffizamoraaa
https://www.instagram.com/syifahadju/,syifahadju
https://www.instagram.com/arieltatum/,arieltatum
https://www.instagram.com/ray.paramarta/,ray.paramarta
https://www.instagram.com/winstongomez/,winstongomez
https://www.instagram.com/sintaboshoven/,sintaboshoven
https://www.instagram.com/miurachnd/,miurachnd
https://www.instagram.com/bellezaa_17/,bellezaa_17
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/diva.azzura/,diva.azzura
https://www.instagram.com/agynessidik/,agynessidik
https://www.instagram.com/zize.official/,zize.official
https://www.instagram.com/mahardikayusuf/,mahardikayusuf
https://www.instagram.com/mirelnajwaa/,mirelnajwaa
https://www.instagram.com/sarahkeihl/,sarahkeihl
https://www.instagram.com/elinaaaaajoerg/,elinaaaaajoerg
https://www.instagram.com/uan.kaisar/,uan.kaisar
https://www.instagram.com/divafadhilam/,divafadhilam
https://www.instagram.com/safeandsoundjkt/,safeandsoundjkt
https://www.instagram.com/luccafauri/,luccafauri
https://www.instagram.com/njwftkryn_/,njwftkryn_
https://www.instagram.com/agthpricilla/,agthpricilla
https://www.instagram.com/richardo_r55/,richardo_r55
https://www.instagram.com/reynaldiraia/,reynaldiraia
https://www.instagram.com/fadlyfsl_/,fadlyfsl_
https://www.instagram.com/ibnuwardani/,ibnuwardani
https://www.instagram.com/drfeninugraha.spgk/,drfeninugraha.spgk
https://www.instagram.com/ariefmuhammad/,ariefmuhammad
https://www.instagram.com/azahhra/,azahhra
https://www.instagram.com/nissyaa/,nissyaa
https://www.instagram.com/cacatengker/,cacatengker
https://www.instagram.com/hilgadoui/,hilgadoui
https://www.instagram.com/loritayoung_mua/,loritayoung_mua
https://www.instagram.com/rifato/,rifato
https://www.instagram.com/aikoyunichi/,aikoyunichi
https://www.instagram.com/diandramarsha/,diandramarsha
https://www.instagram.com/nathalieawantara/,nathalieawantara
https://www.instagram.com/saskiamaritza/,saskiamaritza
https://www.instagram.com/viviinovika/,viviinovika
https://www.instagram.com/collinjavap/,collinjavap
https://www.instagram.com/byisabellefarradiva/,byisabellefarradiva
https://www.instagram.com/ardibakrie/,ardibakrie
https://www.instagram.com/shafarp/,shafarp
https://www.instagram.com/raquelklarkin/,raquelklarkin
https://www.instagram.com/auliaputrifnaaa/,auliaputrifnaaa
https://www.instagram.com/septiningtyas/,septiningtyas
https://www.instagram.com/aufa_nanda/,aufa_nanda
https://www.instagram.com/yendryma/,yendryma
https://www.instagram.com/lucintaluna_manjalita/,lucintaluna_manjalita
https://www.instagram.com/imantdj/,imantdj
https://www.instagram.com/rhenopoetiray/,rhenopoetiray
https://www.instagram.com/rakeshd18/,rakeshd18
https://www.instagram.com/rehanmubarak/,rehanmubarak
https://www.instagram.com/sherylsheinafia/,sherylsheinafia
https://www.instagram.com/lidyapraditta/,lidyapraditta
https://www.instagram.com/timothyallesandro/,timothyallesandro
https://www.instagram.com/ochiipramita/,ochiipramita
https://www.instagram.com/satinezaneta/,satinezaneta
https://www.instagram.com/mputrasetia/,mputrasetia
https://www.instagram.com/riaricis1795/,riaricis1795
https://www.instagram.com/billsatya/,billsatya
https://www.instagram.com/zefanyamalingkas/,zefanyamalingkas
https://www.instagram.com/loexyanta/,loexyanta
https://www.instagram.com/maudyayunda/,maudyayunda
https://www.instagram.com/ussiyfauziah/,ussiyfauziah
https://www.instagram.com/bungapuspaa/,bungapuspaa
https://www.instagram.com/carissaperusset/,carissaperusset
https://www.instagram.com/hassanalaydrus/,hassanalaydrus
https://www.instagram.com/tamiialwi/,tamiialwi
https://www.instagram.com/michelleearuan/,michelleearuan
https://www.instagram.com/tofanarisantoso/,tofanarisantoso
https://www.instagram.com/adlinrambe/,adlinrambe
https://www.instagram.com/derysyaputraraeger/,derysyaputraraeger
https://www.instagram.com/dimasronisaputra/,dimasronisaputra
https://www.instagram.com/putrailhaq/,putrailhaq
https://www.instagram.com/dxdaa/,dxdaa
https://www.instagram.com/febbyrastanty/,febbyrastanty
https://www.instagram.com/g.alqorni/,g.alqorni
https://www.instagram.com/eldynysf/,eldynysf
https://www.instagram.com/emyaghnia/,emyaghnia
https://www.instagram.com/dusan.ph/,dusan.ph
https://www.instagram.com/kxthriana/,kxthriana
https://www.instagram.com/naura21/,naura21
https://www.instagram.com/bubahalfian/,bubahalfian
https://www.instagram.com/arinokitanya/,arinokitanya
https://www.instagram.com/zaglishabrict/,zaglishabrict
https://www.instagram.com/danielwenas/,danielwenas
https://www.instagram.com/keisyalevronka/,keisyalevronka
https://www.instagram.com/sonjamiraa/,sonjamiraa
https://www.instagram.com/aditlubis/,aditlubis
https://www.instagram.com/irzannfaiq/,irzannfaiq
https://www.instagram.com/aryavasco/,aryavasco
https://www.instagram.com/havizadevianjani/,havizadevianjani
https://www.instagram.com/syala.na/,syala.na
https://www.instagram.com/risyabrabo/,risyabrabo
https://www.instagram.com/ispeakbrandedofficial_/,ispeakbrandedofficial_
https://www.instagram.com/luxcrime_id/,luxcrime_id
https://www.instagram.com/marshel_widianto/,marshel_widianto
https://www.instagram.com/ibnuriza/,ibnuriza
https://www.instagram.com/babylanabila/,babylanabila
https://www.instagram.com/pjk.moon9/,pjk.moon9
https://www.instagram.com/irfanfandi17/,irfanfandi17
https://www.instagram.com/elijahkasper/,elijahkasper
https://www.instagram.com/shannongbr/,shannongbr
https://www.instagram.com/prillylatuconsina96/,prillylatuconsina96
https://www.instagram.com/nabillaayumi/,nabillaayumi
https://www.instagram.com/champagnepapi/,champagnepapi
https://www.instagram.com/febriannindyop/,febriannindyop
https://www.instagram.com/kotomi.ozawa/,kotomi.ozawa
https://www.instagram.com/tianamannering/,tianamannering
https://www.instagram.com/spacelux.official/,spacelux.official
https://www.instagram.com/shandypurnamasari/,shandypurnamasari
https://www.instagram.com/alghazali7/,alghazali7
https://www.instagram.com/jeje.poleddicted/,jeje.poleddicted
https://www.instagram.com/sukagerakclub/,sukagerakclub
https://www.instagram.com/ranggayusuf/,ranggayusuf
https://www.instagram.com/gitajanu/,gitajanu
https://www.instagram.com/nikitamirzanimawardi_172/,nikitamirzanimawardi_172
https://www.instagram.com/keviinhugo/,keviinhugo
https://www.instagram.com/pgatour/,pgatour
https://www.instagram.com/boedy_jvs/,boedy_jvs
https://www.instagram.com/razanzu/,razanzu
https://www.instagram.com/rifkyseptiaji/,rifkyseptiaji
https://www.instagram.com/teukuryz/,teukuryz
https://www.instagram.com/victoria_makeupatelier/,victoria_makeupatelier
https://www.instagram.com/rudyadiputra/,rudyadiputra
https://www.instagram.com/syahfaaevg/,syahfaaevg
https://www.instagram.com/zevanyaawee/,zevanyaawee
https://www.instagram.com/raffinagita1717/,raffinagita1717
https://www.instagram.com/muntazhalilintar/,muntazhalilintar
https://www.instagram.com/bifafelicio/,bifafelicio
https://www.instagram.com/granzetta/,granzetta
https://www.instagram.com/nsyakieb85/,nsyakieb85
https://www.instagram.com/shalvarizaldii/,shalvarizaldii
https://www.instagram.com/dr.tirta/,dr.tirta
https://www.instagram.com/ammarsyahdi/,ammarsyahdi
https://www.instagram.com/titipdongkak_reborn/,titipdongkak_reborn
https://www.instagram.com/sibisma/,sibisma
https://www.instagram.com/tya_ariestya/,tya_ariestya
https://www.instagram.com/titi_kamall/,titi_kamall
https://www.instagram.com/azhkalfa/,azhkalfa
https://www.instagram.com/ade_govinda/,ade_govinda
https://www.instagram.com/jennifer_ipel/,jennifer_ipel
https://www.instagram.com/diniyaan/,diniyaan
https://www.instagram.com/darakezia/,darakezia
https://www.instagram.com/rarafauri/,rarafauri
https://www.instagram.com/fazatmandhika/,fazatmandhika
https://www.instagram.com/sakinatama/,sakinatama
https://www.instagram.com/safiraprameswari/,safiraprameswari
https://www.instagram.com/natashalinadla/,natashalinadla
https://www.instagram.com/fahiramira/,fahiramira
https://www.instagram.com/ichsanrindengan/,ichsanrindengan
https://www.instagram.com/ta.nara/,ta.nara
https://www.instagram.com/24olik/,24olik
https://www.instagram.com/mariaasharita/,mariaasharita
https://www.instagram.com/nabiilamhrn/,nabiilamhrn
https://www.instagram.com/yukikt/,yukikt
https://www.instagram.com/amy_r_qanita/,amy_r_qanita
https://www.instagram.com/lamiyazra/,lamiyazra
https://www.instagram.com/chikievers/,chikievers
https://www.instagram.com/ahmadabdul/,ahmadabdul
https://www.instagram.com/aditadiyatma/,aditadiyatma
https://www.instagram.com/rifkykrismon/,rifkykrismon
https://www.instagram.com/evelyntandionoo/,evelyntandionoo
https://www.instagram.com/jonathanandriano/,jonathanandriano
https://www.instagram.com/tivalsalsabilah/,tivalsalsabilah
https://www.instagram.com/leoafandi_/,leoafandi_
https://www.instagram.com/_aldyrizky/,_aldyrizky
https://www.instagram.com/neswerpus/,neswerpus
https://www.instagram.com/haykaly/,haykaly
https://www.instagram.com/unadembler/,unadembler
https://www.instagram.com/ranaesya/,ranaesya
https://www.instagram.com/callie_officialshop/,callie_officialshop
https://www.instagram.com/rajalatuconsina/,rajalatuconsina
https://www.instagram.com/ammar_tsaqif/,ammar_tsaqif
https://www.instagram.com/abrahamandrew29/,abrahamandrew29
https://www.instagram.com/8rooky_/,8rooky_
https://www.instagram.com/renaldypjs/,renaldypjs
https://www.instagram.com/rakhenaputri/,rakhenaputri
https://www.instagram.com/chintyagabriella/,chintyagabriella
https://www.instagram.com/plusninadiana/,plusninadiana
https://www.instagram.com/bernils.3/,bernils.3
https://www.instagram.com/dethahir/,dethahir
https://www.instagram.com/alyamaharannyy/,alyamaharannyy
https://www.instagram.com/tohakarta/,tohakarta
https://www.instagram.com/zaskiasungkar15/,zaskiasungkar15
https://www.instagram.com/olivianuzan/,olivianuzan
https://www.instagram.com/keziajudith/,keziajudith
https://www.instagram.com/angiemiraclee/,angiemiraclee
https://www.instagram.com/krisnkros/,krisnkros
https://www.instagram.com/salshaindradjaja/,salshaindradjaja
https://www.instagram.com/michaelkammerlohrr/,michaelkammerlohrr
https://www.instagram.com/anugrahlindu/,anugrahlindu
https://www.instagram.com/sooyaaa__/,sooyaaa__
https://www.instagram.com/vampirehollie/,vampirehollie
https://www.instagram.com/menelusurimasa/,menelusurimasa
https://www.instagram.com/lestikejora/,lestikejora
https://www.instagram.com/lany/,lany
https://www.instagram.com/dillaljaidi/,dillaljaidi
https://www.instagram.com/abunsungkar/,abunsungkar
https://www.instagram.com/salshabillaadr/,salshabillaadr
https://www.instagram.com/shikuthebrand/,shikuthebrand
https://www.instagram.com/jkt48gracia/,jkt48gracia
https://www.instagram.com/jkt48.kathrina/,jkt48.kathrina
https://www.instagram.com/fandinasutionn/,fandinasutionn
https://www.instagram.com/estapramanita/,estapramanita
https://www.instagram.com/bernadyaribka/,bernadyaribka
https://www.instagram.com/cantikcitra/,cantikcitra
https://www.instagram.com/vonnyfelicia/,vonnyfelicia
https://www.instagram.com/bylizzieparra/,bylizzieparra
https://www.instagram.com/cinema.21/,cinema.21
https://www.instagram.com/imeldatherinne/,imeldatherinne
https://www.instagram.com/changyonggggg/,changyonggggg
https://www.instagram.com/kittendust/,kittendust
https://www.instagram.com/callistarum/,callistarum
https://www.instagram.com/williamroberts08/,williamroberts08
https://www.instagram.com/terangwicaksono/,terangwicaksono
https://www.instagram.com/shakiranajwa/,shakiranajwa
https://www.instagram.com/er1ca/,er1ca
https://www.instagram.com/bazaarindonesia/,bazaarindonesia
https://www.instagram.com/fsmgmt.id/,fsmgmt.id
https://www.instagram.com/yasaminjasem/,yasaminjasem
https://www.instagram.com/zaraadhsty/,zaraadhsty
https://www.instagram.com/jourdy.pranata/,jourdy.pranata
https://www.instagram.com/jethro.armand/,jethro.armand
https://www.instagram.com/ntsana/,ntsana
https://www.instagram.com/viranada_wd/,viranada_wd
https://www.instagram.com/aaliyah.massaid/,aaliyah.massaid
https://www.instagram.com/angga/,angga
https://www.instagram.com/xolovelyayana/,xolovelyayana
https://www.instagram.com/davinaakaramoy/,davinaakaramoy
https://www.instagram.com/idgitaf/,idgitaf
https://www.instagram.com/adrianarmanasco/,adrianarmanasco
https://www.instagram.com/nadiyarawil/,nadiyarawil
https://www.instagram.com/rintiksedu/,rintiksedu
https://www.instagram.com/vidiooriginals/,vidiooriginals
https://www.instagram.com/venemapictures/,venemapictures
https://www.instagram.com/mikha_hernan/,mikha_hernan
https://www.instagram.com/bondol.jpg/,bondol.jpg
https://www.instagram.com/bryandomani_bd_/,bryandomani_bd_
https://www.instagram.com/aphrodit.a/,aphrodit.a
https://www.instagram.com/mawar_eva/,mawar_eva
https://www.instagram.com/raisyabawazier/,raisyabawazier
https://www.instagram.com/abellyc/,abellyc
https://www.instagram.com/caitlinhalderman/,caitlinhalderman
https://www.instagram.com/kaay.raw/,kaay.raw
https://www.instagram.com/wshusen/,wshusen
https://www.instagram.com/claudiaudie/,claudiaudie
https://www.instagram.com/loveable.redaksi/,loveable.redaksi
https://www.instagram.com/deryzky/,deryzky
https://www.instagram.com/raihaanun/,raihaanun
https://www.instagram.com/wardahbeauty/,wardahbeauty
https://www.instagram.com/kylakameron/,kylakameron
https://www.instagram.com/raniaayamin/,raniaayamin
https://www.instagram.com/shabrinaaluna/,shabrinaaluna
https://www.instagram.com/nkcthi/,nkcthi
https://www.instagram.com/nadialaydrus/,nadialaydrus
https://www.instagram.com/cha_schagerl/,cha_schagerl
https://www.instagram.com/michimomo/,michimomo
https://www.instagram.com/adipati/,adipati
https://www.instagram.com/jesicaceren/,jesicaceren
https://www.instagram.com/alwifachry/,alwifachry
https://www.instagram.com/luthfiaulia/,luthfiaulia
https://www.instagram.com/cakecaine/,cakecaine
https://www.instagram.com/galihsoedirdjo/,galihsoedirdjo
https://www.instagram.com/nianaguerrero/,nianaguerrero
https://www.instagram.com/liarahmat13/,liarahmat13
https://www.instagram.com/yosiemauliza/,yosiemauliza
https://www.instagram.com/just.yumi/,just.yumi
https://www.instagram.com/amandarawles/,amandarawles
https://www.instagram.com/vidialdiano/,vidialdiano
https://www.instagram.com/lauvsongs/,lauvsongs
https://www.instagram.com/wodecase.id/,wodecase.id
https://www.instagram.com/marshatimothy/,marshatimothy
https://www.instagram.com/greciasuhardi/,greciasuhardi
https://www.instagram.com/jejesoekarno/,jejesoekarno
https://www.instagram.com/zivamagnolya/,zivamagnolya
https://www.instagram.com/nandaarsynt/,nandaarsynt
https://www.instagram.com/vondear/,vondear
https://www.instagram.com/omardaniel_/,omardaniel_
https://www.instagram.com/yogaarizona/,yogaarizona
https://www.instagram.com/danialrifki/,danialrifki
https://www.instagram.com/ditodarmawan__/,ditodarmawan__
https://www.instagram.com/faizvishal/,faizvishal
https://www.instagram.com/dwisasono/,dwisasono
https://www.instagram.com/randymartinnn/,randymartinnn
https://www.instagram.com/clarinnaputri/,clarinnaputri
https://www.instagram.com/twindararasati/,twindararasati
https://www.instagram.com/blackpinkofficial/,blackpinkofficial
https://www.instagram.com/azela.putri/,azela.putri
https://www.instagram.com/hasyakyla/,hasyakyla
https://www.instagram.com/linda_darmawan03/,linda_darmawan03
https://www.instagram.com/ojmo_/,ojmo_
https://www.instagram.com/abberahman85/,abberahman85
https://www.instagram.com/jaiiibruh/,jaiiibruh
https://www.instagram.com/claudiasulewski/,claudiasulewski
https://www.instagram.com/khivaiskak/,khivaiskak
https://www.instagram.com/chikifawzi/,chikifawzi
https://www.instagram.com/gheaindrawari/,gheaindrawari
https://www.instagram.com/anaoctarina/,anaoctarina
https://www.instagram.com/patricialourence/,patricialourence
https://www.instagram.com/philipekarunia/,philipekarunia
https://www.instagram.com/siviazizah/,siviazizah
https://www.instagram.com/time.international/,time.international
https://www.instagram.com/niapriskilla/,niapriskilla
https://www.instagram.com/js_khairen/,js_khairen
https://www.instagram.com/galabbythahira/,galabbythahira
https://www.instagram.com/danniasalsabilla/,danniasalsabilla
https://www.instagram.com/zahwaqilah/,zahwaqilah
https://www.instagram.com/anarghia/,anarghia
https://www.instagram.com/bebytsabina/,bebytsabina
https://www.instagram.com/farhanrasyidd/,farhanrasyidd
https://www.instagram.com/odaniooo/,odaniooo
https://www.instagram.com/ansellmaputri/,ansellmaputri
https://www.instagram.com/riacinnamon/,riacinnamon
https://www.instagram.com/gushcloudid/,gushcloudid
https://www.instagram.com/raissarmdhn/,raissarmdhn
https://www.instagram.com/nisacookie/,nisacookie
https://www.instagram.com/halidbadjri_fs/,halidbadjri_fs
https://www.instagram.com/jakecgoss/,jakecgoss
https://www.instagram.com/kesharatuliu05/,kesharatuliu05
https://www.instagram.com/raniamarchella/,raniamarchella
https://www.instagram.com/aruanmarsha/,aruanmarsha
https://www.instagram.com/mvppictures_id/,mvppictures_id
https://www.instagram.com/bojvoyej/,bojvoyej
https://www.instagram.com/rezachandika/,rezachandika
https://www.instagram.com/davaheinzsyahry/,davaheinzsyahry
https://www.instagram.com/sandypradana88/,sandypradana88
https://www.instagram.com/naura.ayu/,naura.ayu
https://www.instagram.com/natasharyder/,natasharyder
https://www.instagram.com/alodita/,alodita
https://www.instagram.com/refalhady/,refalhady
https://www.instagram.com/arash_buana/,arash_buana
https://www.instagram.com/kiaraleswara/,kiaraleswara
https://www.instagram.com/ratnajuni/,ratnajuni
https://www.instagram.com/ninakpw/,ninakpw
https://www.instagram.com/zidnylthfa/,zidnylthfa
https://www.instagram.com/ericaputrii/,ericaputrii
https://www.instagram.com/yurayunita/,yurayunita
https://www.instagram.com/nadhira.ulya/,nadhira.ulya
https://www.instagram.com/vaurindaaisha/,vaurindaaisha
https://www.instagram.com/tynadwijayanti/,tynadwijayanti
https://www.instagram.com/nadyamaudy/,nadyamaudy
https://www.instagram.com/bellagap/,bellagap
https://www.instagram.com/jusuf_long/,jusuf_long
https://www.instagram.com/sarahayuh_/,sarahayuh_
https://www.instagram.com/jehaku.official/,jehaku.official
https://www.instagram.com/keshyavlr/,keshyavlr
https://www.instagram.com/amandasmess/,amandasmess
https://www.instagram.com/jeremiemoeremans/,jeremiemoeremans
https://www.instagram.com/aratst/,aratst
https://www.instagram.com/annetteedoarda/,annetteedoarda
https://www.instagram.com/feliandreca/,feliandreca
https://www.instagram.com/daraarafah/,daraarafah
https://www.instagram.com/sharstagramm/,sharstagramm
https://www.instagram.com/barliasmara/,barliasmara
https://www.instagram.com/graceayuari/,graceayuari
https://www.instagram.com/roses_are_rosie/,roses_are_rosie
https://www.instagram.com/antonioblancojr/,antonioblancojr
https://www.instagram.com/shireeenz/,shireeenz
https://www.instagram.com/dagelan/,dagelan
https://www.instagram.com/dindakirana.s/,dindakirana.s
https://www.instagram.com/nadyaaqilla/,nadyaaqilla
https://www.instagram.com/adikaraf/,adikaraf
https://www.instagram.com/indrabrasco/,indrabrasco
https://www.instagram.com/fomstudio_/,fomstudio_
https://www.instagram.com/rsn.dw/,rsn.dw
https://www.instagram.com/braynlim/,braynlim
https://www.instagram.com/saniachia/,saniachia
https://www.instagram.com/reginaaphx/,reginaaphx
https://www.instagram.com/jenniferchrstie/,jenniferchrstie
https://www.instagram.com/tissabiani/,tissabiani
https://www.instagram.com/alikaislamadina/,alikaislamadina
https://www.instagram.com/ifanhartanto/,ifanhartanto
https://www.instagram.com/jovitakaren/,jovitakaren
https://www.instagram.com/modynz/,modynz
https://www.instagram.com/dikta/,dikta
https://www.instagram.com/steffizamoraaa/,steffizamoraaa
https://www.instagram.com/syifahadju/,syifahadju
https://www.instagram.com/rurypadwa/,rurypadwa
https://www.instagram.com/kevinardillova/,kevinardillova
https://www.instagram.com/m.olndo/,m.olndo
https://www.instagram.com/deboys13/,deboys13
https://www.instagram.com/tiaratrdp_/,tiaratrdp_
https://www.instagram.com/elinaaaaajoerg/,elinaaaaajoerg
https://www.instagram.com/lulu_anggriani/,lulu_anggriani
https://www.instagram.com/lalalalisa_m/,lalalalisa_m
https://www.instagram.com/noldapocha/,noldapocha
https://www.instagram.com/ghazi_alhabsyi/,ghazi_alhabsyi
https://www.instagram.com/ariirhamm/,ariirhamm
https://www.instagram.com/stefanytalita/,stefanytalita
https://www.instagram.com/riomotret/,riomotret
https://www.instagram.com/naziracnoer/,naziracnoer
https://www.instagram.com/awdella/,awdella
https://www.instagram.com/natasharizkynew/,natasharizkynew
https://www.instagram.com/patragumala/,patragumala
https://www.instagram.com/ersyaurel/,ersyaurel
https://www.instagram.com/komengkemong/,komengkemong
https://www.instagram.com/mpok.atiek/,mpok.atiek
https://www.instagram.com/arcollectionn_/,arcollectionn_
https://www.instagram.com/diyanahnurra/,diyanahnurra
https://www.instagram.com/ranzkyle/,ranzkyle
https://www.instagram.com/megandomani1410/,megandomani1410
https://www.instagram.com/joviadhiguna/,joviadhiguna
https://www.instagram.com/julianasteph/,julianasteph
https://www.instagram.com/vicymelanie/,vicymelanie
https://www.instagram.com/dorippu/,dorippu
https://www.instagram.com/pauljasonklein/,pauljasonklein
https://www.instagram.com/adiskayl/,adiskayl
https://www.instagram.com/dewanggaelsandro/,dewanggaelsandro
https://www.instagram.com/dermalogia/,dermalogia
https://www.instagram.com/bianca_nelwan/,bianca_nelwan
https://www.instagram.com/kyranayda/,kyranayda
https://www.instagram.com/turahparthayana/,turahparthayana
https://www.instagram.com/pevpearce/,pevpearce
https://www.instagram.com/ariefmuhammad/,ariefmuhammad
https://www.instagram.com/jenniferbachdim/,jenniferbachdim
https://www.instagram.com/fauzan_nasrul/,fauzan_nasrul
https://www.instagram.com/sarahazka/,sarahazka
https://www.instagram.com/princessmegonondo/,princessmegonondo
https://www.instagram.com/marishachacha/,marishachacha
https://www.instagram.com/sandythema/,sandythema
https://www.instagram.com/niaswara_/,niaswara_
https://www.instagram.com/akbaralaziz/,akbaralaziz
https://www.instagram.com/ssseruni/,ssseruni
https://www.instagram.com/ardhitopramono/,ardhitopramono
https://www.instagram.com/tiarapangestika/,tiarapangestika
https://www.instagram.com/zendaya/,zendaya
https://www.instagram.com/tutorialhidub/,tutorialhidub
https://www.instagram.com/cindercella/,cindercella
https://www.instagram.com/tommyprabowo/,tommyprabowo
https://www.instagram.com/vinnagracia/,vinnagracia
https://www.instagram.com/tioradit/,tioradit
https://www.instagram.com/putriayeesha/,putriayeesha
https://www.instagram.com/dessydiniyanti/,dessydiniyanti
https://www.instagram.com/nenagiesta/,nenagiesta
https://www.instagram.com/faynabilalxndr/,faynabilalxndr
https://www.instagram.com/barrykusuma/,barrykusuma
https://www.instagram.com/gita_bhebhita/,gita_bhebhita
https://www.instagram.com/alyaanz/,alyaanz
https://www.instagram.com/ochiipramita/,ochiipramita
https://www.instagram.com/rifankalbuadi7/,rifankalbuadi7
https://www.instagram.com/rozanqaidi/,rozanqaidi
https://www.instagram.com/gracelsyy/,gracelsyy
https://www.instagram.com/shandywilliam_/,shandywilliam_
https://www.instagram.com/satinezaneta/,satinezaneta
https://www.instagram.com/dessey/,dessey
https://www.instagram.com/malidadinda_/,malidadinda_
https://www.instagram.com/andirazh/,andirazh
https://www.instagram.com/anjanidinavdw/,anjanidinavdw
https://www.instagram.com/sentot_sahid/,sentot_sahid
https://www.instagram.com/ussiyfauziah/,ussiyfauziah
https://www.instagram.com/carissaperusset/,carissaperusset
https://www.instagram.com/honeyrobertss_/,honeyrobertss_
https://www.instagram.com/ifyalyssa/,ifyalyssa
https://www.instagram.com/aldymldni/,aldymldni
https://www.instagram.com/luluelhasbu/,luluelhasbu
https://www.instagram.com/abdelachrian/,abdelachrian
https://www.instagram.com/hamidahrachmayanti/,hamidahrachmayanti
https://www.instagram.com/sabinaaksaa/,sabinaaksaa
https://www.instagram.com/sunhairstylist/,sunhairstylist
https://www.instagram.com/almaaurelia/,almaaurelia
https://www.instagram.com/aulion/,aulion
https://www.instagram.com/dewiahmaad/,dewiahmaad
https://www.instagram.com/lelepons/,lelepons
https://www.instagram.com/ninaseptiani/,ninaseptiani
https://www.instagram.com/bima24prasetyo/,bima24prasetyo
https://www.instagram.com/salmaastia/,salmaastia
https://www.instagram.com/moroccanmusthaves/,moroccanmusthaves
https://www.instagram.com/vebbypalwinta/,vebbypalwinta
https://www.instagram.com/jojoanito/,jojoanito
https://www.instagram.com/emyaghnia/,emyaghnia
https://www.instagram.com/diantyy.a/,diantyy.a
https://www.instagram.com/rachelpatricia/,rachelpatricia
https://www.instagram.com/keisyalevronka/,keisyalevronka
https://www.instagram.com/intanmita/,intanmita
https://www.instagram.com/fidelhertamakeup/,fidelhertamakeup
https://www.instagram.com/irzannfaiq/,irzannfaiq
https://www.instagram.com/ilham_nk/,ilham_nk
https://www.instagram.com/rakoprijanto/,rakoprijanto
https://www.instagram.com/megaiskanti/,megaiskanti
https://www.instagram.com/cinta_brian/,cinta_brian
https://www.instagram.com/dermatologistjakarta/,dermatologistjakarta
https://www.instagram.com/filltheblankspace/,filltheblankspace
https://www.instagram.com/rekawijayakusuma/,rekawijayakusuma
https://www.instagram.com/henandrya/,henandrya
https://www.instagram.com/agrasuseno/,agrasuseno
https://www.instagram.com/zulfamaharani/,zulfamaharani
https://www.instagram.com/prillylatuconsina96/,prillylatuconsina96
https://www.instagram.com/jeqaf/,jeqaf
https://www.instagram.com/yclionk/,yclionk
https://www.instagram.com/boimlenno/,boimlenno
https://www.instagram.com/naufalazharr/,naufalazharr
https://www.instagram.com/tianamannering/,tianamannering
https://www.instagram.com/yow.ha/,yow.ha
https://www.instagram.com/pejalankembarr/,pejalankembarr
https://www.instagram.com/eduwart_/,eduwart_
https://www.instagram.com/rahmaniaastrini/,rahmaniaastrini
https://www.instagram.com/abrar_aabs/,abrar_aabs
https://www.instagram.com/rachgoddard/,rachgoddard
https://www.instagram.com/rebeccatamara/,rebeccatamara
https://www.instagram.com/aphang_alimsudio/,aphang_alimsudio
https://www.instagram.com/cassandraslee/,cassandraslee
https://www.instagram.com/wanda_haraa/,wanda_haraa
https://www.instagram.com/naonomnom/,naonomnom
https://www.instagram.com/jakartakonser/,jakartakonser
https://www.instagram.com/ersamayori/,ersamayori
https://www.instagram.com/suciaurelias/,suciaurelias
https://www.instagram.com/kafisilly/,kafisilly
https://www.instagram.com/imaji_zoe/,imaji_zoe
https://www.instagram.com/ichachndra/,ichachndra
https://www.instagram.com/radinindranayaka/,radinindranayaka
https://www.instagram.com/le.roseville/,le.roseville
https://www.instagram.com/umayshahab/,umayshahab
https://www.instagram.com/ryanogilvy/,ryanogilvy
https://www.instagram.com/lamilami.official/,lamilami.official
https://www.instagram.com/vontiansuwandi/,vontiansuwandi
https://www.instagram.com/teukuryz/,teukuryz
https://www.instagram.com/devinaureel/,devinaureel
https://www.instagram.com/quinanitadiva/,quinanitadiva
https://www.instagram.com/letsfreedive_indonesia/,letsfreedive_indonesia
https://www.instagram.com/bembygusti/,bembygusti
https://www.instagram.com/ameliayusanaa/,ameliayusanaa
https://www.instagram.com/ichsanakbar/,ichsanakbar
https://www.instagram.com/nielshepherd/,nielshepherd
https://www.instagram.com/iwanlatiff/,iwanlatiff
https://www.instagram.com/wear.shoera/,wear.shoera
https://www.instagram.com/salshardls/,salshardls
https://www.instagram.com/sandysandyprasetyo/,sandysandyprasetyo
https://www.instagram.com/shareefadaanish/,shareefadaanish
https://www.instagram.com/agnesnaomi/,agnesnaomi
https://www.instagram.com/dheaseto/,dheaseto
https://www.instagram.com/adityaharivonda/,adityaharivonda
https://www.instagram.com/nataliezenn24/,nataliezenn24
https://www.instagram.com/joyagh/,joyagh
https://www.instagram.com/raffinagita1717/,raffinagita1717
https://www.instagram.com/nagrapakusadewo/,nagrapakusadewo
https://www.instagram.com/dianferdisa/,dianferdisa
https://www.instagram.com/im.amru/,im.amru
https://www.instagram.com/wanikayrie/,wanikayrie
https://www.instagram.com/sarahtuff_/,sarahtuff_
https://www.instagram.com/desmondamos/,desmondamos
https://www.instagram.com/irsyachendikiawan/,irsyachendikiawan"""

# Fungsi untuk mendapatkan rekomendasi calon klien dengan loading 10 detik
def get_recommendations_with_loading(num_recommendations=12):
    """Mendapatkan rekomendasi calon klien dengan loading 10 detik"""
    # Simulasi loading 10 detik
    time.sleep(10)
    
    instagram_df = pd.read_csv(StringIO(INSTAGRAM_DATA))
    
    if len(instagram_df) == 0:
        return pd.DataFrame(columns=['Username', 'Link Instagram'])
    
    # Ambil sampel acak dari data
    if len(instagram_df) <= num_recommendations:
        return instagram_df.sample(n=len(instagram_df))
    else:
        return instagram_df.sample(n=num_recommendations)

# Header utama
st.markdown('<h1 class="main-header">PARTHAISTIC - DAHSBOARD REKOMENDASI CALON KLIEN</h1>', unsafe_allow_html=True)

# Hero Section dengan animasi
st.markdown("""
<div class="hero-section">
    <h2 style="color: #2E86AB; margin-bottom: 1rem; animation: fadeIn 1s ease-out, float 6s ease-in-out infinite;">✨ Temukan Calon Klien Terbaik</h2>
    <p style="color: #666; font-size: 1.2rem; animation: fadeIn 2s ease-out;">
        Dashboard rekomendasi calon klien berbasis data Instagram dengan algoritma cerdas untuk bisnis Anda
    </p>
    
    <!-- Floating elements -->
    <div class="floating-element">📊</div>
    <div class="floating-element">🔍</div>
    <div class="floating-element">🎯</div>
    <div class="floating-element">✨</div>
</div>
""", unsafe_allow_html=True)

# Stats Section dengan animasi
col1, col2, col3 = st.columns(3)

with col2:
    st.markdown("""
    <div class="stats-card">
        <h3 style="animation: pulse 2s infinite;">100%</h3>
        <p style="color: #666;">Data Terverifikasi</p>
        <p style="color: #666; font-size: 0.9rem; margin-top: 10px;">Rekomendasi Pengambilan Data Dari Instagram</p>
    </div>
    """, unsafe_allow_html=True)

# Pencarian Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #2E86AB; margin-bottom: 1.5rem; animation: fadeIn 1s ease-out;'>🔍 Mulai Pencarian</h2>", unsafe_allow_html=True)

# Tombol pencarian utama dengan animasi
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Mulai Pencarian Calon Klien", use_container_width=True, type="primary"):
        st.session_state['search_triggered'] = True
        st.session_state['loading_start_time'] = time.time()

# Cek jika pencarian sudah dipicu
if 'search_triggered' in st.session_state and st.session_state['search_triggered']:
    # Tampilkan animasi loading yang keren
    st.markdown("""
    <div class="loading-container">
        <div class="loading-title">🔍 Mencari Calon Klien Terbaik</div>
        <div class="loading-subtitle">Menganalisis database Instagram untuk rekomendasi terpersonal...</div>
        
        <div class="particles">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        
        <div class="loading-stats">
            <div class="loading-stat">
                <div class="loading-stat-number">850+</div>
                <div class="loading-stat-label">Calon Klien</div>
            </div>
            <div class="loading-stat">
                <div class="loading-stat-number">💯</div>
                <div class="loading-stat-label">Terverifikasi</div>
            </div>
            <div class="loading-stat">
                <div class="loading-stat-number">🎯</div>
                <div class="loading-stat-label">Target Presisi</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dapatkan rekomendasi dengan loading 10 detik
    recommendations = get_recommendations_with_loading(num_recommendations=6)
    
    # Clear loading
    st.empty()
    
    if len(recommendations) > 0:
        st.markdown(f"""
        <div style="text-align: center; animation: success 1s ease-out;">
            <div class="result-count">🎉 Ditemukan {len(recommendations)} calon klien potensial!</div>
            <p style="color: #666; margin-bottom: 2rem; animation: fadeIn 1s ease-out;">
                Berikut adalah rekomendasi calon klien yang cocok dengan profil bisnis Anda:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tampilkan rekomendasi dalam grid dengan animasi
        st.markdown('<div class="result-section" style="animation: fadeIn 1s ease-out;">', unsafe_allow_html=True)
        
        # Buat 3 kolom untuk tampilan yang lebih rapi
        cols = st.columns(3)
        
        for idx, (_, row) in enumerate(recommendations.iterrows()):
            with cols[idx % 3]:
                username = row['Username']
                instagram_link = row['Link Instagram']
                
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="username-badge">@{username}</div>
                    <div style="margin: 0.8rem 0;">
                        <p style="margin: 0.3rem 0; font-size: 0.95rem;">
                            <strong>Profil:</strong> {username}<br>
                            <strong style="color: #E4405F;">Instagram</strong> 
                            <a href="{instagram_link}" target="_blank" class="instagram-link">
                                <span class="instagram-icon">📷</span> Kunjungi Profil
                            </a>
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tombol refresh di tengah
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Cari Rekomendasi Lainnya", use_container_width=True):
                st.session_state['search_triggered'] = True
                st.session_state['loading_start_time'] = time.time()
                st.rerun()
        
        # Informasi tambahan dengan animasi
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: #f8f9fa; border-radius: 10px; animation: fadeIn 1s ease-out;">
            <h4 style="color: #2E86AB;">💡 Tips untuk Menghubungi Calon Klien</h4>
            <p style="color: #666; margin-bottom: 0;">
                1. Perkenalkan diri dan bisnis Anda dengan jelas<br>
                2. Jelaskan nilai tambah yang Anda tawarkan<br>
                3. Buat penawaran yang personal dan relevan<br>
                4. Follow akun Instagram mereka untuk engagement yang lebih baik
            </p>
        </div>
        """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import re
import base64
from io import StringIO, BytesIO

# Konfigurasi Halaman
st.set_page_config(
    page_title="Analisis Klien Parthaistic",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .insight-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 5px solid #2E86AB;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .client-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2E86AB;
        transition: transform 0.2s;
    }
    .client-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .need-indicator {
        background: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .hashtag-indicator {
        background: #007bff;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .post-content {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
        font-style: italic;
        max-height: 150px;
        overflow-y: auto;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
    .search-box {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .download-section {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .target-client-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .similar-client-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border: 1px solid #ff9800;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .similar-client-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .similarity-score {
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .client-info-row {
        display: flex;
        justify-content: space-between;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    .client-info-label {
        font-weight: 600;
        color: #555;
    }
    .client-info-value {
        color: #333;
    }
    .profiling-section {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .youtube-link {
        color: #ff0000;
        text-decoration: none;
        font-weight: bold;
        transition: color 0.3s ease;
    }
    .youtube-link:hover {
        color: #cc0000;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk membuat sample CSV lengkap berdasarkan data Excel
def create_complete_csv_template():
    template_data = """Name,Year,Type,Service 1,Service 2,Service 3,Regular End Period,Link Youtube
Youtubers Depok,2020,Community,Custom Video Production,,,,
LDK Senada STT NF,2021,Community,Project Musikal Pemuda Indonesia,Video Editor,,,
Jakarta Youth Choir,2021,Community,Project Musikal Pemuda Indonesia,,,,
Depok Bercerita,2021,Community,All In Regular,,,2023,https://youtu.be/PBrwimauGUk?si=ODTaGksvck3DdGLz
PKS Muda,2021,Community,All In Regular,,,2022,
BIGREDS Depok,2022,Community,Event Documentation,,,,
PPI UK,2023,Community,Short Video,,,,
Ikatan Ibu Brantas Abipraya,2023,Community,Event Documentation,,,,
FSLDK Jadebek,2023,Community,Video Editor,,,,
Nafkah Community,2023,Community,All In Regular,,,2024,
Singing Engineers,2024,Community,Event Documentation,,,,
Dancing Engineers,2024,Community,Event Documentation,,,,
Youth Talent Alliance,2024,Community,Video Editor,,,,
International Madani Association,2025,Community,Video Editor,,,,
Pulang Production,2020,Corporate,Custom Video Production,,,,
Rumah Kepemimpinan,2020,Corporate,All In Regular,,,2020,
Putra Daerah Membangun,2020,Corporate,Video Editor,,,,
C4Change,2021,Corporate,Video Editor,,,,
Pahlawan Music School,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Duta Futsal,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Rabbani,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Adhiputro Konsultan Internasional,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Mi Studio,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Dompet Dhuafa Sumsel,2021,Corporate,Video Editor,,,,
Themefood,2021,Corporate,Commercial Video Production,,,,
Muslimbox,2021,Corporate,Commercial Video Production,,,,
Indekstat,2021,Corporate,Event Documentation,,,,
STT NF,2021,Corporate,Company Profile,,,,
Magister Manajemen UI,2022,Corporate,E-Learning Video,,,,
MI Taufiqurrahman 2,2022,Corporate,Event Documentation,Photographer,,,
Penerbit Luxima,2022,Corporate,Commercial Video Production,,,,
Top Karir Indonesia,2022,Corporate,Video Editor,,,,
SMKN 51 Jakarta,2022,Corporate,Workshop,,,,
Harrington Official Store,2023,Corporate,Commercial Video Production,,,,
Modernvet,2023,Corporate,Company Profile,,,,
Teh AI,2023,Corporate,Commercial Video Production,,,,
OFFO Living,2023,Corporate,Short Video,,,,
Yayasan Jantung Indonesia,2023,Corporate,Custom Video Production,,,,
Safia Natural,2023,Corporate,Event Documentation,,,,
PTQ Griya Quran,2024,Corporate,Company Profile,Event Documentation,,,
Konservasi Indonesia,2024,Corporate,Event Documentation,,,,
Lingkar Keluarga Matahati,2024,Corporate,Custom Video Production,,,,
Kurita Indonesia,2024,Corporate,Video Editor,,,,
Klinik Soragan 100 C,2024,Corporate,Video Editor,,,,
Coway,2024,Corporate,Commercial Video Production,,,,
SMP Muhammadiyah 2,2024,Corporate,Photographer,,,,
Yayasan Muda Cemerlang,2025,Corporate,Workshop,,,,
Rizky Yudo,2020,Figure,All In Regular,,,2026,
Oni Sahroni,2020,Figure,All In Regular,,,2020,
Ibnu Wardani,2021,Figure,Video Editor,,,,
Ongky Uktolseja,2021,Figure,Project Musikal Pemuda Indonesia,Video Editor,Videographer,
Anton,2021,Figure,Video Editor,,,,
Rizky Januardi,2021,Figure,Video Editor,,,,
Ash Shiddiq,2021,Figure,Video Editor,,,,
Imam Budi Hartono,2021,Figure,Short Video,,,,
The Winfields,2021,Figure,All In Regular,,,2022,https://youtu.be/_CWZxrOrm38?si=W5DtRt4iEYmEW3pl
The Vanderheydes,2022,Figure,All In Regular,,,2023,https://youtu.be/ehNX8_v-5Qw?si=Xtny4q-N3thEifkH
Shenina Cinnamon,2022,Figure,Short Video,,,,
Aqeela Calista,2022,Figure,Short Video,,,,
Hanafiah Muhammad,2022,Figure,Video Editor Regular,,,2023,
Valerie-Veronika TWNS,2022,Figure,All In Regular,,,2022,https://youtu.be/rUX44bQdxYY?si=VtyntCAwypd58Xxz
Raisa Chairunnisa,2022,Figure,Short Film,,,,
SRAH,2022,Figure,All In Regular,,,2023,https://youtu.be/zHU8qR18x6g?si=mKF-U9875mDif-vV
Hanggini,2022,Figure,Short Video,,,,
Doula Alia,2022,Figure,All In Regular,,,2023,https://youtu.be/USTRbIR-_sA?si=pdhZ4S2HLQOWcmzB
Jelita,2022,Figure,All In Regular,,,2022,
Ranty Maria,2022,Figure,Video Editor,,,,
Michin Family,2022,Figure,Video Editor,Videographer,,
Nanda Arsyinta,2022,Figure,All In Regular,,,2023,https://youtu.be/85Z12y6b2rk?si=O7VwLpd3etZ-36N-
Dr. Yuliani Chandranata,2023,Figure,All In Regular,,,2023,
Broto Laras Family,2023,Figure,Custom Video Production,,,,
Sarah Tumiwa,2023,Figure,All In Regular,,,2023,https://youtu.be/avhjB5mDSeg?si=F9mTogU9aZqEfavx
Sabrina Anggraini,2023,Figure,Video Editor,,,2023,https://youtu.be/GZYCgCL8GIw?si=BqvesLjtkN6B5Io1
Jefan Nathanio,2023,Figure,All In Regular,,,2024,https://youtu.be/UIm71CmByzY?si=Hv4324aqA02EGJUc
Handika Pratama,2023,Figure,Video Editor,Videographer,,
Zhafira Aqyla,2023,Figure,Event Documentation,Video Editor,,
DJ Freya,2023,Figure,All In Regular,,,2024,https://youtube.com/@dj_freya?si=hzW60V6H1upKwD2j
Agatha Chelsea,2023,Figure,Video Editor,,,,
Luthfi Aulia,2023,Figure,Creative Writer,,,,
Sabrina Najwa Aulia,2024,Figure,Video Editor,,,,
Rahmad Junaidi,2024,Figure,All In Regular,,,2024,
Bang Ghozi,2024,Figure,All In Regular,,,2026,
BKPM RI,2021,Government,Event Documentation,,,,
Pemkot Depok,2021,Government,All In Regular,Workshop,,2024,
BPI Kemdikbud RI,2023,Government,Short Video,,,,
Brantas Abipraya,2023,Government,Event Documentation,,,,
KKP RI,2024,Government,Event Documentation,,,,
USAID,2024,Government,Event Documentation,,,,
WWF Indonesia,2024,Government,Event Documentation,,,,
Investabook,2024,Government,All In Regular,,,2024,
DAMRI,2021,SOE,Video Editor,,,,
TMII,2021,SOE,Project Musikal Pemuda Indonesia,,,,
BRI,2022,SOE,E-Learning Video,,,,
Indra Karya,2022,SOE,Video Editor,,,,
RSUD ASA Depok,2024,SOE,Company Profile,,,,
Gag Nikel,2024,SOE,Company Profile,Short Film,Photographer,"""
    return template_data

# Fungsi untuk mencari klien serupa
def find_similar_clients(target_client, df, top_n=5):
    """Mencari klien dengan profil serupa berdasarkan berbagai faktor"""
    if target_client not in df['Name'].values:
        return None
    
    target_row = df[df['Name'] == target_client].iloc[0]
    similarities = []
    
    for idx, row in df.iterrows():
        if row['Name'] == target_client:
            continue
            
        similarity_score = 0
        
        # 1. Kesamaan Tipe Klien (bobot: 30%)
        if row['Type'] == target_row['Type']:
            similarity_score += 30
        
        # 2. Kedekatan Tahun (bobot: 20%)
        year_diff = abs(row['Year'] - target_row['Year'])
        if year_diff == 0:
            similarity_score += 20
        elif year_diff <= 1:
            similarity_score += 15
        elif year_diff <= 2:
            similarity_score += 10
        elif year_diff <= 3:
            similarity_score += 5
        
        # 3. Kesamaan Layanan (bobot: 30%)
        target_services = set(target_row['Services'])
        row_services = set(row['Services'])
        
        if target_services and row_services:
            # Jaccard similarity untuk layanan
            intersection = len(target_services.intersection(row_services))
            union = len(target_services.union(row_services))
            if union > 0:
                jaccard_similarity = intersection / union
                similarity_score += jaccard_similarity * 30
        
        # 4. Kesamaan Status Loyalitas (bobot: 15%)
        if row['Is_Loyal'] == target_row['Is_Loyal']:
            similarity_score += 15
        
        # 5. Kesamaan Jumlah Layanan (bobot: 5%)
        service_count_diff = abs(row['Service_Count'] - target_row['Service_Count'])
        if service_count_diff == 0:
            similarity_score += 5
        elif service_count_diff <= 1:
            similarity_score += 3
        
        similarities.append({
            'Name': row['Name'],
            'Similarity_Score': similarity_score,
            'Type': row['Type'],
            'Year': row['Year'],
            'Services': row['Services'],
            'Is_Loyal': row['Is_Loyal'],
            'Link_Youtube': row.get('Link_Youtube', ''),
            'Service_Count': row['Service_Count']
        })
    
    similarities_df = pd.DataFrame(similarities)
    return similarities_df.nlargest(top_n, 'Similarity_Score')

# Header utama
st.markdown('<h1 class="main-header">🎬 Dasbor Analisis Klien Parthaistic</h1>', unsafe_allow_html=True)

# Load data existing clients
@st.cache_data
def load_and_process_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            # Cek apakah file Excel atau CSV
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            st.success("✅ Data berhasil dimuat!")
        except Exception as e:
            st.error(f"❌ Error membaca file: {e}")
            return None
    else:
        # Data default - menggunakan data lengkap
        data = create_complete_csv_template()
        df = pd.read_csv(StringIO(data))
        st.info("📄 Menggunakan data default. Upload file CSV/Excel untuk menggunakan data Anda sendiri.")
    
    # Proses data
    df['Regular End Period'] = pd.to_numeric(df['Regular End Period'], errors='coerce')
    
    services = []
    service_columns = [col for col in df.columns if col.startswith('Service')]
    
    for _, row in df.iterrows():
        client_services = []
        for col in service_columns:
            if pd.notna(row[col]) and str(row[col]).strip():
                client_services.append(str(row[col]).strip())
        services.append(client_services)
    
    df['Services'] = services
    df['Service_Count'] = df['Services'].apply(len)
    df['Is_Loyal'] = df['Regular End Period'].notna()
    df['Loyalty_Duration'] = df['Regular End Period'] - df['Year']
    df['Loyalty_Duration'] = df['Loyalty_Duration'].fillna(0)
    
    # Rename kolom Link Youtube untuk konsistensi
    if 'Link Youtube' in df.columns:
        df = df.rename(columns={'Link Youtube': 'Link_Youtube'})
    
    return df

# Area upload file dengan template download
st.subheader("📁 Upload Data CSV/Excel")

# Section download template
st.markdown("""
<div class="download-section">
    <h4>📋 Template CSV Format</h4>
    <p>Download template CSV lengkap dengan semua data klien Parthaistic untuk melihat format yang benar</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    # Tombol download template CSV lengkap
    template_csv_data = create_complete_csv_template()
    st.download_button(
        label="📥 Download Template CSV Lengkap",
        data=template_csv_data,
        file_name="template_klien_parthaistic_lengkap.csv",
        mime="text/csv",
        help="Download template dengan semua data klien untuk melihat format yang benar",
        use_container_width=True
    )

with col2:
    # Informasi format
    st.info("""
    **📋 Format Kolom CSV/Excel:**
    - **Name**: Nama klien/perusahaan
    - **Year**: Tahun mulai (2020-2025)
    - **Type**: Corporate/Figure/Community/Government/SOE
    - **Service 1-3**: Layanan yang digunakan
    - **Regular End Period**: Tahun berakhir (jika loyal)
    - **Link Youtube**: Link video YouTube hasil kerja sama
    """)

# Upload file
uploaded_file = st.file_uploader(
    "Pilih file CSV atau Excel Anda", 
    type=['csv', 'xlsx'],
    help="Upload file CSV atau Excel dengan format sesuai template yang dapat didownload di atas"
)

# Muat data
df = load_and_process_data(uploaded_file)

if df is not None:
    # Tab Dasbor Utama
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Gambaran Umum", 
        "🎯 Profiling Klien", 
        "🔍 Analisis Klien Loyal", 
        "💡 Wawasan Bisnis"
    ])

    with tab1:
        st.header("📊 Gambaran Umum Bisnis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(df)}</h3>
                <p>Total Klien</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            loyal_clients = len(df[df['Is_Loyal']])
            st.markdown(f"""
            <div class="metric-card">
                <h3>{loyal_clients}</h3>
                <p>Klien Loyal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            loyalty_rate = (loyal_clients / len(df) * 100) if len(df) > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>{loyalty_rate:.1f}%</h3>
                <p>Tingkat Loyalitas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_services = df['Service_Count'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_services:.1f}</h3>
                <p>Rata-rata Layanan/Klien</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Grafik distribusi klien
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Klien berdasarkan Tahun & Tipe")
            year_type_data = df.groupby(['Year', 'Type']).size().reset_index(name='Count')
            fig = px.bar(year_type_data, x='Year', y='Count', color='Type',
                        title="Distribusi Klien berdasarkan Tahun dan Tipe")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🥧 Distribusi Tipe Klien")
            type_counts = df['Type'].value_counts()
            fig = px.pie(values=type_counts.values, names=type_counts.index,
                        title="Distribusi Tipe Klien")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("🎯 Profiling Klien Tingkat Lanjut")
        
        # Container untuk profiling
        st.markdown('<div class="profiling-section">', unsafe_allow_html=True)
        
        # Bagian pencarian klien serupa
        st.subheader("🔍 Temukan Klien Serupa")
        st.markdown("Pilih klien untuk menemukan profil serupa berdasarkan tipe, layanan, tahun, dan status loyalitas:")
        
        selected_client = st.selectbox(
            "Pilih klien untuk analisis kesamaan:", 
            [""] + sorted(df['Name'].tolist()),
            key="client_similarity_selector"
        )
        
        if selected_client:
            similar_clients = find_similar_clients(selected_client, df, top_n=5)
            
            if similar_clients is not None and len(similar_clients) > 0:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Target client card
                    target_info = df[df['Name'] == selected_client].iloc[0]
                    loyalty_status = "Loyal" if target_info['Is_Loyal'] else "Non-loyal"
                    youtube_link = target_info.get('Link_Youtube', '')
                    
                    # Membuat link YouTube yang bisa diklik dengan markdown
                    youtube_display = "Tidak ada"
                    if youtube_link and str(youtube_link).strip() and str(youtube_link).strip() != 'nan':
                        youtube_display = f'<a href="{youtube_link}" target="_blank" class="youtube-link">🎬 Tonton Video di YouTube</a>'
                    
                    st.markdown(f"""
                    <div class="target-client-card">
                        <h4>📋 Klien Target</h4>
                        <h3 style="color: #1976d2; margin: 0.5rem 0;">{selected_client}</h3>
                        <div class="client-info-row">
                            <span class="client-info-label">Tipe:</span>
                            <span class="client-info-value">{target_info['Type']}</span>
                        </div>
                        <div class="client-info-row">
                            <span class="client-info-label">Tahun:</span>
                            <span class="client-info-value">{target_info['Year']}</span>
                        </div>
                        <div class="client-info-row">
                            <span class="client-info-label">Status:</span>
                            <span class="client-info-value">{loyalty_status}</span>
                        </div>
                        <div class="client-info-row">
                            <span class="client-info-label">YouTube:</span>
                            <span class="client-info-value">{youtube_display}</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <span class="client-info-label">Layanan ({target_info['Service_Count']}):</span><br>
                            <span class="client-info-value">{', '.join(target_info['Services'])}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Similar clients
                    st.markdown("### 🤝 Klien Paling Serupa")
                    
                    for idx, client in similar_clients.iterrows():
                        similarity_pct = client['Similarity_Score']
                        loyalty_status = "Loyal" if client['Is_Loyal'] else "Non-loyal"
                        youtube_link = client.get('Link_Youtube', '')
                        
                        # Membuat link YouTube yang bisa diklik
                        youtube_display = "Tidak ada"
                        if youtube_link and str(youtube_link).strip() and str(youtube_link).strip() != 'nan':
                            youtube_display = f'<a href="{youtube_link}" target="_blank" class="youtube-link">🎬 Tonton Video</a>'
                        
                        # Determine similarity level
                        if similarity_pct >= 70:
                            similarity_level = "🔥 Sangat Mirip"
                            card_style = "background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%); border-color: #4caf50;"
                        elif similarity_pct >= 50:
                            similarity_level = "⭐ Cukup Mirip"
                            card_style = "background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-color: #ff9800;"
                        else:
                            similarity_level = "💡 Sedikit Mirip"
                            card_style = "background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-color: #9c27b0;"
                        
                        st.markdown(f"""
                        <div class="similar-client-card" style="{card_style}">
                            <div class="similarity-score">Kesamaan: {similarity_pct:.1f}% - {similarity_level}</div>
                            <h4 style="margin: 0.5rem 0; color: #e65100;">{client['Name']}</h4>
                            <div class="client-info-row">
                                <span class="client-info-label">Tipe:</span>
                                <span class="client-info-value">{client['Type']}</span>
                            </div>
                            <div class="client-info-row">
                                <span class="client-info-label">Tahun:</span>
                                <span class="client-info-value">{client['Year']}</span>
                            </div>
                            <div class="client-info-row">
                                <span class="client-info-label">Status:</span>
                                <span class="client-info-value">{loyalty_status}</span>
                            </div>
                            <div class="client-info-row">
                                <span class="client-info-label">YouTube:</span>
                                <span class="client-info-value">{youtube_display}</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <span class="client-info-label">Layanan ({client['Service_Count']}):</span><br>
                                <span class="client-info-value">{', '.join(client['Services'])}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analisis layanan populer
        st.subheader("🎬 Analisis Popularitas Layanan")
        all_services = []
        for services_list in df['Services']:
            all_services.extend(services_list)
        
        if all_services:
            service_counts = pd.Series(all_services).value_counts().head(10)
            fig = px.bar(x=service_counts.values, y=service_counts.index, orientation='h',
                        title="10 Layanan Paling Populer")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🔍 Analisis Klien Loyal")
        
        loyal_df = df[df['Is_Loyal']].copy()
        
        if len(loyal_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👑 Karakteristik Klien Loyal")
                loyal_types = loyal_df['Type'].value_counts()
                fig = px.pie(values=loyal_types.values, names=loyal_types.index,
                            title="Klien Loyal berdasarkan Tipe")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🎬 Layanan Populer Klien Loyal")
                loyal_services = []
                for services in loyal_df['Services']:
                    loyal_services.extend(services)
                
                if loyal_services:
                    loyal_service_counts = pd.Series(loyal_services).value_counts().head(8)
                    fig = px.bar(x=loyal_service_counts.values, y=loyal_service_counts.index, 
                                orientation='h', title="Layanan Teratas di Kalangan Klien Loyal")
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tidak ada klien loyal yang ditemukan.")

    with tab4:
        st.header("💡 Wawasan Bisnis")
        
        # Generate insights
        insights = []
        
        # Analisis tren pertumbuhan
        yearly_growth = df.groupby('Year').size()
        if len(yearly_growth) > 1:
            latest_growth = yearly_growth.iloc[-1] - yearly_growth.iloc[-2]
            growth_rate = (latest_growth / yearly_growth.iloc[-2]) * 100 if yearly_growth.iloc[-2] > 0 else 0
            insights.append(f"📈 **Tren Pertumbuhan**: Pertumbuhan klien {growth_rate:+.1f}% dari {yearly_growth.index[-2]} ke {yearly_growth.index[-1]}")
        
        # Wawasan loyalitas
        if len(df[df['Is_Loyal']]) > 0:
            loyalty_rate = len(df[df['Is_Loyal']]) / len(df) * 100
            insights.append(f"👑 **Tingkat Loyalitas**: {loyalty_rate:.1f}% klien menjadi pelanggan setia")
        
        # Layanan paling populer
        if all_services:
            most_popular_service = pd.Series(all_services).value_counts().index[0]
            insights.append(f"🌟 **Layanan Paling Populer**: {most_popular_service} adalah layanan yang paling banyak diminta")
        
        # Analisis klien dengan video YouTube
        youtube_clients = df[df['Link_Youtube'].notna() & (df['Link_Youtube'] != '')]
        if len(youtube_clients) > 0:
            youtube_percentage = len(youtube_clients) / len(df) * 100
            insights.append(f"🎬 **Portofolio Video**: {len(youtube_clients)} klien ({youtube_percentage:.1f}%) memiliki video YouTube yang dapat ditampilkan")
        
        # Tampilkan wawasan
        for insight in insights:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ Tidak dapat memuat data. Periksa file CSV/Excel Anda.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎬 Dasbor Analisis Klien Parthaistic | Client Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import re
import time
import random
import json
import requests
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, RateLimitError
import base64
from io import StringIO

# Konfigurasi Halaman
st.set_page_config(
    page_title="Analisis Klien Parthaistic",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Kustom
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .insight-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 5px solid #2E86AB;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .client-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2E86AB;
        transition: transform 0.2s;
    }
    .client-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .need-indicator {
        background: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .hashtag-indicator {
        background: #007bff;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .post-content {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
        font-style: italic;
        max-height: 150px;
        overflow-y: auto;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
    .search-box {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .download-section {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .target-client-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .similar-client-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border: 1px solid #ff9800;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .similar-client-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .similarity-score {
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .client-info-row {
        display: flex;
        justify-content: space-between;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    .client-info-label {
        font-weight: 600;
        color: #555;
    }
    .client-info-value {
        color: #333;
    }
    .profiling-section {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .unified-search-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .engagement-metric {
        background: #17a2b8;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .location-indicator {
        background: #dc3545;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk membuat sample CSV lengkap
def create_complete_csv_template():
    template_data = """Name,Year,Type,Service 1,Service 2,Service 3,Regular End Period,Instagram
Pulang Production,2020,Corporate,Custom Video Production,,,,
Youtubers Depok,2020,Community,Custom Video Production,,,,
Rumah Kepemimpinan,2020,Corporate,All In Regular,,,2020,
Putra Daerah Membangun,2020,Corporate,Video Editor,,,,
Rizky Yudo,2020,Figure,All In Regular,,,2026,@rizkyyudo
Oni Sahroni,2020,Figure,All In Regular,,,2020,@onisahroni
C4Change,2021,Corporate,Video Editor,,,,
DAMRI,2021,SOE,Video Editor,,,,
Ibnu Wardani,2021,Figure,Video Editor,,,,
Pahlawan Music School,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
LDK Senada STT NF,2021,Community,Project Musikal Pemuda Indonesia,Video Editor,,,
Jakarta Youth Choir,2021,Community,Project Musikal Pemuda Indonesia,,,,
Ongky Uktolseja,2021,Figure,Project Musikal Pemuda Indonesia,Video Editor,Videographer,@ongkyuktolseja
Duta Futsal,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Rabbani,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Adhiputro Konsultan Internasional,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
Mi Studio,2021,Corporate,Project Musikal Pemuda Indonesia,,,,
TMII,2021,SOE,Project Musikal Pemuda Indonesia,,,,
Dompet Dhuafa Sumsel,2021,Corporate,Video Editor,,,,
Depok Bercerita,2021,Community,All In Regular,,,2023,
Themefood,2021,Corporate,Commercial Video Production,,,,
Muslimbox,2021,Corporate,Commercial Video Production,,,,
Indekstat,2021,Corporate,Event Documentation,,,,
BKPM RI,2021,Government,Event Documentation,,,,
PKS Muda,2021,Community,All In Regular,,,2022,
STT NF,2021,Corporate,Company Profile,,,,
Pemkot Depok,2021,Government,All In Regular,Workshop,,2024,
Anton,2021,Figure,Video Editor,,,,
Rizky Januardi,2021,Figure,Video Editor,,,,
Ash Shiddiq,2021,Figure,Video Editor,,,,
Imam Budi Hartono,2021,Figure,Short Video,,,,
The Winfields,2021,Figure,All In Regular,,,2022,@thewinfields
Magister Manajemen UI,2022,Corporate,E-Learning Video,,,,
BRI,2022,SOE,E-Learning Video,,,,
Indra Karya,2022,SOE,Video Editor,,,,
BIGREDS Depok,2022,Community,Event Documentation,,,,
MI Taufiqurrahman 2,2022,Corporate,Event Documentation,Photographer,,
Penerbit Luxima,2022,Corporate,Commercial Video Production,,,,
Top Karir Indonesia,2022,Corporate,Video Editor,,,,
SMKN 51 Jakarta,2022,Corporate,Workshop,,,,
The Vanderheydes,2022,Figure,All In Regular,,,2023,@thevanderheydes
Shenina Cinnamon,2022,Figure,Short Video,,,,@sheninacinnamon
Aqeela Calista,2022,Figure,Short Video,,,,@aqeelacalista
Hanafiah Muhammad,2022,Figure,Video Editor Regular,,,2023,@hanafiamh
Valerie-Veronika TWNS,2022,Figure,All In Regular,,,2022,@valerieveronika
Raisa Chairunnisa,2022,Figure,Short Film,,,,@raisachairunnisa
SRAH,2022,Figure,All In Regular,,,2023,@srah.official
Hanggini,2022,Figure,Short Video,,,,@hanggini
Doula Alia,2022,Figure,All In Regular,,,2023,@doulaalia
Jelita,2022,Figure,All In Regular,,,2022,@jelitaj
Ranty Maria,2022,Figure,Video Editor,,,,@rantymaria
Michin Family,2022,Figure,Video Editor,Videographer,,,@michinfamily
Nanda Arsyinta,2022,Figure,All In Regular,,,2023,@nandaarsyinta
PPI UK,2023,Community,Short Video,,,,
Harrington Official Store,2023,Corporate,Commercial Video Production,,,,
Modernvet,2023,Corporate,Company Profile,,,,
Teh AI,2023,Corporate,Commercial Video Production,,,,
OFFO Living,2023,Corporate,Short Video,,,,
BPI Kemdikbud RI,2023,Government,Short Video,,,,
Brantas Abipraya,2023,Government,Event Documentation,,,,
Ikatan Ibu Brantas Abipraya,2023,Community,Event Documentation,,,,
Yayasan Jantung Indonesia,2023,Corporate,Custom Video Production,,,,
FSLDK Jadebek,2023,Community,Video Editor,,,,
Nafkah Community,2023,Community,All In Regular,,,2024,
Safia Natural,2023,Corporate,Event Documentation,,,,
Dr. Yuliani Chandranata,2023,Figure,All In Regular,,,2023,@dryuliani
Broto Laras Family,2023,Figure,Custom Video Production,,,,@brotolaras
Sarah Tumiwa,2023,Figure,All In Regular,,,2023,@sarahtumiwa
Sabrina Anggraini,2023,Figure,Video Editor,,,,@sabrinaanggraini
Jefan Nathanio,2023,Figure,All In Regular,,,2024,@jefannathanio
Handika Pratama,2023,Figure,Video Editor,Videographer,,,@handikapratama
Zhafira Aqyla,2023,Figure,Event Documentation,Video Editor,,,@zhafiraaqyla
DJ Freya,2023,Figure,All In Regular,,,2024,@djfreya
Agatha Chelsea,2023,Figure,Video Editor,,,,@agathachelsea
Luthfi Aulia,2023,Figure,Creative Writer,,,,@luthfiaulia
Sabrina Najwa Aulia,2024,Figure,Video Editor,,,,@sabrinanajwa
Rahmad Junaidi,2024,Figure,All In Regular,,,2024,@rahmadjunaidi
Bang Ghozi,2024,Figure,All In Regular,,,2026,@bangghozi
PTQ Griya Quran,2024,Corporate,Company Profile,Event Documentation,,
Konservasi Indonesia,2024,Corporate,Event Documentation,,,,
KKP RI,2024,Government,Event Documentation,,,,
USAID,2024,Government,Event Documentation,,,,
WWF Indonesia,2024,Government,Event Documentation,,,,
Investabook,2024,Government,All In Regular,,,2024,
Lingkar Keluarga Matahati,2024,Corporate,Custom Video Production,,,,
Kurita Indonesia,2024,Corporate,Video Editor,,,,
RSUD ASA Depok,2024,SOE,Company Profile,,,,
Singing Engineers,2024,Community,Event Documentation,,,,
Dancing Engineers,2024,Community,Event Documentation,,,,
Youth Talent Alliance,2024,Community,Video Editor,,,,
Klinik Soragan 100 C,2024,Corporate,Video Editor,,,,
Coway,2024,Corporate,Commercial Video Production,,,,
SMP Muhammadiyah 2,2024,Corporate,Photographer,,,,
Gag Nikel,2024,SOE,Company Profile,Short Film,Photographer,
Yayasan Muda Cemerlang,2025,Corporate,Workshop,,,,
International Madani Association,2025,Community,Video Editor,,,,"""
    return template_data

# Fungsi untuk mencari klien serupa
def find_similar_clients(target_client, df, top_n=5):
    """Mencari klien dengan profil serupa berdasarkan berbagai faktor"""
    if target_client not in df['Name'].values:
        return None
    
    target_row = df[df['Name'] == target_client].iloc[0]
    similarities = []
    
    for idx, row in df.iterrows():
        if row['Name'] == target_client:
            continue
            
        similarity_score = 0
        
        # 1. Kesamaan Tipe Klien (bobot: 30%)
        if row['Type'] == target_row['Type']:
            similarity_score += 30
        
        # 2. Kedekatan Tahun (bobot: 20%)
        year_diff = abs(row['Year'] - target_row['Year'])
        if year_diff == 0:
            similarity_score += 20
        elif year_diff <= 1:
            similarity_score += 15
        elif year_diff <= 2:
            similarity_score += 10
        elif year_diff <= 3:
            similarity_score += 5
        
        # 3. Kesamaan Layanan (bobot: 30%)
        target_services = set(target_row['Services'])
        row_services = set(row['Services'])
        
        if target_services and row_services:
            # Jaccard similarity untuk layanan
            intersection = len(target_services.intersection(row_services))
            union = len(target_services.union(row_services))
            if union > 0:
                jaccard_similarity = intersection / union
                similarity_score += jaccard_similarity * 30
        
        # 4. Kesamaan Status Loyalitas (bobot: 15%)
        if row['Is_Loyal'] == target_row['Is_Loyal']:
            similarity_score += 15
        
        # 5. Kesamaan Jumlah Layanan (bobot: 5%)
        service_count_diff = abs(row['Service_Count'] - target_row['Service_Count'])
        if service_count_diff == 0:
            similarity_score += 5
        elif service_count_diff <= 1:
            similarity_score += 3
        
        similarities.append({
            'Name': row['Name'],
            'Similarity_Score': similarity_score,
            'Type': row['Type'],
            'Year': row['Year'],
            'Services': row['Services'],
            'Is_Loyal': row['Is_Loyal'],
            'Instagram': row.get('Instagram', ''),
            'Service_Count': row['Service_Count']
        })
    
    similarities_df = pd.DataFrame(similarities)
    return similarities_df.nlargest(top_n, 'Similarity_Score')

# Fungsi untuk login Instagram yang dioptimasi
def instagram_login_optimized(username, password):
    try:
        cl = Client()
        cl.set_user_agent("Instagram 219.0.0.12.117 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US)")
        cl.delay_range = [1, 2]
        cl.login(username, password)
        
        if cl.user_id:
            return cl, True
        else:
            return None, False
            
    except LoginRequired:
        st.error("❌ Login gagal: Username atau password salah")
        return None, False
    except PleaseWaitFewMinutes:
        st.error("⏰ Instagram meminta untuk menunggu. Coba lagi dalam 5-10 menit.")
        return None, False
    except Exception as e:
        error_msg = str(e).lower()
        if "challenge" in error_msg:
            st.error("🔐 Instagram memerlukan verifikasi tambahan. Silakan login melalui aplikasi Instagram terlebih dahulu.")
        elif "rate limit" in error_msg:
            st.error("⚠️ Terlalu banyak percobaan login. Tunggu 10-15 menit sebelum mencoba lagi.")
        else:
            st.error(f"❌ Login gagal: {str(e)}")
        return None, False

# Fungsi untuk mencari pengguna Instagram
def search_instagram_users_optimized(cl, query, max_results=50):
    try:
        time.sleep(1)
        users = cl.search_users(query)
        return users[:max_results] if users else []
    except Exception as e:
        st.error(f"❌ Pencarian gagal: {str(e)}")
        return []

# Fungsi untuk mencari posts berdasarkan hashtag
def search_posts_by_hashtag(cl, hashtag, max_posts=30):
    """Mencari posts berdasarkan hashtag"""
    try:
        time.sleep(random.uniform(1, 2))
        hashtag = hashtag.replace('#', '')
        medias = cl.hashtag_medias_recent(hashtag, amount=max_posts)
        return medias
    except Exception as e:
        return []

# Fungsi untuk mendapatkan detail pengguna
def get_user_details_optimized(cl, user_id):
    try:
        time.sleep(random.uniform(0.5, 1.5))
        user_details = cl.user_info(user_id)
        return user_details
    except Exception:
        return None

# Fungsi untuk mendeteksi lokasi Indonesia (dengan fokus Jabodetabek)
def is_indonesian_user(user_details):
    if not user_details:
        return False, ""
    
    bio = (getattr(user_details, 'biography', '') or "").lower()
    username = getattr(user_details, 'username', '').lower()
    full_name = (getattr(user_details, 'full_name', '') or "").lower()
    
    # Prioritas Jabodetabek
    jabodetabek_keywords = [
        'jakarta', 'depok', 'bogor', 'tangerang', 'bekasi', 'jkt', 'jkarta',
        'jaksel', 'jakbar', 'jaktim', 'jakut', 'jakpus', 'south jakarta',
        'west jakarta', 'east jakarta', 'north jakarta', 'central jakarta',
        'tangsel', 'tangerang selatan', 'bintaro', 'serpong', 'bsd',
        'cibubur', 'cileungsi', 'sentul', 'cikarang', 'karawang'
    ]
    
    # Indonesia umum
    indonesia_keywords = [
        'indonesia', 'surabaya', 'bandung', 'medan', 'semarang', 'palembang',
        'makassar', 'yogyakarta', 'yogya', 'jogja', 'malang', 'solo', 'bali',
        'denpasar', 'balikpapan', 'pontianak', 'manado', 'pekanbaru',
        'banjarmasin', 'samarinda', 'jambi', 'padang', 'aceh', 'lampung',
        'riau', 'sumatra', 'kalimantan', 'sulawesi', 'papua', 'jawa',
        'nusantara', 'batam', 'cirebon', 'tasikmalaya', 'serang', 'cilegon',
        'sukabumi', 'garut', 'purwokerto', 'tegal', 'pekalongan', 'magelang',
        'klaten', 'sukoharjo', 'id', 'idn', 'ina'
    ]
    
    text_to_check = f"{bio} {username} {full_name}"
    
    # Cek Jabodetabek dulu (prioritas tinggi)
    for keyword in jabodetabek_keywords:
        if keyword in text_to_check:
            return True, "Jabodetabek"
    
    # Cek Indonesia umum
    for keyword in indonesia_keywords:
        if keyword in text_to_check:
            return True, "Indonesia"
    
    return False, ""

# Fungsi untuk mendeteksi kebutuhan video/foto
def detect_video_photo_needs(user_details):
    if not user_details:
        return [], 0
    
    bio = (getattr(user_details, 'biography', '') or "").lower()
    username = getattr(user_details, 'username', '').lower()
    full_name = (getattr(user_details, 'full_name', '') or "").lower()
    
    # Kata kunci yang menunjukkan kebutuhan layanan Parthaistic
    need_keywords = {
        'video_production': [
            'videographer', 'videografi', 'video', 'cinematic', 'filmmaker',
            'video production', 'video content', 'video marketing', 'video promosi',
            'video company profile', 'video dokumentasi', 'video event',
            'video wedding', 'video prewedding', 'video commercial', 'video iklan'
        ],
        'photography': [
            'photographer', 'photography', 'fotografer', 'fotografi', 'foto',
            'photo', 'photoshoot', 'foto produk', 'foto wedding', 'foto prewedding',
            'foto maternity', 'foto family', 'foto corporate', 'foto headshot',
            'foto profile', 'foto event', 'foto dokumentasi', 'foto commercial'
        ],
        'content_creation': [
            'content creator', 'konten kreator', 'content', 'konten',
            'social media', 'instagram content', 'tiktok content', 'youtube',
            'digital marketing', 'social media marketing', 'brand content',
            'creative content', 'konten kreatif'
        ],
        'business_needs': [
            'entrepreneur', 'business', 'bisnis', 'startup', 'company',
            'perusahaan', 'brand', 'marketing', 'promosi', 'iklan',
            'company profile', 'profil perusahaan', 'corporate',
            'business owner', 'ceo', 'founder', 'director'
        ],
        'event_wedding': [
            'wedding', 'pernikahan', 'nikah', 'prewedding', 'engagement',
            'event organizer', 'eo', 'wedding organizer', 'wo',
            'event planner', 'wedding planner', 'bride', 'groom'
        ]
    }
    
    detected_needs = []
    confidence_score = 0
    
    text_to_check = f"{bio} {username} {full_name}"
    
    for category, keywords in need_keywords.items():
        category_matches = sum(1 for keyword in keywords if keyword in text_to_check)
        if category_matches > 0:
            detected_needs.append(category.replace('_', ' ').title())
            confidence_score += category_matches * 15
    
    # Boost untuk kata kunci prioritas tinggi
    high_priority_keywords = [
        'videographer', 'photographer', 'content creator', 'wedding',
        'business', 'entrepreneur', 'startup', 'company profile',
        'event organizer', 'marketing'
    ]
    
    for keyword in high_priority_keywords:
        if keyword in text_to_check:
            confidence_score += 20
    
    return detected_needs, min(confidence_score, 100)

# Fungsi untuk menghitung skor potensi klien
def calculate_client_potential_score(user_details, needs, need_confidence, follower_count, location_type):
    base_score = 0

    # Skor berdasarkan followers
    if follower_count >= 100000:
        base_score += 35
    elif follower_count >= 50000:
        base_score += 30
    elif follower_count >= 10000:
        base_score += 25
    elif follower_count >= 5000:
        base_score += 20
    elif follower_count >= 1000:
        base_score += 15
    else:
        return 0  # Tidak memenuhi kriteria minimal

    # Bonus lokasi Jabodetabek
    if location_type == "Jabodetabek":
        base_score += 20
    elif location_type == "Indonesia":
        base_score += 10

    # Skor berdasarkan kebutuhan video/foto
    base_score += min(need_confidence * 0.3, 30)

    # Skor berdasarkan jenis akun
    if getattr(user_details, 'is_business', False):
        base_score += 10
    if getattr(user_details, 'is_verified', False):
        base_score += 5

    # Skor berdasarkan bio yang lengkap
    bio = getattr(user_details, 'biography', '') or ""
    if len(bio) > 50:
        base_score += 5

    return min(int(base_score), 100)

# Fungsi pencarian komprehensif
def comprehensive_client_search(cl, target_count=20):
    """Pencarian komprehensif untuk mendapatkan banyak calon klien Indonesia"""
    all_results = []
    
    # Daftar kata kunci pencarian yang efektif
    search_queries = [
        # Profesi/bidang
        'photographer', 'videographer', 'content creator', 'wedding organizer',
        'event organizer', 'entrepreneur', 'business owner', 'startup founder',
        'marketing manager', 'brand owner', 'food blogger', 'travel blogger',
        'fashion blogger', 'beauty blogger', 'lifestyle blogger',
        
        # Lokasi + profesi
        'jakarta photographer', 'jakarta videographer', 'depok content',
        'bogor wedding', 'tangerang business', 'bekasi entrepreneur',
        
        # Hashtag populer (tanpa #)
        'jakartaphotographer', 'jakartavideographer', 'contentcreatorjakarta',
        'weddingjakarta', 'fotograferjakarta', 'videograferjakarta',
        'businessjakarta', 'startupjakarta', 'eventorganizer',
        
        # Nama umum Indonesia
        'sari', 'dewi', 'putri', 'indra', 'andi', 'budi', 'dian', 'rina'
    ]
    
    # Hashtag untuk pencarian posts
    hashtags_to_search = [
        'butuhvideographer', 'cariphotographer', 'videowedding',
        'contentcreator', 'jakartaphotographer', 'fotograferjakarta',
        'videograferjakarta', 'weddingorganizer', 'eventorganizer',
        'businessowner', 'entrepreneur', 'startup'
    ]
    
    processed_users = set()
    
    try:
        # 1. Pencarian berdasarkan username/profil
        for i, query in enumerate(search_queries):
            if len(all_results) >= target_count:
                break
                
            try:
                users = search_instagram_users_optimized(cl, query, 30)
                
                for user in users:
                    if len(all_results) >= target_count:
                        break
                    
                    user_id = getattr(user, 'pk', None) or getattr(user, 'id', None)
                    if user_id and user_id not in processed_users:
                        processed_users.add(user_id)
                        
                        user_details = get_user_details_optimized(cl, user_id)
                        if user_details:
                            follower_count = getattr(user_details, 'follower_count', 0)
                            is_indonesian, location_type = is_indonesian_user(user_details)
                            
                            if follower_count >= 1000 and is_indonesian:
                                needs, need_confidence = detect_video_photo_needs(user_details)
                                potential_score = calculate_client_potential_score(
                                    user_details, needs, need_confidence, follower_count, location_type
                                )
                                
                                if potential_score >= 15:
                                    all_results.append({
                                        'username': getattr(user_details, 'username', 'N/A'),
                                        'full_name': getattr(user_details, 'full_name', 'N/A'),
                                        'follower_count': follower_count,
                                        'biography': getattr(user_details, 'biography', ''),
                                        'needs': needs,
                                        'need_confidence': need_confidence,
                                        'potential_score': potential_score,
                                        'is_verified': getattr(user_details, 'is_verified', False),
                                        'is_business': getattr(user_details, 'is_business', False),
                                        'location_type': location_type,
                                        'search_method': f'Profile: {query}'
                                    })
                
                time.sleep(random.uniform(2, 3))
                
            except Exception:
                continue
        
        # 2. Pencarian berdasarkan hashtag posts (jika belum cukup)
        if len(all_results) < target_count:
            for hashtag in hashtags_to_search:
                if len(all_results) >= target_count:
                    break
                
                try:
                    posts = search_posts_by_hashtag(cl, hashtag, 20)
                    
                    for post in posts:
                        if len(all_results) >= target_count:
                            break
                        
                        user_id = None
                        if hasattr(post, 'user'):
                            if hasattr(post.user, 'pk'):
                                user_id = post.user.pk
                            elif hasattr(post.user, 'id'):
                                user_id = post.user.id
                        
                        if user_id and user_id not in processed_users:
                            processed_users.add(user_id)
                            
                            user_details = get_user_details_optimized(cl, user_id)
                            if user_details:
                                follower_count = getattr(user_details, 'follower_count', 0)
                                is_indonesian, location_type = is_indonesian_user(user_details)
                                
                                if follower_count >= 1000 and is_indonesian:
                                    needs, need_confidence = detect_video_photo_needs(user_details)
                                    potential_score = calculate_client_potential_score(
                                        user_details, needs, need_confidence, follower_count, location_type
                                    )
                                    
                                    if potential_score >= 15:
                                        all_results.append({
                                            'username': getattr(user_details, 'username', 'N/A'),
                                            'full_name': getattr(user_details, 'full_name', 'N/A'),
                                            'follower_count': follower_count,
                                            'biography': getattr(user_details, 'biography', ''),
                                            'needs': needs,
                                            'need_confidence': need_confidence,
                                            'potential_score': potential_score,
                                            'is_verified': getattr(user_details, 'is_verified', False),
                                            'is_business': getattr(user_details, 'is_business', False),
                                            'location_type': location_type,
                                            'search_method': f'Hashtag: #{hashtag}'
                                        })
                    
                    time.sleep(random.uniform(3, 4))
                    
                except Exception:
                    continue
    
    except Exception as e:
        st.error(f"Error dalam pencarian: {str(e)}")
    
    return all_results

# Inisialisasi session state
if 'instagram_logged_in' not in st.session_state:
    st.session_state.instagram_logged_in = False
if 'instagram_client' not in st.session_state:
    st.session_state.instagram_client = None
if 'instagram_username' not in st.session_state:
    st.session_state.instagram_username = ""
if 'comprehensive_results' not in st.session_state:
    st.session_state.comprehensive_results = []

# Sidebar login Instagram
with st.sidebar:
    st.header("🔐 Login Instagram")
    
    if not st.session_state.instagram_logged_in:
        st.info("💡 **Tips Login:**\n- Pastikan koneksi internet stabil\n- Gunakan username/email yang benar\n- Jika gagal, tunggu 5-10 menit")
        
        insta_username = st.text_input("Username/Email Instagram")
        insta_password = st.text_input("Password Instagram", type="password")
        
        if st.button("🚀 Login Instagram", type="primary"):
            if insta_username and insta_password:
                with st.spinner("Sedang login ke Instagram..."):
                    client, success = instagram_login_optimized(insta_username, insta_password)
                    if success:
                        st.session_state.instagram_logged_in = True
                        st.session_state.instagram_client = client
                        st.session_state.instagram_username = insta_username
                        st.success("✅ Berhasil login ke Instagram!")
                        st.rerun()
            else:
                st.warning("⚠️ Harap masukkan username dan password Instagram")
    else:
        st.success(f"✅ Logged in as: @{st.session_state.instagram_username}")
        if st.button("🚪 Logout Instagram"):
            st.session_state.instagram_logged_in = False
            st.session_state.instagram_client = None
            st.session_state.instagram_username = ""
            st.session_state.comprehensive_results = []
            st.rerun()

# Header utama
st.markdown('<h1 class="main-header">🎬 Dasbor Analisis Klien Parthaistic</h1>', unsafe_allow_html=True)

# Load data existing clients
@st.cache_data
def load_and_process_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Data CSV berhasil dimuat!")
        except Exception as e:
            st.error(f"❌ Error membaca file CSV: {e}")
            return None
    else:
        # Data default - menggunakan data lengkap
        data = create_complete_csv_template()
        df = pd.read_csv(StringIO(data))
        st.info("📄 Menggunakan data default. Upload file CSV untuk menggunakan data Anda sendiri.")
    
    # Proses data
    df['Regular End Period'] = pd.to_numeric(df['Regular End Period'], errors='coerce')
    
    services = []
    service_columns = [col for col in df.columns if col.startswith('Service')]
    
    for _, row in df.iterrows():
        client_services = []
        for col in service_columns:
            if pd.notna(row[col]) and str(row[col]).strip():
                client_services.append(str(row[col]).strip())
        services.append(client_services)
    
    df['Services'] = services
    df['Service_Count'] = df['Services'].apply(len)
    df['Is_Loyal'] = df['Regular End Period'].notna()
    df['Loyalty_Duration'] = df['Regular End Period'] - df['Year']
    df['Loyalty_Duration'] = df['Loyalty_Duration'].fillna(0)
    
    return df

# Area upload file dengan template download
st.subheader("📁 Upload Data CSV")

# Section download template
st.markdown("""
<div class="download-section">
    <h4>📋 Template CSV Format</h4>
    <p>Download template CSV lengkap dengan semua data klien Parthaistic untuk melihat format yang benar</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    # Tombol download template CSV lengkap
    template_csv_data = create_complete_csv_template()
    st.download_button(
        label="📥 Download Template CSV Lengkap",
        data=template_csv_data,
        file_name="template_klien_parthaistic_lengkap.csv",
        mime="text/csv",
        help="Download template dengan semua data klien (90+ entries) untuk melihat format yang benar",
        use_container_width=True
    )

with col2:
    # Informasi format
    st.info("""
    **📋 Format Kolom CSV:**
    - **Name**: Nama klien/perusahaan
    - **Year**: Tahun mulai (2020-2025)
    - **Type**: Corporate/Figure/Community/Government/SOE
    - **Service 1-3**: Layanan yang digunakan
    - **Regular End Period**: Tahun berakhir (jika loyal)
    - **Instagram**: Username (@username)
    """)

# Upload file
uploaded_file = st.file_uploader(
    "Pilih file CSV Anda", 
    type=['csv'],
    help="Upload file CSV dengan format sesuai template yang dapat didownload di atas"
)

# Muat data
df = load_and_process_data(uploaded_file)

if df is not None:
    # Tab Dasbor Utama
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Gambaran Umum", 
        "🎯 Profiling Klien", 
        "🔍 Analisis Klien Loyal", 
        "💡 Wawasan Bisnis", 
        "🔎 Pencarian Calon Klien"
    ])

    with tab1:
        st.header("📊 Gambaran Umum Bisnis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(df)}</h3>
                <p>Total Klien</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            loyal_clients = len(df[df['Is_Loyal']])
            st.markdown(f"""
            <div class="metric-card">
                <h3>{loyal_clients}</h3>
                <p>Klien Loyal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            loyalty_rate = (loyal_clients / len(df) * 100) if len(df) > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>{loyalty_rate:.1f}%</h3>
                <p>Tingkat Loyalitas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_services = df['Service_Count'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_services:.1f}</h3>
                <p>Rata-rata Layanan/Klien</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Grafik distribusi klien
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Klien berdasarkan Tahun & Tipe")
            year_type_data = df.groupby(['Year', 'Type']).size().reset_index(name='Count')
            fig = px.bar(year_type_data, x='Year', y='Count', color='Type',
                        title="Distribusi Klien berdasarkan Tahun dan Tipe")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🥧 Distribusi Tipe Klien")
            type_counts = df['Type'].value_counts()
            fig = px.pie(values=type_counts.values, names=type_counts.index,
                        title="Distribusi Tipe Klien")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("🎯 Profiling Klien Tingkat Lanjut")
        
        # Container untuk profiling
        st.markdown('<div class="profiling-section">', unsafe_allow_html=True)
        
        # Bagian pencarian klien serupa
        st.subheader("🔍 Temukan Klien Serupa")
        st.markdown("Pilih klien untuk menemukan profil serupa berdasarkan tipe, layanan, tahun, dan status loyalitas:")
        
        selected_client = st.selectbox(
            "Pilih klien untuk analisis kesamaan:", 
            [""] + sorted(df['Name'].tolist()),
            key="client_similarity_selector"
        )
        
        if selected_client:
            similar_clients = find_similar_clients(selected_client, df, top_n=5)
            
            if similar_clients is not None and len(similar_clients) > 0:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Target client card
                    target_info = df[df['Name'] == selected_client].iloc[0]
                    loyalty_status = "Loyal" if target_info['Is_Loyal'] else "Non-loyal"
                    instagram_handle = target_info.get('Instagram', 'Tidak ada')
                    
                    st.markdown(f"""
                    <div class="target-client-card">
                        <h4>📋 Klien Target</h4>
                        <h3 style="color: #1976d2; margin: 0.5rem 0;">{selected_client}</h3>
                        <div class="client-info-row">
                            <span class="client-info-label">Tipe:</span>
                            <span class="client-info-value">{target_info['Type']}</span>
                        </div>
                        <div class="client-info-row">
                            <span class="client-info-label">Tahun:</span>
                            <span class="client-info-value">{target_info['Year']}</span>
                        </div>
                        <div class="client-info-row">
                            <span class="client-info-label">Status:</span>
                            <span class="client-info-value">{loyalty_status}</span>
                        </div>
                        <div class="client-info-row">
                            <span class="client-info-label">Instagram:</span>
                            <span class="client-info-value">{instagram_handle}</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <span class="client-info-label">Layanan ({target_info['Service_Count']}):</span><br>
                            <span class="client-info-value">{', '.join(target_info['Services'])}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Similar clients
                    st.markdown("### 🤝 Klien Paling Serupa")
                    
                    for idx, client in similar_clients.iterrows():
                        similarity_pct = client['Similarity_Score']
                        loyalty_status = "Loyal" if client['Is_Loyal'] else "Non-loyal"
                        instagram_handle = client.get('Instagram', 'Tidak ada')
                        
                        # Determine similarity level
                        if similarity_pct >= 70:
                            similarity_level = "🔥 Sangat Mirip"
                            card_style = "background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%); border-color: #4caf50;"
                        elif similarity_pct >= 50:
                            similarity_level = "⭐ Cukup Mirip"
                            card_style = "background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-color: #ff9800;"
                        else:
                            similarity_level = "💡 Sedikit Mirip"
                            card_style = "background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-color: #9c27b0;"
                        
                        st.markdown(f"""
                        <div class="similar-client-card" style="{card_style}">
                            <div class="similarity-score">Kesamaan: {similarity_pct:.1f}% - {similarity_level}</div>
                            <h4 style="margin: 0.5rem 0; color: #e65100;">{client['Name']}</h4>
                            <div class="client-info-row">
                                <span class="client-info-label">Tipe:</span>
                                <span class="client-info-value">{client['Type']}</span>
                            </div>
                            <div class="client-info-row">
                                <span class="client-info-label">Tahun:</span>
                                <span class="client-info-value">{client['Year']}</span>
                            </div>
                            <div class="client-info-row">
                                <span class="client-info-label">Status:</span>
                                <span class="client-info-value">{loyalty_status}</span>
                            </div>
                            <div class="client-info-row">
                                <span class="client-info-label">Instagram:</span>
                                <span class="client-info-value">{instagram_handle}</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <span class="client-info-label">Layanan ({client['Service_Count']}):</span><br>
                                <span class="client-info-value">{', '.join(client['Services'])}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analisis layanan populer
        st.subheader("🎬 Analisis Popularitas Layanan")
        all_services = []
        for services_list in df['Services']:
            all_services.extend(services_list)
        
        if all_services:
            service_counts = pd.Series(all_services).value_counts().head(10)
            fig = px.bar(x=service_counts.values, y=service_counts.index, orientation='h',
                        title="10 Layanan Paling Populer")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🔍 Analisis Klien Loyal")
        
        loyal_df = df[df['Is_Loyal']].copy()
        
        if len(loyal_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👑 Karakteristik Klien Loyal")
                loyal_types = loyal_df['Type'].value_counts()
                fig = px.pie(values=loyal_types.values, names=loyal_types.index,
                            title="Klien Loyal berdasarkan Tipe")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🎬 Layanan Populer Klien Loyal")
                loyal_services = []
                for services in loyal_df['Services']:
                    loyal_services.extend(services)
                
                if loyal_services:
                    loyal_service_counts = pd.Series(loyal_services).value_counts().head(8)
                    fig = px.bar(x=loyal_service_counts.values, y=loyal_service_counts.index, 
                                orientation='h', title="Layanan Teratas di Kalangan Klien Loyal")
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tidak ada klien loyal yang ditemukan.")

    with tab4:
        st.header("💡 Wawasan Bisnis")
        
        # Generate insights
        insights = []
        
        # Analisis tren pertumbuhan
        yearly_growth = df.groupby('Year').size()
        if len(yearly_growth) > 1:
            latest_growth = yearly_growth.iloc[-1] - yearly_growth.iloc[-2]
            growth_rate = (latest_growth / yearly_growth.iloc[-2]) * 100 if yearly_growth.iloc[-2] > 0 else 0
            insights.append(f"📈 **Tren Pertumbuhan**: Pertumbuhan klien {growth_rate:+.1f}% dari {yearly_growth.index[-2]} ke {yearly_growth.index[-1]}")
        
        # Wawasan loyalitas
        if len(df[df['Is_Loyal']]) > 0:
            loyalty_rate = len(df[df['Is_Loyal']]) / len(df) * 100
            insights.append(f"👑 **Tingkat Loyalitas**: {loyalty_rate:.1f}% klien menjadi pelanggan setia")
        
        # Layanan paling populer
        if all_services:
            most_popular_service = pd.Series(all_services).value_counts().index[0]
            insights.append(f"🌟 **Layanan Paling Populer**: {most_popular_service} adalah layanan yang paling banyak diminta")
        
        # Tampilkan wawasan
        for insight in insights:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

    with tab5:
        st.header("🔎 Pencarian Calon Klien Indonesia")
        
        if st.session_state.instagram_logged_in:
            st.markdown("""
            <div class="unified-search-card">
                <h4>🎯 Pencarian Komprehensif Calon Klien</h4>
                <p>Sistem akan mencari calon klien secara otomatis menggunakan berbagai metode untuk mendapatkan minimal 20 rekomendasi klien potensial dari Indonesia, terutama Jabodetabek.</p>
                <p><strong>Metode Pencarian Otomatis:</strong></p>
                <ul>
                    <li>✅ Pencarian berdasarkan profesi (photographer, videographer, content creator, dll)</li>
                    <li>✅ Pencarian berdasarkan lokasi + profesi (Jakarta photographer, Depok content, dll)</li>
                    <li>✅ Pencarian berdasarkan hashtag populer (#jakartaphotographer, #contentcreatorjakarta, dll)</li>
                    <li>✅ Pencarian berdasarkan nama umum Indonesia</li>
                    <li>✅ Analisis posts dengan hashtag relevan</li>
                </ul>
                <p><strong>Filter Otomatis:</strong> Minimal 1000 followers, berlokasi Indonesia (prioritas Jabodetabek), menunjukkan kebutuhan video/foto</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Pengaturan pencarian
            col1, col2 = st.columns([2, 1])
            
            with col1:
                target_results = st.number_input(
                    "🎯 Target Jumlah Hasil:", 
                    min_value=20, 
                    max_value=50, 
                    value=25, 
                    step=5,
                    help="Jumlah calon klien yang ingin ditemukan (minimal 20)"
                )
            
            with col2:
                st.markdown("**🏆 Prioritas Lokasi:**")
                st.info("1. Jabodetabek (+20 poin)\n2. Indonesia lainnya (+10 poin)")
            
            # Tombol pencarian utama
            if st.button("🚀 Mulai Pencarian Komprehensif", type="primary", use_container_width=True):
                with st.spinner(f"Mencari {target_results} calon klien Indonesia..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Memulai pencarian komprehensif...")
                    progress_bar.progress(0.1)
                    
                    # Jalankan pencarian komprehensif
                    results = comprehensive_client_search(st.session_state.instagram_client, target_results)
                    
                    progress_bar.progress(1.0)
                    status_text.text(f"✅ Pencarian selesai! Ditemukan {len(results)} calon klien")
                    
                    st.session_state.comprehensive_results = results
            
            # Tampilkan hasil pencarian
            if st.session_state.comprehensive_results:
                st.subheader("📊 Hasil Pencarian Komprehensif")
                
                # Urutkan berdasarkan skor potensi
                sorted_results = sorted(st.session_state.comprehensive_results, 
                                      key=lambda x: x['potential_score'], reverse=True)
                
                # Statistik singkat
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Ditemukan", len(sorted_results))
                with col2:
                    high_potential = sum(1 for r in sorted_results if r['potential_score'] >= 60)
                    st.metric("Potensi Tinggi", high_potential)
                with col3:
                    jabodetabek_count = sum(1 for r in sorted_results if r['location_type'] == 'Jabodetabek')
                    st.metric("Jabodetabek", jabodetabek_count)
                with col4:
                    avg_followers = sum(r['follower_count'] for r in sorted_results) // len(sorted_results)
                    st.metric("Rata-rata Followers", f"{avg_followers:,}")
                
                # Analisis lokasi
                location_stats = {}
                for result in sorted_results:
                    loc = result['location_type']
                    location_stats[loc] = location_stats.get(loc, 0) + 1
                
                if location_stats:
                    st.subheader("📍 Distribusi Lokasi")
                    col_loc1, col_loc2 = st.columns(2)
                    
                    with col_loc1:
                        for loc, count in location_stats.items():
                            percentage = (count / len(sorted_results)) * 100
                            if loc == "Jabodetabek":
                                st.success(f"🏆 {loc}: {count} klien ({percentage:.1f}%)")
                            else:
                                st.info(f"📍 {loc}: {count} klien ({percentage:.1f}%)")
                    
                    with col_loc2:
                        fig = px.pie(
                            values=list(location_stats.values()), 
                            names=list(location_stats.keys()),
                            title="Distribusi Lokasi Calon Klien"
                        )
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Tampilkan hasil detail
                st.subheader("👥 Daftar Calon Klien")
                
                for i, client in enumerate(sorted_results):
                    verified_badge = "✅" if client['is_verified'] else ""
                    business_badge = "🏢" if client['is_business'] else ""
                    
                    # Tentukan warna skor dan lokasi
                    if client['potential_score'] >= 60:
                        score_class = "score-high"
                        priority = "🔥 PRIORITAS TINGGI"
                    elif client['potential_score'] >= 40:
                        score_class = "score-medium"
                        priority = "⭐ POTENSI BAIK"
                    else:
                        score_class = "score-low"
                        priority = "💡 MONITOR"
                    
                    location_badge = "🏆 Jabodetabek" if client['location_type'] == "Jabodetabek" else "📍 Indonesia"
                    
                    with st.expander(f"{i+1}. @{client['username']} {verified_badge}{business_badge} - Skor: {client['potential_score']}/100", 
                                   expanded=i < 5):
                        
                        col_info1, col_info2 = st.columns([3, 1])
                        
                        with col_info1:
                            st.markdown(f"**👤 Nama:** {client['full_name']}")
                            st.markdown(f"**📊 Followers:** {client['follower_count']:,}")
                            st.markdown(f'<span class="location-indicator">{location_badge}</span>', unsafe_allow_html=True)
                            
                            if client['biography']:
                                st.markdown(f"**📝 Bio:** {client['biography']}")
                            
                            if client['needs']:
                                st.markdown("**🎯 Kebutuhan Terdeteksi:**")
                                for need in client['needs']:
                                    st.markdown(f'<span class="need-indicator">{need}</span>', unsafe_allow_html=True)
                                st.markdown(f"**Confidence Level:** {client['need_confidence']}/100")
                            
                            st.markdown(f"**🔍 Ditemukan via:** {client['search_method']}")
                        
                        with col_info2:
                            st.markdown(f"[📱 Lihat Profil](https://instagram.com/{client['username']})")
                            st.markdown(f'<p class="{score_class}">Skor: {client["potential_score"]}/100</p>', 
                                      unsafe_allow_html=True)
                            
                            if client['potential_score'] >= 60:
                                st.success("🔥 PRIORITAS TINGGI")
                            elif client['potential_score'] >= 40:
                                st.warning("⭐ POTENSI BAIK")
                            else:
                                st.info("💡 MONITOR")
                
                # Export hasil
                if st.button("📥 Download Semua Hasil (CSV)", use_container_width=True):
                    export_df = pd.DataFrame([
                        {
                            'Username': r['username'],
                            'Full Name': r['full_name'],
                            'Followers': r['follower_count'],
                            'Location Type': r['location_type'],
                            'Biography': r['biography'],
                            'Needs': ', '.join(r['needs']),
                            'Need Confidence': r['need_confidence'],
                            'Potential Score': r['potential_score'],
                            'Verified': r['is_verified'],
                            'Business Account': r['is_business'],
                            'Search Method': r['search_method'],
                            'Instagram Link': f"https://instagram.com/{r['username']}"
                        }
                        for r in sorted_results
                    ])
                    
                    csv_data = export_df.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=f"calon_klien_indonesia_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
            
            else:
                st.info("""
                **🎯 Pencarian Komprehensif Calon Klien Indonesia**
                
                ### 🚀 **Fitur Unggulan:**
                - ✅ **Pencarian Otomatis**: Sistem akan mencari menggunakan berbagai metode secara otomatis
                - ✅ **Fokus Indonesia**: Prioritas Jabodetabek, kemudian Indonesia lainnya
                - ✅ **Target Minimal 20**: Mendapatkan banyak rekomendasi sekaligus
                - ✅ **Multi-Method Search**: Kombinasi pencarian profil, hashtag, dan posts
                - ✅ **Smart Filtering**: Otomatis filter berdasarkan followers dan lokasi
                
                ### 🎯 **Kriteria Pencarian:**
                - **Followers**: Minimal 1000 followers
                - **Lokasi**: Indonesia (prioritas Jabodetabek)
                - **Kebutuhan**: Menunjukkan kebutuhan video/foto/content
                - **Aktif**: Akun yang aktif dan relevan
                
                ### 📍 **Prioritas Lokasi:**
                - **🏆 Jabodetabek** (+20 poin): Jakarta, Depok, Bogor, Tangerang, Bekasi
                - **📍 Indonesia Lainnya** (+10 poin): Kota-kota besar lainnya
                
                ### 🔍 **Metode Pencarian Otomatis:**
                1. **Pencarian Profesi**: photographer, videographer, content creator, entrepreneur
                2. **Lokasi + Profesi**: jakarta photographer, depok content, dll
                3. **Hashtag Populer**: #jakartaphotographer, #contentcreatorjakarta
                4. **Nama Indonesia**: Sari, Dewi, Budi, Andi, dll
                5. **Analisis Posts**: Hashtag #butuhvideographer, #cariphotographer
                
                **Klik tombol "Mulai Pencarian Komprehensif" untuk mendapatkan banyak rekomendasi klien sekaligus!**
                """)
        
        else:
            st.warning("⚠️ Login Instagram diperlukan untuk menggunakan fitur pencarian calon klien")
            st.info("Silakan login Instagram di sidebar untuk mengakses fitur ini")

else:
    st.warning("⚠️ Tidak dapat memuat data. Periksa file CSV Anda.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎬 Dasbor Analisis Klien Parthaistic | Comprehensive Indonesia Client Search</p>
    
</div>
""", unsafe_allow_html=True)
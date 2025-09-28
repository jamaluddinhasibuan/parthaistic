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
    .post-search-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 1.5rem;
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
def search_instagram_users_optimized(cl, query, max_results=30):
    try:
        time.sleep(1)
        users = cl.search_users(query)
        return users[:max_results] if users else []
    except Exception as e:
        st.error(f"❌ Pencarian gagal: {str(e)}")
        return []

# Fungsi untuk mendapatkan detail pengguna
def get_user_details_optimized(cl, user_id):
    try:
        time.sleep(random.uniform(0.5, 1.5))
        user_details = cl.user_info(user_id)
        return user_details
    except Exception:
        return None

# Fungsi untuk mendapatkan posts berdasarkan hashtag
def search_posts_by_hashtag(cl, hashtag, max_posts=50):
    """Mencari posts berdasarkan hashtag"""
    try:
        time.sleep(random.uniform(1, 2))
        # Hapus # jika ada
        hashtag = hashtag.replace('#', '')
        medias = cl.hashtag_medias_recent(hashtag, amount=max_posts)
        return medias
    except Exception as e:
        st.error(f"❌ Error mencari hashtag #{hashtag}: {str(e)}")
        return []

# Fungsi untuk mendapatkan posts dari user
def get_user_posts(cl, user_id, max_posts=20):
    """Mendapatkan posts terbaru dari user"""
    try:
        time.sleep(random.uniform(1, 2))
        medias = cl.user_medias(user_id, amount=max_posts)
        return medias
    except Exception:
        return []

# Fungsi untuk menganalisis konten post
def analyze_post_content(post):
    """Menganalisis konten post untuk mendeteksi kebutuhan video/foto"""
    caption = getattr(post, 'caption_text', '') or ""
    caption = caption.lower()
    
    # Kata kunci yang menunjukkan kebutuhan layanan
    service_keywords = {
        'video_production': [
            'butuh video', 'cari videographer', 'need video', 'video content',
            'video marketing', 'video promosi', 'video company profile',
            'video dokumentasi', 'video event', 'video wedding', 'video prewedding',
            'video commercial', 'video iklan', 'video product', 'cinematic video',
            'video shoot', 'video production', 'videografi'
        ],
        'photography': [
            'butuh foto', 'cari photographer', 'need photo', 'foto produk',
            'foto wedding', 'foto prewedding', 'foto maternity', 'foto family',
            'foto corporate', 'foto headshot', 'foto profile', 'foto event',
            'foto dokumentasi', 'foto commercial', 'photoshoot', 'photography',
            'fotografer', 'potret'
        ],
        'content_creation': [
            'content creator', 'konten kreator', 'social media content',
            'instagram content', 'tiktok content', 'youtube content',
            'digital marketing', 'social media marketing', 'brand content',
            'creative content', 'konten kreatif'
        ],
        'business_needs': [
            'company profile', 'profil perusahaan', 'corporate video',
            'business video', 'promotional video', 'marketing material',
            'brand awareness', 'product launch', 'event coverage',
            'launching produk', 'promosi bisnis'
        ]
    }
    
    detected_needs = []
    confidence_score = 0
    
    for category, keywords in service_keywords.items():
        category_matches = sum(1 for keyword in keywords if keyword in caption)
        if category_matches > 0:
            detected_needs.append(category.replace('_', ' ').title())
            confidence_score += category_matches * 10
    
    # Ekstrak hashtags
    hashtags = re.findall(r'#\w+', caption)
    
    # Analisis hashtags untuk kebutuhan layanan
    relevant_hashtags = []
    hashtag_keywords = [
        'video', 'foto', 'photography', 'videography', 'content', 'marketing',
        'wedding', 'prewedding', 'event', 'corporate', 'business', 'produk',
        'commercial', 'cinematic', 'photoshoot', 'videoshoot'
    ]
    
    for hashtag in hashtags:
        hashtag_clean = hashtag.lower().replace('#', '')
        if any(keyword in hashtag_clean for keyword in hashtag_keywords):
            relevant_hashtags.append(hashtag)
            confidence_score += 5
    
    return {
        'needs': detected_needs,
        'confidence': min(confidence_score, 100),
        'hashtags': hashtags,
        'relevant_hashtags': relevant_hashtags,
        'caption_excerpt': caption[:200] + "..." if len(caption) > 200 else caption
    }

# Fungsi untuk mendeteksi lokasi Indonesia
def is_indonesian_user(user_details):
    if not user_details:
        return False
    
    bio = (getattr(user_details, 'biography', '') or "").lower()
    username = getattr(user_details, 'username', '').lower()
    full_name = (getattr(user_details, 'full_name', '') or "").lower()
    
    indonesia_keywords = [
        'indonesia', 'jakarta', 'surabaya', 'bandung', 'medan', 'semarang',
        'palembang', 'makassar', 'depok', 'tangerang', 'bekasi', 'bogor',
        'yogyakarta', 'yogya', 'jogja', 'malang', 'solo', 'bali', 'denpasar',
        'balikpapan', 'pontianak', 'manado', 'pekanbaru', 'banjarmasin',
        'samarinda', 'jambi', 'padang', 'aceh', 'lampung', 'riau', 'sumatra',
        'kalimantan', 'sulawesi', 'papua', 'jawa', 'nusantara', 'batam',
        'cirebon', 'tasikmalaya', 'serang', 'cilegon', 'sukabumi', 'garut',
        'purwokerto', 'tegal', 'pekalongan', 'magelang', 'klaten', 'sukoharjo',
        'id', 'idn', 'ina'
    ]
    
    text_to_check = f"{bio} {username} {full_name}"
    return any(keyword in text_to_check for keyword in indonesia_keywords)

# Fungsi untuk mendeteksi kebutuhan video/foto dari bio
def detect_video_photo_needs(user_details):
    if not user_details:
        return [], 0
    
    bio = (getattr(user_details, 'biography', '') or "").lower()
    username = getattr(user_details, 'username', '').lower()
    full_name = (getattr(user_details, 'full_name', '') or "").lower()
    
    # Kata kunci yang menunjukkan kebutuhan layanan Parthaistic
    need_keywords = {
        'video_production': [
            'butuh video', 'cari videographer', 'need video', 'video content',
            'video marketing', 'video promosi', 'video company profile',
            'video dokumentasi', 'video event', 'video wedding', 'video prewedding',
            'video commercial', 'video iklan', 'video product', 'cinematic video'
        ],
        'photography': [
            'butuh foto', 'cari photographer', 'need photo', 'foto produk',
            'foto wedding', 'foto prewedding', 'foto maternity', 'foto family',
            'foto corporate', 'foto headshot', 'foto profile', 'foto event',
            'foto dokumentasi', 'foto commercial', 'photoshoot'
        ],
        'content_creation': [
            'content creator', 'konten kreator', 'social media content',
            'instagram content', 'tiktok content', 'youtube content',
            'digital marketing', 'social media marketing', 'brand content'
        ],
        'business_needs': [
            'company profile', 'profil perusahaan', 'corporate video',
            'business video', 'promotional video', 'marketing material',
            'brand awareness', 'product launch', 'event coverage'
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
        'butuh video', 'cari videographer', 'butuh foto', 'cari photographer',
        'need video', 'need photo', 'video marketing', 'content creator',
        'company profile', 'video wedding', 'foto wedding'
    ]
    
    for keyword in high_priority_keywords:
        if keyword in text_to_check:
            confidence_score += 25
    
    return detected_needs, min(confidence_score, 100)

# Fungsi untuk menghitung skor potensi klien berdasarkan posts
def calculate_post_based_score(user_details, post_analysis_results, follower_count):
    """Menghitung skor potensi klien berdasarkan analisis posts"""
    base_score = 0

    # Skor berdasarkan followers (minimal 1000 untuk post-based search)
    if follower_count >= 50000:
        base_score += 25
    elif follower_count >= 10000:
        base_score += 20
    elif follower_count >= 5000:
        base_score += 15
    elif follower_count >= 1000:
        base_score += 10
    else:
        return 0  # Tidak memenuhi kriteria minimal

    # Skor berdasarkan analisis posts
    total_confidence = sum(result['confidence'] for result in post_analysis_results)
    avg_confidence = total_confidence / len(post_analysis_results) if post_analysis_results else 0
    base_score += min(avg_confidence * 0.5, 35)

    # Bonus untuk posts dengan hashtags relevan
    relevant_hashtag_count = sum(len(result['relevant_hashtags']) for result in post_analysis_results)
    base_score += min(relevant_hashtag_count * 2, 15)

    # Bonus untuk kebutuhan yang terdeteksi di multiple posts
    all_needs = []
    for result in post_analysis_results:
        all_needs.extend(result['needs'])
    
    unique_needs = len(set(all_needs))
    base_score += min(unique_needs * 5, 15)

    # Skor berdasarkan jenis akun
    if getattr(user_details, 'is_business', False):
        base_score += 10
    if getattr(user_details, 'is_verified', False):
        base_score += 5

    return min(int(base_score), 100)

# Fungsi untuk menghitung skor potensi klien
def calculate_client_potential_score(user_details, needs, need_confidence, follower_count):
    base_score = 0

    # Skor berdasarkan followers (minimal 2000)
    if follower_count >= 50000:
        base_score += 30
    elif follower_count >= 10000:
        base_score += 25
    elif follower_count >= 5000:
        base_score += 20
    elif follower_count >= 2000:
        base_score += 15
    else:
        return 0  # Tidak memenuhi kriteria minimal

    # Skor berdasarkan kebutuhan video/foto
    base_score += min(need_confidence * 0.4, 40)

    # Skor berdasarkan jenis akun
    if getattr(user_details, 'is_business', False):
        base_score += 15
    if getattr(user_details, 'is_verified', False):
        base_score += 10

    # Skor berdasarkan bio yang lengkap
    bio = getattr(user_details, 'biography', '') or ""
    if len(bio) > 50:
        base_score += 10

    return min(int(base_score), 100)

# Inisialisasi session state
if 'instagram_logged_in' not in st.session_state:
    st.session_state.instagram_logged_in = False
if 'instagram_client' not in st.session_state:
    st.session_state.instagram_client = None
if 'instagram_username' not in st.session_state:
    st.session_state.instagram_username = ""
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'post_search_results' not in st.session_state:
    st.session_state.post_search_results = []

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
            st.session_state.search_results = []
            st.session_state.post_search_results = []
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

# Tampilkan contoh format dalam expander
with st.expander("📖 Panduan Format CSV Lengkap", expanded=False):
    st.markdown("""
    ### 🎯 **Kolom yang Diperlukan:**
    
    | Kolom | Deskripsi | Contoh | Wajib? |
    |-------|-----------|---------|---------|
    | **Name** | Nama klien/perusahaan | "PT Contoh Jaya", "Shenina Cinnamon" | ✅ Wajib |
    | **Year** | Tahun mulai kerjasama | 2024, 2023, 2022 | ✅ Wajib |
    | **Type** | Jenis klien | Corporate, Figure, Community, Government, SOE | ✅ Wajib |
    | **Service 1** | Layanan utama | "Video Production", "All In Regular" | ✅ Wajib |
    | **Service 2** | Layanan kedua | "Photography", "Video Editor" | ❌ Opsional |
    | **Service 3** | Layanan ketiga | "Videographer", "Workshop" | ❌ Opsional |
    | **Regular End Period** | Tahun berakhir kontrak | 2025, 2026 (kosong jika tidak loyal) | ❌ Opsional |
    | **Instagram** | Username Instagram | "@rizkyyudo", "@sheninacinnamon" | ❌ Opsional |
    
    ### 🎬 **Contoh Jenis Layanan Parthaistic:**
    - **Video Production**: Custom Video Production, Commercial Video Production, Company Profile
    - **Regular Services**: All In Regular, Video Editor Regular
    - **Specialized**: Event Documentation, E-Learning Video, Short Video, Short Film
    - **Creative**: Project Musikal Pemuda Indonesia, Creative Writer
    - **Photography**: Photographer, Photoshoot
    - **Others**: Workshop, Videographer
    
    ### ✅ **Tips Pengisian:**
    - Gunakan koma (,) sebagai pemisah kolom
    - Kosongkan sel jika tidak ada data (jangan hapus kolom)
    - Format tahun: 2024 (4 digit angka)
    - Username Instagram: @namauser atau kosong
    - Jenis klien harus salah satu: Corporate, Figure, Community, Government, SOE
    
    ### 📊 **Data Statistik Template:**
    - **Total Klien**: 90+ entries
    - **Periode**: 2020-2025
    - **Tipe Klien**: 5 kategori (Corporate, Figure, Community, Government, SOE)
    - **Layanan**: 20+ jenis layanan berbeda
    - **Klien Loyal**: 15+ klien dengan kontrak regular
    """)

# Muat data
df = load_and_process_data(uploaded_file)

if df is not None:
    # Tab Dasbor Utama
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Gambaran Umum", 
        "🎯 Profiling Klien", 
        "🔍 Analisis Klien Loyal", 
        "💡 Wawasan Bisnis", 
        "🔎 Pencarian Profil", 
        "📱 Pencarian Posts & Hashtag"
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
                
                # Insights berdasarkan klien serupa
                st.subheader("💡 Wawasan dari Analisis Kesamaan")
                
                # Analisis pola dari klien serupa
                similar_types = similar_clients['Type'].value_counts()
                similar_services = []
                for services in similar_clients['Services']:
                    similar_services.extend(services)
                
                loyalty_rate_similar = (similar_clients['Is_Loyal'].sum() / len(similar_clients)) * 100
                
                col_insight1, col_insight2 = st.columns(2)
                
                with col_insight1:
                    st.markdown(f"""
                    <div class="insight-box">
                        <h5>📊 Pola Klien Serupa</h5>
                        <p><strong>Tipe Dominan:</strong> {similar_types.index[0] if len(similar_types) > 0 else 'N/A'}</p>
                        <p><strong>Tingkat Loyalitas:</strong> {loyalty_rate_similar:.1f}%</p>
                        <p><strong>Rata-rata Layanan:</strong> {similar_clients['Service_Count'].mean():.1f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_insight2:
                    if similar_services:
                        top_similar_services = pd.Series(similar_services).value_counts().head(3)
                        services_text = "<br>".join([f"• {service} ({count}x)" for service, count in top_similar_services.items()])
                        
                        st.markdown(f"""
                        <div class="insight-box">
                            <h5>🎬 Layanan Populer</h5>
                            {services_text}
                        </div>
                        """, unsafe_allow_html=True)
            
            else:
                st.info("Tidak ditemukan klien yang serupa dengan profil yang dipilih.")
        
        else:
            st.info("""
            **🎯 Cara Menggunakan Analisis Kesamaan Klien:**
            
            1. **Pilih Klien Target** - Pilih dari dropdown klien yang ingin dianalisis
            2. **Lihat Profil Target** - Review karakteristik klien yang dipilih
            3. **Analisis Klien Serupa** - Sistem akan menampilkan 5 klien paling mirip
            4. **Skor Kesamaan** - Berdasarkan tipe, tahun, layanan, dan loyalitas
            5. **Wawasan Bisnis** - Dapatkan insight untuk strategi marketing
            
            **Faktor Penilaian Kesamaan:**
            - ✅ **Tipe Klien** (30%): Corporate, Figure, Community, dll
            - ✅ **Kedekatan Tahun** (20%): Periode kerjasama
            - ✅ **Kesamaan Layanan** (30%): Jenis layanan yang digunakan
            - ✅ **Status Loyalitas** (15%): Loyal vs Non-loyal
            - ✅ **Jumlah Layanan** (5%): Kompleksitas kebutuhan
            
            **Mulai analisis dengan memilih klien di atas!**
            """)
        
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
        st.header("🔎 Pencarian Calon Klien Berdasarkan Profil")
        
        if st.session_state.instagram_logged_in:
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Cari Calon Klien Potensial</h4>
            <p>Temukan calon klien di Indonesia dengan minimal 2000 followers yang membutuhkan layanan video/foto</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Form pencarian sederhana
            with st.container():
                st.markdown('<div class="search-box">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Pilihan kata kunci pencarian
                    search_options = [
                        "butuh videographer jakarta",
                        "cari photographer indonesia", 
                        "video wedding indonesia",
                        "content creator indonesia",
                        "startup indonesia",
                        "business jakarta",
                        "company profile video",
                        "foto produk jakarta"
                    ]
                    
                    selected_keyword = st.selectbox("🔍 Pilih kata kunci pencarian:", search_options)
                    custom_keyword = st.text_input("🔍 Atau masukkan kata kunci sendiri:", 
                                                 placeholder="contoh: dokter jakarta butuh video")
                    
                    search_query = custom_keyword if custom_keyword else selected_keyword
                
                with col2:
                    st.markdown("**Filter:**")
                    min_followers = st.number_input("Min. Followers:", min_value=2000, max_value=100000, value=2000, step=1000)
                    max_results = st.number_input("Max. Hasil:", min_value=5, max_value=20, value=10)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Tombol pencarian
                if st.button("🚀 Mulai Pencarian Profil", type="primary", use_container_width=True):
                    if search_query:
                        with st.spinner(f"Mencari calon klien dengan kata kunci: '{search_query}'"):
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            st.session_state.search_results = []
                            found_count = 0
                            
                            try:
                                # Cari users
                                status_text.text("Mencari pengguna Instagram...")
                                progress_bar.progress(0.2)
                                
                                users = search_instagram_users_optimized(st.session_state.instagram_client, search_query, 50)
                                
                                if users:
                                    total_users = len(users)
                                    
                                    for idx, user in enumerate(users):
                                        if found_count >= max_results:
                                            break
                                        
                                        progress_bar.progress(0.2 + (idx / total_users) * 0.8)
                                        username = getattr(user, 'username', 'unknown')
                                        status_text.text(f"Menganalisis @{username}...")
                                        
                                        try:
                                            user_details = get_user_details_optimized(st.session_state.instagram_client, user.pk)
                                            
                                            if user_details:
                                                follower_count = getattr(user_details, 'follower_count', 0)
                                                
                                                # Filter: minimal followers dan lokasi Indonesia
                                                if follower_count >= min_followers and is_indonesian_user(user_details):
                                                    
                                                    # Deteksi kebutuhan
                                                    needs, need_confidence = detect_video_photo_needs(user_details)
                                                    
                                                    # Hitung skor potensi
                                                    potential_score = calculate_client_potential_score(
                                                        user_details, needs, need_confidence, follower_count
                                                    )
                                                    
                                                    # Simpan jika memenuhi kriteria
                                                    if potential_score >= 20:  # Threshold minimal
                                                        st.session_state.search_results.append({
                                                            'username': getattr(user_details, 'username', 'N/A'),
                                                            'full_name': getattr(user_details, 'full_name', 'N/A'),
                                                            'follower_count': follower_count,
                                                            'biography': getattr(user_details, 'biography', ''),
                                                            'needs': needs,
                                                            'need_confidence': need_confidence,
                                                            'potential_score': potential_score,
                                                            'is_verified': getattr(user_details, 'is_verified', False),
                                                            'is_business': getattr(user_details, 'is_business', False)
                                                        })
                                                        found_count += 1
                                                        status_text.text(f"Ditemukan {found_count} calon klien potensial")
                                            
                                            time.sleep(random.uniform(1, 2))  # Delay untuk menghindari rate limit
                                            
                                        except Exception:
                                            continue
                                    
                                    progress_bar.progress(1.0)
                                    status_text.text(f"✅ Pencarian selesai! Ditemukan {found_count} calon klien")
                                
                                else:
                                    st.warning("Tidak ditemukan pengguna dengan kata kunci tersebut")
                                    
                            except Exception as e:
                                st.error(f"Error saat pencarian: {str(e)}")
                    else:
                        st.warning("Pilih atau masukkan kata kunci pencarian")
            
            # Tampilkan hasil pencarian
            if st.session_state.search_results:
                st.subheader("📊 Hasil Pencarian")
                
                # Urutkan berdasarkan skor potensi
                sorted_results = sorted(st.session_state.search_results, 
                                      key=lambda x: x['potential_score'], reverse=True)
                
                # Statistik singkat
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Ditemukan", len(sorted_results))
                with col2:
                    high_potential = sum(1 for r in sorted_results if r['potential_score'] >= 60)
                    st.metric("Potensi Tinggi", high_potential)
                with col3:
                    avg_followers = sum(r['follower_count'] for r in sorted_results) // len(sorted_results)
                    st.metric("Rata-rata Followers", f"{avg_followers:,}")
                
                # Tampilkan hasil
                for i, client in enumerate(sorted_results):
                    verified_badge = "✅" if client['is_verified'] else ""
                    business_badge = "🏢" if client['is_business'] else ""
                    
                    # Tentukan warna skor
                    if client['potential_score'] >= 60:
                        score_class = "score-high"
                        priority = "🔥 PRIORITAS TINGGI"
                    elif client['potential_score'] >= 40:
                        score_class = "score-medium"
                        priority = "⭐ POTENSI BAIK"
                    else:
                        score_class = "score-low"
                        priority = "💡 POTENSI RENDAH"
                    
                    with st.expander(f"{i+1}. @{client['username']} {verified_badge}{business_badge} - Skor: {client['potential_score']}/100", 
                                   expanded=i < 3):
                        
                        col_info1, col_info2 = st.columns([3, 1])
                        
                        with col_info1:
                            st.markdown(f"**👤 Nama:** {client['full_name']}")
                            st.markdown(f"**📊 Followers:** {client['follower_count']:,}")
                            
                            if client['biography']:
                                st.markdown(f"**📝 Bio:** {client['biography']}")
                            
                            if client['needs']:
                                st.markdown("**🎯 Kebutuhan Terdeteksi:**")
                                for need in client['needs']:
                                    st.markdown(f'<span class="need-indicator">{need}</span>', unsafe_allow_html=True)
                                st.markdown(f"**Confidence Level:** {client['need_confidence']}/100")
                        
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
                if st.button("📥 Download Hasil (CSV)", use_container_width=True):
                    export_df = pd.DataFrame([
                        {
                            'Username': r['username'],
                            'Full Name': r['full_name'],
                            'Followers': r['follower_count'],
                            'Biography': r['biography'],
                            'Needs': ', '.join(r['needs']),
                            'Need Confidence': r['need_confidence'],
                            'Potential Score': r['potential_score'],
                            'Verified': r['is_verified'],
                            'Business Account': r['is_business'],
                            'Instagram Link': f"https://instagram.com/{r['username']}"
                        }
                        for r in sorted_results
                    ])
                    
                    csv_data = export_df.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=f"calon_klien_parthaistic_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
            
            else:
                st.info("""
                **🎯 Cara Menggunakan Pencarian Calon Klien:**
                
                1. **Pilih Kata Kunci** - Pilih dari daftar atau masukkan sendiri
                2. **Atur Filter** - Set minimal followers (min. 2000) dan jumlah hasil
                3. **Mulai Pencarian** - Klik tombol untuk memulai pencarian otomatis
                4. **Lihat Hasil** - Dapatkan daftar calon klien dengan scoring prioritas
                5. **Download Data** - Export hasil untuk follow-up
                
                **Kriteria Pencarian:**
                - ✅ Minimal 2000 followers
                - ✅ Berlokasi di Indonesia
                - ✅ Menunjukkan kebutuhan video/foto
                - ✅ Akun aktif dan relevan
                
                **Mulai pencarian sekarang!**
                """)
        
        else:
            st.warning("⚠️ Login Instagram diperlukan untuk menggunakan fitur pencarian calon klien")
            st.info("Silakan login Instagram di sidebar untuk mengakses fitur ini")

    with tab6:
        st.header("📱 Pencarian Berdasarkan Posts & Hashtag")
        
        if st.session_state.instagram_logged_in:
            st.markdown("""
            <div class="post-search-card">
                <h4>🎯 Pencarian Calon Klien Berdasarkan Konten Posts</h4>
                <p>Fitur baru! Temukan calon klien dengan menganalisis konten posts dan hashtag mereka. 
                Metode ini lebih akurat karena menganalisis apa yang benar-benar mereka posting.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Form pencarian berdasarkan hashtag dan konten
            with st.container():
                st.markdown('<div class="search-box">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("🔍 Pilih Metode Pencarian")
                    
                    search_method = st.radio(
                        "Metode pencarian:",
                        ["Hashtag", "Kata Kunci dalam Caption"],
                        help="Pilih apakah ingin mencari berdasarkan hashtag atau kata kunci dalam caption post"
                    )
                    
                    if search_method == "Hashtag":
                        st.markdown("**📌 Pencarian berdasarkan Hashtag Populer:**")
                        hashtag_options = [
                            "butuhvideographer",
                            "cariphotographer", 
                            "videowedding",
                            "contentcreator",
                            "videoproduction",
                            "photography",
                            "weddingvideo",
                            "companyprofile",
                            "eventdocumentation",
                            "commercialvideo"
                        ]
                        
                        selected_hashtag = st.selectbox("Pilih hashtag:", hashtag_options)
                        custom_hashtag = st.text_input("Atau masukkan hashtag sendiri (tanpa #):", 
                                                     placeholder="contoh: videojkt")
                        
                        search_query = custom_hashtag if custom_hashtag else selected_hashtag
                        
                    else:  # Kata Kunci dalam Caption
                        st.markdown("**💬 Pencarian berdasarkan Kata Kunci dalam Caption:**")
                        caption_keywords = [
                            "butuh videographer",
                            "cari photographer",
                            "video wedding",
                            "dokumentasi event",
                            "company profile",
                            "video promosi",
                            "foto produk",
                            "content creator"
                        ]
                        
                        selected_caption = st.selectbox("Pilih kata kunci caption:", caption_keywords)
                        custom_caption = st.text_input("Atau masukkan kata kunci sendiri:", 
                                                     placeholder="contoh: butuh video untuk startup")
                        
                        search_query = custom_caption if custom_caption else selected_caption
                
                with col2:
                    st.markdown("**⚙️ Pengaturan Pencarian:**")
                    min_followers_post = st.number_input("Min. Followers:", min_value=1000, max_value=100000, value=1000, step=500)
                    max_posts = st.number_input("Max. Posts Dianalisis:", min_value=20, max_value=100, value=50, step=10)
                    max_results_post = st.number_input("Max. Hasil Klien:", min_value=5, max_value=15, value=10)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Tombol pencarian
                if st.button("🚀 Mulai Pencarian Posts", type="primary", use_container_width=True):
                    if search_query:
                        with st.spinner(f"Mencari posts dengan {'hashtag #' if search_method == 'Hashtag' else 'kata kunci'}: '{search_query}'"):
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            st.session_state.post_search_results = []
                            found_count = 0
                            
                            try:
                                if search_method == "Hashtag":
                                    # Pencarian berdasarkan hashtag
                                    status_text.text(f"Mencari posts dengan hashtag #{search_query}...")
                                    progress_bar.progress(0.1)
                                    
                                    posts = search_posts_by_hashtag(st.session_state.instagram_client, search_query, max_posts)
                                    
                                    if posts:
                                        total_posts = len(posts)
                                        status_text.text(f"Menganalisis {total_posts} posts...")
                                        
                                        analyzed_users = set()  # Untuk menghindari duplikasi user
                                        
                                        for idx, post in enumerate(posts):
                                            if found_count >= max_results_post:
                                                break
                                            
                                            progress_bar.progress(0.1 + (idx / total_posts) * 0.9)
                                            
                                            try:
                                                user_id = getattr(post, 'user', {}).pk if hasattr(getattr(post, 'user', {}), 'pk') else None
                                                
                                                if user_id and user_id not in analyzed_users:
                                                    analyzed_users.add(user_id)
                                                    
                                                    # Analisis konten post
                                                    post_analysis = analyze_post_content(post)
                                                    
                                                    if post_analysis['confidence'] >= 20:  # Threshold minimal untuk post
                                                        # Dapatkan detail user
                                                        user_details = get_user_details_optimized(st.session_state.instagram_client, user_id)
                                                        
                                                        if user_details:
                                                            follower_count = getattr(user_details, 'follower_count', 0)
                                                            
                                                            # Filter berdasarkan followers dan lokasi Indonesia
                                                            if follower_count >= min_followers_post and is_indonesian_user(user_details):
                                                                
                                                                # Dapatkan lebih banyak posts dari user untuk analisis yang lebih komprehensif
                                                                user_posts = get_user_posts(st.session_state.instagram_client, user_id, 10)
                                                                
                                                                # Analisis semua posts user
                                                                post_analyses = [analyze_post_content(p) for p in user_posts[:5]]  # Analisis 5 post terakhir
                                                                post_analyses = [pa for pa in post_analyses if pa['confidence'] > 0]
                                                                
                                                                if post_analyses:
                                                                    # Hitung skor berdasarkan posts
                                                                    potential_score = calculate_post_based_score(
                                                                        user_details, post_analyses, follower_count
                                                                    )
                                                                    
                                                                    if potential_score >= 25:  # Threshold untuk post-based search
                                                                        # Gabungkan semua kebutuhan yang terdeteksi
                                                                        all_needs = []
                                                                        all_hashtags = []
                                                                        all_relevant_hashtags = []
                                                                        sample_captions = []
                                                                        
                                                                        for pa in post_analyses:
                                                                            all_needs.extend(pa['needs'])
                                                                            all_hashtags.extend(pa['hashtags'])
                                                                            all_relevant_hashtags.extend(pa['relevant_hashtags'])
                                                                            if pa['caption_excerpt']:
                                                                                sample_captions.append(pa['caption_excerpt'])
                                                                        
                                                                        unique_needs = list(set(all_needs))
                                                                        unique_hashtags = list(set(all_hashtags))
                                                                        unique_relevant_hashtags = list(set(all_relevant_hashtags))
                                                                        
                                                                        avg_confidence = sum(pa['confidence'] for pa in post_analyses) / len(post_analyses)
                                                                        
                                                                        st.session_state.post_search_results.append({
                                                                            'username': getattr(user_details, 'username', 'N/A'),
                                                                            'full_name': getattr(user_details, 'full_name', 'N/A'),
                                                                            'follower_count': follower_count,
                                                                            'biography': getattr(user_details, 'biography', ''),
                                                                            'needs': unique_needs,
                                                                            'avg_confidence': avg_confidence,
                                                                            'potential_score': potential_score,
                                                                            'is_verified': getattr(user_details, 'is_verified', False),
                                                                            'is_business': getattr(user_details, 'is_business', False),
                                                                            'hashtags': unique_hashtags[:10],  # Maksimal 10 hashtag
                                                                            'relevant_hashtags': unique_relevant_hashtags,
                                                                            'sample_captions': sample_captions[:3],  # Maksimal 3 contoh caption
                                                                            'posts_analyzed': len(post_analyses)
                                                                        })
                                                                        found_count += 1
                                                                        status_text.text(f"Ditemukan {found_count} calon klien dari analisis posts")
                                                
                                                time.sleep(random.uniform(0.5, 1.5))  # Delay untuk menghindari rate limit
                                                
                                            except Exception:
                                                continue
                                        
                                        progress_bar.progress(1.0)
                                        status_text.text(f"✅ Analisis selesai! Ditemukan {found_count} calon klien berdasarkan posts")
                                    
                                    else:
                                        st.warning(f"Tidak ditemukan posts dengan hashtag #{search_query}")
                                
                                else:
                                    # Untuk pencarian berdasarkan caption, kita perlu menggunakan pendekatan yang berbeda
                                    # Karena Instagram API tidak mendukung pencarian caption secara langsung
                                    st.info("Pencarian berdasarkan kata kunci caption sedang dalam pengembangan. Silakan gunakan pencarian hashtag untuk saat ini.")
                                    
                            except Exception as e:
                                st.error(f"Error saat pencarian posts: {str(e)}")
                    else:
                        st.warning("Masukkan hashtag atau kata kunci pencarian")
            
            # Tampilkan hasil pencarian posts
            if st.session_state.post_search_results:
                st.subheader("📊 Hasil Pencarian Berdasarkan Posts")
                
                # Urutkan berdasarkan skor potensi
                sorted_post_results = sorted(st.session_state.post_search_results, 
                                           key=lambda x: x['potential_score'], reverse=True)
                
                # Statistik singkat
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Ditemukan", len(sorted_post_results))
                with col2:
                    high_potential = sum(1 for r in sorted_post_results if r['potential_score'] >= 60)
                    st.metric("Potensi Tinggi", high_potential)
                with col3:
                    avg_followers = sum(r['follower_count'] for r in sorted_post_results) // len(sorted_post_results)
                    st.metric("Rata-rata Followers", f"{avg_followers:,}")
                with col4:
                    total_posts = sum(r['posts_analyzed'] for r in sorted_post_results)
                    st.metric("Total Posts Dianalisis", total_posts)
                
                # Tampilkan hasil
                for i, client in enumerate(sorted_post_results):
                    verified_badge = "✅" if client['is_verified'] else ""
                    business_badge = "🏢" if client['is_business'] else ""
                    
                    # Tentukan warna skor
                    if client['potential_score'] >= 60:
                        score_class = "score-high"
                        priority = "🔥 PRIORITAS TINGGI"
                    elif client['potential_score'] >= 40:
                        score_class = "score-medium"
                        priority = "⭐ POTENSI BAIK"
                    else:
                        score_class = "score-low"
                        priority = "💡 POTENSI RENDAH"
                    
                    with st.expander(f"{i+1}. @{client['username']} {verified_badge}{business_badge} - Skor: {client['potential_score']}/100 ({client['posts_analyzed']} posts)", 
                                   expanded=i < 2):
                        
                        col_info1, col_info2 = st.columns([2, 1])
                        
                        with col_info1:
                            st.markdown(f"**👤 Nama:** {client['full_name']}")
                            st.markdown(f"**📊 Followers:** {client['follower_count']:,}")
                            
                            if client['biography']:
                                st.markdown(f"**📝 Bio:** {client['biography']}")
                            
                            if client['needs']:
                                st.markdown("**🎯 Kebutuhan Terdeteksi dari Posts:**")
                                for need in client['needs']:
                                    st.markdown(f'<span class="need-indicator">{need}</span>', unsafe_allow_html=True)
                                st.markdown(f"**Confidence Level:** {client['avg_confidence']:.1f}/100")
                            
                            # Tampilkan hashtags relevan
                            if client['relevant_hashtags']:
                                st.markdown("**📌 Hashtag Relevan:**")
                                for hashtag in client['relevant_hashtags'][:8]:  # Maksimal 8 hashtag
                                    st.markdown(f'<span class="hashtag-indicator">{hashtag}</span>', unsafe_allow_html=True)
                            
                            # Tampilkan contoh caption
                            if client['sample_captions']:
                                st.markdown("**💬 Contoh Caption Posts:**")
                                for idx, caption in enumerate(client['sample_captions'][:2]):  # Maksimal 2 contoh
                                    st.markdown(f'<div class="post-content">Post {idx+1}: {caption}</div>', unsafe_allow_html=True)
                        
                        with col_info2:
                            st.markdown(f"[📱 Lihat Profil](https://instagram.com/{client['username']})")
                            st.markdown(f'<p class="{score_class}">Skor: {client["potential_score"]}/100</p>', 
                                      unsafe_allow_html=True)
                            
                            st.markdown(f'<span class="engagement-metric">Posts: {client["posts_analyzed"]}</span>', unsafe_allow_html=True)
                            
                            if client['potential_score'] >= 60:
                                st.success("🔥 PRIORITAS TINGGI")
                            elif client['potential_score'] >= 40:
                                st.warning("⭐ POTENSI BAIK")
                            else:
                                st.info("💡 MONITOR")
                
                # Export hasil
                if st.button("📥 Download Hasil Posts (CSV)", use_container_width=True):
                    export_df = pd.DataFrame([
                        {
                            'Username': r['username'],
                            'Full Name': r['full_name'],
                            'Followers': r['follower_count'],
                            'Biography': r['biography'],
                            'Needs': ', '.join(r['needs']),
                            'Avg Confidence': r['avg_confidence'],
                            'Potential Score': r['potential_score'],
                            'Posts Analyzed': r['posts_analyzed'],
                            'Relevant Hashtags': ', '.join(r['relevant_hashtags']),
                            'All Hashtags': ', '.join(r['hashtags']),
                            'Verified': r['is_verified'],
                            'Business Account': r['is_business'],
                            'Instagram Link': f"https://instagram.com/{r['username']}"
                        }
                        for r in sorted_post_results
                    ])
                    
                    csv_data = export_df.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=f"calon_klien_posts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
            
            else:
                st.info("""
                **📱 Cara Menggunakan Pencarian Berdasarkan Posts & Hashtag:**
                
                ### 🎯 **Keunggulan Metode Ini:**
                - ✅ **Lebih Akurat**: Menganalisis konten yang benar-benar diposting user
                - ✅ **Deteksi Real-time**: Menemukan kebutuhan aktual dari posts terbaru
                - ✅ **Analisis Hashtag**: Mengidentifikasi hashtag relevan yang digunakan
                - ✅ **Konteks Lengkap**: Melihat caption dan konten untuk pemahaman yang lebih baik
                
                ### 🔍 **Cara Penggunaan:**
                1. **Pilih Metode** - Hashtag atau kata kunci dalam caption
                2. **Tentukan Query** - Pilih dari daftar atau masukkan sendiri
                3. **Atur Filter** - Set minimal followers dan jumlah hasil
                4. **Mulai Pencarian** - Sistem akan menganalisis posts dan konten
                5. **Review Hasil** - Lihat analisis lengkap dengan contoh posts
                
                ### 📌 **Contoh Hashtag Efektif:**
                - `#butuhvideographer` - Mencari yang butuh videographer
                - `#cariphotographer` - Mencari yang butuh photographer  
                - `#videowedding` - Target pasar wedding
                - `#contentcreator` - Target content creator
                - `#companyprofile` - Target perusahaan
                
                ### 💡 **Tips Pencarian:**
                - Gunakan hashtag spesifik untuk hasil yang lebih relevan
                - Coba variasi kata kunci untuk jangkauan yang lebih luas
                - Perhatikan engagement rate dari posts yang ditemukan
                - Analisis hashtag yang digunakan untuk strategi marketing
                
                **Mulai pencarian berdasarkan posts sekarang!**
                """)
        
        else:
            st.warning("⚠️ Login Instagram diperlukan untuk menggunakan fitur pencarian berdasarkan posts")
            st.info("Silakan login Instagram di sidebar untuk mengakses fitur ini")

else:
    st.warning("⚠️ Tidak dapat memuat data. Periksa file CSV Anda.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎬 Dasbor Analisis Klien Parthaistic | Enhanced with Post & Hashtag Search</p>
    <p>Versi 9.0 - Complete Client Analysis with Advanced Post-based Discovery</p>
</div>
""", unsafe_allow_html=True)
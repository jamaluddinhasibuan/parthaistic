import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from collections import Counter
import re
import time
import random
import json
import requests
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, RateLimitError
import base64

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
    .following-tag {
        background: #17a2b8;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .post-tag {
        background: #fd7e14;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .score-high { color: #28a745; font-weight: bold; }
    .score-medium { color: #ffc107; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }
    .upload-box {
        border: 2px dashed #2E86AB;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk login Instagram
def instagram_login(username, password):
    try:
        cl = Client()
        cl.set_user_agent("Instagram 219.0.0.12.117 Android")
        cl.login(username, password)
        return cl, True
    except LoginRequired:
        st.error("❌ Login gagal: Username atau password salah")
        return None, False
    except PleaseWaitFewMinutes:
        st.error("⏰ Instagram meminta untuk menunggu beberapa menit. Coba lagi nanti.")
        return None, False
    except Exception as e:
        st.error(f"❌ Login gagal: {str(e)}")
        return None, False

# Fungsi untuk mencari pengguna Instagram
def search_instagram_users(cl, query, max_results=100):
    try:
        time.sleep(2)
        users = cl.search_users(query)
        return users[:max_results] if users else []
    except RateLimitError:
        st.warning("⚠️ Rate limit tercapai. Menunggu 60 detik...")
        time.sleep(60)
        try:
            users = cl.search_users(query)
            return users[:max_results] if users else []
        except Exception as e:
            st.error(f"❌ Pencarian gagal setelah retry: {str(e)}")
            return []
    except Exception as e:
        st.error(f"❌ Pencarian gagal: {str(e)}")
        return []

# Fungsi untuk mencari berdasarkan hashtag
def search_by_hashtag(cl, hashtag, max_results=50):
    try:
        time.sleep(2)
        medias = cl.hashtag_medias_recent(hashtag, max_results)
        return medias
    except Exception as e:
        st.error(f"❌ Pencarian hashtag gagal: {str(e)}")
        return []

# Fungsi untuk mendapatkan detail pengguna
def get_user_details(cl, user_id):
    try:
        time.sleep(random.uniform(1, 3))
        user_details = cl.user_info(user_id)
        return user_details
    except RateLimitError:
        st.warning("⚠️ Rate limit tercapai saat mengambil detail user. Menunggu...")
        time.sleep(30)
        return None
    except Exception:
        return None

# Fungsi untuk mendapatkan postingan terbaru pengguna
def get_user_recent_posts(cl, user_id, count=10):
    try:
        time.sleep(random.uniform(1, 2))
        medias = cl.user_medias(user_id, count)
        return medias
    except Exception:
        return []

# Fungsi untuk menganalisis caption postingan
def analyze_post_captions(medias):
    video_photo_needs = []
    hashtags_found = []
    
    # Kata kunci untuk kebutuhan video/foto dalam postingan
    need_keywords = [
        'butuh videographer', 'cari videographer', 'need videographer',
        'butuh photographer', 'cari photographer', 'need photographer',
        'butuh video editor', 'cari video editor', 'need video editor',
        'butuh foto', 'cari foto', 'need photo',
        'butuh video', 'cari video', 'need video',
        'jasa video', 'jasa foto', 'video service', 'photo service',
        'video wedding', 'foto wedding', 'wedding videographer',
        'wedding photographer', 'prewedding video', 'prewedding foto',
        'company profile video', 'video promosi', 'video iklan',
        'foto produk', 'product photo', 'commercial video',
        'event documentation', 'dokumentasi event', 'liputan event'
    ]
    
    # Hashtag yang menunjukkan kebutuhan
    target_hashtags = [
        '#butuhvideographer', '#carivideographer', '#needvideographer',
        '#butuhphotographer', '#cariphotographer', '#needphotographer',
        '#jasavideo', '#jasafoto', '#videoservice', '#photoservice',
        '#videowedding', '#fotowedding', '#weddingvideographer',
        '#weddingphotographer', '#preweddingvideo', '#preweddingfoto',
        '#companyprofile', '#videopromosi', '#videoiklan',
        '#fotoproduk', '#productphoto', '#commercialvideo',
        '#eventdocumentation', '#dokumentasievent', '#liputanevent',
        '#videomarketing', '#contentcreator', '#digitalmarketing'
    ]
    
    for media in medias:
        caption = getattr(media, 'caption_text', '') or ""
        caption_lower = caption.lower()
        
        # Cek kebutuhan dalam caption
        for keyword in need_keywords:
            if keyword in caption_lower:
                video_photo_needs.append(f"Post: {keyword}")
        
        # Cek hashtag
        for hashtag in target_hashtags:
            if hashtag in caption_lower:
                hashtags_found.append(hashtag)
    
    return list(set(video_photo_needs)), list(set(hashtags_found))

# Fungsi untuk mendapatkan daftar following pengguna (sampel)
def get_user_following_sample(cl, user_id, max_count=50):
    try:
        time.sleep(random.uniform(2, 4))
        following = cl.user_following(user_id, max_count)
        return following
    except Exception:
        return []

# Fungsi untuk mendeteksi lokasi Indonesia
def is_indonesian_user(user_details):
    if not user_details:
        return False
    
    bio = (getattr(user_details, 'biography', '') or "").lower()
    username = getattr(user_details, 'username', '').lower()
    full_name = (getattr(user_details, 'full_name', '') or "").lower()
    
    # Kata kunci lokasi Indonesia yang diperluas
    indonesia_keywords = [
        'indonesia', 'jakarta', 'surabaya', 'bandung', 'medan', 'semarang',
        'palembang', 'makassar', 'depok', 'tangerang', 'bekasi', 'bogor',
        'yogyakarta', 'yogya', 'jogja', 'malang', 'solo', 'bali', 'denpasar',
        'balikpapan', 'pontianak', 'manado', 'pekanbaru', 'banjarmasin',
        'samarinda', 'jambi', 'padang', 'aceh', 'lampung', 'riau', 'sumatra',
        'kalimantan', 'sulawesi', 'papua', 'jawa', 'nusantara', 'batam',
        'cirebon', 'tasikmalaya', 'serang', 'cilegon', 'sukabumi', 'garut',
        'purwokerto', 'tegal', 'pekalongan', 'magelang', 'klaten', 'sukoharjo',
        'karanganyar', 'wonogiri', 'pacitan', 'magetan', 'ngawi', 'madiun',
        'ponorogo', 'tulungagung', 'blitar', 'kediri', 'jombang', 'mojokerto',
        'sidoarjo', 'gresik', 'lamongan', 'tuban', 'bojonegoro', 'nganjuk',
        'lumajang', 'jember', 'bondowoso', 'situbondo', 'probolinggo',
        'pasuruan', 'banyuwangi', 'id', 'idn', 'ina'
    ]
    
    text_to_check = f"{bio} {username} {full_name}"
    return any(keyword in text_to_check for keyword in indonesia_keywords)

# Fungsi untuk mendeteksi kebutuhan video/foto
def detect_video_photo_needs(user_details):
    if not user_details:
        return [], 0
    
    bio = (getattr(user_details, 'biography', '') or "").lower()
    username = getattr(user_details, 'username', '').lower()
    full_name = (getattr(user_details, 'full_name', '') or "").lower()
    
    # Kata kunci kebutuhan video/foto yang sangat spesifik
    need_keywords = {
        'video_production': [
            'butuh video', 'cari videographer', 'need video', 'video content',
            'video marketing', 'video promosi', 'video company profile',
            'video dokumentasi', 'video event', 'video wedding', 'video prewedding',
            'video commercial', 'video iklan', 'video product', 'video tutorial',
            'video edukasi', 'video campaign', 'video social media', 'video instagram',
            'video youtube', 'video tiktok', 'video reels', 'video story',
            'cinematic video', 'video sinematik', 'video profesional'
        ],
        'photography': [
            'butuh foto', 'cari photographer', 'need photo', 'foto produk',
            'foto wedding', 'foto prewedding', 'foto maternity', 'foto family',
            'foto corporate', 'foto headshot', 'foto profile', 'foto event',
            'foto dokumentasi', 'foto commercial', 'foto fashion', 'foto food',
            'foto architecture', 'foto interior', 'foto landscape', 'foto portrait',
            'photo session', 'photoshoot', 'foto studio', 'foto outdoor'
        ],
        'content_creation': [
            'content creator', 'konten kreator', 'social media content',
            'instagram content', 'tiktok content', 'youtube content',
            'digital marketing', 'social media marketing', 'brand content',
            'creative content', 'visual content', 'multimedia content'
        ],
        'business_needs': [
            'company profile', 'profil perusahaan', 'corporate video',
            'business video', 'promotional video', 'marketing material',
            'brand awareness', 'product launch', 'event coverage',
            'documentation', 'testimoni video', 'training video'
        ]
    }
    
    detected_needs = []
    confidence_score = 0
    
    text_to_check = f"{bio} {username} {full_name}"
    
    for category, keywords in need_keywords.items():
        category_matches = sum(1 for keyword in keywords if keyword in text_to_check)
        if category_matches > 0:
            detected_needs.append(category.replace('_', ' ').title())
            confidence_score += category_matches * 10
    
    # Boost score untuk kata kunci yang sangat spesifik
    high_value_keywords = [
        'butuh video', 'cari videographer', 'butuh foto', 'cari photographer',
        'need video', 'need photo', 'video marketing', 'content creator'
    ]
    
    for keyword in high_value_keywords:
        if keyword in text_to_check:
            confidence_score += 25
    
    return detected_needs, min(confidence_score, 100)

# Fungsi untuk menganalisis following patterns
def analyze_following_patterns(cl, user_id, existing_clients_data):
    try:
        following_list = get_user_following_sample(cl, user_id, 30)
        if not following_list:
            return [], 0
        
        # Daftar akun yang relevan dengan industri kreatif/video/foto
        creative_industry_accounts = [
            'videographer', 'photographer', 'filmmaker', 'contentcreator',
            'digitalmarketing', 'socialmedia', 'creative', 'production',
            'studio', 'agency', 'media', 'visual', 'cinema', 'photo'
        ]
        
        # Analisis berdasarkan existing clients
        existing_client_usernames = []
        if existing_clients_data is not None:
            for _, row in existing_clients_data.iterrows():
                instagram = str(row.get('Instagram', '')).replace('@', '').lower()
                if instagram and instagram != 'nan':
                    existing_client_usernames.append(instagram)
        
        relevant_following = []
        pattern_score = 0
        
        for followed_user in following_list:
            username = getattr(followed_user, 'username', '').lower()
            
            # Cek apakah mengikuti existing clients
            if username in existing_client_usernames:
                relevant_following.append(f"Existing Client: @{username}")
                pattern_score += 20
            
            # Cek apakah mengikuti akun industri kreatif
            for keyword in creative_industry_accounts:
                if keyword in username:
                    relevant_following.append(f"Creative Industry: @{username}")
                    pattern_score += 10
                    break
        
        return relevant_following[:10], min(pattern_score, 100)
    
    except Exception:
        return [], 0

# Fungsi untuk menghitung skor potensi klien
def calculate_client_potential_score(user_details, needs, need_confidence, following_score, follower_count, post_needs, hashtags):
    base_score = 0
    
    # Skor berdasarkan followers (max 25 poin)
    if follower_count >= 100000:
        base_score += 25
    elif follower_count >= 50000:
        base_score += 20
    elif follower_count >= 10000:
        base_score += 15
    elif follower_count >= 5000:
        base_score += 10
    elif follower_count >= 1000:
        base_score += 5
    
    # Skor berdasarkan kebutuhan video/foto (max 30 poin)
    base_score += min(need_confidence * 0.3, 30)
    
    # Skor berdasarkan pola following (max 25 poin)
    base_score += min(following_score * 0.25, 25)
    
    # Skor berdasarkan postingan yang menunjukkan kebutuhan (max 20 poin)
    post_score = len(post_needs) * 5 + len(hashtags) * 3
    base_score += min(post_score, 20)
    
    # Skor berdasarkan verifikasi (10 poin)
    if getattr(user_details, 'is_verified', False):
        base_score += 10
    
    # Skor berdasarkan akun bisnis (5 poin)
    if getattr(user_details, 'is_business', False):
        base_score += 5
    
    # Skor berdasarkan bio yang lengkap (5 poin)
    bio = getattr(user_details, 'biography', '') or ""
    if len(bio) > 50:
        base_score += 5
    
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

# Sidebar login Instagram
with st.sidebar:
    st.header("🔐 Login Instagram")
    
    if not st.session_state.instagram_logged_in:
        insta_username = st.text_input("Username Instagram")
        insta_password = st.text_input("Password Instagram", type="password")
        
        if st.button("🚀 Login Instagram", type="primary"):
            if insta_username and insta_password:
                with st.spinner("Sedang login ke Instagram..."):
                    client, success = instagram_login(insta_username, insta_password)
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
        # Data default jika tidak ada file yang diupload
        data = """Name,Year,Type,Service 1,Service 2,Service 3,Regular End Period,Instagram
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
        
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        st.info("📄 Menggunakan data default. Upload file CSV untuk menggunakan data Anda sendiri.")
    
    # Bersihkan dan proses data
    df['Regular End Period'] = pd.to_numeric(df['Regular End Period'], errors='coerce')
    
    # Buat kombinasi layanan
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
    
    # Definisikan klien loyal (mereka yang memiliki Periode Akhir Reguler)
    df['Is_Loyal'] = df['Regular End Period'].notna()
    df['Loyalty_Duration'] = df['Regular End Period'] - df['Year']
    df['Loyalty_Duration'] = df['Loyalty_Duration'].fillna(0)
    
    return df

# Area upload file
st.subheader("📁 Upload Data CSV")
uploaded_file = st.file_uploader(
    "Pilih file CSV Anda", 
    type=['csv'],
    help="Upload file CSV dengan kolom: Name, Year, Type, Service 1, Service 2, Service 3, Regular End Period, Instagram"
)

# Template download
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Download Template CSV"):
        template_data = """Name,Year,Type,Service 1,Service 2,Service 3,Regular End Period,Instagram
Contoh Klien 1,2024,Corporate,Video Editor,,,,
Contoh Klien 2,2024,Figure,All In Regular,,,2025,@username
Contoh Klien 3,2023,Community,Custom Video Production,Video Editor,,,"""
        
        st.download_button(
            label="📄 Download Template",
            data=template_data,
            file_name="template_klien_parthaistic.csv",
            mime="text/csv"
        )

with col2:
    if uploaded_file:
        st.success("✅ File CSV berhasil diupload!")
        # Preview data
        if st.checkbox("👀 Preview Data"):
            preview_df = pd.read_csv(uploaded_file)
            st.dataframe(preview_df.head(), use_container_width=True)
    else:
        st.info("🔄 Menggunakan data contoh. Upload file CSV untuk analisis data Anda.")

# Muat data
df = load_and_process_data(uploaded_file)

if df is not None:
    # Tampilkan info dataset
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Kolom Data", len(df.columns))
    with col3:
        unique_services = len(set([service for services in df['Services'] for service in services]))
        st.metric("Unique Services", unique_services)

    # Filter Sidebar
    st.sidebar.header("🔍 Opsi Filter & Analisis")
    selected_years = st.sidebar.multiselect("Pilih Tahun", sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
    selected_types = st.sidebar.multiselect("Pilih Tipe Klien", df['Type'].unique(), default=df['Type'].unique())

    # Filter data
    filtered_df = df[(df['Year'].isin(selected_years)) & (df['Type'].isin(selected_types))]

    # Tab Dasbor Utama
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Gambaran Umum", "🎯 Profiling Klien", "🔍 Analisis Klien Loyal", "💡 Wawasan Bisnis", "🔎 Temukan Klien Baru", "📱 Pencarian Berdasarkan Postingan"])

    with tab1:
        st.header("📊 Gambaran Umum Bisnis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(filtered_df)}</h3>
                <p>Total Klien</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            loyal_clients = len(filtered_df[filtered_df['Is_Loyal']])
            st.markdown(f"""
            <div class="metric-card">
                <h3>{loyal_clients}</h3>
                <p>Klien Loyal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            loyalty_rate = (loyal_clients / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>{loyalty_rate:.1f}%</h3>
                <p>Tingkat Loyalitas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_services = filtered_df['Service_Count'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_services:.1f}</h3>
                <p>Rata-rata Layanan/Klien</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Grafik
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Klien berdasarkan Tahun & Tipe")
            year_type_data = filtered_df.groupby(['Year', 'Type']).size().reset_index(name='Count')
            fig = px.bar(year_type_data, x='Year', y='Count', color='Type',
                        title="Distribusi Klien berdasarkan Tahun dan Tipe")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🥧 Distribusi Tipe Klien")
            type_counts = filtered_df['Type'].value_counts()
            fig = px.pie(values=type_counts.values, names=type_counts.index,
                        title="Distribusi Tipe Klien")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Popularitas layanan
        st.subheader("🎬 Analisis Popularitas Layanan")
        all_services = []
        for services_list in filtered_df['Services']:
            all_services.extend(services_list)
        
        if all_services:
            service_counts = pd.Series(all_services).value_counts().head(10)
            fig = px.bar(x=service_counts.values, y=service_counts.index, orientation='h',
                        title="10 Layanan Paling Banyak Diminta")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("🎯 Profiling Klien Tingkat Lanjut")
        
        # Fungsi kesamaan profil
        def find_similar_clients(target_client, df, top_n=5):
            if target_client not in df['Name'].values:
                return None
            
            target_row = df[df['Name'] == target_client].iloc[0]
            similarities = []
            
            for idx, row in df.iterrows():
                if row['Name'] == target_client:
                    continue
                    
                similarity_score = 0
                
                # Kesamaan Tipe
                if row['Type'] == target_row['Type']:
                    similarity_score += 3
                
                # Kedekatan Tahun
                year_diff = abs(row['Year'] - target_row['Year'])
                if year_diff <= 1:
                    similarity_score += 2
                elif year_diff <= 2:
                    similarity_score += 1
                
                # Kesamaan Layanan
                target_services = set(target_row['Services'])
                row_services = set(row['Services'])
                service_intersection = len(target_services.intersection(row_services))
                service_union = len(target_services.union(row_services))
                if service_union > 0:
                    jaccard_similarity = service_intersection / service_union
                    similarity_score += jaccard_similarity * 4
                
                # Kesamaan Loyalitas
                if row['Is_Loyal'] == target_row['Is_Loyal']:
                    similarity_score += 2
                
                similarities.append({
                    'Name': row['Name'],
                    'Similarity_Score': similarity_score,
                    'Type': row['Type'],
                    'Year': row['Year'],
                    'Services': row['Services'],
                    'Is_Loyal': row['Is_Loyal']
                })
            
            similarities_df = pd.DataFrame(similarities)
            return similarities_df.nlargest(top_n, 'Similarity_Score')
        
        # Pemilihan klien untuk profiling
        st.subheader("🔍 Temukan Klien Serupa")
        selected_client = st.selectbox("Pilih klien untuk menemukan profil serupa:", 
                                     [""] + sorted(filtered_df['Name'].tolist()))
        
        if selected_client:
            similar_clients = find_similar_clients(selected_client, filtered_df)
            
            if similar_clients is not None:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    target_info = filtered_df[filtered_df['Name'] == selected_client].iloc[0]
                    st.markdown(f"""
                    <div class="insight-box">
                        <h4>Klien Target: {selected_client}</h4>
                        <p><strong>Tipe:</strong> {target_info['Type']}</p>
                        <p><strong>Tahun:</strong> {target_info['Year']}</p>
                        <p><strong>Layanan:</strong> {', '.join(target_info['Services'])}</p>
                        <p><strong>Loyal:</strong> {'Ya' if target_info['Is_Loyal'] else 'Tidak'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.subheader("🤝 Klien Paling Serupa")
                    for idx, client in similar_clients.iterrows():
                        similarity_pct = (client['Similarity_Score'] / 10) * 100
                        loyalty_status = "Loyal" if client['Is_Loyal'] else "Non-loyal"
                        
                        st.markdown(f"""
                        <div class="insight-box">
                            <h5>{client['Name']} (Kesamaan: {similarity_pct:.1f}%)</h5>
                            <p><strong>Tipe:</strong> {client['Type']} | <strong>Tahun:</strong> {client['Year']} | <strong>Status:</strong> {loyalty_status}</p>
                            <p><strong>Layanan:</strong> {', '.join(client['Services'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Analisis pola
        st.subheader("📊 Analisis Pola Klien")
        
        # Pola kombinasi layanan
        service_combinations = {}
        for services in filtered_df['Services']:
            if len(services) > 1:
                combo = tuple(sorted(services))
                service_combinations[combo] = service_combinations.get(combo, 0) + 1
        
        if service_combinations:
            top_combos = sorted(service_combinations.items(), key=lambda x: x[1], reverse=True)[:10]
            
            combo_df = pd.DataFrame([
                {'Kombinasi': ' + '.join(combo), 'Jumlah': count}
                for combo, count in top_combos
            ])
            
            fig = px.bar(combo_df, x='Jumlah', y='Kombinasi', orientation='h',
                        title="Kombinasi Layanan Paling Umum")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🔍 Analisis Mendalam Klien Loyal")
        
        loyal_df = filtered_df[filtered_df['Is_Loyal']].copy()
        
        if len(loyal_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👑 Karakteristik Klien Loyal")
                
                # Distribusi tipe klien loyal
                loyal_types = loyal_df['Type'].value_counts()
                fig = px.pie(values=loyal_types.values, names=loyal_types.index,
                            title="Klien Loyal berdasarkan Tipe")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("⏰ Analisis Durasi Loyalitas")
                
                loyalty_duration = loyal_df[loyal_df['Loyalty_Duration'] > 0]['Loyalty_Duration']
                if len(loyalty_duration) > 0:
                    fig = px.histogram(loyalty_duration, nbins=10,
                                     title="Distribusi Durasi Loyalitas (Tahun)")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Tidak ada data durasi loyalitas yang tersedia")
            
            # Layanan klien loyal
            st.subheader("🎬 Layanan Populer di Kalangan Klien Loyal")
            loyal_services = []
            for services in loyal_df['Services']:
                loyal_services.extend(services)
            
            if loyal_services:
                loyal_service_counts = pd.Series(loyal_services).value_counts().head(8)
                fig = px.bar(x=loyal_service_counts.values, y=loyal_service_counts.index, 
                            orientation='h', title="Layanan Teratas di Kalangan Klien Loyal")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Faktor keberhasilan loyalitas
            st.subheader("✨ Faktor Keberhasilan Loyalitas")
            
            total_clients_by_type = filtered_df.groupby('Type').size()
            loyal_clients_by_type = loyal_df.groupby('Type').size()
            loyalty_rate_by_type = (loyal_clients_by_type / total_clients_by_type * 100).fillna(0)
            
            factors_df = pd.DataFrame({
                'Tipe_Klien': loyalty_rate_by_type.index,
                'Tingkat_Loyalitas': loyalty_rate_by_type.values
            }).sort_values('Tingkat_Loyalitas', ascending=False)
            
            fig = px.bar(factors_df, x='Tipe_Klien', y='Tingkat_Loyalitas',
                        title="Tingkat Loyalitas berdasarkan Tipe Klien (%)")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Tidak ada klien loyal yang ditemukan dalam filter yang dipilih.")

    with tab4:
        st.header("💡 Intelijen Bisnis & Wawasan yang Dapat Ditindaklanjuti")
        
        # Hasilkan wawasan
        insights = []
        
        # Analisis tren pertumbuhan
        yearly_growth = filtered_df.groupby('Year').size()
        if len(yearly_growth) > 1:
            latest_growth = yearly_growth.iloc[-1] - yearly_growth.iloc[-2]
            growth_rate = (latest_growth / yearly_growth.iloc[-2]) * 100 if yearly_growth.iloc[-2] > 0 else 0
            insights.append(f"📈 **Tren Pertumbuhan**: Pertumbuhan klien {growth_rate:+.1f}% dari {yearly_growth.index[-2]} ke {yearly_growth.index[-1]}")
        
        # Diversifikasi layanan
        avg_services_per_client = filtered_df['Service_Count'].mean()
        if avg_services_per_client < 1.5:
            insights.append("🎯 **Peluang Upselling**: Rata-rata layanan per klien rendah. Fokus pada penjualan silang layanan tambahan.")
        
        # Wawasan loyalitas
        if len(filtered_df[filtered_df['Is_Loyal']]) > 0:
            loyalty_rate = len(filtered_df[filtered_df['Is_Loyal']]) / len(filtered_df) * 100
            insights.append(f"👑 **Tingkat Loyalitas**: {loyalty_rate:.1f}% klien menjadi pelanggan setia")
            
            # Tipe paling loyal
            loyal_by_type = filtered_df.groupby('Type')['Is_Loyal'].mean() * 100
            most_loyal_type = loyal_by_type.idxmax()
            insights.append(f"🏆 **Tipe Klien Terbaik**: Klien {most_loyal_type} memiliki tingkat loyalitas tertinggi ({loyal_by_type[most_loyal_type]:.1f}%)")
        
        # Wawasan layanan
        all_services_flat = []
        for services in filtered_df['Services']:
            all_services_flat.extend(services)
        
        if all_services_flat:
            most_popular_service = pd.Series(all_services_flat).value_counts().index[0]
            insights.append(f"🌟 **Layanan Paling Populer**: {most_popular_service} adalah layanan yang paling banyak diminta")
        
        # Peluang pasar
        recent_clients = filtered_df[filtered_df['Year'] >= 2023]
        if len(recent_clients) > 0:
            trending_type = recent_clients['Type'].value_counts().index[0]
            insights.append(f"🚀 **Tren Pasar**: Klien {trending_type} sedang tren dalam beberapa tahun terakhir")
        
        # Tampilkan wawasan
        st.subheader("🎯 Wawasan Bisnis Utama")
        for insight in insights:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

    with tab5:
        st.header("🔎 Pencarian Calon Klien Berdasarkan Profil")
        
        if st.session_state.instagram_logged_in:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("🎯 Parameter Pencarian Klien")
                
                # Pilihan kata kunci pencarian yang lebih spesifik
                search_categories = {
                    "Video Production Needs": [
                        "butuh videographer jakarta",
                        "cari video editor indonesia", 
                        "video wedding indonesia",
                        "video company profile",
                        "content creator indonesia",
                        "video marketing jakarta"
                    ],
                    "Photography Needs": [
                        "butuh photographer jakarta",
                        "foto wedding indonesia",
                        "foto produk jakarta",
                        "photographer professional",
                        "foto corporate indonesia",
                        "photoshoot jakarta"
                    ],
                    "Business & Corporate": [
                        "startup indonesia",
                        "perusahaan jakarta",
                        "business indonesia",
                        "corporate jakarta",
                        "company indonesia",
                        "brand indonesia"
                    ],
                    "Creative Industry": [
                        "creative agency jakarta",
                        "digital agency indonesia",
                        "marketing agency",
                        "advertising indonesia",
                        "media production",
                        "creative studio"
                    ]
                }
                
                selected_category = st.selectbox("Pilih kategori pencarian:", list(search_categories.keys()))
                search_query = st.selectbox("Pilih kata kunci:", search_categories[selected_category])
                custom_query = st.text_input("Atau masukkan kata kunci kustom:", 
                                           placeholder="contoh: dokter jakarta butuh video")
                
                final_query = custom_query if custom_query else search_query
                
                # Parameter filter
                min_followers = st.slider("Minimal followers:", 1000, 100000, 1000, 1000)
                max_results = st.slider("Maksimal hasil pencarian:", 10, 50, 20, 5)
                
                # Tombol pencarian
                if st.button("🔍 Cari Calon Klien Indonesia", type="primary"):
                    if final_query:
                        with st.spinner(f"Mencari calon klien dengan kata kunci '{final_query}'..."):
                            # Progress tracking
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # Reset hasil pencarian
                            st.session_state.search_results = []
                            successful_searches = 0
                            total_processed = 0
                            
                            # Variasi query untuk hasil yang lebih baik
                            query_variations = [
                                final_query,
                                f"{final_query} indonesia",
                                final_query.replace(" ", "")
                            ]
                            
                            for query_idx, query in enumerate(query_variations):
                                if successful_searches >= max_results:
                                    break
                                
                                status_text.text(f"Mencari dengan: {query}")
                                progress_bar.progress((query_idx + 1) / len(query_variations) * 0.2)
                                
                                try:
                                    users = search_instagram_users(st.session_state.instagram_client, query, 100)
                                    
                                    if users:
                                        for user_idx, user in enumerate(users):
                                            if successful_searches >= max_results:
                                                break
                                            
                                            total_processed += 1
                                            username = getattr(user, 'username', 'unknown')
                                            status_text.text(f"Menganalisis @{username} ({total_processed})")
                                            progress_bar.progress(0.2 + (successful_searches / max_results) * 0.8)
                                            
                                            try:
                                                user_details = get_user_details(st.session_state.instagram_client, user.pk)
                                                
                                                if user_details:
                                                    follower_count = getattr(user_details, 'follower_count', 0)
                                                    
                                                    # Filter: Indonesia, minimal followers
                                                    if (follower_count >= min_followers and 
                                                        is_indonesian_user(user_details)):
                                                        
                                                        # Deteksi kebutuhan video/foto
                                                        needs, need_confidence = detect_video_photo_needs(user_details)
                                                        
                                                        # Analisis pola following
                                                        following_patterns, following_score = analyze_following_patterns(
                                                            st.session_state.instagram_client, 
                                                            user.pk, 
                                                            df
                                                        )
                                                        
                                                        # Analisis postingan terbaru
                                                        recent_posts = get_user_recent_posts(st.session_state.instagram_client, user.pk, 10)
                                                        post_needs, hashtags_found = analyze_post_captions(recent_posts)
                                                        
                                                        # Hitung skor potensi
                                                        potential_score = calculate_client_potential_score(
                                                            user_details, needs, need_confidence, 
                                                            following_score, follower_count, post_needs, hashtags_found
                                                        )
                                                        
                                                        # Hanya simpan jika ada indikasi kebutuhan atau skor tinggi
                                                        if needs or post_needs or hashtags_found or potential_score >= 30:
                                                            st.session_state.search_results.append({
                                                                'username': getattr(user_details, 'username', 'N/A'),
                                                                'full_name': getattr(user_details, 'full_name', 'N/A'),
                                                                'follower_count': follower_count,
                                                                'biography': getattr(user_details, 'biography', ''),
                                                                'needs': needs,
                                                                'need_confidence': need_confidence,
                                                                'following_patterns': following_patterns,
                                                                'following_score': following_score,
                                                                'post_needs': post_needs,
                                                                'hashtags_found': hashtags_found,
                                                                'potential_score': potential_score,
                                                                'is_verified': getattr(user_details, 'is_verified', False),
                                                                'is_business': getattr(user_details, 'is_business', False)
                                                            })
                                                            successful_searches += 1
                                                            status_text.text(f"Ditemukan {successful_searches} calon klien potensial")
                                                
                                                # Delay untuk menghindari rate limit
                                                time.sleep(random.uniform(2, 4))
                                                
                                            except Exception:
                                                continue
                                
                                except Exception as e:
                                    st.warning(f"Error pada query '{query}': {str(e)}")
                                    continue
                            
                            progress_bar.progress(1.0)
                            status_text.text(f"✅ Selesai! Ditemukan {successful_searches} calon klien potensial")
                            
                            if successful_searches == 0:
                                st.warning("Tidak ditemukan calon klien yang memenuhi kriteria. Coba kata kunci yang berbeda.")
                    else:
                        st.warning("Pilih atau masukkan kata kunci pencarian terlebih dahulu.")
            
            with col2:
                st.subheader("📊 Hasil Pencarian - Calon Klien Potensial")
                
                if st.session_state.search_results:
                    # Urutkan berdasarkan skor potensi
                    sorted_results = sorted(st.session_state.search_results, 
                                          key=lambda x: x['potential_score'], reverse=True)
                    
                    st.success(f"🎯 Ditemukan {len(sorted_results)} calon klien potensial!")
                    
                    # Statistik hasil
                    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                    with col_stat1:
                        avg_score = sum(r['potential_score'] for r in sorted_results) / len(sorted_results)
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{avg_score:.0f}</h3>
                            <p>Rata-rata Skor</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat2:
                        high_potential = sum(1 for r in sorted_results if r['potential_score'] >= 70)
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{high_potential}</h3>
                            <p>Potensi Tinggi</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat3:
                        verified_count = sum(1 for r in sorted_results if r['is_verified'])
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{verified_count}</h3>
                            <p>Terverifikasi</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat4:
                        with_post_needs = sum(1 for r in sorted_results if r['post_needs'] or r['hashtags_found'])
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{with_post_needs}</h3>
                            <p>Butuh di Postingan</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tampilkan hasil detail
                    for i, client in enumerate(sorted_results):
                        verified_badge = "✅" if client['is_verified'] else ""
                        business_badge = "🏢" if client['is_business'] else ""
                        
                        # Tentukan warna skor
                        if client['potential_score'] >= 70:
                            score_class = "score-high"
                        elif client['potential_score'] >= 50:
                            score_class = "score-medium"
                        else:
                            score_class = "score-low"
                        
                        with st.expander(f"{i+1}. @{client['username']} {verified_badge}{business_badge} - Skor: {client['potential_score']}/100", 
                                       expanded=i < 3):
                            
                            col_info1, col_info2 = st.columns([2, 1])
                            
                            with col_info1:
                                st.markdown(f"**👤 Nama:** {client['full_name']}")
                                st.markdown(f"**📊 Followers:** {client['follower_count']:,}")
                                
                                if client['biography']:
                                    st.markdown(f"**📝 Bio:** {client['biography']}")
                                
                                # Tampilkan kebutuhan yang terdeteksi dari bio
                                if client['needs']:
                                    st.markdown("**🎯 Kebutuhan dari Bio:**")
                                    for need in client['needs']:
                                        st.markdown(f'<span class="need-indicator">{need}</span>', unsafe_allow_html=True)
                                    st.markdown(f"**Confidence Level:** {client['need_confidence']}/100")
                                
                                # Tampilkan kebutuhan dari postingan
                                if client['post_needs']:
                                    st.markdown("**📱 Kebutuhan dari Postingan:**")
                                    for post_need in client['post_needs']:
                                        st.markdown(f'<span class="post-tag">{post_need}</span>', unsafe_allow_html=True)
                                
                                # Tampilkan hashtag yang ditemukan
                                if client['hashtags_found']:
                                    st.markdown("**#️⃣ Hashtag Relevan:**")
                                    for hashtag in client['hashtags_found']:
                                        st.markdown(f'<span class="post-tag">{hashtag}</span>', unsafe_allow_html=True)
                                
                                # Tampilkan pola following
                                if client['following_patterns']:
                                    st.markdown("**👥 Pola Following Relevan:**")
                                    for pattern in client['following_patterns'][:5]:
                                        st.markdown(f'<span class="following-tag">{pattern}</span>', unsafe_allow_html=True)
                                    st.markdown(f"**Following Score:** {client['following_score']}/100")
                            
                            with col_info2:
                                # Link ke profil
                                st.markdown(f"[📱 Lihat Profil](https://instagram.com/{client['username']})")
                                
                                # Skor potensi dengan warna
                                st.markdown(f'<p class="{score_class}">Skor Potensi: {client["potential_score"]}/100</p>', 
                                          unsafe_allow_html=True)
                                
                                # Rekomendasi tindakan
                                if client['potential_score'] >= 70:
                                    st.success("🔥 PRIORITAS TINGGI - Hubungi segera!")
                                elif client['potential_score'] >= 50:
                                    st.warning("⭐ POTENSI BAIK - Pertimbangkan untuk dihubungi")
                                else:
                                    st.info("💡 POTENSI RENDAH - Monitor untuk masa depan")
                    
                    # Export hasil
                    if st.session_state.search_results:
                        export_df = pd.DataFrame([
                            {
                                'Username': r['username'],
                                'Full Name': r['full_name'],
                                'Followers': r['follower_count'],
                                'Biography': r['biography'],
                                'Bio Needs': ', '.join(r['needs']),
                                'Need Confidence': r['need_confidence'],
                                'Post Needs': ', '.join(r['post_needs']),
                                'Hashtags Found': ', '.join(r['hashtags_found']),
                                'Following Patterns': ', '.join(r['following_patterns'][:3]),
                                'Following Score': r['following_score'],
                                'Potential Score': r['potential_score'],
                                'Verified': r['is_verified'],
                                'Business Account': r['is_business'],
                                'Instagram Link': f"https://instagram.com/{r['username']}"
                            }
                            for r in sorted_results
                        ])
                        
                        csv_data = export_df.to_csv(index=False)
                        
                        st.download_button(
                            label="📥 Download Hasil Pencarian (CSV)",
                            data=csv_data,
                            file_name=f"calon_klien_parthaistic_{final_query.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                
                else:
                    st.info("""
                    **🎯 SISTEM PENCARIAN CALON KLIEN PARTHAISTIC**
                    
                    **Fitur Unggulan:**
                    - ✅ Deteksi otomatis kebutuhan video/foto dari bio Instagram
                    - ✅ Analisis pola following berdasarkan klien existing
                    - ✅ Filter lokasi Indonesia yang akurat
                    - ✅ Minimal 1000 followers untuk kualitas klien
                    - ✅ Scoring system untuk prioritas follow-up
                    - ✅ Export hasil dalam format CSV
                    
                    **Mulai pencarian dengan memilih kata kunci di sebelah kiri!**
                    """)
        else:
            st.warning("⚠️ Login Instagram diperlukan untuk menggunakan fitur pencarian")

    with tab6:
        st.header("📱 Pencarian Berdasarkan Hashtag & Postingan")
        
        if st.session_state.instagram_logged_in:
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Pencarian Calon Klien Berdasarkan Hashtag & Konten Postingan</h4>
            <p>Temukan calon klien yang secara aktif mencari videographer dan photographer melalui hashtag dan caption postingan mereka</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("🔍 Parameter Pencarian Hashtag")
                
                # Hashtag yang menunjukkan kebutuhan video/foto
                hashtag_categories = {
                    "Video Production": [
                        "butuhvideographer",
                        "carivideographer", 
                        "needvideographer",
                        "jasavideo",
                        "videoservice",
                        "videowedding",
                        "weddingvideographer",
                        "videopromosi",
                        "videomarketing"
                    ],
                    "Photography": [
                        "butuhphotographer",
                        "cariphotographer",
                        "needphotographer", 
                        "jasafoto",
                        "photoservice",
                        "fotowedding",
                        "weddingphotographer",
                        "fotoproduk",
                        "productphoto"
                    ],
                    "Event Documentation": [
                        "eventdocumentation",
                        "dokumentasievent",
                        "liputanevent",
                        "eventvideo",
                        "eventphoto",
                        "weddingdocumentation",
                        "corporateevent"
                    ],
                    "Content Creation": [
                        "contentcreator",
                        "digitalmarketing",
                        "socialmediamarketing",
                        "instagramcontent",
                        "tiktokcontent",
                        "youtubecontent"
                    ]
                }
                
                selected_hashtag_category = st.selectbox("Pilih kategori hashtag:", list(hashtag_categories.keys()))
                selected_hashtag = st.selectbox("Pilih hashtag:", hashtag_categories[selected_hashtag_category])
                custom_hashtag = st.text_input("Atau masukkan hashtag kustom (tanpa #):", 
                                             placeholder="contoh: butuhvideo")
                
                final_hashtag = custom_hashtag if custom_hashtag else selected_hashtag
                
                # Parameter filter
                min_followers_hashtag = st.slider("Minimal followers (hashtag):", 1000, 100000, 1000, 1000, key="hashtag_followers")
                max_posts = st.slider("Maksimal postingan untuk dianalisis:", 10, 100, 30, 5)
                
                # Tombol pencarian hashtag
                if st.button("🔍 Cari Berdasarkan Hashtag", type="primary"):
                    if final_hashtag:
                        with st.spinner(f"Mencari postingan dengan hashtag #{final_hashtag}..."):
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # Reset hasil pencarian hashtag
                            hashtag_results = []
                            processed_users = set()
                            
                            try:
                                # Cari postingan berdasarkan hashtag
                                status_text.text(f"Mengambil postingan dari #{final_hashtag}")
                                progress_bar.progress(0.1)
                                
                                medias = search_by_hashtag(st.session_state.instagram_client, final_hashtag, max_posts)
                                
                                if medias:
                                    total_medias = len(medias)
                                    status_text.text(f"Ditemukan {total_medias} postingan, menganalisis...")
                                    
                                    for media_idx, media in enumerate(medias):
                                        progress_bar.progress(0.1 + (media_idx / total_medias) * 0.9)
                                        
                                        try:
                                            user_id = getattr(media, 'user', {}).pk if hasattr(getattr(media, 'user', {}), 'pk') else None
                                            if not user_id or user_id in processed_users:
                                                continue
                                            
                                            processed_users.add(user_id)
                                            
                                            # Ambil detail user
                                            user_details = get_user_details(st.session_state.instagram_client, user_id)
                                            
                                            if user_details:
                                                follower_count = getattr(user_details, 'follower_count', 0)
                                                
                                                # Filter: Indonesia, minimal followers
                                                if (follower_count >= min_followers_hashtag and 
                                                    is_indonesian_user(user_details)):
                                                    
                                                    username = getattr(user_details, 'username', 'N/A')
                                                    status_text.text(f"Menganalisis @{username} dari postingan...")
                                                    
                                                    # Analisis caption postingan
                                                    caption = getattr(media, 'caption_text', '') or ""
                                                    
                                                    # Deteksi kebutuhan dari caption
                                                    caption_needs = []
                                                    caption_lower = caption.lower()
                                                    
                                                    need_keywords_in_caption = [
                                                        'butuh videographer', 'cari videographer', 'need videographer',
                                                        'butuh photographer', 'cari photographer', 'need photographer',
                                                        'butuh video editor', 'cari video editor', 'need video editor',
                                                        'jasa video', 'jasa foto', 'video service', 'photo service',
                                                        'video wedding', 'foto wedding', 'wedding videographer',
                                                        'wedding photographer', 'video promosi', 'foto produk'
                                                    ]
                                                    
                                                    for keyword in need_keywords_in_caption:
                                                        if keyword in caption_lower:
                                                            caption_needs.append(keyword)
                                                    
                                                    # Deteksi kebutuhan dari bio
                                                    bio_needs, need_confidence = detect_video_photo_needs(user_details)
                                                    
                                                    # Analisis pola following
                                                    following_patterns, following_score = analyze_following_patterns(
                                                        st.session_state.instagram_client, 
                                                        user_id, 
                                                        df
                                                    )
                                                    
                                                    # Hitung skor potensi
                                                    potential_score = calculate_client_potential_score(
                                                        user_details, bio_needs, need_confidence, 
                                                        following_score, follower_count, caption_needs, [f"#{final_hashtag}"]
                                                    )
                                                    
                                                    # Tambahkan bonus untuk postingan yang menggunakan hashtag target
                                                    potential_score += 15
                                                    potential_score = min(potential_score, 100)
                                                    
                                                    hashtag_results.append({
                                                        'username': username,
                                                        'full_name': getattr(user_details, 'full_name', 'N/A'),
                                                        'follower_count': follower_count,
                                                        'biography': getattr(user_details, 'biography', ''),
                                                        'post_caption': caption[:200] + "..." if len(caption) > 200 else caption,
                                                        'hashtag_used': f"#{final_hashtag}",
                                                        'caption_needs': caption_needs,
                                                        'bio_needs': bio_needs,
                                                        'need_confidence': need_confidence,
                                                        'following_patterns': following_patterns,
                                                        'following_score': following_score,
                                                        'potential_score': potential_score,
                                                        'is_verified': getattr(user_details, 'is_verified', False),
                                                        'is_business': getattr(user_details, 'is_business', False),
                                                        'post_url': f"https://instagram.com/p/{getattr(media, 'code', '')}"
                                                    })
                                            
                                            # Delay untuk menghindari rate limit
                                            time.sleep(random.uniform(2, 4))
                                            
                                        except Exception:
                                            continue
                                    
                                    progress_bar.progress(1.0)
                                    status_text.text(f"✅ Selesai! Ditemukan {len(hashtag_results)} calon klien dari hashtag")
                                    
                                    # Simpan hasil ke session state dengan key khusus
                                    st.session_state.hashtag_search_results = hashtag_results
                                    
                                else:
                                    st.warning(f"Tidak ditemukan postingan dengan hashtag #{final_hashtag}")
                                    
                            except Exception as e:
                                st.error(f"Error saat mencari hashtag: {str(e)}")
                    else:
                        st.warning("Masukkan hashtag untuk pencarian")
            
            with col2:
                st.subheader("📊 Hasil Pencarian Hashtag")
                
                if 'hashtag_search_results' in st.session_state and st.session_state.hashtag_search_results:
                    hashtag_results = st.session_state.hashtag_search_results
                    
                    # Urutkan berdasarkan skor potensi
                    sorted_hashtag_results = sorted(hashtag_results, 
                                                  key=lambda x: x['potential_score'], reverse=True)
                    
                    st.success(f"🎯 Ditemukan {len(sorted_hashtag_results)} calon klien dari hashtag!")
                    
                    # Statistik hasil hashtag
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    with col_stat1:
                        avg_score_hashtag = sum(r['potential_score'] for r in sorted_hashtag_results) / len(sorted_hashtag_results)
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{avg_score_hashtag:.0f}</h3>
                            <p>Rata-rata Skor</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat2:
                        high_potential_hashtag = sum(1 for r in sorted_hashtag_results if r['potential_score'] >= 70)
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{high_potential_hashtag}</h3>
                            <p>Potensi Tinggi</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_stat3:
                        with_caption_needs = sum(1 for r in sorted_hashtag_results if r['caption_needs'])
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>{with_caption_needs}</h3>
                            <p>Butuh di Caption</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Tampilkan hasil hashtag
                    for i, client in enumerate(sorted_hashtag_results):
                        verified_badge = "✅" if client['is_verified'] else ""
                        business_badge = "🏢" if client['is_business'] else ""
                        
                        # Tentukan warna skor
                        if client['potential_score'] >= 70:
                            score_class = "score-high"
                        elif client['potential_score'] >= 50:
                            score_class = "score-medium"
                        else:
                            score_class = "score-low"
                        
                        with st.expander(f"{i+1}. @{client['username']} {verified_badge}{business_badge} - Skor: {client['potential_score']}/100", 
                                       expanded=i < 3):
                            
                            col_info1, col_info2 = st.columns([2, 1])
                            
                            with col_info1:
                                st.markdown(f"**👤 Nama:** {client['full_name']}")
                                st.markdown(f"**📊 Followers:** {client['follower_count']:,}")
                                
                                if client['biography']:
                                    st.markdown(f"**📝 Bio:** {client['biography']}")
                                
                                # Tampilkan hashtag yang digunakan
                                st.markdown(f"**#️⃣ Hashtag:** {client['hashtag_used']}")
                                
                                # Tampilkan caption postingan
                                if client['post_caption']:
                                    st.markdown(f"**📱 Caption Postingan:** {client['post_caption']}")
                                
                                # Tampilkan kebutuhan dari caption
                                if client['caption_needs']:
                                    st.markdown("**🎯 Kebutuhan dari Caption:**")
                                    for need in client['caption_needs']:
                                        st.markdown(f'<span class="need-indicator">{need}</span>', unsafe_allow_html=True)
                                
                                # Tampilkan kebutuhan dari bio
                                if client['bio_needs']:
                                    st.markdown("**📝 Kebutuhan dari Bio:**")
                                    for need in client['bio_needs']:
                                        st.markdown(f'<span class="need-indicator">{need}</span>', unsafe_allow_html=True)
                                
                                # Tampilkan pola following
                                if client['following_patterns']:
                                    st.markdown("**👥 Pola Following:**")
                                    for pattern in client['following_patterns'][:3]:
                                        st.markdown(f'<span class="following-tag">{pattern}</span>', unsafe_allow_html=True)
                            
                            with col_info2:
                                # Link ke profil dan postingan
                                st.markdown(f"[📱 Lihat Profil](https://instagram.com/{client['username']})")
                                if client['post_url']:
                                    st.markdown(f"[📄 Lihat Postingan]({client['post_url']})")
                                
                                # Skor potensi
                                st.markdown(f'<p class="{score_class}">Skor Potensi: {client["potential_score"]}/100</p>', 
                                          unsafe_allow_html=True)
                                
                                # Rekomendasi
                                if client['potential_score'] >= 70:
                                    st.success("🔥 PRIORITAS TINGGI!")
                                elif client['potential_score'] >= 50:
                                    st.warning("⭐ POTENSI BAIK")
                                else:
                                    st.info("💡 MONITOR")
                    
                    # Export hasil hashtag
                    if sorted_hashtag_results:
                        export_hashtag_df = pd.DataFrame([
                            {
                                'Username': r['username'],
                                'Full Name': r['full_name'],
                                'Followers': r['follower_count'],
                                'Biography': r['biography'],
                                'Hashtag Used': r['hashtag_used'],
                                'Post Caption': r['post_caption'],
                                'Caption Needs': ', '.join(r['caption_needs']),
                                'Bio Needs': ', '.join(r['bio_needs']),
                                'Following Patterns': ', '.join(r['following_patterns'][:3]),
                                'Potential Score': r['potential_score'],
                                'Verified': r['is_verified'],
                                'Business Account': r['is_business'],
                                'Instagram Link': f"https://instagram.com/{r['username']}",
                                'Post URL': r['post_url']
                            }
                            for r in sorted_hashtag_results
                        ])
                        
                        csv_hashtag_data = export_hashtag_df.to_csv(index=False)
                        
                        st.download_button(
                            label="📥 Download Hasil Hashtag (CSV)",
                            data=csv_hashtag_data,
                            file_name=f"calon_klien_hashtag_{final_hashtag}.csv",
                            mime="text/csv"
                        )
                
                else:
                    st.info("""
                    **🎯 PENCARIAN BERDASARKAN HASHTAG & POSTINGAN**
                    
                    **Fitur Unggulan:**
                    - ✅ Pencarian berdasarkan hashtag spesifik
                    - ✅ Analisis caption postingan untuk kebutuhan
                    - ✅ Deteksi otomatis dari bio dan postingan
                    - ✅ Filter lokasi Indonesia
                    - ✅ Scoring berdasarkan relevansi hashtag
                    - ✅ Link langsung ke postingan yang relevan
                    
                    **Cara Kerja:**
                    1. Pilih kategori hashtag yang relevan
                    2. Sistem akan mencari postingan dengan hashtag tersebut
                    3. Analisis setiap user yang menggunakan hashtag
                    4. Deteksi kebutuhan dari caption dan bio
                    5. Berikan skor potensi berdasarkan relevansi
                    
                    **Mulai dengan memilih hashtag di sebelah kiri!**
                    """)
        else:
            st.warning("⚠️ Login Instagram diperlukan untuk fitur pencarian hashtag")

else:
    st.warning("⚠️ Tidak dapat memuat data. Periksa file CSV Anda.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎬 Dasbor Analisis Klien Parthaistic | Advanced Instagram Analytics</p>
    <p>Versi 4.0 - Enhanced dengan Pencarian Hashtag & Analisis Postingan</p>
</div>
""", unsafe_allow_html=True)
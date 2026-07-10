import streamlit as st
from PIL import Image
import os

# Import views modular resmi
from views.parent_view import render_parent_dashboard
from views.volunteer_view import render_volunteer_dashboard
from views.admin_dashboard import render_admin_dashboard

# 1. Konfigurasi Halaman Utama Terpusat
st.set_page_config(page_title="Sahabat Anak", page_icon="👶", layout="centered")

# --- KOORDINAT MASTER LOKASI HOME BASE RELAWAN ---
HOMEBASE_LAT = -7.9502
HOMEBASE_LON = 112.6096

# 2. GLOBAL STATE INITIALIZATION (Pencegah Bug Konsol Lintas Halaman)
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = {}
if "list_relawan_dinamis" not in st.session_state:
    # Inisialisasi awal jaringan relawan terdistribusi agar terbaca di semua view
    st.session_state.list_relawan_dinamis = [
        {"nama": "Pos Relawan Klojen", "lat": -7.9502, "lon": 112.6096, "status": "Standby"},
        {"nama": "Pos Relawan Blimbing", "lat": -7.9421, "lon": 112.6410, "status": "Standby"},
        {"nama": "Pos Relawan Lowokwaru", "lat": -7.9315, "lon": 112.6172, "status": "Standby"}
    ]

# Header Aplikasi Statis
logo_path = "logo_sahabat_anak.jpg"
if os.path.exists(logo_path):
    img = Image.open(logo_path)
    col_logo, col_title = st.columns([1, 3])
    with col_logo:
        st.image(img, width=140)
    with col_title:
        st.markdown("<h1 style='margin-bottom: 0;'>Aplikasi Sahabat Anak</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #2E86C1; margin-top: 0;'>Pusat Penapisan Stres & Proteksi Spasial Dini</h4>", unsafe_allow_html=True)
        st.markdown("<i style='color: gray; font-size: 14px;'>\"Mewujudkan Malang Sehat Jiwa melalui perlindungan anak yang responsif, adaptif, dan terintegrasi.\"</i>", unsafe_allow_html=True)
else:
    st.title("👶 Aplikasi Sahabat Anak")

st.markdown("---")

# 👥 PANEL UTAMA SIDEBAR
st.sidebar.title("🔐 Akses Portal Sistem")
user_role = st.sidebar.selectbox(
    "Pilih Peran Akses Anda:",
    ["Anak / Orang Tua", "Relawan / Psikolog", "Administrator Utama"]
)

# Kontrol Router Navigasi Utama
if user_role == "Anak / Orang Tua":
    render_parent_dashboard(HOMEBASE_LAT, HOMEBASE_LON)
elif user_role == "Relawan / Psikolog":
    render_volunteer_dashboard(HOMEBASE_LAT, HOMEBASE_LON)
elif user_role == "Administrator Utama":
    render_admin_dashboard(HOMEBASE_LAT, HOMEBASE_LON)

# Footer Statis Aplikasi
st.markdown("<br><br><br><br><hr>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns([1, 4])
with col_f1:
    if os.path.exists(logo_path):
        st.image(img, width=60)
with col_f2:
    st.markdown(
        "<p style='color: gray; font-size: 13px; margin-top: 15px;'>"
        "© 2026 Aplikasi Sahabat Anak | Sistem Proteksi Spasial Multimodal<br>"
        "<b>Pengembang: M Nasri AW | Dosen STIEIMA</b></p>", 
        unsafe_allow_html=True
    )
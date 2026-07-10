import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
from src.pdf_generator import generate_report_pdf

def render_admin_dashboard(homebase_lat, homebase_lon):
    st.subheader("📊 Pangkalan Data & Monitor Spasial Utama (Admin)")
    st.markdown("---")
    
    # Proteksi Password Sederhana untuk Admin
    password_input = st.text_input("Masukkan Password Akses Administrator:", type="password", key="admin_pass_input")
    
    if password_input != "adminstieima":
        if password_input != "":
            st.error("🔑 Password Administrator Salah!")
        st.info("💡 Masukkan kode autentikasi administrator untuk memuat radar spasial.")
        return

    st.success("🔓 Hak Akses Operator Terverifikasi.")

    # Inisialisasi Data Relawan Bersebar di Session State
    if "list_relawan_dinamis" not in st.session_state:
        st.session_state.list_relawan_dinamis = [
            {"nama": "Pos Relawan Klojen", "lat": -7.9502, "lon": 112.6096, "status": "Standby"},
            {"nama": "Pos Relawan Blimbing", "lat": -7.9421, "lon": 112.6410, "status": "Standby"},
            {"nama": "Pos Relawan Lowokwaru", "lat": -7.9315, "lon": 112.6172, "status": "Standby"}
        ]

    # Form Input Relawan Baru
    st.markdown("---")
    st.write("### ➕ Pendaftaran & Plotting Lokasi Relawan Baru")
    with st.form("form_tambah_relawan"):
        nama_pos = st.text_input("Nama Pos / Identitas Relawan:", placeholder="Misal: Relawan Sukun")
        c1, c2 = st.columns(2)
        r_lat = c1.number_input("Koordinat Latitude:", value=-7.9600, format="%.5f")
        r_lon = c2.number_input("Koordinat Longitude:", value=112.6200, format="%.5f")
        submit_btn = st.form_submit_button("Plotting ke Peta")
        
        if submit_btn and nama_pos:
            st.session_state.list_relawan_dinamis.append({"nama": nama_pos, "lat": r_lat, "lon": r_lon, "status": "Standby"})
            st.success(f"📍 {nama_pos} Berhasil di-plot ke sistem radar!")

    # 1. Menampilkan Daftar Relawan & Kontrol Penugasan Aktif
    st.markdown("---")
    st.write("### 👥 Daftar Manajemen & Status Penugasan Relawan")
    
    # Render tabel kontrol untuk mengubah status relawan secara dinamis oleh admin
    for idx, relawan in enumerate(st.session_state.list_relawan_dinamis):
        col_name, col_status, col_action = st.columns([3, 2, 2])
        col_name.write(f"🔹 **{relawan['nama']}** ({relawan['lat']:.4f}, {relawan['lon']:.4f})")
        
        if relawan['status'] == "Standby":
            col_status.warning("🟡 Standby / Bersiap")
            if col_action.button("🚨 Tugaskan ke Korban", key=f"assign_{idx}"):
                st.session_state.list_relawan_dinamis[idx]['status'] = "Ditugaskan"
                st.rerun()
        else:
            col_status.success("🟢 Aktif / Ditugaskan")
            if col_action.button("✅ Kembalikan ke Pos", key=f"reset_{idx}"):
                st.session_state.list_relawan_dinamis[idx]['status'] = "Standby"
                st.rerun()

    # Statistik Kasus Spasial
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Laporan Masuk", value="12 Kasus")
    col2.metric(label="Total Jejaring Relawan Aktif", value=len(st.session_state.list_relawan_dinamis))
    col3.metric(label="Kasus Terselesaikan", value="97%")
    
    st.write("### 📋 Histori Rekam Medis Spasial Kasus")
    data_laporan = {
        "Waktu Kejadian": [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "2026-07-09 14:22:10", "2026-07-08 09:15:43"],
        "Profil Anak": ["Perempuan, 8 Tahun", "Laki-laki, 12 Tahun", "Perempuan, 5 Tahun"],
        "Skor Stres": [20, 25, 12],
        "Tingkat Intervensi": ["Level 2: Orang Tua (Kuning)", "Level 3: Bahaya / Relawan (Merah)", "Level 1: Mandiri (Hijau)"],
        "Alamat Deteksi Lokasi": [
            "De Rumah, Kel Penanggungan, Kec Klojen, Kota Malang", 
            "Prima Teknik, Jalan Sunandar Priyosudarmo, Blimbing, Kota Malang",
            "Jalan Sukarno Hatta, Lowokwaru, Kota Malang"
        ]
    }
    df = pd.DataFrame(data_laporan)
    st.dataframe(df)
    
    # Proses Kompilasi PDF
    try:
        pdf_data = generate_report_pdf(df)
        st.download_button(
            label="📥 Download Resmi Dokumen Laporan (Format .PDF)",
            data=pdf_data,
            file_name=f"Laporan_Resmi_Sahabat_Anak_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Gagal menyiapkan dokumen PDF: {e}")

    # Radar Pemantauan Spasial Makro Admin
    st.write("### 🗺️ Radar Pemantauan Spasial Makro Admin")
    m = folium.Map(location=[homebase_lat, homebase_lon], zoom_start=13)
    
    # Plot posisi anak darurat
    folium.Marker(
        [-7.95607, 112.62034], 
        popup="KASUS SOS ACTIVE: Perempuan, 8 Tahun", 
        tooltip="Posisi Anak Darurat",
        icon=folium.Icon(color="red", icon="exclamation-sign")
    ).add_to(m)
    
    # Plotting sebaran warna relawan di sisi admin
    for relawan in st.session_state.list_relawan_dinamis:
        warna_marker = "green" if relawan["status"] == "Ditugaskan" else "orange"
        folium.Marker(
            [relawan["lat"], relawan["lon"]], 
            popup=f"{relawan['nama']} ({relawan['status']})", 
            tooltip=relawan["nama"],
            icon=folium.Icon(color=warna_marker, icon="info-sign")
        ).add_to(m)
        
    st_folium(m, width=700, height=400, key="admin_map_final")
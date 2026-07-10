import streamlit as st
import folium
from streamlit_folium import st_folium

def render_volunteer_dashboard(homebase_lat, homebase_lon):
    st.subheader("🚒 Ruang Kendali Relawan Lapangan")
    st.markdown("---")
    
    # Proteksi Password Sederhana untuk Relawan
    password_input = st.text_input("Masukkan Password Akses Relawan:", type="password", key="vol_pass_input")
    
    if password_input != "relawan2026":
        if password_input != "":
            st.error("🔑 Password Salah! Silakan hubungi Administrator STIEIMA.")
        st.info("💡 Silakan masukkan password akses khusus personel relawan untuk membuka dasbor.")
        return

    st.success("🔓 Akses Diterima. Selamat bertugas!")
    
    # Status Kesiapan Relawan Lokal
    status_relawan = st.toggle("Status Operasional Pos Anda: SIAGA BANTUAN", value=True)
    if status_relawan:
        st.success("🟢 Anda berstatus SIAGA. Radar memantau sebaran kasus aktif di sekitar Anda.")
    else:
        st.warning("🔴 Anda berstatus NON-AKTIF.")
        
    st.write("### 📌 Peta Pemantauan Taktis Spasial (Multi-Marker)")
    st.markdown(
        "**Legenda Warna Peta:**<br>"
        "🔴 `Merah` = Posisi Anak/Korban Darurat | "
        "🟢 `Hijau` = Relawan Aktif (Ditugaskan) | "
        "🟡 `Kuning` = Relawan Standby (Bersiap)", 
        unsafe_allow_html=True
    )
    
    # Peta taktis berbasis lokasi homebase pusat
    m = folium.Map(location=[homebase_lat, homebase_lon], zoom_start=13)
    
    # 2. RENDER PIN MERAH KORBAN (Membaca koordinat dari session state korban aktif jika ada)
    # Untuk simulasi taktis, kita plot posisi kasus darurat aktif yang sedang terjadi
    korban_lat, korban_lon = -7.95607, 112.62034
    folium.Marker(
        [korban_lat, korban_lon], 
        popup="🚨 KORBAN DARURAT: Membutuhkan Pendampingan!", 
        tooltip="KORBAN (MERAH)",
        icon=folium.Icon(color="red", icon="exclamation-sign")
    ).add_to(m)
    
    # RENDER PIN HIJAU & KUNING BERDASARKAN KEPUTUSAN DAFTAR ADMIN
    if "list_relawan_dinamis" in st.session_state:
        for relawan in st.session_state.list_relawan_dinamis:
            if relawan["status"] == "Ditugaskan":
                # Hijau = Relawan Aktif Bergerak Ke Korban
                folium.Marker(
                    [relawan["lat"], relawan["lon"]], 
                    popup=f"Unit Aktif: {relawan['nama']}", 
                    tooltip="RELAWAN AKTIF (HIJAU)",
                    icon=folium.Icon(color="green", icon="play")
                ).add_to(m)
            else:
                # Kuning/Orange = Relawan Standby di Pos Masing-masing
                folium.Marker(
                    [relawan["lat"], relawan["lon"]], 
                    popup=f"Unit Bersiap: {relawan['nama']}", 
                    tooltip="RELAWAN STANDBY (KUNING)",
                    icon=folium.Icon(color="orange", icon="info-sign") # Folium menggunakan 'orange' untuk visualisasi warna kuning tua/emas agar kontras
                ).add_to(m)
    else:
        # Fallback jika data session kosong
        folium.Marker([homebase_lat, homebase_lon], popup="Posisi Anda (Home Base)", icon=folium.Icon(color="orange")).add_to(m)
        
    st_folium(m, width=700, height=400, key="vol_tactic_map")
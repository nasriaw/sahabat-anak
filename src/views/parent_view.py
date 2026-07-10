import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium
from src.detection import calculate_stress_level
from src.telegram_bot import send_sos_alert
from src.database import save_stress_report
from src.geo_matching import get_address_from_coords

def render_parent_dashboard(homebase_lat, homebase_lon):
    # PERBAIKAN: Inisialisasi mandiri di dalam view agar tidak memicu AttributeError
    if "show_analysis" not in st.session_state:
        st.session_state.show_analysis = False
    if "analysis_data" not in st.session_state:
        st.session_state.analysis_data = {}

    st.header("📝 Asesmen Harian Tingkat Stres")
    st.write("Silakan pilih opsi yang paling menggambarkan kondisi anak saat ini:")

    emoji_options = {1: "😄 Hebat / Nyenyak", 2: "🙂 Baik", 3: "😐 Biasa Saja", 4: "😟 Kurang Nyaman", 5: "😭 Buruk / Terganggu"}

    q1 = st.radio("1. Bagaimana perasaan anak saat belajar atau bermain hari ini?", options=[1, 2, 3, 4, 5], format_func=lambda x: emoji_options[x], horizontal=True)
    q2 = st.radio("2. Bagaimana kualitas tidur anak semalam?", options=[1, 2, 3, 4, 5], format_func=lambda x: emoji_options[x], horizontal=True)
    q3 = st.radio("3. Bagaimana nafsu makan anak hari ini?", options=[1, 2, 3, 4, 5], format_func=lambda x: emoji_options[x], horizontal=True)
    q4 = st.radio("4. Apakah anak terlihat atau merasa sulit untuk berkonsentrasi?", options=[1, 2, 3, 4, 5], format_func=lambda x: emoji_options[x], horizontal=True)
    q5 = st.radio("5. Apakah anak mengeluhkan gejala fisik akibat cemas (sakit perut/pusing)?", options=[1, 2, 3, 4, 5], format_func=lambda x: emoji_options[x], horizontal=True)

    st.caption("💡 *Validasi Instrumen Kuesioner diadopsi dari: Pediatric Symptom Checklist (PSC-17), DASS-21, dan KMME Kemenkes RI.*")

    st.markdown("---")
    st.subheader("👥 Profil Demografi Anak")
    gender = st.selectbox("Jenis Kelamin Anak:", ["Laki-laki", "Perempuan"])
    age = st.slider("Usia Anak (Tahun):", min_value=3, max_value=17, value=8)

    st.write("### 📍 Konfirmasi Lokasi Perangkat")
    location_data = streamlit_geolocation()
    lat = location_data.get("latitude")
    lon = location_data.get("longitude")

    if st.button("Kirim Hasil Asesmen"):
        list_jawaban = [q1, q2, q3, q4, q5]
        total_skor, level, warna = calculate_stress_level(list_jawaban)
        
        if lat and lon:
            alamat_fisik = get_address_from_coords(lat, lon)
        else:
            lat, lon = -7.94952, 112.64655  
            alamat_fisik = "Prima Teknik, Jalan Letnan Jenderal Sunandar Priyosudarmo, Blimbing, Kota Malang"

        identitas_label = f"{gender}, {age} Tahun"
        db_sukses, db_pesan = save_stress_report(identitas_label, total_skor, level, list_jawaban)
        
        tg_sent = False
        tg_pesan = ""
        if warna in ["orange", "red"]:
            tg_sukses, tg_pesan = send_sos_alert(identitas_label, level, alamat_fisik, lat, lon)
            tg_sent = tg_sukses

        st.session_state.analysis_data = {
            "total_skor": total_skor, "level": level, "warna": warna,
            "lat": lat, "lon": lon, "alamat": alamat_fisik, "identitas": identitas_label,
            "db_pesan": db_pesan, "tg_sent": tg_sent, "tg_pesan": tg_pesan
        }
        st.session_state.show_analysis = True

    # Pengecekan state yang sekarang dijamin aman
    if st.session_state.show_analysis:
        res = st.session_state.analysis_data
        st.markdown("---")
        st.subheader("📊 Hasil Analisis Sementara")
        st.metric(label="Total Skor Stres (Skala 0-25)", value=f"{res['total_skor']} / 25")
        st.success(res['db_pesan'])
        
        st.info(f"📍 GPS Terdeteksi Aktif: Lat {res['lat']:.5f}, Lon {res['lon']:.5f}")
        st.write(f"🏠 *Alamat Estimasi Kejadian:* {res['alamat']}")
        
        m = folium.Map(location=[res['lat'], res['lon']], zoom_start=14)
        folium.Marker([res['lat'], res['lon']], popup=f"SOS Anak ({res['identitas']})", icon=folium.Icon(color="red" if res['warna'] == "red" else "orange", icon="home")).add_to(m)
        
        if "list_relawan_dinamis" in st.session_state:
            for relawan in st.session_state.list_relawan_dinamis:
                warna_m = "green" if relawan["status"] == "Ditugaskan" else "orange"
                folium.Marker([relawan["lat"], relawan["lon"]], popup=f"Unit: {relawan['nama']}", icon=folium.Icon(color=warna_m)).add_to(m)
        else:
            folium.Marker([homebase_lat, homebase_lon], popup="Home Base Relawan Pusat", icon=folium.Icon(color="green", icon="info-sign")).add_to(m)
            
        st_folium(m, width=700, height=350, key="parent_map")
        
        if res['tg_sent']:
            st.success("🚨 Alert rute peta navigasi penanganan sukses dipancarkan ke Telegram Relawan!\n\n**Tunggu ya dik, kakak siap meluncur menemani adik**")
        
        if res['warna'] == "green": st.success(f"Status Terkendali: Kondisi psikologis anak stabil.")
        elif res['warna'] == "orange": st.warning(f"Status: {res['level']} - Ortu disarankan melakukan pendekatan suportif.")
        elif res['warna'] == "red": st.error(f"Status: {res['level']} - Peringatan Kedaruratan Emosional!")
        
        if st.button("🔄 Bersihkan Hasil & Asesmen Ulang"):
            st.session_state.show_analysis = False
            st.rerun()
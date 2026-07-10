import requests
import streamlit as st
from datetime import datetime

def send_sos_alert(child_name, status_stress, address, lat, lon):
    """
    Mengirim notifikasi darurat lengkap dengan waktu masuk laporan dan tautan navigasi
    """
    TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID")
    
    if not TOKEN or not CHAT_ID:
        return False, "Kredensial Telegram belum diatur di secrets.toml!"
    
    # Mengambil jam pelaporan masuk saat ini
    jam_masuk = datetime.now().strftime("%H:%M:%S WIB")
    gmaps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    message = (
        f"🚨 *ALARM DARURAT - SAHABAT ANAK* 🚨\n\n"
        f"🏃‍♂️ *Nama Anak:* {child_name}\n"
        f"📊 *Kondisi Stres:* {status_stress}\n"
        f"🕒 *Jam Pelaporan:* {jam_masuk}\n"
        f"📍 *Alamat Kejadian:* {address}\n"
        f"🌐 *Koordinat:* `{lat:.5f}, {lon:.5f}`\n\n"
        f"🗺️ *Tautan Navigasi:* [Klik Menuju Lokasi Anak]({gmaps_link})\n\n"
        f"⚠️ *Mohon Relawan di regional terdekat segera bergerak memberikan bantuan.*"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, "Notifikasi berhasil dikirim!"
        else:
            return False, f"Error Code: {response.status_code}"
    except Exception as e:
        return False, str(e)
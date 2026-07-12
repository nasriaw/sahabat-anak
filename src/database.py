import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from datetime import datetime
import pytz

def init_firebase():
    """
    Inisialisasi SDK Firebase Admin dengan fallback keamanan penuh.
    """
    if not firebase_admin._apps:
        try:
            # 1. Coba deteksi Cloud Secrets Streamlit (Untuk Produksi/Cloud)
            if "firebase" in st.secrets:
                firebase_info = dict(st.secrets["firebase"])
                # Pastikan karakter escape newline diproses dengan benar
                if "private_key" in firebase_info:
                    firebase_info["private_key"] = firebase_info["private_key"].replace("\\n", "\n")
                
                cred = credentials.Certificate(firebase_info)
                firebase_admin.initialize_app(cred)
            else:
                # 2. Gunakan file JSON Lokal (Untuk Pengembangan/Localhost)
                cred = credentials.Certificate("data/firebase_creds.json")
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Gagal Inisialisasi Firebase Cloud: {str(e)}")

def save_stress_report(nama_anak, total_skor, level_stres, jawaban):
    """
    Menyimpan laporan langsung ke Cloud Firestore.
    """
    try:
        init_firebase()
        db = firestore.client()
        
        zona_wib = pytz.timezone('Asia/Jakarta')
        waktu_sekarang = datetime.now(zona_wib)
        
        data = {
            "nama_anak": nama_anak,
            "total_skor": total_skor,
            "level_stres": level_stres,
            "jawaban_kuesioner": jawaban,
            "timestamp": waktu_sekarang
        }
        
        # Simpan ke koleksi stress_reports
        db.collection("stress_reports").add(data)
        return True, "Data berhasil dicatat di Cloud Firebase!"
    except Exception as e:
        # Menampilkan pesan error spesifik jika gagal push data
        return False, f"Firebase Gagal Menyimpan: {str(e)}"

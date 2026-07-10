import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from datetime import datetime

def init_firebase():
    """
    Inisialisasi koneksi SDK Firebase Admin secara aman.
    Dapat mendeteksi file lokal (saat coding) atau berbasis Cloud Secrets (saat deploy).
    """
    if not firebase_admin._apps:
        try:
            # 1. Coba baca dari Streamlit Cloud Secrets berbentuk struktur dictionary
            if "firebase" in st.secrets:
                firebase_secrets = dict(st.secrets["firebase"])
                cred = credentials.Certificate(firebase_secrets)
                firebase_admin.initialize_app(cred)
            else:
                # 2. Jika tidak ada di cloud secrets, gunakan file json lokal (untuk uji coba PC/Laptop)
                key_path = st.secrets.get("FIREBASE_KEY_PATH", "data/firebase_creds.json")
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Gagal koneksi arsitektur Firebase: {e}")

def save_stress_report(child_name, total_score, status_level, answers):
    """
    Menyimpan data kuesioner ke dalam koleksi 'stress_reports' di Firestore
    """
    init_firebase()
    db = firestore.client()
    
    # Payload data yang akan dikirim
    data = {
        "nama_anak": child_name,
        "total_skor": total_score,
        "level_stres": status_level,
        "jawaban_kuesioner": answers,
        "timestamp": datetime.now() # Untuk deteksi jangka panjang Prophet/Scikit-Learn nanti
    }
    
    try:
        # Menambahkan dokumen baru dengan ID otomatis
        db.collection("stress_reports").add(data)
        return True, "Data berhasil dicatat di Cloud Firebase!"
    except Exception as e:
        return False, str(e)

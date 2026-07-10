from geopy.geocoders import Nominatim
import streamlit as st

def get_address_from_coords(lat, lon):
    """
    Mengubah koordinat Latitude dan Longitude menjadi alamat fisik (Reverse Geocoding)
    """
    try:
        # Menggunakan user_agent unik untuk mematuhi kebijakan OSM
        geolocator = Nominatim(user_agent="sahabat_anak_app_stieima")
        location = geolocator.reverse((lat, lon), timeout=10)
        if location:
            return location.address
        return "Alamat tidak ditemukan"
    except Exception as e:
        return f"Gagal memproses alamat: {str(e)}"
def calculate_stress_level(answers):
    """
    Menghitung total skor kuesioner dan menentukan level intervensi (Triase)
    answers: list berisi 5 nilai integer (1-5)
    """
    total_skor = sum(answers)
    
    # Menentukan tingkatan berdasarkan ambang batas PRD
    if total_skor <= 15:
        level = "Level 1: Mandiri (Hijau)"
        warna = "green"
    elif total_skor <= 20:
        level = "Level 2: Orang Tua (Kuning)"
        warna = "orange"
    else:
        level = "Level 3: Bahaya / Relawan (Merah)"
        warna = "red"
        
    return total_skor, level, warna
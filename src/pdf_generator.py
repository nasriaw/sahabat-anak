import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def generate_report_pdf(dataframe):
    """
    Mengonversi data histori laporan dari Pandas Dataframe menjadi dokumen PDF formal (Letter)
    menggunakan ReportLab dan mengembalikannya dalam bentuk BytesIO stream.
    """
    buffer = io.BytesIO()
    
    # 1. Inisialisasi Dokumen PDF
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    story = []
    
    # 2. Definisikan Gaya Gaya Teks (Styles)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A5276"),
        alignment=1, # Terpusat
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'HeaderSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.gray,
        alignment=1,
        spaceAfter=15
    )
    
    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8,
        leading=11
    )
    
    cell_header_style = ParagraphStyle(
        'TableHeaderCell',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.whitesmoke,
        fontName='Helvetica-Bold'
    )

    # 3. Konten KOP Surat / Header
    story.append(Paragraph("APLIKASI SAHABAT ANAK", title_style))
    story.append(Paragraph(
        f"Dokumen Laporan Sistem Pemantauan Stres & Spasial Real-Time<br/>"
        f"Program Intervensi Dini Malang Sehat Jiwa | Dicetak pada: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", 
        subtitle_style
    ))
    story.append(Spacer(1, 10))
    
    # 4. Transformasi Dataframe ke Format Tabel ReportLab
    # Ambil header kolom asli
    table_data = [[Paragraph(col, cell_header_style) for col in dataframe.columns]]
    
    # Masukkan baris data teks dengan pembungkus Paragraph agar auto-wrap jika teks panjang
    for _, row in dataframe.iterrows():
        row_data = []
        for item in row:
            row_data.append(Paragraph(str(item), cell_style))
        table_data.append(row_data)
        
    # Lebar kolom otomatis disesuaikan dengan kertas Letter (total lebar sekitar 540 poin)
    col_widths = [90, 80, 50, 110, 210]
    
    report_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Desain Dekorasi Tabel Formal
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E86C1")), # Header tabel biru
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F6F7")]), # Baris selang-seling abu-abu
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    story.append(report_table)
    story.append(Spacer(1, 40))
    
    # 5. Bagian Blok Tanda Tangan Dokumen Resmi
    ts_style = ParagraphStyle('TS', parent=styles['Normal'], fontSize=9, leading=13, alignment=2)
    story.append(Paragraph("<b>Dikeluarkan Oleh:</b><br/>Pusat Data Administrator STIEIMA<br/><br/><br/><br/>________________________<br/><b>Ir. M Nasri AW, M.Eng.Sc, M.Kom.</b>", ts_style))
    
    # Bangun PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
# 🏥 Dashboard Visualisasi Capaian SPM Dinas Kesehatan

Dashboard ini dibangun untuk memonitoring capaian Standar Pelayanan Minimal (SPM) bidang kesehatan. Proyek ini dikembangkan menggunakan Python dan Streamlit untuk mempermudah visualisasi data kinerja per triwulan.

🔗 **Live Demo:** [Klik di sini untuk melihat Website](https://web-triwulan-dinas-kesehatan.streamlit.app)

## 🛠️ Teknologi yang Digunakan
- **Python**: Bahasa pemrograman utama.
- **Streamlit**: Framework untuk membangun web app data science.
- **Pandas**: Untuk manipulasi dan pembersihan data (Data Cleaning).
- **Seaborn & Matplotlib**: Untuk visualisasi grafik tren dan donut chart.

## ✨ Fitur Utama
1. **Upload Data Dinamis**: User dapat mengupload file Excel/CSV laporan terbaru.
2. **Visualisasi Interaktif**: 
   - Grafik Garis (Line Chart) untuk melihat tren kenaikan/penurunan per semester.
   - Donut Chart untuk melihat proporsi kontribusi per periode.
3. **Responsive Layout**: Menggunakan container dengan scroll agar nyaman dilihat di berbagai ukuran layar.
4. **Auto-Clean Data**: Algoritma otomatis memperbaiki format header Excel yang tidak standar.

## 🚀 Cara Menjalankan di Lokal
1. Clone repository ini.
2. Install dependencies: `pip install -r requirements.txt`
3. Jalankan aplikasi: `streamlit run web_triwulan.py`

---
*Proyek ini dibuat sebagai bagian dari Magang di Dinas Kesehatan Kota Klaten.*

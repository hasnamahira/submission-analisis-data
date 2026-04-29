# Bike Sharing Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis data penyewaan sepeda tahun 2011–2012.  
Dashboard ini digunakan untuk mengeksplorasi pola penggunaan sepeda berdasarkan waktu, musim, dan tipe hari.

---

## 📌 Fitur Dashboard

- 📈 Analisis tren penyewaan sepeda per bulan  
- 📊 Perbandingan penggunaan pada Working Day vs Weekend/Holiday  
- ⏰ Analisis jam dengan jumlah penyewaan tertinggi  
- 👥 Proporsi pengguna (casual vs registered)  
- 🔎 Filter data berdasarkan rentang tanggal  

---

## 📂 Struktur Project

```
submission-dashboard/
│
├── dashboard/
│   ├── dashboard.py
│   ├── day_clean.csv
│   ├── hour_clean.csv
│
├── README.md
├── requirements.txt
```

---

## ⚙️ Instalasi

Pastikan sudah menginstal Python (versi 3.8 atau lebih baru).

### 1. Clone repository
```bash
git clone https://github.com/username/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```

### 2. (Opsional) Buat virtual environment
```bash
python -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

Jika belum ada file `requirements.txt`, gunakan:

```
streamlit
pandas
matplotlib
```

---

## ▶️ Cara Menjalankan Dashboard

Jalankan perintah berikut di terminal:

```bash
streamlit run dashboard/dashboard.py
```

Lalu buka di browser:

```
http://localhost:8501
```

---

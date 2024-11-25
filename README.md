# Sistem Klasifikasi Status Stunting

Aplikasi web untuk mengklasifikasikan status stunting pada balita berdasarkan berbagai parameter antropometri.

## Fitur

- Klasifikasi status BB/U (Berat Badan menurut Umur)
- Klasifikasi status TB/U (Tinggi Badan menurut Umur)
- Klasifikasi status BB/TB (Berat Badan menurut Tinggi Badan)
- Interface web yang responsif
- API endpoint untuk integrasi

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Backend: Python Flask
- Machine Learning: scikit-learn
- Deployment: 
  - Frontend: GitHub Pages
  - Backend: Render

## Demo

- Frontend: [https://fadlyhts.github.io/klasifikasistuntingbalita/](https://fadlyhts.github.io/klasifikasistuntingbalita/)
- Backend API: [https://klasifikasistuntingbalita.onrender.com](https://klasifikasistuntingbalita.onrender.com)

## Cara Penggunaan

1. Buka aplikasi melalui link di atas
2. Isi form dengan data balita:
   - Jenis Kelamin
   - Berat Badan Lahir (kg)
   - Tinggi Badan Lahir (cm)
   - Berat Badan Saat Ini (kg)
   - Tinggi Badan Saat Ini (cm)
   - Z-Score BB/U
   - Z-Score TB/U
   - Z-Score BB/TB
3. Klik tombol "Prediksi Status"
4. Hasil klasifikasi akan ditampilkan

## Setup Local Development

1. Clone repository ini
2. Install dependencies dengan menjalankan perintah `pip install -r requirements.txt`
3. Jalankan aplikasi dengan perintah `flask run`
4. Buka browser dan akses `http://localhost:5000` untuk melihat aplikasi

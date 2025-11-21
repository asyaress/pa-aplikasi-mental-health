# 🧠 Aplikasi Pemantauan Kesejahteraan Mental Berbasis WHO-5

Repositori ini merupakan tempat pengumpulan *Program, Flowchart, dan Laporan* untuk proyek aplikasi  
**“Pemantauan Kesejahteraan Mental (Mental Health) Berbasis Check-in Harian WHO-5 Well-Being Index”**  
oleh **Kelompok 1 – “BERPASRAH KEPADA YANG MAHA KUASA”** pada mata kuliah **Algoritma Pemrograman Dasar**.

---

## 🎯 Gambaran Umum Aplikasi

Aplikasi ini digunakan untuk memantau kesejahteraan mental pasien/ pengguna secara berkala melalui:

- **Check-in harian** berisi 5 pertanyaan dengan skala Likert (0–5).
- Pertanyaan disesuaikan dengan **profil pengguna** (mahasiswa, pekerja, dll.).
- Skor harian dikonversi menjadi **kategori warna**:
  - 🟥 **Merah** – risiko tinggi
  - 🟧 **Oranye** – perlu perhatian
  - 🟨 **Kuning** – cukup baik
  - 🟩 **Hijau** – baik

Data mingguan dapat dipantau oleh dokter untuk melihat tren kondisi mental pasien.

---

## 👥 Peran Pengguna

### 1. Dokter (Admin)
- Mendaftarkan dan mengelola data pasien (biodata, akun login).
- Menentukan **jenis pertanyaan** sesuai kategori pasien  
  (misalnya: mahasiswa, pekerja, ibu rumah tangga, dll.).
- Melihat rekap:
  - Skor harian dan mingguan.
  - Jumlah hari dengan kategori Merah/Oranye/Kuning/Hijau.
- Menggunakan data sebagai bahan **evaluasi dan kesimpulan klinis awal**.

### 2. Pasien (User)
- Login ke aplikasi setiap hari.
- Menjawab **5 pertanyaan singkat** terkait kesejahteraan mental, misalnya:  
  *“Hari ini seberapa sering kamu merasa ceria saat di kampus?”*
- Mendapatkan ringkasan sederhana:
  - Skor hari itu.
  - Kategori warna (Merah–Hijau).

---

## ⚙️ Fitur Utama

- **Manajemen Akun & Data Pasien**
  - Registrasi pasien oleh dokter.
  - Penyimpanan biodata dan tipe responden (kuliah, pekerja, dll.).

- **Bank Pertanyaan WHO-5 yang Dimodifikasi**
  - Pertanyaan dasar mengacu pada *WHO-5 Well-Being Index*.
  - Kalimat disesuaikan dengan konteks (kampus/kerja) tanpa mengubah makna inti.

- **Check-in Harian**
  - 5 pertanyaan per hari.
  - Skala Likert 0–5 (0 = tidak pernah, 5 = selalu).

- **Perhitungan Skor & Kategori Warna**
  - Total skor harian dari 5 pertanyaan.
  - Konversi otomatis ke kategori warna (Merah/Oranye/Kuning/Hijau).

- **Laporan Mingguan Dokter**
  - Rekap jumlah hari tiap kategori warna.
  - Grafik/ tabel sederhana untuk melihat tren kesejahteraan mental pasien.

---

## 🎨 Desain UI/UX

Desain antarmuka aplikasi dapat dilihat melalui tautan Figma berikut:

- 📱 **Mobile**: [PA-APD Mobile](https://www.figma.com/design/qef0m1pZXYzzHfbgdzuSdN/PA-APD-mobile?node-id=0-1&t=3AOqCCryGQMcbRSG-1)
- 🖥️ **Desktop (User)**: [PA-APD Desktop](https://www.figma.com/design/PpICwarNo84K6lQsx3sHDB/PA-APD-Desktop?node-id=0-1&t=MkEHdRuSOvcA0J1E-1)
- 🧑‍⚕️ **Admin (Dokter)**: [PA-APD Admin](https://www.figma.com/design/b4cqmvL1THnddhFkLdieir/PA-APD-Admin?node-id=0-1&t=jRTtFUjlImlEM5SI-1)

---
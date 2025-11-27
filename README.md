# 🧠 Aplikasi Pemantauan Kesejahteraan Mental Berbasis WHO-5

Repositori ini berisi **source code, flowchart, dan laporan** untuk proyek aplikasi  
**“Pemantauan Kesejahteraan Mental (Mental Health) Berbasis Check-in Harian WHO-5 Well-Being Index”**  
oleh **Kelompok 1 – “BERPASRAH KEPADA YANG MAHA KUASA”**  
pada mata kuliah **Algoritma Pemrograman Dasar**.

Aplikasi ini dibuat dengan **Python (Tkinter + CustomTkinter)** dan menyimpan data dalam bentuk **file JSON**  
(bukan database SQL).

---

## 🎯 Gambaran Umum Aplikasi

Aplikasi digunakan untuk memantau kesejahteraan mental pasien/pengguna secara berkala melalui:

- **Check-in harian** berisi 5 pertanyaan dengan skala Likert (0–5).
- Pertanyaan disesuaikan dengan **profil pengguna** (mahasiswa, pekerja, dll.).
- Skor harian dikonversi menjadi **kategori warna**:
  - 🟥 **Merah** – risiko tinggi
  - 🟧 **Oranye** – perlu perhatian
  - 🟨 **Kuning** – cukup baik
  - 🟩 **Hijau** – baik
- Dokter/admin dapat memantau:
  - Tren skor WHO-5 dari waktu ke waktu.
  - Rekap kategori harian dalam periode tertentu.
  - Data biodata dan riwayat check-in pasien.

Semua logika aplikasi berjalan di sisi **desktop** (Python GUI), bukan aplikasi web.

---

## 👥 Role & Cara Akses

Role pengguna diatur melalui `data/users.json` dan `data/roles.json`. Saat ini ada **3 peran utama**:

### 1. 🛠 Admin

- Login via **aplikasi desktop** (menu Dokter/Admin dari halaman awal).
- Fitur utama:
  - Mengelola data **user & role**.
  - Mengelola **data pasien** (biodata + akun login).
  - Mengelola **data dokter**.
  - Mengelola **set pertanyaan** (`set_pertanyaan.json`) dan **item pertanyaan** (`item_pertanyaan.json`).

UI admin di-handle oleh package:

```text
admin/
  ├─ app.py              # AdminApp: main window untuk dashboard admin
  ├─ config.py           # Konfigurasi tampilan (judul window, warna, ukuran)
  ├─ core/
  │   └─ datastore.py    # Helper baca/tulis JSON + bentuk data tabel
  ├─ layout.py           # Sidebar + action bar (komponen UI reusable)
  ├─ pasien/             # Modul tabel & form CRUD pasien
  ├─ dokter/             # Modul tabel & form CRUD dokter
  ├─ questions/          # Modul tabel & form CRUD pertanyaan
  └─ roles/              # Modul tabel & form CRUD role
```

### 2. 👨‍⚕️ Dokter

- Login melalui **aplikasi desktop**, diarahkan ke **Dashboard Dokter** (bukan admin).
- Package utama:

```text
dokter/
  └─ ... (dashboard dokter, list pasien, lihat detail & grafik WHO-5)
```

- Fitur (secara garis besar):
  - Melihat **list pasien** yang diasosiasikan dengan dokter tersebut.
  - Melihat **detail pasien** (biodata + diagnosa).
  - Melihat **riwayat skor WHO-5** dalam bentuk **grafik line** (Matplotlib).
  - Membaca riwayat check-in pasien dari `data/jawaban_harian.json`.

### 3. 🙂 Pasien

- Menggunakan **aplikasi bergaya mobile** (tetap GUI desktop, layout mirip mobile).
- Kode terkait pasien ada di:

```text
loginmobile/   # Halaman login pasien
pasien/        # Dashboard & flow check-in WHO-5
```

- Fitur:
  - Login dengan username & password yang dibuatkan oleh dokter/admin.
  - Melakukan **check-in harian** (5 pertanyaan WHO-5 yang dimodifikasi).
  - Mendapatkan ringkasan:
    - Skor hari itu.
    - Kategori warna (Merah–Hijau).

---

## ⚙️ Fitur Utama (Sesuai Kode di Repo)

### 🔐 1. Sistem Login & Role

**Backend autentikasi** diatur oleh:

- `auth.py`  
  Mengatur:
  - Baca user dari `data/users.json`.
  - Baca role dari `data/roles.json`.
  - Mapping user → dokter/pasien lewat:
    - `data/dokter.json`
    - `data/pasien.json`
  - Menambah field tambahan ke objek user saat login:
    - `role_name`
    - `nama`, `spesialis`, `id_dokter` (kalau dokter)
    - `nama`, `id_pasien`, `id_dokter`, `jenis_kelamin`, dll. (kalau pasien)
    - `nama = "Administrator"` (kalau admin)

Untuk login **desktop (dokter/admin)**:

```text
logindesktop/
  ├─ app.py                    # Window login desktop
  └─ mixins_desktop_login.py   # DesktopLoginLogicMixin (logika login & redirect)
```

- `DesktopLoginLogicMixin`:
  - Cek username & password via `AuthBackend`.
  - Kalau sukses:
    - Kalau role = 1 → panggil `open_admin_dashboard(...)`.
    - Kalau role = 2 → panggil `open_dokter_dashboard(...)`.
    - Kalau role = 3 → panggil `open_pasien_dashboard(...)` (jika dihubungkan).

Untuk login **“mobile style” pasien**:

```text
loginmobile/
  └─ app_flexible.py (dan file terkait)
```

- Menangani tampilan login dan routing ke dashboard pasien.

---

### 🧑‍💼 2. Dashboard Admin

Class utama:

- `admin/app.py` → `class AdminApp`

Fitur utama AdminApp:

- Menggunakan **CustomTkinter**:
  - Sidebar biru (menu: _Pasien, Dokter, Questions, Role_).
  - ActionBar (search, tombol tambah).
  - `CTkScrollableFrame` untuk tabel data.

Data yang dikelola:

- Pasien → `data/pasien.json`
- Dokter → `data/dokter.json`
- Role → `data/roles.json`
- Pertanyaan → `data/item_pertanyaan.json` & `data/set_pertanyaan.json`

Struktur modul CRUD:

```text
admin/pasien/
  ├─ pasien_table.py     # Render tabel pasien (read & edit/delete trigger)
  └─ pasien_add_form.py  # Form tambah/edit pasien

admin/dokter/
  ├─ dokter_table.py
  └─ dokter_add_form.py

admin/questions/
  ├─ question_table.py
  └─ question_add_form.py

admin/roles/
  ├─ role_table.py
  └─ role_add_form.py
```

`admin/core/datastore.py` berisi fungsi helper seperti:

- `load_patients_for_table()`
- `load_doctors_for_table()`
- `load_question_sets()`
- `load_questions_for_table(...)`
- `load_roles_for_table()`

Yang akan mengubah raw JSON → data yang siap untuk dirender di tabel.

---

### 👨‍⚕️ 3. Dashboard Dokter

Dokter login lewat **desktop login**, lalu diarahkan ke modul di `dokter/`.

Secara garis besar:

- Menampilkan list pasien yang berelasi dengan dokter tertentu (via `id_dokter`).
- Saat klik salah satu pasien → panggil `PatientDetailMixin.view_detail(...)` (di salah satu file dokter).
- `PatientDetailMixin`:
  - Buka `CTkToplevel` berisi:
    - Panel kiri: biodata pasien.
    - Panel kanan: grafik riwayat skor WHO-5.
  - Data diambil dari `data/jawaban_harian.json` dengan filter `id_pasien`.

Grafik dibuat dengan:

- `matplotlib.figure.Figure`
- `FigureCanvasTkAgg` untuk embed di CustomTkinter.

---

### 📱 4. Flow Aplikasi Pasien (Check-in Harian)

Untuk pasien:

- Setelah login via folder `loginmobile`, user diarahkan ke flow di folder `pasien/`.
- Pengguna akan:
  - Menjawab 5 pertanyaan (WHO-5 versi dimodifikasi).
  - Pilih skor 0–5 (misalnya dengan tombol atau radio button).
- Aplikasi akan:
  - Hitung total skor.
  - Konversi ke **persentase**.
  - Mapping ke kategori (misal: Memadai / Rendah / Berisiko → warna hijau/kuning/merah).
  - Simpan hasil ke `data/jawaban_harian.json` dengan struktur:
    - `id_pasien`
    - `tanggal`
    - `total_score`
    - `total_percentage`
    - `kategori` (atau serupa, tergantung kode paling akhir).

---

## 📂 Struktur Folder (Ringkas)

Struktur utama (versi ringkas dan relevan):

```text
pa-aplikasi-mental-health/
├─ main.py                # Landing page: pilih login Pasien atau Dokter/Admin
├─ auth.py                # AuthBackend: autentikasi & mapping role
├─ data/
│  ├─ users.json
│  ├─ pasien.json
│  ├─ dokter.json
│  ├─ roles.json
│  ├─ item_pertanyaan.json
│  ├─ set_pertanyaan.json
│  └─ jawaban_harian.json
├─ loginmobile/           # Login & UI style mobile untuk pasien
├─ logindesktop/          # Login desktop untuk dokter/admin
├─ admin/                 # Dashboard admin: CRUD pasien, dokter, role, pertanyaan
├─ dokter/                # Dashboard dokter: monitor pasien & grafik WHO-5
├─ pasien/                # Flow check-in WHO-5 & tampilan pasien
└─ README.md
```

> Beberapa file/folder `backup/` masih disertakan sebagai arsip versi lama dan **bukan** flow utama.

---

## 🎨 Desain UI/UX (Figma)

Desain tampilan aplikasi (sebagai acuan layout) dapat dilihat di:

- 📱 **Mobile (Pasien)**  
  PA-APD Mobile  
  <https://www.figma.com/design/qef0m1pZXYzzHfbgdzuSdN/PA-APD-mobile?node-id=0-1>

- 🖥️ **Desktop (User)**  
  PA-APD Desktop  
  <https://www.figma.com/design/PpICwarNo84K6lQsx3sHDB/PA-APD-Desktop?node-id=0-1>

- 🧑‍⚕️ **Admin (Dokter/Admin)**  
  PA-APD Admin  
  <https://www.figma.com/design/b4cqmvL1THnddhFkLdieir/PA-APD-Admin?node-id=0-1>

---

## 🚀 Cara Menjalankan Aplikasi

1. **Clone repository**

   ```bash
   git clone https://github.com/asyaress/pa-aplikasi-mental-health.git
   cd pa-aplikasi-mental-health
   ```

2. **Install dependency Python**

   Minimal:

   ```bash
   pip install customtkinter matplotlib
   ```

   > Jika ada modul lain yang belum ter-install, Python akan menampilkan error di terminal.  
   > Cukup `pip install <nama_modul>` sesuai pesan error.

3. **Jalankan aplikasi utama**

   ```bash
   python main.py
   ```

   - Akan muncul **landing window**.
   - Pilih:
     - **Login Pasien (Mobile)** → masuk ke flow pasien.
     - **Login Dokter / Admin (Desktop)** → masuk ke login desktop.
       - Kalau role user = Admin → buka AdminApp (dashboard admin).
       - Kalau role user = Dokter → buka dashboard dokter.

---

## 📝 Catatan Penting

- Proyek ini dibuat untuk **keperluan akademik** (tugas Algoritma dan Pemrograman Dasar).
- Interpretasi skor WHO-5 di aplikasi ini **bukan** pengganti diagnosis profesional.
- Flow, struktur data, dan tampilan UI masih dapat dikembangkan lebih lanjut (misalnya migrasi ke database atau web app).

---

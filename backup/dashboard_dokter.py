import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json
import os
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class dokterDashboard:
    def __init__(self, user, on_logout=None):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("dashboard dokter ni kids")
        self.window.geometry("1200x700")
        self.window.configure(fg_color="#f8f9fa")

        self.user = user
        self.on_logout = on_logout  # sekarang ini datang dari parameter

        self.data_folder = "data"

        self.patients_data = self.load_patients_for_current_doctor()

        self.build_ui()

    # --- Helper baca file JSON di folder data ---
    def load_json(self, filename):
        filepath = os.path.join(self.data_folder, filename)

        try:
            if not os.path.exists(filepath):
                print(f"File {filepath} tidak ditemukan")
                return []

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data

        except json.JSONDecodeError:
            print(f"Format JSON {filepath} tidak valid")
            return []
        except Exception as e:
            print(f"Error baca file {filepath}: {e}")
            return []

    def save_json(self, filename, data):
        filepath = os.path.join(self.data_folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error nulis file {filepath}: {e}")

    # --- Ambil pasien sesuai dokter yang login ---
    def load_patients_for_current_doctor(self):
        id_dokter = self.user.get("id_dokter")
        print("ID dokter saat ini:", id_dokter)

        all_pasien = self.load_json("pasien.json")
        all_jawaban = self.load_json("jawaban_harian.json")

        patients_rows = []

        for p in all_pasien:
            if p.get("id_dokter") != id_dokter:
                continue

            nama = p.get("nama", "-")
            diagnosa = p.get("diagnosa", "-")
            jenis = p.get("pekerjaan", p.get("pendidikan", "-"))

            # ambil semua jawaban harian pasien ini
            related = [j for j in all_jawaban if j.get("id_pasien") == p.get("id")]

            # kategori WHO-5 terakhir (kalau ada)
            kategori = "-"
            if related:
                related.sort(key=lambda x: x.get("tanggal", ""))
                last = related[-1]
                kategori = last.get("kategori", "-")

            # hitung progress 2 minggu: berapa kali check-in (max 14)
            total_checkin = len(related)
            progress_label = f"{total_checkin}/14"
            selesai_2minggu = total_checkin >= 14

            tanggal_konsul = p.get("tanggal_konsul", "")

            patients_rows.append(
                {
                    "id_pasien": p.get("id"),
                    "nama": nama,
                    "diagnosa": diagnosa,
                    "jenis": jenis,
                    "kategori": kategori,
                    "detail": p,  # objek pasien lengkap dari JSON
                    "total_checkin": total_checkin,
                    "progress_label": progress_label,
                    "selesai_2minggu": selesai_2minggu,
                    "tanggal_konsul": tanggal_konsul,
                }
            )

        return patients_rows

    def build_ui(self):
        # 1. Sidebar (Kiri)
        self.sidebar = ctk.CTkFrame(
            self.window, fg_color="#ffffff", width=65, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        # Menu Sidebar
        ctk.CTkLabel(
            self.sidebar, text="♾️", font=("Arial", 30), text_color="#007bff"
        ).pack(pady=(30, 20))
        ctk.CTkButton(
            self.sidebar,
            text="➕",
            width=50,
            height=50,
            text_color="#000000",
            fg_color="#ffffff",
            hover_color="#0e98f5",
            corner_radius=10,
            command=self.open_create_patient_window,
        ).pack(pady=10)

        # Tombol Logout di bagian bawah sidebar
        self.logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            width=60,
            height=32,
            fg_color="#fecaca",
            text_color="#b91c1c",
            hover_color="#fca5a5",
            corner_radius=10,
            command=self.logout,
        )
        self.logout_button.pack(side="bottom", pady=20)

        # menus = ["🏠", "🗓", "💬", "⏱", "⚙️", "↩️"]
        # for icon in menus:
        #     label = ctk.CTkButton(
        #         self.sidebar,
        #         text=icon,
        #         font=("Arial", 20),
        #         text_color="#000000",
        #         fg_color="transparent",
        #         hover_color="#0e98f5",
        #         width=50,
        #         height=50,
        #         corner_radius=10,
        #     )
        #     label.pack(pady=18)

        # 2. Main Content (Kanan)
        self.main_content = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # # 3. ACTION BAR (Wadah untuk Search dan Ikon Aksi)
        # self.action_bar = ctk.CTkFrame(
        #     self.main_content, fg_color="#ffffff", height=60, corner_radius=10
        # )
        # self.action_bar.pack(side="top", fill="x", pady=5, padx=15)

        # # 3a. Bagian Kiri (Search)
        # self.left_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        # self.left_action.pack(side="left", padx=15, pady=10, fill="y")

        # self.search_entry = ctk.CTkEntry(
        #     self.left_action,
        #     placeholder_text="🔍 Cari Pasien...",
        #     width=250,
        #     height=35,
        #     border_width=1,
        #     border_color="#ddd",
        #     fg_color="#f9f9f9",
        # )
        # self.search_entry.pack(side="left")
        # self.search_entry.bind("<Return>", self.enter_pressed)

        # # Tambahkan label "4 Terpilih"
        # ctk.CTkLabel(
        #     self.left_action,
        #     text="4 Terpilih",
        #     text_color="#3B8ED0",
        #     font=("Arial Bold", 12),
        # ).pack(side="left", padx=15)

        # # 3b. Bagian Kanan (Icons Aksi)
        # right_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        # right_action.pack(side="right", padx=15, fill="y")

        # ctk.CTkLabel(
        #     right_action, text="1 - 10 of 52", text_color="#555", font=("Arial", 12)
        # ).pack(side="left", padx=(0, 15))
        # ctk.CTkLabel(
        #     right_action, text="< >", text_color="#555", font=("Arial Bold", 14)
        # ).pack(side="left", padx=(0, 15))

        # # Tombol Aksi tanpa Lambda
        # def create_action_handler(icon_text):
        #     def handler():
        #         print(f"Aksi {icon_text} ditekan")

        #     return handler

        # for ic in ["Y", "🖨️", "⬇️", "⤢"]:
        #     ctk.CTkButton(
        #         right_action,
        #         text=ic,
        #         width=35,
        #         height=35,
        #         fg_color="transparent",
        #         text_color="#555",
        #         hover_color="#eee",
        #         font=("Arial", 16),
        #         command=create_action_handler(ic),
        #     ).pack(side="left", padx=2),

        # 4. Scrollable Frame untuk Tabel
        self.table_scroll_frame = ctk.CTkScrollableFrame(
            self.main_content, fg_color="#ffffff", corner_radius=10
        )
        self.table_scroll_frame.pack(side="top", fill="both", expand=True, pady=(0, 0))

        # Tabel
        self.render_table(self.patients_data)

    def open_create_patient_window(self):
        # Window popup
        win = ctk.CTkToplevel(self.window)
        win.title("Tambah Pasien Baru")
        win.geometry("600x750")
        win.grab_set()  # fokus ke window ini dulu
        self.create_patient_window = win

        # Frame luar (background abu2 terang)
        outer_frame = ctk.CTkFrame(win, fg_color="#f8f9fa")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable frame (ada scrollbar otomatis kalau konten kepanjangan)
        scroll_frame = ctk.CTkScrollableFrame(
            outer_frame,
            fg_color="#ffffff",
            corner_radius=10,
        )
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        frame = scroll_frame  # biar nama variabel tetap 'frame' di bawah

        # Judul
        title = ctk.CTkLabel(
            frame,
            text="Tambah Pasien Baru",
            font=("Arial Bold", 20),
            text_color="#111827",
        )
        title.pack(pady=(10, 20))

        # helper bikin entry + label
        def add_labeled_entry(parent, label_text, show=None):
            lbl = ctk.CTkLabel(
                parent,
                text=label_text,
                font=("Arial", 12),
                text_color="#4b5563",
            )
            lbl.pack(anchor="w", padx=10, pady=(5, 0))

            ent = ctk.CTkEntry(
                parent,
                height=32,
                show=show,
            )
            ent.pack(fill="x", padx=10, pady=(0, 5))

            return ent

        # --- Data login pasien ---
        self.new_username_entry = add_labeled_entry(frame, "Username Login Pasien")
        self.new_password_entry = add_labeled_entry(
            frame,
            "Password Login Pasien",
            show="*",
        )

        # --- Biodata ---
        self.new_name_entry = add_labeled_entry(frame, "Nama Lengkap")

        # Jenis kelamin pakai option menu
        ctk.CTkLabel(
            frame,
            text="Jenis Kelamin",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.new_gender_option = ctk.CTkOptionMenu(
            frame,
            values=["Pilih Jenis Kelamin", "Laki-laki", "Perempuan"],
            height=32,
        )
        self.new_gender_option.set("Pilih Jenis Kelamin")
        self.new_gender_option.pack(fill="x", padx=10, pady=(0, 5))

        # ⬇⬇⬇ TANGGAL LAHIR: 3 INPUT (TANGGAL, BULAN, TAHUN) ⬇⬇⬇
        ctk.CTkLabel(
            frame,
            text="Tanggal Lahir",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        birth_frame = ctk.CTkFrame(frame, fg_color="transparent")
        birth_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.birth_day_entry = ctk.CTkEntry(
            birth_frame,
            width=70,
            placeholder_text="HH",  # Hari
            height=32,
        )
        self.birth_day_entry.pack(side="left")

        self.birth_month_entry = ctk.CTkEntry(
            birth_frame,
            width=70,
            placeholder_text="BB",  # Bulan
            height=32,
        )
        self.birth_month_entry.pack(side="left", padx=5)

        self.birth_year_entry = ctk.CTkEntry(
            birth_frame,
            width=100,
            placeholder_text="TTTT",  # Tahun
            height=32,
        )
        self.birth_year_entry.pack(side="left")

        # ⬇⬇⬇ PENDIDIKAN: OPTION MENU ⬇⬇⬇
        ctk.CTkLabel(
            frame,
            text="Pendidikan",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.new_education_option = ctk.CTkOptionMenu(
            frame,
            values=[
                "Pilih Pendidikan",
                "Tidak Sekolah",
                "SD/Sederajat",
                "SMP/Sederajat",
                "SMA/Sederajat",
                "Perguruan Tinggi",
            ],
            height=32,
        )
        self.new_education_option.set("Pilih Pendidikan")
        self.new_education_option.pack(fill="x", padx=10, pady=(0, 5))

        # ⬇⬇⬇ PEKERJAAN: OPTION MENU ⬇⬇⬇
        ctk.CTkLabel(
            frame,
            text="Pekerjaan",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.new_job_option = ctk.CTkOptionMenu(
            frame,
            values=[
                "Pilih Pekerjaan",
                "PNS",
                "Pegawai Swasta",
                "Wiraswasta",
                "Buruh",
                "Petani",
                "Ibu Rumah Tangga",
                "Tidak Bekerja",
            ],
            height=32,
        )
        self.new_job_option.set("Pilih Pekerjaan")
        self.new_job_option.pack(fill="x", padx=10, pady=(0, 5))

        # Alamat pakai Textbox
        ctk.CTkLabel(
            frame,
            text="Alamat",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.new_address_text = ctk.CTkTextbox(
            frame,
            height=80,
        )
        self.new_address_text.pack(fill="x", padx=10, pady=(0, 5))

        self.new_phone_entry = add_labeled_entry(frame, "No. HP")
        self.new_diagnosa_entry = add_labeled_entry(frame, "Diagnosa")

        # Tombol simpan
        btn_save = ctk.CTkButton(
            frame,
            text="Simpan Pasien",
            height=36,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.submit_new_patient,
        )
        btn_save.pack(fill="x", padx=10, pady=(15, 5))

        # Tombol batal
        btn_cancel = ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        )
        btn_cancel.pack(fill="x", padx=10, pady=(0, 10))

    def open_edit_patient_window(self, row_data):
        pasien = row_data.get("detail", {})
        self.editing_pasien_id = row_data.get("id_pasien")

        win = ctk.CTkToplevel(self.window)
        win.title(f"Edit Pasien - {pasien.get('nama', '-')}")
        win.geometry("600x750")
        win.grab_set()
        self.edit_patient_window = win

        outer_frame = ctk.CTkFrame(win, fg_color="#f8f9fa")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scroll_frame = ctk.CTkScrollableFrame(
            outer_frame,
            fg_color="#ffffff",
            corner_radius=10,
        )
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        frame = scroll_frame

        # Judul
        ctk.CTkLabel(
            frame,
            text="Edit Data Pasien",
            font=("Arial Bold", 20),
            text_color="#111827",
        ).pack(pady=(10, 20))

        # helper label+entry
        def add_labeled_entry(parent, label_text, initial_value="", show=None):
            lbl = ctk.CTkLabel(
                parent,
                text=label_text,
                font=("Arial", 12),
                text_color="#4b5563",
            )
            lbl.pack(anchor="w", padx=10, pady=(5, 0))

            ent = ctk.CTkEntry(
                parent,
                height=32,
                show=show,
            )
            ent.pack(fill="x", padx=10, pady=(0, 5))

            if initial_value:
                ent.insert(0, initial_value)

            return ent

        # --- Nama ---
        self.edit_name_entry = add_labeled_entry(
            frame,
            "Nama Lengkap",
            pasien.get("nama", ""),
        )

        # --- Jenis Kelamin ---
        ctk.CTkLabel(
            frame,
            text="Jenis Kelamin",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.edit_gender_option = ctk.CTkOptionMenu(
            frame,
            values=["Laki-laki", "Perempuan"],
            height=32,
        )
        gender_val = pasien.get("jenis_kelamin", "Laki-laki")
        if gender_val not in ["Laki-laki", "Perempuan"]:
            gender_val = "Laki-laki"
        self.edit_gender_option.set(gender_val)
        self.edit_gender_option.pack(fill="x", padx=10, pady=(0, 5))

        # --- Tanggal Lahir (parse yyyy-mm-dd) ---
        ctk.CTkLabel(
            frame,
            text="Tanggal Lahir",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        birth_frame = ctk.CTkFrame(frame, fg_color="transparent")
        birth_frame.pack(fill="x", padx=10, pady=(0, 5))

        tgl = pasien.get("tanggal_lahir") or ""
        year_val = month_val = day_val = ""
        if len(tgl.split("-")) == 3:
            year_val, month_val, day_val = tgl.split("-")

        self.edit_birth_day_entry = ctk.CTkEntry(
            birth_frame,
            width=70,
            placeholder_text="HH",
            height=32,
        )
        self.edit_birth_day_entry.pack(side="left")
        if day_val:
            self.edit_birth_day_entry.insert(0, day_val)

        self.edit_birth_month_entry = ctk.CTkEntry(
            birth_frame,
            width=70,
            placeholder_text="BB",
            height=32,
        )
        self.edit_birth_month_entry.pack(side="left", padx=5)
        if month_val:
            self.edit_birth_month_entry.insert(0, month_val)

        self.edit_birth_year_entry = ctk.CTkEntry(
            birth_frame,
            width=100,
            placeholder_text="TTTT",
            height=32,
        )
        self.edit_birth_year_entry.pack(side="left")
        if year_val:
            self.edit_birth_year_entry.insert(0, year_val)

        # --- Pendidikan ---
        ctk.CTkLabel(
            frame,
            text="Pendidikan",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        education_values = [
            "Tidak Sekolah",
            "SD/Sederajat",
            "SMP/Sederajat",
            "SMA/Sederajat",
            "Perguruan Tinggi",
        ]

        self.edit_education_option = ctk.CTkOptionMenu(
            frame,
            values=education_values,
            height=32,
        )
        edu_val = pasien.get("pendidikan", "SMA/Sederajat")
        if edu_val not in education_values:
            edu_val = "SMA/Sederajat"
        self.edit_education_option.set(edu_val)
        self.edit_education_option.pack(fill="x", padx=10, pady=(0, 5))

        # --- Pekerjaan ---
        ctk.CTkLabel(
            frame,
            text="Pekerjaan",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        job_values = [
            "PNS",
            "Pegawai Swasta",
            "Wiraswasta",
            "Buruh",
            "Petani",
            "Ibu Rumah Tangga",
            "Tidak Bekerja",
        ]

        self.edit_job_option = ctk.CTkOptionMenu(
            frame,
            values=job_values,
            height=32,
        )
        job_val = pasien.get("pekerjaan", "Tidak Bekerja")
        if job_val not in job_values:
            job_val = "Tidak Bekerja"
        self.edit_job_option.set(job_val)
        self.edit_job_option.pack(fill="x", padx=10, pady=(0, 5))

        # --- Alamat ---
        ctk.CTkLabel(
            frame,
            text="Alamat",
            font=("Arial", 12),
            text_color="#4b5563",
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.edit_address_text = ctk.CTkTextbox(
            frame,
            height=80,
        )
        self.edit_address_text.pack(fill="x", padx=10, pady=(0, 5))
        if pasien.get("alamat"):
            self.edit_address_text.insert("1.0", pasien.get("alamat"))

        # --- No HP ---
        self.edit_phone_entry = add_labeled_entry(
            frame,
            "No. HP",
            pasien.get("no_hp", ""),
        )

        # --- Diagnosa ---
        self.edit_diagnosa_entry = add_labeled_entry(
            frame,
            "Diagnosa (opsional)",
            pasien.get("diagnosa", ""),
        )

        # Tombol simpan
        ctk.CTkButton(
            frame,
            text="Simpan Perubahan",
            height=36,
            fg_color="#22c55e",
            hover_color="#16a34a",
            command=self.submit_edit_patient,
        ).pack(fill="x", padx=10, pady=(15, 5))

        # Tombol batal
        ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        ).pack(fill="x", padx=10, pady=(0, 10))

    def open_set_konsul_window(self, row_data):
        pasien = row_data.get("detail", {})
        id_pasien = row_data.get("id_pasien")
        existing_date = pasien.get("tanggal_konsul") or ""

        win = ctk.CTkToplevel(self.window)
        win.title(f"Atur Tanggal Konsul - {pasien.get('nama', '-')}")
        win.geometry("400x250")
        win.grab_set()
        self.konsul_window = win
        self.konsul_for_id = id_pasien

        frame = ctk.CTkFrame(win, fg_color="#ffffff", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Pilih Tanggal Konsultasi",
            font=("Arial Bold", 18),
            text_color="#111827",
        ).pack(pady=(10, 20))

        date_frame = ctk.CTkFrame(frame, fg_color="transparent")
        date_frame.pack(pady=(0, 10))

        # default ke hari ini
        today = datetime.date.today()
        def_day = today.day
        def_month = today.month
        def_year = today.year

        # kalau sudah ada tanggal_konsul, pakai itu
        if len(existing_date.split("-")) == 3:
            try:
                y, m, d = existing_date.split("-")
                def_year = int(y)
                def_month = int(m)
                def_day = int(d)
            except ValueError:
                pass

        day_values = [f"{i:02d}" for i in range(1, 32)]
        month_values = [f"{i:02d}" for i in range(1, 13)]
        year_values = [str(def_year + i) for i in range(0, 3)]  # tahun ini + 2 tahun

        self.konsul_day_option = ctk.CTkOptionMenu(
            date_frame,
            values=day_values,
            width=80,
        )
        self.konsul_day_option.set(f"{def_day:02d}")
        self.konsul_day_option.pack(side="left", padx=5)

        self.konsul_month_option = ctk.CTkOptionMenu(
            date_frame,
            values=month_values,
            width=80,
        )
        self.konsul_month_option.set(f"{def_month:02d}")
        self.konsul_month_option.pack(side="left", padx=5)

        self.konsul_year_option = ctk.CTkOptionMenu(
            date_frame,
            values=year_values,
            width=100,
        )
        self.konsul_year_option.set(str(def_year))
        self.konsul_year_option.pack(side="left", padx=5)

        # Tombol simpan
        ctk.CTkButton(
            frame,
            text="Simpan Tanggal Konsul",
            height=36,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.submit_konsul_date,
        ).pack(fill="x", padx=10, pady=(15, 5))

        ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        ).pack(fill="x", padx=10, pady=(0, 10))

    def submit_konsul_date(self):
        if not hasattr(self, "konsul_for_id"):
            messagebox.showerror("Error", "Data pasien tidak ditemukan.")
            return

        day = self.konsul_day_option.get()
        month = self.konsul_month_option.get()
        year = self.konsul_year_option.get()

        # validasi sederhana
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            messagebox.showerror(
                "Error",
                "Tanggal konsultasi tidak valid.",
            )
            return

        try:
            # cek apakah tanggal bener (28/29/30/31 dsb)
            datetime.date(int(year), int(month), int(day))
        except ValueError:
            messagebox.showerror(
                "Error",
                "Tanggal konsultasi tidak valid.",
            )
            return

        tanggal_konsul = f"{year}-{month}-{day}"

        pasien_list = self.load_json("pasien.json")
        updated = False

        for p in pasien_list:
            if p.get("id") == self.konsul_for_id:
                p["tanggal_konsul"] = tanggal_konsul
                updated = True
                break

        if not updated:
            messagebox.showerror("Error", "Pasien tidak ditemukan di database.")
            return

        self.save_json("pasien.json", pasien_list)

        messagebox.showinfo(
            "Berhasil",
            f"Tanggal konsultasi disimpan: {tanggal_konsul}",
        )

        # tutup window
        if hasattr(self, "konsul_window"):
            self.konsul_window.destroy()

        # refresh tabel
        self.patients_data = self.load_patients_for_current_doctor()
        self.render_table(self.patients_data)

    def submit_new_patient(self):
        # Ambil nilai dari form
        username = (self.new_username_entry.get() or "").strip()
        password = (self.new_password_entry.get() or "").strip()
        nama = (self.new_name_entry.get() or "").strip()
        jenis_kelamin = self.new_gender_option.get()

        # Tanggal lahir: 3 input (hari, bulan, tahun)
        day = (self.birth_day_entry.get() or "").strip()
        month = (self.birth_month_entry.get() or "").strip()
        year = (self.birth_year_entry.get() or "").strip()

        alamat = (self.new_address_text.get("1.0", "end") or "").strip()
        no_hp = (self.new_phone_entry.get() or "").strip()
        diagnosa = (self.new_diagnosa_entry.get() or "").strip()

        # Pendidikan & pekerjaan dari OptionMenu
        pendidikan = self.new_education_option.get()
        pekerjaan = self.new_job_option.get()

        # --- VALIDASI ---
        if not username or not password or not nama:
            messagebox.showerror(
                "Error",
                "Username, password, dan nama pasien wajib diisi.",
            )
            return

        if jenis_kelamin == "Pilih Jenis Kelamin":
            messagebox.showerror("Error", "Silakan pilih jenis kelamin pasien.")
            return

        if pendidikan == "Pilih Pendidikan":
            messagebox.showerror("Error", "Silakan pilih pendidikan pasien.")
            return

        if pekerjaan == "Pilih Pekerjaan":
            messagebox.showerror("Error", "Silakan pilih pekerjaan pasien.")
            return

        if no_hp and not no_hp.replace("+", "").replace("-", "").isdigit():
            messagebox.showerror(
                "Error",
                "No. HP hanya boleh berisi angka, +, dan -.",
            )
            return

        # Bangun string tanggal_lahir kalau diisi
        tanggal_lahir = ""
        if day or month or year:
            # Kalau salah satu terisi, semua wajib diisi
            if not (day and month and year):
                messagebox.showerror(
                    "Error",
                    "Tanggal lahir belum lengkap. Isi hari, bulan, dan tahun.",
                )
                return

            if not (day.isdigit() and month.isdigit() and year.isdigit()):
                messagebox.showerror(
                    "Error",
                    "Tanggal lahir harus berupa angka semua.",
                )
                return

            day = day.zfill(2)
            month = month.zfill(2)
            tanggal_lahir = f"{year}-{month}-{day}"  # yyyy-mm-dd

        # --- Load data lama ---
        users = self.load_json("users.json")
        pasien_list = self.load_json("pasien.json")

        # Cek username unik
        for u in users:
            if u.get("username") == username:
                messagebox.showerror(
                    "Error",
                    "Username sudah digunakan. Silakan pilih username lain.",
                )
                return

        # Buat ID baru
        new_user_id = max([u.get("id", 0) for u in users], default=0) + 1
        new_pasien_id = max([p.get("id", 0) for p in pasien_list], default=0) + 1

        # Role 3 = Pasien
        new_user = {
            "id": new_user_id,
            "username": username,
            "password": password,
            "id_role": 3,
        }
        users.append(new_user)
        self.save_json("users.json", users)

        # id_dokter langsung dari dokter yang login
        id_dokter = self.user.get("id_dokter")

        new_pasien = {
            "id": new_pasien_id,
            "id_user": new_user_id,
            "id_dokter": id_dokter,
            "nama": nama,
            "jenis_kelamin": jenis_kelamin,
            "tanggal_lahir": tanggal_lahir,
            "pendidikan": pendidikan,
            "pekerjaan": pekerjaan,
            "alamat": alamat,
            "no_hp": no_hp,
            "diagnosa": diagnosa,
            "id_set_pertanyaan": 1,  # set WHO-5 default
            "tanggal_konsul": "",  # belum dijadwalkan
        }
        pasien_list.append(new_pasien)
        self.save_json("pasien.json", pasien_list)

        messagebox.showinfo(
            "Berhasil",
            "Data pasien baru berhasil ditambahkan.",
        )

        # Tutup window form
        if hasattr(self, "create_patient_window"):
            self.create_patient_window.destroy()

        # Refresh tabel di dashboard
        self.patients_data = self.load_patients_for_current_doctor()
        self.render_table(self.patients_data)

    def submit_edit_patient(self):
        id_pasien = getattr(self, "editing_pasien_id", None)
        if not id_pasien:
            messagebox.showerror("Error", "Data pasien yang diedit tidak ditemukan.")
            return

        nama = (self.edit_name_entry.get() or "").strip()
        jenis_kelamin = self.edit_gender_option.get()

        day = (self.edit_birth_day_entry.get() or "").strip()
        month = (self.edit_birth_month_entry.get() or "").strip()
        year = (self.edit_birth_year_entry.get() or "").strip()

        pendidikan = self.edit_education_option.get()
        pekerjaan = self.edit_job_option.get()
        alamat = (self.edit_address_text.get("1.0", "end") or "").strip()
        no_hp = (self.edit_phone_entry.get() or "").strip()
        diagnosa = (self.edit_diagnosa_entry.get() or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama pasien wajib diisi.")
            return

        if no_hp and not no_hp.replace("+", "").replace("-", "").isdigit():
            messagebox.showerror(
                "Error",
                "No. HP hanya boleh berisi angka, +, dan -.",
            )
            return

        # Build tanggal lahir
        tanggal_lahir = ""
        if day or month or year:
            if not (day and month and year):
                messagebox.showerror(
                    "Error",
                    "Tanggal lahir belum lengkap. Isi hari, bulan, dan tahun.",
                )
                return
            if not (day.isdigit() and month.isdigit() and year.isdigit()):
                messagebox.showerror(
                    "Error",
                    "Tanggal lahir harus berupa angka semua.",
                )
                return

            day = day.zfill(2)
            month = month.zfill(2)
            tanggal_lahir = f"{year}-{month}-{day}"  # yyyy-mm-dd

        # --- Load dan update pasien.json ---
        pasien_list = self.load_json("pasien.json")
        updated = False

        for p in pasien_list:
            if p.get("id") == id_pasien:
                p["nama"] = nama
                p["jenis_kelamin"] = jenis_kelamin
                p["tanggal_lahir"] = tanggal_lahir
                p["pendidikan"] = pendidikan
                p["pekerjaan"] = pekerjaan
                p["alamat"] = alamat
                p["no_hp"] = no_hp
                p["diagnosa"] = diagnosa
                updated = True
                break

        if not updated:
            messagebox.showerror(
                "Error",
                "Pasien tidak ditemukan di database.",
            )
            return

        self.save_json("pasien.json", pasien_list)

        messagebox.showinfo(
            "Berhasil",
            "Data pasien berhasil diperbarui.",
        )

        # Tutup window edit
        if hasattr(self, "edit_patient_window"):
            self.edit_patient_window.destroy()

        # Refresh tabel
        self.patients_data = self.load_patients_for_current_doctor()
        self.render_table(self.patients_data)

    def create_detail_handler(self, row_data):
        def handler():
            self.view_detail(row_data)

        return handler

    def create_edit_handler(self, row_data):
        def handler():
            self.open_edit_patient_window(row_data)

        return handler

    def create_set_konsul_handler(self, row_data):
        def handler():
            self.open_set_konsul_window(row_data)

        return handler

    def render_table(self, data):
        # Bersihkan konten frame scrollable sebelum render ulang
        for widget in self.table_scroll_frame.winfo_children():
            widget.destroy()

        # Header Tabel
        header_row = ctk.CTkFrame(
            self.table_scroll_frame, fg_color="#f1f1f1", height=40
        )
        header_row.pack(fill="x")

        headers = [
            "Nama Pasien",
            "Diagnosa",
            "Jenis",
            "Kategori",
            "Progress 2 Minggu",
            "Tanggal Konsul",
            "Aksi",
        ]
        col_widths = [160, 220, 120, 110, 130, 130, 120]

        for i, h in enumerate(headers):
            label = ctk.CTkLabel(
                header_row,
                text=h,
                font=("Arial bold", 13),
                text_color="black",
                width=col_widths[i],
                anchor="w",
            )
            label.pack(side="left", padx=15, pady=5)

        # Isi Tabel
        for row_data in data:
            row_frame = ctk.CTkFrame(
                self.table_scroll_frame, fg_color="#ffffff", height=45
            )
            row_frame.pack(fill="x", pady=1)

            nama = row_data.get("nama", "-")
            diagnosa = row_data.get("diagnosa", "-")
            jenis = row_data.get("jenis", "-")
            kategori = row_data.get("kategori", "-")
            progress_label = row_data.get("progress_label", "-")
            selesai_2minggu = row_data.get("selesai_2minggu", False)
            tanggal_konsul = row_data.get("tanggal_konsul") or ""

            # Kolom 1 - Nama Pasien
            ctk.CTkLabel(
                row_frame,
                text=nama,
                font=("Arial Bold", 13),
                anchor="w",
                width=col_widths[0],
            ).pack(side="left", padx=15)

            # Kolom 2 - Diagnosa
            ctk.CTkLabel(
                row_frame,
                text=diagnosa,
                width=col_widths[1],
                anchor="w",
                font=("Arial", 13),
            ).pack(side="left", padx=15)

            # Kolom 3 - Jenis
            ctk.CTkLabel(
                row_frame,
                text=jenis,
                width=col_widths[2],
                anchor="w",
                font=("Arial", 13),
            ).pack(side="left", padx=15)

            # Kolom 4 - Kategori WHO-5
            badge_color = self.badge_colour(kategori)
            ctk.CTkLabel(
                row_frame,
                text=kategori,
                width=col_widths[3] - 20,
                fg_color=badge_color,
                corner_radius=6,
                font=("Arial Bold", 13),
                text_color="black",
            ).pack(side="left", padx=15)

            # Kolom 5 - Progress 2 Minggu (X/14)
            progress_bg = "#bbf7d0" if selesai_2minggu else "#e5e7eb"
            ctk.CTkLabel(
                row_frame,
                text=progress_label,
                width=col_widths[4] - 20,
                fg_color=progress_bg,
                corner_radius=6,
                font=("Arial Bold", 13),
                text_color="#111827",
            ).pack(side="left", padx=15)

            # Kolom 6 - Tanggal Konsul
            if tanggal_konsul:
                konsul_text = tanggal_konsul
                konsul_bg = "#bfdbfe"  # biru muda kalau sudah dijadwalkan
            else:
                konsul_text = "-"
                konsul_bg = "#e5e7eb"

            ctk.CTkLabel(
                row_frame,
                text=konsul_text,
                width=col_widths[5] - 20,
                fg_color=konsul_bg,
                corner_radius=6,
                font=("Arial", 13),
                text_color="#111827",
            ).pack(side="left", padx=15)

            # Kolom 7 - Aksi
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_frame.pack(side="left", padx=10)

            # Detail
            ctk.CTkButton(
                action_frame,
                text="👁",
                text_color="#01030E",
                width=32,
                height=32,
                fg_color="transparent",
                hover_color="#3B8ED0",
                command=self.create_detail_handler(row_data),
            ).pack(side="left", padx=2)

            # Edit
            ctk.CTkButton(
                action_frame,
                text="✏️",
                text_color="#01030E",
                width=32,
                height=32,
                fg_color="transparent",
                hover_color="#22c55e",
                command=self.create_edit_handler(row_data),
            ).pack(side="left", padx=2)

            # Atur tanggal konsul:
            # hanya muncul kalau:
            #  - sudah selesai 2 minggu (>=14 check-in)
            #  - dan BELUM ada tanggal_konsul
            if selesai_2minggu and not tanggal_konsul:
                ctk.CTkButton(
                    action_frame,
                    text="📅",
                    text_color="#01030E",
                    width=32,
                    height=32,
                    fg_color="transparent",
                    hover_color="#f97316",
                    command=self.create_set_konsul_handler(row_data),
                ).pack(side="left", padx=2)

    def enter_pressed(self, event):
        keyword = self.search_entry.get()
        self.search_patient(keyword)

    def search_patient(self, keyword):
        keyword = keyword.strip()

        if keyword == "":
            self.render_table(self.patients_data)
            return

        result = []
        keyword_lower = keyword.lower()
        for p in self.patients_data:
            nama = (p.get("nama") or "").lower()
            if keyword_lower in nama:
                result.append(p)

        if not result:
            messagebox.showinfo("Hasil", "Pasien tidak ditemukan")

        self.render_table(result)

        # badge warna per kategori

    def badge_colour(self, kategori):
        k = (kategori or "").lower()

        if k in ["memadai", "hijau"]:
            return "#bbf7d0"  # hijau muda

        if k in ["rendah", "kuning", "orange"]:
            return "#fef08a"  # kuning / sedang

        if k in ["berisiko", "merah"]:
            return "#fecaca"  # merah / berisiko

        return "#e5e7eb"

    def view_detail(self, row_data):
        pasien = row_data.get("detail", {})
        id_pasien = row_data.get("id_pasien")

        # --- Ambil riwayat jawaban ---
        all_jawaban = self.load_json("jawaban_harian.json")
        history = [j for j in all_jawaban if j.get("id_pasien") == id_pasien]
        history.sort(key=lambda x: x.get("tanggal", ""))

        # --- Buat window baru ---
        win = ctk.CTkToplevel(self.window)
        win.title(f"Detail Pasien - {pasien.get('nama', '-')}")
        win.geometry("900x600")
        win.grab_set()  # fokus ke window detail

        container = ctk.CTkFrame(win, fg_color="#f8f9fa")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Kiri: Biodata
        left = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=10)
        left.pack(side="left", fill="y", padx=(0, 15), pady=10)

        ctk.CTkLabel(
            left,
            text="Biodata Pasien",
            font=("Arial Bold", 18),
            text_color="#111827",
        ).pack(anchor="w", padx=15, pady=(15, 10))

        def add_field(label, value):
            ctk.CTkLabel(
                left,
                text=f"{label}",
                font=("Arial", 12),
                text_color="#6b7280",
            ).pack(anchor="w", padx=15, pady=(5, 0))
            ctk.CTkLabel(
                left,
                text=f"{value}",
                font=("Arial Bold", 13),
                text_color="#111827",
            ).pack(anchor="w", padx=15)

        add_field("Nama", pasien.get("nama", "-"))
        add_field("Jenis Kelamin", pasien.get("jenis_kelamin", "-"))
        add_field("Tanggal Lahir", pasien.get("tanggal_lahir", "-"))
        add_field("Pendidikan", pasien.get("pendidikan", "-"))
        add_field("Pekerjaan", pasien.get("pekerjaan", "-"))
        add_field("Alamat", pasien.get("alamat", "-"))
        add_field("No. HP", pasien.get("no_hp", "-"))
        add_field("Diagnosa", pasien.get("diagnosa", row_data.get("diagnosa", "-")))
        add_field("Tanggal Konsultasi", pasien.get("tanggal_konsul", "-"))

        # Kanan: Grafik
        right = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=10)
        right.pack(side="right", fill="both", expand=True, pady=10)

        ctk.CTkLabel(
            right,
            text="Riwayat Skor WHO-5",
            font=("Arial Bold", 18),
            text_color="#111827",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        if history:
            tanggal = [h.get("tanggal", "") for h in history]
            skor = [h.get("total_percentage", 0) for h in history]

            fig = Figure(figsize=(5, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(tanggal, skor, marker="o")
            ax.set_ylim(0, 100)
            ax.set_xlabel("Tanggal")
            ax.set_ylabel("Skor WHO-5 (%)")
            ax.set_title("Perubahan Skor dari Waktu ke Waktu")
            ax.grid(True, alpha=0.3)

            canvas = FigureCanvasTkAgg(fig, master=right)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        else:
            ctk.CTkLabel(
                right,
                text="Belum ada riwayat check-in untuk pasien ini.",
                font=("Arial", 13),
                text_color="#6b7280",
            ).pack(fill="both", expand=True, padx=15, pady=15)

    def run(self):
        self.window.mainloop()

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Yakin ingin logout?")
        if not confirm:
            return

        # Tutup window dashboard
        self.window.destroy()

        # Kalau ada callback, panggil (biar balik ke login)
        if self.on_logout is not None:
            self.on_logout()


if __name__ == "__main__":
    # SIMULASI dokter yang login (buat testing doang)
    contoh_user = {"id_role": 2, "id_dokter": 1, "nama": "Dokter Testing"}
    app = dokterDashboard(contoh_user)
    app.run()

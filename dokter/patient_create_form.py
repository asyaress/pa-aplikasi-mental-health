import customtkinter as ctk
from tkinter import messagebox

class CreatePatientMixin:
    """Form tambah pasien (create)."""

    # ---------- CREATE PASIEN ----------
    def open_create_patient_window(self):
        win = ctk.CTkToplevel(self.window)
        win.title("Tambah Pasien Baru")
        win.geometry("600x750")
        win.grab_set()
        self.create_patient_window = win

        outer_frame = ctk.CTkFrame(win, fg_color="#f8f9fa")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scroll_frame = ctk.CTkScrollableFrame(
            outer_frame,
            fg_color="#ffffff",
            corner_radius=10,
        )
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        frame = scroll_frame

        ctk.CTkLabel(
            frame,
            text="Tambah Pasien Baru",
            font=("Arial Bold", 20),
            text_color="#111827",
        ).pack(pady=(10, 20))

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
            ent.pack(fill="x", padx=10, pady=(0, 5)) #

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

        # Jenis kelamin
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

        # Tanggal lahir (3 input)
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
            placeholder_text="HH",
            height=32,
        )
        self.birth_day_entry.pack(side="left")

        self.birth_month_entry = ctk.CTkEntry(
            birth_frame,
            width=70,
            placeholder_text="BB",
            height=32,
        )
        self.birth_month_entry.pack(side="left", padx=5)

        self.birth_year_entry = ctk.CTkEntry(
            birth_frame,
            width=100,
            placeholder_text="TTTT",
            height=32,
        )
        self.birth_year_entry.pack(side="left")

        # Pendidikan
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

        # Pekerjaan
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

        # Alamat
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

        ctk.CTkButton(
            frame,
            text="Simpan Pasien",
            height=36,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.submit_new_patient,
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

    def submit_new_patient(self):
        username = (self.new_username_entry.get() or "").strip()
        password = (self.new_password_entry.get() or "").strip()
        nama = (self.new_name_entry.get() or "").strip()
        jenis_kelamin = self.new_gender_option.get()

        day = (self.birth_day_entry.get() or "").strip()
        month = (self.birth_month_entry.get() or "").strip()
        year = (self.birth_year_entry.get() or "").strip()

        alamat = (self.new_address_text.get("1.0", "end") or "").strip()
        no_hp = (self.new_phone_entry.get() or "").strip()
        diagnosa = (self.new_diagnosa_entry.get() or "").strip()

        pendidikan = self.new_education_option.get()
        pekerjaan = self.new_job_option.get()

        # VALIDASI
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

        # Tanggal lahir
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
            tanggal_lahir = f"{year}-{month}-{day}"

        # Load data
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

        new_user_id = max([u.get("id", 0) for u in users], default=0) + 1
        new_pasien_id = max([p.get("id", 0) for p in pasien_list], default=0) + 1

        new_user = {
            "id": new_user_id,
            "username": username,
            "password": password,
            "id_role": 3,
        }
        users.append(new_user)
        self.save_json("users.json", users)

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
            "id_set_pertanyaan": 1,
            "tanggal_konsul": "",
        }
        pasien_list.append(new_pasien)
        self.save_json("pasien.json", pasien_list)

        messagebox.showinfo("Berhasil", "Data pasien baru berhasil ditambahkan.")

        if hasattr(self, "create_patient_window"):
            self.create_patient_window.destroy()

        self.patients_data = self.load_patients_for_current_doctor()
        self.render_table(self.patients_data)

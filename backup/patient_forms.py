import customtkinter as ctk
from tkinter import messagebox
import datetime


class PatientFormMixin:
    """
    Mixin untuk semua window/form pasien:
    - tambah pasien
    - edit pasien
    - atur tanggal konsultasi
    """

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

    # ---------- EDIT PASIEN ----------
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

        ctk.CTkLabel(
            frame,
            text="Edit Data Pasien",
            font=("Arial Bold", 20),
            text_color="#111827",
        ).pack(pady=(10, 20))

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

        # Nama
        self.edit_name_entry = add_labeled_entry(
            frame,
            "Nama Lengkap",
            pasien.get("nama", ""),
        )

        # Jenis kelamin
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

        # Tanggal lahir
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

        # Pendidikan
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

        # Pekerjaan
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

        # Alamat
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

        # No HP
        self.edit_phone_entry = add_labeled_entry(
            frame,
            "No. HP",
            pasien.get("no_hp", ""),
        )

        # Diagnosa
        self.edit_diagnosa_entry = add_labeled_entry(
            frame,
            "Diagnosa (opsional)",
            pasien.get("diagnosa", ""),
        )

        ctk.CTkButton(
            frame,
            text="Simpan Perubahan",
            height=36,
            fg_color="#22c55e",
            hover_color="#16a34a",
            command=self.submit_edit_patient,
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

        if hasattr(self, "edit_patient_window"):
            self.edit_patient_window.destroy()

        self.patients_data = self.load_patients_for_current_doctor()
        self.render_table(self.patients_data)

    # ---------- TANGGAL KONSUL ----------
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

        today = datetime.date.today()
        def_day = today.day
        def_month = today.month
        def_year = today.year

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
        year_values = [str(def_year + i) for i in range(0, 3)]

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

        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            messagebox.showerror("Error", "Tanggal konsultasi tidak valid.")
            return

        try:
            datetime.date(int(year), int(month), int(day))
        except ValueError:
            messagebox.showerror("Error", "Tanggal konsultasi tidak valid.")
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

        if hasattr(self, "konsul_window"):
            self.konsul_window.destroy()

        self.patients_data = self.load_patients_for_current_doctor()
        self.render_table(self.patients_data)

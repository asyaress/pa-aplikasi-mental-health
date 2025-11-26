import customtkinter as ctk
from tkinter import messagebox


class EditPatientMixin:
    """Form edit pasien."""

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

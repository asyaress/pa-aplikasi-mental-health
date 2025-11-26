import customtkinter as ctk
from tkinter import messagebox
import datetime


class KonsulPatientMixin:
    """Form atur tanggal konsultasi pasien."""

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

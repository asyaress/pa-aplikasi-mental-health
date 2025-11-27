import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_edit_patient(app, pasien):
    win = ctk.CTkToplevel(app.window)
    win.title("Edit Pasien")
    win.geometry("520x650")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame, text="Edit Data Pasien", font=("Arial Bold", 20), text_color="#111827"
    ).pack(pady=(5, 15))

    def add_entry(label, initial=""):
        ctk.CTkLabel(
            frame, text=label, font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(6, 0))
        ent = ctk.CTkEntry(frame, height=32)
        ent.pack(fill="x", pady=(0, 2))
        if initial:
            ent.insert(0, initial)
        return ent

    nama_entry = add_entry("Nama lengkap", pasien.get("nama", ""))

    ctk.CTkLabel(
        frame, text="Jenis kelamin", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(6, 0))

    gender_menu = ctk.CTkOptionMenu(
        frame,
        values=["Pilih", "Laki-laki", "Perempuan"],
        height=32,
    )
    jk = pasien.get("jenis_kelamin", "Pilih")
    if jk not in ["Laki-laki", "Perempuan"]:
        jk = "Pilih"
    gender_menu.set(jk)
    gender_menu.pack(fill="x", pady=(0, 2))

    pendidikan_entry = add_entry("Pendidikan", pasien.get("pendidikan", ""))
    pekerjaan_entry = add_entry("Pekerjaan", pasien.get("pekerjaan", ""))

    ctk.CTkLabel(
        frame, text="Diagnosa", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(6, 0))

    diagnosa_text = ctk.CTkTextbox(frame, height=80)
    diagnosa_text.pack(fill="x", pady=(0, 10))
    diagnosa_text.insert("1.0", pasien.get("diagnosa", ""))

    def on_save():
        nama = (nama_entry.get() or "").strip()
        gender = gender_menu.get()
        pendidikan = (pendidikan_entry.get() or "").strip()
        pekerjaan = (pekerjaan_entry.get() or "").strip()
        diagnosa = (diagnosa_text.get("1.0", "end") or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama pasien wajib diisi.")
            return

        if gender == "Pilih":
            gender = ""

        pasien_list = datastore.get_all_patients()
        target_id = pasien.get("id")
        updated = False
        for p in pasien_list:
            if p.get("id") == target_id:
                p["nama"] = nama
                p["jenis_kelamin"] = gender
                p["pendidikan"] = pendidikan
                p["pekerjaan"] = pekerjaan
                p["diagnosa"] = diagnosa
                updated = True
                break

        if not updated:
            messagebox.showerror("Error", "Pasien tidak ditemukan di database.")
            return

        datastore.save_all_patients(pasien_list)
        messagebox.showinfo("Berhasil", "Data pasien berhasil diperbarui.")

        app.patients_data = datastore.load_patients_for_table()
        app.render_table()
        win.destroy()

    ctk.CTkButton(
        frame,
        text="Simpan",
        height=36,
        fg_color="#3b82f6",
        hover_color="#2563eb",
        command=on_save,
    ).pack(fill="x", pady=(10, 4))

    ctk.CTkButton(
        frame,
        text="Batal",
        height=32,
        fg_color="#e5e7eb",
        text_color="#111827",
        hover_color="#d1d5db",
        command=win.destroy,
    ).pack(fill="x")

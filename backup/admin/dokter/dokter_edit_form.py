import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_edit_doctor(app, dokter):
    win = ctk.CTkToplevel(app.window)
    win.title("Edit Dokter")
    win.geometry("520x520")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame, text="Edit Data Dokter", font=("Arial Bold", 20), text_color="#111827"
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

    nama_entry = add_entry("Nama dokter", dokter.get("nama", ""))
    spesialis_entry = add_entry("Spesialis", dokter.get("spesialis", ""))
    tempat_awal = dokter.get("tempat_praktik", dokter.get("tempat_kerja", ""))
    tempat_entry = add_entry("Tempat praktik", tempat_awal)
    hp_entry = add_entry("No. HP", dokter.get("no_hp", ""))

    def on_save():
        nama = (nama_entry.get() or "").strip()
        spesialis = (spesialis_entry.get() or "").strip()
        tempat = (tempat_entry.get() or "").strip()
        no_hp = (hp_entry.get() or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama dokter wajib diisi.")
            return

        dokter_list = datastore.get_all_doctors()
        target_id = dokter.get("id")
        updated = False
        for d in dokter_list:
            if d.get("id") == target_id:
                d["nama"] = nama
                d["spesialis"] = spesialis
                d["tempat_praktik"] = tempat
                d["no_hp"] = no_hp
                updated = True
                break

        if not updated:
            messagebox.showerror("Error", "Dokter tidak ditemukan di database.")
            return

        datastore.save_all_doctors(dokter_list)
        messagebox.showinfo("Berhasil", "Data dokter berhasil diperbarui.")

        app.doctors_data = datastore.load_doctors_for_table()
        app.render_table()
        win.destroy()

    ctk.CTkButton(
        frame,
        text="Simpan",
        height=36,
        fg_color="#3b82f6",
        hover_color="#2563eb",
        command=on_save,
    ).pack(fill="x", pady=(12, 4))

    ctk.CTkButton(
        frame,
        text="Batal",
        height=32,
        fg_color="#e5e7eb",
        text_color="#111827",
        hover_color="#d1d5db",
        command=win.destroy,
    ).pack(fill="x")

import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_add_doctor(app):
    win = ctk.CTkToplevel(app.window)
    win.title("Tambah Dokter")
    win.geometry("520x520")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame, text="Tambah Dokter Baru", font=("Arial Bold", 20), text_color="#111827"
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

    username_entry = add_entry("Username login dokter")
    password_entry = add_entry("Password login dokter")

    nama_entry = add_entry("Nama dokter")
    spesialis_entry = add_entry("Spesialis")
    tempat_entry = add_entry("Tempat praktik")
    hp_entry = add_entry("No. HP")

    def on_save():
        nama = (nama_entry.get() or "").strip()
        spesialis = (spesialis_entry.get() or "").strip()
        tempat = (tempat_entry.get() or "").strip()
        no_hp = (hp_entry.get() or "").strip()
        username = (username_entry.get() or "").strip()
        password = (password_entry.get() or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama dokter wajib diisi.")
            return

        if not username or not password:
            messagebox.showerror("Error", "Username dan password wajib diisi.")
            return

        users = datastore.get_all_users()
        for u in users:
            if u.get("username") == username:
                messagebox.showerror("Error", "Username sudah digunakan.")
                return

        dokter_list = datastore.get_all_doctors()

        new_user_id = max([u.get("id", 0) for u in users], default=0) + 1
        new_dokter_id = max([d.get("id", 0) for d in dokter_list], default=0) + 1

        users.append(
            {
                "id": new_user_id,
                "username": username,
                "password": password,
                "id_role": 2,
            }
        )

        dokter_list.append(
            {
                "id": new_dokter_id,
                "id_user": new_user_id,
                "nama": nama,
                "spesialis": spesialis,
                "tempat_praktik": tempat,
                "no_hp": no_hp,
            }
        )

        datastore.save_all_users(users)
        datastore.save_all_doctors(dokter_list)

        messagebox.showinfo("Berhasil", "Data dokter baru berhasil ditambahkan.")
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

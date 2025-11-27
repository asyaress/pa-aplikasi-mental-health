import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_add_patient(app):
    win = ctk.CTkToplevel(app.window)
    win.title("Tambah Pasien")
    win.geometry("520x650")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame, text="Tambah Pasien Baru", font=("Arial Bold", 20), text_color="#111827"
    ).pack(pady=(5, 15))

    def add_entry(label):
        ctk.CTkLabel(
            frame, text=label, font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(6, 0))
        ent = ctk.CTkEntry(frame, height=32)
        ent.pack(fill="x", pady=(0, 2))
        return ent

    username_entry = add_entry("Username login pasien")
    password_entry = add_entry("Password login pasien")
    dokter_id_entry = add_entry("ID Dokter (angka, mis. 1)")

    nama_entry = add_entry("Nama lengkap")

    ctk.CTkLabel(
        frame, text="Jenis kelamin", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(6, 0))

    gender_menu = ctk.CTkOptionMenu(
        frame,
        values=["Pilih", "Laki-laki", "Perempuan"],
        height=32,
    )
    gender_menu.set("Pilih")
    gender_menu.pack(fill="x", pady=(0, 2))

    pendidikan_entry = add_entry("Pendidikan")
    pekerjaan_entry = add_entry("Pekerjaan")

    ctk.CTkLabel(
        frame, text="Diagnosa", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(6, 0))

    diagnosa_text = ctk.CTkTextbox(frame, height=80)
    diagnosa_text.pack(fill="x", pady=(0, 10))

    def on_save():
        nama = (nama_entry.get() or "").strip()
        gender = gender_menu.get()
        pendidikan = (pendidikan_entry.get() or "").strip()
        pekerjaan = (pekerjaan_entry.get() or "").strip()
        diagnosa = (diagnosa_text.get("1.0", "end") or "").strip()
        username = (username_entry.get() or "").strip()
        password = (password_entry.get() or "").strip()
        dokter_str = (dokter_id_entry.get() or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama pasien wajib diisi.")
            return

        if gender == "Pilih":
            gender = ""

        if not username or not password:
            messagebox.showerror("Error", "Username dan password wajib diisi.")
            return

        users = datastore.get_all_users()
        for u in users:
            if u.get("username") == username:
                messagebox.showerror("Error", "Username sudah digunakan.")
                return

        try:
            id_dokter = int(dokter_str) if dokter_str else 0
        except ValueError:
            messagebox.showerror("Error", "ID Dokter harus berupa angka.")
            return

        pasien_list = datastore.get_all_patients()

        new_user_id = max([u.get("id", 0) for u in users], default=0) + 1
        new_pasien_id = max([p.get("id", 0) for p in pasien_list], default=0) + 1

        users.append(
            {
                "id": new_user_id,
                "username": username,
                "password": password,
                "id_role": 3,
            }
        )
        pasien_list.append(
            {
                "id": new_pasien_id,
                "id_user": new_user_id,
                "id_dokter": id_dokter,
                "nama": nama,
                "jenis_kelamin": gender,
                "pendidikan": pendidikan,
                "pekerjaan": pekerjaan,
                "diagnosa": diagnosa,
                "id_set_pertanyaan": 1,
            }
        )

        datastore.save_all_users(users)
        datastore.save_all_patients(pasien_list)

        messagebox.showinfo("Berhasil", "Data pasien baru berhasil ditambahkan.")

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

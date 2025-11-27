import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_add_role(app):
    win = ctk.CTkToplevel(app.window)
    win.title("Tambah Role")
    win.geometry("420x260")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame, text="Tambah Role Baru", font=("Arial Bold", 20), text_color="#111827"
    ).pack(pady=(5, 15))

    ctk.CTkLabel(
        frame, text="Nama role", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(6, 0))

    nama_entry = ctk.CTkEntry(frame, height=32)
    nama_entry.pack(fill="x", pady=(0, 10))

    def on_save():
        nama = (nama_entry.get() or "").strip()
        if not nama:
            messagebox.showerror("Error", "Nama role wajib diisi.")
            return

        roles = datastore.get_all_roles()
        new_id = max([r.get("id", 0) for r in roles], default=0) + 1
        roles.append({"id": new_id, "nama_role": nama})
        datastore.save_all_roles(roles)

        messagebox.showinfo("Berhasil", "Role baru berhasil ditambahkan.")
        app.roles_data = datastore.load_roles_for_table()
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

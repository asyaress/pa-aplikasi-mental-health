import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_edit_role(app, role):
    win = ctk.CTkToplevel(app.window)
    win.title("Edit Role")
    win.geometry("420x260")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame, text="Edit Role", font=("Arial Bold", 20), text_color="#111827"
    ).pack(pady=(5, 15))

    ctk.CTkLabel(
        frame,
        text=f"ID Role: {role.get('id')}",
        font=("Arial", 11),
        text_color="#6b7280",
    ).pack(anchor="w", pady=(0, 4))

    ctk.CTkLabel(
        frame, text="Nama role", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(6, 0))

    nama_entry = ctk.CTkEntry(frame, height=32)
    nama_entry.pack(fill="x", pady=(0, 10))
    nama_entry.insert(0, role.get("nama_role", ""))

    def on_save():
        nama = (nama_entry.get() or "").strip()
        if not nama:
            messagebox.showerror("Error", "Nama role wajib diisi.")
            return

        roles = datastore.get_all_roles()
        target_id = role.get("id")
        updated = False
        for r in roles:
            if r.get("id") == target_id:
                r["nama_role"] = nama
                updated = True
                break

        if not updated:
            messagebox.showerror("Error", "Role tidak ditemukan di database.")
            return

        datastore.save_all_roles(roles)
        messagebox.showinfo("Berhasil", "Data role berhasil diperbarui.")

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

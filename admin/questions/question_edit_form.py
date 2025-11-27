import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore


def open_edit_question(app, item):
    win = ctk.CTkToplevel(app.window)
    win.title("Edit Pertanyaan")
    win.geometry("520x430")
    win.grab_set()

    frame = ctk.CTkFrame(win, fg_color="#f9fafb")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        frame,
        text="Edit Item Pertanyaan",
        font=("Arial Bold", 20),
        text_color="#111827",
    ).pack(pady=(5, 15))

    sets = datastore.load_question_sets()
    sets_list = list(sets.values())
    if not sets_list:
        ctk.CTkLabel(
            frame,
            text="Belum ada set_pertanyaan di set_pertanyaan.json",
            font=("Arial", 11),
            text_color="#b91c1c",
        ).pack(pady=(0, 10))
        display_to_id = {}
        set_values = ["-"]
    else:
        set_values = [f"{s.get('id')} - {s.get('nama_set', '')}" for s in sets_list]
        display_to_id = {
            f"{s.get('id')} - {s.get('nama_set', '')}": s.get("id") for s in sets_list
        }

    ctk.CTkLabel(
        frame, text="Set Pertanyaan", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(4, 0))

    set_menu = ctk.CTkOptionMenu(frame, values=set_values, height=32)
    current_set_id = item.get("id_set_pertanyaan")
    current_disp = next(
        (k for k, v in display_to_id.items() if v == current_set_id), set_values[0]
    )
    set_menu.set(current_disp)
    set_menu.pack(fill="x", pady=(0, 8))

    ctk.CTkLabel(
        frame, text="Nomor urut", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(4, 0))

    nomor_entry = ctk.CTkEntry(frame, height=32)
    nomor_entry.pack(fill="x", pady=(0, 8))
    nomor_entry.insert(0, str(item.get("nomor_urut", "")))

    ctk.CTkLabel(
        frame, text="Teks pertanyaan", font=("Arial", 12), text_color="#4b5563"
    ).pack(anchor="w", pady=(4, 0))

    teks_box = ctk.CTkTextbox(frame, height=120)
    teks_box.pack(fill="x", pady=(0, 10))
    teks_box.insert("1.0", item.get("teks_pertanyaan", ""))

    def on_save():
        disp = set_menu.get()
        set_id = display_to_id.get(disp)
        nomor_str = (nomor_entry.get() or "").strip()
        teks = (teks_box.get("1.0", "end") or "").strip()

        if not set_id:
            messagebox.showerror("Error", "Set pertanyaan belum dipilih.")
            return

        if not nomor_str or not teks:
            messagebox.showerror("Error", "Nomor urut dan teks pertanyaan wajib diisi.")
            return

        try:
            nomor = int(nomor_str)
        except ValueError:
            messagebox.showerror("Error", "Nomor urut harus berupa angka.")
            return

        items = datastore.get_all_items()
        target_id = item.get("id")
        updated = False
        for it in items:
            if it.get("id") == target_id:
                it["id_set_pertanyaan"] = set_id
                it["nomor_urut"] = nomor
                it["teks_pertanyaan"] = teks
                updated = True
                break

        if not updated:
            messagebox.showerror("Error", "Item pertanyaan tidak ditemukan.")
            return

        datastore.save_all_items(items)
        messagebox.showinfo("Berhasil", "Pertanyaan berhasil diperbarui.")

        app.question_sets = datastore.load_question_sets()
        app.questions_data = datastore.load_questions_for_table(app.question_sets)
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

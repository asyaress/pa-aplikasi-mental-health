import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore
from . import question_edit_form


def render_question_table(app):
    header_frame = ctk.CTkFrame(app.table_frame, fg_color="#fafafa", height=50)
    header_frame.pack(fill="x", pady=(0, 1))
    header_frame.pack_propagate(False)

    headers = ["", "No.", "Pertanyaan", "Set Pertanyaan", "Aksi"]
    widths = [50, 60, 520, 360, 130]

    for i, h in enumerate(headers):
        if i == 0:
            ctk.CTkLabel(
                header_frame,
                text="",
                width=widths[i],
                font=("Arial Bold", 13),
                text_color="#333",
            ).pack(side="left", padx=5)
        else:
            ctk.CTkLabel(
                header_frame,
                text=h,
                width=widths[i],
                font=("Arial Bold", 13),
                text_color="#333",
                anchor="center",
            ).pack(side="left", padx=5)

    for idx, row in enumerate(app.questions_data):
        nomor, teks, nama_set, item_dict = row

        row_frame = ctk.CTkFrame(app.table_frame, fg_color="white", height=70)
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)

        checkbox_container = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[0]
        )
        checkbox_container.pack(side="left", padx=5)
        checkbox_container.pack_propagate(False)

        var = ctk.BooleanVar(value=False)
        app.checkbox_vars.append(var)

        check = ctk.CTkCheckBox(
            checkbox_container,
            text="",
            variable=var,
            command=app.update_selection_count,
            checkbox_width=18,
            checkbox_height=18,
            fg_color="#1e5a9e",
            hover_color="#1d4ed8",
        )
        check.place(relx=0.5, rely=0.5, anchor="center")

        no_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[1]
        )
        no_frame.pack(side="left", padx=5)
        no_frame.pack_propagate(False)

        ctk.CTkLabel(
            no_frame,
            text=str(nomor),
            font=("Arial Bold", 12),
            text_color="#111",
        ).place(relx=0.5, rely=0.5, anchor="center")

        teks_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[2]
        )
        teks_frame.pack(side="left", padx=5)
        teks_frame.pack_propagate(False)

        ctk.CTkLabel(
            teks_frame,
            text=teks,
            font=("Arial", 12),
            text_color="#333",
            anchor="w",
            wraplength=widths[2] - 20,
        ).place(relx=0, rely=0.5, anchor="w")

        set_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[3]
        )
        set_frame.pack(side="left", padx=5)
        set_frame.pack_propagate(False)

        ctk.CTkLabel(
            set_frame,
            text=nama_set,
            font=("Arial", 12),
            text_color="#333",
            anchor="center",
        ).place(relx=0.5, rely=0.5, anchor="center")

        aksi_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[4]
        )
        aksi_frame.pack(side="left", padx=5)
        aksi_frame.pack_propagate(False)

        edit_btn = ctk.CTkButton(
            aksi_frame,
            text="✏️",
            width=34,
            height=30,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            command=lambda i=idx: _open_edit(app, i),
        )
        edit_btn.pack(side="left", padx=4, pady=10)

        delete_btn = ctk.CTkButton(
            aksi_frame,
            text="🗑",
            width=34,
            height=30,
            fg_color="#ef4444",
            hover_color="#b91c1c",
            text_color="white",
            command=lambda i=idx: _delete_question(app, i),
        )
        delete_btn.pack(side="left", padx=4, pady=10)


def _open_edit(app, row_index: int):
    row = app.questions_data[row_index]
    item = row[3]
    question_edit_form.open_edit_question(app, item)


def _delete_question(app, row_index: int):
    row = app.questions_data[row_index]
    item = row[3]
    teks = item.get("teks_pertanyaan", "")[:40] + "..."
    target_id = item.get("id")

    if not target_id:
        messagebox.showerror("Error", "Item pertanyaan tidak memiliki ID valid.")
        return

    if not messagebox.askyesno("Konfirmasi", f'Hapus pertanyaan:\n"{teks}" ?'):
        return

    items = datastore.get_all_items()
    items = [it for it in items if it.get("id") != target_id]
    datastore.save_all_items(items)

    app.question_sets = datastore.load_question_sets()
    app.questions_data = datastore.load_questions_for_table(app.question_sets)
    app.render_table()

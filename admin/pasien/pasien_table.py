import customtkinter as ctk
from tkinter import messagebox
from ..core.helpers import badge_color
from ..core import datastore
from . import pasien_edit_form


def render_patient_table(app):
    header_frame = ctk.CTkFrame(app.table_frame, fg_color="#fafafa", height=50)
    header_frame.pack(fill="x", pady=(0, 1))
    header_frame.pack_propagate(False)

    headers = ["", "Nama Pasien", "Diagnosa", "Jenis", "Kategori Mingguan", "Aksi"]
    widths = [50, 280, 220, 220, 200, 130]

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

    for idx, row_data in enumerate(app.patients_data):
        row_frame = ctk.CTkFrame(app.table_frame, fg_color="white", height=70)
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)

        widths = [50, 280, 220, 220, 200, 130]

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

        name_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[1]
        )
        name_frame.pack(side="left", padx=5)
        name_frame.pack_propagate(False)

        avatar = ctk.CTkLabel(
            name_frame,
            text="👤",
            font=("Arial", 18),
            width=40,
            height=40,
            fg_color="#e5e7eb",
            corner_radius=20,
        )
        avatar.pack(side="left", padx=(10, 12), pady=15)

        name_container = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_container.pack(side="left", fill="y", expand=True, pady=15)

        ctk.CTkLabel(
            name_container,
            text=row_data[0] if row_data[0] != "Cell Content" else "Cell Content",
            font=("Arial Bold", 12),
            text_color="#111",
            anchor="w",
        ).pack(anchor="w", pady=(0, 2))

        ctk.CTkLabel(
            name_container,
            text="Sub Content",
            font=("Arial", 10),
            text_color="#999",
            anchor="w",
        ).pack(anchor="w")

        diagnosa_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[2]
        )
        diagnosa_frame.pack(side="left", padx=5)
        diagnosa_frame.pack_propagate(False)

        ctk.CTkLabel(
            diagnosa_frame,
            text=row_data[1],
            font=("Arial", 12),
            text_color="#333",
            anchor="center",
        ).place(relx=0.5, rely=0.5, anchor="center")

        jenis_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[3]
        )
        jenis_frame.pack(side="left", padx=5)
        jenis_frame.pack_propagate(False)

        ctk.CTkLabel(
            jenis_frame,
            text=row_data[2],
            font=("Arial", 12),
            text_color="#333",
            anchor="center",
        ).place(relx=0.5, rely=0.5, anchor="center")

        kategori_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[4]
        )
        kategori_frame.pack(side="left", padx=5)
        kategori_frame.pack_propagate(False)

        kategori = row_data[3]
        badge_bg = badge_color(kategori)

        kategori_label = ctk.CTkLabel(
            kategori_frame,
            text=kategori,
            font=("Arial Bold", 11),
            text_color="#111827",
            fg_color=badge_bg,
            corner_radius=12,
            width=widths[4] - 40,
        )
        kategori_label.place(relx=0.5, rely=0.5, anchor="center")

        aksi_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[5]
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
            command=lambda i=idx: _delete_patient(app, i),
        )
        delete_btn.pack(side="left", padx=4, pady=10)


def _open_edit(app, row_index: int):
    row = app.patients_data[row_index]
    pasien_dict = row[4]
    pasien_edit_form.open_edit_patient(app, pasien_dict)


def _delete_patient(app, row_index: int):
    row = app.patients_data[row_index]
    pasien = row[4]
    nama = pasien.get("nama", "Pasien")
    target_id = pasien.get("id")

    if not target_id:
        messagebox.showerror("Error", "Pasien tidak memiliki ID valid.")
        return

    if not messagebox.askyesno("Konfirmasi", f"Hapus data pasien '{nama}'?"):
        return

    pasien_list = datastore.get_all_patients()
    pasien_list = [p for p in pasien_list if p.get("id") != target_id]
    datastore.save_all_patients(pasien_list)

    app.patients_data = datastore.load_patients_for_table()
    app.render_table()

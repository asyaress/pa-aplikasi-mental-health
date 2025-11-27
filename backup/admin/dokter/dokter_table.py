import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore
from . import dokter_edit_form


def render_doctor_table(app):
    header_frame = ctk.CTkFrame(app.table_frame, fg_color="#fafafa", height=50)
    header_frame.pack(fill="x", pady=(0, 1))
    header_frame.pack_propagate(False)

    headers = ["", "Nama Dokter", "Spesialis", "Tempat Praktik", "Status", "Aksi"]
    widths = [50, 280, 220, 260, 160, 130]

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

    for idx, row_data in enumerate(app.doctors_data):
        row_frame = ctk.CTkFrame(app.table_frame, fg_color="white", height=70)
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)

        widths = [50, 280, 220, 260, 160, 130]

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
            text="👨‍⚕️",
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
            text=row_data[0],
            font=("Arial Bold", 12),
            text_color="#111",
            anchor="w",
        ).pack(anchor="w", pady=(0, 2))

        ctk.CTkLabel(
            name_container,
            text=row_data[1],
            font=("Arial", 10),
            text_color="#999",
            anchor="w",
        ).pack(anchor="w")

        spes_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[2]
        )
        spes_frame.pack(side="left", padx=5)
        spes_frame.pack_propagate(False)

        ctk.CTkLabel(
            spes_frame,
            text=row_data[1],
            font=("Arial", 12),
            text_color="#333",
            anchor="center",
        ).place(relx=0.5, rely=0.5, anchor="center")

        tmp_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[3])
        tmp_frame.pack(side="left", padx=5)
        tmp_frame.pack_propagate(False)

        ctk.CTkLabel(
            tmp_frame,
            text=row_data[2],
            font=("Arial", 12),
            text_color="#333",
            anchor="center",
        ).place(relx=0.5, rely=0.5, anchor="center")

        status_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[4]
        )
        status_frame.pack(side="left", padx=5)
        status_frame.pack_propagate(False)

        status = row_data[3]
        bg = "#bbf7d0" if status == "Aktif" else "#e5e7eb"

        ctk.CTkLabel(
            status_frame,
            text=status,
            font=("Arial Bold", 11),
            text_color="#111827",
            fg_color=bg,
            corner_radius=12,
            width=widths[4] - 40,
        ).place(relx=0.5, rely=0.5, anchor="center")

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
            command=lambda i=idx: _delete_doctor(app, i),
        )
        delete_btn.pack(side="left", padx=4, pady=10)


def _open_edit(app, row_index: int):
    row = app.doctors_data[row_index]
    dokter = row[4]
    dokter_edit_form.open_edit_doctor(app, dokter)


def _delete_doctor(app, row_index: int):
    row = app.doctors_data[row_index]
    dokter = row[4]
    nama = dokter.get("nama", "Dokter")
    target_id = dokter.get("id")

    if not target_id:
        messagebox.showerror("Error", "Dokter tidak memiliki ID valid.")
        return

    if not messagebox.askyesno("Konfirmasi", f"Hapus data dokter '{nama}'?"):
        return

    dokter_list = datastore.get_all_doctors()
    dokter_list = [d for d in dokter_list if d.get("id") != target_id]
    datastore.save_all_doctors(dokter_list)

    app.doctors_data = datastore.load_doctors_for_table()
    app.render_table()

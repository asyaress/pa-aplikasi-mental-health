import customtkinter as ctk
from tkinter import messagebox
from ..core import datastore
from . import role_edit_form


def render_role_table(app):
    header_frame = ctk.CTkFrame(app.table_frame, fg_color="#fafafa", height=50)
    header_frame.pack(fill="x", pady=(0, 1))
    header_frame.pack_propagate(False)

    headers = ["", "ID Role", "Nama Role", "Aksi"]
    widths = [50, 100, 500, 130]

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

    for idx, row in enumerate(app.roles_data):
        rid, nama_role, role_dict = row

        row_frame = ctk.CTkFrame(app.table_frame, fg_color="white", height=60)
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

        id_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[1])
        id_frame.pack(side="left", padx=5)
        id_frame.pack_propagate(False)

        ctk.CTkLabel(
            id_frame,
            text=str(rid),
            font=("Arial Bold", 12),
            text_color="#111",
        ).place(relx=0.5, rely=0.5, anchor="center")

        nama_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[2]
        )
        nama_frame.pack(side="left", padx=5)
        nama_frame.pack_propagate(False)

        ctk.CTkLabel(
            nama_frame,
            text=nama_role,
            font=("Arial", 12),
            text_color="#333",
            anchor="w",
        ).place(relx=0.0, rely=0.5, anchor="w")

        aksi_frame = ctk.CTkFrame(
            row_frame, fg_color="transparent", width=widths[3]
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
            command=lambda i=idx: _delete_role(app, i),
        )
        delete_btn.pack(side="left", padx=4, pady=10)


def _open_edit(app, row_index: int):
    row = app.roles_data[row_index]
    role_dict = row[2]
    role_edit_form.open_edit_role(app, role_dict)


def _delete_role(app, row_index: int):
    row = app.roles_data[row_index]
    role = row[2]
    rid = role.get("id")
    nama = role.get("nama_role", "Role")

    if not rid:
        messagebox.showerror("Error", "Role tidak memiliki ID valid.")
        return

    users = datastore.get_all_users()
    used_count = sum(1 for u in users if u.get("id_role") == rid)
    if used_count > 0:
        messagebox.showerror(
            "Tidak bisa dihapus",
            f"Role '{nama}' masih digunakan oleh {used_count} user.",
        )
        return

    if not messagebox.askyesno("Konfirmasi", f"Hapus role '{nama}'?"):
        return

    roles = datastore.get_all_roles()
    roles = [r for r in roles if r.get("id") != rid]
    datastore.save_all_roles(roles)

    app.roles_data = datastore.load_roles_for_table()
    app.render_table()

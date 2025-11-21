import customtkinter as ctk
from tkinter import messagebox


class AdminDashboard:
    def _init_(self, user):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Dashboard Admin")
        self.window.geometry("1200x700")
        self.window.configure(fg_color="#f8f9fa")

        self.user = user

        # ========================
        # KONFIGURASI MASTER DATA
        # ========================
        self.master_config = {
            "user": {
                "title": "Master User",
                "headers": ["Nama Lengkap", "Username", "Email", "Role", "Status", "Aksi"],
                "col_widths": [180, 140, 220, 120, 100, 80],
                # index kolom yang akan jadi badge warna (0-based)
                "badge_column": 4,  # Status
            },
            "dokter": {
                "title": "Master Dokter",
                "headers": ["Nama Dokter", "Spesialis", "No. STR", "Status", "Aksi"],
                "col_widths": [220, 200, 150, 100, 80],
                "badge_column": 3,  # Status
            },
            "role": {
                "title": "Master Role",
                "headers": ["Nama Role", "Deskripsi", "Level Akses", "Status", "Aksi"],
                "col_widths": [160, 290, 120, 100, 80],
                "badge_column": 3,  # Status
            },
            "pertanyaan": {
                "title": "Master Pertanyaan",
                "headers": ["Kode", "Pertanyaan", "Kategori", "Tipe Jawaban", "Status", "Aksi"],
                "col_widths": [70, 320, 140, 140, 100, 80],
                "badge_column": 4,  # Status
            },
        }

        # Data dummy untuk contoh
        self.master_data = {
            "user": [
                ["Admin Utama", "admin", "admin@example.com", "Admin", "Aktif"],
                ["Dina Putri", "dina", "dina@example.com", "Dokter", "Aktif"],
                ["Rafi Akun", "rafi", "rafi@example.com", "Pasien", "Nonaktif"],
            ],
            "dokter": [
                ["dr. Diftya", "Psikiater", "STR-00112233", "Aktif"],
                ["dr. Nanda", "Psikolog Klinis", "STR-00445566", "Aktif"],
                ["dr. Adi", "Psikiater Anak", "STR-00778899", "Nonaktif"],
            ],
            "role": [
                ["Admin", "Akses penuh ke semua modul", "Level 1", "Aktif"],
                ["Dokter", "Mengelola data pasien & konsultasi", "Level 2", "Aktif"],
                ["Pasien", "Mengisi kuesioner & konsultasi", "Level 3", "Aktif"],
                ["Viewer", "Hanya dapat melihat laporan", "Level 4", "Nonaktif"],
            ],
            "pertanyaan": [
                ["Q001", "Seberapa sering Anda merasa cemas dalam 2 minggu terakhir?", "Kecemasan", "Skala Likert 1-5", "Aktif"],
                ["Q002", "Apakah Anda mengalami kesulitan tidur?", "Tidur", "Ya / Tidak", "Aktif"],
                ["Q003", "Seberapa sering Anda merasa sedih tanpa alasan jelas?", "Mood", "Skala Likert 1-5", "Draft"],
            ],
        }

        # Mapping judul segmentedButton -> key
        self.title_to_key = {
            cfg["title"]: key for key, cfg in self.master_config.items()
        }

        # Page awal
        self.current_master = "user"

        self.build_ui()

    # ========================
    # BUILD UI
    # ========================
    def build_ui(self):
        # 1. Sidebar kiri
        self.sidebar = ctk.CTkFrame(
            self.window, fg_color="#ffffff", width=65, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        ctk.CTkLabel(
            self.sidebar, text="♾", font=("Arial", 30), text_color="#007bff"
        ).pack(pady=(30, 20))

        ctk.CTkButton(
            self.sidebar,
            text="➕",
            width=50,
            height=50,
            text_color="#000000",
            fg_color="#ffffff",
            hover_color="#0e98f5",
            corner_radius=10,
        ).pack(pady=10)

        menus = ["🏠", "🗓", "💬", "⏱", "⚙", "↩"]
        for icon in menus:
            label = ctk.CTkButton(
                self.sidebar,
                text=icon,
                font=("Arial", 20),
                text_color="#000000",
                fg_color="transparent",
                hover_color="#0e98f5",
                width=50,
                height=50,
                corner_radius=10,
            )
            label.pack(pady=18)

        # 2. Main Content (kanan)
        self.main_content = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        self.main_content.pack(
            side="right", fill="both", expand=True, padx=20, pady=20
        )

        # 2a. Header: judul + segmented button untuk pilih halaman
        header_frame = ctk.CTkFrame(
            self.main_content, fg_color="#f8f9fa"
        )
        header_frame.pack(side="top", fill="x", padx=15, pady=(0, 5))

        # Judul halaman (berubah sesuai master yang dipilih)
        self.page_title_label = ctk.CTkLabel(
            header_frame,
            text=self.master_config[self.current_master]["title"],
            font=("Arial Bold", 22),
            text_color="#212529",
        )
        self.page_title_label.pack(side="left")

        # Segmented Button untuk ganti halaman
        self.nav_segment = ctk.CTkSegmentedButton(
            header_frame,
            # urut sesuai config
            values=[
                self.master_config["user"]["title"],
                self.master_config["dokter"]["title"],
                self.master_config["role"]["title"],
                self.master_config["pertanyaan"]["title"],
            ],
            command=self.segment_changed,
        )
        self.nav_segment.pack(side="right", padx=10)
        self.nav_segment.set(self.master_config[self.current_master]["title"])

        # 3. ACTION BAR (search + info paging + icon aksi)
        self.action_bar = ctk.CTkFrame(
            self.main_content, fg_color="#ffffff", height=60, corner_radius=10
        )
        self.action_bar.pack(side="top", fill="x", pady=5, padx=15)

        # 3a. Bagian kiri (search)
        self.left_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.left_action.pack(side="left", padx=15, pady=10, fill="y")

        self.search_entry = ctk.CTkEntry(
            self.left_action,
            placeholder_text="🔍 Cari data...",
            width=250,
            height=35,
            border_width=1,
            border_color="#ddd",
            fg_color="#f9f9f9",
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", self.enter_pressed)

        ctk.CTkLabel(
            self.left_action,
            text="",
            text_color="#3B8ED0",
            font=("Arial Bold", 12),
        ).pack(side="left", padx=15)

        # 3b. Bagian kanan (info + ikon)
        right_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        right_action.pack(side="right", padx=15, fill="y")

        ctk.CTkLabel(
            right_action, text="1 - 10", text_color="#555", font=("Arial", 12)
        ).pack(side="left", padx=(0, 15))
        ctk.CTkLabel(
            right_action, text="< >", text_color="#555", font=("Arial Bold", 14)
        ).pack(side="left", padx=(0, 15))

        # fungsi handler umum
        def create_action_handler(icon_text):
            def handler():
                print(f"Aksi {icon_text} ditekan di {self.master_config[self.current_master]['title']}")

            return handler

        for ic in ["Y", "🖨", "⬇", "⤢"]:
            ctk.CTkButton(
                right_action,
                text=ic,
                width=35,
                height=35,
                fg_color="transparent",
                text_color="#555",
                hover_color="#eee",
                font=("Arial", 16),
                command=create_action_handler(ic),
            ).pack(side="left", padx=2)

        # 4. Scrollable Frame untuk tabel
        self.table_scroll_frame = ctk.CTkScrollableFrame(
            self.main_content, fg_color="#ffffff", corner_radius=10
        )
        self.table_scroll_frame.pack(
            side="top", fill="both", expand=True, pady=(0, 0), padx=15
        )

        # Render awal
        self.apply_current_master()

    # ========================
    # EVENT & HELPERS
    # ========================

    def segment_changed(self, value):
        """Callback saat segmented button diganti."""
        key = self.title_to_key.get(value)
        if key:
            self.current_master = key
            self.apply_current_master()

    def apply_current_master(self):
        """Update judul, placeholder search, dan tabel sesuai halaman aktif."""
        cfg = self.master_config[self.current_master]
        self.page_title_label.configure(text=cfg["title"])

        # Sesuaikan placeholder search
        placeholder = f"🔍 Cari {cfg['title']}..."
        self.search_entry.configure(placeholder_text=placeholder)
        self.search_entry.delete(0, "end")

        # Render tabel full data
        self.render_table(self.master_data[self.current_master])

    def enter_pressed(self, event):
        keyword = self.search_entry.get()
        self.search_current(keyword)

    def search_current(self, keyword: str):
        keyword = keyword.strip()
        data_source = self.master_data[self.current_master]

        if keyword == "":
            self.render_table(data_source)
            return

        kw = keyword.lower()
        result = []
        for row in data_source:
            for cell in row:
                if kw in str(cell).lower():
                    result.append(row)
                    break

        if not result:
            messagebox.showinfo(
                "Hasil",
                f"Data pada {self.master_config[self.current_master]['title']} tidak ditemukan",
            )

        self.render_table(result)

    # Fungsi untuk membuat handler detail
    def create_detail_handler(self, row_data):
        def handler():
            self.view_detail(row_data)

        return handler

    # ========================
    # RENDER TABEL GENERIK
    # ========================
    def render_table(self, data):
        # Bersihkan isi frame
        for widget in self.table_scroll_frame.winfo_children():
            widget.destroy()

        cfg = self.master_config[self.current_master]
        headers = cfg["headers"]
        col_widths = cfg["col_widths"]
        badge_column = cfg["badge_column"]

        # Header
        header_row = ctk.CTkFrame(
            self.table_scroll_frame, fg_color="#f1f1f1", height=40
        )
        header_row.pack(fill="x")

        for i, h in enumerate(headers):
            label = ctk.CTkLabel(
                header_row,
                text=h,
                font=("Arial bold", 13),
                text_color="black",
                width=col_widths[i],
                anchor="w",
            )
            label.pack(side="left", padx=15, pady=5)

        # Isi
        for row_data in data:
            row_frame = ctk.CTkFrame(
                self.table_scroll_frame, fg_color="#ffffff", height=45
            )
            row_frame.pack(fill="x", pady=1)

            # Semua kolom kecuali "Aksi" (kolom terakhir)
            for i in range(len(headers) - 1):
                text_value = row_data[i] if i < len(row_data) else ""

                # Jika kolom ini adalah badge (Status/Kategori)
                if badge_column is not None and i == badge_column:
                    badge_color = self.badge_colour(str(text_value))
                    ctk.CTkLabel(
                        row_frame,
                        text=text_value,
                        width=col_widths[i] - 20,
                        fg_color=badge_color,
                        corner_radius=6,
                        font=("Arial Bold", 13),
                        text_color="black",
                    ).pack(side="left", padx=15)
                else:
                    ctk.CTkLabel(
                        row_frame,
                        text=text_value,
                        font=("Arial", 13),
                        anchor="w",
                        width=col_widths[i],
                    ).pack(side="left", padx=15)

            # Kolom Aksi (tombol detail)
            ctk.CTkButton(
                row_frame,
                text="👁",
                text_color="#01030E",
                width=40,
                height=40,
                fg_color="transparent",
                hover_color="#3B8ED0",
                command=self.create_detail_handler(row_data),
            ).pack(side="left", padx=25)

    # ========================
    # WARNA BADGE
    # ========================
    def badge_colour(self, kategori):
        k = str(kategori).lower()

        # Status umum
        if k in ["aktif", "active", "memadai"]:
            return "#bbf7d0"  # hijau muda
        if k in ["nonaktif", "tidak aktif", "berisiko"]:
            return "#fecaca"  # merah muda
        if k in ["rendah", "pending", "draft"]:
            return "#fef08a"  # kuning
        return "#e5e7eb"  # abu default

    # ========================
    # DETAIL POPUP
    # ========================
    def view_detail(self, data):
        cfg = self.master_config[self.current_master]
        headers = cfg["headers"]

        lines = []
        # Jangan tampilkan "Aksi"
        for i, h in enumerate(headers):
            if h.lower() == "aksi":
                continue
            if i < len(data):
                lines.append(f"{h}: {data[i]}")

        messagebox.showinfo(
            f"Detail {cfg['title']}",
            "\n".join(lines),
        )

    def run(self):
        self.window.mainloop()


if _name_ == "_main_":
    contoh_user = {"Nama": "Admin"}
    app = AdminDashboard(contoh_user)
    app.run()
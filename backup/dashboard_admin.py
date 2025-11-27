import customtkinter as ctk  # Library untuk membuat GUI modern
from tkinter import messagebox  # Untuk menampilkan popup message
import json  # Untuk membaca dan menulis file JSON
import os  # Untuk cek file exists atau tidak


class ModernDashboard:
    def __init__(self, user):
        # Constructor - dijalankan saat object dibuat

        ctk.set_appearance_mode("light")  # Set tema terang
        ctk.set_default_color_theme("blue")  # Set warna tema biru

        self.window = ctk.CTk()  # Buat window utama
        self.window.title("Dashboard")  # Judul window
        self.window.geometry("1400x800")  # Ukuran window (lebar x tinggi)
        self.window.configure(fg_color="#2d2d2d")  # Background gelap
        self.window.resizable(True, True)

        self.user = user  # Simpan data user yang login

        self.data_folder = "data"
        self.pasien_file = os.path.join(self.data_folder, "pasien.json")
        self.users_file = os.path.join(self.data_folder, "users.json")
        self.dokter_file = os.path.join(self.data_folder, "dokter.json")
        self.item_file = os.path.join(self.data_folder, "item_pertanyaan.json")
        self.set_file = os.path.join(self.data_folder, "set_pertanyaan.json")
        self.role_file = os.path.join(self.data_folder, "roles.json")

        # menu aktif sekarang (sementara cuma pasien yang hidup)
        self.current_menu = "Pasien"

        # Data pasien untuk tabel
        self.patients_data = self.load_patients_from_json()
        self.doctors_data = self.load_doctors_from_json()
        self.question_sets = self.load_question_sets()
        self.questions_data = self.load_questions_from_json()
        self.roles_data = self.load_roles_from_json()

        # State untuk checkbox selection
        self.selected_rows = []  # List untuk menyimpan row yang dipilih
        self.checkbox_vars = []  # List untuk menyimpan checkbox variables

        self.build_ui()  # Panggil fungsi untuk membangun UI

    def load_patients_from_json(self):
        """Baca pasien.json dan bentuk data untuk tabel"""
        try:
            if not os.path.exists(self.pasien_file):
                return self.get_dummy_data()

            with open(self.pasien_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            patients = []
            for p in data:
                nama = p.get("nama", "Unknown")
                diagnosa = p.get("diagnosa", "Tidak ada diagnosa")
                pekerjaan = p.get("pekerjaan", p.get("pendidikan", "Tidak diketahui"))
                kategori = self.determine_kategori(diagnosa)

                # Struktur per-baris:
                # [0]=nama, [1]=diagnosa, [2]=jenis/pekerjaan, [3]=kategori, [4]=dict pasien asli
                patients.append([nama, diagnosa, pekerjaan, kategori, p])

            return patients if patients else self.get_dummy_data()

        except Exception:
            return self.get_dummy_data()

    def load_doctors_from_json(self):
        """Baca dokter.json dan bentuk data untuk tabel"""
        try:
            if not os.path.exists(self.dokter_file):
                return []

            with open(self.dokter_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            doctors = []
            for d in data:
                nama = d.get("nama", "Dokter")
                spesialis = d.get("spesialis", "-")
                tempat = d.get("tempat_praktik", d.get("tempat_kerja", "-"))
                status = "Aktif" if d.get("is_active", True) else "Nonaktif"

                # [0]=nama, [1]=spesialis, [2]=tempat, [3]=status, [4]=dict asli
                doctors.append([nama, spesialis, tempat, status, d])

            return doctors
        except Exception:
            return []

    def load_question_sets(self):
        """Baca set_pertanyaan.json sebagai dict {id: set_dict}"""
        data = self._load_json_file(self.set_file)
        sets_by_id = {}
        for s in data:
            sid = s.get("id")
            if sid is not None:
                sets_by_id[sid] = s
        return sets_by_id

    def load_questions_from_json(self):
        """Baca item_pertanyaan.json dan gabungkan dengan nama set."""
        items = self._load_json_file(self.item_file)
        sets_by_id = self.question_sets or self.load_question_sets()

        rows = []
        for it in items:
            nomor = it.get("nomor_urut", 0)
            teks = it.get("teks_pertanyaan", "")
            id_set = it.get("id_set_pertanyaan")
            nama_set = sets_by_id.get(id_set, {}).get("nama_set", f"Set {id_set}")
            # [0]=nomor, [1]=teks, [2]=nama_set, [3]=dict item asli
            rows.append([nomor, teks, nama_set, it])

        rows.sort(key=lambda r: r[0])
        return rows

    def load_roles_from_json(self):
        """Baca role.json dan bentuk data untuk tabel."""
        data = self._load_json_file(self.role_file)
        roles = []
        for r in data:
            rid = r.get("id")
            nama = r.get("nama_role", "")
            # [0]=id, [1]=nama_role, [2]=dict asli
            roles.append([rid, nama, r])

        # sort berdasarkan id
        roles.sort(key=lambda x: x[0] if x[0] is not None else 0)
        return roles

    def get_dummy_data(self):
        """Data dummy jika JSON tidak ada"""
        return [
            ["Cell Content", "Gangguan Kecemasan", "Pelajar (SMA)", "Cell Content", {}],
            ["Cell Content", "Bipolar", "Pelajar (Mahasiswa)", "Cell Content", {}],
            ["Cell Content", "Anxiety", "Pekerja Kontrak", "Cell Content", {}],
            ["Cell Content", "OCD", "Pekerja Lepas", "Cell Content", {}],
            [
                "Cell Content",
                "Skizofrenia",
                "Sedang Mencari Pekerjaan",
                "Cell Content",
                {},
            ],
            ["Cell Content", "Gangguan tidur", "Pekerja Keras", "Cell Content", {}],
            ["Cell Content", "Insomnia", "Pelajar", "Cell Content", {}],
            ["Cell Content", "Moody", "Pelajar", "Cell Content", {}],
            ["Cell Content", "Gangguan makan", "Pekerja Tetap", "Cell Content", {}],
            ["Cell Content", "Depresi", "Pekerja Lepas", "Cell Content", {}],
        ]

    def determine_kategori(self, diagnosa):
        """Fungsi untuk menentukan kategori risiko"""
        diagnosa_lower = diagnosa.lower()

        if any(
            word in diagnosa_lower
            for word in ["berat", "akut", "parah", "skizofrenia", "bipolar"]
        ):
            return "Berisiko"
        elif any(word in diagnosa_lower for word in ["ringan", "minor"]):
            return "Memadai"
        else:
            return "Rendah"

    def _load_json_file(self, path):
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json_file(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def badge_color(self, kategori):
        k = (kategori or "").lower()
        if "berisiko" in k:
            return "#fecaca"  # merah muda
        if "memadai" in k:
            return "#bbf7d0"  # hijau muda
        return "#fef08a"  # kuning / default

    def build_ui(self):
        """Fungsi untuk membangun semua elemen UI"""

        # ==================== SIDEBAR KIRI (Blue) ====================
        self.sidebar = ctk.CTkFrame(
            self.window, fg_color="#1e5a9e", width=250, corner_radius=0  # Biru
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Fixed width

        # Logo/Title
        ctk.CTkLabel(
            self.sidebar, text="Dashboard", font=("Arial Bold", 24), text_color="white"
        ).pack(pady=(30, 40), padx=20)

        # Search box di sidebar
        search_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 30))

        self.sidebar_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search",
            height=35,
            fg_color="#8cb4d9",  # Biru muda/terang
            border_width=2,
            border_color="#a8c5e0",  # Border biru lebih terang
            text_color="#1a4d7a",  # Text biru gelap
            placeholder_text_color="#4a7ba7",  # Placeholder biru medium
            corner_radius=8,
        )
        self.sidebar_search.pack(fill="x")

        # Menu items
        menu_items = [
            ("Pasien", "👥"),
            ("Dokter", "👨‍⚕️"),
            ("Questions", "❓"),
            ("Role", "🔐"),
        ]

        for item, icon in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {item}",
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#1d4ed8",
                anchor="w",
                height=45,
                command=lambda i=item: self.menu_clicked(i),
            )
            btn.pack(fill="x", padx=20, pady=2)

            # Tambahkan arrow
            arrow_label = ctk.CTkLabel(
                btn, text="›", font=("Arial", 20), text_color="white"
            )
            arrow_label.place(relx=0.95, rely=0.5, anchor="e")

        # ==================== MAIN CONTENT AREA ====================
        self.main_content = ctk.CTkFrame(
            self.window, fg_color="#f5f5f5", corner_radius=0
        )
        self.main_content.pack(side="right", fill="both", expand=True)

        # ==================== ACTION BAR ====================
        action_bar = ctk.CTkFrame(
            self.main_content, fg_color="white", height=60, corner_radius=0
        )
        action_bar.pack(fill="x", padx=30, pady=20)

        # Left side - Settings icon & Search
        left_action = ctk.CTkFrame(action_bar, fg_color="transparent")
        left_action.pack(side="left", padx=15, pady=10)

        ctk.CTkButton(
            left_action,
            text="⚙",
            width=35,
            height=35,
            fg_color="transparent",
            text_color="#666",
            hover_color="#f0f0f0",
            font=("Arial", 18),
        ).pack(side="left", padx=(0, 10))

        self.main_search = ctk.CTkEntry(
            left_action,
            placeholder_text="🔍 Search",
            width=250,
            height=35,
            border_width=1,
            border_color="#ddd",
            fg_color="white",
        )
        self.main_search.pack(side="left", padx=(0, 15))
        self.main_search.bind("<Return>", self.search_triggered)

        # Selected count
        self.selected_label = ctk.CTkLabel(
            left_action,
            text="0 Selected",
            text_color="#2563eb",
            font=("Arial Bold", 12),
        )
        self.selected_label.pack(side="left")

        right_action = ctk.CTkFrame(action_bar, fg_color="transparent")
        right_action.pack(side="right", padx=15)

        # label paging (bisa kita update kalau perlu)
        self.pagination_label = ctk.CTkLabel(
            right_action,
            text=f"1 - {len(self.patients_data)} of {len(self.patients_data)}",
            text_color="#666",
            font=("Arial", 12),
        )
        self.pagination_label.pack(side="left", padx=10)

        # tombol tambah pasien
        self.add_patient_button = ctk.CTkButton(
            right_action,
            text="+ Pasien",
            width=110,
            height=35,
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="white",
            font=("Arial Bold", 13),
            corner_radius=8,
            command=self.open_add_patient,
        )
        self.add_patient_button.pack(side="left", padx=10)

        # ==================== TABLE ====================
        self.table_frame = ctk.CTkScrollableFrame(
            self.main_content, fg_color="white", corner_radius=0
        )
        self.table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        self.render_table()

    def render_table(self):
        """Pilih tabel mana yang ditampilkan berdasarkan menu aktif."""
        # bersihkan konten lama
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = []
        self.selected_rows = []

        if self.current_menu == "Dokter":
            total = len(self.doctors_data)
            self.pagination_label.configure(text=f"1 - {total} of {total}")
            self.render_doctor_table()

        elif self.current_menu == "Questions":
            total = len(self.questions_data)
            self.pagination_label.configure(text=f"1 - {total} of {total}")
            self.render_question_table()

        elif self.current_menu == "Role":
            total = len(self.roles_data)
            self.pagination_label.configure(text=f"1 - {total} of {total}")
            self.render_role_table()

        else:  # default: Pasien
            total = len(self.patients_data)
            self.pagination_label.configure(text=f"1 - {total} of {total}")
            self.render_patient_table()

    def render_patient_table(self):
        """Render tabel pasien."""

        # Header
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#fafafa", height=50)
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

        # Rows
        for idx, row_data in enumerate(self.patients_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white", height=70)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            widths = [50, 280, 220, 220, 200, 130]

            # === KOLOM 1: Checkbox ===
            checkbox_container = ctk.CTkFrame(
                row_frame, fg_color="transparent", width=widths[0]
            )
            checkbox_container.pack(side="left", padx=5)
            checkbox_container.pack_propagate(False)

            var = ctk.BooleanVar(value=False)
            self.checkbox_vars.append(var)

            check = ctk.CTkCheckBox(
                checkbox_container,
                text="",
                variable=var,
                command=self.update_selection_count,
                checkbox_width=18,
                checkbox_height=18,
                fg_color="#1e5a9e",
                hover_color="#1d4ed8",
            )
            check.place(relx=0.5, rely=0.5, anchor="center")

            # === KOLOM 2: Avatar + Nama Pasien ===
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

            # === KOLOM 3: Diagnosa ===
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

            # === KOLOM 4: Jenis ===
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

            # === KOLOM 5: Kategori Mingguan ===
            kategori_frame = ctk.CTkFrame(
                row_frame, fg_color="transparent", width=widths[4]
            )
            kategori_frame.pack(side="left", padx=5)
            kategori_frame.pack_propagate(False)

            kategori = row_data[3]
            badge_bg = self.badge_color(kategori)

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

            # === KOLOM 6: Aksi (Edit / Hapus) ===
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
                command=lambda i=idx: self.open_edit_patient(i),
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
                command=lambda i=idx: self.delete_patient(i),
            )
            delete_btn.pack(side="left", padx=4, pady=10)

    def render_doctor_table(self):
        """Render tabel dokter."""

        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#fafafa", height=50)
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

        for idx, row_data in enumerate(self.doctors_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white", height=70)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            # === KOLOM 1: checkbox ===
            checkbox_container = ctk.CTkFrame(
                row_frame, fg_color="transparent", width=widths[0]
            )
            checkbox_container.pack(side="left", padx=5)
            checkbox_container.pack_propagate(False)

            var = ctk.BooleanVar(value=False)
            self.checkbox_vars.append(var)

            check = ctk.CTkCheckBox(
                checkbox_container,
                text="",
                variable=var,
                command=self.update_selection_count,
                checkbox_width=18,
                checkbox_height=18,
                fg_color="#1e5a9e",
                hover_color="#1d4ed8",
            )
            check.place(relx=0.5, rely=0.5, anchor="center")

            # === KOLOM 2: Nama dokter ===
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
                text=row_data[1],  # spesialis
                font=("Arial", 10),
                text_color="#999",
                anchor="w",
            ).pack(anchor="w")

            # === KOLOM 3: Spesialis ===
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

            # === KOLOM 4: Tempat praktik ===
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

            # === KOLOM 5: Status ===
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

            # === KOLOM 6: Aksi ===
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
                command=lambda i=idx: self.open_edit_doctor(i),
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
                command=lambda i=idx: self.delete_doctor(i),
            )
            delete_btn.pack(side="left", padx=4, pady=10)

    def render_question_table(self):
        """Render tabel item pertanyaan (WHO-5, dsb)."""

        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#fafafa", height=50)
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

        for idx, row in enumerate(self.questions_data):
            nomor, teks, nama_set, item_dict = row

            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white", height=70)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            # kolom 1: checkbox
            checkbox_container = ctk.CTkFrame(
                row_frame, fg_color="transparent", width=widths[0]
            )
            checkbox_container.pack(side="left", padx=5)
            checkbox_container.pack_propagate(False)

            var = ctk.BooleanVar(value=False)
            self.checkbox_vars.append(var)

            check = ctk.CTkCheckBox(
                checkbox_container,
                text="",
                variable=var,
                command=self.update_selection_count,
                checkbox_width=18,
                checkbox_height=18,
                fg_color="#1e5a9e",
                hover_color="#1d4ed8",
            )
            check.place(relx=0.5, rely=0.5, anchor="center")

            # kolom 2: nomor
            no_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[1])
            no_frame.pack(side="left", padx=5)
            no_frame.pack_propagate(False)

            ctk.CTkLabel(
                no_frame,
                text=str(nomor),
                font=("Arial Bold", 12),
                text_color="#111",
            ).place(relx=0.5, rely=0.5, anchor="center")

            # kolom 3: teks pertanyaan
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

            # kolom 4: nama set
            set_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[3])
            set_frame.pack(side="left", padx=5)
            set_frame.pack_propagate(False)

            ctk.CTkLabel(
                set_frame,
                text=nama_set,
                font=("Arial", 12),
                text_color="#333",
                anchor="center",
            ).place(relx=0.5, rely=0.5, anchor="center")

            # kolom 5: aksi
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
                command=lambda i=idx: self.open_edit_question(i),
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
                command=lambda i=idx: self.delete_question(i),
            )
            delete_btn.pack(side="left", padx=4, pady=10)

    def render_role_table(self):
        """Render tabel role (Admin / Dokter / Pasien)."""

        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#fafafa", height=50)
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

        for idx, row in enumerate(self.roles_data):
            rid, nama_role, role_dict = row

            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white", height=60)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            # kolom 1: checkbox
            checkbox_container = ctk.CTkFrame(
                row_frame, fg_color="transparent", width=widths[0]
            )
            checkbox_container.pack(side="left", padx=5)
            checkbox_container.pack_propagate(False)

            var = ctk.BooleanVar(value=False)
            self.checkbox_vars.append(var)

            check = ctk.CTkCheckBox(
                checkbox_container,
                text="",
                variable=var,
                command=self.update_selection_count,
                checkbox_width=18,
                checkbox_height=18,
                fg_color="#1e5a9e",
                hover_color="#1d4ed8",
            )
            check.place(relx=0.5, rely=0.5, anchor="center")

            # kolom 2: ID
            id_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[1])
            id_frame.pack(side="left", padx=5)
            id_frame.pack_propagate(False)

            ctk.CTkLabel(
                id_frame,
                text=str(rid),
                font=("Arial Bold", 12),
                text_color="#111",
            ).place(relx=0.5, rely=0.5, anchor="center")

            # kolom 3: nama role
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

            # kolom 4: aksi
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
                command=lambda i=idx: self.open_edit_role(i),
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
                command=lambda i=idx: self.delete_role(i),
            )
            delete_btn.pack(side="left", padx=4, pady=10)

    def update_selection_count(self):
        """Update label jumlah yang dipilih"""
        count = sum(1 for var in self.checkbox_vars if var.get())
        self.selected_label.configure(text=f"{count} Selected")

    def search_triggered(self, event):
        """Handle search"""
        keyword = self.main_search.get()
        print(f"Searching for: {keyword}")

    def menu_clicked(self, menu_name):
        """Handle menu click"""
        print(f"Menu clicked: {menu_name}")
        self.current_menu = menu_name

        if menu_name == "Pasien":
            self.add_patient_button.configure(
                text="+ Pasien",
                command=self.open_add_patient,
            )
            self.patients_data = self.load_patients_from_json()
            self.render_table()

        elif menu_name == "Dokter":
            self.add_patient_button.configure(
                text="+ Dokter",
                command=self.open_add_doctor,
            )
            self.doctors_data = self.load_doctors_from_json()
            self.render_table()

        elif menu_name == "Questions":
            self.add_patient_button.configure(
                text="+ Pertanyaan",
                command=self.open_add_question,
            )
            self.question_sets = self.load_question_sets()
            self.questions_data = self.load_questions_from_json()
            self.render_table()

        elif menu_name == "Role":
            self.add_patient_button.configure(
                text="+ Role",
                command=self.open_add_role,
            )
            self.roles_data = self.load_roles_from_json()
            self.render_table()

        else:
            messagebox.showinfo("Info", f"Menu '{menu_name}' belum diimplementasikan.")

    # ========== CRUD PASIEN ==========

    def open_add_patient(self):
        self.open_patient_form(mode="add")

    def open_edit_patient(self, row_index: int):
        """Buka form edit untuk baris tertentu"""
        row = self.patients_data[row_index]
        pasien_dict = row[4]
        self.open_patient_form(mode="edit", pasien=pasien_dict)

    def open_patient_form(self, mode="add", pasien=None):
        """Form tambah / edit pasien (admin)"""
        is_edit = mode == "edit"

        win = ctk.CTkToplevel(self.window)
        win.title("Edit Pasien" if is_edit else "Tambah Pasien")
        win.geometry("520x650")
        win.grab_set()
        self.patient_form_window = win

        frame = ctk.CTkFrame(win, fg_color="#f9fafb")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = "Edit Data Pasien" if is_edit else "Tambah Pasien Baru"
        ctk.CTkLabel(
            frame, text=title, font=("Arial Bold", 20), text_color="#111827"
        ).pack(pady=(5, 15))

        # helper label + entry
        def add_entry(label, initial=""):
            lbl = ctk.CTkLabel(
                frame, text=label, font=("Arial", 12), text_color="#4b5563"
            )
            lbl.pack(anchor="w", pady=(6, 0))
            ent = ctk.CTkEntry(frame, height=32)
            ent.pack(fill="x", pady=(0, 2))
            if initial:
                ent.insert(0, initial)
            return ent

        # ---- Bagian akun login (hanya saat tambah) ----
        if not is_edit:
            self.form_username = add_entry("Username login pasien")
            self.form_password = add_entry("Password login pasien")

            self.form_id_dokter = add_entry("ID Dokter (angka, mis. 1)")

        else:
            # saat edit: simpan id & id_dokter yang ada
            self.form_username = None
            self.form_password = None
            self.form_id_dokter = None
            self.edit_pasien_id = pasien.get("id")
            self.edit_pasien_id_dokter = pasien.get("id_dokter")

        # ---- Biodata ----
        nama_awal = pasien.get("nama", "") if is_edit else ""
        self.form_nama = add_entry("Nama lengkap", nama_awal)

        # Jenis kelamin
        ctk.CTkLabel(
            frame, text="Jenis kelamin", font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(6, 0))

        self.form_gender = ctk.CTkOptionMenu(
            frame,
            values=["Pilih", "Laki-laki", "Perempuan"],
            height=32,
        )
        if is_edit:
            jk = pasien.get("jenis_kelamin", "Pilih")
            if jk not in ["Laki-laki", "Perempuan"]:
                jk = "Pilih"
            self.form_gender.set(jk)
        else:
            self.form_gender.set("Pilih")
        self.form_gender.pack(fill="x", pady=(0, 2))

        pendidikan_awal = pasien.get("pendidikan", "") if is_edit else ""
        self.form_pendidikan = add_entry("Pendidikan", pendidikan_awal)

        pekerjaan_awal = pasien.get("pekerjaan", "") if is_edit else ""
        self.form_pekerjaan = add_entry("Pekerjaan", pekerjaan_awal)

        ctk.CTkLabel(
            frame, text="Diagnosa", font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(6, 0))

        self.form_diagnosa = ctk.CTkTextbox(frame, height=80)
        self.form_diagnosa.pack(fill="x", pady=(0, 10))
        if is_edit:
            self.form_diagnosa.insert("1.0", pasien.get("diagnosa", ""))

        # tombol simpan & batal
        btn_save = ctk.CTkButton(
            frame,
            text="Simpan",
            height=36,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=lambda: self.save_patient_form(mode, pasien),
        )
        btn_save.pack(fill="x", pady=(10, 4))

        ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        ).pack(fill="x")

    def save_patient_form(self, mode, pasien_lama=None):
        """Simpan hasil form (tambah / edit) ke JSON"""
        is_edit = mode == "edit"

        nama = (self.form_nama.get() or "").strip()
        gender = self.form_gender.get()
        pendidikan = (self.form_pendidikan.get() or "").strip()
        pekerjaan = (self.form_pekerjaan.get() or "").strip()
        diagnosa = (self.form_diagnosa.get("1.0", "end") or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama pasien wajib diisi.")
            return

        if gender == "Pilih":
            gender = ""

        # load file pasien
        pasien_list = self._load_json_file(self.pasien_file)

        if is_edit:
            # update pasien yang ada
            target_id = pasien_lama.get("id")
            updated = False
            for p in pasien_list:
                if p.get("id") == target_id:
                    p["nama"] = nama
                    p["jenis_kelamin"] = gender
                    p["pendidikan"] = pendidikan
                    p["pekerjaan"] = pekerjaan
                    p["diagnosa"] = diagnosa
                    updated = True
                    break

            if not updated:
                messagebox.showerror("Error", "Pasien tidak ditemukan di database.")
                return

            self._save_json_file(self.pasien_file, pasien_list)
            messagebox.showinfo("Berhasil", "Data pasien berhasil diperbarui.")

        else:
            # tambah pasien + akun login dasar
            username = (self.form_username.get() or "").strip()
            password = (self.form_password.get() or "").strip()
            id_dokter_str = (self.form_id_dokter.get() or "").strip()

            if not username or not password:
                messagebox.showerror("Error", "Username dan password wajib diisi.")
                return

            # load users
            users = self._load_json_file(self.users_file)

            # cek username unik
            for u in users:
                if u.get("username") == username:
                    messagebox.showerror("Error", "Username sudah digunakan.")
                    return

            new_user_id = max([u.get("id", 0) for u in users], default=0) + 1
            new_pasien_id = max([p.get("id", 0) for p in pasien_list], default=0) + 1

            try:
                id_dokter = int(id_dokter_str) if id_dokter_str else 0
            except ValueError:
                messagebox.showerror("Error", "ID Dokter harus berupa angka.")
                return

            new_user = {
                "id": new_user_id,
                "username": username,
                "password": password,
                "id_role": 3,
            }
            users.append(new_user)

            new_pasien = {
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
            pasien_list.append(new_pasien)

            self._save_json_file(self.users_file, users)
            self._save_json_file(self.pasien_file, pasien_list)

            messagebox.showinfo("Berhasil", "Data pasien baru berhasil ditambahkan.")

        # refresh tabel & tutup form
        self.patients_data = self.load_patients_from_json()
        self.render_table()
        if hasattr(self, "patient_form_window"):
            self.patient_form_window.destroy()

    def delete_patient(self, row_index: int):
        """Hapus pasien dari JSON"""
        row = self.patients_data[row_index]
        pasien = row[4]
        nama = pasien.get("nama", "Pasien")
        target_id = pasien.get("id")

        if not target_id:
            messagebox.showerror("Error", "Pasien tidak memiliki ID valid.")
            return

        if not messagebox.askyesno("Konfirmasi", f"Hapus data pasien '{nama}'?"):
            return

        pasien_list = self._load_json_file(self.pasien_file)
        pasien_list = [p for p in pasien_list if p.get("id") != target_id]
        self._save_json_file(self.pasien_file, pasien_list)

        # refresh tabel
        self.patients_data = self.load_patients_from_json()
        self.render_table()

        # ========== CRUD DOKTER ==========

    def open_add_doctor(self):
        self.open_doctor_form(mode="add")

    def open_edit_doctor(self, row_index: int):
        row = self.doctors_data[row_index]
        dokter = row[4]
        self.open_doctor_form(mode="edit", dokter=dokter)

    def open_doctor_form(self, mode="add", dokter=None):
        is_edit = mode == "edit"

        win = ctk.CTkToplevel(self.window)
        win.title("Edit Dokter" if is_edit else "Tambah Dokter")
        win.geometry("520x520")
        win.grab_set()
        self.doctor_form_window = win

        frame = ctk.CTkFrame(win, fg_color="#f9fafb")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = "Edit Data Dokter" if is_edit else "Tambah Dokter Baru"
        ctk.CTkLabel(
            frame, text=title, font=("Arial Bold", 20), text_color="#111827"
        ).pack(pady=(5, 15))

        def add_entry(label, initial=""):
            lbl = ctk.CTkLabel(
                frame, text=label, font=("Arial", 12), text_color="#4b5563"
            )
            lbl.pack(anchor="w", pady=(6, 0))
            ent = ctk.CTkEntry(frame, height=32)
            ent.pack(fill="x", pady=(0, 2))
            if initial:
                ent.insert(0, initial)
            return ent

        if not is_edit:
            self.doc_username = add_entry("Username login dokter")
            self.doc_password = add_entry("Password login dokter")
        else:
            self.doc_username = None
            self.doc_password = None
            self.edit_dokter_id = dokter.get("id")
            self.edit_dokter_id_user = dokter.get("id_user")

        nama_awal = dokter.get("nama", "") if is_edit else ""
        self.doc_nama = add_entry("Nama dokter", nama_awal)

        spes_awal = dokter.get("spesialis", "") if is_edit else ""
        self.doc_spesialis = add_entry("Spesialis", spes_awal)

        tmp_awal = (
            dokter.get("tempat_praktik", dokter.get("tempat_kerja", ""))
            if is_edit
            else ""
        )
        self.doc_tempat = add_entry("Tempat praktik", tmp_awal)

        hp_awal = dokter.get("no_hp", "") if is_edit else ""
        self.doc_nohp = add_entry("No. HP", hp_awal)

        btn_save = ctk.CTkButton(
            frame,
            text="Simpan",
            height=36,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=lambda: self.save_doctor_form(mode, dokter),
        )
        btn_save.pack(fill="x", pady=(12, 4))

        ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        ).pack(fill="x")

    def save_doctor_form(self, mode, dokter_lama=None):
        is_edit = mode == "edit"

        nama = (self.doc_nama.get() or "").strip()
        spesialis = (self.doc_spesialis.get() or "").strip()
        tempat = (self.doc_tempat.get() or "").strip()
        no_hp = (self.doc_nohp.get() or "").strip()

        if not nama:
            messagebox.showerror("Error", "Nama dokter wajib diisi.")
            return

        dokter_list = self._load_json_file(self.dokter_file)

        if is_edit:
            target_id = dokter_lama.get("id")
            updated = False
            for d in dokter_list:
                if d.get("id") == target_id:
                    d["nama"] = nama
                    d["spesialis"] = spesialis
                    d["tempat_praktik"] = tempat
                    d["no_hp"] = no_hp
                    updated = True
                    break

            if not updated:
                messagebox.showerror("Error", "Dokter tidak ditemukan di database.")
                return

            self._save_json_file(self.dokter_file, dokter_list)
            messagebox.showinfo("Berhasil", "Data dokter berhasil diperbarui.")

        else:
            username = (self.doc_username.get() or "").strip()
            password = (self.doc_password.get() or "").strip()

            if not username or not password:
                messagebox.showerror("Error", "Username dan password wajib diisi.")
                return

            users = self._load_json_file(self.users_file)

            for u in users:
                if u.get("username") == username:
                    messagebox.showerror("Error", "Username sudah digunakan.")
                    return

            new_user_id = max([u.get("id", 0) for u in users], default=0) + 1
            new_dokter_id = max([d.get("id", 0) for d in dokter_list], default=0) + 1

            new_user = {
                "id": new_user_id,
                "username": username,
                "password": password,
                "id_role": 2,  # dokter
            }
            users.append(new_user)

            new_dokter = {
                "id": new_dokter_id,
                "id_user": new_user_id,
                "nama": nama,
                "spesialis": spesialis,
                "tempat_praktik": tempat,
                "no_hp": no_hp,
            }
            dokter_list.append(new_dokter)

            self._save_json_file(self.users_file, users)
            self._save_json_file(self.dokter_file, dokter_list)

            messagebox.showinfo("Berhasil", "Data dokter baru berhasil ditambahkan.")

        # refresh tabel & tutup
        self.doctors_data = self.load_doctors_from_json()
        self.render_table()
        if hasattr(self, "doctor_form_window"):
            self.doctor_form_window.destroy()

    def delete_doctor(self, row_index: int):
        row = self.doctors_data[row_index]
        dokter = row[4]
        nama = dokter.get("nama", "Dokter")
        target_id = dokter.get("id")

        if not target_id:
            messagebox.showerror("Error", "Dokter tidak memiliki ID valid.")
            return

        if not messagebox.askyesno("Konfirmasi", f"Hapus data dokter '{nama}'?"):
            return

        dokter_list = self._load_json_file(self.dokter_file)
        dokter_list = [d for d in dokter_list if d.get("id") != target_id]
        self._save_json_file(self.dokter_file, dokter_list)

        self.doctors_data = self.load_doctors_from_json()
        self.render_table()

    # ========== CRUD QUESTIONS ==========

    def open_add_question(self):
        self.open_question_form(mode="add")

    def open_edit_question(self, row_index: int):
        row = self.questions_data[row_index]
        item = row[3]  # dict item_pertanyaan
        self.open_question_form(mode="edit", item=item)

    def open_question_form(self, mode="add", item=None):
        is_edit = mode == "edit"

        win = ctk.CTkToplevel(self.window)
        win.title("Edit Pertanyaan" if is_edit else "Tambah Pertanyaan")
        win.geometry("520x430")
        win.grab_set()
        self.question_form_window = win

        frame = ctk.CTkFrame(win, fg_color="#f9fafb")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = "Edit Item Pertanyaan" if is_edit else "Tambah Item Pertanyaan"
        ctk.CTkLabel(
            frame, text=title, font=("Arial Bold", 20), text_color="#111827"
        ).pack(pady=(5, 15))

        # --- pilih set pertanyaan ---
        sets_list = list(self.question_sets.values())
        if not sets_list:  # kalau belum ada set sama sekali
            ctk.CTkLabel(
                frame,
                text="Belum ada set_pertanyaan di set_pertanyaan.json",
                font=("Arial", 11),
                text_color="#b91c1c",
            ).pack(pady=(0, 10))
            self.q_set_display_to_id = {}
            set_values = ["-"]
        else:
            set_values = [f"{s.get('id')} - {s.get('nama_set', '')}" for s in sets_list]
            self.q_set_display_to_id = {
                f"{s.get('id')} - {s.get('nama_set', '')}": s.get("id")
                for s in sets_list
            }

        ctk.CTkLabel(
            frame, text="Set Pertanyaan", font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(4, 0))

        self.q_set_menu = ctk.CTkOptionMenu(frame, values=set_values, height=32)
        if is_edit:
            current_set_id = item.get("id_set_pertanyaan")
            current_disp = next(
                (k for k, v in self.q_set_display_to_id.items() if v == current_set_id),
                set_values[0],
            )
            self.q_set_menu.set(current_disp)
        else:
            self.q_set_menu.set(set_values[0])
        self.q_set_menu.pack(fill="x", pady=(0, 8))

        # --- nomor urut ---
        ctk.CTkLabel(
            frame, text="Nomor urut", font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(4, 0))

        self.q_nomor = ctk.CTkEntry(frame, height=32)
        self.q_nomor.pack(fill="x", pady=(0, 8))
        if is_edit:
            self.q_nomor.insert(0, str(item.get("nomor_urut", "")))

        # --- teks pertanyaan ---
        ctk.CTkLabel(
            frame, text="Teks pertanyaan", font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(4, 0))

        self.q_teks = ctk.CTkTextbox(frame, height=120)
        self.q_teks.pack(fill="x", pady=(0, 10))
        if is_edit:
            self.q_teks.insert("1.0", item.get("teks_pertanyaan", ""))

        btn_save = ctk.CTkButton(
            frame,
            text="Simpan",
            height=36,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=lambda: self.save_question_form(mode, item),
        )
        btn_save.pack(fill="x", pady=(10, 4))

        ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        ).pack(fill="x")

    def save_question_form(self, mode, item_lama=None):
        is_edit = mode == "edit"

        disp = self.q_set_menu.get()
        set_id = self.q_set_display_to_id.get(disp)
        nomor_str = (self.q_nomor.get() or "").strip()
        teks = (self.q_teks.get("1.0", "end") or "").strip()

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

        items = self._load_json_file(self.item_file)

        if is_edit:
            target_id = item_lama.get("id")
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

            self._save_json_file(self.item_file, items)
            messagebox.showinfo("Berhasil", "Pertanyaan berhasil diperbarui.")

        else:
            new_id = max([it.get("id", 0) for it in items], default=0) + 1
            new_item = {
                "id": new_id,
                "id_set_pertanyaan": set_id,
                "nomor_urut": nomor,
                "teks_pertanyaan": teks,
            }
            items.append(new_item)
            self._save_json_file(self.item_file, items)
            messagebox.showinfo("Berhasil", "Pertanyaan baru berhasil ditambahkan.")

        # refresh tabel
        self.question_sets = self.load_question_sets()
        self.questions_data = self.load_questions_from_json()
        self.render_table()
        if hasattr(self, "question_form_window"):
            self.question_form_window.destroy()

    def delete_question(self, row_index: int):
        row = self.questions_data[row_index]
        item = row[3]
        teks = item.get("teks_pertanyaan", "")[:40] + "..."
        target_id = item.get("id")

        if not target_id:
            messagebox.showerror("Error", "Item pertanyaan tidak memiliki ID valid.")
            return

        if not messagebox.askyesno("Konfirmasi", f'Hapus pertanyaan:\n"{teks}" ?'):
            return

        items = self._load_json_file(self.item_file)
        items = [it for it in items if it.get("id") != target_id]
        self._save_json_file(self.item_file, items)

        self.questions_data = self.load_questions_from_json()
        self.render_table()

    # ========== CRUD ROLE ==========

    def open_add_role(self):
        self.open_role_form(mode="add")

    def open_edit_role(self, row_index: int):
        row = self.roles_data[row_index]
        role_dict = row[2]
        self.open_role_form(mode="edit", role=role_dict)

    def open_role_form(self, mode="add", role=None):
        is_edit = mode == "edit"

        win = ctk.CTkToplevel(self.window)
        win.title("Edit Role" if is_edit else "Tambah Role")
        win.geometry("420x260")
        win.grab_set()
        self.role_form_window = win

        frame = ctk.CTkFrame(win, fg_color="#f9fafb")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = "Edit Role" if is_edit else "Tambah Role Baru"
        ctk.CTkLabel(
            frame, text=title, font=("Arial Bold", 20), text_color="#111827"
        ).pack(pady=(5, 15))

        if is_edit:
            ctk.CTkLabel(
                frame,
                text=f"ID Role: {role.get('id')}",
                font=("Arial", 11),
                text_color="#6b7280",
            ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            frame, text="Nama role", font=("Arial", 12), text_color="#4b5563"
        ).pack(anchor="w", pady=(6, 0))

        self.role_nama = ctk.CTkEntry(frame, height=32)
        self.role_nama.pack(fill="x", pady=(0, 10))

        if is_edit:
            self.role_nama.insert(0, role.get("nama_role", ""))

        btn_save = ctk.CTkButton(
            frame,
            text="Simpan",
            height=36,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=lambda: self.save_role_form(mode, role),
        )
        btn_save.pack(fill="x", pady=(10, 4))

        ctk.CTkButton(
            frame,
            text="Batal",
            height=32,
            fg_color="#e5e7eb",
            text_color="#111827",
            hover_color="#d1d5db",
            command=win.destroy,
        ).pack(fill="x")

    def save_role_form(self, mode, role_lama=None):
        is_edit = mode == "edit"

        nama = (self.role_nama.get() or "").strip()
        if not nama:
            messagebox.showerror("Error", "Nama role wajib diisi.")
            return

        roles = self._load_json_file(self.role_file)

        if is_edit:
            target_id = role_lama.get("id")
            updated = False
            for r in roles:
                if r.get("id") == target_id:
                    r["nama_role"] = nama
                    updated = True
                    break

            if not updated:
                messagebox.showerror("Error", "Role tidak ditemukan di database.")
                return

            self._save_json_file(self.role_file, roles)
            messagebox.showinfo("Berhasil", "Data role berhasil diperbarui.")

        else:
            new_id = max([r.get("id", 0) for r in roles], default=0) + 1
            new_role = {"id": new_id, "nama_role": nama}
            roles.append(new_role)
            self._save_json_file(self.role_file, roles)
            messagebox.showinfo("Berhasil", "Role baru berhasil ditambahkan.")

        self.roles_data = self.load_roles_from_json()
        self.render_table()
        if hasattr(self, "role_form_window"):
            self.role_form_window.destroy()

    def delete_role(self, row_index: int):
        row = self.roles_data[row_index]
        role = row[2]
        rid = role.get("id")
        nama = role.get("nama_role", "Role")

        if not rid:
            messagebox.showerror("Error", "Role tidak memiliki ID valid.")
            return

        # cek apakah masih dipakai di users.json
        users = self._load_json_file(self.users_file)
        used_count = sum(1 for u in users if u.get("id_role") == rid)
        if used_count > 0:
            messagebox.showerror(
                "Tidak bisa dihapus",
                f"Role '{nama}' masih digunakan oleh {used_count} user.",
            )
            return

        if not messagebox.askyesno("Konfirmasi", f"Hapus role '{nama}'?"):
            return

        roles = self._load_json_file(self.role_file)
        roles = [r for r in roles if r.get("id") != rid]
        self._save_json_file(self.role_file, roles)

        self.roles_data = self.load_roles_from_json()
        self.render_table()

    def run(self):
        """Jalankan aplikasi"""
        self.window.mainloop()


# ==================== MAIN PROGRAM ====================
if __name__ == "__main__":
    contoh_user = {"Nama": "Admin"}
    app = ModernDashboard(contoh_user)
    app.run()

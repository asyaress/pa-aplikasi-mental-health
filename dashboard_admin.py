# Import library yang dibutuhkan
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

        self.user = user  # Simpan data user yang login
        self.json_file = "pasien.json"  # Nama file JSON
        
        # Data dummy untuk demo
        self.patients_data = self.load_patients_from_json()
        
        # State untuk checkbox selection
        self.selected_rows = []  # List untuk menyimpan row yang dipilih
        self.checkbox_vars = []  # List untuk menyimpan checkbox variables

        self.build_ui()  # Panggil fungsi untuk membangun UI

    def load_patients_from_json(self):
        """Fungsi untuk membaca data pasien dari file JSON"""
        try:
            if not os.path.exists(self.json_file):
                # Jika file tidak ada, return data dummy
                return self.get_dummy_data()
            
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            patients = []
            for p in data:
                nama = p.get("nama", "Unknown")
                diagnosa = p.get("diagnosa", "Tidak ada diagnosa")
                pekerjaan = p.get("pekerjaan", "Tidak bekerja")
                kategori = self.determine_kategori(diagnosa)
                
                patients.append([nama, diagnosa, pekerjaan, kategori, p])
            
            return patients if patients else self.get_dummy_data()
        
        except:
            return self.get_dummy_data()

    def get_dummy_data(self):
        """Data dummy jika JSON tidak ada"""
        return [
            ["Cell Content", "Gangguan Kecemasan", "Pelajar (SMA)", "Cell Content", {}],
            ["Cell Content", "Bipolar", "Pelajar (Mahasiswa)", "Cell Content", {}],
            ["Cell Content", "Anxiety", "Pekerja Kontrak", "Cell Content", {}],
            ["Cell Content", "OCD", "Pekerja Lepas", "Cell Content", {}],
            ["Cell Content", "Skizofrenia", "Sedang Mencari Pekerjaan", "Cell Content", {}],
            ["Cell Content", "Gangguan tidur", "Pekerja Keras", "Cell Content", {}],
            ["Cell Content", "Insomnia", "Pelajar", "Cell Content", {}],
            ["Cell Content", "Moody", "Pelajar", "Cell Content", {}],
            ["Cell Content", "Gangguan makan", "Pekerja Tetap", "Cell Content", {}],
            ["Cell Content", "Depresi", "Pekerja Lepas", "Cell Content", {}],
        ]

    def determine_kategori(self, diagnosa):
        """Fungsi untuk menentukan kategori risiko"""
        diagnosa_lower = diagnosa.lower()
        
        if any(word in diagnosa_lower for word in ["berat", "akut", "parah", "skizofrenia", "bipolar"]):
            return "Berisiko"
        elif any(word in diagnosa_lower for word in ["ringan", "minor"]):
            return "Memadai"
        else:
            return "Rendah"

    def build_ui(self):
        """Fungsi untuk membangun semua elemen UI"""
        
        # ==================== SIDEBAR KIRI (Blue) ====================
        self.sidebar = ctk.CTkFrame(
            self.window,
            fg_color="#1e5a9e",  # Biru
            width=250,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Fixed width

        # Logo/Title
        ctk.CTkLabel(
            self.sidebar,
            text="Dashboard",
            font=("Arial Bold", 24),
            text_color="white"
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
            corner_radius=8
        )
        self.sidebar_search.pack(fill="x")

        # Menu items
        menu_items = [
            ("Pasien", "👥"),
            ("Dokter", "👨‍⚕️"),
            ("Questions", "❓"),
            ("Role", "🔐")
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
                command=lambda i=item: self.menu_clicked(i)
            )
            btn.pack(fill="x", padx=20, pady=2)
            
            # Tambahkan arrow
            arrow_label = ctk.CTkLabel(
                btn,
                text="›",
                font=("Arial", 20),
                text_color="white"
            )
            arrow_label.place(relx=0.95, rely=0.5, anchor="e")

        # ==================== MAIN CONTENT AREA ====================
        self.main_content = ctk.CTkFrame(
            self.window,
            fg_color="#f5f5f5",
            corner_radius=0
        )
        self.main_content.pack(side="right", fill="both", expand=True)

        # ==================== ACTION BAR ====================
        action_bar = ctk.CTkFrame(
            self.main_content,
            fg_color="white",
            height=60,
            corner_radius=0
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
            font=("Arial", 18)
        ).pack(side="left", padx=(0, 10))

        self.main_search = ctk.CTkEntry(
            left_action,
            placeholder_text="🔍 Search",
            width=250,
            height=35,
            border_width=1,
            border_color="#ddd",
            fg_color="white"
        )
        self.main_search.pack(side="left", padx=(0, 15))
        self.main_search.bind("<Return>", self.search_triggered)

        # Selected count
        self.selected_label = ctk.CTkLabel(
            left_action,
            text="0 Selected",
            text_color="#2563eb",
            font=("Arial Bold", 12)
        )
        self.selected_label.pack(side="left")

        # Right side - Pagination & Actions
        right_action = ctk.CTkFrame(action_bar, fg_color="transparent")
        right_action.pack(side="right", padx=15)

        ctk.CTkLabel(
            right_action,
            text=f"1 - 10 of {len(self.patients_data)}",
            text_color="#666",
            font=("Arial", 12)
        ).pack(side="left", padx=10)

        # Settings icon (right)
        ctk.CTkButton(
            right_action,
            text="⚙",
            width=35,
            height=35,
            fg_color="transparent",
            text_color="#666",
            hover_color="#f0f0f0",
            font=("Arial", 18)
        ).pack(side="left")

        # ==================== TABLE ====================
        self.table_frame = ctk.CTkScrollableFrame(
            self.main_content,
            fg_color="white",
            corner_radius=0
        )
        self.table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        self.render_table()

    def render_table(self):
        """Render tabel dengan data"""
        # Clear existing widgets
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.checkbox_vars = []
        self.selected_rows = []

        # Header
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#fafafa", height=50)
        header_frame.pack(fill="x", pady=(0, 1))
        header_frame.pack_propagate(False)

        headers = ["", "Nama Pasien", "Diagnosa", "Jenis", "Kategori Mingguan", "Aksi"]
        widths = [50, 280, 220, 220, 200, 130]

        # Render header
        for i, h in enumerate(headers):
            if i == 0:
                # Kolom kosong untuk checkbox (tapi tidak ada checkbox di header)
                ctk.CTkLabel(
                    header_frame,
                    text="",
                    width=widths[i],
                    font=("Arial Bold", 13),
                    text_color="#333"
                ).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(
                    header_frame,
                    text=h,
                    width=widths[i],
                    font=("Arial Bold", 13),
                    text_color="#333",
                    anchor="center"
                ).pack(side="left", padx=5)

        # Rows
        for idx, row_data in enumerate(self.patients_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white", height=70)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)

            # === KOLOM 1: Checkbox ===
            checkbox_container = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[0])
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
                hover_color="#1d4ed8"
            )
            check.place(relx=0.5, rely=0.5, anchor="center")

            # === KOLOM 2: Avatar + Nama Pasien ===
            name_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[1])
            name_frame.pack(side="left", padx=5)
            name_frame.pack_propagate(False)

            # Avatar circle
            avatar = ctk.CTkLabel(
                name_frame,
                text="👤",
                font=("Arial", 18),
                width=40,
                height=40,
                fg_color="#e5e7eb",
                corner_radius=20
            )
            avatar.pack(side="left", padx=(10, 12), pady=15)

            # Name + Sub Content
            name_container = ctk.CTkFrame(name_frame, fg_color="transparent")
            name_container.pack(side="left", fill="y", expand=True, pady=15)
            
            ctk.CTkLabel(
                name_container,
                text=row_data[0] if row_data[0] != "Cell Content" else "Cell Content",
                font=("Arial Bold", 12),
                text_color="#111",
                anchor="w"
            ).pack(anchor="w", pady=(0, 2))
            
            ctk.CTkLabel(
                name_container,
                text="Sub Content",
                font=("Arial", 10),
                text_color="#999",
                anchor="w"
            ).pack(anchor="w")

            # === KOLOM 3: Diagnosa ===
            diagnosa_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[2])
            diagnosa_frame.pack(side="left", padx=5)
            diagnosa_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                diagnosa_frame,
                text=row_data[1],
                font=("Arial", 12),
                text_color="#333",
                anchor="center"
            ).place(relx=0.5, rely=0.5, anchor="center")

            # === KOLOM 4: Jenis ===
            jenis_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[3])
            jenis_frame.pack(side="left", padx=5)
            jenis_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                jenis_frame,
                text=row_data[2],
                font=("Arial", 12),
                text_color="#333",
                anchor="center"
            ).place(relx=0.5, rely=0.5, anchor="center")

            # === KOLOM 5: Kategori Mingguan ===
            kategori_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[4])
            kategori_frame.pack(side="left", padx=5)
            kategori_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                kategori_frame,
                text="Cell Content",
                font=("Arial", 12),
                text_color="#333",
                anchor="center"
            ).place(relx=0.5, rely=0.5, anchor="center")

            # === KOLOM 6: Aksi ===
            aksi_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=widths[5])
            aksi_frame.pack(side="left", padx=5)
            aksi_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                aksi_frame,
                text="Cell Content",
                font=("Arial", 12),
                text_color="#333",
                anchor="center"
            ).place(relx=0.5, rely=0.5, anchor="center")

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

    def run(self):
        """Jalankan aplikasi"""
        self.window.mainloop()


# ==================== MAIN PROGRAM ====================
if __name__ == "__main__":
    contoh_user = {"Nama": "Admin"}
    app = ModernDashboard(contoh_user)
    app.run()
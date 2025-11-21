import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class dokter2Dashboard:
    def __init__(self, user):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("dashboard dokter ni kids")
        self.window.geometry("1200x700")
        self.window.configure(fg_color="#f8f9fa")

        self.user = user 
        
        # Data Pasien (Tetap)
        self.patients_data = [
            ["Alya", "Gangguan Kecemasan", "Pelajar (SMA)", "Memadai"],
            ["Bella", "Bipolar", "Mahasiswa", "Rendah"],
            ["Rafi", "Anxiety", "Pekerja Kontrak", "Berisiko"],
            ["Nisa", "OCD", "Pekerja Lepas", "Rendah"],
            ["Andi", "Skizofrenia", "Sedang Mencari Kerja", "Rendah"],
        ]

        self.build_ui()

    def build_ui(self):
        # 1. Sidebar (Kiri)
        self.sidebar=ctk.CTkFrame(self.window, fg_color="#ffffff", width = 65, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx =0, pady=0)

        # Menu Sidebar
        ctk.CTkLabel(self.sidebar, text="♾️", font=("Arial", 30), text_color="#007bff").pack(pady=(30, 20))
        ctk.CTkButton(self.sidebar, text="➕", width=50, height=50, text_color="#000000", fg_color="#ffffff", 
                      hover_color="#0e98f5", corner_radius=10).pack(pady=10)
        
        menus = ["🏠", "🗓", "💬", "⏱", "⚙️","↩️"]
        for icon in menus:
            label = ctk.CTkButton(self.sidebar, text=icon, font=("Arial", 20), text_color="#000000", fg_color="transparent", 
                                  hover_color="#0e98f5", width=50, height=50, corner_radius=10)
            label.pack(pady=18)

        # 2. Main Content (Kanan)
        self.main_content = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # 3. ACTION BAR (Wadah untuk Search dan Ikon Aksi)
        self.action_bar = ctk.CTkFrame(self.main_content, fg_color="#ffffff", height=60, corner_radius=10)
        self.action_bar.pack(side="top", fill="x", pady=5, padx=15)

        # 3a. Bagian Kiri (Search)
        self.left_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.left_action.pack(side="left", padx=15, pady=10, fill="y") 

        self.search_entry = ctk.CTkEntry(self.left_action, placeholder_text="🔍 Cari Pasien...", width=250, height=35, 
                                         border_width=1, border_color="#ddd", fg_color="#f9f9f9")
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", self.enter_pressed)
        
        # Tambahkan label "4 Terpilih"
        ctk.CTkLabel(self.left_action, text="4 Terpilih", text_color="#3B8ED0", font=("Arial Bold", 12)).pack(side="left", padx=15)

        # 3b. Bagian Kanan (Icons Aksi)
        right_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        right_action.pack(side="right", padx=15, fill="y") 
        
        ctk.CTkLabel(right_action, text="1 - 10 of 52", text_color="#555", font=("Arial", 12)).pack(side="left", padx=(0, 15))
        ctk.CTkLabel(right_action, text="< >", text_color="#555", font=("Arial Bold", 14)).pack(side="left", padx=(0, 15))
        
        # Tombol Aksi tanpa Lambda
        def create_action_handler(icon_text):
            def handler():
                print(f"Aksi {icon_text} ditekan")
            return handler
        
        for ic in ["Y", "🖨️", "⬇️", "⤢"]:
             ctk.CTkButton(right_action, text=ic, width=35, height=35, fg_color="transparent", 
                          text_color="#555", hover_color="#eee", font=("Arial", 16),
                          command=create_action_handler(ic)).pack(side="left", padx=2),

        # 4. Scrollable Frame untuk Tabel
        self.table_scroll_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="#ffffff", corner_radius=10)
        self.table_scroll_frame.pack(side="top", fill="both", expand=True, pady=(0, 0))

        # Tabel
        self.render_table(self.patients_data)

    # Fungsi untuk membuat handler tanpa lambda, menggunakan closure
    def create_detail_handler(self, row_data):
        def handler():
            self.view_detail(row_data)
        return handler

    def render_table(self, data):
        # Bersihkan konten frame scrollable sebelum render ulang
        for widget in self.table_scroll_frame.winfo_children():
            widget.destroy()

        # Header Tabel
        header_row = ctk.CTkFrame(self.table_scroll_frame, fg_color="#f1f1f1", height=40)
        header_row.pack(fill="x")
        
        headers=["Nama Pasien", "Diagnosa", "Jenis", "Kategori", "Aksi"]
        col_widths=[180, 250, 170, 120, 80]

        for i, h in enumerate(headers):
            label=ctk.CTkLabel(header_row, text=h,
                               font= ("Arial bold", 13),
                               text_color="black",
                               width=col_widths[i],
                               anchor="w"
                                )
            label.pack(side="left", padx=15, pady=5)
            
        # Isi Tabel
        for row_data in data:
            row_frame = ctk.CTkFrame(self.table_scroll_frame,fg_color="#ffffff", height=45)
            row_frame.pack(fill="x", pady=1)

            # Kolom 1 - Nama Pasien
            ctk.CTkLabel(row_frame, text=row_data[0], font=("Arial Bold", 13), 
                         anchor="w", width=col_widths[0]).pack(side="left", padx=15)

            # Kolom 2 - Diagnosa
            ctk.CTkLabel(row_frame, text=row_data[1], width=col_widths[1],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=15)

            # Kolom 3 - Jenis
            ctk.CTkLabel(row_frame, text=row_data[2], width=col_widths[2],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=15)

            badge_color = self.badge_colour(row_data[3])
            
            # Kolom 4 - Kategori (Badge)
            ctk.CTkLabel(row_frame, text=row_data[3], width=col_widths[3]-20, 
                         fg_color=badge_color, corner_radius=6,
                         font=("Arial Bold", 13), text_color="black"
                         ).pack(side="left", padx=15)
            
            # Kolom 5 - Tombol Detail
            ctk.CTkButton(row_frame, text="👁",
                          text_color="#01030E",
                          width=40, height=40,
                          fg_color="transparent",
                          hover_color="#3B8ED0",
                          command=self.create_detail_handler(row_data)
                          ).pack(side="left", padx=25)
            
    def enter_pressed(self, event):
        keyword=self.search_entry.get()
        self.search_patient(keyword)

    def search_patient(self, keyword):
        keyword=keyword.strip()

        if keyword == "":
            self.render_table(self.patients_data)
            return
        
        result = []
        keyword_lower = keyword.lower() 
        for p in self.patients_data:
            nama = p[0].lower()
            if keyword_lower in nama:
                result.append(p)

        if not result:
            messagebox.showinfo("Hasil", "Pasien tidak ditemukan")
        
        self.render_table(result)

    # badge warna per kategori
    def badge_colour(self, kategori):
        if kategori == "Memadai": return "#bbf7d0"
        if kategori == "Rendah": return "#fef08a"
        if kategori == "Berisiko": return "#fecaca"
        return "#e5e7eb"
    
    def view_detail(self, data):
        messagebox.showinfo(
            "Detail Pasien",
            f"Nama: {data[0]}\nDiagnosa: {data[1]}\nJenis: {data[2]}\nKategori: {data[3]}"
        )
    
    def run(self):
        self.window.mainloop()

    
if __name__ == "__main__":
    contoh_user = {"Nama": "dr. Diftya"}
    app = dokter2Dashboard(contoh_user)
    app.run()
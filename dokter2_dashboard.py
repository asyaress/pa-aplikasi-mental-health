import customtkinter as ctk
from tkinter import messagebox
# from PIL import Image # Dihapus karena tidak digunakan

class dokter2Dashboard:
    def __init__(self, user):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("dashboard dokter ni kids")
        self.window.geometry("1200x700")
        self.window.configure(fg_color="#f8f9fa")

        self.user = user 
        

        self.patients_data = [
            ["Alya", "Gangguan Kecemasan", "Pelajar (SMA)", "Memadai"],
            ["Bella", "Bipolar", "Mahasiswa", "Rendah"],
            ["Rafi", "Anxiety", "Pekerja Kontrak", "Berisiko"],
            ["Nisa", "OCD", "Pekerja Lepas", "Rendah"],
            ["Andi", "Skizofrenia", "Sedang Mencari Kerja", "Rendah"],
        ]

        self.build_ui()

    def build_ui(self):

        # sidebar
        self.sidebar=ctk.CTkFrame(self.window, fg_color="#ffffff", width = 65, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx =0, pady=0)

        # menu 
        ctk.CTkLabel(self.sidebar, text="♾️", font=("Arial", 30), text_color="#007bff").pack(pady=(30, 20))
        ctk.CTkButton(self.sidebar, text="➕", width=50, height=50, fg_color="#3B8ED0", 
                      hover_color="#1e70b6", text_color="white", corner_radius=10).pack(pady=10)
        
        menus = ["🏠", "🗓", "💬", "⏱", "⚙️","↩️"]
        for icon in menus:
            label = ctk.CTkButton(self.sidebar, text=icon, font=("Arial", 20), text_color="#000000", fg_color="transparent", 
                                  hover_color="#0e98f5", width=50, height=50, corner_radius=10)
            label.pack(pady=18)

        self.main_content = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # ACTION BAR
        self.action_bar = ctk.CTkFrame(self.main_content, fg_color="#ffffff", height=60, corner_radius=10)
        self.action_bar.pack(side="top", fill="x", pady=(0, 15))

        # (Search)
        self.left_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.left_action.pack(side="left", padx=15, pady=10, fill="y") 

        self.search_entry = ctk.CTkEntry(self.left_action, placeholder_text="🔍 Cari Pasien...", width=250, height=35, 
                                         border_width=1, border_color="#ddd", fg_color="#f9f9f9")
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", self.enter_pressed)
        
        # Tambahkan label "4 Terpilih" yang hilang dari aksi bar
        ctk.CTkLabel(self.left_action, text="4 Terpilih", text_color="#3B8ED0", font=("Arial Bold", 12)).pack(side="left", padx=15)

        # Kanan
        right_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        right_action.pack(side="right", padx=15, fill="y") 
        
        ctk.CTkLabel(right_action, text="1 - 10 of 52", text_color="#555", font=("Arial", 12)).pack(side="left", padx=(0, 15))
        ctk.CTkLabel(right_action, text="< >", text_color="#555", font=("Arial Bold", 14)).pack(side="left", padx=(0, 15))
        
        for ic in ["Y", "🖨️", "⬇️", "⤢"]:
             ctk.CTkButton(right_action, text=ic, width=35, height=35, fg_color="transparent", 
                          text_color="#555", hover_color="#eee", font=("Arial", 16),
                          command=lambda i=ic: print(f"Aksi {i} ditekan")).pack(side="left", padx=2)

        self.table_scroll_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="#ffffff", corner_radius=10)
        self.table_scroll_frame.pack(side="top", fill="both", expand=True, pady=(0, 0))

        # tabel
        self.render_table(self.patients_data)

    def render_table(self, data):
        for widget in self.table_scroll_frame.winfo_children():
            # Widget destroy menghapus semua widget di bawah table frame, tidak ada pengecualian krn buat pencarian ulang
            widget.destroy()


        header_row = ctk.CTkFrame(self.table_scroll_frame, fg_color="#f1f1f1", height=40)
        header_row.pack(fill="x")
        
        headers=["Nama Pasien", "Diagnosa", "Jenis", "Kategori", "Aksi"]
        col_widths=[180, 250, 170, 120, 80]

        # width=col_widths[i] ngambil variabel col_widths sesuai iterasi

        for i, h in enumerate(headers):
            label=ctk.CTkLabel(header_row, text=h,
                               font= ("Arial bold", 13),
                               text_color="black",
                               width=col_widths[i],
                               anchor="w"
                                )
            label.pack(side="left", padx=(10 if i == 0 else 5), pady=10)

        for row_data in data:
            row_frame = ctk.CTkFrame(self.table_scroll_frame,fg_color="#ffffff", height=45)
            row_frame.pack(fill="x", pady=1)

            # Kolom 1 (dengan Ikon Pasien)
            name_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=col_widths[0])
            name_frame.pack(side="left", padx=10)
            ctk.CTkLabel(name_frame, text="👤", font=("Arial", 20), text_color="#888").pack(side="left", padx=(0, 5))
            ctk.CTkLabel(name_frame, text=row_data[0], font=("Arial Bold", 13), anchor="w").pack(side="left")

            ctk.CTkLabel(row_frame, text=row_data[1], width=col_widths[1],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=row_data[2], width=col_widths[2],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=10)

            badge_color = self.badge_colour(row_data[3])
            # Mengurangi lebar badge agar terlihat lebih kecil
            ctk.CTkLabel(row_frame, text=row_data[3], width=col_widths[3]-20, 
                         fg_color=badge_color, corner_radius=6,
                         font=("Arial Bold", 13), text_color="black",
                         ).pack(side="left", padx=10)
            
            # Memperbaiki command ke fungsi handler yang benar
            ctk.CTkButton(row_frame, text="👁",
                          text_color="#01030E",
                          width=40, height=40,
                          fg_color="transparent",
                          hover_color="#eee",
                          command=lambda r_data=row_data: self.view_detail(r_data)
                          ).pack(side="left", padx=45)
            
    def enter_pressed(self, event):
        keyword=self.search_entry.get()
        self.search_patient(keyword)

    def search_patient(self, keyword):
        keyword=keyword.strip()

        if keyword == "":
            self.render_table(self.patients_data)
            return
        
        # Hapus duplikasi check keyword == ""

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
        # Mengganti warna ke versi yang lebih muda agar kontras di light mode
        if kategori == "Memadai": return "#bbf7d0"
        if kategori == "Rendah": return "#fef08a"
        if kategori == "Berisiko": return "#fecaca"
        return "#e5e7eb"
    
    def view_detail(self, data):
        # FIX: JUDUL SUDAH ADA ("Detail Pasien"), TIDAK PERLU DITAMBAH
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
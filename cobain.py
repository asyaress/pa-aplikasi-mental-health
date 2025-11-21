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
        self.sidebar.pack(side="left", fill="y", padx =20, pady=20)

        # menu 
        ctk.CTkLabel(self.sidebar, text="♾️", font=("Arial", 30), text_color="#007bff").pack(pady=(30, 20))
        ctk.CTkButton(self.sidebar, text="➕", width=50, height=50, fg_color="#3B8ED0", 
                      hover_color="#1e70b6", text_color="white", corner_radius=10).pack(pady=10)
        
        menus = ["🏠", "🗓", "💬", "⏱", "⚙️","↩️"]
        for icon in menus:
            label = ctk.CTkButton(self.sidebar, text=icon, font=("Arial", 20), text_color="#000000", fg_color="#FFFFFF", 
                                  hover_color="#0e98f5", width=50, height=50, corner_radius=10)
            label.pack(pady=18)

         # Konten Utama (Kanan) 
        self.main_content = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # ACTION BAR
        self.action_bar = ctk.CTkFrame(self.main_content, fg_color="#ffffff", height=60, corner_radius=10)
        self.action_bar.pack(side="top", fill="x", pady=(0, 15))

        # header
        header = ctk.CTkFrame(self.window, fg_color = "white", height = 60)
        header.pack(fill="x")

        # search bar 

        # 2a. Bagian Kiri (Search)
        self.left_action = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.left_action.pack(side="left", padx=15, pady=10)

        self.search_entry = ctk.CTkEntry(self.left_action, placeholder_text="🔍 Cari Pasien...", width=250, height=35, 
                                         border_width=1, border_color="#ddd", fg_color="#f9f9f9")
        
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", self.enter_pressed)

        # tabel
        self.render_table(self.patients_data)

    # error
    def render_table(self, data):
        for widget in self.left_action.winfo_children():
                if widget != self.left_action:
                    widget.destroy()


        header_row = ctk.CTkFrame(self.left_action, fg_color="#ffffff", height=40)
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
            label.pack(side="left", padx=15, pady=5)

        for row_data in data:
            row_frame = ctk.CTkFrame(self.left_action,fg_color="#ffffff", height=45)
            row_frame.pack(fill="x")

            ctk.CTkLabel(row_frame, text=row_data[0], width=col_widths[0],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=row_data[1], width=col_widths[1],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=row_data[2], width=col_widths[2],
                         anchor="w", font=("Arial", 13)).pack(side="left", padx=10)

            badge_color = self.badge_colour(row_data[3])
            ctk.CTkLabel(row_frame, text=row_data[3], width=col_widths[3], 
                         fg_color=badge_color, corner_radius=6,
                         font=("Arial Bold", 13), text_color="black",
                        ).pack(side="left", padx=10)
            
            def detail_handler(row_data):
                def handler():
                    self.view_detail(row_data)
                return handler

            ctk.CTkButton(row_frame, text="👁",
                          text_color="#01030E",
                          width=40, height=40,
                          fg_color="#ffffff",
                          hover_color="white",
                          command=detail_handler(row_data)
                          ).pack(side="left", padx=45)
            
    def enter_pressed(self, event):
        keyword=self.search_entry.get()
        self.search_patient(keyword)

    def search_patient(self, keyword):
        keyword=keyword.strip()

        if keyword == "":
            self.render_table(self.patients_data)
            return
        
        if keyword == "":
            self.render_table(self.patients_data)
            return

        result = []
        for p in self.patients_data:
            nama = p[0]
            if keyword in nama:
                result.append(p)

        if not result:
            messagebox.showinfo("Hasil", "Pasien tidak ditemukan")
        
        self.render_table(result)

    # badge warna per kategori
    def badge_colour(self, kategori):
        if kategori == "Memadai": return "#79dd88"
        if kategori == "Rendah": return "#ffe08a"
        if kategori == "Berisiko": return "#f3a6a6"
        return "#d1d1d1"
    
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


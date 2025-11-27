import customtkinter as ctk


class ActionBar:
    def __init__(self, parent, on_search, on_add):
        # 1. Frame utama (Wadah Bar)
        self.frame = ctk.CTkFrame(
            parent, fg_color="#f8f8f8", height=60, corner_radius=10
        )
        # Mengisi lebar penuh dengan padding di samping
        self.frame.pack(fill="x", padx=30, pady=15) 

        # Catatan: Frame 'left' tidak dibuat karena sudah tidak dibutuhkan.
        
        # 2. Bagian Kanan (Wadah Tombol)
        right = ctk.CTkFrame(self.frame, fg_color="transparent")
        # side="right" memastikan tombol menempel di ujung kanan self.frame
        right.pack(side="right", padx=15, pady=0) 

        # 3. Tombol Tambah
        self.add_button = ctk.CTkButton(
            right,
            text="+ TAMBAH BARU", # Mengubah teks agar lebih informatif
            width=140,
            height=35,
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="white",
            font=("Arial Bold", 13),
            corner_radius=8,
            command=on_add,
        )
        self.add_button.pack(side="left", padx=0) # Pack di dalam frame 'right'

    def update_add_button(self, text, command):
        """Method untuk mengubah teks dan fungsi tombol Tambah saat dibutuhkan."""
        self.add_button.configure(text=text, command=command)
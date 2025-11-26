import customtkinter as ctk
from tkinter import messagebox

# pastikan ini sesuai dengan paket yang sudah kamu buat tadi
from loginmobile import MobileLoginAppFlexible
from logindesktop import DesktopLoginApp


class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # root window utama
        self.window = ctk.CTk()
        self.window.title("Mental Health Monitoring System")

        # ukuran awal, tapi bisa di-resize
        self.window.geometry("900x600")
        self.window.minsize(700, 480)
        self.window.configure(fg_color="white")

        # ----- CANVAS BACKGROUND (RESPONSIVE) -----
        self.canvas = ctk.CTkCanvas(
            self.window,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # redraw background saat window di-resize
        self.window.bind("<Configure>", self.on_resize)

        # ----- CONTENT FRAME DI ATAS CANVAS -----
        self.content_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.build_content()

    # =====================================================================
    #  UI CONTENT (judul + 2 button)
    # =====================================================================
    def build_content(self):
        # frame dalam biar tampak seperti card
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=16)
        card.pack(padx=20, pady=20)

        title_label = ctk.CTkLabel(
            card,
            text="Mental Health\nMonitoring System",
            font=("Arial Bold", 28),
            text_color="#000000",
            justify="center",
        )
        title_label.pack(padx=30, pady=(24, 6))

        subtitle_label = ctk.CTkLabel(
            card,
            text="WHO-5 Well-Being Index\nDaily Check-In",
            font=("Arial", 14),
            text_color="#666666",
            justify="center",
        )
        subtitle_label.pack(padx=30, pady=(0, 18))

        ctk.CTkLabel(
            card,
            text="Pilih jenis login:",
            font=("Arial", 13),
            text_color="#333333",
        ).pack(pady=(4, 12))

        # dua tombol, ditaruh dalam frame horizontal
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(0, 20))

        pasien_btn = ctk.CTkButton(
            btn_frame,
            text="Login Pasien (Mobile)",
            width=200,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.open_pasien_login,
        )
        pasien_btn.pack(side="left", padx=8, pady=6)

        dokter_btn = ctk.CTkButton(
            btn_frame,
            text="Login Dokter / Admin",
            width=200,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.open_dokter_login,
        )
        dokter_btn.pack(side="left", padx=8, pady=6)

        hint_label = ctk.CTkLabel(
            card,
            text="Mode pasien menggunakan tampilan mobile\n"
            "(393x852) seperti yang sudah kamu buat.",
            font=("Arial", 10),
            text_color="#999999",
            justify="center",
        )
        hint_label.pack(padx=20, pady=(0, 16))

    # =====================================================================
    #  CANVAS RESPONSIVE BACKGROUND
    # =====================================================================
    def on_resize(self, event):
        """Redraw background shapes saat window di-resize."""
        # cegah saat belum fully init
        if event.widget is not self.window:
            return

        self.canvas.delete("all")

        w = event.width
        h = event.height

        # sedikit margin
        margin = 0

        # lingkaran biru besar di kiri bawah
        circle1_size = int(w * 0.9)
        self.canvas.create_oval(
            -int(w * 0.25),
            int(h * 0.35),
            -int(w * 0.25) + circle1_size,
            int(h * 0.35) + circle1_size,
            fill="#3b5998",
            outline="",
        )

        # lingkaran biru muda di kanan atas
        circle2_size = int(w * 0.8)
        self.canvas.create_oval(
            int(w * 0.45),
            -int(h * 0.4),
            int(w * 0.45) + circle2_size,
            -int(h * 0.4) + circle2_size,
            fill="#8b9dc3",
            outline="",
        )

        # overlay putih tipis di tengah (biar halus)
        self.canvas.create_rectangle(
            margin,
            int(h * 0.2),
            w - margin,
            h - margin,
            fill="white",
            outline="",
        )

    # =====================================================================
    #  ACTION BUTTONS
    # =====================================================================
    def open_pasien_login(self):
        """Buka login mobile untuk pasien."""
        try:
            # tutup main window, lalu buka login mobile
            self.window.destroy()
            app = MobileLoginAppFlexible()
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka login pasien.\n\n{e}")

    def open_dokter_login(self):
        """Buka login desktop untuk dokter/admin."""
        try:
            # tutup main window, lalu buka login desktop
            self.window.destroy()
            app = DesktopLoginApp()
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka login dokter/admin.\n\n{e}")

    # =====================================================================
    #  MAINLOOP
    # =====================================================================
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()

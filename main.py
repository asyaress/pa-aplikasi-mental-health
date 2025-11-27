import customtkinter as ctk
from tkinter import messagebox

from loginmobile import MobileLoginAppFlexible
from logindesktop import DesktopLoginApp


class MainApp:  # class untuk komunikasi ctk
    def __init__(self):
        ctk.set_appearance_mode("light")  # tema utama window
        ctk.set_default_color_theme("blue")  # tema aplikasi

        self.window = ctk.CTk()  # ini manggil ctk
        self.window.title("Mental Health Monitoring System")  # judul window

        self.window.geometry("900x600")  # ukuran awal window
        self.window.minsize(700, 480)  # ukuran window minimal terbesar
        self.window.configure(fg_color="white")  # warna back window

        self.canvas = ctk.CTkCanvas(  # bikin canvas
            self.window,  # panggil ctk
            bg="white",  # bikin canvas warna putih
            highlightthickness=0,  # ketebalan canvas
        )
        self.canvas.pack(
            fill="both", expand=True
        )  # pack (menaruh di dalam window utama), both nenperbolehkan canvas untuk diperbesar ke x, y
        # expand memperbesar ke segala arah

        # self.window.bind("<Configure>", self.on_resize) # bind python cek apakah ada perubahan ukuran window
        # #kalau ada semua canvas di window ter resize sesuai ukuran window sekarang

        self.content_frame = ctk.CTkFrame(
            self.window, fg_color="transparent"
        )  # bikin frame untuk menampung semua content
        self.content_frame.place(
            relx=0.5, rely=0.5, anchor="center"
        )  # agar semua content otomatis center
        # rel = relative jadi kalau window berubah posisinya menyesuaikan

        self.build_content()

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
            hover_color="#2d4373",  # diarahkan kursor mouse warnanya berubah
            corner_radius=10,
            command=self.open_pasien_login,  # saat button di klik apa yang terjadi
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

    def open_pasien_login(self):
        try:
            self.window.destroy()  # tutup window utama (sebelumny)
            app = (
                MobileLoginAppFlexible()
            )  # panggil class di folder loginmobile file nya app_login_mobile
            app.run()  # run class yang dipanggil
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka login pasien.\n\n{e}")

    def open_dokter_login(self):
        """Buka login desktop untuk dokter/admin."""
        try:
            self.window.destroy()  # tutup window utama (sebelumny)
            app = (
                DesktopLoginApp()
            )  # panggil class di folder logindesktop file nya app_login_desktop
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka login dokter/admin.\n\n{e}")

    def run(self):
        self.window.mainloop()  # run dan di hold sampai user melakukan interaksi dengan program


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
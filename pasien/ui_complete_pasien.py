import customtkinter as ctk


class CompletedStateMixin:
    def show_completed_state(self):
        # ubah judul & subjudul pas sudah 2 minggu ngisi
        self.title_label.configure(text="Program 2 minggu selesai 🎉")
        self.subtitle_label.configure(
            text="Terima kasih sudah mengisi WHO-5 selama 2 minggu.\n"
            "Berikut jadwal konsultasi kamu:"
        )

        # bersihin isi card sebelumnya
        for widget in self.card_container.winfo_children():
            widget.destroy()

        # card utama info selesai program
        card = ctk.CTkFrame(self.card_container, fg_color="white", corner_radius=15)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        info_label = ctk.CTkLabel(
            card,
            text="Kamu sudah menyelesaikan program check-in\nWHO-5 selama 14 hari.",
            font=("Arial", 14),
            text_color="#111827",
            justify="center",
        )
        info_label.pack(padx=24, pady=(28, 16))

        # teks jadwal konsultasi, beda kalau tanggal konsul sudah di-set atau belum
        if self.tanggal_konsul:
            konsul_text = f"Jadwal Konsultasi:\n{self.tanggal_konsul}"
        else:
            konsul_text = (
                "Jadwal Konsultasi belum ditentukan.\n"
                "Silakan menunggu konfirmasi dari dokter."
            )

        konsul_label = ctk.CTkLabel(
            card,
            text=konsul_text,
            font=("Arial Bold", 15),
            text_color="#111827",
            justify="center",
        )
        konsul_label.pack(padx=24, pady=(6, 24))

        self.update_week_progress_ui()

        # hapus tombol navigasi lama (kembali/lanjut)
        for w in self.nav_frame.winfo_children():
            w.destroy()

        # ganti dengan tombol satu aja: tutup
        close_btn = ctk.CTkButton(
            self.nav_frame,
            text="Tutup",
            width=160,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.window.destroy,
        )
        close_btn.pack(padx=6)

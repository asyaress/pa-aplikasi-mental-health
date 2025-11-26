import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PatientDetailMixin:
    """
    Mixin untuk window detail pasien + grafik WHO-5.
    """

    def view_detail(self, row_data):
        pasien = row_data.get("detail", {})
        id_pasien = row_data.get("id_pasien")

        all_jawaban = self.load_json("jawaban_harian.json")
        history = [j for j in all_jawaban if j.get("id_pasien") == id_pasien]
        history.sort(key=lambda x: x.get("tanggal", ""))

        win = ctk.CTkToplevel(self.window)
        win.title(f"Detail Pasien - {pasien.get('nama', '-')}")
        win.geometry("900x600")
        win.grab_set()

        container = ctk.CTkFrame(win, fg_color="#f8f9fa")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Kiri: Biodata
        left = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=10)
        left.pack(side="left", fill="y", padx=(0, 15), pady=10)

        ctk.CTkLabel(
            left,
            text="Biodata Pasien",
            font=("Arial Bold", 18),
            text_color="#111827",
        ).pack(anchor="w", padx=15, pady=(15, 10))

        def add_field(label, value):
            ctk.CTkLabel(
                left,
                text=f"{label}",
                font=("Arial", 12),
                text_color="#6b7280",
            ).pack(anchor="w", padx=15, pady=(5, 0))
            ctk.CTkLabel(
                left,
                text=f"{value}",
                font=("Arial Bold", 13),
                text_color="#111827",
            ).pack(anchor="w", padx=15)

        add_field("Nama", pasien.get("nama", "-"))
        add_field("Jenis Kelamin", pasien.get("jenis_kelamin", "-"))
        add_field("Tanggal Lahir", pasien.get("tanggal_lahir", "-"))
        add_field("Pendidikan", pasien.get("pendidikan", "-"))
        add_field("Pekerjaan", pasien.get("pekerjaan", "-"))
        add_field("Alamat", pasien.get("alamat", "-"))
        add_field("No. HP", pasien.get("no_hp", "-"))
        add_field("Diagnosa", pasien.get("diagnosa", row_data.get("diagnosa", "-")))
        add_field("Tanggal Konsultasi", pasien.get("tanggal_konsul", "-"))

        # Kanan: Grafik WHO-5
        right = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=10)
        right.pack(side="right", fill="both", expand=True, pady=10)

        ctk.CTkLabel(
            right,
            text="Riwayat Skor WHO-5",
            font=("Arial Bold", 18),
            text_color="#111827",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        if history:
            tanggal = [h.get("tanggal", "") for h in history]
            skor = [h.get("total_percentage", 0) for h in history]

            fig = Figure(figsize=(5, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(tanggal, skor, marker="o")
            ax.set_ylim(0, 100)
            ax.set_xlabel("Tanggal")
            ax.set_ylabel("Skor WHO-5 (%)")
            ax.set_title("Perubahan Skor dari Waktu ke Waktu")
            ax.grid(True, alpha=0.3)

            canvas = FigureCanvasTkAgg(fig, master=right)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        else:
            ctk.CTkLabel(
                right,
                text="Belum ada riwayat check-in untuk pasien ini.",
                font=("Arial", 13),
                text_color="#6b7280",
            ).pack(fill="both", expand=True, padx=15, pady=15)

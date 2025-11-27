import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PatientDetailMixin:
    """
    Mixin untuk window detail pasien + grafik WHO-5.
    """

    def _kategori_dari_skor(self, skor_persen: float) -> str:
        if skor_persen >= 70:
            return "Memadai"
        elif skor_persen >= 50:
            return "Rendah"
        else:
            return "Berisiko"

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

        # ==================== KIRI: BIODATA ====================
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

        # ==================== KANAN: WHO-5 + STATISTIK ====================
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

            # ---------- RATA-RATA & KATEGORI ----------
            avg_score = sum(skor) / len(skor) if skor else 0
            last_score = skor[-1] if skor else 0

            avg_kategori = self._kategori_dari_skor(avg_score)
            last_kategori = self._kategori_dari_skor(last_score)

            # Frame info statistik di atas grafik
            stats_frame = ctk.CTkFrame(right, fg_color="#f9fafb", corner_radius=8)
            stats_frame.pack(fill="x", padx=15, pady=(0, 10))

            # Rata-rata skor (angka)
            ctk.CTkLabel(
                stats_frame,
                text=f"Rata-rata Skor WHO-5: {avg_score:.1f}%",
                font=("Arial Bold", 13),
                text_color="#111827",
            ).pack(anchor="w", padx=12, pady=(8, 0))

            # Badge kategori rata-rata
            ctk.CTkLabel(
                stats_frame,
                text=f"Kategori Rata-rata: {avg_kategori}",
                font=("Arial", 12),
                text_color="#111827",
                fg_color=self.badge_colour(avg_kategori),
                corner_radius=999,
                width=10,
                height=24,
            ).pack(anchor="w", padx=12, pady=(4, 0))

            # Badge kategori skor terakhir (opsional)
            ctk.CTkLabel(
                stats_frame,
                text=f"Kategori Skor Terakhir: {last_kategori} ({last_score:.1f}%)",
                font=("Arial", 12),
                text_color="#111827",
                fg_color=self.badge_colour(last_kategori),
                corner_radius=999,
                width=10,
                height=24,
            ).pack(anchor="w", padx=12, pady=(4, 8))

            # ---------- Grafik ----------
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

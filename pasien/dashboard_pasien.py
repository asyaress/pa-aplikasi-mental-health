import customtkinter as ctk
from tkinter import messagebox

from .data_pasien import PatientDataMixin
from .ui_base_pasien import BaseLayoutMixin
from .ui_questions_pasien import QuestionFlowMixin
from .ui_complete_pasien import CompletedStateMixin
from .scoring_pasien import ScoringMixin


class PasienDashboard(
    PatientDataMixin,
    BaseLayoutMixin,
    QuestionFlowMixin,
    CompletedStateMixin,
    ScoringMixin,
):
    def __init__(self, user_data):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Daily Check-In - WHO-5")
        self.window.geometry("393x852")
        self.window.resizable(False, False)
        self.window.configure(fg_color="#f8f9fa")

        # ---- data user / pasien ----
        self.user_data = user_data
        self.id_pasien = user_data.get("id_pasien")
        self.nama_pasien = user_data.get("nama", "Pasien")
        self.nama_dokter = user_data.get("nama_dokter", "-")

        # statistik check-in & info pasien
        self.total_checkin, self.today_already_filled = self.get_checkin_stats()
        self.tanggal_konsul = self.get_tanggal_konsul()

        # kalau belum 14 tapi hari ini sudah isi -> keluar
        if self.total_checkin < 14 and self.today_already_filled:
            messagebox.showwarning(
                "Sudah Mengisi",
                "Anda sudah mengisi WHO-5 hari ini.\n"
                "Silakan kembali besok untuk check-in berikutnya.",
            )
            self.window.destroy()
            return

        # pertanyaan WHO-5
        self.questions = self.load_questions()
        self.current_question = 0
        self.answers = []
        self.selected_value = None

        # UI dasar
        self.build_base_layout()

        # kalau program selesai -> langsung tampilan selesai
        if self.total_checkin >= 14:
            self.show_completed_state()
        else:
            self.show_question_card()

        self.update_week_progress_ui()

    def run(self):
        self.window.mainloop()

import customtkinter as ctk
from tkinter import messagebox

from .data_service import DataServiceMixin
from .patient_form_mixin import PatientFormMixin
from .patient_table import PatientTableMixin
from .patient_detail import PatientDetailMixin


class dokterDashboard(
    DataServiceMixin,
    PatientFormMixin,
    PatientTableMixin,
    PatientDetailMixin,
):
    def __init__(self, user, on_logout=None):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("dashboard dokter")
        self.window.geometry("1200x700")
        self.window.configure(fg_color="#f8f9fa")

        self.user = user
        self.on_logout = on_logout
        self.data_folder = "data"

        # data pasien
        self.patients_data = self.load_patients_for_current_doctor()

        # bangun UI (sidebar + tabel)
        self.build_ui()

    def run(self):
        self.window.mainloop()

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Yakin ingin logout?")
        if not confirm:
            return

        self.window.destroy()

        if self.on_logout is not None:
            self.on_logout()


if __name__ == "__main__":
    contoh_user = {"id_role": 2, "id_dokter": 1, "nama": "Dokter Testing"}
    app = dokterDashboard(contoh_user)
    app.run()

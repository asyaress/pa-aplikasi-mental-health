import customtkinter as ctk
from .config import WINDOW_TITLE, WINDOW_SIZE, ROOT_BG, MAIN_BG
from .core import datastore
from .layout import build_sidebar, ActionBar
from .pasien import pasien_table, pasien_add_form
from .dokter import dokter_table, dokter_add_form
from .questions import question_table, question_add_form
from .roles import role_table, role_add_form


class AdminApp:
    def __init__(self, user, on_logout=None):
        """
        on_logout: callback yang dikirim dari layar login.
        Misal di login mixin:
            dashboard = AdminApp(user, on_logout=back_to_login)
        """
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.user = user
        self.on_logout = on_logout  # <- simpan callback logout dari luar

        self.window = ctk.CTk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(fg_color=ROOT_BG)
        self.window.resizable(True, True)

        self.current_menu = "Pasien"

        self.patients_data = []
        self.doctors_data = []
        self.question_sets = {}
        self.questions_data = []
        self.roles_data = []

        self.checkbox_vars = []

        self.sidebar = None
        self.main_content = None
        self.table_frame = None
        self.action_bar = None

        self.load_all_data()
        self.build_ui()

    # ---------- DATA ----------

    def load_all_data(self):
        self.patients_data = datastore.load_patients_for_table()
        self.doctors_data = datastore.load_doctors_for_table()
        self.question_sets = datastore.load_question_sets()
        self.questions_data = datastore.load_questions_for_table(self.question_sets)
        self.roles_data = datastore.load_roles_for_table()

    # ---------- UI ----------

    def build_ui(self):
        # sidebar
        self.sidebar = build_sidebar(self.window, self.menu_clicked)

        # tombol logout di bawah sidebar
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#ef4444",
            hover_color="#b91c1c",
            text_color="white",
            corner_radius=8,
            command=self.logout,  # <- fungsi logout di bawah
        )
        logout_btn.pack(side="bottom", fill="x", padx=20, pady=20)

        # main content
        self.main_content = ctk.CTkFrame(self.window, fg_color=MAIN_BG, corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.action_bar = ActionBar(
            self.main_content,
            on_search=self.handle_search,
            on_add=self.handle_add_clicked,
        )

        self.table_frame = ctk.CTkScrollableFrame(
            self.main_content, fg_color="white", corner_radius=0
        )
        self.table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        self.render_table()

    def _clear_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.checkbox_vars = []

    def render_table(self):
        self._clear_table()

        if self.current_menu == "Pasien":
            self.action_bar.update_add_button(
                "+ Pasien", lambda: pasien_add_form.open_add_patient(self)
            )
            pasien_table.render_patient_table(self)

        elif self.current_menu == "Dokter":
            self.action_bar.update_add_button(
                "+ Dokter", lambda: dokter_add_form.open_add_doctor(self)
            )
            dokter_table.render_doctor_table(self)

        elif self.current_menu == "Questions":
            self.action_bar.update_add_button(
                "+ Pertanyaan", lambda: question_add_form.open_add_question(self)
            )
            question_table.render_question_table(self)

        elif self.current_menu == "Role":
            self.action_bar.update_add_button(
                "+ Role", lambda: role_add_form.open_add_role(self)
            )
            role_table.render_role_table(self)

    def update_selection_count(self):
        count = sum(1 for v in self.checkbox_vars if v.get())
        # kalau nanti mau dipakai di ActionBar, bisa diteruskan ke sana

    # ---------- MENU & ACTION ----------

    def menu_clicked(self, menu_name: str):
        self.current_menu = menu_name

        if menu_name == "Pasien":
            self.patients_data = datastore.load_patients_for_table()
        elif menu_name == "Dokter":
            self.doctors_data = datastore.load_doctors_for_table()
        elif menu_name == "Questions":
            self.question_sets = datastore.load_question_sets()
            self.questions_data = datastore.load_questions_for_table(self.question_sets)
        elif menu_name == "Role":
            self.roles_data = datastore.load_roles_for_table()

        self.render_table()

    def handle_search(self, keyword: str):
        print(f"Searching for: {keyword}")

    def handle_add_clicked(self):
        # Akan dioverride setiap kali render_table dipanggil melalui update_add_button
        pass

    # ---------- LOGOUT ----------

    def logout(self):
        """
        Dipanggil saat tombol Logout di sidebar diklik.
        - Tutup window admin
        - Kalau ada callback on_logout (dari login screen), panggil itu.
        """
        # tutup window admin dulu
        self.window.destroy()

        # kalau login screen ngirimin callback, panggil biar bisa munculin lagi
        if self.on_logout is not None:
            self.on_logout()

    # ---------- RUN LOOP ----------

    def run(self):
        self.window.mainloop()

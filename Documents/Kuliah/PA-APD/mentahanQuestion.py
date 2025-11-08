import customtkinter as ctk
from tkinter import messagebox

class MobileQuestionPage:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
eight
        self.create_ui()

    def create_ui(self):
        main_container = ctk.CTkFrame(self.window, fg_color="white")
        main_container.pack(fill="both", expand=True)

        content = ctk.CTkFrame(main_container, fg_color="white")
        content.pack(fill="both", expand=True, padx=30, pady=10)

        profile_icon_label = ctk.CTkLabel(content, text="🙍", font=("Arial", 24))
        profile_icon_label.pack(anchor="ne",pady= (30, 0), padx=(12, 8))

        greeting_label = ctk.CTkLabel(
            content,
            text="Hai, Diftya",
            font=("Arial Bold", 20),
            text_color="#000000",
            anchor="w",
        )
        greeting_label.pack(anchor="w", pady=(0, 5))

        greeting2_label = ctk.CTkLabel(
            content,
            text="""Ayo mulai sesi kita 
hari ini""",
            font=("Arial Bold", 32),
            text_color="#000000",
            anchor="w",
            justify="left",
        )
        greeting2_label.pack(anchor="w", pady=(3, 3))


        subtitle_label = ctk.CTkLabel(
            content,
            text="""Silahkan jawab 5 pertanyaan berikut (tidak ada jawaban yang salah, 
mohon mengisi dengan jujur)""",
            font=("Arial", 10),
            text_color="#666666",
            anchor="w",
            justify="left"
        )
        subtitle_label.pack(anchor="w", pady=(25, 25))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MobileQuestionPage()
    app.run()
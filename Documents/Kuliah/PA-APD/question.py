import customtkinter as ctk
from tkinter import messagebox

class MobileQuestionPage:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Ukuran window seperti layar HP
        width, height = 393, 852
        self.window = ctk.CTk()
        self.window.title("Question Page 1")
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(True, True)
        self.window.configure(fg_color="white")

        self.width = width
        self.height = height

        self.create_ui()

    def create_ui(self):
        # Frame utama (full layar)
        main_container = ctk.CTkFrame(self.window, fg_color="white")
        main_container.pack(fill="both", expand=True)

        # Frame konten di tengah
        content = ctk.CTkFrame(main_container, fg_color="white")
        content.pack(fill="both", expand=True, padx=24, pady=24)

        # Ikon profil di kanan atas
        profile_icon_label = ctk.CTkLabel(content, text="🙍", font=("Arial", 24))
        profile_icon_label.pack(anchor="ne", pady=(10, 0))

        # Sapaan
        greeting_label = ctk.CTkLabel(
            content,
            text="Hai, Alyar",
            font=("Arial Bold", 20),
            text_color="#000000",
            anchor="w",
        )
        greeting_label.pack(anchor="w", pady=(0, 5))

        greeting2_label = ctk.CTkLabel(
            content,
            text="Ayo mulai sesi kita\nhari ini",
            font=("Arial Bold", 28),
            text_color="#000000",
            anchor="w",
            justify="left",
        )
        greeting2_label.pack(anchor="w", pady=(5, 15))

        subtitle_label = ctk.CTkLabel(
            content,
            text="""Silahkan jawab 5 pertanyaan berikut (tidak ada jawaban yang salah,
mohon mengisi dengan jujur)""",
            font=("Arial", 10),
            text_color="#666666",
            anchor="w",
            justify="left",
        )
        subtitle_label.pack(anchor="w", pady=(0, 20))

        # CARD pertanyaan
        question_card = ctk.CTkFrame(content, fg_color="#f7f7f7", corner_radius=16)
        question_card.pack(fill="x", pady=10, padx=4)

        question_label = ctk.CTkLabel(
            question_card,
            text="Dari skala 1-5, seberapa sering kamu merasa bahagia hari ini?",
            font=("Arial", 13),
            text_color="#000000",
            wraplength=330,
            justify="left"
        )
        question_label.pack(pady=(15, 10), padx=10)

        # Tombol skala (1–5) secara horizontal
        button_container = ctk.CTkFrame(question_card, fg_color="#f7f7f7")
        button_container.pack(pady=(0, 15))

        for i in range(1, 6):
            button = ctk.CTkButton(
                button_container,
                text=str(i),
                width=48,
                height=36,
                fg_color="#003399",
                hover_color="#002266",
                text_color="white",
                font=("Arial", 14, "bold"),
                corner_radius=8,
                command=lambda x=i: self.answer_selected(x),
            )
            button.pack(side="left", padx=6)

        # Progress bar
        progress = ctk.CTkProgressBar(content, width=300)
        progress.set(0.2)
        progress.pack(pady=(60, 20))

        # Tombol next
        next_button = ctk.CTkButton(
            content,
            text=">",
            width=50,
            height=40,
            fg_color="#003399",
            text_color="white",
            font=("Arial", 16, "bold"),
            corner_radius=8,
            command=self.next_question
        )
        next_button.pack(pady=(5, 10))

    def answer_selected(self, value):
        messagebox.showinfo("Jawaban", f"Kamu memilih skala: {value}")

    def next_question(self):
        messagebox.showinfo("Next", "Lanjut ke pertanyaan berikutnya!")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = MobileQuestionPage()
    app.run()

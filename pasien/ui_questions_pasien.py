import customtkinter as ctk
from tkinter import messagebox


class QuestionFlowMixin:
    """Semua yang terkait tampilan & flow pertanyaan."""

    def show_question_card(self):
        for widget in self.card_container.winfo_children():
            widget.destroy()

        if not self.questions or self.current_question >= len(self.questions):
            error_label = ctk.CTkLabel(
                self.card_container,
                text="Tidak ada pertanyaan tersedia",
                font=("Arial Bold", 16),
                text_color="red",
            )
            error_label.pack(expand=True)
            return

        current_q = self.questions[self.current_question]

        card = ctk.CTkFrame(self.card_container, fg_color="white", corner_radius=15)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        num_label = ctk.CTkLabel(
            card,
            text=f"Pertanyaan {self.current_question + 1} dari {len(self.questions)}",
            font=("Arial", 11),
            text_color="#666666",
        )
        num_label.pack(padx=22, pady=(22, 6))

        text = current_q.get("teks_pertanyaan", "Pertanyaan tidak tersedia")

        q_label = ctk.CTkLabel(
            card,
            text=text,
            font=("Arial Bold", 17),
            text_color="#000000",
            wraplength=320,
            justify="center",
        )
        q_label.pack(padx=26, pady=(8, 22))

        scale_desc = ctk.CTkLabel(
            card,
            text="0 = Tidak pernah\n5 = Sepanjang waktu",
            font=("Arial", 11),
            text_color="#999999",
            justify="center",
        )
        scale_desc.pack(pady=(0, 18))

        scale_frame = ctk.CTkFrame(card, fg_color="transparent")
        scale_frame.pack(pady=(6, 40))

        self.scale_buttons = []
        for i in range(6):
            btn = ctk.CTkButton(
                scale_frame,
                text=str(i),
                width=46,
                height=46,
                font=("Arial Bold", 18),
                fg_color="#3b5998",
                hover_color="#2d4373",
                corner_radius=10,
                command=lambda x=i: self.select_scale(x),
            )
            btn.pack(side="left", padx=4)
            self.scale_buttons.append(btn)

        if self.current_question < len(self.answers):
            self.select_scale(self.answers[self.current_question])
            if self.current_question >= len(self.questions) - 1:
                self.next_button.configure(text="Submit")
        else:
            self.selected_value = None
            self.next_button.configure(text="Lanjut")

        if self.current_question == 0:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")

    def select_scale(self, value):
        self.selected_value = value
        for i, btn in enumerate(self.scale_buttons):
            btn.configure(fg_color="#2d4373" if i == value else "#3b5998")

    def next_question(self):
        if self.selected_value is None:
            messagebox.showwarning("Peringatan", "Mohon pilih jawaban terlebih dahulu")
            return

        if self.current_question < len(self.answers):
            self.answers[self.current_question] = self.selected_value
        else:
            self.answers.append(self.selected_value)

        if self.current_question >= len(self.questions) - 1:
            self.submit_answers()
            return

        self.current_question += 1
        self.selected_value = None
        self.show_question_card()

    def previous_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.selected_value = None
            self.show_question_card()

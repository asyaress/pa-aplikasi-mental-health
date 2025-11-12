import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os

class PasienDashboard:
    def __init__(self, user_data):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Daily Check-In - WHO-5")
        self.window.geometry("393x852")
        self.window.resizable(False, False)
        self.window.configure(fg_color="#f8f9fa")

        self.user_data = user_data
        self.id_pasien = user_data.get("id_pasien")
        self.nama_pasien = user_data.get("nama", "Pasien")

        if not self.check_can_submit_today():
            messagebox.showwarning(
                "Sudah Mengisi",
                "Anda sudah mengisi WHO-5 hari ini.\nSilakan kembali besok untuk check-in berikutnya.",
            )
            self.window.destroy()
            return

        self.questions = self.load_questions()
        self.current_question = 0
        self.answers = []
        self.selected_value = None

        self.create_ui()

    def load_json(self, filename):
        try:
            filepath = os.path.join("data", filename)

            if not os.path.exists(filepath):
                return []

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data

        except json.JSONDecodeError:
            return []
        except Exception as e:
            return []

    def save_json(self, filename, data):
        try:
            filepath = os.path.join("data", filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            return False

    def check_can_submit_today(self):
        jawaban_list = self.load_json("jawaban_harian.json")

        if not jawaban_list:
            return True

        today = datetime.now().strftime("%Y-%m-%d")

        for jawaban in jawaban_list:
            if (
                jawaban.get("id_pasien") == self.id_pasien
                and jawaban.get("tanggal") == today
            ):
                return False

        return True

    def load_questions(self):
        items = self.load_json("item_pertanyaan.json")

        if not items:
            return []

        who5_items = [item for item in items if item.get("id_set_pertanyaan") == 1]
        who5_items.sort(key=lambda x: x.get("nomor_urut", 0))

        return who5_items

    def create_ui(self):
        main_container = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(
            main_container, fg_color="white", corner_radius=0, height=145
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", padx=20, pady=18)

        top_row = ctk.CTkFrame(header_content, fg_color="transparent")
        top_row.pack(fill="x")

        nama_depan = self.nama_pasien.split()[0] if self.nama_pasien else "Pasien"

        greeting_label = ctk.CTkLabel(
            top_row,
            text=f"Hai, {nama_depan}",
            font=("Arial", 17),
            text_color="#333333",
            anchor="w",
        )
        greeting_label.pack(side="left")

        profile_button = ctk.CTkButton(
            top_row,
            text="Profile",
            width=70,
            height=35,
            fg_color="transparent",
            hover_color="#e0e0e0",
            text_color="#333333",
            font=("Arial", 12),
            corner_radius=17,
        )
        profile_button.pack(side="right")

        title_label = ctk.CTkLabel(
            header_content,
            text="Ayo mulai sesi kita\nhari ini",
            font=("Arial Bold", 32),
            text_color="#000000",
            anchor="w",
            justify="left",
        )
        title_label.pack(anchor="w", pady=(10, 5))

        subtitle_label = ctk.CTkLabel(
            header_content,
            text="WHO-5 Well-Being Index\n(Dalam 2 minggu terakhir)",
            font=("Arial", 12),
            text_color="#666666",
            anchor="w",
            justify="left",
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        self.card_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.card_container.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        self.create_question_card()

        bottom_container = ctk.CTkFrame(
            main_container, fg_color="transparent", height=120
        )
        bottom_container.pack(fill="x", padx=20, pady=(0, 30))
        bottom_container.pack_propagate(False)

        self.progress_bar = ctk.CTkProgressBar(
            bottom_container,
            height=8,
            corner_radius=4,
            fg_color="#e0e0e0",
            progress_color="#3b5998",
        )
        self.progress_bar.pack(fill="x", pady=(0, 20))

        if len(self.questions) > 0:
            self.progress_bar.set(1 / len(self.questions))
        else:
            self.progress_bar.set(0)

        nav_frame = ctk.CTkFrame(bottom_container, fg_color="transparent")
        nav_frame.pack()

        self.prev_button = ctk.CTkButton(
            nav_frame,
            text="Kembali",
            width=120,
            height=50,
            font=("Arial Bold", 14),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.previous_question,
            state="disabled",
        )
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(
            nav_frame,
            text="Lanjut",
            width=120,
            height=50,
            font=("Arial Bold", 14),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.next_question,
        )
        self.next_button.pack(side="left", padx=10)

    def create_question_card(self):
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

        question_card = ctk.CTkFrame(
            self.card_container, fg_color="white", corner_radius=15
        )
        question_card.pack(fill="both", expand=True)

        question_num_label = ctk.CTkLabel(
            question_card,
            text=f"Pertanyaan {self.current_question + 1} dari {len(self.questions)}",
            font=("Arial", 12),
            text_color="#666666",
        )
        question_num_label.pack(padx=25, pady=(30, 10))

        question_text = current_q.get("teks_pertanyaan", "Pertanyaan tidak tersedia")

        question_label = ctk.CTkLabel(
            question_card,
            text=question_text,
            font=("Arial Bold", 17),
            text_color="#000000",
            wraplength=320,
            justify="center",
        )
        question_label.pack(padx=25, pady=(10, 30))

        scale_desc = ctk.CTkLabel(
            question_card,
            text="0 = Tidak pernah\n5 = Sepanjang waktu",
            font=("Arial", 11),
            text_color="#999999",
            justify="center",
        )
        scale_desc.pack(pady=(0, 20))

        scale_frame = ctk.CTkFrame(question_card, fg_color="transparent")
        scale_frame.pack(pady=(10, 50))

        self.scale_buttons = []
        for i in range(0, 6):
            btn = ctk.CTkButton(
                scale_frame,
                text=str(i),
                width=50,
                height=50,
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

    def select_scale(self, value):
        self.selected_value = value

        for i, btn in enumerate(self.scale_buttons):
            if i == value:
                btn.configure(fg_color="#2d4373")
            else:
                btn.configure(fg_color="#3b5998")

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
        self.create_question_card()

        progress = (self.current_question + 1) / len(self.questions)
        self.progress_bar.set(progress)

        self.prev_button.configure(state="normal")
        if self.current_question >= len(self.questions) - 1:
            self.next_button.configure(text="Submit")

    def previous_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.selected_value = None
            self.create_question_card()

            progress = (self.current_question + 1) / len(self.questions)
            self.progress_bar.set(progress)

            if self.current_question == 0:
                self.prev_button.configure(state="disabled")
            self.next_button.configure(text="Lanjut")

    def calculate_who5_score(self):
        total_raw = sum(self.answers)
        total_percentage = total_raw * 4

        if total_percentage <= 28:
            kategori = "merah"
        elif total_percentage <= 50:
            kategori = "orange"
        elif total_percentage <= 70:
            kategori = "kuning"
        else:
            kategori = "hijau"

        return total_raw, total_percentage, kategori

    def save_to_database(self, total_raw, total_percentage, kategori):
        try:
            jawaban_list = self.load_json("jawaban_harian.json")

            if not jawaban_list:
                jawaban_list = []

            if jawaban_list:
                new_id = max([j.get("id", 0) for j in jawaban_list]) + 1
            else:
                new_id = 1

            new_jawaban = {
                "id": new_id,
                "id_pasien": self.id_pasien,
                "tanggal": datetime.now().strftime("%Y-%m-%d"),
                "jawaban_1": self.answers[0] if len(self.answers) > 0 else 0,
                "jawaban_2": self.answers[1] if len(self.answers) > 1 else 0,
                "jawaban_3": self.answers[2] if len(self.answers) > 2 else 0,
                "jawaban_4": self.answers[3] if len(self.answers) > 3 else 0,
                "jawaban_5": self.answers[4] if len(self.answers) > 4 else 0,
                "total_raw": total_raw,
                "total_percentage": total_percentage,
                "kategori": kategori,
            }

            jawaban_list.append(new_jawaban)

            success = self.save_json("jawaban_harian.json", jawaban_list)

            if success:
                print("Data berhasil disimpan")
                print(f"ID: {new_id}, Tanggal: {new_jawaban['tanggal']}")
                return True
            else:
                return False

        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def submit_answers(self):
        total_raw, total_percentage, kategori = self.calculate_who5_score()

        print("\nWHO-5 DAILY CHECK-IN")
        print(f"Pasien: {self.nama_pasien}")
        print(f"ID Pasien: {self.id_pasien}")
        print(f"Tanggal: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Total Raw: {total_raw}/25")
        print(f"Total Percentage: {total_percentage}/100")
        print(f"Kategori: {kategori.upper()}")

        success = self.save_to_database(total_raw, total_percentage, kategori)

        if success:
            kategori_label = {
                "merah": "Merah - Perlu Perhatian",
                "orange": "Orange - Kurang Baik",
                "kuning": "Kuning - Cukup Baik",
                "hijau": "Hijau - Baik",
            }

            messagebox.showinfo(
                "Terima Kasih",
                f"Check-in harian berhasil\n\n"
                f"Kategori: {kategori_label.get(kategori, kategori.upper())}\n"
                f"Skor: {total_percentage}/100\n\n"
                f"Data telah tersimpan",
            )

            self.window.destroy()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data\nSilakan coba lagi")

    def run(self):
        self.window.mainloop()

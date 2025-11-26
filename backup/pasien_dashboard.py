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

        # ---- data user / pasien ----
        self.user_data = user_data
        self.id_pasien = user_data.get("id_pasien")
        self.nama_pasien = user_data.get("nama", "Pasien")
        self.nama_dokter = user_data.get("nama_dokter", "-")

        # statistik check-in & info pasien (tanggal_konsul)
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

        # pertanyaan WHO-5 (cuma dipakai kalau total_checkin < 14)
        self.questions = self.load_questions()
        self.current_question = 0
        self.answers = []
        self.selected_value = None

        # UI dasar (header + card_container + bottom)
        self.build_base_layout()

        # kalau program 2 minggu sudah selesai -> langsung tampilan selesai
        if self.total_checkin >= 14:
            self.show_completed_state()
        else:
            self.show_question_card()

        self.update_week_progress_ui()

    # ========== UTIL JSON ==========

    def load_json(self, filename):
        try:
            filepath = os.path.join("data", filename)
            if not os.path.exists(filepath):
                return []
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_json(self, filename, data):
        try:
            filepath = os.path.join("data", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    # ========== DATA PASIEN / CHECK-IN ==========

    def get_checkin_stats(self):
        """
        Hitung total check-in pasien ini (max 14)
        dan apakah hari ini sudah mengisi.
        """
        jawaban_list = self.load_json("jawaban_harian.json")
        today = datetime.now().strftime("%Y-%m-%d")

        total = 0
        today_filled = False

        for j in jawaban_list:
            if j.get("id_pasien") == self.id_pasien:
                total += 1
                if j.get("tanggal") == today:
                    today_filled = True

        return total, today_filled

    def get_tanggal_konsul(self):
        pasien_list = self.load_json("pasien.json")
        for p in pasien_list:
            if p.get("id") == self.id_pasien:
                return p.get("tanggal_konsul", "") or ""
        return ""

    def load_questions(self):
        items = self.load_json("item_pertanyaan.json")
        if not items:
            return []
        who5_items = [item for item in items if item.get("id_set_pertanyaan") == 1]
        who5_items.sort(key=lambda x: x.get("nomor_urut", 0))
        return who5_items

    # ========== UI DASAR (HEADER + FOOTER) ==========

    def build_base_layout(self):
        main_container = ctk.CTkFrame(self.window, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True)

        # ----- HEADER (adaptif mobile) -----
        header_frame = ctk.CTkFrame(
            main_container, fg_color="white", corner_radius=0, height=190
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", padx=18, pady=14)

        # baris atas: nama + tombol profile
        top_row = ctk.CTkFrame(header_content, fg_color="transparent")
        top_row.pack(fill="x")

        nama_depan = self.nama_pasien.split()[0] if self.nama_pasien else "Pasien"

        self.greeting_label = ctk.CTkLabel(
            top_row,
            text=f"Hai, {nama_depan}",
            font=("Arial", 16),
            text_color="#333333",
            anchor="w",
        )
        self.greeting_label.pack(side="left")

        profile_button = ctk.CTkButton(
            top_row,
            text="Profile",
            width=70,
            height=28,
            fg_color="transparent",
            hover_color="#e0e0e0",
            text_color="#333333",
            font=("Arial", 11),
            corner_radius=14,
        )
        profile_button.pack(side="right")

        # judul & sub judul
        self.title_label = ctk.CTkLabel(
            header_content,
            text="Ayo mulai sesi\nhari ini",
            font=("Arial Bold", 22),
            text_color="#000000",
            anchor="w",
            justify="left",
        )
        self.title_label.pack(anchor="w", pady=(6, 2))

        self.subtitle_label = ctk.CTkLabel(
            header_content,
            text="WHO-5 Well-Being Index\n(2 minggu terakhir)",
            font=("Arial", 11),
            text_color="#777777",
            anchor="w",
            justify="left",
        )
        self.subtitle_label.pack(anchor="w")

        # ----- AREA TENGAH (CARD) -----
        self.card_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.card_container.pack(fill="both", expand=True, padx=16, pady=(8, 8))

        # ----- BAGIAN BAWAH (PROGRESS + NAV) -----
        bottom_container = ctk.CTkFrame(
            main_container, fg_color="transparent", height=150
        )
        bottom_container.pack(fill="x", padx=18, pady=(0, 18))
        bottom_container.pack_propagate(False)

        self.progress_label = ctk.CTkLabel(
            bottom_container,
            text="Progress 2 minggu: 0/14",
            font=("Arial", 11),
            text_color="#333333",
            anchor="w",
        )
        self.progress_label.pack(anchor="w", pady=(0, 4))

        self.week_progress_bar = ctk.CTkProgressBar(
            bottom_container,
            height=8,
            corner_radius=4,
            fg_color="#e0e0e0",
            progress_color="#3b5998",
        )
        self.week_progress_bar.pack(fill="x", pady=(0, 8))

        self.consult_label = ctk.CTkLabel(
            bottom_container,
            text="Jadwal Konsul: -",
            font=("Arial", 11),
            text_color="#555555",
            anchor="w",
        )
        self.consult_label.pack(anchor="w", pady=(2, 10))

        self.nav_frame = ctk.CTkFrame(bottom_container, fg_color="transparent")
        self.nav_frame.pack(pady=(4, 0))

        self.prev_button = ctk.CTkButton(
            self.nav_frame,
            text="Kembali",
            width=118,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.previous_question,
            state="disabled",
        )
        self.prev_button.pack(side="left", padx=6)

        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Lanjut",
            width=118,
            height=44,
            font=("Arial Bold", 13),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=10,
            command=self.next_question,
        )
        self.next_button.pack(side="left", padx=6)

    def update_week_progress_ui(self):
        selesai = min(self.total_checkin, 14)
        self.progress_label.configure(text=f"Progress 2 minggu: {selesai}/14")

        if selesai <= 0:
            self.week_progress_bar.set(0)
        else:
            self.week_progress_bar.set(selesai / 14)

        if selesai >= 14:
            if self.tanggal_konsul:
                teks = f"Jadwal Konsul: {self.tanggal_konsul}"
            else:
                teks = "Jadwal Konsul: belum ditentukan"
        else:
            teks = "Jadwal Konsul: -"
        self.consult_label.configure(text=teks)

    # ========== MODE: PERTANYAAN ==========
    def show_question_card(self):
        # bersihkan card_container
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
        question_card.pack(fill="both", expand=True, padx=4, pady=4)

        question_num_label = ctk.CTkLabel(
            question_card,
            text=f"Pertanyaan {self.current_question + 1} dari {len(self.questions)}",
            font=("Arial", 11),
            text_color="#666666",
        )
        question_num_label.pack(padx=22, pady=(22, 6))

        question_text = current_q.get("teks_pertanyaan", "Pertanyaan tidak tersedia")

        question_label = ctk.CTkLabel(
            question_card,
            text=question_text,
            font=("Arial Bold", 17),
            text_color="#000000",
            wraplength=320,
            justify="center",
        )
        question_label.pack(padx=26, pady=(8, 22))

        scale_desc = ctk.CTkLabel(
            question_card,
            text="0 = Tidak pernah\n5 = Sepanjang waktu",
            font=("Arial", 11),
            text_color="#999999",
            justify="center",
        )
        scale_desc.pack(pady=(0, 18))

        scale_frame = ctk.CTkFrame(question_card, fg_color="transparent")
        scale_frame.pack(pady=(6, 40))

        self.scale_buttons = []
        for i in range(0, 6):
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

        # kalau sebelumnya sudah pernah dijawab, auto-select
        if self.current_question < len(self.answers):
            self.select_scale(self.answers[self.current_question])
            # supaya next button text benar
            if self.current_question >= len(self.questions) - 1:
                self.next_button.configure(text="Submit")
        else:
            self.selected_value = None
            self.next_button.configure(text="Lanjut")

        # tombol prev diatur
        if self.current_question == 0:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")

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

        # kalau sudah pertanyaan terakhir -> submit
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

    # ========== MODE: PROGRAM SELESAI (14/14) ==========

    def show_completed_state(self):
        # ubah teks header biar terasa selesai
        self.title_label.configure(text="Program 2 minggu selesai 🎉")
        self.subtitle_label.configure(
            text="Terima kasih sudah mengisi WHO-5 selama 2 minggu.\n"
            "Berikut jadwal konsultasi kamu:"
        )

        # bersihkan area pertanyaan & ganti dengan kartu info
        for widget in self.card_container.winfo_children():
            widget.destroy()

        card = ctk.CTkFrame(self.card_container, fg_color="white", corner_radius=15)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        info_label = ctk.CTkLabel(
            card,
            text="Kamu sudah menyelesaikan program check-in\n"
                 "WHO-5 selama 14 hari.",
            font=("Arial", 14),
            text_color="#111827",
            justify="center",
        )
        info_label.pack(padx=24, pady=(28, 16))

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

        # ganti tombol navigasi jadi 1 tombol "Tutup"
        for w in self.nav_frame.winfo_children():
            w.destroy()

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

    # ========== HITUNG & SIMPAN HASIL ==========

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
            jawaban_list = self.load_json("jawaban_harian.json") or []

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
            return self.save_json("jawaban_harian.json", jawaban_list)
        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def submit_answers(self):
        total_raw, total_percentage, kategori = self.calculate_who5_score()

        success = self.save_to_database(total_raw, total_percentage, kategori)

        if success:
            messagebox.showinfo(
                "Terima Kasih",
                "Check-in harian berhasil.\n\nData telah tersimpan.",
            )
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data\nSilakan coba lagi")

    # ========== MAINLOOP ==========

    def run(self):
        self.window.mainloop()
from datetime import datetime
from tkinter import messagebox


class ScoringMixin:

    def calculate_who5_score(self):
        # hitung skor mentah dan konversi ke persen (0–100)
        total_raw = sum(self.answers)
        total_percentage = total_raw * 4

        # mapping skor ke kategori warna, biar gampang dibaca di UI
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
            # load semua jawaban harian dulu
            jawaban_list = self.load_json("jawaban_harian.json") or []

            # auto-generate id baru, ambil dari id terbesar sebelumnya
            if jawaban_list:
                new_id = max([j.get("id", 0) for j in jawaban_list]) + 1
            else:
                new_id = 1

            # bentuk satu record jawaban lengkap
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
        # hitung skor lalu coba simpan ke “database” (file JSON)
        total_raw, total_percentage, kategori = self.calculate_who5_score()
        success = self.save_to_database(total_raw, total_percentage, kategori)

        if success:
            messagebox.showinfo(
                "Terima Kasih",
                "Check-in harian berhasil.\n\nData telah tersimpan.",
            )
            self.window.destroy()  # tutup window setelah submit
        else:
            messagebox.showerror("Error", "Gagal menyimpan data\nSilakan coba lagi")

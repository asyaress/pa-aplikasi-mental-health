import json
import os
from datetime import datetime


class PatientDataMixin:
    """Helper baca / tulis JSON dan data pasien."""

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
        who5_items = [i for i in items if i.get("id_set_pertanyaan") == 1]
        who5_items.sort(key=lambda x: x.get("nomor_urut", 0))
        return who5_items

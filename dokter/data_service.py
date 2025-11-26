import json
import os


class DataServiceMixin:
    """
    Mixin untuk urusan data (JSON) dan load pasien sesuai dokter.
    """

    data_folder: str
    user: dict

    def load_json(self, filename):
        filepath = os.path.join(self.data_folder, filename)

        try:
            if not os.path.exists(filepath):
                print(f"File {filepath} tidak ditemukan")
                return []

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data

        except json.JSONDecodeError:
            print(f"Format JSON {filepath} tidak valid")
            return []
        except Exception as e:
            print(f"Error baca file {filepath}: {e}")
            return []

    def save_json(self, filename, data):
        filepath = os.path.join(self.data_folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error nulis file {filepath}: {e}")

    def load_patients_for_current_doctor(self):
        """
        Ambil list pasien berdasarkan id_dokter yang sedang login.
        Sekaligus hitung progress 2 minggu dan ambil tanggal_konsul.
        """
        id_dokter = self.user.get("id_dokter")
        print("ID dokter saat ini:", id_dokter)

        all_pasien = self.load_json("pasien.json")
        all_jawaban = self.load_json("jawaban_harian.json")

        patients_rows = []

        for p in all_pasien:
            if p.get("id_dokter") != id_dokter:
                continue

            nama = p.get("nama", "-")
            diagnosa = p.get("diagnosa", "-")
            jenis = p.get("pekerjaan", p.get("pendidikan", "-"))

            # ambil semua jawaban harian pasien ini
            related = [j for j in all_jawaban if j.get("id_pasien") == p.get("id")]

            # kategori WHO-5 terakhir (kalau ada)
            kategori = "-"
            if related:
                related.sort(key=lambda x: x.get("tanggal", ""))
                last = related[-1]
                kategori = last.get("kategori", "-")

            # hitung progress 2 minggu: berapa kali check-in (max 14)
            total_checkin = len(related)
            progress_label = f"{total_checkin}/14"
            selesai_2minggu = total_checkin >= 14

            tanggal_konsul = p.get("tanggal_konsul", "")

            patients_rows.append(
                {
                    "id_pasien": p.get("id"),
                    "nama": nama,
                    "diagnosa": diagnosa,
                    "jenis": jenis,
                    "kategori": kategori,
                    "detail": p,  # objek pasien lengkap dari JSON
                    "total_checkin": total_checkin,
                    "progress_label": progress_label,
                    "selesai_2minggu": selesai_2minggu,
                    "tanggal_konsul": tanggal_konsul,
                }
            )

        return patients_rows

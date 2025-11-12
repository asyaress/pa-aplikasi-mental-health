import json
import os

class AuthBackend:
    def __init__(self):
        self.data_folder = "data"
        self.current_user = None

    def load_json(self, filename):
        filepath = os.path.join(self.data_folder, filename)

        try:
            if not os.path.exists(filepath):
                print(f"Error: File {filepath} tidak ditemukan!")
                return []

            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data

        except json.JSONDecodeError:
            print(f"Error: File {filepath} format JSON tidak valid!")
            return []
        except Exception as e:
            print(f"Error membaca file {filename}: {e}")
            return []

    def save_json(self, filename, data):
        filepath = os.path.join(self.data_folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error menyimpan file {filename}: {e}")
            return False

    def get_all_users(self):
        return self.load_json("users.json")

    def get_all_roles(self):
        return self.load_json("roles.json")

    def get_all_dokter(self):
        return self.load_json("dokter.json")

    def get_all_pasien(self):
        return self.load_json("pasien.json")

    def get_role_name(self, id_role):
        roles = self.get_all_roles()

        for role in roles:
            if role["id"] == id_role:
                return role["nama_role"]

        return "Unknown"

    def get_dokter_by_user_id(self, id_user):
        dokter_list = self.get_all_dokter()

        for dokter in dokter_list:
            if dokter["id_user"] == id_user:
                return dokter

        return None

    def get_pasien_by_user_id(self, id_user):
        pasien_list = self.get_all_pasien()

        for pasien in pasien_list:
            if pasien["id_user"] == id_user:
                return pasien

        return None

    def login(self, username, password):
        users = self.get_all_users()

        if not users:
            print("Error: Tidak ada data user!")
            return None

        for user in users:
            if user["username"] == username and user["password"] == password:
                user["role_name"] = self.get_role_name(user["id_role"])

                if user["id_role"] == 2:  # Dokter
                    dokter_data = self.get_dokter_by_user_id(user["id"])
                    if dokter_data:
                        user["nama"] = dokter_data["nama"]
                        user["spesialis"] = dokter_data["spesialis"]
                        user["id_dokter"] = dokter_data["id"]

                elif user["id_role"] == 3:  # Pasien
                    pasien_data = self.get_pasien_by_user_id(user["id"])
                    if pasien_data:
                        user["nama"] = pasien_data["nama"]
                        user["id_pasien"] = pasien_data["id"]
                        user["id_dokter"] = pasien_data["id_dokter"]
                        user["jenis_kelamin"] = pasien_data["jenis_kelamin"]
                        user["pendidikan"] = pasien_data["pendidikan"]
                        user["pekerjaan"] = pasien_data["pekerjaan"]
                        user["diagnosa"] = pasien_data["diagnosa"]

                elif user["id_role"] == 1:  # Admin
                    user["nama"] = "Administrator"

                self.current_user = user
                return user

        return None

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def is_logged_in(self):
        return self.current_user is not None
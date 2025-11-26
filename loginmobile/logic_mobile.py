from tkinter import messagebox


class LoginLogicMixin:
    """
    Mixin: logika login & redirect ke dashboard sesuai role.
    Butuh:
      - self.auth  (AuthBackend)
      - self.window (CTk root)
      - self.email_entry, self.password_entry (dari UI mixin)
    """

    def login(self):
        username = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Mohon isi username dan password!")
            return

        print("=" * 50)
        print("Mencoba login...")
        print(f"Username: {username}")
        print(f"Password: {'*' * len(password)}")

        user = self.auth.login(username, password)

        if user:
            print("\nLOGIN BERHASIL!")
            print(f"ID User: {user['id']}")
            print(f"Nama: {user.get('nama', 'N/A')}")
            print(f"Username: {user['username']}")
            print(f"Role: {user['role_name']} (ID: {user['id_role']})")

            if user["id_role"] == 2:
                print(f"Spesialis: {user.get('spesialis', 'N/A')}")
            elif user["id_role"] == 3:
                print(f"ID Pasien: {user.get('id_pasien', 'N/A')}")
                print(f"Diagnosa: {user.get('diagnosa', 'N/A')}")

            print("=" * 50)

            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {user.get('nama', user['username'])}!\n\n"
                f"Role: {user['role_name']}",
            )

            self.redirect_dashboard(user)
        else:
            print("\nLOGIN GAGAL!")
            print("Username atau Password salah!")
            print("=" * 50)

            messagebox.showerror(
                "Login Gagal",
                "Username atau Password salah!\n\n"
                "Silakan coba lagi atau hubungi admin.",
            )

    # --------- Redirect sesuai role ---------

    def redirect_dashboard(self, user):
        role_id = user["id_role"]
        role_name = user["role_name"]

        print(f"\n→ Redirect ke Dashboard {role_name}...")

        if role_id == 1:
            print("  (TODO) Membuka Dashboard Admin...")

        elif role_id == 2:
            print("  Membuka Dashboard Dokter...")
            self.open_dokter_dashboard(user)

        elif role_id == 3:
            print("  Membuka Dashboard Pasien...")
            self.open_pasien_dashboard(user)

        else:
            print("  Role tidak dikenali!")
            messagebox.showerror("Error", "Role user tidak valid!")

    # --------- DASHBOARD PASIEN ---------

    def open_pasien_dashboard(self, user):
        try:
            from pasien import PasienDashboard  # paket pasien yang sudah kamu buat

            print("\nMembuka Pasien Dashboard...")
            print(f"   User: {user.get('nama')}")
            print(f"   ID Pasien: {user.get('id_pasien')}")

            self.window.withdraw()

            dashboard = PasienDashboard(user)
            dashboard.run()

            print("\n👋 Dashboard pasien ditutup. Menutup aplikasi...")
            self.window.destroy()

        except ImportError as e:
            print("\nError: Paket 'pasien' tidak ditemukan!")
            print(f"   Detail: {e}")
            messagebox.showerror(
                "Error",
                "Dashboard pasien tidak ditemukan!\n\n"
                "Pastikan folder 'pasien' dan file di dalamnya sudah benar.",
            )
            self.window.deiconify()
        except Exception as e:
            print(f"\nError saat membuka dashboard pasien: {e}")
            self.window.deiconify()

    # --------- DASHBOARD DOKTER ---------

    def open_dokter_dashboard(self, user):
        try:
            # asumsi paket dokter sudah modular: from dokter import dokterDashboard
            from dokter import dokterDashboard

            print("\nMembuka Dokter Dashboard...")
            print(f"   Dokter: {user.get('nama')}")
            print(f"   ID Dokter: {user.get('id_dokter')}")

            self.window.withdraw()

            dashboard = dokterDashboard(user)
            dashboard.run()

            print("\n👋 Dashboard dokter ditutup. Menutup aplikasi...")
            self.window.destroy()

        except ImportError as e:
            print("\nError: Paket 'dokter' tidak ditemukan!")
            print(f"   Detail: {e}")
            messagebox.showerror(
                "Error",
                "Dashboard dokter tidak ditemukan!\n\n"
                "Pastikan folder 'dokter' dan file di dalamnya sudah benar.",
            )
            self.window.deiconify()
        except Exception as e:
            print(f"\nError saat membuka dashboard dokter: {e}")
            self.window.deiconify()

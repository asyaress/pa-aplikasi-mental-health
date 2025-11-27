from tkinter import messagebox


class DesktopLoginLogicMixin:
    """
    Mixin untuk logika login desktop.
    Butuh:
      - self.auth  (AuthBackend)
      - self.window (CTk)
      - self.username_entry, self.password_entry (dibuat di UI mixin)
    """

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in username and password")
            return

        user = self.auth.login(username, password)

        if user:
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {user.get('nama', user['username'])}\n\n"
                f"Role: {user['role_name']}",
            )
            self.redirect_dashboard(
                user
            )  # arahkan otomatis  ke page dashboard pertanyaan
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password\n\nPlease try again",
            )

    # ---------- Redirect ke dashboard sesuai role ----------

    def redirect_dashboard(self, user):  # otomatis ngarahin ke page dashboard lain
        role_id = user["id_role"]

        if role_id == 1:
            # ADMIN
            self.open_admin_dashboard(user)
        elif role_id == 2:
            # DOKTER
            self.open_dokter_dashboard(user)
        elif role_id == 3:
            # PASIEN
            self.open_pasien_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid user role")

    #  Dashboard Admin di sini

    def open_admin_dashboard(self, user):
        try:
            from admin.app import AdminApp

            print("\nMembuka Admin Dashboard...")
            print(f"   Admin: {user.get('nama', user.get('username'))}")

            # sembunyikan window login
            self.window.withdraw()

            def back_to_login():
                # callback ini dikirim ke AdminApp
                print("\nKembali ke halaman login dari dashboard admin...")
                self.window.deiconify()

            # kirim callback ke AdminApp
            app = AdminApp(user, on_logout=back_to_login)
            app.run()  # block sampai window admin selesai (destroy)

            print("\n Dashboard admin ditutup.")

        except ImportError as e:
            ...
            self.window.deiconify()
        except Exception as e:
            ...
            self.window.deiconify()

    # ---------- Dashboard Pasien ----------

    def open_pasien_dashboard(self, user):
        try:
            from pasien import PasienDashboard

            self.window.withdraw()
            dashboard = PasienDashboard(user)
            dashboard.run()
            self.window.destroy()

        except ImportError:
            messagebox.showerror(
                "Error",
                "Dashboard file not found\n\n"
                "Please check folder 'pasien' dan class PasienDashboard",
            )
            self.window.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard\n\n{str(e)}")
            self.window.deiconify()

    # ---------- Dashboard Dokter ----------

    def open_dokter_dashboard(self, user):
        try:
            from dokter.dashboard import dokterDashboard

            print("\nMembuka Dokter Dashboard...")
            print(f"   Dokter: {user.get('nama')}")
            print(f"   ID Dokter: {user.get('id_dokter')}")

            self.window.withdraw()

            def back_to_login():
                print("\nKembali ke halaman login dari dashboard dokter...")
                self.window.deiconify()

            dashboard = dokterDashboard(user, on_logout=back_to_login)
            dashboard.run()

            print("\n👋 Dashboard dokter ditutup.")

        except ImportError as e:
            print("\nError saat import dashboard dokter:")
            print(f"   Detail: {e}")
            messagebox.showerror(
                "Error",
                "File / modul dashboard_dokter tidak ditemukan!\n\n"
                "Pastikan folder 'dokter' dan file 'dashboard_dokter.py' sudah benar.",
            )
            self.window.deiconify()
        except Exception as e:
            print(f"\nError saat membuka dashboard dokter: {e}")
            self.window.deiconify()

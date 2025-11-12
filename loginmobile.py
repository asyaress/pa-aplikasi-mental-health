import customtkinter as ctk
from tkinter import messagebox
from auth import AuthBackend


class MobileLoginAppFlexible:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        width, height = 393, 852

        self.window = ctk.CTk()
        self.window.title("Login - Mental Health App")
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(False, False)
        self.window.configure(fg_color="white")

        self.width = width
        self.height = height

        self.auth = AuthBackend()
        self.create_ui()

    def create_ui(self):
        main_container = ctk.CTkFrame(self.window, fg_color="white")
        main_container.pack(fill="both", expand=True)

        canvas_height = int(self.height * 0.35)
        canvas = ctk.CTkCanvas(
            main_container,
            width=self.width,
            height=canvas_height,
            bg="white",
            highlightthickness=0,
        )
        canvas.pack(side="top", fill="x")

        circle1_size = int(self.width * 0.95)
        canvas.create_oval(
            -int(self.width * 0.2),
            int(canvas_height * 0.15),
            circle1_size - int(self.width * 0.2),
            canvas_height + int(canvas_height * 0.35),
            fill="#3b5998",
            outline="",
        )

        circle2_size = int(self.width * 0.9)
        canvas.create_oval(
            int(self.width * 0.48),
            -int(canvas_height * 0.4),
            int(self.width * 0.48) + circle2_size,
            int(canvas_height * 0.73),
            fill="#8b9dc3",
            outline="",
        )

        content = ctk.CTkFrame(main_container, fg_color="white")
        content.pack(fill="both", expand=True, padx=30, pady=10)

        welcome_label = ctk.CTkLabel(
            content,
            text="Welcome Back,",
            font=("Arial Bold", 26),
            text_color="#000000",
            anchor="w",
        )
        welcome_label.pack(anchor="w", pady=(10, 3))

        subtitle_label = ctk.CTkLabel(
            content,
            text="Log in now to continue",
            font=("Arial", 13),
            text_color="#666666",
            anchor="w",
        )
        subtitle_label.pack(anchor="w", pady=(0, 25))

        email_label = ctk.CTkLabel(
            content,
            text="Username",
            font=("Arial Medium", 12),
            text_color="#333333",
            anchor="w",
        )
        email_label.pack(anchor="w", pady=(0, 6))

        email_frame = ctk.CTkFrame(
            content, fg_color="#f5f5f5", corner_radius=8, height=48
        )
        email_frame.pack(fill="x", pady=(0, 18))
        email_frame.pack_propagate(False)

        email_icon_label = ctk.CTkLabel(email_frame, text="👤", font=("Arial", 14))
        email_icon_label.pack(side="left", padx=(12, 8))

        self.email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="Masukkan username",
            font=("Arial", 12),
            fg_color="transparent",
            border_width=0,
            text_color="#333333",
            placeholder_text_color="#999999",
        )
        self.email_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))

        password_label = ctk.CTkLabel(
            content,
            text="Password",
            font=("Arial Medium", 12),
            text_color="#333333",
            anchor="w",
        )
        password_label.pack(anchor="w", pady=(0, 6))

        password_frame = ctk.CTkFrame(
            content, fg_color="#f5f5f5", corner_radius=8, height=48
        )
        password_frame.pack(fill="x", pady=(0, 25))
        password_frame.pack_propagate(False)

        lock_icon_label = ctk.CTkLabel(password_frame, text="🔒", font=("Arial", 14))
        lock_icon_label.pack(side="left", padx=(12, 8))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Masukkan password",
            font=("Arial", 12),
            show="●",
            fg_color="transparent",
            border_width=0,
            text_color="#333333",
            placeholder_text_color="#999999",
        )
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))

        login_button = ctk.CTkButton(
            content,
            text="Log in",
            font=("Arial Bold", 14),
            height=48,
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=8,
            command=self.login,
        )
        login_button.pack(fill="x", pady=(0, 15))

        info_label = ctk.CTkLabel(
            content,
            text="Demo: pasien1 / pasien123",
            font=("Arial", 10),
            text_color="#999999",
        )
        info_label.pack(pady=(10, 0))

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

            # Tampilkan data tambahan sesuai role
            if user["id_role"] == 2:  # Dokter
                print(f"Spesialis: {user.get('spesialis', 'N/A')}")
            elif user["id_role"] == 3:  # Pasien
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

    def redirect_dashboard(self, user):
        role_id = user["id_role"]
        role_name = user["role_name"]

        print(f"\n→ Redirect ke Dashboard {role_name}...")

        if role_id == 1:
            print("  Membuka Dashboard Admin...")
            # TODO: self.open_admin_dashboard(user)

        elif role_id == 2:
            print("  Membuka Dashboard Dokter...")
            # TODO: self.open_dokter_dashboard(user)

        elif role_id == 3:
            print("  Membuka Dashboard Pasien...")
            self.open_pasien_dashboard(user)

        else:
            print("  Role tidak dikenali!")
            messagebox.showerror("Error", "Role user tidak valid!")

    def open_pasien_dashboard(self, user):
        try:
            from pasien_dashboard import PasienDashboard

            print("\nMembuka Pasien Dashboard...")
            print(f"   User: {user.get('nama')}")
            print(f"   ID Pasien: {user.get('id_pasien')}")

            self.window.withdraw()

            dashboard = PasienDashboard(user)
            dashboard.run()

            print("\n👋 Dashboard ditutup. Menutup aplikasi...")
            self.window.destroy()

        except ImportError as e:
            print(f"\nError: File pasien_dashboard.py tidak ditemukan!")
            print(f"   Detail: {e}")
            messagebox.showerror(
                "Error",
                "File dashboard pasien tidak ditemukan!\n\n"
                "Pastikan file pasien_dashboard.py ada di folder yang sama.",
            )
            self.window.deiconify()
        except Exception as e:
            self.window.deiconify()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = MobileLoginAppFlexible()
    app.run()

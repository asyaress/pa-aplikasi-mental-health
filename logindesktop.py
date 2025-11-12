import customtkinter as ctk
from tkinter import messagebox
from auth import AuthBackend


class DesktopLoginApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Mental Health Monitoring System - Login")
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        window_width = 1200
        window_height = 700
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.resizable(False, False)
        self.window.configure(fg_color="white")

        self.auth = AuthBackend()
        self.create_ui()

    def create_ui(self):
        left_frame = ctk.CTkFrame(self.window, fg_color="#3b5998", corner_radius=0)
        left_frame.place(x=0, y=0, relwidth=0.5, relheight=1)

        title_label = ctk.CTkLabel(
            left_frame,
            text="Mental Health\nMonitoring System",
            font=("Arial Bold", 48),
            text_color="white",
            justify="center"
        )
        title_label.place(relx=0.5, rely=0.4, anchor="center")

        subtitle_label = ctk.CTkLabel(
            left_frame,
            text="WHO-5 Well-Being Index\nDaily Check-In System",
            font=("Arial", 18),
            text_color="#e0e0e0",
            justify="center"
        )
        subtitle_label.place(relx=0.5, rely=0.55, anchor="center")

        right_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=0)
        right_frame.place(relx=0.5, y=0, relwidth=0.5, relheight=1)

        login_container = ctk.CTkFrame(right_frame, fg_color="white")
        login_container.place(relx=0.5, rely=0.5, anchor="center")

        welcome_label = ctk.CTkLabel(
            login_container,
            text="Welcome Back",
            font=("Arial Bold", 36),
            text_color="#000000"
        )
        welcome_label.pack(pady=(0, 10))

        subtitle_login = ctk.CTkLabel(
            login_container,
            text="Please login to continue",
            font=("Arial", 16),
            text_color="#666666"
        )
        subtitle_login.pack(pady=(0, 40))

        username_label = ctk.CTkLabel(
            login_container,
            text="Username",
            font=("Arial Medium", 14),
            text_color="#333333",
            anchor="w"
        )
        username_label.pack(anchor="w", pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            login_container,
            width=400,
            height=50,
            placeholder_text="Enter your username",
            font=("Arial", 14),
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=8
        )
        self.username_entry.pack(pady=(0, 20))

        password_label = ctk.CTkLabel(
            login_container,
            text="Password",
            font=("Arial Medium", 14),
            text_color="#333333",
            anchor="w"
        )
        password_label.pack(anchor="w", pady=(0, 8))

        self.password_entry = ctk.CTkEntry(
            login_container,
            width=400,
            height=50,
            placeholder_text="Enter your password",
            font=("Arial", 14),
            show="*",
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=8
        )
        self.password_entry.pack(pady=(0, 30))

        login_button = ctk.CTkButton(
            login_container,
            text="Login",
            width=400,
            height=50,
            font=("Arial Bold", 16),
            fg_color="#3b5998",
            hover_color="#2d4373",
            corner_radius=8,
            command=self.login
        )
        login_button.pack(pady=(0, 20))

        info_label = ctk.CTkLabel(
            login_container,
            text="Demo: pasien1 / pasien123",
            font=("Arial", 12),
            text_color="#999999"
        )
        info_label.pack(pady=(10, 0))

        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())

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
                f"Welcome, {user.get('nama', user['username'])}\n\nRole: {user['role_name']}"
            )
            self.redirect_dashboard(user)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password\n\nPlease try again"
            )

    def redirect_dashboard(self, user):
        role_id = user["id_role"]

        if role_id == 1:
            pass
        elif role_id == 2:
            pass
        elif role_id == 3:
            self.open_pasien_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid user role")

    def open_pasien_dashboard(self, user):
        try:
            from pasien_dashboard import PasienDashboard

            self.window.withdraw()
            dashboard = PasienDashboard(user)
            dashboard.run()
            self.window.destroy()

        except ImportError as e:
            messagebox.showerror(
                "Error",
                "Dashboard file not found\n\nPlease check pasien_dashboard.py"
            )
            self.window.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard\n\n{str(e)}")
            self.window.deiconify()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = DesktopLoginApp()
    app.run()
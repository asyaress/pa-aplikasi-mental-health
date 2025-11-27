import customtkinter as ctk
from ..config import SIDEBAR_WIDTH, PRIMARY_COLOR


def build_sidebar(root, on_menu_click):
    sidebar = ctk.CTkFrame(
        root, fg_color=PRIMARY_COLOR, width=SIDEBAR_WIDTH, corner_radius=0
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(
        sidebar, text="Dashboard", font=("Arial Bold", 24), text_color="white"
    ).pack(pady=(30, 40), padx=20)

    search_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    search_frame.pack(fill="x", padx=20, pady=(0, 30))

    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="🔍 Search",
        height=35,
        fg_color="#8cb4d9",
        border_width=2,
        border_color="#a8c5e0",
        text_color="#1a4d7a",
        placeholder_text_color="#4a7ba7",
        corner_radius=8,
    )
    search_entry.pack(fill="x")

    menu_items = [
        ("Pasien", "👥"),
        ("Dokter", "👨‍⚕️"),
        ("Questions", "❓"),
        ("Role", "🔐"),
    ]

    for name, icon in menu_items:
        btn = ctk.CTkButton(
            sidebar,
            text=f"  {name}",
            font=("Arial", 14),
            fg_color="transparent",
            hover_color="#1d4ed8",
            anchor="w",
            height=45,
            command=lambda n=name: on_menu_click(n),
        )
        btn.pack(fill="x", padx=20, pady=2)

        arrow_label = ctk.CTkLabel(
            btn, text="›", font=("Arial", 20), text_color="white"
        )
        arrow_label.place(relx=0.95, rely=0.5, anchor="e")

    return sidebar

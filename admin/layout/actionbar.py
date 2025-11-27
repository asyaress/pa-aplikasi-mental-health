import customtkinter as ctk


class ActionBar:
    def __init__(self, parent, on_search, on_add):
        self.frame = ctk.CTkFrame(
            parent, fg_color="white", height=60, corner_radius=0
        )
        self.frame.pack(fill="x", padx=30, pady=20)

        left = ctk.CTkFrame(self.frame, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)

        ctk.CTkButton(
            left,
            text="⚙",
            width=35,
            height=35,
            fg_color="transparent",
            text_color="#666",
            hover_color="#f0f0f0",
            font=("Arial", 18),
        ).pack(side="left", padx=(0, 10))

        self.search_entry = ctk.CTkEntry(
            left,
            placeholder_text="🔍 Search",
            width=250,
            height=35,
            border_width=1,
            border_color="#ddd",
            fg_color="white",
        )
        self.search_entry.pack(side="left", padx=(0, 15))
        self.search_entry.bind(
            "<Return>", lambda event: on_search(self.search_entry.get())
        )

        self.selected_label = ctk.CTkLabel(
            left,
            text="0 Selected",
            text_color="#2563eb",
            font=("Arial Bold", 12),
        )
        self.selected_label.pack(side="left")

        right = ctk.CTkFrame(self.frame, fg_color="transparent")
        right.pack(side="right", padx=15)

        self.pagination_label = ctk.CTkLabel(
            right,
            text="1 - 0 of 0",
            text_color="#666",
            font=("Arial", 12),
        )
        self.pagination_label.pack(side="left", padx=10)

        self.add_button = ctk.CTkButton(
            right,
            text="+",
            width=110,
            height=35,
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="white",
            font=("Arial Bold", 13),
            corner_radius=8,
            command=on_add,
        )
        self.add_button.pack(side="left", padx=10)

    def update_add_button(self, text, command):
        self.add_button.configure(text=text, command=command)

    def update_pagination(self, total):
        self.pagination_label.configure(text=f"1 - {total} of {total}")

    def update_selected(self, count):
        self.selected_label.configure(text=f"{count} Selected")

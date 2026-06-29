from typing import Optional

import customtkinter as ctk

from app.tools.registry import TOOL_REGISTRY, ToolMeta


class AppShell(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DTDUBBING Tools")
        self.geometry("1000x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        self._content_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._content_container.grid(row=0, column=1, sticky="nsew")

        self._current_frame: Optional[ctk.CTkFrame] = None
        self._show_landing()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")

        ctk.CTkLabel(
            sidebar, text="DTDUBBING Tools", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=16, pady=(20, 12), anchor="w")

        ctk.CTkButton(
            sidebar,
            text="Trang chủ",
            anchor="w",
            fg_color="transparent",
            text_color=("black", "white"),
            command=self._show_landing,
        ).pack(padx=8, pady=4, fill="x")

        for tool in TOOL_REGISTRY:
            ctk.CTkButton(
                sidebar,
                text=tool.name,
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                command=lambda t=tool: self._show_tool(t),
            ).pack(padx=8, pady=4, fill="x")

    def _clear_content(self):
        if self._current_frame is not None:
            self._current_frame.destroy()
            self._current_frame = None

    def _show_landing(self):
        self._clear_content()
        frame = ctk.CTkFrame(self._content_container, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(frame, text="Danh sách tool", font=ctk.CTkFont(size=20, weight="bold")).pack(
            anchor="w", pady=(0, 16)
        )

        for tool in TOOL_REGISTRY:
            card = ctk.CTkButton(
                frame,
                fg_color=("gray90", "gray20"),
                hover_color=("gray80", "gray25"),
                text_color=("black", "white"),
                anchor="w",
                height=64,
                text=f"{tool.name}\n{tool.description}",
                command=lambda t=tool: self._show_tool(t),
            )
            card.pack(fill="x", pady=6)

        self._current_frame = frame

    def _show_tool(self, tool: ToolMeta):
        self._clear_content()
        frame = tool.frame_class(self._content_container)
        frame.pack(fill="both", expand=True, padx=24, pady=24)
        self._current_frame = frame

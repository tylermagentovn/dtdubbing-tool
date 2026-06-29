from dataclasses import dataclass
from typing import Type

import customtkinter as ctk

from app.tools.srt_split.gui import SrtSplitFrame


@dataclass
class ToolMeta:
    id: str
    name: str
    description: str
    frame_class: Type[ctk.CTkFrame]


TOOL_REGISTRY: list[ToolMeta] = [
    ToolMeta(
        id="srt-split",
        name="Tách SRT",
        description="Chia file SRT gốc theo thời lượng từng episode video",
        frame_class=SrtSplitFrame,
    ),
]

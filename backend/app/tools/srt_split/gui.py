import os
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk

from app.tools.srt_split.service import SrtSplitOutcome, split_srt_files


class SrtSplitFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.srt_path: Optional[str] = None
        self.video_paths: list[str] = []
        self.output_dir: Optional[str] = None

        ctk.CTkLabel(self, text="Tách SRT", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            self,
            text="Chia file SRT gốc thành các file SRT riêng cho từng tập, dựa theo thời lượng video tương ứng.",
            text_color="gray",
            wraplength=640,
            justify="left",
        ).pack(anchor="w", pady=(0, 16))

        srt_row = ctk.CTkFrame(self, fg_color="transparent")
        srt_row.pack(fill="x", pady=6)
        ctk.CTkButton(srt_row, text="Chọn file SRT gốc", command=self._pick_srt).pack(side="left")
        self.srt_label = ctk.CTkLabel(srt_row, text="Chưa chọn file", text_color="gray")
        self.srt_label.pack(side="left", padx=12)

        ctk.CTkButton(self, text="Chọn video các tập", command=self._pick_videos).pack(anchor="w", pady=(12, 6))

        self.video_list_frame = ctk.CTkScrollableFrame(self, height=180)
        self.video_list_frame.pack(fill="x", pady=(0, 12))
        self._render_video_list()

        out_row = ctk.CTkFrame(self, fg_color="transparent")
        out_row.pack(fill="x", pady=6)
        ctk.CTkButton(out_row, text="Chọn thư mục lưu kết quả (tuỳ chọn)", command=self._pick_output_dir).pack(
            side="left"
        )
        self.output_label = ctk.CTkLabel(
            out_row, text="Mặc định: lưu cùng thư mục với file SRT gốc", text_color="gray"
        )
        self.output_label.pack(side="left", padx=12)

        self.submit_btn = ctk.CTkButton(self, text="Tách SRT", command=self._submit)
        self.submit_btn.pack(anchor="w", pady=16)

        self.results_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True)

    def _pick_srt(self):
        path = filedialog.askopenfilename(
            title="Chọn file SRT gốc",
            filetypes=[("Subtitle files", "*.srt"), ("All files", "*.*")],
        )
        if path:
            self.srt_path = path
            self.srt_label.configure(text=os.path.basename(path), text_color=("black", "white"))

    def _pick_videos(self):
        paths = filedialog.askopenfilenames(
            title="Chọn video các tập",
            filetypes=[("Video files", "*.mp4 *.mkv *.mov *.avi *.webm"), ("All files", "*.*")],
        )
        if paths:
            self.video_paths = list(paths)
            self._render_video_list()

    def _pick_output_dir(self):
        path = filedialog.askdirectory(title="Chọn thư mục lưu kết quả")
        if path:
            self.output_dir = path
            self.output_label.configure(text=path, text_color=("black", "white"))

    def _render_video_list(self):
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()

        if not self.video_paths:
            ctk.CTkLabel(self.video_list_frame, text="Chưa chọn video nào.", text_color="gray").pack(anchor="w")
            return

        for index, path in enumerate(self.video_paths):
            row = ctk.CTkFrame(self.video_list_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"Ep {index + 1}", width=50).pack(side="left", padx=(8, 4))
            ctk.CTkLabel(row, text=os.path.basename(path), anchor="w").pack(side="left", fill="x", expand=True)
            ctk.CTkButton(row, text="↑", width=30, command=lambda i=index: self._move(i, -1)).pack(
                side="left", padx=2
            )
            ctk.CTkButton(row, text="↓", width=30, command=lambda i=index: self._move(i, 1)).pack(
                side="left", padx=2
            )
            ctk.CTkButton(row, text="Xoá", width=50, command=lambda i=index: self._remove(i)).pack(
                side="left", padx=(2, 8)
            )

    def _move(self, index: int, delta: int):
        target = index + delta
        if target < 0 or target >= len(self.video_paths):
            return
        self.video_paths[index], self.video_paths[target] = self.video_paths[target], self.video_paths[index]
        self._render_video_list()

    def _remove(self, index: int):
        del self.video_paths[index]
        self._render_video_list()

    def _submit(self):
        if not self.srt_path or not self.video_paths:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn file SRT và ít nhất 1 video.")
            return

        self.submit_btn.configure(state="disabled", text="Đang xử lý...")
        self.update_idletasks()
        try:
            outcome = split_srt_files(self.srt_path, self.video_paths, self.output_dir)
            self._render_results(outcome)
        except Exception as exc:
            messagebox.showerror("Lỗi", str(exc))
        finally:
            self.submit_btn.configure(state="normal", text="Tách SRT")

    def _render_results(self, outcome: SrtSplitOutcome):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.results_frame, text="Kết quả", font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", pady=(8, 6)
        )

        if outcome.warnings:
            warn_frame = ctk.CTkFrame(self.results_frame, fg_color="#fef3c7")
            warn_frame.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(
                warn_frame, text="Cảnh báo:", text_color="#92400e", font=ctk.CTkFont(weight="bold")
            ).pack(anchor="w", padx=10, pady=(8, 2))
            for w in outcome.warnings:
                ctk.CTkLabel(
                    warn_frame,
                    text=f"Tập {w.episode_index}, cue #{w.cue_index}: {w.message}",
                    text_color="#92400e",
                    wraplength=600,
                    justify="left",
                ).pack(anchor="w", padx=10, pady=(0, 8))

        for ep in outcome.episodes:
            row = ctk.CTkFrame(self.results_frame)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(
                row,
                text=f"Tập {ep.episode_index} — {os.path.basename(ep.source_video_path)}",
                font=ctk.CTkFont(weight="bold"),
            ).pack(anchor="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(
                row,
                text=f"Đã lưu: {ep.output_path} ({ep.cue_count} cue)",
                text_color="gray",
            ).pack(anchor="w", padx=10, pady=(0, 8))

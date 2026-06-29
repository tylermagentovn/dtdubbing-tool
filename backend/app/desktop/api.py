import webview

VIDEO_FILE_TYPES = ("Video Files (*.mp4;*.mkv;*.mov;*.avi;*.webm)", "All files (*.*)")
SRT_FILE_TYPES = ("Subtitle Files (*.srt)", "All files (*.*)")


class DesktopApi:
    _window: webview.Window

    def pick_srt_file(self):
        result = self._window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=SRT_FILE_TYPES,
        )
        return result[0] if result else None

    def pick_video_files(self):
        result = self._window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=True,
            file_types=VIDEO_FILE_TYPES,
        )
        return list(result) if result else []

    def pick_output_folder(self):
        result = self._window.create_file_dialog(webview.FOLDER_DIALOG)
        return result[0] if result else None

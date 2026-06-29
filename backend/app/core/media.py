import shutil
import subprocess
import sys
from pathlib import Path


def _bundled_binary_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "ffmpeg"
    return Path(__file__).resolve().parent.parent.parent / "vendor" / "ffmpeg"


def find_ffprobe() -> str:
    binary_name = "ffprobe.exe" if sys.platform == "win32" else "ffprobe"
    bundled = _bundled_binary_dir() / binary_name
    if bundled.exists():
        return str(bundled)

    system_path = shutil.which("ffprobe")
    if system_path:
        return system_path

    raise FileNotFoundError(
        "ffprobe not found (not bundled and not on PATH). "
        "Install ffmpeg locally for development, or bundle it under vendor/ffmpeg/ for production."
    )


def get_duration_seconds(video_path: str) -> float:
    ffprobe = find_ffprobe()
    result = subprocess.run(
        [
            ffprobe,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            video_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())

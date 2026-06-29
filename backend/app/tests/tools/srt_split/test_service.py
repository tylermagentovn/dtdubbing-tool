import shutil
import subprocess

import pytest

from app.tools.srt_split.service import split_srt_files

ffmpeg_available = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def _make_test_video(path, duration_seconds: int) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=black:s=64x64:d={duration_seconds}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


@pytest.mark.skipif(not ffmpeg_available, reason="ffmpeg/ffprobe not installed on this machine")
def test_split_srt_files_writes_per_episode_files_with_rebased_timestamps(tmp_path):
    ep1_video = tmp_path / "ep01.mp4"
    ep2_video = tmp_path / "ep02.mp4"
    _make_test_video(ep1_video, duration_seconds=5)
    _make_test_video(ep2_video, duration_seconds=5)

    srt_path = tmp_path / "master.srt"
    srt_path.write_text(
        "1\n00:00:01,000 --> 00:00:02,000\nEp1 cue\n\n"
        "2\n00:00:07,000 --> 00:00:08,000\nEp2 cue\n",
        encoding="utf-8",
    )

    outcome = split_srt_files(str(srt_path), [str(ep1_video), str(ep2_video)])

    assert len(outcome.episodes) == 2
    ep1_out = outcome.episodes[0].output_path
    ep2_out = outcome.episodes[1].output_path

    assert ep1_out.endswith("ep01.srt")
    assert ep2_out.endswith("ep02.srt")

    ep1_content = open(ep1_out, encoding="utf-8").read()
    ep2_content = open(ep2_out, encoding="utf-8").read()

    assert "00:00:01,000 --> 00:00:02,000" in ep1_content
    assert "00:00:02,000 --> 00:00:03,000" in ep2_content  # 7s - 5s ep1 duration = 2s
    assert outcome.warnings == []


def test_split_srt_files_requires_at_least_one_video_path(tmp_path):
    srt_path = tmp_path / "master.srt"
    srt_path.write_text("1\n00:00:01,000 --> 00:00:02,000\nHi\n", encoding="utf-8")

    with pytest.raises(ValueError):
        split_srt_files(str(srt_path), [])

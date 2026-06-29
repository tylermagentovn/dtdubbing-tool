from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.core.media import get_duration_seconds
from app.tools.srt_split.splitter import CueWarning, split_cues_by_durations
from app.tools.srt_split.srt_parser import parse_srt
from app.tools.srt_split.srt_writer import render_srt


@dataclass
class EpisodeResult:
    episode_index: int
    source_video_path: str
    output_path: str
    cue_count: int


@dataclass
class SrtSplitOutcome:
    episodes: list[EpisodeResult]
    warnings: list[CueWarning]


def split_srt_files(
    srt_path: str, video_paths: list[str], output_dir: Optional[str] = None
) -> SrtSplitOutcome:
    if not video_paths:
        raise ValueError("At least one video path is required")

    srt_content = Path(srt_path).read_text(encoding="utf-8-sig")
    cues = parse_srt(srt_content)

    durations = [get_duration_seconds(path) for path in video_paths]
    result = split_cues_by_durations(cues, durations)

    out_dir = Path(output_dir) if output_dir else Path(srt_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    episodes = []
    for i, (video_path, bucket) in enumerate(zip(video_paths, result.buckets)):
        output_path = out_dir / f"{Path(video_path).stem}.srt"
        output_path.write_text(render_srt(bucket.cues), encoding="utf-8")
        episodes.append(
            EpisodeResult(
                episode_index=i + 1,
                source_video_path=video_path,
                output_path=str(output_path),
                cue_count=len(bucket.cues),
            )
        )

    return SrtSplitOutcome(episodes=episodes, warnings=result.warnings)

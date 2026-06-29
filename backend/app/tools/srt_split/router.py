from pathlib import Path

from fastapi import APIRouter

from app.core.media import get_duration_seconds
from app.tools.srt_split.schemas import EpisodeSrtFile, SrtSplitRequest, SrtSplitResponse
from app.tools.srt_split.splitter import split_cues_by_durations
from app.tools.srt_split.srt_parser import parse_srt
from app.tools.srt_split.srt_writer import render_srt

router = APIRouter(prefix="/api/tools/srt-split", tags=["srt-split"])


@router.post("/split", response_model=SrtSplitResponse)
def split_srt(body: SrtSplitRequest) -> SrtSplitResponse:
    srt_content = Path(body.srt_path).read_text(encoding="utf-8-sig")
    cues = parse_srt(srt_content)

    durations = [get_duration_seconds(path) for path in body.video_paths]
    result = split_cues_by_durations(cues, durations)

    output_dir = Path(body.output_dir) if body.output_dir else Path(body.srt_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    episodes = []
    for i, (video_path, bucket) in enumerate(zip(body.video_paths, result.buckets)):
        output_path = output_dir / f"{Path(video_path).stem}.srt"
        output_path.write_text(render_srt(bucket.cues), encoding="utf-8")
        episodes.append(
            EpisodeSrtFile(
                episode_index=i + 1,
                source_video_path=video_path,
                output_path=str(output_path),
                cue_count=len(bucket.cues),
            )
        )

    return SrtSplitResponse(episodes=episodes, warnings=result.warnings)

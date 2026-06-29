from __future__ import annotations

from dataclasses import dataclass, field

from app.tools.srt_split.srt_parser import Cue


@dataclass
class CueWarning:
    episode_index: int
    cue_index: int
    message: str


@dataclass
class Bucket:
    cues: list[Cue] = field(default_factory=list)


@dataclass
class SplitResult:
    buckets: list[Bucket]
    warnings: list[CueWarning]


def _build_boundaries_ms(durations_seconds: list[float]) -> list[tuple[int, int]]:
    boundaries: list[tuple[int, int]] = []
    cursor = 0
    for duration in durations_seconds:
        start = cursor
        end = cursor + round(duration * 1000)
        boundaries.append((start, end))
        cursor = end
    return boundaries


def _find_episode_index_for_start(start_ms: int, boundaries_ms: list[tuple[int, int]]) -> int | None:
    for i, (start, end) in enumerate(boundaries_ms):
        if start <= start_ms < end:
            return i
    return None


def split_cues_by_durations(cues: list[Cue], durations_seconds: list[float]) -> SplitResult:
    boundaries_ms = _build_boundaries_ms(durations_seconds)
    buckets = [Bucket() for _ in durations_seconds]
    warnings: list[CueWarning] = []

    for cue in cues:
        ep_idx = _find_episode_index_for_start(cue.start_ms, boundaries_ms)

        if ep_idx is None:
            warnings.append(
                CueWarning(
                    episode_index=len(durations_seconds),
                    cue_index=cue.index,
                    message=(
                        f"Cue starts at {cue.start_ms}ms, beyond total episodes "
                        "duration; dropped"
                    ),
                )
            )
            continue

        ep_start, ep_end = boundaries_ms[ep_idx]
        rebased_start = cue.start_ms - ep_start
        rebased_end = cue.end_ms - ep_start
        episode_duration_ms = ep_end - ep_start

        if rebased_end > episode_duration_ms:
            overflow_ms = rebased_end - episode_duration_ms
            warnings.append(
                CueWarning(
                    episode_index=ep_idx + 1,
                    cue_index=cue.index,
                    message=f"Cue end overflows episode boundary by {overflow_ms}ms; clamped",
                )
            )
            rebased_end = episode_duration_ms

        buckets[ep_idx].cues.append(
            Cue(index=cue.index, start_ms=rebased_start, end_ms=rebased_end, text=cue.text)
        )

    return SplitResult(buckets=buckets, warnings=warnings)

from app.tools.srt_split.srt_parser import Cue


def _format_timestamp(ms: int) -> str:
    hh, rem = divmod(ms, 3_600_000)
    mm, rem = divmod(rem, 60_000)
    ss, mmm = divmod(rem, 1000)
    return f"{hh:02d}:{mm:02d}:{ss:02d},{mmm:03d}"


def render_srt(cues: list[Cue]) -> str:
    blocks = []
    for i, cue in enumerate(cues, start=1):
        timing = f"{_format_timestamp(cue.start_ms)} --> {_format_timestamp(cue.end_ms)}"
        blocks.append(f"{i}\n{timing}\n{cue.text}")
    return "\n\n".join(blocks) + "\n"

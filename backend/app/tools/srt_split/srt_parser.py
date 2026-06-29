import re
from dataclasses import dataclass

_TIMING_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
)


@dataclass
class Cue:
    index: int
    start_ms: int
    end_ms: int
    text: str


def _timestamp_to_ms(hh: str, mm: str, ss: str, mmm: str) -> int:
    return (
        int(hh) * 3_600_000
        + int(mm) * 60_000
        + int(ss) * 1000
        + int(mmm)
    )


def parse_srt(raw_text: str) -> list[Cue]:
    text = raw_text.lstrip("﻿")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    blocks = re.split(r"\n{2,}", text.strip())
    cues: list[Cue] = []
    counter = 0

    for block in blocks:
        lines = [line for line in block.split("\n")]
        if not lines:
            continue

        timing_line_idx = None
        match = None
        for i, line in enumerate(lines):
            m = _TIMING_RE.search(line)
            if m:
                timing_line_idx = i
                match = m
                break

        if match is None:
            continue

        counter += 1
        start_ms = _timestamp_to_ms(*match.group(1, 2, 3, 4))
        end_ms = _timestamp_to_ms(*match.group(5, 6, 7, 8))
        text_lines = lines[timing_line_idx + 1 :]
        cue_text = "\n".join(text_lines).strip()

        cues.append(Cue(index=counter, start_ms=start_ms, end_ms=end_ms, text=cue_text))

    return sorted(cues, key=lambda c: c.start_ms)

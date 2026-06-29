from app.tools.srt_split.srt_parser import parse_srt

BASIC_SRT = """1
00:00:01,000 --> 00:00:03,500
Hello world

2
00:00:05,200 --> 00:00:07,000
Second line
"""


def test_parses_basic_cues():
    cues = parse_srt(BASIC_SRT)
    assert len(cues) == 2
    assert cues[0].start_ms == 1000
    assert cues[0].end_ms == 3500
    assert cues[0].text == "Hello world"
    assert cues[1].start_ms == 5200
    assert cues[1].end_ms == 7000


def test_strips_bom():
    cues = parse_srt("﻿" + BASIC_SRT)
    assert len(cues) == 2


def test_handles_crlf():
    crlf_text = BASIC_SRT.replace("\n", "\r\n")
    cues = parse_srt(crlf_text)
    assert len(cues) == 2
    assert cues[0].start_ms == 1000


def test_handles_dot_ms_separator():
    text = "1\n00:00:01.000 --> 00:00:02.000\nDot separator\n"
    cues = parse_srt(text)
    assert len(cues) == 1
    assert cues[0].end_ms == 2000


def test_sorts_by_start_time():
    text = (
        "1\n00:00:10,000 --> 00:00:11,000\nLater\n\n"
        "2\n00:00:01,000 --> 00:00:02,000\nEarlier\n"
    )
    cues = parse_srt(text)
    assert [c.text for c in cues] == ["Earlier", "Later"]


def test_skips_malformed_blocks():
    text = BASIC_SRT + "\n\nnot a valid block at all"
    cues = parse_srt(text)
    assert len(cues) == 2


def test_multiline_cue_text_preserved():
    text = "1\n00:00:01,000 --> 00:00:02,000\nLine one\nLine two\n"
    cues = parse_srt(text)
    assert cues[0].text == "Line one\nLine two"

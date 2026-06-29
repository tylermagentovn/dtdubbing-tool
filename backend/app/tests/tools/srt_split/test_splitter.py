from app.tools.srt_split.srt_parser import Cue
from app.tools.srt_split.splitter import split_cues_by_durations


def test_assigns_cues_to_correct_episode_and_rebases():
    cues = [
        Cue(index=1, start_ms=1000, end_ms=2000, text="ep1 cue"),
        Cue(index=2, start_ms=11000, end_ms=12000, text="ep2 cue"),
    ]
    result = split_cues_by_durations(cues, [10.0, 10.0])

    assert len(result.buckets) == 2
    assert len(result.buckets[0].cues) == 1
    assert result.buckets[0].cues[0].start_ms == 1000
    assert result.buckets[0].cues[0].end_ms == 2000

    assert len(result.buckets[1].cues) == 1
    assert result.buckets[1].cues[0].start_ms == 1000
    assert result.buckets[1].cues[0].end_ms == 2000
    assert result.warnings == []


def test_boundary_crossing_cue_assigned_to_start_episode_and_clamped():
    # episode 1 is [0, 10000)ms; this cue starts at 9000 (inside ep1) and ends at 11000 (inside ep2)
    cues = [Cue(index=1, start_ms=9000, end_ms=11000, text="straddler")]
    result = split_cues_by_durations(cues, [10.0, 10.0])

    assert len(result.buckets[0].cues) == 1
    assert len(result.buckets[1].cues) == 0

    straddler = result.buckets[0].cues[0]
    assert straddler.start_ms == 9000
    assert straddler.end_ms == 10000  # clamped to episode 1's end

    assert len(result.warnings) == 1
    assert result.warnings[0].episode_index == 1
    assert result.warnings[0].cue_index == 1
    assert "clamped" in result.warnings[0].message


def test_cue_beyond_total_duration_is_dropped_with_warning():
    cues = [Cue(index=1, start_ms=25000, end_ms=26000, text="too late")]
    result = split_cues_by_durations(cues, [10.0, 10.0])

    assert all(len(b.cues) == 0 for b in result.buckets)
    assert len(result.warnings) == 1
    assert "dropped" in result.warnings[0].message


def test_empty_cues_returns_empty_buckets_no_warnings():
    result = split_cues_by_durations([], [10.0, 10.0])
    assert len(result.buckets) == 2
    assert all(len(b.cues) == 0 for b in result.buckets)
    assert result.warnings == []

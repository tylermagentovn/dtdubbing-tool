from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SrtSplitRequest(BaseModel):
    srt_path: str
    video_paths: list[str]
    output_dir: Optional[str] = None

    @field_validator("video_paths")
    @classmethod
    def must_have_videos(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("At least one video path is required")
        return v


class CueWarning(BaseModel):
    episode_index: int
    cue_index: int
    message: str


class EpisodeSrtFile(BaseModel):
    episode_index: int
    source_video_path: str
    output_path: str
    cue_count: int


class SrtSplitResponse(BaseModel):
    episodes: list[EpisodeSrtFile]
    warnings: list[CueWarning] = Field(default_factory=list)

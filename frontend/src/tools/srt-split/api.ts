import { apiClient } from '../../shared/api/client'

export interface CueWarning {
  episode_index: number
  cue_index: number
  message: string
}

export interface EpisodeSrtFile {
  episode_index: number
  source_video_path: string
  output_path: string
  cue_count: number
}

export interface SrtSplitResponse {
  episodes: EpisodeSrtFile[]
  warnings: CueWarning[]
}

export interface SrtSplitRequest {
  srt_path: string
  video_paths: string[]
  output_dir?: string | null
}

export function splitSrt(payload: SrtSplitRequest): Promise<SrtSplitResponse> {
  return apiClient.post<SrtSplitResponse>('/api/tools/srt-split/split', payload)
}

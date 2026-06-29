export interface ToolMeta {
  id: string
  name: string
  description: string
  path: string
}

export const TOOL_REGISTRY: ToolMeta[] = [
  {
    id: 'srt-split',
    name: 'Tách SRT',
    description: 'Chia file SRT gốc theo thời lượng từng episode video',
    path: '/tools/srt-split',
  },
]

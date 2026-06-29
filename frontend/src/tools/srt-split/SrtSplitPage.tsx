import { useState } from 'react'
import { Button } from '../../shared/ui/Button'
import { getDesktopApi } from '../../shared/desktop/pywebview'
import { ApiError } from '../../shared/api/client'
import { splitSrt, type SrtSplitResponse } from './api'
import { VideoPathList } from './components/VideoPathList'
import { ResultsPanel } from './components/ResultsPanel'

function basename(path: string): string {
  return path.split(/[\\/]/).pop() ?? path
}

export function SrtSplitPage() {
  const [srtPath, setSrtPath] = useState<string | null>(null)
  const [videoPaths, setVideoPaths] = useState<string[]>([])
  const [outputDir, setOutputDir] = useState<string | null>(null)
  const [result, setResult] = useState<SrtSplitResponse | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handlePickSrt = async () => {
    const api = await getDesktopApi()
    const path = await api.pick_srt_file()
    if (path) setSrtPath(path)
  }

  const handlePickVideos = async () => {
    const api = await getDesktopApi()
    const paths = await api.pick_video_files()
    if (paths.length > 0) setVideoPaths(paths)
  }

  const handlePickOutputDir = async () => {
    const api = await getDesktopApi()
    const path = await api.pick_output_folder()
    if (path) setOutputDir(path)
  }

  const handleSubmit = async () => {
    if (!srtPath || videoPaths.length === 0) return
    setIsProcessing(true)
    setError(null)
    setResult(null)
    try {
      const res = await splitSrt({ srt_path: srtPath, video_paths: videoPaths, output_dir: outputDir })
      setResult(res)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Có lỗi xảy ra khi tách SRT')
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div style={{ maxWidth: 640 }}>
      <h1 style={{ fontSize: '1.5rem' }}>Tách SRT</h1>
      <p style={{ color: '#666' }}>
        Chia file SRT gốc thành các file SRT riêng cho từng tập, dựa theo thời lượng video tương ứng.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginTop: '1rem' }}>
        <div>
          <Button variant="secondary" onClick={() => void handlePickSrt()}>
            Chọn file SRT gốc
          </Button>
          <div style={{ marginTop: '0.4rem', fontSize: '0.9rem', color: srtPath ? '#111' : '#999' }}>
            {srtPath ? basename(srtPath) : 'Chưa chọn file'}
          </div>
        </div>

        <div>
          <Button variant="secondary" onClick={() => void handlePickVideos()}>
            Chọn video các tập
          </Button>
          <div style={{ marginTop: '0.6rem' }}>
            <VideoPathList paths={videoPaths} onReorder={setVideoPaths} />
          </div>
        </div>

        <div>
          <Button variant="secondary" onClick={() => void handlePickOutputDir()}>
            Chọn thư mục lưu kết quả (tuỳ chọn)
          </Button>
          <div style={{ marginTop: '0.4rem', fontSize: '0.9rem', color: outputDir ? '#111' : '#999' }}>
            {outputDir ? outputDir : 'Mặc định: lưu cùng thư mục với file SRT gốc'}
          </div>
        </div>

        <Button
          onClick={() => void handleSubmit()}
          disabled={!srtPath || videoPaths.length === 0 || isProcessing}
        >
          {isProcessing ? 'Đang xử lý...' : 'Tách SRT'}
        </Button>

        {error && <div style={{ color: '#dc2626' }}>{error}</div>}
      </div>

      {result && <ResultsPanel result={result} />}
    </div>
  )
}

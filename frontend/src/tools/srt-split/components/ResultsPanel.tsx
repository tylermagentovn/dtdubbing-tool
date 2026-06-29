import type { SrtSplitResponse } from '../api'

function basename(path: string): string {
  return path.split(/[\\/]/).pop() ?? path
}

export function ResultsPanel({ result }: { result: SrtSplitResponse }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h2 style={{ fontSize: '1.1rem' }}>Kết quả</h2>

      {result.warnings.length > 0 && (
        <div
          style={{
            background: '#fef3c7',
            border: '1px solid #fcd34d',
            borderRadius: 6,
            padding: '0.75rem',
            marginBottom: '1rem',
            fontSize: '0.9rem',
          }}
        >
          <strong>Cảnh báo:</strong>
          <ul style={{ margin: '0.5rem 0 0', paddingLeft: '1.2rem' }}>
            {result.warnings.map((w, i) => (
              <li key={i}>
                Tập {w.episode_index}, cue #{w.cue_index}: {w.message}
              </li>
            ))}
          </ul>
        </div>
      )}

      <ul style={{ padding: 0, margin: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
        {result.episodes.map((ep) => (
          <li
            key={ep.episode_index}
            style={{ border: '1px solid #e5e4e7', borderRadius: 6, padding: '0.6rem' }}
          >
            <div style={{ fontWeight: 600 }}>
              Tập {ep.episode_index} — {basename(ep.source_video_path)}
            </div>
            <div style={{ fontSize: '0.85rem', color: '#555' }}>
              Đã lưu: {ep.output_path} ({ep.cue_count} cue)
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

interface VideoPathListProps {
  paths: string[]
  onReorder: (paths: string[]) => void
}

function basename(path: string): string {
  return path.split(/[\\/]/).pop() ?? path
}

export function VideoPathList({ paths, onReorder }: VideoPathListProps) {
  const move = (index: number, delta: number) => {
    const next = [...paths]
    const target = index + delta
    if (target < 0 || target >= next.length) return
    ;[next[index], next[target]] = [next[target], next[index]]
    onReorder(next)
  }

  const remove = (index: number) => {
    onReorder(paths.filter((_, i) => i !== index))
  }

  if (paths.length === 0) {
    return <p style={{ color: '#666', fontSize: '0.9rem' }}>Chưa chọn video nào.</p>
  }

  return (
    <ol style={{ padding: 0, margin: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
      {paths.map((path, index) => (
        <li
          key={path}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            border: '1px solid #e5e4e7',
            borderRadius: 6,
            padding: '0.4rem 0.6rem',
          }}
        >
          <span style={{ fontWeight: 600, minWidth: '2rem' }}>Ep {index + 1}</span>
          <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {basename(path)}
          </span>
          <button onClick={() => move(index, -1)} disabled={index === 0}>↑</button>
          <button onClick={() => move(index, 1)} disabled={index === paths.length - 1}>↓</button>
          <button onClick={() => remove(index)}>Xoá</button>
        </li>
      ))}
    </ol>
  )
}

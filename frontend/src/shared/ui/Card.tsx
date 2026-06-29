import type { ReactNode } from 'react'

export function Card({ children }: { children: ReactNode }) {
  return (
    <div
      style={{
        border: '1px solid #e5e4e7',
        borderRadius: 8,
        padding: '1.25rem',
        background: 'var(--card-bg, #fff)',
      }}
    >
      {children}
    </div>
  )
}

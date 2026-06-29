import type { ButtonHTMLAttributes } from 'react'

type Variant = 'primary' | 'secondary'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
}

const baseStyle = {
  border: '1px solid #ccc',
  borderRadius: 6,
  padding: '0.5rem 1rem',
  fontSize: '0.95rem',
}

const variantStyle: Record<Variant, React.CSSProperties> = {
  primary: { ...baseStyle, background: '#2563eb', color: '#fff', borderColor: '#2563eb' },
  secondary: { ...baseStyle, background: '#fff', color: '#111' },
}

export function Button({ variant = 'primary', style, ...props }: ButtonProps) {
  return <button style={{ ...variantStyle[variant], ...style }} {...props} />
}

import { NavLink } from 'react-router-dom'
import { TOOL_REGISTRY } from '../tool-registry/registry'

export function Sidebar() {
  return (
    <aside
      style={{
        width: 220,
        borderRight: '1px solid #e5e4e7',
        padding: '1rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
      }}
    >
      <NavLink to="/" style={{ fontWeight: 600, marginBottom: '1rem', textDecoration: 'none' }}>
        DTDUBBING Tools
      </NavLink>

      {TOOL_REGISTRY.map((tool) => (
        <NavLink
          key={tool.id}
          to={tool.path}
          style={({ isActive }) => ({
            textDecoration: 'none',
            padding: '0.4rem 0.6rem',
            borderRadius: 6,
            background: isActive ? '#eef2ff' : 'transparent',
          })}
        >
          {tool.name}
        </NavLink>
      ))}
    </aside>
  )
}

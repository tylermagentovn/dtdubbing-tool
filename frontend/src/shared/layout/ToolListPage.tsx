import { Link } from 'react-router-dom'
import { TOOL_REGISTRY } from '../tool-registry/registry'
import { Card } from '../ui/Card'

export function ToolListPage() {
  return (
    <div>
      <h1 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Danh sách tool</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '1rem' }}>
        {TOOL_REGISTRY.map((tool) => (
          <Link key={tool.id} to={tool.path} style={{ textDecoration: 'none', color: 'inherit' }}>
            <Card>
              <h2 style={{ fontSize: '1.1rem', margin: '0 0 0.5rem' }}>{tool.name}</h2>
              <p style={{ margin: 0, fontSize: '0.9rem', color: '#666' }}>{tool.description}</p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}

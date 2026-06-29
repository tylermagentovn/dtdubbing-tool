import { Route, Routes } from 'react-router-dom'
import { AppShell } from './shared/layout/AppShell'
import { ToolListPage } from './shared/layout/ToolListPage'
import { SrtSplitPage } from './tools/srt-split/SrtSplitPage'

function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<ToolListPage />} />
        <Route path="/tools/srt-split" element={<SrtSplitPage />} />
      </Route>
    </Routes>
  )
}

export default App

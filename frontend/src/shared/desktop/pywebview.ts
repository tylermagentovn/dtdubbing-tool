export interface PywebviewApi {
  pick_srt_file(): Promise<string | null>
  pick_video_files(): Promise<string[]>
  pick_output_folder(): Promise<string | null>
}

declare global {
  interface Window {
    pywebview?: { api: PywebviewApi }
  }
}

function readyPromise(): Promise<void> {
  if (window.pywebview) return Promise.resolve()
  return new Promise((resolve) => {
    window.addEventListener('pywebviewready', () => resolve(), { once: true })
  })
}

export async function getDesktopApi(): Promise<PywebviewApi> {
  await readyPromise()
  if (!window.pywebview) {
    throw new Error('pywebview API không khả dụng — app phải chạy trong cửa sổ desktop')
  }
  return window.pywebview.api
}

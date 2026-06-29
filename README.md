# DTDUBBING Tools

App desktop local (pywebview + FastAPI) chứa các tool nội bộ cho DTDUBBING, chủ yếu liên quan đến xử lý ffmpeg. Không cần đăng nhập, không cần upload file qua mạng — backend đọc/ghi trực tiếp trên đĩa của máy đang chạy app.

## Cấu trúc

- `backend/` — FastAPI + pywebview (Python). Mỗi tool là 1 package trong `backend/app/tools/<tool_name>/`.
- `frontend/` — React + TypeScript (Vite). Mỗi tool là 1 folder trong `frontend/src/tools/<tool-name>/`.

## Chạy dev

```bash
# 1. Backend deps
cd backend
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 2. Frontend deps
cd ../frontend
npm install

# 3. Chạy Vite dev server (hot reload)
npm run dev   # http://localhost:5173

# 4. Chạy app desktop, trỏ vào Vite dev server
cd ../backend
DTDUBBING_DEV_URL=http://localhost:5173 ./venv/bin/python -m app.desktop.main
```

Cửa sổ desktop sẽ mở lên, gọi API qua `window.pywebview.api` (native file dialogs) và qua FastAPI tại `http://127.0.0.1:8765`.

## Build ra file .exe (chạy trực tiếp trên máy Windows — PyInstaller không cross-compile được)

Toàn bộ các bước dưới đây chạy trong **PowerShell trên Windows**, không chạy trên Mac.

### Bước 0 — Cài công cụ trên máy Windows

- [Python 3.11+](https://www.python.org/downloads/) — khi cài, tick **"Add python.exe to PATH"**.
- [Node.js LTS](https://nodejs.org/) — để build frontend.
- (Khuyên dùng) Windows 10/11 bản mới đã có sẵn **WebView2 Runtime** (Edge engine) mà pywebview cần để hiển thị UI. Nếu app chạy lên mà cửa sổ trống/không hiện gì, cài [WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/) rồi thử lại.

### Bước 1 — Copy code dự án sang máy Windows

Copy/clone toàn bộ thư mục `dtdubbing-tool` sang máy Windows (qua git, USB, hoặc zip rồi giải nén).

### Bước 2 — Tải ffmpeg cho Windows

1. Vào trang chính thức **https://ffmpeg.org/download.html** → chọn icon Windows → chọn 1 link build (gyan.dev hoặc BtbN, đều được ffmpeg.org official giới thiệu) → tải bản **"release essentials"** hoặc **"release full"** (file `.zip` hoặc `.7z`).
2. Giải nén ra, vào thư mục con `bin\`, sẽ thấy 2 file `ffmpeg.exe` và `ffprobe.exe`.
3. Trong project, tạo thư mục `backend\vendor\ffmpeg\` và copy 2 file đó vào — dùng được ngay khi chạy dev/test trên Windows (code tự tìm ở đây qua `app/core/media.py::_bundled_binary_dir()`).

### Bước 3 — Cài dependencies Python + Node

```powershell
cd dtdubbing-tool\backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt

cd ..\frontend
npm install
```

### Bước 4 — Build frontend tĩnh và copy vào backend

```powershell
cd dtdubbing-tool\frontend
npm run build
rmdir /s /q ..\backend\static
xcopy dist ..\backend\static /E /I /Y
```

### Bước 5 — Đóng gói bằng PyInstaller

Lưu ý: trên Windows, dấu phân tách của `--add-data` là `;` (không phải `:` như macOS/Linux).

```powershell
cd ..\backend
venv\Scripts\pyinstaller --name DTDubbingTools --onedir app\desktop\main.py --add-data "static;static"
```

Kết quả nằm ở `backend\dist\DTDubbingTools\` (chứa `DTDubbingTools.exe` + các file hỗ trợ).

Nếu khi chạy thử báo lỗi `ModuleNotFoundError: <tên module>` (thường gặp với các plugin của uvicorn như `httptools`, `websockets`), thêm `--hidden-import <tên module>` vào lệnh trên rồi build lại.

### Bước 6 — Copy ffmpeg vào bản build

```powershell
mkdir dist\DTDubbingTools\ffmpeg
copy vendor\ffmpeg\ffmpeg.exe dist\DTDubbingTools\ffmpeg\
copy vendor\ffmpeg\ffprobe.exe dist\DTDubbingTools\ffmpeg\
```

(`_bundled_binary_dir()` tìm ffmpeg ở thư mục `ffmpeg\` ngay cạnh file `.exe` khi app đã đóng gói.)

### Bước 7 — Chạy thử và phân phối

Double-click `dist\DTDubbingTools\DTDubbingTools.exe` để test. Nếu chạy ổn, zip nguyên thư mục `DTDubbingTools\` lại và gửi cho máy studio khác — chỉ cần giải nén và chạy file `.exe`, không cần cài Python/Node/ffmpeg riêng.

## Test backend

```bash
cd backend
./venv/bin/python -m pytest -q
```

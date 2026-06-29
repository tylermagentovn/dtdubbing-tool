# DTDUBBING Tools

App desktop local (CustomTkinter, Python thuần) chứa các tool nội bộ cho DTDUBBING, chủ yếu liên quan đến xử lý ffmpeg. Không cần đăng nhập, không cần mạng/web server — chọn file qua dialog native của hệ điều hành, xử lý và ghi kết quả trực tiếp ra đĩa.

## Cấu trúc

```
backend/
  app/
    core/media.py              # wrapper gọi ffprobe (tìm bundled binary hoặc PATH hệ thống)
    tools/
      registry.py               # danh sách tool hiển thị ở sidebar — thêm tool mới: thêm 1 entry ở đây
      srt_split/
        srt_parser.py            # parse file .srt
        splitter.py               # logic chia cue theo duration từng tập
        srt_writer.py             # render cue thành .srt
        service.py                 # orchestrate: đọc srt, gọi ffprobe, ghi file kết quả
        gui.py                      # CustomTkinter Frame cho tool này
    desktop/
      app_shell.py               # cửa sổ chính: sidebar + vùng nội dung, chuyển tool
      main.py                     # entry point chạy app
    tests/                       # pytest, chạy logic trực tiếp (không cần mock GUI)
```

Mỗi tool mới: tạo 1 package trong `backend/app/tools/<tool_name>/` với 1 `*.py` chứa logic xử lý + 1 `gui.py` chứa `CTkFrame`, rồi thêm `ToolMeta` vào `registry.py`. Không cần sửa `app_shell.py`.

## Chạy dev

```bash
cd backend
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python -m app.desktop.main
```

Cần có `ffmpeg`/`ffprobe` trên máy dev (`brew install ffmpeg` trên macOS, hoặc xem hướng dẫn tải ở phần build dưới) — nếu không có, tool Tách SRT sẽ báo lỗi khi tính duration video.

## Test

```bash
cd backend
./venv/bin/python -m pytest -q
```

## Build ra file .exe (chạy trực tiếp trên máy Windows — PyInstaller không cross-compile được)

Toàn bộ các bước dưới đây chạy trong **PowerShell trên Windows**.

### Bước 0 — Cài Python trên máy Windows

[Python 3.11+](https://www.python.org/downloads/) — khi cài, tick **"Add python.exe to PATH"**. Bản cài chính thức từ python.org đã có sẵn Tk/tkinter, không cần cài thêm gì cho GUI.

### Bước 1 — Copy code dự án sang máy Windows

Copy/clone toàn bộ thư mục `dtdubbing-tool` sang máy Windows.

### Bước 2 — Tải ffmpeg cho Windows

1. Vào trang chính thức **https://ffmpeg.org/download.html** → chọn icon Windows → chọn 1 link build (gyan.dev hoặc BtbN, đều được ffmpeg.org giới thiệu) → tải bản **"release essentials"**.
2. Giải nén, vào thư mục con `bin\`, lấy 2 file `ffmpeg.exe` và `ffprobe.exe`.
3. Tạo thư mục `backend\vendor\ffmpeg\` trong project, copy 2 file đó vào (dùng được ngay khi test trên Windows trước khi build — xem `app/core/media.py::_bundled_binary_dir()`).

### Bước 3 — Cài dependencies

```powershell
cd dtdubbing-tool\backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

### Bước 4 — Đóng gói bằng PyInstaller

```powershell
venv\Scripts\pyinstaller --name DTDubbingTools --onedir app\desktop\main.py
```

Kết quả nằm ở `backend\dist\DTDubbingTools\` (chứa `DTDubbingTools.exe` + các file hỗ trợ).

Nếu chạy thử báo lỗi liên quan tới `tkinter`/`_tkinter` không tìm thấy, thêm cờ `--collect-all customtkinter` vào lệnh trên rồi build lại.

### Bước 5 — Copy ffmpeg vào bản build

```powershell
mkdir dist\DTDubbingTools\ffmpeg
copy vendor\ffmpeg\ffmpeg.exe dist\DTDubbingTools\ffmpeg\
copy vendor\ffmpeg\ffprobe.exe dist\DTDubbingTools\ffmpeg\
```

### Bước 6 — Chạy thử và phân phối

Double-click `dist\DTDubbingTools\DTDubbingTools.exe`. Nếu chạy ổn, zip nguyên thư mục `DTDubbingTools\` và gửi cho máy khác trong studio — chỉ cần giải nén và chạy `.exe`, không cần cài Python/ffmpeg riêng.

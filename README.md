# 25分｜跨平台番茄鐘

一個以「提醒一定看得到」為核心的 Windows／macOS 桌面番茄鐘。每輪專注固定 25 分鐘，完成時顯示全螢幕置頂休息卡，隨機提供小知識、名言或追點小遊戲。提醒必須按下「開始下一輪」或「1 分鐘後再提醒」才會離開，不依賴聲音或短暫動畫。

## 功能

- 25 分鐘開始、暫停、繼續與重設
- 全螢幕、置頂、需互動的休息提醒
- 隨機小知識、名言與 8 次追點小遊戲
- 可延後 1 分鐘再次提醒
- 自動開始下一輪專注
- 以 SQLite 保存每日完成輪數與專注分鐘數
- 僅使用 Python 標準函式庫，執行階段沒有額外依賴

## 開發環境

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Tk 8.6（Windows 官方 Python 安裝程式通常已包含；macOS 建議使用 python.org 安裝版本）

## 執行

```powershell
cd pause25
uv sync --group dev
uv run pause25
```

macOS 的 Terminal 指令相同；第一行改成專案所在路徑。

## 測試

```powershell
uv run pytest
```

測試涵蓋倒數狀態、完成事件只觸發一次，以及 SQLite 資料在程式關閉重開後仍存在。

## 產生桌面執行檔

Windows 與 macOS 必須分別在各自的作業系統建置，PyInstaller 不能跨平台產生另一個系統的程式。

```powershell
uv sync --group dev
uv run pyinstaller --noconfirm --windowed --name Pause25 --paths src src/pause25/__main__.py
```

完成後檔案在 `dist/Pause25/`。Windows 可開啟 `Pause25.exe`；macOS 可開啟 `Pause25.app`。

## 資料位置

- Windows：`%LOCALAPPDATA%\Pause25\pause25.sqlite3`
- macOS：`~/Library/Application Support/Pause25/pause25.sqlite3`

刪除程式本體不會自動刪除專注紀錄。

## 常見錯誤與處理

### `uv` 不是可辨識的指令

依照 [uv 官方安裝說明](https://docs.astral.sh/uv/getting-started/installation/) 安裝後，關閉並重新開啟 Terminal／PowerShell。

### `ModuleNotFoundError: No module named '_tkinter'`

目前 Python 未包含 Tk。Windows 請重新執行 Python 安裝程式並勾選 `tcl/tk and IDLE`；macOS 建議改用 python.org 的 Python 3.12+ 安裝版本。

### macOS 第一次開啟 `.app` 被阻擋

在 Finder 對 `Pause25.app` 按右鍵選「打開」。若要分發給其他人，仍需使用 Apple Developer ID 簽署與 notarization。

### 提醒沒有蓋住另一個螢幕

目前版本會覆蓋主視窗所在的顯示器。多螢幕同時覆蓋與系統通知整合不在此 MVP 範圍。

## 操作驗收清單

1. 執行 `uv run pause25`，預期看到 `25:00` 與「開始專注」。
2. 按「開始專注」，預期時間開始倒數，狀態顯示「專注中」。
3. 按「暫停」再按「繼續專注」，預期倒數停住後從原時間繼續。
4. 等倒數完成，預期出現全螢幕置頂休息卡，內容為小知識、名言或小遊戲之一。
5. 按 `Esc`，預期提醒不會關閉；按「1 分鐘後再提醒」，預期視窗暫時離開並在 1 分鐘後再次出現。
6. 按「我休息好了，開始下一輪」，預期休息卡關閉且新的 25 分鐘自動開始。
7. 關閉並重開程式，預期「今天」的輪數與累積分鐘仍保留。

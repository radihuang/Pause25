# 25分｜跨平台番茄鐘

一個以「提醒一定看得到」為核心的 Windows／macOS 桌面番茄鐘。每輪專注固定 25 分鐘，完成時顯示全螢幕置頂休息卡，隨機提供小知識、名言或追點小遊戲。提醒必須按下「開始下一輪」或「1 分鐘後再提醒」才會離開，不依賴聲音或短暫動畫。

## 功能

- 25 分鐘開始、暫停、繼續與重設
- 全螢幕、置頂、需互動的休息提醒
- 隨機鯨豚選擇題、名言與大範圍 8 次追點小遊戲
- 小知識作答後標示正解並顯示完整解釋
- Windows High DPI 與 macOS Retina 清晰顯示
- 可延後 1 分鐘再次提醒
- 休息卡內建 5 分鐘倒數，歸零自動開始下一輪
- 休息提示固定提醒喝水裝水、買咖啡、上廁所與寫日記
- 自動開始下一輪專注
- 以 SQLite 保存每日完成輪數與專注分鐘數
- 使用 Pillow 高倍繪製並縮小計時圓環，避免 Tkinter 圓弧鋸齒

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

測試涵蓋倒數狀態、完成事件、SQLite 持久化、DPI 尺寸換算、抗鋸齒圓環輸出、小遊戲目標重新定位、鯨豚題庫與休息提醒文案。

## 產生桌面執行檔

Windows 與 macOS 必須分別在各自的作業系統建置，PyInstaller 不能跨平台產生另一個系統的程式。

Windows：

```powershell
uv sync --group dev
uv run pyinstaller --noconfirm --windowed --manifest windows.manifest --name Pause25 --paths src src/pause25/__main__.py
```

macOS：

```bash
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

### Windows 介面仍然模糊

在 `Pause25.exe` 按右鍵開啟「內容」→「相容性」→「變更高 DPI 設定」，確認未勾選「覆寫高 DPI 縮放行為」。程式已內建 Per-Monitor V2 DPI 宣告，Windows 的手動相容性覆寫反而會讓介面再次被點陣放大。

## 操作驗收清單

1. 執行 `uv run pause25`，預期看到 `25:00` 與「開始專注」。
2. 按「開始專注」，預期時間開始倒數，狀態顯示「專注中」。
3. 按「暫停」再按「繼續專注」，預期倒數停住後從原時間繼續。
4. 等倒數完成，預期出現全螢幕置頂休息卡，內容為鯨豚選擇題、名言或小遊戲之一；上方顯示「休息倒數 05:00」及「休息一下：喝水裝水／買咖啡／上廁所／寫日記」。
   （若不按任何按鈕，5 分鐘倒數歸零後休息卡自動關閉，新的 25 分鐘自動開始。）
5. 按 `Esc`，預期提醒不會關閉；按「1 分鐘後再提醒」，預期視窗暫時離開並在 1 分鐘後再次出現。
6. 按「我休息好了，開始下一輪」，預期休息卡關閉且新的 25 分鐘自動開始。
7. 關閉並重開程式，預期「今天」的輪數與累積分鐘仍保留。
8. 將 Windows 顯示縮放設為 125% 或 150% 後開啟程式，預期文字與圓環清晰，視窗內容不會縮小或被裁切。

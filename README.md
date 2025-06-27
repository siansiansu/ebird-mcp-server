# eBird MCP Server

![demo](demo.gif)

這是一個結合 eBird API 與 Model Context Protocol (MCP) 的工具，讓使用者可以透過自然語言，直接在 Claude 的對話視窗中查詢鳥類觀測資料。

## 功能特色

本工具目前支援以下 eBird API 功能：

- **觀測資料 (Observations)**
  - 查詢特定地區的近期鳥類觀測紀錄。
  - 查詢特定地區、特定鳥種的近期觀測紀錄。
  - 查詢特定地區的近期稀有鳥種（Notable）觀測紀錄。
  - 查詢座標附近的鳥類觀測紀錄。
  - 查詢座標附近的稀有鳥種觀測紀錄。
  - 查詢座標附近、特定鳥種的觀測紀錄。
- **賞鳥紀錄 (Checklists)**
  - 查詢特定賞鳥紀錄（Checklist）的詳細內容。
- **熱點與物種 (Hotspots & Taxonomy)**
  - 查詢特定地區的賞鳥熱點（Hotspots）。
  - 查詢座標附近的賞鳥熱點。
  - 查詢 eBird 的官方鳥類分類名錄。
  - 查詢特定物種的所有可識別亞種（Taxonomy Forms）。

## 前置準備

在開始之前，請完成以下準備工作。

### 1. 取得 eBird API 金鑰

您必須擁有一個 eBird 帳號，並前往以下網址申請 API 金鑰：

[https://ebird.org/api/keygen](https://ebird.org/api/keygen)

申請完成後，請將您的金鑰複製下來，稍後會用到。

### 2. 安裝 Claude 桌面應用程式

本工具需要搭配 Claude 桌面應用程式使用。請至官網下載並安裝：

[https://claude.ai/download](https://claude.ai/download)

安裝完成後，登入您的 Claude 帳號。

## 安裝與執行 (macOS)

### 1. 設定 Python 環境

```bash
# 進入專案目錄
cd /path/to/ebird-mcp-server

# 安裝專案依賴套件
pip install -r requirements.txt
```

### 2. 設定 Claude 桌面應用程式

1.  打開 Claude 桌面應用程式。
2.  點擊左下角的頭像，選擇 **Settings**。
3.  找到 **MCP Servers** 區塊，點擊 **Edit settings.json**。
4.  將以下 JSON 內容貼入，並替換成您自己的設定：

```json
{
  "mcpServers": {
    "ebird-api": {
      "command": "/path/to/ebird-mcp-server/.venv/bin/python",
      "args": [
        "/path/to/Workspace/ebird-mcp-server/server.py"
      ],
      "env": {
        "EBIRD_API_KEY": "你的 eBird API 金鑰"
      }
    }
  }
}
```

**請務必修改以下路徑與金鑰**：
- `command`: `python` 執行檔絕對路徑。
- `args`: `server.py` 的絕對路徑。
- `EBIRD_API_KEY`: 您在第一步取得的 eBird API 金鑰。

### 3. 執行 MCP Server

設定完成後重新啟動 Claude 桌面版，Claude 會自動啟動並管理這個 MCP Server。您現在可以在任何對話中，透過 `@ebird-api` 來呼叫相關工具。

## 安裝與執行 (Windows)

### 1. 設定 Python 環境

1.  前往 [Python 官網](https://www.python.org/downloads/windows/) 下載並安裝 Python 3.10 或更新版本。**安裝時，請務必勾選 `Add Python to PATH` 選項。**
2.  打開 **命令提示字元 (Command Prompt)** 或 **PowerShell**。
3.  建立環境：

```bash
# 進入專案目錄
cd C:\path\to\ebird-mcp-server
```

4.  安裝專案依賴套件：

```bash
pip install -r requirements.txt
```

### 2. 設定 Claude 桌面版 App

1.  打開 Claude 桌面應用程式。
2.  點擊左下角的頭像，選擇 **Settings**。
3.  找到 **MCP Servers** 區塊，點擊 **Edit settings.json**。
4.  將以下 JSON 內容貼入並替換成您自己的設定：

```json
{
  "mcpServers": {
    "ebird-api": {
      "command": "C:/path/to/ebird-mcp-server/.venv/Scripts/python.exe",
      "args": [
        "C:/path/to/ebird-mcp-server/server.py"
      ],
      "env": {
        "EBIRD_API_KEY": "你的 eBird API 金鑰"
      }
    }
  }
}
```

**請務必修改以下路徑與金鑰**：
- `command`: 您虛擬環境中 `python.exe` 的絕對路徑。
- `args`: `server.py` 的絕對路徑。
- `EBIRD_API_KEY`: 您在第一步取得的 eBird API 金鑰。

### 3. 執行 MCP Server

設定完成後重新啟動 Claude 桌面版，Claude 會自動啟動並管理這個 MCP Server。您現在可以在任何對話中，透過 `@ebird-api` 來呼叫相關工具。

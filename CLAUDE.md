# HubforAA

各プロジェクトのサーバーをブラウザから起動・管理するポータルアプリ。

## 起動

```bash
uvicorn main:app --port 8010
```

ブラウザ: http://localhost:8010

## 機能

- 各プロジェクトの死活確認（`/api/check/{port}`）
- 各プロジェクトのサーバー起動（`/api/start/{name}`）
- ブラウザから各プロジェクトへのリンク

## 管理対象プロジェクト

| プロジェクト名 | フォルダ | ポート |
|---|---|---|
| aa-for-data-structures | `AAforDataStructures/` | 8006 |
| search-bar-animation | `SearchBarAnimation/` | 8004 |
| sort-animation-v3 | `AllSortAnimationByBar_JS_v3/` | 8003 |
| array-animation | `ArrayAnimation/` | 8005 |

※ `AllSortAnimationByBar_JS` (8000) / `AllSortAnimationByBar_JS_v2` (8002) はフリーズ済みのため除外。

## ファイル構成

```
main.py     # FastAPI サーバー（子プロセス管理 + 死活確認 API）
static/     # ポータル UI（HTML/JS）
```

## API

```
GET  /api/check/{port}   # ポートが開いているか確認 → {"online": bool}
POST /api/start/{name}   # 対象プロジェクトを subprocess で起動
```

## GitHub Pages

- URL: https://hirotakauoi.github.io/HubforAA/
- `gh-pages` ブランチの `index.html` を配信
- `static/index.html` を更新したら `gh-pages` ブランチにも反映すること:

```bash
cd HubforAA
git checkout gh-pages
git checkout main -- static/index.html
cp static/index.html index.html
git add index.html
git commit -m "gh-pages: update"
git push origin gh-pages
git checkout main
```

## 動作モード

`index.html` はアクセス元で自動切替:

| モード | 条件 | 動作 |
|---|---|---|
| ローカル | `localhost` / `127.0.0.1` | 死活確認 + 起動ボタン + Demo リンク |
| GitHub Pages | それ以外 | Render URL へのリンクのみ |

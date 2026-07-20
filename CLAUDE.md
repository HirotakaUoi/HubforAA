# HubforAA

各プロジェクトのサーバーをブラウザから起動・管理するポータルアプリ。

## 起動

```bash
uvicorn main:app --port 8010
```

ブラウザ: http://localhost:8010

### ダブルクリック起動（macOS）

プロジェクトルート直下の **`HubforAA.app`** をダブルクリックすると、
8010番が応答しない場合のみサーバーを起動（`.venv/bin/uvicorn`、最大15秒待機）し、
既定ブラウザで Hub ページを開く。起動済みならブラウザ表示のみ（二重起動しない）。

- 現在バージョン: **v1.3**（v1.0 初版 / v1.1 フォールバックをマシン別候補リスト化 /
  v1.2 .venv が別マシン製で壊れている場合を検知して uv 等へフォールバック /
  v1.3 ログを `~/Library/Logs/HubforAA/` へ移動）
- **注意**: `.venv` は Dropbox で同期されるが、中身は作成マシン専用の絶対パス
  （スクリプトの shebang・python シンボリックリンク）を含むため他マシンでは動かない。
  ランチャーは「python が実際に動くか」を確認してから .venv を使い、ダメなら
  `uv run` → システム python3 の順でフォールバックする（uvicorn スクリプトは
  シェバン問題を避けるため経由せず、常に `python -m uvicorn` で起動）
- **版数管理ルール**: .app を変更したら、スクリプト冒頭コメントの版数と
  `Info.plist` の `CFBundleVersion` / `CFBundleShortVersionString` を必ず上げ、
  `touch HubforAA.app` でバンドルの更新日時も合わせる
  （Finder は最上位フォルダの日時しか表示しないため）
- 実体はシェルスクリプト: `HubforAA.app/Contents/MacOS/HubforAA`
- 自分の位置からプロジェクトルートを逆算するため Dropbox 同期先の別マシンでも動作
  （移動された場合は標準パスにフォールバック）
- 起動ログ: `~/Library/Logs/HubforAA/hub_launcher.log`
  （v1.3 から。Dropbox 同期を避けるためプロジェクト外に出力）
- 別マシンで「開けない」場合は `chmod +x HubforAA.app/Contents/MacOS/HubforAA` を一度実行

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

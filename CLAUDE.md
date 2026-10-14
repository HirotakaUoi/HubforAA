# HubforAA

各プロジェクトのサーバーをブラウザから起動・管理するポータルアプリ。

## 起動

```bash
./run_server.sh HubforAA 8010    # プロジェクトルートから
```

ブラウザ: http://localhost:8010

### ダブルクリック起動（macOS）

プロジェクトルート直下の **`HubforAA.app`** をダブルクリックすると、
8010番が応答しない場合のみサーバーを起動（`run_server.sh` 経由、最大60秒待機）し、
既定ブラウザで Hub ページを開く。起動済みならブラウザ表示のみ（二重起動しない）。

- 現在バージョン: **v1.4**（v1.0 初版 / v1.1 フォールバックをマシン別候補リスト化 /
  v1.2 .venv が別マシン製で壊れている場合を検知して uv 等へフォールバック /
  v1.3 ログを `~/Library/Logs/HubforAA/` へ移動 /
  v1.4 起動を共通スクリプト `run_server.sh` に委譲）
- `.venv` の扱い（Dropbox 同期で全マシン共有）はルートの `CLAUDE.md`
  「.venv の共有方式」を参照
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

`/api/start` はルートの共通スクリプト `run_server.sh <プロジェクト> <ポート>` を
起動するだけ（.venv の確認・Python 本体の導入・relocatable での作り直しはスクリプト側）。
Hub 自身の python（`sys.executable`）は使わない。以前はそれを使っていたため、稼働中に
Hub の `.venv` が別マシン製に差し替わる（Dropbox 同期）と全プロジェクトが起動不能に
なっていた（2026-09-29 修正）。画面側は最大60秒待ち、起動しなければダイアログで通知する。

## GitHub Pages

- URL: https://algorithm-animation-hub.fishbone.jp/ （カスタムドメイン。gh-pages の `CNAME`。
  旧 URL https://hirotakauoi.github.io/HubforAA/ はここへ 301 転送される）
- `gh-pages` ブランチの `index.html` を配信（ほかに `CNAME` があるので消さないこと）
- `static/index.html` を更新したら `gh-pages` ブランチにも反映すること。
  このフォルダは Hub サーバーが使用中かつ Dropbox 同期中なので、`git checkout gh-pages` で
  作業ツリーを切り替えず、**別の場所に worktree を作って**反映する:

```bash
cd HubforAA
git fetch origin
W=$(mktemp -d)/gh-pages
git worktree add -B gh-pages "$W" origin/gh-pages
git show main:static/index.html > "$W/index.html"
git -C "$W" commit -am "gh-pages: main の static/index.html を反映"
git -C "$W" push origin gh-pages
git worktree remove "$W"
```

## 動作モード

`index.html` はアクセス元で自動切替:

| モード | 条件 | 動作 |
|---|---|---|
| ローカル | `localhost` / `127.0.0.1` | 死活確認 + 起動ボタン + Render リンク |
| GitHub Pages | それ以外 | Render URL へのリンクのみ |

# HubforAA

アルゴリズムアニメーション プロジェクト群のポータルサイトです。

**GitHub Pages（公開ページ）:** https://hirotakauoi.github.io/HubforAA/

---

## 概要

各プロジェクトへのリンク集として機能します。

- **GitHub Pages でアクセスした場合** — Render にデプロイされた各プロジェクトへのリンクを表示
- **ローカルで起動した場合（`localhost:8010`）** — ローカルサーバーの死活確認・起動ボタン・Render Demo リンクを表示

---

## 管理プロジェクト

| プロジェクト | 説明 | Render |
|---|---|---|
| [AAforDataStructures](https://github.com/HirotakaUoi/AAforDataStructures) | データ構造アニメーション（Ch.3〜11、22種） | https://aafordatastructures.onrender.com |
| [SearchBarAnimation](https://github.com/HirotakaUoi/SearchBarAnimation) | 棒グラフ形式の探索アニメーション | https://searchbaranimation.onrender.com |
| [AllSortAnimationByBar_JS_v3](https://github.com/HirotakaUoi/AllSortAnimationByBar_JS_v3) | ソートアニメーション v3（15種） | https://allsortanimationbybar-js-v3.onrender.com |
| [ArrayAnimation](https://github.com/HirotakaUoi/ArrayAnimation) | 探索・ソート・その他アルゴリズム（16種） | https://arrayanimation.onrender.com |

---

## ローカルでの起動

```bash
uv run uvicorn main:app --port 8010
```

ブラウザで http://localhost:8010 を開いてください。

> **前提:** 各プロジェクトが HubforAA と同じ親フォルダ内に配置されている必要があります。

---

## アーキテクチャ

```
[ブラウザ]
    │  localhost:8010（ローカル時）
    ▼
[FastAPI / main.py]  ── /api/check/{port}  → ポート疎通確認
    │                ── /api/start/{name}  → subprocess で子サーバー起動
    ▼
[static/index.html]  ── IS_LOCAL 判定で表示モードを切替
```

### API

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/api/check/{port}` | GET | 指定ポートが開いているか確認 → `{"online": bool}` |
| `/api/start/{name}` | POST | 指定プロジェクトのサーバーを起動 |

---

## gh-pages の更新

`static/index.html` を変更した際は `gh-pages` ブランチにも反映してください。

```bash
git checkout gh-pages
git checkout main -- static/index.html
cp static/index.html index.html
git add index.html
git commit -m "gh-pages: update"
git push origin gh-pages
git checkout main
```

---

## ファイル構成

```
HubforAA/
├── main.py          # FastAPI サーバー（死活確認 API + 子プロセス管理）
├── static/
│   └── index.html   # ポータル UI（ローカル / GitHub Pages ハイブリッド）
├── pyproject.toml
└── README.md
```

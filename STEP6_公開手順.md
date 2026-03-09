# STEP 6：Vercel公開 + ドメイン設定 手順書

---

## 完成ファイル一覧（公開前確認）

```
knife-db/
├── index.html          ← トップページ（フィルター付き）
├── about.html          ← Aboutページ（AdSense審査必須）
├── privacy.html        ← プライバシーポリシー（AdSense審査必須）
├── sitemap.xml         ← 検索エンジン用サイトマップ
├── data.json           ← データ30件
├── generate_pages.py   ← ページ生成スクリプト
└── items/              ← 個別ページ30件
    ├── yu-kurosaki.html
    └── ...（30ファイル）
```

---

## PHASE 1：GitHubにアップロード（10分）

### ① GitHubアカウント作成
→ https://github.com にアクセスしてアカウント作成（無料）

### ② 新しいリポジトリを作成
1. GitHubにログイン後、右上「+」→「New repository」
2. Repository name: `japan-knife-makers`（任意）
3. Public を選択
4. 「Create repository」をクリック

### ③ ファイルをアップロード
**方法A（簡単）：ブラウザからドラッグ＆ドロップ**
1. 作成したリポジトリページで「uploading an existing file」をクリック
2. `knife-db` フォルダの中身を**すべて選択**してドラッグ＆ドロップ
3. ※ `items/` フォルダは中のファイルをまとめてドラッグでOK
4. 「Commit changes」をクリック

**方法B（Git CLIが使える場合）：**
```bash
cd knife-db
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/[ユーザー名]/japan-knife-makers.git
git push -u origin main
```

---

## PHASE 2：Vercelにデプロイ（5分）

1. https://vercel.com にアクセス
2. 「Sign Up」→「Continue with GitHub」でGitHubと連携
3. 「Add New Project」→「Import Git Repository」
4. `japan-knife-makers` を選択
5. 設定はすべてデフォルトのまま「Deploy」をクリック
6. 数分で `https://japan-knife-makers-xxxx.vercel.app` に公開完了

**確認ポイント：**
- [ ] トップページが表示されるか
- [ ] フィルターが動作するか
- [ ] `items/yu-kurosaki.html` が開けるか
- [ ] `about.html` `privacy.html` が開けるか

---

## PHASE 3：独自ドメイン取得＆紐付け（30分）

### ① ドメインを取得する（おすすめ：お名前.com / Xserverドメイン）

**おすすめドメイン候補（先着順で取得）：**
```
japan-knife-makers.com   ← 最優先で確認
japanknifedatabase.com
knife-japan.com
japanese-blacksmiths.com
```

**取得先：**
- お名前.com：https://www.onamae.com/
- Xserverドメイン：https://www.xdomain.ne.jp/
- .com で年間1,000〜1,500円が目安

### ② VercelにカスタムドメインをAdd（無料）

1. Vercelダッシュボード → プロジェクト選択
2. 「Settings」→「Domains」
3. 取得したドメインを入力 → 「Add」
4. 表示されたDNSレコードをドメイン管理画面に設定

**DNSレコードの設定例（お名前.comの場合）：**
```
タイプ: A
名前: @
値:  76.76.21.21（Vercelが指定する値）

タイプ: CNAME
名前: www
値:  cname.vercel-dns.com
```

5. 設定後10〜30分でドメインが反映される

---

## PHASE 4：サイトマップのURL更新（5分）

`sitemap.xml` の `YOUR-DOMAIN.com` を実際のドメインに書き換える。

```xml
<!-- 変更前 -->
<loc>https://YOUR-DOMAIN.com/index.html</loc>

<!-- 変更後（例） -->
<loc>https://japan-knife-makers.com/index.html</loc>
```

変更後、GitHubにpush → Vercelが自動で再デプロイする。

---

## PHASE 5：Google Search Console登録（15分）

1. https://search.google.com/search-console にアクセス
2. 「プロパティを追加」→ ドメインを入力
3. 所有権確認：
   - **HTMLファイル方式**：Googleが提供するHTMLファイルを knife-db/ に追加してGitHub push
   - または **メタタグ方式**：`index.html` の `<head>` 内にメタタグを追加
4. 確認完了後、「サイトマップ」→ `sitemap.xml` のURLを送信

```
送信するURL例：
https://japan-knife-makers.com/sitemap.xml
```

---

## PHASE 6：Google Analytics設定（15分）

1. https://analytics.google.com にアクセス
2. アカウント・プロパティを作成
3. 「Webストリーム」でサイトURLを入力
4. トラッキングコード（GTM-xxxxx）を取得
5. `index.html` の `<head>` 直後に貼り付け

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## PHASE 7：AdSense申請（コンテンツ充実後）

**申請タイミング：公開から2〜4週間後（コンテンツ充実後）**

### 申請前チェックリスト
- [ ] 独自ドメインで公開されている
- [ ] `about.html` がある
- [ ] `privacy.html` がある
- [ ] 各個別ページの本文が300語以上（★現状は要追加）
- [ ] Google Search Consoleで20ページ以上インデックス済み
- [ ] サイトが正常に表示される（エラーページなし）

### 申請手順
1. https://www.google.com/adsense にアクセス
2. サイトURLを入力して申請
3. 審査コード（HTMLタグ）を `index.html` の `<head>` に追加
4. 数日〜2週間で審査結果が届く

---

## 優先タスク一覧（公開後）

| 優先度 | タスク | 目安時間 |
|--------|--------|---------|
| 🔴 高 | 各個別ページの本文を300語以上に拡充（AIで一括生成） | 1〜2時間 |
| 🔴 高 | Google Search Console登録・サイトマップ送信 | 15分 |
| 🟡 中 | Google Analytics設定 | 15分 |
| 🟡 中 | data.jsonを80件以上に拡充 | 1〜2時間 |
| 🟢 低 | AdSense申請（1ヶ月後目安） | 15分 |
| 🟢 低 | 多言語版（スペイン語）の準備 | 将来 |

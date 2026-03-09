# STEP 3：データベース設計書 & AI収集プロンプト集
## 包丁鍛冶・産地データベース（英語サイト向け）

---

## 1. カラム設計（最終版）

| カラム名（JSON key） | 型 | 説明 | 例 |
|-------------------|----|------|-----|
| id | number | 連番ID | 1 |
| nameJa | string | 鍛冶場・ブランド名（日本語） | "黒崎 優" |
| nameEn | string | 英語名・ローマ字名 | "Yu Kurosaki" |
| type | string | "individual"（職人個人）or "brand"（ブランド） | "individual" |
| forge | string | 鍛冶場・工房名 | "Kurosaki Hamono" |
| region | string | 産地名（英語） | "Echizen" |
| prefecture | string | 都道府県（英語） | "Fukui" |
| city | string | 市区町村（英語） | "Echizen City" |
| masterSmith | string or null | 主要な鍛冶師名 | "Yu Kurosaki" |
| foundedYear | number or null | 創業年 | 1952 |
| specialtyTypes | array | 得意な刃の種類 | ["Gyuto", "Yanagiba"] |
| steelTypes | array | 使用鋼材 | ["Aogami Super", "R2/SG2"] |
| handleStyle | string | "Wa"/"Western"/"Both" | "Both" |
| priceRange | string | "budget"/<$100 / "mid"/$100-300 / "high"/$300-600 / "premium">$600 | "mid" |
| priceMin | number | 最低価格（USD） | 150 |
| priceMax | number | 最高価格（USD） | 500 |
| canVisit | boolean | 工房・店舗訪問可否 | true |
| workshopExperience | boolean | 鍛冶体験・研ぎ体験提供 | false |
| rating | number | 1〜5の総合評価 | 5 |
| description | string | 英語説明文（100〜150文字） | "Youngest blacksmith to receive..." |
| url | string | 公式サイトURL | "https://..." |
| tags | array | 検索・フィルター用タグ | ["sakai", "blue-steel"] |

---

## 2. 産地・リージョンの標準表記

データ収集時に以下の統一名を使うこと。

| 産地 | region（JSON値） | prefecture | 主な特徴 |
|------|----------------|------------|---------|
| 堺 | Sakai | Osaka | 分業制・単刃・本職向け。90%の本職包丁シェア |
| 越前（武生・今立） | Echizen | Fukui | 武生刃物産地。竹刃物村（Takefu Knife Village）の本拠地 |
| 関 | Seki | Gifu | 日本最大の刃物産地。世界三大刃物産地の一つ |
| 土佐 | Tosa | Kochi | 野鍛冶の伝統。自由鍛造。機能優先の実質的な包丁 |
| 燕三条 | Sanjo | Niigata | 越後三条打刃物。伝統的工芸品指定 |
| 三木 | Miki | Hyogo | 播州刃物。ガーデンツールと包丁の複合産地 |
| 安来 | Yasugi | Shimane | 安来鋼（ヤスキハガネ）の産地。鋼材の供給元 |

---

## 3. タグ一覧（標準化）

以下のタグから適切なものを選んで付与する。

**産地タグ：**
`sakai` / `echizen` / `seki` / `tosa` / `sanjo` / `miki` / `takefu-village`

**鋼材タグ：**
`blue-steel` / `white-steel` / `aogami-super` / `aogami-1` / `aogami-2` / `shirogami-1` / `shirogami-2` / `vg-10` / `r2-sg2` / `hap40` / `ginsan` / `stainless` / `damascus` / `carbon-steel` / `iron-clad` / `copper-clad`

**刃種タグ：**
`gyuto` / `yanagiba` / `deba` / `santoku` / `nakiri` / `petty` / `sujihiki` / `kiritsuke` / `bunka` / `usuba` / `single-bevel`

**特徴タグ：**
`laser-grind` / `thin-blade` / `high-end` / `budget` / `beginner-friendly` / `professional` / `collector` / `handmade` / `master-blacksmith` / `award-winning` / `traditional` / `modern-style` / `shop-visit` / `experience` / `waitlist` / `cult-favorite` / `best-value` / `heritage` / `next-generation` / `premium` / `ultra-rare` / `widely-available`

**ハンドルタグ（任意）：**
`wa-handle` / `western-handle`

**人気地域タグ（任意）：**
`usa-popular` / `english-site` / `worldwide-shipping`

---

## 4. 価格帯の基準（USD）

| priceRange値 | 目安（USD）| 対象ユーザー |
|-------------|-----------|------------|
| budget | $20〜$100 | 入門者 |
| mid | $100〜$300 | 料理好き・セミプロ |
| high | $300〜$600 | プロ・コレクター |
| premium | $600以上 | 本職・コレクター最上位 |

---

## 5. AI収集プロンプト集

### プロンプト①：産地別に追加収集する（基本）

```
あなたは日本の包丁産地と鍛冶師に詳しい専門家です。

以下の条件で[産地名]の包丁鍛冶場・ブランドのデータを収集してください。

【条件】
- ハルシネーション禁止。実在する鍛冶場・ブランドのみ掲載する
- データが不確かな場合はそのフィールドをnullにする
- 英語圏のユーザーが読む想定で description は英語で書く
- 以下のJSONフォーマットで出力する

【フォーマット】
{
  "id": [連番],
  "nameJa": "[日本語名]",
  "nameEn": "[英語名・ローマ字]",
  "type": "brand" または "individual",
  "forge": "[工房名]",
  "region": "[産地：Sakai/Echizen/Seki/Tosa/Sanjo/Mikilのいずれか]",
  "prefecture": "[都道府県・英語]",
  "city": "[市区町村・英語]",
  "masterSmith": "[主要鍛冶師名 or null]",
  "foundedYear": [創業年 or null],
  "specialtyTypes": ["Gyuto", "Yanagiba"等],
  "steelTypes": ["Aogami #2"等],
  "handleStyle": "Wa" または "Western" または "Both",
  "priceRange": "budget" または "mid" または "high" または "premium",
  "priceMin": [USD最低価格],
  "priceMax": [USD最高価格],
  "canVisit": true または false,
  "workshopExperience": true または false,
  "rating": [1〜5],
  "description": "[英語説明 100〜150文字]",
  "url": "[公式URL or 空文字]",
  "tags": ["タグ1", "タグ2" ...]
}

【対象産地】[ここに産地名を入れる：例 Sakai / Echizen / Seki / Tosa]
【目標件数】20件
```

---

### プロンプト②：既存データの空白を埋める

```
以下のJSONデータについて、不足・不正確なフィールドを補完してください。

【作業内容】
1. url が空文字のものを優先的に公式サイトを調べて補完する
2. foundedYear が null のものを可能な範囲で補完する
3. description が不自然な英語の場合は修正する
4. tags に抜けがあれば追加する（標準タグリストに従う）
5. 変更した箇所のみ "updated_fields" に列記する

【注意】
- 確認できない情報は変更しない（null のまま）
- ハルシネーション禁止

[JSONデータをここに貼り付け]
```

---

### プロンプト③：ハルシネーションチェック（Perplexity向け）

```
以下の包丁鍛冶場・ブランド情報について、事実確認をしてください。

確認項目：
1. 実在するか（名前・産地・創業年）
2. 説明文に明らかな誤りがないか
3. 公式サイトURLが正しく機能しているか

チェック対象：
[名前・産地・説明文・URLを貼り付け]

判定：
- ○：正確
- △：一部修正が必要（修正内容を明記）
- ×：実在しない・大きな誤り（削除推奨）
```

---

### プロンプト④：英語説明文の品質チェック

```
以下の英語説明文をネイティブスピーカーが読んで自然かチェックしてください。

条件：
- 100〜150文字に収める
- 商品説明ではなくブランド・職人の「紹介文」として自然な文体
- 専門用語（Gyuto, Aogami等）はそのまま使用してOK
- 不自然な場合は修正版を提案する

[説明文リストを貼り付け]
```

---

### プロンプト⑤：新規タグの提案

```
以下の包丁鍛冶場データを分析して、
サイトのフィルター機能を改善するための新しいタグカテゴリを提案してください。

現在のタグカテゴリ：産地 / 鋼材 / 刃種 / 特徴 / ハンドル

提案してほしいこと：
- 現在のタグでは表現できない重要な特徴はあるか？
- 外国人ユーザーが特に使いそうな絞り込み条件は何か？
- 追加すると検索性が上がるタグを10個提案してほしい

[data.jsonの内容を貼り付け]
```

---

## 6. データ収集ロードマップ

| フェーズ | 目標件数 | 産地 | 優先度 |
|---------|---------|------|--------|
| Phase 1（現在） | 30件 ✅ | 堺・越前・関・土佐・三条・三木 | 完了 |
| Phase 2 | 80件 | 堺を20件→50件に拡充 + 越前を追加 | 最優先 |
| Phase 3 | 130件 | 土佐・三条を拡充 + 安来・その他追加 | 高 |
| Phase 4 | 200件 | 廃業した伝説的鍛冶師・希少品も収録 | 中 |
| Phase 5 | 300件+ | マイナー産地・職人体験施設を網羅 | 低 |

---

## 7. データ品質チェックリスト

収集後に以下を確認する（全件確認は不要・20件に1件程度を抜き打ち）

- [ ] 名前のスペルが正しいか（英語・日本語両方）
- [ ] 産地・都道府県が合っているか
- [ ] 価格帯が実態と乖離していないか（Amazon/公式サイトで確認）
- [ ] URLが実際に開くか
- [ ] description が英語として自然か
- [ ] 閉業・廃業した鍛冶場が「現役」として掲載されていないか

---

## 8. 現在のデータ統計（Phase 1完了時点）

| 産地 | 件数 |
|------|------|
| Echizen（越前） | 9件 |
| Sakai（堺） | 8件 |
| Seki（関） | 4件 |
| Tosa（土佐） | 4件 |
| Sanjo（三条） | 3件 |
| Miki（三木） | 1件 |
| Seki（ミソノ） | 1件 |
| **合計** | **30件** |

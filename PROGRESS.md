# KEIJI Progress Log

## 2026-05-13 — AI生徒会長モード連続実行

### 完了したバックログ

1. P4商品同定エンジンの実装計画を `docs/P4_product_identity_engine_spec.md` に反映済み。
2. P4用フォルダ構成は `src/keiji/p4_identity/` 配下で維持し、属性抽出とスコア集約モジュールを追加。
3. P4用設定読み込みは既存の `load_rule_config` と `config/product_identity_rules.v1.yaml` を継続利用。
4. 商品名の正規化処理は既存 `normalizer.py` を利用。
5. JAN/ASIN/型番/容量/色/セット数/状態の抽出処理を `attribute_extractor.py` に追加。
6. 商品一致スコアリング処理を `scorer.py` に追加し、設定ファイルの重みを利用可能にした。
7. ハード拒否条件は既存のキーワード・購入上限・状態ポリシーに加え、タイトル由来の中古/開封/ジャンク状態を優先して判定するよう強化。
8. P4ユニットテストを追加し、属性抽出・セット数・設定重み・タイトル由来JAN・タイトル由来中古ブロックを検証。
9. P3利益計算エンジンの実装計画を `docs/P3_profit_engine_spec.md` に反映済み。
10. P3用設定読み込みは既存の `load_rule_config` と `config/profit_rules.v1.yaml` を継続利用。
11. 原価・送料・手数料・予備費の計算処理を `costs.py` に分離して監査しやすくした。
12. ROI・純利益・損益分岐点計算は `roi_calculator.py` で `CostBreakdown` を使うよう整理。
13. 購入可否判定処理は既存 `decision.py` / `capital_guard.py` を維持。
14. P3ユニットテストを追加し、予備費込みの総費用と損益分岐点を検証。
15. P3/P4統合フローの最小実装は既存 `offline_runner.py` で維持。
16. README/docs 更新として、P4/P3仕様書を実装状態に合わせて更新。
17. 進捗・残課題・次タスクを本ファイルに記録。

### 変更した主なファイル

- `src/keiji/p4_identity/attribute_extractor.py`
- `src/keiji/p4_identity/scorer.py`
- `src/keiji/p4_identity/engine.py`
- `src/keiji/p4_identity/decision.py`
- `src/keiji/p4_identity/variant_matcher.py`
- `src/keiji/p3_profit/costs.py`
- `src/keiji/p3_profit/roi_calculator.py`
- `tests/unit/p4_identity/test_attribute_extractor_and_scoring.py`
- `tests/unit/p3_profit/test_cost_breakdown.py`
- `docs/P4_product_identity_engine_spec.md`
- `docs/P3_profit_engine_spec.md`

### 残課題

- P4属性抽出は保守的な正規表現ベースのため、型番抽出の精度向上には追加フィクスチャが必要。
- P4ブランド比較は正規化で扱っているが、独立した `brand_matcher.py` はまだ作っていない。
- P3のリスク調整は簡易ペナルティのままなので、販売価格不確実性・返品リスク・競合リスクを個別理由として扱う余地がある。
- 外部API・ブラウザ自動化・購入/決済実行は初期MVPでは未実装のまま維持する。

### 次タスク

1. 手元CSV/JSONフィクスチャを増やし、型番・容量・色・セット数の誤検知ケースを追加する。
2. P4に独立したブランド照合モジュールを追加し、互換品/非純正/ブランド名の含まれ方をより明示的に監査する。
3. P3のリスク調整を設定ファイル化し、理由コードと人間向け説明を拡充する。
4. 監査エクスポートにP4抽出属性とP3コスト内訳を含める。

### 次回Codexへの継続プロンプト

AGENTS.md と docs/PRD.md を前提に、外部API・ブラウザ自動化・購入/決済実行を行わず、ローカルフィクスチャだけで作業してください。次は P4 のブランド照合モジュール追加、属性抽出フィクスチャ拡充、P3 リスク調整の設定ファイル化、監査出力への抽出属性/コスト内訳追加を、テストとdocs更新込みで連続実行してください。

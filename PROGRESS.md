# KEIJI Progress

## 2026-05-13 AI 生徒会長モード継続作業

### 前提・安全確認

- `AGENTS.md` と `docs/PRD.md` の安全境界を前提に、初期 MVP はローカル・オフライン・人間承認必須として継続。
- 購入、決済、ログイン、カート投入、チェックアウト、ブラウザ自動化、外部 API 呼び出しは未実装のまま維持。
- 既存ドキュメント/設定から非 KEIJI プロジェクト固有名の混入を除去し、境界表現を汎用化。

### バックログ進捗

| # | タスク | 状態 | メモ |
|---:|---|---|---|
| 1 | P4商品同定エンジンの実装計画を確定 | 完了 | `docs/P4_product_identity_engine_spec.md` を現行モジュール構成に合わせて更新。 |
| 2 | P4用のフォルダ構成を作成 | 完了 | `src/keiji/p4_identity/` 配下で分割済み。今回 `attribute_extractor.py`, `brand_matcher.py`, `exclusion_rules.py`, `scoring.py` を追加。 |
| 3 | P4用の設定読み込み処理を作成 | 完了 | `keiji.common.config_loader` と `config/product_identity_rules.v1.yaml` を使用。 |
| 4 | 商品名の正規化処理を作成 | 完了 | Unicode/大小文字/記号/ブランド alias 正規化を維持。 |
| 5 | JAN/型番/容量/色/セット数/状態の抽出処理を作成 | 完了 | `attribute_extractor.py` でローカル正規表現抽出を追加し、不足 JAN/ASIN/型番を P4 正規化へ補完。 |
| 6 | 商品一致スコアリング処理を作成 | 完了 | `scoring.py` で設定済み重みによるスコア合成を追加。 |
| 7 | ハード拒否条件の判定処理を作成 | 完了 | `exclusion_rules.py` へブロックキーワード/5,000 JPY SKU 上限を分離。 |
| 8 | P4のユニットテストを作成 | 完了 | 属性抽出、ブランド衝突、設定重みスコアリング、抽出 ID による同定を追加。 |
| 9 | P3利益計算エンジンの実装計画を確定 | 完了 | `docs/P3_profit_engine_spec.md` を現行 MVP 実装と将来拡張の境界に合わせて更新。 |
| 10 | P3用の設定読み込み処理を作成 | 完了 | `config/profit_rules.v1.yaml` と共通 config loader を使用。 |
| 11 | 原価・送料・手数料・予備費の計算処理を作成 | 完了 | 購入価格、入力送料、Amazon 手数料、fulfillment/storage/other buffer を計算。 |
| 12 | ROI・純利益・損益分岐点の計算処理を作成 | 完了 | `roi_calculator.py` に実装済み。 |
| 13 | 購入可否判定処理を作成 | 完了 | P3 decision/capital guard で pass/review/fail/blocked/skipped を判定。 |
| 14 | P3のユニットテストを作成 | 完了 | 既存 P3 fixture/threshold tests が継続パス。 |
| 15 | P3/P4統合フローの最小実装を作成 | 完了 | offline runner と P4->P3 gate を維持。 |
| 16 | READMEまたはdocsに実装内容を追記 | 完了 | P4/P3 specs と境界 docs を更新。 |
| 17 | PROGRESS.mdに進捗・残課題・次タスクを記録 | 完了 | 本ファイル。 |

### 今回の主な変更ファイル

- `src/keiji/p4_identity/attribute_extractor.py`
- `src/keiji/p4_identity/brand_matcher.py`
- `src/keiji/p4_identity/exclusion_rules.py`
- `src/keiji/p4_identity/scoring.py`
- `src/keiji/p4_identity/normalizer.py`
- `src/keiji/p4_identity/variant_matcher.py`
- `src/keiji/p4_identity/engine.py`
- `src/keiji/p4_identity/decision.py`
- `tests/unit/p4_identity/test_attribute_extractor_and_scoring.py`
- `docs/P4_product_identity_engine_spec.md`
- `docs/P3_profit_engine_spec.md`
- `docs/PRD.md`
- `docs/operations_manual.md`
- `docs/decisions/ADR-0001-project-boundary.md`
- `docs/test_plan.md`
- `docs/progress/2026-05-12-overnight-log.md`
- `config/risk_policy.v1.yaml`
- `PROGRESS.md`

### 残課題

- P4 属性抽出は安全側の最小正規表現。より多いカテゴリ/型番形式に広げる場合は、ローカル fixture を追加してから段階的に対応する。
- P3 の shipping/risk adjustment は現行 MVP では `fee_estimator.py` と `engine.py` 内の単純ロジック。カテゴリ別配送・返品・価格変動リスクを拡張する場合は専用 module 化する。
- 外部 API adapter は明示承認と認証情報が必要になるまで実装を進めない。
- 購入/決済/出品の実行は引き続き人間判断が必要で、MVP 内では実装しない。

### 次回 Codex 継続プロンプト

```text
AGENTS.md と PROGRESS.md を読み、KEIJI の安全境界を維持してください。購入・決済・ログイン・ブラウザ自動化・外部 API 呼び出しは実装しないでください。次はローカル fixture を追加しながら、P4 attribute_extractor の型番/容量/セット数抽出パターンを拡充し、P3 の risk_adjuster / shipping_estimator をローカル設定ベースの専用モジュールとして切り出してください。変更ごとに deterministic unit tests を追加し、最後に unittest/pytest を実行して結果を報告してください。
```

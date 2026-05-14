# KEIJI STATUS

## 1. 今回の作業概要

- PR #4 を本命候補として扱う前提で、リポジトリ直下に `STATUS.md` と `TASK_BOARD.md` を明示的に配置した。
- `STATUS.md` には、PR #4 が PR #1〜#3 を包含している確認結果、変更ファイル要約、テスト結果、未完了タスク、ブロッカー、人間判断事項、次回 Codex 指示を記録した。
- `TASK_BOARD.md` には、Codex A〜D の担当領域、触ってよいファイル範囲、完了状況、次にやるべき作業を記録した。
- main への merge は行っていない。
- 外部 API、購入、決済、出品、ブラウザ自動化、ログイン処理は実行も実装もしていない。

## 2. PR #4 が PR #1〜#3 を包含している確認結果

結論: **PR #4 は PR #1〜#3 を包含しているため、PR #1〜#3 は重複候補としてマージ不要。**

| PR | 包含確認 | PR #4/current branch に含まれる内容 | 判断 |
|---|---|---|---|
| PR #1 | OK | offline-first KEIJI MVP、P4 商品同定、P3 利益計算、設定、docs、fixtures、unit/integration tests | 重複のためマージ不要 |
| PR #2 | OK | local smoke workflow、audit export、review/status report、CLI、integration tests | 重複のためマージ不要 |
| PR #3 | OK | P4 attribute extraction、brand matcher、hard exclusion rules、scoring split、PROGRESS tracking | 重複のためマージ不要 |

確認に使った代表ファイル:

- P4: `src/keiji/p4_identity/*`, `config/product_identity_rules.v1.yaml`, `tests/unit/p4_identity/*`, `tests/fixtures/p4/*`
- P3: `src/keiji/p3_profit/*`, `config/profit_rules.v1.yaml`, `tests/unit/p3_profit/*`, `tests/fixtures/p3/*`
- P4/P3 integration: `src/keiji/pipeline/*`, `tests/unit/pipeline/*`, `tests/integration/*`
- Persistence/audit/review: `src/keiji/db/*`, `src/keiji/io/*`, `scripts/export_*`, `scripts/review_candidate.py`
- Smoke/CI/docs: `scripts/local_smoke.py`, `.github/workflows/tests.yml`, `README.md`, `PROGRESS.md`, `STATUS.md`, `TASK_BOARD.md`

## 3. 変更ファイルの要約

今回の明示更新対象:

- `STATUS.md`
  - PR #4 の本命扱い、PR #1〜#3 の包含確認、テスト結果、未完了タスク、ブロッカー、人間判断事項、次回 Codex 指示を記録。
- `TASK_BOARD.md`
  - Codex A〜D の担当、触ってよいファイル範囲、完了状況、次タスクを整理。

既に PR #4 に含まれている主要カテゴリ:

- `.github/workflows/tests.yml`: GitHub Actions 用 offline test workflow。
- `src/keiji/p4_identity/*`: P4 商品同定エンジン。
- `src/keiji/p3_profit/*`: P3 利益計算エンジン。
- `src/keiji/pipeline/*`: P4 → P3 integration / offline runner。
- `src/keiji/db/*`: SQLite schema / repositories。
- `src/keiji/io/*`: local input/export/report helpers。
- `scripts/*.py`: local CLI utilities。
- `config/*.yaml`: versioned local rules。
- `tests/*`: deterministic local tests and fixtures。
- `docs/*`, `README.md`, `PROGRESS.md`: specs, operation docs, progress records。

## 4. テスト実行結果

Latest local verification after updating `STATUS.md` and `TASK_BOARD.md`:

- PASS: `python -m pytest -q` — `42 passed, 8 subtests passed in 1.00s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 42 tests in 0.869s`, `OK`。
- Previous local smoke verification recorded in this branch:
  - PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-check` — `smoke_ok=true`。

テストは local fixtures と local SQLite を使う deterministic test であり、外部 API や browser automation は不要。

## 5. 未完了タスク

- P4 attribute extraction の fixture 拡充。
  - category-specific model number。
  - capacity / size 表記ゆれ。
  - set count / pack count 表記ゆれ。
  - edition / domestic-or-import edge cases。
- P3 の shipping estimator を、現行の単純な入力送料 + configured fulfillment cost から専用 module に切り出す。
- P3 の risk adjuster を、現行の reason-count penalty から local config driven module に切り出す。
- Review packet / operation report を非エンジニア向けにさらに読みやすくする。
- External API adapter は明示承認があるまで fake/local adapter の範囲に留める。

## 6. ブロッカー

現時点の local development / test execution についてのブロッカーはなし。

以下は意図的に停止・保留する事項:

- API key / credentials が必要な作業。
- 外部サービス接続が必要な作業。
- 購入、決済、出品、checkout、login、cart 操作。
- main への merge。
- Browser automation / scraping。

## 7. 人間判断が必要な事項

- PR #4 を最終的に merge するかどうか。
- PR #1〜#3 を close するか、コメントで「PR #4 に包含済み」と明記するか。
- External API adapter をいつ、どの API に限定して有効化するか。
- 初期 MVP の実運用開始前に、購入予算 50,000 JPY / SKU 上限 5,000 JPY を変更するか。
- P4 ambiguous / P3 review candidates の human approval ルールを運用上どこまで厳格にするか。

## 8. 次に Codex へ渡すべき指示

```text
AGENTS.md、STATUS.md、TASK_BOARD.md、docs/PRD.md を読んで、KEIJI の offline-first / human-approval-first 方針を維持してください。main へ merge せず、購入・決済・出品・ログイン・cart・checkout・browser automation・live external API を実装しないでください。次は TASK_BOARD.md の担当範囲に従い、まず Codex C と Codex A の連携として P4 attribute extraction の local fixtures を追加し、fixture で失敗する edge case だけを実装で補ってください。その後、Codex B として P3 shipping_estimator / risk_adjuster の専用 module 化を local config と deterministic tests 付きで進めてください。最後に python -m pytest -q と PYTHONPATH=src python -m unittest discover -s tests -v を実行し、結果を STATUS.md に追記してください。
```

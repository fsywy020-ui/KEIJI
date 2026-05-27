# KEIJI STATUS

## Yahoo!デベロッパー登録ページ公開 — 2026-05-27

- Goal: Yahoo!ショッピングAPI検証に向け、Yahoo!デベロッパー登録で使えるサイトURL、プライバシーポリシーURL、利用規約URLを作成・公開する。
- Scope: `docs/yahoo-developer-registration/` にトップページ、プライバシーポリシー、利用規約、登録入力値案、公式情報確認メモを追加。
- Constraints: 購入、決済、出品、login、cart、checkout、browser automation、scraping、live external API、外部通知送信は実行しない。APIキー、Client Secret、トークン、認証コードは記載しない。
- Done: Yahoo!公式情報を再確認し、登録用ページ一式のローカル下書きを作成。Yahoo! APIクレジット表示はトップページ下部に配置候補を追加。
- Update: 運営者名 `輝煌堂`、連絡先 `restartllc88@gmail.com` をローカル下書きへ反映。
- Record: `docs/goals/api-adapter-research/notes/yahoo_public_page_prep_2026-05-26.md` に、作成物、公式確認、未実行の安全境界、次の判断事項を記録。
- Publish: MitaさんのOKを受け、GitHub Pagesを `main` / `docs` で有効化。以下のURLがHTTP 200で表示されることを確認。
  - Site: `https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/`
  - Privacy: `https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/privacy.html`
  - Terms: `https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/terms.html`
- Source check:
  - Yahoo! ID連携 v2「Client IDを登録する」
  - Yahoo!デベロッパーネットワーク「クレジット表示」
  - Yahoo!デベロッパーネットワーク「ガイドライン」
  - Yahoo!ショッピングAPI「各種申請に関するヘルプ」
- Blocked / Human Approval: Yahoo!デベロッパー登録フォーム送信、Client ID / Secret の保存、API接続実装は引き続きMitaさん確認後に行う。

## Codex Review Assist 移行 — 2026-05-17

- Goal: 旧外部操作AI前提のP8 handoff設計を、Codex中心のlocal review assist設計へ移行する。
- Scope: P8 handoff実装を `review_handoff` へリネームし、生成物、docs、tests、owner smoke出力、計画ExcelをCodex Review Assist表記へ更新する。
- Excel: `C:\Users\KEIJI MITA\OneDrive\デスクトップ\ai_resale_project_master_plan_2026-05-17_codex_updated.xlsx` を作成。元Excelは上書きしない。
- Constraints: 購入、決済、出品、login、cart、checkout、browser automation、scraping、external agent API、live external API、外部通知送信は実装・実行しない。CodexもKEIJIも外部購入側操作は行わない。
- Done: コード/docs/tests/Excel更新、local smoke、unittest、旧表記スキャン、差分チェック、PR #15作成、GitHub checks成功、mainマージまで完了。
- Test results:
  - PASS: `python scripts/owner_smoke.py --out-dir storage/smoke` — `smoke_ok=true out_dir=storage\smoke processed=1`。
  - PASS: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` — `Ran 69 tests in 9.596s`, `OK`。
  - PASS: 旧外部操作AI関連表記スキャン — repo対象ファイルとExcel複製の残存0件。
  - PASS: `git diff --check`。
  - PASS: GitHub Actions `KEIJI Local Tests` — Python 3.11 / 3.12 offline test suite SUCCESS（PR #15）。
- PR: https://github.com/fsywy020-ui/KEIJI/pull/15
- Merge commit: `bdd8fe402603393ea58d2d7ddcfd7e510b42c805`
- Blocked / Human Approval: 実購入、外部API、ブラウザ実操作、出品・決済関連は引き続き個別承認が必要。

## API連携なし owner向け安全実装 — 2026-05-17

- Goal: 非エンジニアownerがWindows/PowerShellでも迷わずlocal smokeを実行し、生成Markdownを安全な順番で確認できるようにする。
- Scope: `scripts/owner_smoke.py` を追加し、`PYTHONPATH=src` を手作業で設定しなくても `local_smoke` を実行できる入口を作る。あわせて `storage/smoke/owner_review_index.md` を生成し、読む順番、禁止事項、`BUY_CANDIDATE` が購入許可ではないことを1枚で確認できるようにする。
- Constraints: 購入、決済、出品、login、cart、checkout、browser automation、scraping、external agent API、live external API、外部通知送信は実装・実行しない。APIキー、token、password、private keyなど秘密情報を追加しない。
- Done: PR #14 はmainへマージ済み。GitHub Actions Python 3.11 / 3.12 offline test suite はSUCCESS。
- Test results:
  - PASS: `python scripts/owner_smoke.py --out-dir storage/smoke` — `smoke_ok=true out_dir=storage\smoke processed=1`。
  - PASS: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` — `Ran 69 tests in 23.663s`, `OK`。
  - PASS: `git diff --check`。
  - NOTE: local環境では `python -m pytest -q` は `No module named pytest` のため未実行。GitHub ActionsではPR時に `pytest` をインストールして実行する設定。
- Safety scan: 差分内の秘密情報・禁止操作キーワードは、禁止事項の説明文・テスト文言のみ。購入、決済、出品、login、cart、checkout、browser automation、scraping、external agent API、live external API、外部通知送信の実装は追加していない。
- PR: https://github.com/fsywy020-ui/KEIJI/pull/14
- Next: mainマージ、origin/main反映確認、タスクボード最終監査。
- Blocked / Human Approval: 外部API連携、external agent API、購入・決済・出品関連、自動ブラウザ操作は引き続き個別承認が必要。

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

- PASS: `python -m pytest -q` — `42 passed, 8 subtests passed in 1.02s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 42 tests in 0.869s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-check` — `smoke_ok=true out_dir=/tmp/keiji-smoke-check processed=1`。

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

## Merge Readiness

- Merge readiness: **READY**

### マージしてよい理由

- PR #4 は PR #1〜#3 の機能範囲を包含しており、重複 PR を別途 merge する必要がない。
- P4 商品同定 → P3 利益計算 → persistence/audit/review export の offline MVP flow が実装済み。
- GitHub Actions workflow、local unittest、pytest、local smoke workflow が揃っている。
- 初期 MVP の安全境界として、購入・決済・出品・login・cart・checkout・browser automation・live external API は実装されていない。
- 初期仕入れ枠 50,000 JPY、1 SKU 上限 5,000 JPY、Amazon 中心、人間承認必須、完全自動購入禁止の方針が config/docs/code に反映されている。

### まだ注意すべき点

- READY は「local/offline MVP として merge 判断可能」という意味であり、実購入・実決済・実出品の承認ではない。
- External API adapter を有効化する場合は、別 PR で API ごとの明示承認、credentials 管理、contract tests、監査方針を追加する必要がある。
- P4 attribute extraction と P3 risk/shipping assumptions は安全側の最小実装なので、運用カテゴリに合わせて local fixtures を増やす必要がある。

### テスト結果

- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 42 tests in 0.807s`, `OK`。
- PASS: `python -m pytest -q` — `42 passed, 8 subtests passed in 1.02s`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-check` — `smoke_ok=true out_dir=/tmp/keiji-smoke-check processed=1`。

### 秘密情報チェック結果

- PASS: secret-ish pattern scan で API key / token / password / private key の実値混入は見つからなかった。
- Note: docs 内に「credentials/secrets を追加していない」という説明文は存在するが、これは秘密情報そのものではない。

### 外部操作・自動購入リスクチェック結果

- PASS: code/config/docs scan で、初期 MVP が購入・決済・出品・checkout・login・cart・browser automation・scraping・live external API を実行しない設計であることを確認。
- `src/keiji/pipeline/offline_runner.py` は local-only で外部 API / browser / purchase / payment / checkout / login を行わない旨を明記している。
- Review/export scripts は pending review と local report を作るだけで、外部操作は行わない。

### 指定除外プロジェクト混入チェック結果

- PASS: `AGENTS.md` の境界指示文を除き、指定除外プロジェクト関連参照は検出されなかった。
- `AGENTS.md` 内の境界指示記載は、このリポジトリ境界を定義するための指示文として扱う。

### PR #1〜#3の扱い

- PR #1: PR #4 に包含済み。重複のため merge 不要。
- PR #2: PR #4 に包含済み。重複のため merge 不要。
- PR #3: PR #4 に包含済み。重複のため merge 不要。

### マージ後の最初の作業

1. 非エンジニア owner は `README.md` → `STATUS.md` → `TASK_BOARD.md` → `docs/local_offline_operation_guide.md` の順に読む。
2. ローカルで `PYTHONPATH=src python scripts/local_smoke.py --out-dir storage/smoke` を実行し、生成された review/status/audit outputs を確認する。
3. 実運用前に P4 ambiguous / P3 review の人間承認基準を確認する。
4. PR #1〜#3 を close する場合は、「PR #4 に包含済みのため merge 不要」とコメントする。
5. 次の開発は `TASK_BOARD.md` の Post-Merge Next Tasks に従い、P4 fixtures 拡充から始める。


## Final Owner-Merge Comment

PR #4 is ready for owner merge. No purchase, payment, listing, checkout, login, browser automation, scraping, or live external API execution is implemented. PR #1〜#3 are duplicate/no-merge candidates because their scope is included in PR #4.

---

## Post-Merge Phase 1 Update: P4〜P7 Offline MVP

### 今回の作業内容

- P4 商品同定 edge-case fixture を拡充し、JAN 一致でも容量・セット数・色・edition・国内正規品/並行輸入品・型番・サイズ・新旧モデル・状態・まとめ売り/単品・付属品差がある場合は安全側に倒す確認を追加した。
- P4 attribute extraction に size / generation / included accessories / bundle type の conservative extraction を追加し、JAN 一致時でも型番差があれば human review が必要な ambiguous 判定にした。
- P5 `market_monitoring` を追加し、local CSV/JSON の市場観測データ、local importer、FakeMarketAdapter、live access disabled error を実装した。
- P6 `candidate_scoring` を追加し、P4/P3/P5 をまとめて購入候補スコアと conservative recommendation を出せるようにした。
- P7 `review` を追加し、人間承認用 review packet を JSON/CSV/Markdown に local output できるようにした。
- `scripts/local_smoke.py` を拡張し、既存 P4/P3/persistence/report に加えて P5/P6/P7 review packet も出力するようにした。

### 変更ファイル

- P4: `src/keiji/p4_identity/attribute_extractor.py`, `src/keiji/p4_identity/decision.py`, `tests/fixtures/p4/identity_cases.v1.json`
- P5: `src/keiji/market_monitoring/*`, `data/samples/market_observations.example.csv`, `tests/fixtures/market_observations.v1.json`, `tests/unit/market_monitoring/*`
- P6: `src/keiji/candidate_scoring/*`, `tests/unit/candidate_scoring/*`
- P7: `src/keiji/review/*`, `tests/unit/review/*`
- Integration/smoke: `tests/integration/test_p4_to_p7_offline_flow.py`, `scripts/local_smoke.py`
- Docs: `README.md`, `STATUS.md`, `TASK_BOARD.md`, `docs/local_offline_operation_guide.md`

### テスト結果

- PASS: `python -m pytest -q` — `50 passed, 21 subtests passed in 1.09s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 50 tests in 0.807s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-p4-p7` — `smoke_ok=true out_dir=/tmp/keiji-smoke-p4-p7 processed=1`。

### 未完了タスク

- P8 Codex 連携前の準備として、Codex が参照できる local review packet schema と human-only 操作手順をさらに固定化する。
- P5 の live adapter は未実装のまま維持する。実装には API 名、目的、認証情報、承認者、禁止事項の明示承認が必要。
- P7 の HTML review packet export は既存 pending review HTML とは別系統では未実装。必要なら local-only で追加する。

### ブロッカー

- remote `origin` と `main` branch がこの作業環境には存在しなかったため、最新 main の fetch/pull は実行できなかった。現在の `work` branch 状態から新規 branch `p4-p7-offline-mvp` を作成して作業した。
- 外部 API、browser automation、scraping、購入・決済・出品実行は intentionally blocked。

### 人間判断が必要な事項

- P8 Codex 連携準備に進む前に、Codex の役割を「購入直前の人間補助」に限定する wording / checklist を owner が確認する。
- `BUY_CANDIDATE` であっても購入してよいわけではなく、人間承認記録と手動確認を必須にする運用を owner が承認する。
- P5 live API adapter をいつ、どのサービスに限定して許可するかは未決定。

### 次に Codex へ渡す指示

```text
AGENTS.md、STATUS.md、TASK_BOARD.md、docs/PRD.md、docs/local_offline_operation_guide.md を読み、KEIJI の offline-first / human-approval-first 方針を維持してください。次は P8 Codex 連携前準備として、local review packet schema、human checklist、blocked action audit の仕様を docs と tests で固めてください。購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、live external API は実装しないでください。
```

---

## PR #5 Merge Readiness Check — 2026-05-14

### Merge readiness: READY

PR #5 is ready to merge from the local pre-merge check perspective.

### Checks performed

- `python -m pytest -q` — PASS: `50 passed, 21 subtests passed in 0.99s`.
- `PYTHONPATH=src python -m unittest discover -s tests -v` — PASS: `Ran 50 tests in 0.810s`, `OK`.
- `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-pr5-merge-check` — PASS: `smoke_ok=true out_dir=/tmp/keiji-smoke-pr5-merge-check processed=1`.
- Other-project contamination scan — PASS: no non-AGENTS cross-project references found.
- Safety keyword scan over `src tests scripts config` found only policy text, safety comments, tests, or disabled/live-blocked wording; no purchase/payment/listing/checkout/login/cart/browser automation/scraping/live external API implementation was found.

### Merge constraints

- main was not merged into directly.
- No purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, or live external API behavior was added during this check.
- This check did not inspect unavailable GitHub inline comments beyond the prompt-provided PR summary/diff context.

---

## PR #5 Merge Readiness

- Merge readiness: READY

### マージしてよい理由

- P4〜P7 の offline MVP 範囲を満たしている。P4 は商品同定を安全側に強化し、P5 は local CSV/JSON と FakeAdapter の範囲、P6 は候補スコアリングのみ、P7 は local review packet 出力のみで構成されている。
- P4 商品同定は、JAN が一致しても容量・セット数・色・edition・国内正規品/並行輸入品・型番・サイズ・新旧モデル・状態・まとめ売り/単品・付属品差がある場合に `same` へ寄せず、`ambiguous` / `blocked` / human review 側へ倒す fixture と実装になっている。
- P5 市場監視は local CSV/JSON importer と FakeAdapter に留まり、live API access は disabled error で止める設計になっている。
- P6 は `BUY_CANDIDATE` を出せるが、全候補に `human_approval_required_for_all_purchase_decisions` を付与し、自動購入・決済・出品の実行処理を持たない。
- P7 review packet は JSON/CSV/Markdown の local file output のみで、Slack/Discord/LINE/email 等の外部通知送信を実装していない。
- README.md、STATUS.md、TASK_BOARD.md、docs/local_offline_operation_guide.md は PR #5 の P4〜P7 offline flow と安全境界を説明する更新が入っている。

### まだ注意すべき点

- `READY` は local pre-merge check としての判断であり、GitHub 上の branch protection / required checks / 未取得の inline comments は owner が最終確認する。
- `BUY_CANDIDATE` は「買ってよい」ではなく、「人間が確認する候補」。購入・決済・出品は KEIJI の外で人間が別途判断する。
- P8 Codex 連携に進む前に、Codex の役割を「購入直前の人間補助」に限定する policy / checklist / blocked action audit を固定化する。
- External API adapter は明示承認があるまで追加しない。

### テスト結果

- PASS: `python -m pytest -q` — `50 passed, 21 subtests passed in 0.81s`.
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 50 tests in 0.624s`, `OK`.
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-pr5-final-check` — `smoke_ok=true out_dir=/tmp/keiji-smoke-pr5-final-check processed=1`.
- GitHub Actions workflow check: `.github/workflows/tests.yml` exists and is configured to run unittest, pytest, and offline smoke workflow on pull_request / push to main or work / workflow_dispatch. Remote GitHub Actions execution itself was not run from this local environment.

### 秘密情報チェック結果

- PASS: likely secret assignment scan found no API key, token, password, private key, AWS key, GitHub PAT, or OpenAI-style secret key values.
- PASS: Other-project reference scan found no non-status/non-instruction project contamination.
- Notes: broad keyword scans can match safe words such as `token` in `title_matcher` or policy text; those were reviewed as false positives and not secrets.

### 外部操作・自動購入リスクチェック結果

- PASS: forbidden action scan found no implementation of purchase, payment, listing, login, cart operation, checkout automation, browser automation, scraping, or live external API calls.
- Matches found by the scan were policy/config prohibitions, safety comments, tests asserting disabled behavior, GitHub `actions/checkout`, or `FakeMarketAdapter.fetch_live()` raising `LiveMarketAccessDisabledError`.
- PR #5 keeps KEIJI offline-first / human-approval-first and does not execute external operations.

### 人間判断が必要な事項

- Owner should approve merging PR #5 after confirming any GitHub-hosted required checks and inline comments not visible in this local environment.
- Owner should confirm that `BUY_CANDIDATE` wording is operationally understood as a review recommendation only, not purchase permission.
- Owner should decide when, if ever, a specific external API adapter may be explicitly approved.

### マージ後の最初の作業

1. Run `PYTHONPATH=src python scripts/local_smoke.py --out-dir storage/smoke` on the merged main branch.
2. Open `storage/smoke/p7_review_packets.md`, `pending_review.md`, `status.md`, and `audit_log.md` for human review.
3. Start P8 Codex確認補助への移行準備 by documenting the Codex review-assist contract, allowed/forbidden fields, human checklist, and blocked action audit tests.
4. Do not implement Codex purchase execution, payment, checkout, login, cart operation, browser automation, scraping, or live external API access.

---

## PR #5 Review Fix: Market Observation Matching — 2026-05-14

### 修正内容

- Codex Review 指摘に対応し、P5 market observation matching を「候補側と市場データ側の両方に実値がある JAN / ASIN / model_number が一致する場合のみ紐づける」方式に修正した。
- `None == None`、空文字同士、空白文字同士は一致扱いにしない。
- `scripts/local_smoke.py` は安全な matching helper を使うように変更し、identifier 不足時は market observation を付与せず P6/P7 側で `p5_market_data_missing` として扱う。
- `FakeMarketAdapter` も同じ helper を使うように揃え、local smoke と fake adapter の matching 思想を統一した。
- 追加テストで、空 identifier 同士が一致しないこと、JAN/ASIN/model_number は実値同士のみ一致すること、P7 review packet に誤った market data が混入しないことを確認した。

### テスト結果

- PASS: `python -m pytest -q` — `55 passed, 21 subtests passed in 1.35s`.
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 55 tests in 1.238s`, `OK`.
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-p4-p7` — `smoke_ok=true out_dir=/tmp/keiji-smoke-p4-p7 processed=1`.

### 残課題

- 現時点で PR #5 review fix に関する blocker はなし。
- 将来、title 類似度など identifier 以外の market matching を追加する場合は、誤紐づけ防止の fixture と human review gate を先に追加する。
- live external API adapter は引き続き未実装。明示承認があるまで追加しない。

### PR #5 Merge Readiness 再判定

- Merge readiness: READY
- 理由: review 指摘の market observation 誤紐づけリスクを修正し、必須テストが通過した。PR #5 は引き続き offline-first / human-approval-first の範囲に留まり、購入・決済・出品・checkout・login・cart 操作・browser automation・scraping・live external API を実装していない。

---

## P8 Codex review-assist Safety Contract Update

### Scope

- Added a local P8 Codex review-assist safety contract that wraps P7 review packets for human-led pre-purchase assistance only.
- Added local blocked-action evaluation and JSONL audit output for forbidden Codex action requests.
- Added P8 docs for handoff policy, human checklist, and blocked-action policy.
- Extended local smoke output with P8 handoff packets and blocked-action audit records.

### PR #6 handling

PR #6 remains `mergeable: false` and includes duplicate P5〜P7 diff content. It is treated as a no-merge candidate. This P8 branch was prepared from the current post-PR #5 main-equivalent state in this workspace and does not use PR #6's branch or merge PR #6.

### Safety status

P8 remains local-only. It does not implement purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, external agent API calls, or live external APIs. Human approval remains required before any external purchase-side action outside KEIJI.

---

## PR #7 Review Fix — 2026-05-14

### 修正内容

- `src/keiji/review_handoff/blocked_actions.py` の P8 blocked-action audit で、生成済みの `audit_event_id` を含む `BlockedActionDecision` を先に作成してから JSONL payload に serialize するよう修正した。これにより、返却 decision と JSONL 監査ログ payload の `audit_event_id` が一致し、payload 側が `null` にならない。
- `scripts/local_smoke.py` の smoke run 開始時に `p8_review_handoff_blocked_actions_audit.jsonl` が存在する場合は削除するよう修正した。SQLite DB と同様に P8 blocked-action audit artifact も fresh run として生成され、同じ `--out-dir` の再実行で古いイベントを蓄積しない。
- 追加テストで、audit path 指定時の返却 decision / JSONL payload の `audit_event_id` 一致、payload の非 null、同じ smoke `--out-dir` の2回実行時に P8 JSONL が1 run 分だけになることを確認した。

### テスト結果

- PASS: `python -m pytest -q` — `62 passed, 21 subtests passed in 2.10s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 62 tests in 1.627s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-p8` — `smoke_ok=true out_dir=/tmp/keiji-smoke-p8 processed=1`。

### 残課題

- PR #7 の GitHub-hosted required checks / branch protection は owner が GitHub 上で最終確認する。
- P8 wording / checklist は、実運用前に owner review が必要。
- External API adapter、external agent API、購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、live external API は引き続き未実装・禁止。
- PR #6 は引き続きマージ不要候補として扱う。

### PR #7 Merge Readiness 再判定

- Merge readiness: READY
- 理由: Codex Review 指摘2件に対応済みで、返却 decision と JSONL audit payload の `audit_event_id` 整合性、および local smoke の P8 blocked-action audit reset がテストで確認済み。指定された pytest / unittest / smoke run はすべて PASS。main への merge は行っていない。

---

## タスクボード運用導入 — 2026-05-14

### 作業記録

- タスクボード運用を導入した。
- `AGENTS.md` に Codex 向け標準ルールとしてタスクボード運用ルールを追加した。
- `docs/task_board_workflow.md` を追加し、タスクボードの目的、ライブ表示利用時/非利用時の運用、ChatGPT生徒会長での見せ方、Codex 作業時の反映先、禁止事項、owner approval の扱いを明文化した。
- `TASK_BOARD.md` に `タスクボード運用ルール` を追記した。
- コード実装、外部 API、自動購入、自動決済、自動出品、自動ブラウザ操作は追加していない。

### タスクボード

- Goal: Codex Studio と ChatGPT生徒会長の両方で、今後の KEIJI repo 作業を同じ `タスクボード` 形式で見える化する。
- Constraints: docs / 運用ルールのみを変更し、purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API は実装・実行しない。
- In Progress: なし。今回の docs 更新は完了。
- Next: owner が PR を確認し、今後の作業で `TASK_BOARD.md` / `STATUS.md` / PR description の同期運用を開始する。
- Blocked / Human Approval: 外部 API 接続、自動操作、購入・決済・出品関連の実装は引き続き個別の明示承認が必要。
- Done: `AGENTS.md`、`docs/task_board_workflow.md`、`TASK_BOARD.md`、`STATUS.md` を更新した。

### テスト結果

- PASS: `python -m pytest -q` — `62 passed, 21 subtests passed in 2.26s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 62 tests in 1.301s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-task-board` — `smoke_ok=true out_dir=/tmp/keiji-smoke-task-board processed=1`。

---

## P4 Edge-case Fixture Expansion — 2026-05-15

### 作業記録

- P8 owner review は文書上 OK として扱い、次タスクとして P4 fixture 拡充へ進んだ。
- `tests/fixtures/p4/identity_cases.v1.json` に型番表記ゆれ、容量単位表記ゆれ、色、セット数、サイズ、edition、国内正規品/並行輸入品の edge-case fixture を追加した。
- 追加 fixture で落ちたケースに限り、`src/keiji/p4_identity/attribute_extractor.py` に容量単位正規化、navy 色 alias、箱単位のセット数、日本正規品 alias、free size 抽出を最小追加した。
- `tests/unit/p4_identity/test_attribute_extractor_and_scoring.py` に追加 attribute extraction の unit tests を追加した。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API は実装・実行していない。

### タスクボード

- Goal: P4 商品同定 edge-case fixture を拡充し、fixture で落ちたケースだけ最小限の P4 実装修正を行う。
- Constraints: offline-first / human-approval-first。購入・決済・出品・login・cart・checkout・browser automation・scraping・external agent API・live external API は禁止。main へ直接 push しない。
- In Progress: なし。今回の fixture / minimal fix は完了。
- Next: owner が PR を確認し、次の P4 fixture 追加または P3 shipping estimator へ進むか判断する。
- Blocked / Human Approval: 外部 API、external agent API、購入・決済・出品関連、自動ブラウザ操作は引き続き個別承認が必要。
- Done: P4 edge-case fixtures、最小 attribute extractor 修正、追加 unit tests、pytest / unittest / smoke verification。

### テスト結果

- PASS: `python -m pytest tests/unit/p4_identity -q` — `20 passed, 26 subtests passed in 0.11s`。
- PASS: `python -m pytest -q` — `64 passed, 30 subtests passed in 2.64s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 64 tests in 3.097s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-p4-edge` — `smoke_ok=true out_dir=/tmp/keiji-smoke-p4-edge processed=1`。

---

## P3 Shipping Estimator / Risk Adjuster — 2026-05-15

### 作業記録

- PR #10 は main にマージ済み、P4 edge-case fixture 拡充は完了済みという前提で、次工程として P3 利益計算改善に着手した。
- `src/keiji/p3_profit/shipping_estimator.py` を追加し、送料、梱包費、fulfillment assumption を `config/profit_rules.v1.yaml` の local config から読む構造にした。
- `src/keiji/p3_profit/risk_adjuster.py` を追加し、price uncertainty、return risk、budget concentration を local config driven な structured risk details として扱う構造にした。
- 既存の reason-count penalty は廃止し、`risk_adjusted_profit_yen` は named risk detail の合計 penalty から算出するようにした。
- P3 output には最小限の追加として `shipping` summary と in-memory `risk_details` を追加した。Review packet には human review 用に `risk_details` を含めるが、SQLite persistence / existing reports は既存 schema のままとし、schema migration は不要と判断した。
- `docs/P3_profit_engine_spec.md` に、shipping estimator / risk adjuster の責務、P3 output / persistence / reports への影響、税務・会計助言ではなく運用上の概算であることを追記した。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API は実装・実行していない。

### タスクボード

- Goal: P3利益計算に local config driven な shipping estimator と risk adjuster を追加し、既存P3 engineを壊さず説明可能性を高める。
- Constraints: fixture / tests first、offline-first / human-approval-first、税務・会計助言ではなく運用上の概算。main へ直接 push しない。購入・決済・出品・login・cart・checkout・browser automation・scraping・external agent API・live external API は禁止。
- In Progress: なし。実装、docs/status更新、テストは完了。
- Next: Owner が PR を確認し、risk detail を今後 persistence schema に正規化するかどうかを判断する。現時点では schema migration なしで運用可能。
- Blocked / Human Approval: external adapter、live API、external agent API、購入・決済・出品関連、自動ブラウザ操作は引き続き個別承認が必要。
- Done: P3 shipping estimator、P3 risk adjuster、config更新、P3 unit tests、docs/status/task board更新、指定テスト実行。

### テスト結果

- PASS: `python -m pytest tests/unit/p3_profit -q` — `8 passed, 4 subtests passed in 0.04s`。
- PASS: `python -m pytest -q` — `68 passed, 30 subtests passed in 1.96s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 68 tests in 1.820s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-p3-risk-shipping` — `smoke_ok=true out_dir=/tmp/keiji-smoke-p3-risk-shipping processed=1`。

---

## Owner Review Guide / Local Review Output Improvements — 2026-05-15

### 作業記録

- 非エンジニア owner が smoke output と review packet を読むための `docs/non_engineer_review_guide.md` を追加した。
- `README.md` と `docs/local_offline_operation_guide.md` に owner 向けの読み順を追加した。
- `pending_review.md` / `pending_review.html` の出力を、human approval required、forbidden actions、P4確認ポイント、P3 operational estimate、shipping/fees、`risk_details` 参照が分かる形に改善した。
- `p7_review_packets.md` の出力を、recommendation legend、P4 identity summary、P3 profit summary、shipping assumptions、`risk_details`、do-not-purchase reasons、human approval checklist が目立つ形に改善した。
- `p8_review_handoff_packets.md` の出力を、Codexに任せてよい範囲、禁止事項、P3 snapshot、shipping、`risk_details`、required human approvals が分かる形に改善した。
- `BUY_CANDIDATE` / `TEST_BUY_CANDIDATE` は購入許可ではなく、人間確認候補であることを docs と generated Markdown に明記した。
- P3 は税務・会計助言ではなく、local/manual assumptions に基づく運用上の概算であることを明記した。
- SQLite migration や大きな schema 変更は行っていない。`risk_details` の正規化永続化は将来検討に留める。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API、Slack/Discord/LINE/email 等の外部通知送信は実装・実行していない。

### タスクボード

- Goal: KEIJI の review packet / smoke output / operation guide を、非エンジニア owner が迷わず確認できる形に改善する。
- Constraints: offline-first / human-approval-first。mainへ直接pushしない。購入・決済・出品・login・cart・checkout・browser automation・scraping・external agent API・live external API・外部通知送信は実装・実行しない。P3は運用上の概算として記述し、税務・会計助言に見える表現を避ける。
- In Progress: なし。docs と local-only Markdown output 改善は完了。
- Next: owner が `docs/non_engineer_review_guide.md` と `/tmp/keiji-smoke-owner-review-guide/` の Markdown outputs を確認し、実運用前に wording / checklist が十分か判断する。
- Blocked / Human Approval: 実運用開始、購入判断、外部API/external agent API、購入・決済・出品・checkout・login・cart 操作・browser automation・scraping・外部通知は引き続き個別の owner approval が必要。
- Done: guide追加、README/operation guide導線追加、P7/P8/pending review Markdown/HTML改善、tests更新、smoke output確認。

### テスト結果

- PASS: `python -m pytest -q` — `68 passed, 30 subtests passed in 2.30s`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 68 tests in 1.804s`, `OK`。
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-owner-review-guide` — `smoke_ok=true out_dir=/tmp/keiji-smoke-owner-review-guide processed=1`。
- PASS: generated Markdown inspection confirmed `shipping`, `risk_details`, `Human approval required`, `Forbidden actions`, `BUY_CANDIDATE` not purchase permission, and `live external API` prohibition appear in `pending_review.md`, `p7_review_packets.md`, and/or `p8_review_handoff_packets.md`.

### 残課題

- Owner が non-engineer guide と generated Markdown wording を確認する。
- `risk_details` の SQLite 正規化永続化は、必要になった場合のみ別タスクで schema change / migration として検討する。
- External API adapter、external agent API、購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、live external API、外部通知送信は引き続き未実装・禁止。

---

## Owner Review Output Wording Improvements — 2026-05-17

### 作業記録

- `local_smoke` 生成Markdownを非エンジニアowner目線で再確認し、読みにくい箇所を文言改善した。
- `pending_review.md` 相当の出力で、空の `Reason:` を `(none)` と表示し、`human_review 0` のような技術寄り表示を owner向け説明へ変更した。
- `p7_review_packets.md` 相当の出力で、`True/False` 表示、追加リスク控除なしの誤読、重複チェック項目を改善した。
- `p8_review_handoff_packets.md` 相当の出力で、Required Human Approvals に日本語説明を追加し、購入・決済は KEIJI / Codex が実行しないことを強めた。
- `status.md` / `audit_log.md` 相当の出力に、`purchase_candidates` / `purchase_candidate_created` は購入許可・購入承認ではないという安全注意を追加した。
- `docs/non_engineer_review_guide.md` に status / audit / risk details の誤読防止説明を追加した。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API、外部通知送信は実装・実行していない。

### タスクボード

- Goal: local_smoke の Markdown を、非エンジニア owner が迷わず安全に読める文言へ改善する。
- Constraints: offline-first / human-approval-first。mainへ直接pushしない。購入・決済・出品・login・cart・checkout・browser automation・scraping・external agent API・live external API・外部通知送信は実装・実行しない。
- In Progress: なし。文言改善と検証は完了。
- Next: Owner が差分を確認し、PR作成・pushするか判断する。
- Blocked / Human Approval: GitHub push / PR作成 / merge は owner approval 待ち。実購入・外部連携は引き続き個別承認が必要。
- Done: Markdown生成元、non-engineer guide、期待テスト更新、local smoke / unittest 検証。

### テスト結果

- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir storage/smoke` — `smoke_ok=true out_dir=storage\smoke processed=1`。
- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — `Ran 68 tests in 6.633s`, `OK`。
- PASS: targeted integration unittest 6件 — `Ran 6 tests in 4.428s`, `OK`。
- NOTE: `python -m pytest -q` / `uv run python -m pytest -q` は、現在のPython環境に `pytest` が未導入のため実行不可。pytest用の依存追加は行っていない。

### 残課題

- Owner が生成Markdownの最終文言を確認する。
- PR化する場合は、このブランチからGitHubへpushし、PR本文に安全境界と検証結果を記載する。

---

## タスクボード導入状況 — 2026-05-16

### 作業記録

- 作業開始前に `git status` を確認し、未コミット変更がないことを確認した。
- `git fetch origin` と `git pull --ff-only` を実行し、`Already up to date.` を確認した。
- Mitaさんの許可に基づき、`C:\AI_projects\KEIJI` で `npx goalbuddy` を実行した。
- タスクボード機能 0.3.6 がCodex / Claude Code向けにローカル導入された。
- 導入先として、Codex plugin は `C:\Users\KEIJI MITA\.codex\plugins\cache\goalbuddy\goalbuddy\0.3.6`、Claude Code skill は `C:\Users\KEIJI MITA\.claude\skills\goalbuddy` と表示された。
- GitHub共有用の正本として `TASK_BOARD.md` / `STATUS.md` を維持する方針を `AGENTS.md` と `TASK_BOARD.md` に追記した。

### タスクボード

- Goal: タスクボードのライブ運用とGitHub共有用 `TASK_BOARD.md` / `STATUS.md` 運用を両立させる。
- Constraints: タスクボードを使っても、購入、決済、出品、checkout、login、cart操作、投稿、送信、保存確定、削除、browser automation、scraping、external agent API、live external API はMitaさんの明示承認なしに実行しない。commit / push / PR作成 / merge / deploy / 外部公開もしない。
- In Progress: なし。ローカル導入と共有Markdownへの運用ルール追記は完了。
- Next: 次回の複数ステップ作業で必要に応じて `$goal-prep` を使い、`docs/goals/<slug>/goal.md` と `docs/goals/<slug>/state.yaml` を作成する。タスクボードで進捗が変わった場合は `TASK_BOARD.md` / `STATUS.md` へ要約を反映する。
- Blocked / Human Approval: `docs/goals/` をGitHub共有対象にするか、`.goalbuddy-board/` を `.gitignore` に追加するか、GitHub Projects連携を使うかはMitaさん判断。commit / push / PR作成は未承認。
- Done: `npx goalbuddy` 実行、タスクボード機能 0.3.6導入確認、`AGENTS.md` / `TASK_BOARD.md` / `STATUS.md` 更新。

### 確認結果

- `npx goalbuddy` は成功し、次の案内が表示された: Codexを再起動後に `$goal-prep`、Claude Codeを再起動後に `/goal-prep` を使う。
- この作業ではタスクボードのGoal作成、ライブボード起動、GitHub Projects連携、commit、push、PR作成は行っていない。
- `.env`、APIキー、認証情報、Cookie、トークン、秘密情報は読んでいない。

### 次にCodexへ渡すべき指示

```text
AGENTS.md、TASK_BOARD.md、STATUS.md を読み、タスクボードは毎回立ち上げ・確認・更新してください。TASK_BOARD.md / STATUS.md はGitHub共有用の正本として扱ってください。複数ステップ作業では必要に応じて $goal-prep を使い、タスクボードで変わった進捗や判断は TASK_BOARD.md / STATUS.md に要約してください。購入、決済、出品、checkout、login、cart操作、投稿、送信、保存確定、削除、browser automation、scraping、external agent API、live external API、commit、push、PR作成、merge、deploy、外部公開はMitaさんの明示承認なしに実行しないでください。
```

---

## タスクボード形式整備 — 2026-05-16

### 作業記録

- Mitaさんの指示に基づき、ユーザー向け呼称を「タスクボード」に統一した。
- `TASK_BOARD.md` の先頭に `Backlog` / `Ready` / `In Progress` / `Review` / `Done` / `Blocked` の現在ボードを追加した。
- 既存タスク、過去の完了状況、担当範囲、作業記録は削除せず、詳細履歴として残した。
- `AGENTS.md` に、毎回の作業開始・作業中・作業終了時のタスクボード運用ルールを追記した。
- 阿羅漢 AI生徒会長モードは既存AGENTSに定義済みであり、KEIJI作業では毎回その前提で動くことを `AGENTS.md` に明記した。

### 現在状況

- `TASK_BOARD.md` は、現在状態を先頭の6レーンで確認できる形になった。
- 今回の作業は `Done` と `Review` に反映済み。
- commit / push / PR作成は未実行。

### 次の一手

- Mitaさんが `TASK_BOARD.md` の6レーン構成と `AGENTS.md` の運用ルールを確認する。
- 問題なければ、次に commit / push するかをMitaさんが判断する。

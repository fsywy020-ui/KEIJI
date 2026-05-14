# KEIJI TASK BOARD

## Board Policy

- PR #4 を本命候補として扱う。
- PR #1〜#3 は PR #4 に包含済みの重複候補として扱う。
- main へ merge しない。
- 外部 API、購入、決済、出品、login、cart、checkout、browser automation は実装しない。
- すべての開発は local fixtures / local config / deterministic tests を優先する。

## 1. Codex A：P4 商品同定エンジン

### 触ってよいファイル範囲

- `src/keiji/p4_identity/*`
- `config/product_identity_rules.v1.yaml`
- `tests/unit/p4_identity/*`
- `tests/fixtures/p4/*`
- P4 に関する docs:
  - `docs/P4_product_identity_engine_spec.md`
  - `docs/P3_P4_integration_flow.md`

### 現在の完了状況

- P4 engine foundation 完了。
- Normalization / identifier / brand / title / variant / condition matching 完了。
- Attribute extraction 完了。
- Hard exclusion rules 完了。
- Scoring / decision / explain helper 完了。
- P4 unit fixtures/tests 完了。

### 次にやるべき作業

1. 型番抽出 edge cases の local fixtures を追加。
2. 容量・サイズ・色・セット数の表記ゆれ fixtures を追加。
3. ambiguous / blocked の evidence code をさらに運用しやすく整理。
4. P4 decision の human-readable explanation を review report により出しやすくする。

## 2. Codex B：P3 利益計算エンジン

### 触ってよいファイル範囲

- `src/keiji/p3_profit/*`
- `config/profit_rules.v1.yaml`
- `tests/unit/p3_profit/*`
- `tests/fixtures/p3/*`
- P3 に関する docs:
  - `docs/P3_profit_engine_spec.md`
  - `docs/P3_P4_integration_flow.md`

### 現在の完了状況

- P3 engine foundation 完了。
- Fee estimation 完了。
- ROI / net profit / margin / break-even calculation 完了。
- Capital guard 完了。
- P4 gate による skipped/review/pass/fail/blocked decision 完了。
- P3 unit fixtures/tests 完了。

### 次にやるべき作業

1. `shipping_estimator.py` を追加し、送料・梱包・fulfillment assumptions を local config から読めるようにする。
2. `risk_adjuster.py` を追加し、price uncertainty / return risk / budget concentration を local config driven にする。
3. P3 output に risk details を追加する場合は persistence/report tests も更新する。
4. Tax/accounting advice に見える表現を避け、運用上の概算であることを docs に明記する。

## 3. Codex C：テスト・サンプルデータ

### 触ってよいファイル範囲

- `tests/*`
- `tests/fixtures/*`
- `data/samples/*`
- `scripts/local_smoke.py`
- `scripts/validate_candidates.py`
- CI workflow:
  - `.github/workflows/tests.yml`

### 現在の完了状況

- Unit tests 完了。
- Integration tests 完了。
- Contract tests 完了。
- Offline smoke workflow 完了。
- GitHub Actions test workflow 完了。
- Sample CSV / JSON fixtures 完了。

### 次にやるべき作業

1. P4 edge-case fixtures を増やす。
2. P3 profit edge-case fixtures を増やす。
3. CLI tests に invalid input / empty audit / no candidate cases を追加する。
4. CI で pytest / unittest / smoke が継続して通ることを維持する。

## 4. Codex D：docs / README / 進捗管理

### 触ってよいファイル範囲

- `README.md`
- `STATUS.md`
- `TASK_BOARD.md`
- `PROGRESS.md`
- `docs/*`
- `AGENTS.md` は原則編集しない。人間から明示指示がある場合のみ編集する。

### 現在の完了状況

- README quick start 完了。
- Non-engineer summary 完了。
- PR #4 status / duplicate PR handling 記録完了。
- Progress tracking 完了。
- Architecture / operation / approval docs 完了。

### 次にやるべき作業

1. STATUS.md の test result を各実装タスク後に更新する。
2. TASK_BOARD.md の担当別 next task を実装進捗に合わせて更新する。
3. 非エンジニア向け operation guide をより短く手順化する。
4. PR #1〜#3 を close する場合のコメント文案を docs または STATUS.md に追加する。

## 5. 各担当の触ってよいファイル範囲まとめ

| 担当 | 主な範囲 | 原則触らない範囲 |
|---|---|---|
| Codex A | `src/keiji/p4_identity/*`, P4 config/tests/fixtures/docs | P3 internals, DB schema migration unless P4 persistence changes required |
| Codex B | `src/keiji/p3_profit/*`, P3 config/tests/fixtures/docs | P4 decision policy unless gate contract changes required |
| Codex C | `tests/*`, `tests/fixtures/*`, `data/samples/*`, smoke/validation scripts, CI | Production logic except test-driven minimal fixes |
| Codex D | `README.md`, `STATUS.md`, `TASK_BOARD.md`, `PROGRESS.md`, `docs/*` | Core code unless docs examples expose a bug |

## 6. 現在の完了状況

- P4 商品同定 MVP: 完了。
- P3 利益計算 MVP: 完了。
- P4 → P3 integration: 完了。
- Persistence / audit / review candidate: 完了。
- CLI / smoke workflow: 完了。
- Tests / fixtures: 完了。
- GitHub Actions workflow: 完了。
- PR #4 contains PR #1〜#3 confirmation: 完了。
- STATUS.md / TASK_BOARD.md root placement: 完了。

## 7. 次にやるべき作業

1. Codex C: P4 extraction edge-case fixtures を追加。
2. Codex A: fixtures で落ちた P4 extraction / evidence のみ修正。
3. Codex B: `shipping_estimator.py` を local config driven で追加。
4. Codex B: `risk_adjuster.py` を local config driven で追加。
5. Codex D: 変更後に README / STATUS / TASK_BOARD / docs を更新。
6. Codex C: `python -m pytest -q` と `PYTHONPATH=src python -m unittest discover -s tests -v` を実行し、STATUS.md に結果を追記。

## 8. Post-Merge Next Tasks

1. Owner / Codex D: Read `README.md`, `STATUS.md`, `TASK_BOARD.md`, and `docs/local_offline_operation_guide.md` in that order.
2. Owner / Codex C: Run `PYTHONPATH=src python scripts/local_smoke.py --out-dir storage/smoke` and inspect `pending_review.*`, `status.*`, and `audit_log.*`.
3. Codex C: Add local P4 edge-case fixtures before changing P4 extraction behavior.
4. Codex A: Improve P4 extraction/evidence only for failing local fixtures.
5. Codex B: Add local-config-driven `shipping_estimator.py` with unit tests.
6. Codex B: Add local-config-driven `risk_adjuster.py` with unit tests.
7. Codex D: Add a short non-engineer PR #1〜#3 close-comment template if those duplicate PRs are closed.
8. Human owner: Decide whether any external API adapter work is approved; until then, keep all adapters fake/local and offline.


---

## Post-Merge Phase 1 Board: P4〜P7 Offline MVP

| Phase | Status | Result | Next |
|---|---|---|---|
| P4 商品同定エンジン強化 | 完了 | edge-case fixtures 追加、size/generation/accessory/bundle extraction 追加、JAN一致+型番差は ambiguous | 実運用 fixture が増えたら category-specific patterns を追加 |
| P5 市場監視 offline 土台 | 完了 | `market_monitoring` local CSV/JSON importer と `FakeMarketAdapter` を追加、live access disabled | 明示承認まで live adapter は未着手 |
| P6 候補スコアリング | 完了 | P4/P3/P5 を統合し conservative recommendation を生成 | weight/threshold は実績 fixture で調整 |
| P7 通知・人間承認フロー | 完了 | local JSON/CSV/Markdown review packet を生成 | 必要なら local-only HTML packet export を追加 |
| P4〜P7 統合テスト | 完了 | BUY_CANDIDATE / WATCH_ONLY / BLOCKED / NEEDS_HUMAN_REVIEW を検証 | P8 前に blocked action audit tests を追加 |
| docs / status 更新 | 完了 | README / STATUS / TASK_BOARD / local operation guide 更新 | P8 準備 docs を追加 |

## P8 Manus 連携前の準備タスク

1. Manus の役割を「購入直前の人間補助」に限定する local policy doc を作る。
2. P7 review packet schema を P8 から参照可能な固定 contract として tests に追加する。
3. Manus に渡してよい情報 / 渡してはいけない情報を docs に明記する。
4. blocked actions audit として login/cart/checkout/payment/purchase/listing/browser automation/scraping/live API が実行されないことを追加テストする。
5. Owner 承認なしに external adapter を作らないことを TASK_BOARD に維持する。

---

## PR #5 Merge後の次工程: P8 Manus連携前準備

### 目的

PR #5 merge 後は、新機能実装ではなく、Manus 連携に入る前の安全 contract / docs / tests を固める。

### 完了条件

- Manus は「購入直前の人間補助」に限定され、自動購入・決済・checkout・login・cart 操作をしないことが docs と tests で明確になっている。
- P7 review packet schema が P8 handoff contract として固定されている。
- Manus に渡してよい情報 / 渡してはいけない情報が明文化されている。
- blocked action audit tests が login/cart/checkout/payment/purchase/listing/browser automation/scraping/live API を禁止事項として確認する。

### タスク

| ID | Owner | Task | Status | Notes |
|---|---|---|---|---|
| P8-1 | Codex D | Manus handoff policy doc を追加 | 未着手 | 購入直前の人間補助に限定する。 |
| P8-2 | Codex C | P7 review packet schema contract test を追加 | 未着手 | P8 が参照する fields を固定する。 |
| P8-3 | Codex D | allowed / forbidden handoff fields を docs 化 | 未着手 | 認証情報、決済情報、checkout data は渡さない。 |
| P8-4 | Codex C | blocked action audit tests を追加 | 未着手 | login/cart/checkout/payment/purchase/listing/browser automation/scraping/live API を禁止確認。 |
| P8-5 | Owner | External API adapter を許可するか判断 | 未着手 | 明示承認がない限り実装しない。 |

### 引き続き禁止

- main への直接 push。
- 自動購入、決済、出品、checkout、login、cart 操作。
- Browser automation / scraping。
- Live external API access。
- API key、token、password、private key 等の秘密情報追加。

---

## PR #5 Review Fix 完了: Market Observation Matching

| Item | Status | Notes |
|---|---|---|
| 空 identifier 同士を market observation match しない | 完了 | JAN / ASIN / model_number は双方に実値がある場合のみ一致。 |
| `scripts/local_smoke.py` の matching 修正 | 完了 | safe helper 経由に変更。identifier 不足時は market data を付与しない。 |
| `FakeMarketAdapter` との思想統一 | 完了 | fake adapter も同じ safe helper を利用。 |
| 追加テスト | 完了 | 空 identifier、JAN一致、ASIN/model一致、P7 packet混入防止を確認。 |
| PR #5 Merge Readiness 再判定 | READY | 必須テスト通過。main merge / direct push は未実施。 |

次工程は引き続き P8 Manus連携前準備。外部API接続、購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、live external API は実装しない。

## P8 Manus Handoff Safety Contract

### Done in this PR

- Add `src/keiji/manus_handoff/` for local P8 handoff packet creation, blocked-action evaluation, and local JSON/Markdown exports.
- Add P8 unit, integration, and security tests.
- Add local smoke outputs for `p8_manus_handoff_packets.json`, `p8_manus_handoff_packets.md`, and `p8_blocked_actions_audit.jsonl`.
- Document PR #6 as a no-merge candidate because it remains mergeable false and duplicates P5〜P7 scope.

### Still forbidden

Do not implement purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, Manus API calls, or live external APIs.

### Next tasks

- Owner reviews the P8 wording before any real Manus-assisted manual workflow.
- If future Manus integration is requested, require explicit approval naming API, credentials, reviewer, purpose, and forbidden boundaries.

---

## PR #7 Review Fix 完了 — 2026-05-14

| Item | Status | Notes |
|---|---|---|
| P8 audit_event_id の JSONL 保持 | 完了 | audit id 入りの decision を作成してから serialize し、返却値と JSONL payload の id 一致・非 null をテスト済み。 |
| local_smoke P8 audit reset | 完了 | smoke run 開始時に既存 `p8_blocked_actions_audit.jsonl` を削除し、同じ out-dir の再実行でも古いイベントを蓄積しないことをテスト済み。 |
| 追加テスト | 完了 | unit test と integration test を追加し、pytest / unittest / smoke run が PASS。 |
| PR #7 Merge Readiness | READY | Codex Review 指摘2件は修正済み。GitHub 上の required checks は owner が最終確認する。 |
| PR #6 | マージ不要候補を維持 | PR #7 review fix の対象外。 |

引き続き、main merge、自動購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、Manus API、live external API は行わない。

---

## タスクボード運用ルール

- 今後の開発タスクは `Goal` / `Constraints` / `In Progress` / `Next` / `Blocked` / `Done` で管理する。
- Codex Studio では GoalBuddy を優先し、利用可能な場合は `/goal`、`goal-prep`、または同等の準備 workflow を先に使う。
- ChatGPT生徒会長も同じ形式で毎回見える化し、Codex Studio / GoalBuddy 側のカード、`STATUS.md`、`TASK_BOARD.md` と整合させる。
- P8 以降も offline-first / human-approval-first を維持する。
- owner approval が必要な判断は `Blocked / Human Approval` に置き、購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、Manus API、live external API は明示承認なしに実装・実行しない。

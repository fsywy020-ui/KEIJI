# KEIJI TASK BOARD

## 現在のタスクボード

このファイルは、GitHub共有用の人間向けタスクボード正本です。作業中にライブ表示のタスクボードを使う場合でも、最終的な共有状態はこの `TASK_BOARD.md` に反映します。

### Backlog

| ID | タスク | 担当 | 完了条件 |
|---|---|---|---|
| B-001 | P4の実運用fixtureが増えた場合、category-specific extraction / evidence をfixture-firstで調整する | Codex A / C | 追加fixture、最小実装修正、pytest / unittest / smoke確認 |
| B-002 | P3のshipping category override / risk penaltyを実績fixtureに合わせて調整する | Codex B / C | local config更新、P3 unit tests、STATUS更新 |
| B-003 | `risk_details` を将来SQLite schemaに正規化するか検討する | Owner / Codex B | 必要性判断、実施する場合は別タスク化 |
| B-004 | 外部API adapterを使うか判断する | Owner | API名、目的、認証、禁止境界を明示承認するか決定 |

### Ready

| ID | タスク | 担当 | 着手条件 |
|---|---|---|---|
| R-001 | 次回の複数ステップ作業でタスクボードを起動・更新する | Codex | 作業開始時に `AGENTS.md` / `STATUS.md` / `TASK_BOARD.md` とgit状態を確認 |
| R-002 | Owner review guideとgenerated Markdown wordingを確認する | Owner | `docs/non_engineer_review_guide.md` とsmoke出力を読む |
| R-003 | 非エンジニア向けoperation guideをさらに短く手順化する | Codex D | Ownerが読みづらい箇所を指定 |

### In Progress

| ID | タスク | 担当 | 現在状況 |
|---|---|---|---|
| IP-001 | Codex Review Assist移行PR作成・main反映 | Codex | ローカル検証済み。PR作成、GitHub checks確認、mainマージを実施中 |

### Review

| ID | タスク | 確認者 | 確認ポイント |
|---|---|---|---|
| RV-001 | タスクボード呼称統一と常時運用ルール | Mitaさん | 「タスクボード」表記、開始時/作業中/終了時ルール、commit/push禁止が意図通りか |

### Done

| ID | タスク | 完了条件と確認結果 |
|---|---|---|
| D-001 | P4商品同定MVP | P4 engine / fixtures / tests完了 |
| D-002 | P3利益計算MVP | P3 engine / shipping estimator / risk adjuster / tests完了 |
| D-003 | P4→P3 integration | offline runner / gate / persistence / audit / review flow完了 |
| D-004 | P5〜P8 offline / human-approval-first flow | local market monitoring、candidate scoring、review packet、Codex review-assist safety contract完了 |
| D-005 | Owner review output改善 | 非エンジニア向けguide、Markdown/HTML出力改善、tests確認完了 |
| D-006 | タスクボード導入 | `npx goalbuddy` 実行、タスクボード機能 0.3.6導入、共有Markdownへの初回追記完了 |
| D-007 | タスクボード常時運用ルール整備 | `AGENTS.md` / `TASK_BOARD.md` / `STATUS.md` に毎回運用ルールと6レーン構成を反映。git diff確認待ち |
| D-008 | Owner review output改善 main反映 | PR #13 をmainへマージ済み。レビュー出力の安全文言改善完了 |
| D-009 | API連携なしowner向け安全実装 main反映 | PR #14 をmainへマージ済み。owner_smoke導線とowner_review_index追加完了 |
| D-010 | 旧外部操作AI前提をCodex確認補助へ移行 | コード/docs/testsを `review_handoff` / Codex Review Assist 方針へ更新。Excel複製 `ai_resale_project_master_plan_2026-05-17_codex_updated.xlsx` 作成。owner_smoke / unittest / 旧表記スキャン / diff check完了 |
| D-011 | タスクボード生成物のGit管理方針整理 | `docs/goals/` のgoal/state/notesは共有対象にし、画面表示用 `.goalbuddy-board/` は `.gitignore` 対象に整理 |

### Blocked

| ID | タスク | 理由 | 解除条件 |
|---|---|---|---|
| BL-001 | 購入、決済、出品、checkout、login、cart操作 | KEIJI安全境界により禁止 | Mitaさんの明示承認が必要 |
| BL-002 | 投稿、送信、保存確定、削除、外部公開、deploy | 外部影響があるため禁止 | Mitaさんの明示承認が必要 |
| BL-003 | browser automation、scraping、external agent API、live external API | 初期MVP範囲外かつ高リスク | 対象、目的、認証、禁止境界の明示承認が必要 |
| BL-004 | 購入・決済・出品に近いCodex/browser実操作 | 今回の移行後も初期MVP範囲外 | 対象、目的、停止条件を別途明示承認するまで実装・実行しない |

### Current Goal / Constraints / Next

- Goal: 旧外部操作AI前提のP8表記・コード・計画表を、Codex中心のlocal review assist方針へ移行する。
- Constraints: 購入、決済、出品、login、cart、checkout、browser automation、scraping、external agent API、live external API、外部通知送信は実装・実行しない。秘密情報を追加しない。
- Next: PR作成、GitHub checks確認、mainマージまで完了する。

---

## 詳細履歴・既存タスク

以下は既存タスク、過去の完了状況、担当範囲、作業記録です。削除せず保持し、上の `Backlog` / `Ready` / `In Progress` / `Review` / `Done` / `Blocked` に現在状態を要約します。

## Board Policy

- PR #4 を本命候補として扱う。
- PR #1〜#3 は PR #4 に包含済みの重複候補として扱う。
- 現在はMitaさん承認済みのPRのみmainへmergeする。
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

## P8 Codex 連携前の準備タスク

1. Codex の役割を「購入直前の人間補助」に限定する local policy doc を作る。
2. P7 review packet schema を P8 から参照可能な固定 contract として tests に追加する。
3. Codex に渡してよい情報 / 渡してはいけない情報を docs に明記する。
4. blocked actions audit として login/cart/checkout/payment/purchase/listing/browser automation/scraping/live API が実行されないことを追加テストする。
5. Owner 承認なしに external adapter を作らないことを TASK_BOARD に維持する。

---

## PR #5 Merge後の次工程: P8 Codex確認補助への移行準備

### 目的

PR #5 merge 後は、新機能実装ではなく、Codex 連携に入る前の安全 contract / docs / tests を固める。

### 完了条件

- Codex は「購入直前の人間補助」に限定され、自動購入・決済・checkout・login・cart 操作をしないことが docs と tests で明確になっている。
- P7 review packet schema が P8 handoff contract として固定されている。
- Codex に渡してよい情報 / 渡してはいけない情報が明文化されている。
- blocked action audit tests が login/cart/checkout/payment/purchase/listing/browser automation/scraping/live API を禁止事項として確認する。

### タスク

| ID | Owner | Task | Status | Notes |
|---|---|---|---|---|
| P8-1 | Codex D | Codex review-assist policy doc を追加 | 未着手 | 購入直前の人間補助に限定する。 |
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

次工程は引き続き P8 Codex確認補助への移行準備。外部API接続、購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、live external API は実装しない。

## P8 Codex review-assist Safety Contract

### Done in this PR

- Add `src/keiji/review_handoff/` for local P8 handoff packet creation, blocked-action evaluation, and local JSON/Markdown exports.
- Add P8 unit, integration, and security tests.
- Add local smoke outputs for `p8_review_handoff_packets.json`, `p8_review_handoff_packets.md`, and `p8_review_handoff_blocked_actions_audit.jsonl`.
- Document PR #6 as a no-merge candidate because it remains mergeable false and duplicates P5〜P7 scope.

### Still forbidden

Do not implement purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, external agent API calls, or live external APIs.

### Next tasks

- Owner reviews the P8 wording before any real Codex-assisted manual workflow.
- If future Codex integration is requested, require explicit approval naming API, credentials, reviewer, purpose, and forbidden boundaries.

---

## PR #7 Review Fix 完了 — 2026-05-14

| Item | Status | Notes |
|---|---|---|
| P8 audit_event_id の JSONL 保持 | 完了 | audit id 入りの decision を作成してから serialize し、返却値と JSONL payload の id 一致・非 null をテスト済み。 |
| local_smoke P8 audit reset | 完了 | smoke run 開始時に既存 `p8_review_handoff_blocked_actions_audit.jsonl` を削除し、同じ out-dir の再実行でも古いイベントを蓄積しないことをテスト済み。 |
| 追加テスト | 完了 | unit test と integration test を追加し、pytest / unittest / smoke run が PASS。 |
| PR #7 Merge Readiness | READY | Codex Review 指摘2件は修正済み。GitHub 上の required checks は owner が最終確認する。 |
| PR #6 | マージ不要候補を維持 | PR #7 review fix の対象外。 |

引き続き、main merge、自動購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、external agent API、live external API は行わない。

---

## タスクボード常時運用ルール

- 今後の開発タスクは `Backlog` / `Ready` / `In Progress` / `Review` / `Done` / `Blocked` で管理する。
- 作業開始時は必ず `AGENTS.md` / `STATUS.md` / `TASK_BOARD.md` を読み、`git status` → `git fetch origin` → `git pull --ff-only` を確認する。
- 新しい作業は `Backlog` または `Ready` に追加し、着手時に `In Progress` へ移す。
- 完了した作業は `Done` に移し、完了条件と確認結果を書く。
- 保留・詰まり・人間承認待ちは `Blocked` に移し、理由を書く。
- Mitaさん確認待ちは `Review` に置き、確認ポイントを書く。
- Codex Studio でライブ表示のタスクボードが使える場合は毎回起動・更新する。使えない場合も `TASK_BOARD.md` 上で同じ形式を維持する。
- ChatGPT生徒会長も同じ形式で毎回見える化し、`STATUS.md`、`TASK_BOARD.md` と整合させる。
- P8 以降も offline-first / human-approval-first を維持する。
- owner approval が必要な判断は `Blocked` に置き、購入、決済、出品、checkout、login、cart 操作、投稿、送信、保存確定、削除、browser automation、scraping、external agent API、live external API は明示承認なしに実装・実行しない。

---

## P4 Edge-case Fixture Expansion — 2026-05-15

### Goal

P8 owner review を文書上 OK として扱った後、タスクボードに従って P4 商品同定 edge-case fixture を拡充する。

### Constraints

- コード変更より先に local fixture を追加する。
- Fixture で落ちたケースだけ、P4 実装を最小限修正する。
- Offline-first / human-approval-first を維持する。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API は実装・実行しない。
- main へ直接 push しない。

### In Progress

- なし。P4 edge-case fixture 追加と最小実装修正は完了。

### Next

- Owner が PR を確認する。
- 次の P4 改善は、追加 fixture が失敗した場合だけ category-specific extraction / evidence を最小修正する。

### Blocked / Human Approval

- External API adapter、external agent API、購入・決済・出品・checkout・login・cart 操作・browser automation・scraping・live external API は引き続き個別の owner approval が必要。

### Done

- 型番表記ゆれ、容量単位表記ゆれ、色、セット数、サイズ、edition、国内正規品/並行輸入品の P4 fixture を追加。
- Fixture で落ちた容量正規化、navy 色 alias、箱単位のセット数、日本正規品 alias、free size 抽出だけを P4 attribute extractor に最小追加。
- P4 unit tests、全 pytest、unittest discover、local smoke が PASS。

---

## P3 Shipping Estimator / Risk Adjuster — 2026-05-15

### Goal

P3利益計算に local config driven な `shipping_estimator.py` と `risk_adjuster.py` を追加し、既存P3 engineを壊さず、送料・梱包費・fulfillment assumptions・price uncertainty・return risk・budget concentration を説明可能にする。

### Constraints

- Fixture / tests first で進める。
- Offline-first / human-approval-first を維持する。
- 税務・会計助言ではなく、運用上の概算として扱う。
- main へ直接 push しない。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API は実装・実行しない。

### In Progress

- なし。今回の P3 shipping / risk module 追加は完了。

### Next

- Owner が PR を確認する。
- 次回 Codex-ready instruction: 実運用 fixture が増えたら、local config の shipping category override / risk penalty を fixture-first で調整する。
- Owner-visible decision: structured `risk_details` を将来 SQLite schema に正規化するか。現時点では review packet に含め、既存 persistence schema は維持する。

### Blocked / Human Approval

- External API adapter、live shipping/rate lookup、external agent API、購入・決済・出品・checkout・login・cart 操作・browser automation・scraping・live external API は引き続き個別の owner approval が必要。

### Done

- `shipping_estimator.py` を追加し、local config の shipping assumptions を P3 engine に統合。
- `risk_adjuster.py` を追加し、reason-count penalty を structured local risk adjustment に置換。
- `config/profit_rules.v1.yaml` に `shipping` / `risk_adjustment` rules を追加。
- P3 output に最小限の `shipping` summary / `risk_details` を追加し、review packet に risk details を反映。
- `docs/P3_profit_engine_spec.md`、`STATUS.md`、`TASK_BOARD.md` を更新。
- P3 unit tests と full pytest が PASS。

---

## Owner Review Guide / Local Review Output Improvements — 2026-05-15

### Goal

KEIJI の review packet / smoke output / operation guide を、非エンジニア owner が迷わず確認できる形に改善する。

### Constraints

- Offline-first / human-approval-first を維持する。
- mainへ直接pushしない。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API、Slack/Discord/LINE/email 等の外部通知送信は実装・実行しない。
- `BUY_CANDIDATE` / `TEST_BUY_CANDIDATE` は購入許可ではなく、人間確認候補として明記する。
- P3は税務・会計助言ではなく、運用上の概算として記述する。
- 大きな schema 変更や SQLite migration は避ける。

### In Progress

- なし。今回の docs / local Markdown output 改善は完了。

### Next

- Owner が `docs/non_engineer_review_guide.md`、`storage/smoke/pending_review.md` 相当、`p7_review_packets.md`、`p8_review_handoff_packets.md` を確認する。
- 次回 Codex-ready instruction: owner が読みづらい表現や不足チェック項目を指定した場合、docs/output wording を fixture-first / local-only で調整する。

### Blocked / Human Approval

- 実運用開始、購入判断、外部API/external agent API、購入・決済・出品・checkout・login・cart 操作・browser automation・scraping・live external API・外部通知送信は引き続き個別の owner approval が必要。
- `risk_details` の SQLite 正規化永続化は、owner が必要と判断した場合のみ別タスクで検討する。

### Done

- `docs/non_engineer_review_guide.md` を追加し、smoke後に見るファイル、各Markdownの見方、recommendation meaning、P4/P3確認ポイント、shipping/`risk_details`、Codex境界、owner checklist を明文化。
- `README.md` と `docs/local_offline_operation_guide.md` に owner 向け読み順を追加。
- `src/keiji/io/review_report.py` の pending review Markdown/HTML に human approval、forbidden actions、P3 operational estimate、shipping/fees、`risk_details` 参照を追加。
- `src/keiji/review/packet.py` / `src/keiji/review/export.py` の P7 packet に shipping summary と owner向け sections を追加。
- `src/keiji/review_handoff/export.py` の P8 Markdown に allowed tasks、forbidden actions、P3 snapshot、shipping、`risk_details` を追加。
- Tests updated for owner-facing output expectations.
- `python -m pytest -q`、`PYTHONPATH=src python -m unittest discover -s tests -v`、`PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-owner-review-guide` が PASS。

---

## Owner Review Output Wording Improvements — 2026-05-17

### Goal

`local_smoke` の Markdown を、非エンジニア owner が迷わず安全に読める文言へ改善する。

### Constraints

- Offline-first / human-approval-first を維持する。
- mainへ直接pushしない。
- Purchase、payment、listing、checkout、login、cart operation、browser automation、scraping、external agent API、live external API、外部通知送信は実装・実行しない。
- 修正は表示文言、Markdown出力、non-engineer guide、期待テストに限定する。

### In Progress

- なし。文言改善と検証は完了。

### Next

- Owner が差分を確認する。
- Owner approval 後に、必要ならGitHubへpushしてPRを作成する。

### Blocked / Human Approval

- GitHub push / PR作成 / merge は owner approval 待ち。
- 実購入、決済、出品、外部API、external agent API、自動ブラウザ操作、外部通知は引き続き個別承認が必要。

### Done

- `pending_review.md` 相当の出力で、空の `Reason:` と技術寄りの human review 表示を改善。
- `p7_review_packets.md` 相当の出力で、`True/False`、追加リスク控除なし、重複チェック項目を改善。
- `p8_review_handoff_packets.md` 相当の出力で、Required Human Approvals の日本語説明と KEIJI / Codex 非実行を強化。
- `status.md` / `audit_log.md` 相当の出力に、購入許可・購入承認ではない安全注意を追加。
- `docs/non_engineer_review_guide.md` と integration tests を更新。
- `PYTHONPATH=src python scripts/local_smoke.py --out-dir storage/smoke` と `PYTHONPATH=src python -m unittest discover -s tests -v` が PASS。

---

## タスクボード導入と共有運用 — 2026-05-16

### Goal

Codexアプリ版でライブ表示のタスクボードを使いながら、GitHub共有用の `TASK_BOARD.md` / `STATUS.md` を正本として維持する。

### Constraints

- ライブ表示のタスクボードは進行確認と作業整理のために使う。
- `TASK_BOARD.md` はGitHub共有用の人間向けタスクボード正本として維持する。
- `STATUS.md` は作業記録、確認結果、テスト結果、残課題、人間判断事項の正本として維持する。
- `docs/goals/<slug>/state.yaml` は進行中Goalのライブボード正本だが、GitHub共有用の正本ではない。
- タスクボードを使っても、購入、決済、出品、checkout、login、cart操作、投稿、送信、保存確定、削除、browser automation、scraping、external agent API、live external API はMitaさんの明示承認なしに実行しない。
- commit、push、PR作成、merge、deploy、外部公開はMitaさんの明示承認まで行わない。

### In Progress

- なし。タスクボードのローカルセットアップと共有Markdownへの運用ルール追記は完了。

### Next

- 次回の複数ステップ作業では、必要に応じて `$goal-prep` でタスクボード用のGoalを作成する。
- タスクボードで作業した場合は、チェックポイントごとに `TASK_BOARD.md` と `STATUS.md` へ要約を反映する。
- `.goalbuddy-board/` などの生成物をGit管理対象にするか、`.gitignore` へ追加するかをMitaさんが判断する。

### Blocked / Human Approval

- タスクボードのGitHub Projects連携は未使用。使う場合は、GitHubへの書き込みが発生するため別途明示承認が必要。
- `docs/goals/` をGitHub共有対象にするかどうかはMitaさん判断。
- commit / push / PR作成は未承認のため実行しない。

### Done

- `npx goalbuddy` を実行し、タスクボード機能 0.3.6 がCodex / Claude Code向けにローカル導入された。
- `AGENTS.md` にタスクボードと `TASK_BOARD.md` / `STATUS.md` の役割分担を追記。
- `TASK_BOARD.md` にタスクボード導入タスクと今後の運用ルールを追記。

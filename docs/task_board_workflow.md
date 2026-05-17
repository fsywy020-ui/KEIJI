# タスクボード / GoalBuddy Workflow

## 目的

`タスクボード` は、KEIJI の開発・レビュー・PR triage・複数ステップの作業を、Codex Studio と ChatGPT生徒会長の両方から常に同じ形で確認できるようにするための GoalBuddy-style タスク管理ルールです。

タスクボードは、作業の目的、制約、進行中の作業、次の手、ブロッカー、人間承認待ち、完了事項を明示し、offline-first / human-approval-first の方針を崩さないために使います。

## 標準レーン

すべてのタスクボードは、以下のレーンで管理します。

- Goal
- Constraints
- In Progress
- Next
- Blocked / Human Approval
- Done

## GoalBuddy が使える場合

Codex Studio / GoalBuddy が利用可能な場合は、実装・レビュー・PR triage・複数ステップの repository task を始める前に、先に `/goal`、`goal-prep`、または環境で設定された同等コマンドを実行します。

GoalBuddy のカードは、`TASK_BOARD.md` と `STATUS.md` の内容と一致するように保ちます。大きな変更に入る前には、`AGENTS.md`、`STATUS.md`、`TASK_BOARD.md`、関連 docs を再確認します。

## GoalBuddy が使えない場合

GoalBuddy が使えない環境でも、同じ `タスクボード` 構造を手動で維持します。

- Codex の応答
- PR description
- `STATUS.md`
- `TASK_BOARD.md`
- 必要な status notes

上記のいずれか、または複数に、Goal / Constraints / In Progress / Next / Blocked / Human Approval / Done を見える形で反映します。

## ChatGPT生徒会長での見せ方

ChatGPT生徒会長側でも、Codex Studio と同じレーンで進捗を表示します。

- Goal: 今回の目的
- Constraints: 守る制約、禁止事項、承認条件
- In Progress: 現在進めている作業
- Next: 次に実行可能な checkpoint
- Blocked / Human Approval: owner approval または人間判断が必要な事項
- Done: 完了した作業と確認結果

## Codex 作業時の反映先

Codex 作業では、タスクボード更新を以下に反映します。

- PR description: 変更内容、制約、テスト結果、次の owner-visible decision を記録する。
- `STATUS.md`: 今回の作業記録、テスト結果、残課題、禁止事項に触れていないことを記録する。
- `TASK_BOARD.md`: 現在の Goal / Constraints / In Progress / Next / Blocked / Done を更新する。

## 禁止事項

明示的かつ個別の owner approval がない限り、タスクボード運用や Codex 作業で以下を実装・実行しません。

- purchase
- payment
- listing
- checkout
- login
- cart operation
- browser automation
- scraping
- external agent API
- live external API

## Owner approval が必要な場合

owner approval が必要な判断、外部連携、運用開始判断、制約変更は、`Blocked / Human Approval` に置きます。

承認待ちの項目には、以下を明記します。

- 何を承認してほしいか
- 承認がない場合に進めてはいけない作業
- 禁止事項との関係
- 次に Codex が実行できる安全な指示

## 運用原則

- Keep work offline-first and human-approval-first.
- Prefer small checkpoint-based steps over large one-shot changes.
- Re-check `AGENTS.md`, `STATUS.md`, `TASK_BOARD.md`, and relevant docs before major changes.
- Make forbidden actions explicit: no purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, external agent API, or live external API unless separately and explicitly approved.
- End with the next owner-visible decision or the next Codex-ready instruction.

# KEIJI レビュー出力の文言改善

## Objective

非エンジニアownerが、KEIJIの `local_smoke` Markdown出力を「購入許可」と誤解せず、安全に確認できる文言へ改善する。

## Original Request

Mitaさんから、タスクボードを右側Windowに表示しながら、`local_smoke` 出力Markdownの文言改善を進めるよう依頼された。

## Intake Summary

- 依頼の形: `specific`
- 読む人: KEIJI owner / 非エンジニア確認者
- 実行権限: `approved`
- 完了確認: `test`
- 完了条件: 生成Markdownの文言が改善され、local smoke と unittest が通り、右側タスクボードに現在地が表示されていること。
- 失敗しやすい点: 静的な簡易表をタスクボードとして出してしまうこと。文言改善のつもりで human-approval-first の安全境界を弱めてしまうこと。
- 見落とし注意: `BUY_CANDIDATE` が購入許可に見える、`purchase_candidate_created` が購入承認に見える、追加リスク控除なしが「リスクなし」に見える、Codex確認補助文言が購入実行に見える。
- 既存前提: offline-first / human-approval-first。購入、決済、出品、login、cart、checkout、browser automation、scraping、external agent API、live external API、外部通知は追加しない。

## Goal Kind

`specific`

## Current Tranche

ローカルの文言改善のみを完了し、生成Markdownを検証し、PR / push 判断のためにowner向けタスクボードを表示し続ける。

## Non-Negotiable Constraints

- Do not push to main directly.
- Do not implement or execute purchase, payment, listing, login, cart, checkout, browser automation, scraping, external agent API, live external API, or external notification sending.
- Keep all work local/offline unless Mitaさん explicitly approves a GitHub operation.
- Do not add secrets, API keys, credentials, tokens, passwords, or private keys.
- Treat `BUY_CANDIDATE` / `TEST_BUY_CANDIDATE` as human review candidates only.

## Stop Rule

ローカル文言改善の検証が完了し、残るowner判断がタスクボードに明確に表示されたら停止する。

## Canonical Board

Machine truth lives at:

`docs/goals/owner-review-output-wording/state.yaml`

## Run Command

```text
/goal Follow docs/goals/owner-review-output-wording/goal.md.
```

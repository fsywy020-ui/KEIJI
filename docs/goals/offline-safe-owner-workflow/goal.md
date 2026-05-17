# KEIJI API連携なし安全実装

## 目的

API連携、購入、決済、出品、login、cart、checkout、browser automation、scraping、Manus API、live external API、外部通知を行わずに、KEIJIの非エンジニアowner向け運用をさらに安全で迷いにくくする。

## 今回の完了条件

- 現在の `AGENTS.md` / `STATUS.md` / `TASK_BOARD.md` / docs / tests / smoke出力を再確認する。
- API連携なしで進められる最も効果的な設計・実装範囲を決める。
- 実装、テスト、smoke確認、ドキュメント更新、タスクボード更新を行う。
- GitHub PRを作成し、チェック成功後にmainへマージする。

## 絶対にやらないこと

- 購入、決済、出品、注文確定。
- login、cart、checkout。
- browser automation、scraping。
- Manus API、live external API。
- Slack、Discord、LINE、emailなど外部通知送信。
- APIキー、token、password、private keyなど秘密情報の追加。

## 今回の進め方

タスクボードを右側に表示し、各カードの開始前・完了後に状態を更新する。GitHub操作は、Mitaさんの「PRしてマージまで任せる」という承認範囲内で、今回のPR作成とmainマージに限定する。

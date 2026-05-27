# Yahoo!デベロッパー登録ページ準備記録

Date: 2026-05-26

## 結論

Yahoo!デベロッパー登録に向けて、輝煌堂 物販API検証用の公開ページを作成し、GitHub Pagesで公開した。

## 反映済みの公開情報

- 運営者名: 輝煌堂
- 連絡先: restartllc88@gmail.com

## 作成済みファイル

- `docs/yahoo-developer-registration/index.html`
- `docs/yahoo-developer-registration/privacy.html`
- `docs/yahoo-developer-registration/terms.html`
- `docs/yahoo-developer-registration/registration_values.md`
- `docs/yahoo-developer-registration/official_source_notes.md`
- `docs/yahoo-developer-registration/README.md`

## 公開URL

- サイトURL: https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/
- プライバシーポリシーURL: https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/privacy.html
- 利用規約URL: https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/terms.html

## ページ内容

- 輝煌堂 物販API検証は、物販業務における価格調査、商品情報確認、仕入れ判断補助を目的とするAPI検証用ツールとして説明。
- 初期検証はYahoo!ショッピングAPIの読み取り用途を中心にする。
- 注文API、お問い合わせ管理API、定期購入APIなど追加申請が必要なAPIは初期検証対象外。
- 購入、決済、出品、価格変更、注文確定、ログイン、カート投入、チェックアウトの自動実行は行わない。
- Yahoo! APIクレジット表示をトップページ下部に配置。
- プライバシーポリシーには、取得する情報、現段階で取得しない個人情報、利用目的、第三者提供、保存期間と削除、安全管理を記載。
- 利用規約には、対象範囲、禁止事項、外部API規約順守、人間による確認、免責を記載。

## 公式情報確認

確認した主な公式ページ:

- Yahoo! ID連携 v2「Client IDを登録する」
- Yahoo!デベロッパーネットワーク「クレジット表示」
- Yahoo!デベロッパーネットワーク「ガイドライン」
- Yahoo!ショッピングAPI「各種申請に関するヘルプ」
- Yahoo!ショッピングAPI「導入までの流れ」

判断:

- 登録で重要なのは、豪華なサイトではなく、実在する用途説明、プライバシーポリシー、利用規約、運営者情報、連絡先、クレジット表示。
- Yahoo!側の承認可否は、申請画面の入力内容、公開URL、利用者区分、選択スコープ、審査によって変わるため保証はできない。
- ただし、現在の下書きは「何のツールか」「何をしないか」「情報をどう扱うか」を説明できる状態になっている。

## 公開確認

- GitHub Pages source: `main` / `docs`
- GitHub Pages status: built
- サイトURL: HTTP 200
- プライバシーポリシーURL: HTTP 200
- 利用規約URL: HTTP 200

## 次に決めること

1. Yahoo!デベロッパー登録画面へ入力するタイミング。
2. ID連携利用有無をどう選ぶか。
3. 登録後にClient IDやSecretをどこに安全に保管するか。

## 安全境界

以下は未実行:

- PR作成
- Yahoo!デベロッパー登録フォーム送信
- APIキー、Client Secret、トークン、認証コードの記録
- 購入、決済、出品、注文確定、価格変更、外部送信

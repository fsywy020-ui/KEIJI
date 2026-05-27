# Yahoo!デベロッパー登録 入力値案

Date: 2026-05-26

## 推奨入力

アプリケーション名:

```text
KEIJI 物販API検証
```

アプリケーションの説明:

```text
KEIJIは、物販業務における価格調査・商品情報確認を目的としたAPI検証用ツールです。
Yahoo!ショッピングAPIから取得した商品情報を、社内検証および仕入れ判断の補助に利用します。
購入、決済、出品、価格変更、注文確定の自動実行は行いません。
初期検証では、商品情報、カテゴリ、ランキング、在庫や販売状態などの確認に関わる読み取り用途を中心に扱います。
```

サイトURL:

```text
https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/
```

プライバシーポリシーURL:

```text
https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/privacy.html
```

利用規約URL:

```text
https://fsywy020-ui.github.io/KEIJI/yahoo-developer-registration/terms.html
```

## 現時点の判断

- 公開ページ、プライバシーポリシー、利用規約は用意する方針が安全。
- ただし、公開URL作成やGitHub Pages公開は外部公開なので、Mitaさん確認後に実行する。
- Yahoo!ショッピングAPIの読み取り・調査用途に絞る。
- 注文API、問い合わせ管理API、定期購入API、出品・価格変更・購入・決済系は今回対象外。
- Yahoo! JAPAN IDの属性取得APIで氏名・メールアドレスなどを取得する予定は初期検証では置かない。
- URLは `https://localhost/` のようなローカルURLではなく、ホスト名にドットを含む公開URLにする。

## 公開前にMitaさんが決めること

- 公開する運営者名: `輝煌堂`
- 公開する連絡先: `restartllc88@gmail.com`
- GitHub Pagesで公開してよいか。
- ID連携利用有無を「利用する」にするか。ショッピングAPIのテスト環境では公式ヘルプ上「利用する」指定が必要。

## 公開前の確認事項

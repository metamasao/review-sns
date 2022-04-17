# 簡単な自己紹介とレビューSNS作成について

## はじめに
本稿ではまず私は何に興味があるのか、勉強する際にどういったことに注意を払ってきたのかといった簡単な自己紹介を行います。次に私が作成したレビューSNSについて、設計思想から基本的な機能やなぜこのようなアプリケーションを作ったのかという動機、目的を達成するために工夫した点、どのような書籍や記事に基づいて作成したのか説明します。最後に、今回作ったアプリケーションについての反省や、これまで勉強したこと、今後勉強したいことについて述べます。

## 自己紹介
私は統計的学習に当初興味があり勉強していましたが、webに関する基本的知識があまりになさすぎると思い、去年7月頃から勉強し始めたところ、こちらのほうが面白くやりがいを感じるようになり、現在web系エンジニアになるべく独学で勉強しています（「独学」という言葉は巨人の方に乗ることを否定するきらいがあるのであまり好きではありませんが、他の方との差異を強調する可能性があるので使いました）。また勉強する際には、和書に限定せず洋書も含めてできる限り信頼できる書籍を探し、それに依拠するまたは公式ドキュメントに基いて学習を進めました。ネットの記事を参考にすることもありますが、それも信頼できる書籍から参照されている場合のみに限っています。どのような書籍を参考にしたのかは次節以降に記します。以下、簡単に私が興味のあることを書いています。

- ?

## レビューSNSについて

### なぜ書評SNSを作ったか
私だけではないと思いますが、次のような問題に頭を悩ませるひとがいると思います。「ある分野の入門書を探してるけど、何が最適なテキストなのかわからない」「とりあえず入門書を1冊読んだけど、次に何を読めばいいのかわからない」。このような困難を少しでも克服できるようなSNSを作りたい。このような動機から本アプリケーションを作成しました。

### 設計思想について
Test以外ではできる限りDRYに従い、ModelやViewを作るときはFat ModelやThin View(Controller)の方針に従いロジックなどはViewではなくできる限りModelに記述しました。また、伝統的なFat Model(属性やメソッドが単純にたくさん定義されたModel)にするのではなく、抽象モデルのMix-inクラスを作成しそれを継承することで、DRYを効率よく達成しようとしました(https://blog.kevinastone.com/django-model-behaviors)。このようなMix-inクラスうち、とりわけ汎用性が高いのはcoreディレクトリに、各アプリに依存性が高いMix-inクラスは各アプリで書くようにしました。

### アプリケーションの概要
本アプリケーションでは、会員登録後に、本の登録（OpenBDのAPIから本の情報を取得）、ある本についてのレビューの作成、ユーザーフォローと「いいね」（Axiosを用いた非同期通信）ができ、フォローしたユーザの活動（誰をフォローしたか、どのレビューをいいねしたか）も確認できます。レビューを作成する場合には次の本を指定し推薦文を書くことが必須となっており、こうすることで次に何を読めばいいのかという問題を解消しようと努めました。

本の登録
![本の登録](picture_for_readme/ajax_book_create.gif)

ユーザーフォロー
![ユーザーフォロー](picture_for_readme/ajax_user_follow.gif)

いいね
![いいね](picture_for_readme/ajax_review_like.gif)

フォローしてるユーザーの活動
![フォローしてるユーザーの活動](picture_for_readme/action.gif)

### 各アプリの機能や工夫したところ
### 参考にした書籍や記事

- Vincent, Williams S. , "Django for Beginners"
- Vincent, Williams S. , "Django for Professionals"
- Greenfield, Daniel Roy, and Greenfield, Audrey Roy, "Two Scoops of Django 1.11"


  
## 反省、参考文献、今後の展望










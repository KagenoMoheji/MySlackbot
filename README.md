# MySlackbot
個人学習用のSlackbot．（テスト）機能をどんどん追加していく．

## 動作環境
- Python3.6.6
- Heroku
- GoogleChrome-headless/chromedriver
- Dialogflow

## 機能
### 1．デフォルトリプライ
- 予期しないメンションがあった場合に，デフォルトのリプライを送りつつhelpマニュアルを記載する．
### 2．固定リプライ
- 「元気？」というメンションに対し，固定のリプライを送る．
- 「help」というメンションに対し，helpマニュアルを記載したリプライをする．
### 3．コマンド風入力
- 「＊＊」で囲んで指定の入力をすると，コマンド風に処理がなされる．
##### 3-1． [おうむ/おうむ返し/repeat/Repeat]
- ＊＊コマンドの後に記述したメンション内容をオウム返しでリプライする．
##### 3-2． [天気]
- ＊＊コマンドの後に「時期(今日/明日/明後日)・地域」と入力して，その天気情報をリプライする．
- 地域コードの取得はSelenium & chromedriverによるスクレイピングを以下で使用．  
[1次細分区定義表](http://weather.livedoor.com/forecast/rss/primary_area.xml)
##### 3-3.　[apiai/APIAI/Dialogflow/dialogflow/API.AI/DIALOGFLOW]
- Dialogflowと関連付けてのテスト実装．
- ＊＊コマンドの後に学習済みのテーマのキーワードを入力することでDialogflowからのレスポンスを取得しリプライする．
- 複数キーワードがレスポンスに必要な場合に「:+:」で対話botを超簡易で実現．
    - ただしDialogflow側でも「:+:」で連結した文字列を学習させておく必要がある．
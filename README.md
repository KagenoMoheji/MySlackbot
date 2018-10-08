# SlackWeatherBot
livedoorのWeather Hacksを用いて地域・時期を「コマンド風」入力してのリプライをするSlackBotの実装．

## 動作環境
- Python3.6.6
- Heroku
- GoogleChrome-headless/chromedriver

## 機能
### 1．デフォルトリプライ
- 予期しないメンションがあった場合に，デフォルトのリプライを送りつつhelpマニュアルを記載する．
### 2．固定リプライ
- 「元気？」というメンションに対し，固定のリプライを送る．
### 3．コマンド風入力
「＊＊」で囲んで指定の入力をすると，コマンド風に処理がなされる．
##### 3-1． [おうむ/おうむ返し/repeat/Repeat]
- ＊＊コマンドの後に記述したメンション内容をオウム返しでリプライする．
##### 3-2． [天気]
- ＊＊コマンドの後に「時期(今日/明日/明後日)・地域」と入力して，その天気情報をリプライする．
- 地域コードの取得はchromedriverによるスクレイピングを以下で使用．  
[1次細分区定義表](http://weather.livedoor.com/forecast/rss/primary_area.xml)

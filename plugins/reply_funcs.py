from slackbot.bot import respond_to, listen_to, default_reply
import re
from plugins.modules.weather_module import WeatherModule # 外部.py（モジュール）の読み込み

@default_reply()
def default(message):
    info="""[とりせつ]
    ```
    私は成長中です．いろんな機能を習得していきます．
    基本的に「@bot_cocogs」宛にメンションすれば動作します．
    
    （1）以下メンションを入力すると機能します．
    ●help
    - とりせつを表示します．
    ●元気？/How are you?
    - 固定リプライを送ります．
    
    （2）「＊＊」の間に以下コマンドを入力し，メンション本文を入力すると機能します．
    ●おうむ/おうむ返し/repeat/Repeat
    - メンション例
        @bot_cocogs
        ＊おうむ＊
        おうむ返しして
    - メンション本文をおうむ返しします．
    ●天気/weather
    - メンション例
        @bot_cocogs
        ＊天気＊
        今日・北海道
    - 指定した「時期（今日，明日，明後日）・地域名」の天気をリプライします．
    ```
    """
    message.reply("申し訳ございません．対応するメッセージが見つかりませんでした．\n\n" + info)

@respond_to("元気？")
@respond_to("How are you?")
def fixed_reply(message):
    message.reply("\n[固定(Fixed)]\nあぁ，元気です．\nWell, I'm fine, thanks.")


@respond_to("help")
def help(message):
    info="""[とりせつ]
    ```
    私は成長中です．いろんな機能を習得していきます．
    基本的に「@bot_cocogs」宛にメンションすれば動作します．
    
    （1）以下メンションを入力すると機能します．
    ●help
    - とりせつを表示します．
    ●元気？/How are you?
    - 固定リプライを送ります．
    
    （2）「＊＊」の間に以下コマンドを入力し，メンション本文を入力すると機能します．
    ●おうむ/おうむ返し/repeat/Repeat
    - メンション例
        @bot_cocogs
        ＊おうむ＊
        おうむ返しして
    - メンション本文をおうむ返しします．
    ●天気/weather
    - メンション例
        @bot_cocogs
        ＊天気＊
        今日・東京
    - 指定した「時期（今日/明日/明後日）・地域名」の天気をリプライします．
    ```
    """
    message.send(info)




'''
===========================================================================
コマンド風実装
「＊＊」で囲まれた文字列を含む文字列の場合にここで処理．
===========================================================================
'''
@respond_to(u"＊.+＊")
def starcmd_reply(message):
    text=message.body["text"] # メンション内容全文取得
    reply_type=re.search(r"＊(.+)＊", text) # メンション内容からメンションの種類判別子（＊＊で囲まれた部分）を取得
    if reply_type:
        reply_type=reply_type.group(1)
        text=re.sub(r"＊(.+)＊", "", text) # メンション本文を取得
        
        if reply_type in {"おうむ","おうむ返し","repeat","Repeat"}:
            message.send("\n[おうむ返し(Repeat)]\n```{0}```".format(text))
        elif reply_type in {"天気", "weather"}:
            wm = WeatherModule(text)
            if wm.getWeatherInfo() != 0:
                message.reply(str(wm.getWeatherInfo()))
            else:
                message.reply("\n入力した地域名の天気情報を取得できませんでした．\n再度別の地域名でお試しください．")
        else:
            message.send("\n＊＊コマンドを認識できませんでした．")
    else:
        message.send("")


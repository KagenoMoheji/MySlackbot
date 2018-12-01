from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json

class WeatherModule():
    '''
    天気情報取得モジュール
    参考：https://qiita.com/usomaru/items/529b6f40902ee1eda125
    '''
    def __init__(self):
        '''
        [引数]
        なし
        [処理]
        ●グローバル変数の定義
        ●以下リンクから地域名と地域コードの組み合わせをすべてスクレイピングで取得する．
        http://weather.livedoor.com/forecast/rss/primary_area.xml
        [戻り値]
        なし
        '''
        # グローバル変数の定義
        self.when = ""
        self.cityName = ""
        self.where = ""
        self.cityDict = {}

        url="http://weather.livedoor.com/forecast/rss/primary_area.xml"
        # ChromeDriverの用意
        options = Options()
        #options.binary_location = "/app/.apt/usr/bin/google-chrome" # Heroku対応？
        options.add_argument("--disable-gpu") # Heroku対応？
        options.add_argument("--no-sandbox") # Heroku対応？
        #options.add_argument("--disable-dev-shm-usage") # Heroku対応？
        options.add_argument("--headless") # ブラウザ非表示
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(10) # 指定タグが見つかるまでの待ち時間
        
        # スクレイピング
        driver.get(url)
        cityNameTags = driver.find_elements_by_css_selector(
            "#collapsible4 .expanded\
             .collapsible-content\
             .collapsible .expanded\
             .collapsible-content\
             .line:nth-child(3)\
             .html-attribute:nth-child(1)\
             .html-attribute-value"
            )
        cityCodeTags = driver.find_elements_by_css_selector(
            "#collapsible4 .expanded\
             .collapsible-content\
             .collapsible .expanded\
             .collapsible-content\
             .line:nth-child(3)\
             .html-attribute:nth-child(2)\
             .html-attribute-value"
            )

        # タグ内のテキストを取得し辞書にまとめる
        self.cityDict = {cityNameTag.text:cityCodeTag.text for cityNameTag,cityCodeTag in zip(cityNameTags,cityCodeTags)}
        #print(self.cityDict)
        
        # ドライバを閉じる
        driver.quit()
    
    def arrangeInput(self, text):
        '''
        [引数]
        ●text：メンション本文
        [処理]
        ●メンション本文を分割して「時期」「地域(コード)」を取得する．
        [戻り値]
        なし
        '''
        text_arr = text.split("・")
        self.when = text_arr[0].replace("\n","")
        self.cityName = text_arr[1]
        self.where = self.getCityCode(self.cityName)
    
    def getCityCode(self, cityName):
        '''
        [引数]
        ●cityName：メンション本文から取得した地域
        [処理]
        ●地域名から，以下リンクに基づき地域コードを取得する．
        http://weather.livedoor.com/forecast/rss/primary_area.xml
        [戻り値]
        ●地域名に対応する地域コード．
        ●該当する地域コードがなかった場合-1を返す．
        '''
        # 入力の地域名に一致するキーがcityDictに存在したら地域コードを返す
        if cityName in self.cityDict:
            return self.cityDict[cityName]
        else:
            return -1
    
    def getWeatherInfo(self):
        '''
        [引数]
        なし
        [処理]
        ●入力の時期・地域(コード)から出力を求め，リプライ文を生成して返す．
        [戻り値]
        ●生成したリプライ文
        [参考]
        http://weather.livedoor.com/weather_hacks/webservice
        https://algorithm.joho.info/programming/python/weather-py/
        http://tarao-mendo.blogspot.com/2018/03/python-requests-weather-api.html
        http://rongonxp.hatenablog.jp/entry/2017/10/05/230320
        '''
        # livedoorお天気webサービスのリンクを格納
        url = "http://weather.livedoor.com/forecast/webservice/json/v1"
        
        # urlパラメータとしての地域の指定
        payload = {"city": self.where}

        try:
            # お天気webサービスからの結果をjson形式で取得．
            data = requests.get(url, params = payload).json()
            #print(data)

            # 入力に対する出力の天気情報を抽出
            for datum in data["forecasts"]:
                if datum["dateLabel"].replace("\n","") == self.when: # 改行が入っている場合があるので除去
                    weather = datum["telop"]
                    break
        except:
            return -1 # 検索都市が登録されていなかったら-1を返して例外処理
        
        # 入力に対する回答を生成
        reply = "\n[天気]\n```{0}における{1}の天気 ： {2}```".format(self.cityName, self.when, weather)
        return reply
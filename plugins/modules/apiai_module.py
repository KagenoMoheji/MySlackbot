import os, uuid, json
import apiai

class ApiaiModule():
    '''
    [参考]
    https://qiita.com/flatfisher/items/53923e33ce1f23b3820a
    https://qiita.com/nagase/items/67d334d8d59df5ce28eb
    '''
    def __init__(self):
        '''
        [引数]
        なし
        [戻り値]
        なし
        '''
        self.CLIENT_ACCESS_TOKEN = os.environ["DF_CLIENT_ACCESS_TOKEN"]
        self.user_responses = "" # ユーザからの回答一覧．リストではなく「:+:」でつなぐものとして簡易に実装．

    def getResponse(self, text):
        '''
        [引数]
        ●text：メンチョン本文
        [戻り値]
        ●Dialogflowから渡されたリプライ文
        '''
        ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)

        request = ai.text_request()
        request.lang = "ja"
        request.session_id = str(uuid.uuid4()) #DialogFlow間のセッションIDをランダムなUUID型でセット
        
        self.user_responses += ":+:[{0}]".format(text) # ユーザレスポンスを加えていく
        request.query = self.user_responses

        response = request.getresponse()
        # https://techacademy.jp/magazine/18987
        json_res = json.loads(response.read().decode()) # 標準出力はsjis？なので文字コードの変換を行い，JSONに変換．
        print(json_res)

        if not json_res["result"]["actionIncomplete"]: # レスポンスが完全なものだったらユーザレスポンスをクリア．
            self.user_responses = ""

        return json_res["result"]["fulfillment"]["speech"]
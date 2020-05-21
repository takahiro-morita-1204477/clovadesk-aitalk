# coding: utf-8

from flask import Flask, request, jsonify
import os, random
import cek
import pya3rt

import requests
import json
import types

#A3RT
apikey = "DZZ5WVUNn4GIYHZFe1lTJRXZgRQawm83"

#CotoGoto
ENDPOINT = 'https://www.cotogoto.ai/webapi/noby.json'
MY_KEY = '6cc2adb8f63f85adc3572a10cd8fd0ec'

app = Flask(__name__)

clova = cek.Clova(
    application_id="com.example.tutorial.test3",
    default_language="ja",
    debug_mode=True)

@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    app.logger.info('Lambda function invoked index()')
    return 'hello from Flask!'

# /clova に対してのPOSTリクエストを受け付けるサーバーを立てる
@app.route('/clova', methods=['POST'])
def my_service():
    print(request.headers)
    body_dict = clova.route(body=request.data, header=request.headers)
    response = jsonify(body_dict)
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response

# 起動時の処理
@clova.handle.launch
def launch_request_handler(clova_request):
    open_message = "会話のテーマを教えてください"
    welcome_japanese = cek.Message(message=open_message, language="ja")
    response = clova.response([welcome_japanese])
    return response


# callAITalkが解析されたら実行
@clova.handle.intent("callAITalk")
def number_handler(clova_request):
    app.logger.info("Intent started")
    talk_theme = clova_request.slot_value("TalkTheme")
    app.logger.info(talk_theme)
    message_list = []
    for i in range(2):
        app.logger.info(i)
        app.logger.info("A3RT")
        response = a3rtclient.talk(talk_theme)
        talk_theme = response['results'][0]['reply']
        app.logger.info(talk_theme)
        message = cek.Message(message=talk_theme, language="ja")
        message_list.append(message)
        app.logger.info("CotoGoto")
        response = CotoGoto(talk_theme)
        talk_theme = response['text']
        app.logger.info(talk_theme) 
        message = cek.Message(message=talk_theme, language="ja")
        message_list.append(message)
    response = clova.response(message_list)
    """
    #A3RT
    a3rt_response = a3rtclient.talk(talk_theme)
    a3rt_message = a3rt_response['results'][0]['reply']
    app.logger.info(a3rt_message)
    #CotoGoto
    cotogoto_response = CotoGoto(a3rt_message)
    cotogoto_message = cotogoto_response['text']
    app.logger.info(cotogoto_message)
    message1 = cek.Message(message=a3rt_message, language="ja")
    message2 = cek.Message(message=cotogoto_message, language="ja")
    response = clova.response([message1,message2])
    """
    return response


# 終了時
@clova.handle.end
def end_handler(clova_request):
    # Session ended, this handler can be used to clean up
    app.logger.info("Session ended.")

# 認識できなかった場合
@clova.handle.default
def default_handler(request):
    return clova.response("Sorry I don't understand! Could you please repeat?")


def CotoGoto(word):
    payload = {'text': word, 'app_key': MY_KEY}
    r = requests.get(ENDPOINT, params=payload)
    data = r.json()
    return data

if __name__ == '__main__':
    a3rtclient = pya3rt.TalkClient(apikey)
    port = int(os.getenv("PORT", 5000))
    app.debug = True
    app.run(host="0.0.0.0", port=port)

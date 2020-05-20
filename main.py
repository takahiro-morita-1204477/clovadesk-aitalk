# coding: utf-8

from flask import Flask, request, jsonify
import os, random
import cek
import pya3rt

apikey = "DZZ5WVUNn4GIYHZFe1lTJRXZgRQawm83"

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
    open_message = "知りたい情報を教えてください"
    welcome_japanese = cek.Message(message=open_message, language="ja")
    response = clova.response([welcome_japanese])
    return response


# callAITalkが解析されたら実行
@clova.handle.intent("callAITalk")
def number_handler(clova_request):
    app.logger.info("Intent started")
    response = a3rtclient.talk("おはよう")
    app.logger.info(response['results'][0]['reply'])
    message_japanese = cek.Message(message=response['results'][0]['reply'], language="ja")
    response = clova.response([message_japanese])
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


if __name__ == '__main__':
    a3rtclient = pya3rt.TalkClient(apikey)
    port = int(os.getenv("PORT", 5000))
    app.debug = True
    app.run(host="0.0.0.0", port=port)

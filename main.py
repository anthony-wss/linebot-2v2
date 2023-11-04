from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = 'oYBe6ayOXKvD/VDqzraDroLR/2oibv9G91D/ZRvZlawE4anIl5x+y0xUzoY6iXMszZxGQHiZECCct8hzcL+YhD067JjyFrear7hEsXrcVMDBgUNeP5kcpq705LB8sTdr9mB2uOFOHNkSsrZTqDf7SAdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '229a3440f2e76fd4debc1e06f07494af'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6yXgl6EnoTGjHNGDO+E1JWCaAEmTGoplRL2qqEjKarnudNegs23ZSdH+af04NYY0PHdjZJrmuqqpOEWOYIfQJAJ8UetTLJA7E9sGYnRc5d3mB5yJaFCuoO40NtQfDbOsrILUtKAZ08PZTg2VYYf0BQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6eb39b7b1dac0a77aba60dbca241383b')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '你說什麼？'
    if msg == '我愛老公':
        s = '老公也愛你'
        sticker_message = StickerSendMessage(
        package_id='11537',
        sticker_id='54002737'
        )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s)
        )


if __name__ == "__main__":
    app.run()
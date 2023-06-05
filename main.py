import os
import re
from lib import wrtn, db

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


# APP 생성
db.init()
app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")
assert app_token and bot_token, "토큰을 등록해주세요."
app = App(token=bot_token)


@app.event("message")
def handle_message_events(event, client, message, say):
    try:
        text = message.get("text")
        # 설정값 저장
        if re.match(r"(\w+)=(\w+)", text):
            key, value = text.split("=", 1)
            db.store_config(key, value)
            say(f"👉 key : {key}\n👉 value : {value}\n설정 값이 저장되었습니다👍")
            return
        say("작성중입니다🙏")
        resp = "".join([i for i in wrtn.conversation(text, "GPT3.5")])
        resp = resp.replace("\\n", "\n")
        resp = resp.replace("\\t", "\t")
        resp = resp.replace('\\"', '"')
        resp = resp.replace("\\'", "'")
        say(resp)
    except AssertionError as ex:
        if str(ex) == "101001":
            say("토큰이 만료되었습니다.\n('authorization_token' 또는 'refresh_token')토큰을 다시 발급받아주세요.")
        elif str(ex) == "101002":
            say("채팅 방이 존재하지 않습니다.\n'room_id'를 다시 저장해주세요.")
        else:
            say(f"답변 작성간 오류가 발생하였습니다😂\n오류 내용 : {ex}")
    except Exception as ex:
        say(f"답변 작성간 알 수 없는 오류가 발생하였습니다😂\n오류 내용 : {ex}")


if __name__ == '__main__':
    SocketModeHandler(app, app_token).start()

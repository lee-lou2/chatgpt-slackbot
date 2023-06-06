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
        if text == "도움말":
            say("👉 `refresh_token=<REFRESH_TOKEN>` : 토큰 지정\n👉 `model=<GPT3.5 or GPT4>` : 모델 지정\n👉 그 외 : `GPT` 답변")
            return
        # 설정값 저장
        if re.match(r"(\w+)=(\w+)", text):
            key, value = text.split("=", 1)
            db.store_config(key, value)
            say(f"👉 key : {key}\n👉 value : {value}\n설정 값이 저장되었습니다👍")
            return
        say("작성중입니다🙏")
        resp = "".join([i for i in wrtn.conversation(text)])
        resp = resp.replace("\\n", "\n")
        resp = resp.replace("\\t", "\t")
        resp = resp.replace('\\"', '"')
        resp = resp.replace("\\'", "'")
        say(resp)
    except AssertionError as ex:
        if str(ex) == "101001":
            say("토큰이 만료되었습니다.\n`refresh_token` 토큰을 다시 발급은 후\n`refresh_token=<TOKEN>`을 입력해주세요.")
        elif str(ex) == "101002":
            say("채팅 방이 존재하지 않습니다.\n'room_id'를 제거 후 초기화하였습니다. 다시 시도해주세요.")
        elif str(ex) == "101003":
            say("답변 작성간 오류가 발생하였습니다.")
        elif str(ex) == "101004":
            say("대화방 생성간 오류가 발생하였습니다.")
        elif str(ex) == "101005":
            say("대화방 조회간 오류가 발생하였습니다.")
        else:
            say(f"답변 작성간 오류가 발생하였습니다😂\n오류 내용 : {ex}")
    except Exception as ex:
        say(f"답변 작성간 알 수 없는 오류가 발생하였습니다😂\n오류 내용 : {ex}")


if __name__ == '__main__':
    SocketModeHandler(app, app_token).start()

import re
import requests

from . import db


def _refresh_tokens(refresh_token: str):
    """
    토큰 재발급
    response = {
        "result": "SUCCESS",
        "data": {
            "accessToken": "<TOKEN>"
        },
    }
    """
    url = "https://api.wow.wrtn.ai/auth/refresh"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Refresh": refresh_token,
    }
    resp = requests.post(url, headers=headers)
    assert resp.status_code == 201, 101001
    data = resp.json()
    return data.get("data").get("accessToken")
  

def _get_access_token():
    """토큰 조회"""
    refresh_token = db.fetch_config("refresh_token")
    # 1. 리프레스 토큰이 없는 경우
    assert refresh_token, 101001
    access_token = _refresh_tokens(refresh_token)
    # 2. 리프레스 토큰이 만료된 경우
    assert access_token, 101001
    return access_token

def _create_room(access_token: str) -> str:
    """
    채팅방 생성
    response = {
        "result": "SUCCESS",
        "data": {
            "userId": "<USER_ID>",
            "isDeleted": false,
            "version": "1.2.0",
            "_id": "<ROOM_ID>",
            "createdAt": "<CREATED_AT>",
            "updatedAt": "<UPDATED_AT>",
            "__v": 0
        }
    }
    """
    url = "https://api.wow.wrtn.ai/chat"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    resp = requests.post(url, headers=headers)
    assert resp.status_code == 201, 101004
    return resp.json().get("data", {}).get("_id")


def _has_room(access_token: str, room_id: str) -> bool:
    """
    채팅방 존재 여부
    response = {
        "result": "SUCCESS",
        "data": [
            {
                "_id": "<ROOM_ID>",
                "userId": "<USER_ID>",
                "isDeleted": False,
                "version": "1.2.0",
                "createdAt": "<CREATED_AT>",
                "updatedAt": "<UPDATED_AT>",
                "__v": 0,
                "topic": "<TOPIC>",
            },
        ],
    }
    """
    url = "https://api.wow.wrtn.ai/chat"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200, 101005
    data = resp.json()
    for room in data.get("data", []):
        if room.get("_id") == room_id:
            return True
    db.delete_config("room_id")
    return False


def _generate(access_token: str, message: str, room_id: str, model: str = "GPT3.5"):
    """
    챗봇 대화 생성
    data: {}
    data: {"chunk":"Hello"}
    data: {"chunk":"!"}
    data: {}
    data: {"message":{"reroll":false,"dynamicChipList":["무엇을 도와드릴까요?","지금 시간이 얼마인가요?","당신이 어디서 왔나요?"],"_id":"647d2bf87178110265bbbf1c","chatId":"647d2a904c657fd37c6dda86","userId":"646b16ec7d42cb0fa56cca99","model":"GPT3.5","isDeleted":false,"role":"assistant","type":"DynamicChipOutput","content":"Hello! How can I assist you today?","liked":false,"disliked":false,"meta":{"platform":"web","williamRequestId":"83401ae0-3515-4f98-8711-f35cefe5a5a3","hamletRequestId":"830c7b54-6891-4800-bb96-43aa198a61d8"},"version":"1.2.4","createdAt":"2023-06-05T00:27:36.345Z","updatedAt":"2023-06-05T00:27:36.345Z","__v":0}}
    data: {"end":"[DONE]"}
    """
    url = f"https://william.wow.wrtn.ai/generate/stream2/{room_id}?type=big&model={model}&platform=web"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {"message": message, "reroll": False}
    resp = requests.post(url, headers=headers, json=payload)
    assert resp.status_code == 201, 101003
    for line in resp.iter_lines():
        if not line:
            continue
        decoded_line = line.decode("utf-8")
        pattern = r'data: {"chunk":"(.*?)"}'
        match = re.match(pattern, decoded_line)
        if not match:
            continue
        yield str(match.group(1))


def conversation(message: str, model: str = "GPT3.5"):
    """대화 생성"""
    access_token = _get_access_token()
    models = ["GPT3.5", "GPT4"]
    assert model in models, f"model은 {models} 중 하나여야 합니다."
    room_id = db.fetch_config("room_id")
    room_id = room_id if room_id is not None else _create_room(access_token)
    assert _has_room(access_token, room_id), 101002
    return _generate(access_token, message, room_id, model)

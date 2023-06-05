# 💬 무료 ChatGPT로 슬랙봇 생성

:::tip
뤼튼 API를 이용해 무료로 슬랙봇을 만들어보세요!
:::

## 1. 슬랙 APP 생성

### 1.1 슬랙 APP 선택

👉 **'From scratch'** 선택

![img](./img/1.png)

### 1.2 슬랙 APP 이름 설정

👉 **App Name** : 원하는 이름

👉 **Pick a workspace ...** : 생성을 희망하는 워크플로우 선택

👉 전체 입력 후 **'Create App'** 선택

![img](./img/2.png)

### 1.3 Socket Mode 켜기

👉 **Connect using Socket Mode** : **On**

👉 **Token** : 슬랩 앱 토큰(아래 코드에서 'SLACK_APP_TOKEN' 으로 사용)

![img](./img/10.png)
![img](./img/11.png)
![img](./img/12.png)

### 1.4 Event Subscriptions 설정

👉 **Enable Events** : On

👉 **Subscribe to bot events** : `message.channels` 추가

![img](./img/3.png)
![img](./img/4.png)

### 1.5 OAuth & Permissions 설정

👉 **Scopes** : `chat:write` 추가

👉 **Install to Workspace** : 클릭

![img](./img/5.png)
![img](./img/6.png)
![img](./img/7.png)

### 1.6 앱 설치 및 Bot Token 확인

👉 **Bot User OAuth Token** : 복사 (이 토큰이 아래에서 'SLACK_BOT_TOKEN' 으로 사용)

![img](./img/8.png)
![img](./img/9.png)


## 2. 슬랙 봇 지정

### 2.1 슬랙 실행

👉 슬랙 워크스페이스에 접속

### 2.2 채널 생성

![img](./img/13.png)

### 2.3 앱 추가

![img](./img/14.png)

## 3. 코드 가져오기

```bash
$ git clone https://github.com/lee-lou2/chatgpt-slackbot
```


## 4. 슬랙봇 실행 코드

```bash
$ pip install -r requirements.txt

$ export SLACK_APP_TOKEN="<위에서 저장한 코드>"
$ export SLACK_BOT_TOKEN="<위에서 저장한 코드>"

$ python main.py
```

## 5. 뤼튼 가입 및 토큰 조회

👉 [뤼튼 가입](https://wrtn.ai/)
👉 개발자 도구 켜기
👉 애플리케이션 > 쿠키 탭으로 이동
👉 검색창에 `refresh_token` 검색
👉 `refresh_token` 값 복사

![img](./img/15.png)

## 6. 뤼튼 토큰 설정

👉 생성된 슬랙 채널에서 `refresh_token=<복사된_토큰>` 입력하면 데이터베이스 자동으로 저장

## 7. 파이썬 애니웨어에 배포

👉 준비중
# YouTube 채널 모니터링 (yt-monitor)

3개 한국 경제/증시 YouTube 채널의 최근 24시간 영상을 탐색하고 요약합니다.

## 대상 채널

- **한경글로벌마켓** (`@hkglobalmarket`) — 미국 증시, 월가 분석
- **한국경제TV** (`@hkwowtv`) — 한국 경제/증권 종합 (자막 미제공)
- **증시각도기TV** (`@koreanstockrider`) — 미국/한국/중국 시황 분석

## 실행 절차

### 1단계: 최신 영상 탐색

각 채널의 RSS 피드를 `WebFetch`로 조회하여 최근 24시간 내 업로드된 영상 목록을 수집합니다.

- RSS URL: `https://www.youtube.com/feeds/videos.xml?channel_id=<CHANNEL_ID>`
- 채널 설정: `data/config.json` 참조

### 2단계: 자막 추출

`mcp__MAGIC-MEALKITS__youtube_transcript` 또는 `mmk youtube transcript` 명령어로
각 영상의 자막을 추출합니다.

- format: `text` (토큰 절약)
- preferred_lang: `ko`
- 한국경제TV는 자막 미제공이므로 제목 기반 요약만 수행

### 3단계: AI 요약

추출된 자막을 기반으로 각 영상의 핵심 내용을 요약합니다:

- 주요 시장 동향
- 핵심 종목/이슈
- 전문가 의견 및 전망
- 투자 시사점

### 4단계: Notion 저장 (선택)

Notion MCP 도구가 사용 가능한 경우 요약 결과를 Notion 페이지로 저장합니다.

### 5단계: Slack 알림 전송 (선택)

`SLACK_WEBHOOK_URL` 환경변수가 설정된 경우 요약 결과를 Slack 채널로 전송합니다.

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

### 6단계: 사용자 알림

PushNotification으로 모니터링 결과를 사용자에게 전달합니다.

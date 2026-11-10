# YouTube 채널 모니터링

## 개요
`data/config.json`에 등록된 YouTube 채널의 최근 영상을 탐색하고, 자막 추출 → AI 요약 → Notion 저장 → Slack 알림을 수행합니다.

## 절차

### 1. 채널별 최신 영상 탐색
- `data/config.json`의 각 채널 RSS 피드를 조회하여 최근 24시간 내 업로드된 영상 목록을 가져옵니다.
- Shorts(60초 이하 영상)는 건너뜁니다.

### 2. 자막 추출
- `mcp__MAGIC-MEALKITS__youtube_transcript` 도구 또는 `mmk youtube transcript` CLI로 자막을 추출합니다.
- 한국어(`ko`) 자막을 우선합니다.
- `text` 포맷으로 추출하여 토큰을 절약합니다.

### 3. AI 요약
- 추출된 자막을 기반으로 채널별 핵심 내용을 요약합니다.
- 요약 항목: 시장 동향, 주요 종목 언급, 투자 시사점

### 4. 결과 저장
- 요약 결과를 `data/reports/` 디렉토리에 날짜별 마크다운 파일로 저장합니다.
- Notion 도구가 사용 가능한 경우 Notion 페이지로도 저장합니다.

### 5. 알림 전송
- 환경변수 `SLACK_WEBHOOK_URL`이 설정된 경우 Slack 웹훅으로 요약을 전송합니다.
- PushNotification으로 사용자에게 완료 알림을 보냅니다.

## 필요 도구
- `mcp__MAGIC-MEALKITS__youtube_transcript` (MCP)
- `mcp__MAGIC-MEALKITS__youtube_metadata` (MCP)
- `WebFetch` (RSS 피드 조회)
- `Notion` MCP 도구 (선택)
- Slack Webhook (선택)

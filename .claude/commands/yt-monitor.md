# YouTube 채널 모니터링

## 개요
data/config.json에 등록된 YouTube 채널들의 최근 24시간 내 새 영상을 탐색하고,
자막 추출 → AI 요약 → Notion 저장 → Slack 알림을 수행합니다.

## 절차

### 1. 채널 스캔
- data/config.json에서 모니터링 대상 채널 목록을 로드합니다
- 각 채널의 최근 영상 목록을 가져옵니다
- 최근 24시간 이내 업로드된 영상만 필터링합니다

### 2. 자막 추출
- mmk youtube transcript 또는 MCP youtube_transcript 도구를 사용합니다
- 한국어(ko) 자막을 우선 추출합니다
- 자막이 없는 영상은 건너뜁니다

### 3. AI 요약
- 추출된 자막을 기반으로 핵심 내용을 요약합니다
- 요약 포맷:
  - 제목
  - 채널명
  - 핵심 포인트 (3-5개)
  - 시장 전망/투자 시사점
  - 영상 URL

### 4. Notion 저장
- Notion MCP 도구를 사용하여 요약 내용을 저장합니다
- 저장 실패 시 로컬 파일(data/summaries/)에 백업합니다

### 5. Slack 알림
- SLACK_WEBHOOK_URL 환경변수가 설정된 경우 알림을 전송합니다
- 미설정 시 건너뜁니다

### 6. 결과 보고
- 처리된 영상 수, 성공/실패 현황을 보고합니다
- PushNotification으로 결과를 알립니다

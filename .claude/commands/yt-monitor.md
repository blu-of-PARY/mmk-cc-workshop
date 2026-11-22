# YouTube 채널 모니터링

## 개요
data/config.json에 등록된 YouTube 채널의 최근 24시간 내 새 영상을 탐색하고,
자막 추출 → AI 요약 → Notion 저장 → Slack 알림 전송을 수행합니다.

## 대상 채널
- 한경글로벌마켓 (@hkglobalmarket)
- 한국경제TV (@hkwowtv)
- 증시각도기TV (@koreanstockrider)

## 실행 절차

### 1. 환경 확인
- `SLACK_WEBHOOK_URL` 환경변수 설정 확인
- `mmk` CLI 사용 가능 여부 확인
- Notion MCP 도구 접근 가능 여부 확인

### 2. 채널 RSS 피드 조회
각 채널의 RSS 피드를 조회하여 최근 24시간 이내 게시된 영상을 필터링합니다.
- RSS 피드 URL: `https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}`
- 금융/시장 관련 콘텐츠만 선별 (건강, 라이프스타일 등 비관련 콘텐츠 제외)

### 3. 자막 추출
`mcp__MAGIC-MEALKITS__youtube_transcript` 도구 사용:
- format: 'text' (토큰 절약)
- preferred_lang: 'ko'

### 4. AI 요약 생성
각 영상에 대해 다음 형식으로 요약:
- 핵심 요약 (3-5개 불릿포인트)
- 주요 키워드
- 시장 영향/시사점

### 5. Notion 저장
Notion MCP 도구를 사용하여 요약 페이지 생성

### 6. Slack 알림
`SLACK_WEBHOOK_URL`로 요약 결과 전송:
- 채널별 새 영상 수
- 주요 시장 이슈 요약
- Notion 페이지 링크

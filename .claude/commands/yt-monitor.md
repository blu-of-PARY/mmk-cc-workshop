# YouTube 채널 모니터링

data/config.json에 등록된 YouTube 채널들의 최근 24시간 내 새 영상을 탐색하고, 자막 추출 → AI 요약 → Notion 저장 → Slack 알림을 수행합니다.

## 절차

### 1. 채널 피드 확인
- `data/config.json`에서 채널 목록 로드
- 각 채널의 YouTube RSS 피드(`https://www.youtube.com/feeds/videos.xml?channel_id=<ID>`)를 WebFetch로 조회
- 최근 24시간 이내 업로드된 영상 필터링 (Shorts 제외, 2분 이상 영상만)

### 2. 자막 추출
- `mcp__MAGIC-MEALKITS__youtube_transcript` 도구로 각 영상의 자막 추출
- format: text, preferred_lang: ko

### 3. AI 요약
- 추출된 자막을 기반으로 3~5개 핵심 포인트 요약 (한국어)
- 시장 인사이트, 투자 시사점 정리

### 4. Notion 저장
- Notion MCP 도구를 사용하여 요약 페이지 생성
- 제목, 채널명, 영상 URL, 요약 내용 포함

### 5. Slack 알림
- SLACK_WEBHOOK_URL 환경변수 필요
- 채널별 새 영상 수와 핵심 요약을 Slack 메시지로 전송

## 모니터링 대상 채널

| 채널명 | 핸들 | 주요 콘텐츠 |
|--------|-------|-------------|
| 한경글로벌마켓 | @hkglobalmarket | 해외주식, 미국증시, 월가 브리핑 |
| 한국경제TV | @hkwowtv | 국내외 경제/증권 뉴스, 시황 분석 |
| 증시각도기TV | @koreanstockrider | 미국/한국 시황, 투자 전략 |

## 환경변수

- `SLACK_WEBHOOK_URL`: Slack Incoming Webhook URL (선택)
- `MMK_SERVER`: mmk CLI 서버 URL (필수)
- `MMK_TOKEN`: mmk CLI 인증 토큰 (필수)

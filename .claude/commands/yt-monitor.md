# YouTube 주식 채널 모니터링

한국 증시 유튜브 채널의 신규 영상을 수집하고, 자막을 추출하여 요약한 뒤 Notion과 Slack으로 전송한다.

## 절차

### 1단계: 영상 수집
`data/config.json`의 채널별 `channel_id`로 YouTube RSS 피드를 조회한다:
```
https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}
```
WebFetch 도구로 각 채널의 RSS를 병렬 조회하여 video_id, title, published 날짜를 추출한다.

### 2단계: 영상 필터링
- `filter.max_age_hours` 이내 영상만 선택 (기본 24시간)
- 채널별 `keywords`가 있으면 제목에 키워드 포함 영상만 선택 (빈 배열이면 전체 포함)
- `filter.exclude_keywords`에 해당하는 제목 제외
- YouTube Shorts URL (`/shorts/`) 제외
- 필터링 통과 영상이 0개이면 "새로운 영상이 없습니다" 보고 후 종료

### 3단계: 자막 추출
MCP 도구 `mcp__MAGIC-MEALKITS__youtube_transcript`로 각 영상의 한국어 자막을 추출한다.
- `format`: text (토큰 절약)
- `preferred_lang`: ko
- `with_metadata`: true (첫 조회 시)
- 자막 없는 영상은 "자막 없음 - 직접 시청 필요"로 기록

### 4단계: AI 요약
각 영상의 자막을 한국어로 요약한다:
- **핵심 내용**: 3~5개 불릿 포인트
- **언급된 종목/시장**: 관련 종목명, 지수
- **시장 전망**: 강세/약세/중립 판단 근거
- **리스크 요인**: 주의할 점
- 크로스 채널 테마 분석 추가

### 5단계: Notion 저장
`mcp__Notion__notion-create-pages`로 요약 리포트를 Notion 드래프트 페이지로 저장한다.

### 6단계: Slack 전송
환경변수 `SLACK_WEBHOOK_URL`이 설정되어 있으면 curl로 요약 메시지를 전송한다.
미설정이면 "Slack 미설정" 보고 후 건너뛴다.

### 7단계: 알림
PushNotification으로 처리 결과 요약을 전송한다.
- 수집 채널 수, 필터링 통과 영상 수
- 자막 추출 성공/실패 수
- 핵심 크로스 채널 테마 (1~2문장)
- Notion/Slack 전송 결과

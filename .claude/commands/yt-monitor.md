# YouTube 증시 채널 모니터링

data/config.json에 등록된 YouTube 채널들의 최근 24시간 내 새 영상을 탐색하고, 자막 추출 → AI 요약 → Notion 저장 → Slack 알림을 수행합니다.

## 절차

### 1. 채널 목록 로드
- `data/config.json`에서 채널 목록(channel_id, name, rss_feed) 읽기

### 2. 최근 영상 탐색
- 각 채널의 YouTube RSS 피드(`https://www.youtube.com/feeds/videos.xml?channel_id=<ID>`) 조회
- 최근 24시간 이내 게시된 영상 필터링
- Shorts 제외 (mmk youtube videotype으로 확인)

### 3. 자막 추출
- `mmk youtube transcript <url>` 명령으로 자막 추출
- 자막이 없는 영상(너무 최신이거나 자막 미지원)은 건너뛰기

### 4. AI 요약
- 추출된 자막을 기반으로 400~600자 한국어 요약 생성
- 핵심 포인트 3~5개 추출
- 관련 키워드 태깅 (반도체, 미국증시, 한국증시, AI, 실적, 유가 등)

### 5. Notion 저장
- Notion "증시 유튜브 모니터링" 데이터베이스에 저장
- data_source: `collection://c69360f0-25ec-4945-bc06-47e7d1648632`
- 필드: 제목, Video ID, URL, 게시일, 상태(처리완료), 요약, 채널, 키워드
- 중복 확인: Video ID로 기존 항목 검색 후 신규만 추가

### 6. Slack 알림
- 환경변수 `SLACK_WEBHOOK_URL`로 웹훅 전송
- 처리된 영상 수, 채널별 요약 포함

## 모니터링 대상 채널

| 채널명 | Channel ID | 핸들 |
|--------|-----------|------|
| 한경글로벌마켓 | UCWskYkV4c4S9D__rsfOl2JA | @한경글로벌마켓 |
| 한국경제TV | UCF8AeLlUbEpKju6v1H6p8Eg | @hkwowtv |
| 증시각도기TV | UCdOjVxkj5JA0iDu3_xcsTyQ | @koreanstockrider |

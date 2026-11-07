# YouTube 채널 모니터 (/yt-monitor)

data/config.json에 등록된 YouTube 채널들의 최근 24시간 내 새 영상을 탐색하고,
자막 추출 → AI 요약 → Notion 저장 → Slack 알림을 수행하는 자동화 명령입니다.

## 실행 절차

### 1단계: 환경 확인
- `MMK_TOKEN` 환경변수 확인 (YouTube 자막 추출용)
- `SLACK_WEBHOOK_URL` 환경변수 확인 (Slack 알림용)
- `data/config.json` 파일 로드

### 2단계: 채널별 최신 영상 탐색
각 채널에 대해:
1. YouTube 채널 페이지를 크롤링하여 최신 videoId 목록 수집
2. `mcp__MAGIC-MEALKITS__youtube_metadata`로 메타데이터 확인
3. 제목/날짜 기반으로 최근 24시간 내 영상 필터링

### 3단계: 자막 추출
- `mcp__MAGIC-MEALKITS__youtube_transcript` (format=text, preferred_lang=ko) 사용
- 자막 없는 영상은 제목/메타데이터 기반으로 요약

### 4단계: AI 요약 생성
각 영상별:
- 핵심 내용 3-5줄 요약
- 주요 수치/데이터 추출
- 시장 영향 분석

### 5단계: 리포트 생성
- `data/summaries/YYYY-MM-DD_report.md` 파일로 저장
- 종합 시장 판단 테이블 포함

### 6단계: Notion 저장 (선택)
- Notion MCP 도구를 사용하여 요약 페이지 생성

### 7단계: Slack 알림 (선택)
- `SLACK_WEBHOOK_URL`로 요약 메시지 전송
- 환경변수 미설정 시 스킵

### 8단계: Git 커밋 & 푸시
- 생성된 파일들을 커밋하고 지정 브랜치에 푸시

## 대상 채널
- 한경글로벌마켓 (@hkglobalmarket)
- 한국경제TV (@hkwowtv)
- 증시각도기TV (@koreanstockrider)

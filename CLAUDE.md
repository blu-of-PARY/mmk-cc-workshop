# Claude Code 워크샵 스타터

강의 실습용 Claude Code 워크샵 스타터 프로젝트입니다.

## 프로젝트 목적

이 프로젝트를 fork하여 Claude Code 웹에서 바로 자동화 바이브 코딩을 시작할 수 있습니다.

## mmk CLI

mmk (Magic Meal Kits)는 YouTube 자막 추출, 메타데이터 조회 등을 지원하는 CLI 도구입니다.

**중요: 현재 토큰은 YouTube 전용입니다. `mmk youtube` 명령어만 사용하세요.**
`mmk notion`, `mmk paymint` 등 다른 명령어는 권한이 없어 실패합니다 (403 insufficient_scope).

### 설정

```bash
export MMK_SERVER="https://magic-meal-kits-r7fpfharja-uw.a.run.app"
export MMK_TOKEN="<강사가 제공한 토큰>"
```

### 사용 가능한 명령어

```bash
# YouTube 자막 추출
mmk youtube transcript <youtube-url>
mmk youtube transcript <youtube-url> --format json
mmk youtube transcript <youtube-url> --format srt

# YouTube 메타데이터 조회
mmk youtube metadata <youtube-url>

# YouTube 영상 타입 확인 (일반 영상 vs Short)
mmk youtube videotype <youtube-url>
```

### 사용 불가 명령어 (토큰 권한 없음)

- `mmk notion ...` — 사용 불가
- `mmk paymint ...` — 사용 불가
- `mmk threads ...` — 사용 불가

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node, mmk 버전
- 원격 환경 여부

## 증시 유튜브 모니터링 시스템

한국 증시 유튜브 채널을 자동 모니터링하여 자막 추출 → AI 요약 → Slack 알림 → Notion 저장하는 시스템.

### 모니터링 대상 채널

| 채널 | 대상 콘텐츠 | 필터 키워드 |
|------|-----------|-----------|
| 한경글로벌마켓 | 빈난새의 개장전요것만, 김현석의 월스트리트나우 | `개장전요것만`, `월스트리트나우` |
| 한국경제TV | 당잠사 | `당잠사` |
| 증시각도기TV | 전체 | (필터 없음) |

### 스킬 목록

| 스킬 | 설명 |
|------|------|
| `/yt-setup` | 초기 설정 (Notion DB 생성, Slack 연결 테스트) |
| `/yt-discover` | RSS 피드로 새 영상 탐색 |
| `/yt-summarize <url>` | 영상 자막 추출 + AI 요약 |
| `/yt-notify-slack` | Slack 웹훅 알림 전송 |
| `/yt-save-notion` | Notion DB 저장 |
| `/yt-monitor` | 전체 파이프라인 오케스트레이터 |

### 사용법

```bash
# 1. 초기 설정 (최초 1회)
/yt-setup

# 2. 수동 테스트
/yt-discover
/yt-summarize https://www.youtube.com/watch?v=VIDEO_ID

# 3. 자동 실행 (1시간 간격)
/loop 1h /yt-monitor
```

### 환경변수

Slack 웹훅 URL은 환경변수로 설정해야 합니다:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 설정 파일

- `data/config.json` — 채널 목록, 필터, Notion DB ID
- `data/processed.json` — 처리 완료 영상 기록 (중복 방지)
- `.claude/scripts/parse-rss.py` — YouTube RSS XML 파서

### Notion DB 스키마

제목(Title), Video ID, 채널(Select), URL, 게시일(Date), 요약, 키워드(Multi-select), 상태(Select)

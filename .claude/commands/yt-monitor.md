# YouTube 증시 모니터링 — 메인 오케스트레이터

한국 증시 유튜브 채널을 모니터링하여 새 영상 발견 → 자막 추출 → AI 요약 → Notion 저장 → Slack 알림 파이프라인을 실행합니다.

---

## Step 1: 설정 및 상태 로드

다음 파일들을 읽으세요:
- `data/config.json` — 채널 목록, 필터 설정, Notion ID
- `data/processed.json` — 이미 처리된 영상 목록
- 환경변수 `$SLACK_WEBHOOK_URL` — Slack 웹훅 URL (Bash에서 `echo $SLACK_WEBHOOK_URL`로 확인)

`config.json`의 `notion.data_source_id`가 비어있으면 "먼저 `/yt-setup`을 실행하세요"라고 안내하고 종료하세요.
`$SLACK_WEBHOOK_URL` 환경변수가 비어있으면 Slack 알림을 건너뛰세요.

## Step 2: RSS 피드 수집 및 파싱

`config.json`의 각 채널에 대해 RSS 피드를 수집하세요:

```bash
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>" | python3 .claude/scripts/parse-rss.py "<channel_name>"
```

각 채널의 결과를 하나의 영상 목록으로 합치세요.

## Step 3: 필터링

각 영상에 대해 순서대로 필터를 적용하세요:

1. **중복 제외**: `processed.json`의 `processed_videos`에 `videoId`가 있으면 스킵
2. **시간 필터**: 영상의 `publishedAt`이 현재 시각으로부터 `config.filter.max_age_hours`(기본 24시간) 이내인 것만 통과
3. **키워드 필터**: 채널의 `title_keywords`가 비어있지 않으면(`[]`이 아니면), 영상 제목에 키워드 중 하나라도 포함되어야 통과. `title_keywords`가 `[]`(빈 배열)이면 해당 채널의 모든 영상 통과.
4. **Shorts 제외** (빠른 방식): URL에 `/shorts/`가 포함되어 있으면 바로 스킵. URL로 판단 불가한 경우에만 `youtube_video_type` MCP 도구 사용.
5. **LIVE/편집본 중복 제거**: 같은 채널에서 제목이 80% 이상 유사한 영상이 2개 이상이면 `[LIVE`가 포함되지 않은 편집본만 처리 (LIVE 버전 스킵). 둘 다 LIVE가 아니면 최신 것만 처리.

## Step 4: 새 영상 처리

필터를 통과한 각 영상에 대해 다음을 수행하세요.

### 4-1. 자막 추출

`youtube_transcript` MCP 도구를 호출하세요:
- video_url: 영상 URL
- format: `text`
- preferred_lang: `ko`
- with_metadata: false

자막이 없으면 `youtube_metadata` MCP 도구로 메타데이터만 가져와서 간단 요약을 생성하세요.

### 4-2. AI 요약 생성

자막 내용을 **간결하게** 분석하세요:

- **핵심 요약**: 2~3문장
- **주요 포인트**: 3~5개 bullet
- **언급 종목/섹터**: 있으면 나열 (없으면 생략)
- **키워드**: 3~5개 (Notion DB에 등록된 키워드 중 선택: 휴전, 유가, 호르무즈해협, 금리인하, 공매도청산, 반도체, 삼성전자, 미국증시, 한국증시, 인플레이션, 에너지, 이란전쟁, AI, 실적, 환율)

### 4-3. Notion 일괄 저장

**모든 영상의 요약을 먼저 생성한 뒤**, `notion-create-pages` MCP를 **한 번만** 호출하여 일괄 저장하세요:

```json
{
  "parent": {
    "type": "data_source_id",
    "data_source_id": "<config의 notion.data_source_id>"
  },
  "pages": [
    {
      "properties": {
        "제목": "<영상 제목>",
        "Video ID": "<videoId>",
        "채널": "<채널명>",
        "userDefined:URL": "<영상 URL>",
        "date:게시일:start": "<YYYY-MM-DD>",
        "요약": "<핵심 요약 2~3문장>",
        "키워드": "[\"키워드1\", \"키워드2\"]",
        "상태": "처리완료"
      },
      "content": "## 핵심 요약\n<요약>\n\n## 주요 포인트\n<bullets>\n\n## 언급 종목/섹터\n<리스트>"
    }
  ]
}
```

**주의**: 페이지 content에 원본 자막 전문을 포함하지 마세요 (너무 길어서 불필요).

### 4-4. Slack 알림

모든 영상의 요약을 **하나의 메시지로 통합**하여 전송하세요:

```markdown
*증시 유튜브 모니터링 요약*
_<현재 날짜>_

---

*1. [채널명] 영상 제목*
<링크>
<핵심 요약 2~3문장>
• 포인트 1
• 포인트 2

---

*2. [채널명] 영상 제목*
...
```

1. `slack_convert_markdown` MCP 도구로 Block Kit JSON 변환
2. curl로 `$SLACK_WEBHOOK_URL`에 POST

**영상이 많으면 Slack 메시지 길이 제한(3000자)에 주의하세요. 초과 시 2개 메시지로 나눠 전송.**

### 4-5. 상태 업데이트

처리된 모든 영상을 `data/processed.json`에 한번에 업데이트하세요.

## Step 5: 실행 결과 보고

```
[YT 증시 모니터] 실행 완료
- 채널 수: 3개
- 발견 영상: N개
- 필터 통과: M개
- 처리 완료: M개
- 처리된 영상:
  1. [채널명] 영상 제목
  2. [채널명] 영상 제목
```

새 영상이 없으면:
```
[YT 증시 모니터] 새 영상 없음
```

## 오류 처리

- 개별 영상 자막 추출 실패 → 해당 영상 건너뛰고 다음 처리
- Slack 전송 실패 → Notion 저장은 계속 진행
- RSS 수집 실패 → 해당 채널 건너뛰고 다음 채널 처리

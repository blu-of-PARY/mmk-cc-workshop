# YouTube 증시 모니터링 — 메인 오케스트레이터

이 스킬은 한국 증시 유튜브 채널을 모니터링하여 새 영상을 발견하고,
자막 추출 → AI 요약 → Notion 저장 → Slack 알림의 전체 파이프라인을 실행합니다.

**`/loop 1h /yt-monitor`로 매시간 자동 실행됩니다.**

---

## 전체 파이프라인

### Step 1: 설정 및 상태 로드

다음 파일들을 읽으세요:
- `data/config.json` — 채널 목록, 필터 설정, Notion ID
- `data/processed.json` — 이미 처리된 영상 목록
- 환경변수 `$SLACK_WEBHOOK_URL` — Slack 웹훅 URL (Bash에서 `echo $SLACK_WEBHOOK_URL`로 확인)

`config.json`의 `notion.data_source_id`가 비어있으면 "먼저 `/yt-setup`을 실행하세요"라고 안내하고 종료하세요.
`$SLACK_WEBHOOK_URL` 환경변수가 비어있으면 Slack 알림을 건너뛰세요.

### Step 2: RSS 피드 수집 및 파싱

`config.json`의 각 채널에 대해 RSS 피드를 수집하세요:

```bash
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>" | python3 .claude/scripts/parse-rss.py "<channel_name>"
```

각 채널의 결과를 하나의 영상 목록으로 합치세요.

### Step 3: 필터링

각 영상에 대해 순서대로 필터를 적용하세요:

1. **중복 제외**: `processed.json`의 `processed_videos`에 `videoId`가 있으면 스킵
2. **시간 필터**: 영상의 `publishedAt`이 현재 시각으로부터 `config.filter.max_age_hours`(기본 24시간) 이내인 것만 통과
3. **키워드 필터**: 채널의 `title_keywords`가 비어있지 않으면(`[]`이 아니면), 영상 제목에 키워드 중 하나라도 포함되어야 통과. `title_keywords`가 `[]`(빈 배열)이면 해당 채널의 모든 영상 통과.
4. **Shorts 제외**: `config.filter.skip_shorts`가 true이면, `youtube_video_type` MCP 도구로 확인하여 Short인 영상 스킵

**중요**: Shorts 체크는 API 호출이 필요하므로 다른 필터를 먼저 적용하여 후보를 줄인 뒤 마지막에 수행하세요.

### Step 4: 새 영상 처리

필터를 통과한 각 영상에 대해 다음을 수행하세요:

#### 4-1. 자막 추출

`youtube_transcript` MCP 도구를 호출하세요:
- video_url: 영상 URL
- format: `text`
- preferred_lang: `ko`
- with_metadata: false

자막이 없으면 `youtube_metadata` MCP 도구로 메타데이터만 가져와서 간단 요약을 생성하세요.

#### 4-2. AI 요약 생성

자막 내용을 분석하여 다음을 생성하세요:

- **핵심 요약**: 2~3문장으로 영상 핵심 내용
- **주요 포인트**: bullet list로 핵심 포인트 3~5개
- **언급 종목/섹터**: 영상에서 언급된 주식 종목이나 섹터 (없으면 생략)
- **키워드**: 핵심 키워드 3~5개

#### 4-3. Notion 저장

`notion-create-pages` MCP 도구를 호출하세요:

```json
{
  "parent": {
    "type": "data_source_id",
    "data_source_id": "<config의 notion.data_source_id>"
  },
  "pages": [{
    "properties": {
      "제목": "<영상 제목>",
      "Video ID": "<videoId>",
      "채널": "<채널명>",
      "URL": "<영상 URL>",
      "게시일": "<YYYY-MM-DD>",
      "요약": "<핵심 요약 2~3문장>",
      "키워드": "<키워드1, 키워드2, ...>",
      "상태": "처리완료"
    },
    "content": "## 핵심 요약\n<요약 내용>\n\n## 주요 포인트\n<bullet list>\n\n## 언급 종목/섹터\n<종목 리스트>\n\n---\n\n## 원본 자막\n<자막 전문>"
  }]
}
```

#### 4-4. Slack 알림

Slack 알림용 마크다운을 구성하세요:

```markdown
*새 증시 영상 알림*

*채널:* <채널명>
*제목:* <영상 제목>
*링크:* <영상 URL>

*핵심 요약*
<2~3문장 요약>

*주요 포인트*
• 포인트 1
• 포인트 2
• 포인트 3

*키워드:* `키워드1` `키워드2` `키워드3`
```

1. `slack_convert_markdown` MCP 도구로 Block Kit JSON 변환
2. 변환된 blocks를 curl로 전송:

```bash
curl -X POST -H 'Content-Type: application/json' \
  --data '{"blocks": <blocks_json>}' \
  "$SLACK_WEBHOOK_URL"
```

#### 4-5. 상태 업데이트

`data/processed.json`을 읽어서 새 영상 정보를 추가한 뒤 파일에 다시 저장하세요:

```python
python3 -c "
import json, sys
with open('data/processed.json') as f:
    data = json.load(f)
data['processed_videos']['<videoId>'] = {
    'title': '<제목>',
    'channel': '<채널명>',
    'processed_at': '<현재 ISO 8601 시간>'
}
data['last_run'] = '<현재 ISO 8601 시간>'
with open('data/processed.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Updated processed.json')
"
```

**각 영상을 하나씩 완전히 처리(요약→Notion→Slack→상태 저장)한 뒤 다음 영상으로 넘어가세요.**

### Step 5: 실행 결과 보고

모니터링 결과를 간결하게 보고하세요:

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
[YT 증시 모니터] 새 영상 없음 (마지막 실행: <last_run 시간>)
```

---

## 오류 처리

- 개별 영상 처리 중 오류가 발생하면 해당 영상은 건너뛰고 다음 영상을 처리하세요.
- Slack 전송 실패 시 Notion 저장은 계속 진행하세요.
- RSS 피드 수집 실패 시 해당 채널은 건너뛰고 다음 채널을 처리하세요.
- 모든 오류는 최종 보고에 포함하세요.

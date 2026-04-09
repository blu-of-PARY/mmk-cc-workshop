# Notion 데이터베이스에 영상 정보 저장

이 스킬은 YouTube 영상 요약 정보를 Notion 데이터베이스에 저장합니다.

## 인자

이 스킬은 직접 호출보다는 `/yt-monitor` 오케스트레이터에서 사용됩니다.
테스트 시에는 `$ARGUMENTS`에 YouTube URL을 전달하세요.

## 수행 단계

### 1. 설정 로드

`data/config.json`에서 `notion.data_source_id`를 읽으세요.
비어있으면 먼저 `/yt-setup`을 실행하라고 안내하세요.

### 2. Notion 페이지 생성

`notion-create-pages` MCP 도구를 사용하여 페이지를 생성하세요:

**parent:**
```json
{
  "type": "data_source_id",
  "data_source_id": "<config에서 읽은 data_source_id>"
}
```

**pages:**
```json
[{
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
  "content": "<전체 요약 마크다운 내용>\n\n---\n\n## 원본 자막\n<자막 전문>"
}]
```

### 3. processed.json 업데이트

저장 성공 후 `data/processed.json`에 해당 영상을 추가하세요:

```json
{
  "processed_videos": {
    "<videoId>": {
      "title": "<영상 제목>",
      "channel": "<채널명>",
      "processed_at": "<ISO 8601 시간>",
      "notion_page_id": "<생성된 page_id>"
    }
  }
}
```

기존 내용을 유지하면서 새 항목만 추가합니다.

### 4. 결과 보고

저장 성공 여부와 Notion 페이지 URL을 보고하세요.

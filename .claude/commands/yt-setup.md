# YouTube 증시 모니터링 초기 설정

이 스킬은 YouTube 증시 모니터링 시스템의 초기 설정을 수행합니다.

## 수행 단계

### 1. 환경 검증

다음 항목을 확인하세요:
- `data/config.json` 파일이 존재하는지 확인
- `data/processed.json` 파일이 존재하는지 확인
- `.claude/scripts/parse-rss.py` 파일이 존재하는지 확인

### 2. Slack 웹훅 테스트

환경변수 `$SLACK_WEBHOOK_URL`을 확인하세요 (Bash에서 `echo $SLACK_WEBHOOK_URL`).
설정되어 있으면 테스트 메시지를 전송하세요:

```bash
curl -X POST -H 'Content-Type: application/json' \
  --data '{"text":"[YT 증시 모니터] 설정 완료! Slack 연결 테스트 성공."}' \
  "$SLACK_WEBHOOK_URL"
```

환경변수가 없으면 사용자에게 설정 방법을 안내하세요:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 3. Notion 데이터베이스 생성

`data/config.json`의 `notion.data_source_id`가 비어있으면, Notion에 새 데이터베이스를 생성하세요.

`notion-create-database` MCP 도구를 사용하여 아래 스키마로 생성:
- parent: `data/config.json`의 `notion.parent_page_id` 사용
- title: "증시 유튜브 모니터링"
- schema:
```sql
CREATE TABLE (
  "제목" TITLE,
  "Video ID" RICH_TEXT,
  "채널" SELECT('한경글로벌마켓':blue, '한국경제TV':green, '증시각도기TV':purple),
  "URL" URL,
  "게시일" DATE,
  "요약" RICH_TEXT,
  "키워드" MULTI_SELECT(),
  "상태" SELECT('처리완료':green, '오류':red)
)
```

생성 후 반환된 data_source_id를 `data/config.json`의 `notion.data_source_id`에 저장하세요.
database_id도 `notion.database_id`에 저장하세요.

### 4. RSS 피드 테스트

`data/config.json`의 채널 목록에서 첫 번째 채널로 RSS 피드를 테스트하세요:

```bash
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>" | python3 .claude/scripts/parse-rss.py "<channel_name>"
```

결과가 JSON 배열로 출력되면 성공입니다.

### 5. 결과 보고

설정 결과를 사용자에게 보고하세요:
- Slack 연결 상태
- Notion DB 생성/연결 상태 (database_id, data_source_id)
- RSS 피드 테스트 결과
- 모니터링 대상 채널 목록

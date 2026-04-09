# Slack 알림 전송

이 스킬은 YouTube 영상 요약을 Slack으로 전송합니다.

## 인자

`$ARGUMENTS` — 전송할 메시지 내용 (마크다운 형식) 또는 "test"(테스트 메시지 전송)

## 수행 단계

### 1. 설정 로드

환경변수 `$SLACK_WEBHOOK_URL`을 확인하세요 (Bash에서 `echo $SLACK_WEBHOOK_URL`).
환경변수가 비어있으면 경고 메시지를 출력하고 종료하세요.

### 2. 메시지 구성

인자가 "test"이면 테스트 메시지를 전송합니다:
```
[YT 증시 모니터] 테스트 알림입니다. 연결이 정상입니다.
```

그 외에는 전달받은 마크다운 내용을 사용합니다.

### 3. Block Kit 변환

`slack_convert_markdown` MCP 도구를 사용하여 마크다운을 Slack Block Kit JSON으로 변환하세요.

### 4. Slack 전송

변환된 Block Kit JSON을 curl로 웹훅 URL에 POST하세요:

```bash
curl -X POST -H 'Content-Type: application/json' \
  --data '{"blocks": <block_kit_json>}' \
  "$SLACK_WEBHOOK_URL"
```

응답이 "ok"이면 성공, 그 외에는 오류를 보고하세요.

### 5. 결과 보고

전송 성공/실패 여부를 사용자에게 알려주세요.

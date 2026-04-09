# YouTube 영상 자막 추출 및 요약

이 스킬은 YouTube 영상의 자막을 추출하고 AI 요약을 생성합니다.

## 인자

`$ARGUMENTS` — YouTube 영상 URL (예: https://www.youtube.com/watch?v=VIDEO_ID)

## 수행 단계

### 1. 메타데이터 조회

`youtube_metadata` MCP 도구를 사용하여 영상 메타데이터를 조회하세요:
- video_url: `$ARGUMENTS`
- 제목, 채널명, 게시일 등을 기록

### 2. 자막 추출

`youtube_transcript` MCP 도구를 사용하여 자막을 추출하세요:
- video_url: `$ARGUMENTS`
- format: `text` (토큰 절약을 위해)
- preferred_lang: `ko`
- with_metadata: false

자막이 없는 경우 (라이브 스트림 등), 메타데이터의 제목과 설명만으로 간단 요약을 생성하세요.

### 3. AI 요약 생성

추출한 자막을 분석하여 다음을 생성하세요:

**요약 형식:**

```
## 핵심 요약
2~3문장으로 영상의 핵심 내용을 요약합니다.

## 주요 포인트
- 포인트 1
- 포인트 2
- 포인트 3
(최대 5개)

## 언급된 종목/섹터
삼성전자, 반도체, 금리 등 (없으면 생략)

## 키워드
증시, 미국장, 금리 등 핵심 키워드 3~5개
```

### 4. 결과 출력

다음 정보를 구조화하여 출력하세요:
- 영상 제목
- 채널명
- 영상 URL
- 게시일
- 요약 전문
- 키워드 목록
- 언급 종목 목록

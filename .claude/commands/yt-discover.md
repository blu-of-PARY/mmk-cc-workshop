# YouTube 채널 새 영상 탐색

이 스킬은 설정된 YouTube 채널들의 RSS 피드를 조회하여 새 영상 목록을 가져옵니다.

## 수행 단계

### 1. 설정 로드

`data/config.json`을 읽어서 채널 목록과 필터 설정을 로드하세요.

### 2. RSS 피드 수집

각 채널에 대해 RSS 피드를 가져오세요:

```bash
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>" | python3 .claude/scripts/parse-rss.py "<channel_name>"
```

### 3. 필터링

`data/processed.json`을 읽어서 이미 처리된 영상을 확인하세요.

각 영상에 대해 다음 필터를 적용하세요:

1. **중복 제외**: `processed.json`의 `processed_videos`에 있는 videoId는 스킵
2. **Shorts 제외**: `config.filter.skip_shorts`가 true이면, `youtube_video_type` MCP 도구로 확인하여 Short인 영상은 스킵
3. **시간 필터**: `config.filter.max_age_hours` 이내에 게시된 영상만 포함
4. **키워드 필터**: 채널의 `title_keywords`가 비어있지 않으면, 영상 제목에 키워드 중 하나라도 포함된 영상만 선택. 비어있으면(`[]`) 해당 채널의 모든 영상 통과.

### 4. 결과 출력

필터를 통과한 새 영상 목록을 출력하세요:
- 채널명
- 영상 제목
- 영상 URL
- 게시일

총 발견된 영상 수와 필터 통과 영상 수를 함께 보고하세요.

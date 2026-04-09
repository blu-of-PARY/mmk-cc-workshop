#!/usr/bin/env python3
"""YouTube RSS XML 피드를 파싱하여 JSON으로 출력하는 스크립트.

Usage:
    curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID" | python3 parse-rss.py [channel_name]
"""

import json
import sys
import xml.etree.ElementTree as ET

NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def parse_feed(xml_text: str, channel_name: str = "") -> list[dict]:
    root = ET.fromstring(xml_text)
    entries = []

    for entry in root.findall("atom:entry", NAMESPACES):
        video_id = entry.find("yt:videoId", NAMESPACES)
        title = entry.find("atom:title", NAMESPACES)
        published = entry.find("atom:published", NAMESPACES)
        link = entry.find('atom:link[@rel="alternate"]', NAMESPACES)
        author = entry.find("atom:author/atom:name", NAMESPACES)

        if video_id is None or title is None:
            continue

        entries.append({
            "videoId": video_id.text,
            "title": title.text,
            "channelName": channel_name or (author.text if author is not None else ""),
            "publishedAt": published.text if published is not None else "",
            "url": link.get("href") if link is not None else f"https://www.youtube.com/watch?v={video_id.text}",
        })

    return entries


def main():
    xml_text = sys.stdin.read()
    channel_name = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        entries = parse_feed(xml_text, channel_name)
        print(json.dumps(entries, ensure_ascii=False, indent=2))
    except ET.ParseError as e:
        print(json.dumps({"error": f"XML parse error: {e}"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

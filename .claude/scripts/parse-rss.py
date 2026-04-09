#!/usr/bin/env python3
"""YouTube RSS XML 파서 — stdin으로 XML을 받아 JSON 배열을 stdout으로 출력."""

import sys
import json
import xml.etree.ElementTree as ET

def parse_feed(xml_text, channel_name=""):
    root = ET.fromstring(xml_text)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }

    entries = []
    for entry in root.findall("atom:entry", ns):
        video_id = entry.find("yt:videoId", ns)
        title = entry.find("atom:title", ns)
        published = entry.find("atom:published", ns)
        link = entry.find("atom:link", ns)

        if video_id is None or title is None:
            continue

        entries.append({
            "videoId": video_id.text,
            "title": title.text,
            "channelName": channel_name,
            "publishedAt": published.text if published is not None else "",
            "url": link.get("href", "") if link is not None else f"https://www.youtube.com/watch?v={video_id.text}",
        })

    return entries

if __name__ == "__main__":
    channel_name = sys.argv[1] if len(sys.argv) > 1 else ""
    xml_text = sys.stdin.read()
    try:
        entries = parse_feed(xml_text, channel_name)
        print(json.dumps(entries, ensure_ascii=False, indent=2))
    except ET.ParseError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

import requests
import json
import os
import time

POPULAR_URL = "https://api.bilibili.com/x/web-interface/popular"
VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
}


def get_video_tags(aid: int) -> list[str]:
    try:
        resp = requests.get(
            f"{VIDEO_INFO_URL}?aid={aid}",
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data["code"] != 0:
            return []
        tags = data.get("data", {}).get("tags", [])
        if isinstance(tags, list) and tags and isinstance(tags[0], dict):
            return [t["tag_name"] for t in tags]
        return tags
    except Exception:
        return []


def format_count(num: int) -> str:
    """格式化播放量"""
    if num >= 1_0000_0000:
        return f"{num/1_0000_0000:.1f}亿"
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return str(num)


def main():
    print("正在抓取B站热门视频 Top 10 ...\n")

    resp = requests.get(
        f"{POPULAR_URL}?ps=10&pn=1",
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    result = resp.json()

    if result["code"] != 0:
        print(f"API 返回错误: code={result['code']}, message={result.get('message')}")
        return

    items = result["data"]["list"]
    results = []

    for i, item in enumerate(items, 1):
        aid = item["aid"]
        bvid = item["bvid"]
        title = item["title"]
        up_name = item["owner"]["name"]
        view_count = item["stat"]["view"]
        category = item.get("tname", "未知")

        tags = get_video_tags(aid)
        time.sleep(0.5)

        print(f"{'='*60}")
        print(f"  No.{i}  {title}")
        print(f"  BV号 : {bvid}")
        print(f"  UP主 : {up_name}")
        print(f"  播放量: {format_count(view_count)} ({view_count})")
        print(f"  分区  : {category}")
        print(f"  标签  : {', '.join(tags) if tags else '无'}")

        results.append({
            "rank": i,
            "title": title,
            "bvid": bvid,
            "aid": aid,
            "uploader": up_name,
            "view_count": view_count,
            "category": category,
            "tags": tags,
        })

    output_path = os.path.join(os.path.dirname(__file__), "bilibili_top10.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"结果已保存至: {output_path}")


if __name__ == "__main__":
    main()

# Bilibili 热门视频 Top 10 抓取

使用 Bilibili 官方 API 获取当前热门播放前十的视频信息。

## 环境

```powershell
conda create -n bilibili python=3.12 requests -y
conda activate bilibili
```

## 运行

```powershell
python bilibili_top10.py
```

输出字段：排名、标题、BV号、UP主、播放量、分区、标签。结果同时保存至 `bilibili_top10.json`。

#!/usr/bin/env python3
"""
斗破苍穹等级更新脚本 - 详细版 (斗帝5万起)
包含完整的等级细分：星级、巅峰、转数、半圣、斗圣初中后期等
共计 95 个等级
"""

import os
import re
import requests

# ============== 详细等级配置 ==============

def generate_ranks():
    """生成完整的等级列表"""
    ranks = []
    
    # ========== 斗之气 1-9段 (0-8) ==========
    for i in range(1, 10):
        ranks.append({
            "name": f"斗之气{i}段",
            "short_name": "斗之气",
            "min_stars": i - 1,  # 0-8
            "emoji": "🌑",
            "color": "696969",
            "tier": "斗之气",
            "sub_level": f"{i}段"
        })
    
    # ========== 斗者 1-9星 (9-53) ==========
    base, step = 9, 5
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星斗者",
            "short_name": "斗者",
            "min_stars": base + (i - 1) * step,
            "emoji": "🌒",
            "color": "8B7355",
            "tier": "斗者",
            "sub_level": f"{i}星"
        })
    
    # ========== 斗师 1-9星 (54-118) ==========
    base, step = 54, 8
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星斗师",
            "short_name": "斗师",
            "min_stars": base + (i - 1) * step,
            "emoji": "🌓",
            "color": "6B8E23",
            "tier": "斗师",
            "sub_level": f"{i}星"
        })
    
    # ========== 大斗师 1-9星 (120-200) ==========
    base, step = 120, 10
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星大斗师",
            "short_name": "大斗师",
            "min_stars": base + (i - 1) * step,
            "emoji": "🌔",
            "color": "4682B4",
            "tier": "大斗师",
            "sub_level": f"{i}星"
        })
    
    # ========== 斗灵 1-9星 (220-380) ==========
    base, step = 220, 20
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星斗灵",
            "short_name": "斗灵",
            "min_stars": base + (i - 1) * step,
            "emoji": "🌕",
            "color": "9370DB",
            "tier": "斗灵",
            "sub_level": f"{i}星"
        })
    
    # ========== 斗王 1-9星 (400-640) ==========
    base, step = 400, 30
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星斗王",
            "short_name": "斗王",
            "min_stars": base + (i - 1) * step,
            "emoji": "⭐",
            "color": "FF6347",
            "tier": "斗王",
            "sub_level": f"{i}星"
        })
    
    # ========== 斗皇 1-9星 (680-1000) ==========
    base, step = 680, 40
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星斗皇",
            "short_name": "斗皇",
            "min_stars": base + (i - 1) * step,
            "emoji": "🌟",
            "color": "FFD700",
            "tier": "斗皇",
            "sub_level": f"{i}星"
        })
    
    # ========== 斗宗 1-9星 + 巅峰 (1050-1800) ==========
    base, step = 1050, 75
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}星斗宗",
            "short_name": "斗宗",
            "min_stars": base + (i - 1) * step,
            "emoji": "💫",
            "color": "FF1493",
            "tier": "斗宗",
            "sub_level": f"{i}星"
        })
    ranks.append({
        "name": "斗宗巅峰",
        "short_name": "斗宗",
        "min_stars": 1725,
        "emoji": "💫",
        "color": "FF1493",
        "tier": "斗宗",
        "sub_level": "巅峰"
    })
    
    # ========== 斗尊 1-9转 + 巅峰 (1800-3400) ==========
    base, step = 1800, 160
    for i in range(1, 10):
        ranks.append({
            "name": f"{i}转斗尊",
            "short_name": "斗尊",
            "min_stars": base + (i - 1) * step,
            "emoji": "✨",
            "color": "00CED1",
            "tier": "斗尊",
            "sub_level": f"{i}转"
        })
    ranks.append({
        "name": "斗尊巅峰",
        "short_name": "斗尊",
        "min_stars": 3240,
        "emoji": "✨",
        "color": "00CED1",
        "tier": "斗尊",
        "sub_level": "巅峰"
    })
    
    # ========== 半圣 初级/中级/高级/终极 (3500-4800) ==========
    half_saint_levels = [
        ("初级半圣", 3500, "🔮"),
        ("中级半圣", 3900, "🔮"),
        ("高级半圣", 4300, "🔮"),
        ("终极半圣", 4700, "🔮"),
    ]
    for name, min_s, emoji in half_saint_levels:
        ranks.append({
            "name": name,
            "short_name": "半圣",
            "min_stars": min_s,
            "emoji": emoji,
            "color": "9400D3",
            "tier": "半圣",
            "sub_level": name.replace("半圣", "")
        })
    
    # ========== 斗圣 1-9星 (初期/中期/后期) + 巅峰 (5000-48000) ==========
    base = 5000
    star_step = 4500  # 每星之间的差距
    phase_step = 1500  # 初中后期的差距
    
    saint_phases = ["初期", "中期", "后期"]
    for star in range(1, 10):
        for phase_idx, phase in enumerate(saint_phases):
            min_s = base + (star - 1) * star_step + phase_idx * phase_step
            ranks.append({
                "name": f"{star}星斗圣{phase}",
                "short_name": "斗圣",
                "min_stars": min_s,
                "emoji": "🔥",
                "color": "FF4500",
                "tier": "斗圣",
                "sub_level": f"{star}星{phase}"
            })
    
    # 斗圣巅峰
    ranks.append({
        "name": "斗圣巅峰",
        "short_name": "斗圣",
        "min_stars": 47000,
        "emoji": "🔥",
        "color": "FF4500",
        "tier": "斗圣",
        "sub_level": "巅峰"
    })
    
    # ========== 斗帝 (50000+) ==========
    ranks.append({
        "name": "斗帝",
        "short_name": "斗帝",
        "min_stars": 50000,
        "emoji": "👑",
        "color": "FF0000",
        "tier": "斗帝",
        "sub_level": "无上"
    })
    
    return ranks


# 生成等级列表
RANKS = generate_ranks()

# 大境界颜色映射
TIER_COLORS = {
    "斗之气": "696969",
    "斗者": "8B7355",
    "斗师": "6B8E23",
    "大斗师": "4682B4",
    "斗灵": "9370DB",
    "斗王": "FF6347",
    "斗皇": "FFD700",
    "斗宗": "FF1493",
    "斗尊": "00CED1",
    "半圣": "9400D3",
    "斗圣": "FF4500",
    "斗帝": "FF0000",
}

TIER_EMOJIS = {
    "斗之气": "🌑",
    "斗者": "🌒",
    "斗师": "🌓",
    "大斗师": "🌔",
    "斗灵": "🌕",
    "斗王": "⭐",
    "斗皇": "🌟",
    "斗宗": "💫",
    "斗尊": "✨",
    "半圣": "🔮",
    "斗圣": "🔥",
    "斗帝": "👑",
}


def get_total_stars(username: str, token: str = None) -> int:
    """获取用户所有仓库的 Stars 总数"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    total_stars = 0
    page = 1
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            break
        
        repos = response.json()
        if not repos:
            break
        
        total_stars += sum(repo.get("stargazers_count", 0) for repo in repos)
        page += 1
    
    return total_stars


def get_rank(stars: int) -> dict:
    """根据 Stars 数量获取对应等级"""
    current_rank = RANKS[0]
    current_index = 0
    
    for i, rank in enumerate(RANKS):
        if stars >= rank["min_stars"]:
            current_rank = rank
            current_index = i
    
    next_rank = RANKS[current_index + 1] if current_index + 1 < len(RANKS) else None
    
    # 计算进度
    if next_rank:
        total_range = next_rank["min_stars"] - current_rank["min_stars"]
        current_progress = stars - current_rank["min_stars"]
        progress = (current_progress / total_range) * 100
        progress = min(progress, 100)
        stars_to_next = next_rank["min_stars"] - stars
    else:
        progress = 100
        stars_to_next = 0
    
    return {
        **current_rank,
        "index": current_index + 1,
        "total_ranks": len(RANKS),
        "progress": progress,
        "next_rank": next_rank,
        "stars_to_next": stars_to_next
    }


def generate_progress_bar(progress: float, length: int = 20) -> str:
    """生成文本进度条"""
    filled = int(progress / 100 * length)
    empty = length - filled
    return f"{'█' * filled}{'░' * empty}"


def generate_rank_svg(stars: int, rank: dict, username: str) -> str:
    """生成详细的 SVG 徽章"""
    progress_bar = generate_progress_bar(rank["progress"], 15)
    
    if rank["next_rank"]:
        next_info = f"→ {rank['next_rank']['name']} (还需 {rank['stars_to_next']:,} ⭐)"
    else:
        next_info = "👑 已达巅峰，天下无敌！"
    
    tier = rank["tier"]
    tier_color = TIER_COLORS.get(tier, rank["color"])
    tier_emoji = TIER_EMOJIS.get(tier, rank["emoji"])
    
    svg = f'''<svg width="450" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0a0f;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1a1025;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0d1520;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FFD700" />
      <stop offset="50%" style="stop-color:#FFA500" />
      <stop offset="100%" style="stop-color:#FFD700" />
    </linearGradient>
    <linearGradient id="progressGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#{tier_color}" />
      <stop offset="100%" style="stop-color:#{tier_color}aa" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <rect width="450" height="200" rx="15" fill="url(#bgGrad)"/>
  <rect width="450" height="200" rx="15" fill="none" stroke="#{tier_color}40" stroke-width="2"/>
  
  <!-- 角落装饰 -->
  <path d="M 0 35 L 0 15 Q 0 0 15 0 L 35 0" fill="none" stroke="#{tier_color}80" stroke-width="2"/>
  <path d="M 450 165 L 450 185 Q 450 200 435 200 L 415 200" fill="none" stroke="#{tier_color}80" stroke-width="2"/>
  
  <!-- 标题 -->
  <text x="225" y="28" text-anchor="middle" fill="url(#goldGrad)" font-size="13" font-weight="bold" font-family="sans-serif">
    ⚔️ 斗破苍穹·修炼榜 ⚔️
  </text>
  
  <!-- 大境界 -->
  <text x="225" y="52" text-anchor="middle" fill="#ffffff60" font-size="11" font-family="sans-serif">
    【 {tier} 境界 】
  </text>
  
  <!-- 等级名称 -->
  <text x="225" y="90" text-anchor="middle" fill="#{tier_color}" font-size="30" font-weight="bold" font-family="sans-serif" filter="url(#glow)">
    {tier_emoji} {rank['name']} {tier_emoji}
  </text>
  
  <!-- Stars 数量 -->
  <text x="225" y="120" text-anchor="middle" fill="#FFD700" font-size="18" font-weight="bold" font-family="sans-serif">
    ⭐ {stars:,} 斗气
  </text>
  
  <!-- 下一等级信息 -->
  <text x="225" y="180" text-anchor="middle" fill="#ffffff50" font-size="10" font-family="sans-serif">
    {next_info}
  </text>
  
  <!-- 等级序号 -->
  <text x="420" y="25" text-anchor="end" fill="#ffffff30" font-size="9" font-family="sans-serif">
    Lv.{rank['index']}/{rank['total_ranks']}
  </text>
</svg>'''
    return svg


def generate_markdown_section(stars: int, rank: dict, username: str) -> str:
    """生成 Markdown 格式的等级展示"""
    progress_bar = generate_progress_bar(rank["progress"])
    tier = rank["tier"]
    tier_color = TIER_COLORS.get(tier, rank["color"])
    tier_emoji = TIER_EMOJIS.get(tier, rank["emoji"])
    
    if rank["next_rank"]:
        next_info = f"距离 **{rank['next_rank']['name']}** 还需 **{rank['stars_to_next']:,}** ⭐"
    else:
        next_info = "👑 **已达巅峰，天下无敌！**"
    
    markdown = f'''<div align="center">

## ⚔️ 斗破苍穹·修炼榜 ⚔️

<img src="https://img.shields.io/badge/境界-{tier}-{tier_color}?style=for-the-badge" alt="tier"/>
<img src="https://img.shields.io/badge/等级-{rank['name'].replace(' ', '_')}-{rank['color']}?style=for-the-badge" alt="rank"/>

### {tier_emoji} {rank['name']} {tier_emoji}

<sub>【 {tier} 境界 】· 等级 {rank['index']}/{rank['total_ranks']}</sub>

---

⭐ **斗气值**: **{stars:,}** Stars

```
{progress_bar} {rank['progress']:.1f}%
```

{next_info}

---

<sub>🔄 自动更新 · 三十年河东，三十年河西，莫欺少年穷！</sub>

</div>'''
    return markdown


def update_readme(content: str, new_section: str) -> str:
    """更新 README 中的等级区域"""
    start_marker = "<!-- DOUPO_RANK_START -->"
    end_marker = "<!-- DOUPO_RANK_END -->"
    
    pattern = f"{start_marker}.*?{end_marker}"
    replacement = f"{start_marker}\n{new_section}\n{end_marker}"
    
    if start_marker in content:
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        new_content = f"{replacement}\n\n{content}"
    
    return new_content


def main():
    username = os.environ.get("USERNAME", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    
    if not username:
        print("Error: USERNAME environment variable not set")
        return
    
    print(f"🔍 正在获取 {username} 的 Stars 数据...")
    
    total_stars = get_total_stars(username, token)
    print(f"⭐ 总 Stars: {total_stars}")
    
    rank = get_rank(total_stars)
    print(f"🎖️ 当前等级: {rank['name']} ({rank['tier']} 境界)")
    print(f"📊 等级进度: {rank['index']}/{rank['total_ranks']}")
    
    markdown_section = generate_markdown_section(total_stars, rank, username)
    svg_content = generate_rank_svg(total_stars, rank, username)
    
    svg_path = "assets/doupo-rank.svg"
    os.makedirs("assets", exist_ok=True)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"📝 已保存 SVG 徽章到 {svg_path}")
    
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    else:
        readme_content = ""
    
    new_readme = update_readme(readme_content, markdown_section)
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)
    
    print(f"✅ 已更新 README.md")
    print(f"🔥 {rank['emoji']} {rank['name']} - {total_stars:,} Stars")


if __name__ == "__main__":
    main()

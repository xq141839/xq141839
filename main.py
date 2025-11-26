import os
import re
import requests

# ================= 配置区域 =================
# 👇 把这里的名字改成你的 GitHub 用户名
USERNAME = "你的GitHub用户名"
# ===========================================

def get_total_stars(username):
    """获取用户所有仓库的 Star 总数"""
    total_stars = 0
    page = 1
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100&type=owner"
        try:
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                print(f"Error fetching repos: {r.status_code}")
                break
            data = r.json()
            if not data:
                break
            for repo in data:
                total_stars += repo.get('stargazers_count', 0)
            page += 1
        except Exception as e:
            print(f"Error: {e}")
            break
            
    return total_stars

def get_doupo_rank(stars):
    """根据 Star 数返回 斗破苍穹 等级配置"""
    # 格式: (左侧文字, 右侧文字, 颜色, 经典语录)
    if stars <= 10:
        return "境界", "斗之气·三段", "lightgrey", "三十年河东，三十年河西，莫欺少年穷！"
    elif stars <= 50:
        return "境界", "斗者", "green", "凝聚气旋，正式踏入修炼！"
    elif stars <= 100:
        return "境界", "斗师", "blue", "斗气纱衣，防御初成。"
    elif stars <= 300:
        return "境界", "大斗师", "blueviolet", "斗气铠甲，坚不可摧！"
    elif stars <= 600:
        return "境界", "斗灵", "yellow", "斗气凝物，随心所欲。"
    elif stars <= 1000:
        return "境界", "斗王", "orange", "斗气化翼，调动外界能量！"
    elif stars <= 2000:
        return "境界", "斗皇", "red", "恐怖如斯，强者之列！"
    elif stars <= 5000:
        return "境界", "斗宗", "critical", "踏空而行，宗派之主！"
    elif stars <= 10000:
        return "境界", "斗尊", "inactive", "掌握空间之力！"
    else:
        return "境界", "斗圣·巅峰", "gold", "此子恐怖如斯，断不可留！"

def update_readme(stars):
    label, rank, color, quote = get_doupo_rank(stars)
    
    # 生成徽章 URL
    badge_url = f"https://img.shields.io/badge/{label}-{rank}-{color}?style=for-the-badge&logo=github"
    
    # 生成要插入的 HTML
    new_content = f"""<div align="center">
    <h3>🔥 斗气大陆修炼进度 (Cultivation)</h3>
    <img src="{badge_url}" alt="{rank}" />
    <br/>
    <p>当前星力值 (Total Stars): <strong>{stars}</strong></p>
    <sub>“{quote}”</sub>
</div>
"""

    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 使用正则替换标记中间的内容
        pattern = r".*"
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_content, content, flags=re.DOTALL)
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("✅ README updated successfully!")
        else:
            print("⚠️ Markers not found in README.md")

if __name__ == "__main__":
    stars = get_total_stars(USERNAME)
    print(f"User: {USERNAME}, Total Stars: {stars}")
    update_readme(stars)

#!/usr/bin/env python3
"""
根据内存分析结果保存用户偏好和背景信息

这个脚本分析了 GLM Agent 的内存内容，并基于发现的用户特征
主动保存用户偏好和上下文信息
"""

from glm_langchain_client import GLMClient
import json
from datetime import datetime


def save_analyzed_user_profile():
    """根据内存分析结果保存用户画像"""
    
    # 初始化客户端（启用内存）
    client = GLMClient(enable_memory=True)
    
    print("📊 基于内存分析保存用户偏好和背景信息\n")
    
    # 1. 保存用户偏好 (Preferences)
    print("1️⃣ 保存用户偏好...")
    print("-" * 60)
    
    preferences = {
        "content_type": "movies_and_tv",
        "preferred_style": "recent_content_with_beautiful_actresses",
        "region_preference": "china_mainland",
        "also_interested_in": "economic_news",
    }
    
    for key, value in preferences.items():
        client.memory.save_preference(key, value)
        print(f"   ✓ {key} = {value}")
    
    print()
    
    # 2. 保存用户背景信息 (Context)
    print("2️⃣ 保存用户背景信息...")
    print("-" * 60)
    
    context_data = {
        "primary_interest": "电影电视剧推荐",
        "interaction_style": "简短请求 + 验证类回应",
        "search_frequency": "高频（2.5小时内24次搜索）",
        "total_messages": 213,
        "total_user_messages": 182,
        "total_assistant_responses": 31,
        "interaction_date": "2026-02-14",
        "interaction_duration": "2.5 hours",
        "preferred_search_sources": ["news-search", "china-search"],
    }
    
    for key, value in context_data.items():
        client.memory.save_context(key, value)
        print(f"   ✓ {key}")
    
    print()
    
    # 3. 保存用户行为分析 (Context)
    print("3️⃣ 保存用户行为分析...")
    print("-" * 60)
    
    behavior_analysis = {
        "top_message_1": ("Based on the actual result above, answer my question.", 90),
        "top_message_2": ("ok", 43),
        "top_message_3": ("推荐最近的好看的可以在大陆看的电影电视剧", 16),
        "user_trait_1": "喜欢电影电视剧推荐（主要需求）",
        "user_trait_2": "明确表达偏好'有性感美女的'内容",
        "user_trait_3": "对经济新闻有次要兴趣",
        "user_trait_4": "经常重复搜索已看过的内容",
        "interaction_pattern": "高频率、简短请求",
    }
    
    client.memory.save_context("user_behavior_analysis", behavior_analysis)
    print("   ✓ 用户行为分析已保存")
    
    print()
    
    # 4. 保存推荐优化建议
    print("4️⃣ 保存推荐优化建议...")
    print("-" * 60)
    
    recommendations = {
        "optimization_1": "实现去重机制，避免重复推荐已看过的内容",
        "optimization_2": "优先推荐'最近的'和'有性感美女的'电影电视剧",
        "optimization_3": "在电影推荐中优先显示中国大陆可看的内容",
        "optimization_4": "可偶尔穿插经济新闻内容",
        "optimization_5": "简化交互流程，减少重复确认（ok）",
    }
    
    for key, value in recommendations.items():
        print(f"   ✓ {value}")
    
    client.memory.save_context("optimization_recommendations", recommendations)
    
    print()
    
    # 5. 验证保存结果
    print("5️⃣ 验证保存结果...")
    print("-" * 60)
    
    summary = client.memory.get_memory_summary()
    print(summary)
    
    print()
    print("✅ 用户偏好和背景信息已完整保存！")
    print()
    
    # 6. 显示保存的文件信息
    print("📁 已保存的文件：")
    print("-" * 60)
    print("   • .memories/preferences.json")
    print("   • .memories/context.json")
    print("   • .memories/history.json")
    print()
    
    # 7. 显示如何使用这些信息
    print("🚀 如何使用保存的信息：")
    print("-" * 60)
    print("""
在下次对话时，这些信息会自动注入到系统提示中：
  
  1. AI 会知道用户喜欢电影电视剧推荐
  2. AI 会了解用户的内容偏好
  3. AI 可以避免重复推荐
  4. AI 可以提供更个性化的服务
  
例如，AI 会记住：
  • 用户对"有性感美女的"内容感兴趣
  • 用户关注中国大陆可看的内容
  • 用户也对经济新闻感兴趣
  • 用户的交互方式是简短和直接的
    """)
    
    print()
    print("=" * 60)
    print("分析和保存完成！🎉")
    print("=" * 60)


if __name__ == "__main__":
    save_analyzed_user_profile()

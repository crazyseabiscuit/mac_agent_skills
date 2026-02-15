#!/usr/bin/env python3
"""Automated testing script for GLM Terminal."""
import os
import json
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import subprocess
import re

# Test cases with expected behaviors
TEST_CASES = [
    {
        "id": 1,
        "query": "帮我搜索今天的足球新闻",
        "expected_behavior": "execute_news_search",
        "expected_keywords": ["足球", "新闻", "搜索"],
        "should_contain": ["EXECUTE:", "search_news.py"],
        "points": 10
    },
    {
        "id": 2,
        "query": "搜索杨幂的电视剧",
        "expected_behavior": "execute_china_search",
        "expected_keywords": ["杨幂", "电视剧"],
        "should_contain": ["EXECUTE:", "china_search.py"],
        "points": 10
    },
    {
        "id": 3,
        "query": "我喜欢看科幻电影",
        "expected_behavior": "save_preference",
        "expected_keywords": ["科幻", "电影"],
        "should_contain": ["SAVE_MEMORY:"],
        "points": 10
    },
    {
        "id": 4,
        "query": "查找 NBA 的最新消息",
        "expected_behavior": "execute_news_search",
        "expected_keywords": ["NBA", "新闻"],
        "should_contain": ["EXECUTE:", "search_news.py"],
        "points": 10
    },
    {
        "id": 5,
        "query": "你好",
        "expected_behavior": "normal_response",
        "expected_keywords": ["你好", "助手"],
        "should_not_contain": ["EXECUTE:", "SAVE_MEMORY:"],
        "points": 5
    }
]

SYSTEM_PROMPT = """You are a helpful AI assistant with access to various tools.

When user asks you to search or find information, you MUST execute the actual command:

**News Search** (for general news, sports, tech, etc.):
EXECUTE: python skills/news-search/search_news.py "search query" --limit 10

**China Content Search** (for Chinese movies, TV shows, entertainment):
EXECUTE: python skills/china-search/china_search.py "search query" --type [movie|tv|entertainment]

IMPORTANT: 
1. When you need to search or check information, respond with EXACTLY this format on a new line:
   EXECUTE: [command]
2. When user mentions their preferences, interests, or background, respond with:
   SAVE_MEMORY: preference_key=value OR context_key=value

Do NOT make up information. Always execute the command first to get real data."""

def execute_command(cmd):
    """Execute shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"

def check_response(response, test_case):
    """Check if response meets expectations."""
    score = 0
    feedback = []
    
    # Check if should contain certain strings
    if "should_contain" in test_case:
        for keyword in test_case["should_contain"]:
            if keyword in response:
                score += test_case["points"] // len(test_case["should_contain"])
                feedback.append(f"✅ Contains '{keyword}'")
            else:
                feedback.append(f"❌ Missing '{keyword}'")
    
    # Check if should NOT contain certain strings
    if "should_not_contain" in test_case:
        all_good = True
        for keyword in test_case["should_not_contain"]:
            if keyword in response:
                feedback.append(f"❌ Should not contain '{keyword}'")
                all_good = False
        if all_good:
            score += test_case["points"]
            feedback.append(f"✅ Correctly avoids unwanted patterns")
    
    # Check for expected keywords (bonus points)
    keyword_found = sum(1 for kw in test_case.get("expected_keywords", []) if kw in response)
    if keyword_found > 0:
        feedback.append(f"✅ Found {keyword_found}/{len(test_case.get('expected_keywords', []))} keywords")
    
    return score, feedback

def run_test(client, test_case):
    """Run a single test case."""
    print(f"\n{'='*60}")
    print(f"Test #{test_case['id']}: {test_case['query']}")
    print(f"Expected: {test_case['expected_behavior']}")
    print(f"{'='*60}")
    
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.append(HumanMessage(content=test_case['query']))
    
    # Get AI response
    response = client.invoke(messages)
    print(f"\nAI Response:\n{response}\n")
    
    # Check if response contains EXECUTE command
    if "EXECUTE:" in response:
        for line in response.split("\n"):
            if line.startswith("EXECUTE:"):
                cmd = line.replace("EXECUTE:", "").strip()
                print(f"[Executing: {cmd}]")
                output = execute_command(cmd)
                print(f"Command output (first 200 chars):\n{output[:200]}...\n")
                
                # Simulate asking AI to summarize
                messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))
                messages.append(HumanMessage(content="请用中文总结上面的搜索结果，提取关键信息。"))
                summary = client.invoke(messages)
                print(f"AI Summary:\n{summary}\n")
                response = f"{response}\n[EXECUTED]\n{summary}"
                break
    
    # Evaluate response
    score, feedback = check_response(response, test_case)
    
    print(f"Score: {score}/{test_case['points']}")
    for fb in feedback:
        print(f"  {fb}")
    
    return score, test_case['points']

def main():
    """Run all tests and generate report."""
    print("\n" + "="*60)
    print("GLM TERMINAL AUTOMATED TESTING")
    print("="*60)
    
    # Initialize client
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ Error: ZHIPUAI_API_KEY not set")
        return
    
    client = GLMClient(api_key=api_key)
    
    # Run all tests
    total_score = 0
    max_score = 0
    results = []
    
    for test_case in TEST_CASES:
        try:
            score, max_points = run_test(client, test_case)
            total_score += score
            max_score += max_points
            results.append({
                "id": test_case["id"],
                "query": test_case["query"],
                "score": score,
                "max": max_points,
                "passed": score >= max_points * 0.7  # 70% threshold
            })
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append({
                "id": test_case["id"],
                "query": test_case["query"],
                "score": 0,
                "max": test_case["points"],
                "passed": False,
                "error": str(e)
            })
            max_score += test_case["points"]
    
    # Generate report
    print("\n" + "="*60)
    print("TEST REPORT")
    print("="*60)
    
    for result in results:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{status} Test #{result['id']}: {result['score']}/{result['max']} - {result['query']}")
        if "error" in result:
            print(f"     Error: {result['error']}")
    
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    print(f"\n{'='*60}")
    print(f"FINAL SCORE: {total_score}/{max_score} ({percentage:.1f}%)")
    print(f"{'='*60}")
    
    # Grade
    if percentage >= 90:
        grade = "A (Excellent)"
    elif percentage >= 80:
        grade = "B (Good)"
    elif percentage >= 70:
        grade = "C (Acceptable)"
    elif percentage >= 60:
        grade = "D (Needs Improvement)"
    else:
        grade = "F (Failed)"
    
    print(f"\nGrade: {grade}\n")
    
    # Save results to JSON
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "grade": grade,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print("📊 Detailed results saved to: test_results.json\n")

if __name__ == "__main__":
    main()

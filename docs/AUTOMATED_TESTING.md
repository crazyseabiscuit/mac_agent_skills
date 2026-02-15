# GLM Terminal 自动化测试

## 📋 测试脚本说明

`test_glm_terminal.py` 是一个自动化测试脚本，用于验证 GLM Terminal 的功能是否正常工作。

## 🎯 测试内容

### 测试用例

| ID | 查询 | 预期行为 | 分数 |
|----|------|----------|------|
| 1 | 帮我搜索今天的足球新闻 | 执行新闻搜索 | 10 |
| 2 | 搜索杨幂的电视剧 | 执行中国内容搜索 | 10 |
| 3 | 我喜欢看科幻电影 | 保存用户偏好 | 10 |
| 4 | 查找 NBA 的最新消息 | 执行新闻搜索 | 10 |
| 5 | 你好 | 正常对话响应 | 5 |

### 评分标准

每个测试用例检查：
- ✅ **必须包含**：特定命令或关键词（如 `EXECUTE:`, `SAVE_MEMORY:`）
- ❌ **不应包含**：不该出现的内容
- 🔍 **关键词匹配**：响应中是否包含相关关键词

## 🚀 使用方法

### 1. 基本运行

```bash
export ZHIPUAI_API_KEY="your-api-key"
python test_glm_terminal.py
```

### 2. 查看结果

测试会输出：
```
============================================================
GLM TERMINAL AUTOMATED TESTING
============================================================

============================================================
Test #1: 帮我搜索今天的足球新闻
Expected: execute_news_search
============================================================

AI Response:
EXECUTE: python skills/news-search/search_news.py "足球" --limit 10

[Executing: python skills/news-search/search_news.py "足球" --limit 10]
Command output (first 200 chars):
搜索新闻: 足球
1. Manchester City make quick work...

AI Summary:
根据搜索结果，今天值得关注的足球新闻包括...

Score: 10/10
  ✅ Contains 'EXECUTE:'
  ✅ Contains 'search_news.py'
  ✅ Found 3/3 keywords

============================================================
TEST REPORT
============================================================
✅ PASS Test #1: 10/10 - 帮我搜索今天的足球新闻
✅ PASS Test #2: 10/10 - 搜索杨幂的电视剧
✅ PASS Test #3: 10/10 - 我喜欢看科幻电影
✅ PASS Test #4: 10/10 - 查找 NBA 的最新消息
✅ PASS Test #5: 5/5 - 你好

============================================================
FINAL SCORE: 45/45 (100.0%)
============================================================

Grade: A (Excellent)

📊 Detailed results saved to: test_results.json
```

### 3. 查看详细结果

```bash
cat test_results.json
```

输出示例：
```json
{
  "total_score": 45,
  "max_score": 45,
  "percentage": 100.0,
  "grade": "A (Excellent)",
  "results": [
    {
      "id": 1,
      "query": "帮我搜索今天的足球新闻",
      "score": 10,
      "max": 10,
      "passed": true
    },
    ...
  ]
}
```

## 📊 评分等级

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100% | A | 优秀 |
| 80-89% | B | 良好 |
| 70-79% | C | 可接受 |
| 60-69% | D | 需要改进 |
| <60% | F | 不及格 |

## 🔧 自定义测试用例

编辑 `test_glm_terminal.py` 中的 `TEST_CASES`：

```python
TEST_CASES = [
    {
        "id": 6,
        "query": "你的自定义查询",
        "expected_behavior": "描述预期行为",
        "expected_keywords": ["关键词1", "关键词2"],
        "should_contain": ["必须包含的字符串"],
        "should_not_contain": ["不应包含的字符串"],  # 可选
        "points": 10
    }
]
```

### 字段说明

- **id**: 测试用例编号
- **query**: 用户查询
- **expected_behavior**: 预期行为描述（仅用于显示）
- **expected_keywords**: 响应中应包含的关键词（用于额外验证）
- **should_contain**: 必须包含的字符串列表（主要评分依据）
- **should_not_contain**: 不应包含的字符串列表（可选）
- **points**: 该测试用例的总分

## 📈 测试场景示例

### 场景 1：测试新闻搜索
```python
{
    "id": 1,
    "query": "今天有什么科技新闻",
    "expected_behavior": "execute_news_search",
    "expected_keywords": ["科技", "新闻"],
    "should_contain": ["EXECUTE:", "search_news.py"],
    "points": 10
}
```

### 场景 2：测试记忆保存
```python
{
    "id": 2,
    "query": "我住在北京",
    "expected_behavior": "save_context",
    "expected_keywords": ["北京"],
    "should_contain": ["SAVE_MEMORY:"],
    "points": 10
}
```

### 场景 3：测试正常对话
```python
{
    "id": 3,
    "query": "什么是人工智能",
    "expected_behavior": "normal_response",
    "expected_keywords": ["人工智能", "AI"],
    "should_not_contain": ["EXECUTE:", "SAVE_MEMORY:"],
    "points": 5
}
```

## 🐛 故障排除

### 问题 1：API Key 错误
```
❌ Error: ZHIPUAI_API_KEY not set
```

**解决**：
```bash
export ZHIPUAI_API_KEY="your-api-key"
```

### 问题 2：命令执行失败
```
Error: Command 'python skills/news-search/...' failed
```

**解决**：
- 确认 skills 文件夹存在
- 确认相关依赖已安装
- 检查 API keys（TAVILY_API_KEY, GNEWS_API_KEY）

### 问题 3：测试超时
```
Error: timeout
```

**解决**：
- 检查网络连接
- 增加 timeout 时间（在 `execute_command` 函数中）

## 💡 最佳实践

### 1. 定期运行测试
```bash
# 每次修改代码后运行
python test_glm_terminal.py
```

### 2. 持续集成
```bash
# 在 CI/CD 中运行
#!/bin/bash
export ZHIPUAI_API_KEY=$SECRET_KEY
python test_glm_terminal.py
if [ $? -eq 0 ]; then
    echo "Tests passed"
else
    echo "Tests failed"
    exit 1
fi
```

### 3. 比较测试结果
```bash
# 保存历史结果
cp test_results.json test_results_$(date +%Y%m%d).json

# 比较两次测试
diff test_results_20260214.json test_results_20260215.json
```

## 📝 扩展功能

### 添加性能测试
```python
import time

start_time = time.time()
response = client.invoke(messages)
elapsed = time.time() - start_time

if elapsed > 5:
    feedback.append(f"⚠️ Slow response: {elapsed:.2f}s")
```

### 添加并发测试
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(run_test, client, tc) for tc in TEST_CASES]
    results = [f.result() for f in futures]
```

### 生成 HTML 报告
```python
html = f"""
<html>
<body>
<h1>Test Report</h1>
<p>Score: {total_score}/{max_score}</p>
<p>Grade: {grade}</p>
</body>
</html>
"""
with open("report.html", "w") as f:
    f.write(html)
```

## 🎯 总结

这个测试脚本可以：
- ✅ 自动运行预定义的查询
- ✅ 验证 AI 响应是否符合预期
- ✅ 执行实际命令并检查结果
- ✅ 生成详细的评分报告
- ✅ 保存结果到 JSON 文件

**快速开始**：
```bash
python test_glm_terminal.py
```

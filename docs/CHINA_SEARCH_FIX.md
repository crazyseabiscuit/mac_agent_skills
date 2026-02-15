# China Search 搜索改进

## 问题
搜索"杨幂 电视剧"时返回不相关结果（杨振宁、杨紫等）

## 原因
1. Bing 搜索没有精确匹配
2. 豆瓣/微博爬取被反爬虫阻止
3. 缺少可靠的搜索源

## 解决方案

### 1. 添加 Tavily API 支持
- 使用 Tavily HTTP API（无需额外依赖）
- 优先搜索豆瓣、知乎、微博等中文网站
- 结果更准确、更相关

### 2. 改进 Bing 搜索
- 添加引号精确匹配：`"杨幂" 电视剧 豆瓣`
- 过滤不相关结果
- 只保留标题/描述中包含查询词的结果

### 3. 搜索优先级
```
Tavily (最可靠) → 豆瓣 → 微博 → Bing (备用)
```

## 测试结果

**修复前**：
```bash
$ python skills/china-search/china_search.py "杨幂" --type tv
❌ 返回：杨振宁、杨紫、杨伟等不相关结果
```

**修复后**：
```bash
$ python skills/china-search/china_search.py "杨幂" --type tv
✅ 返回：
1. 杨幂 - 豆瓣
2. 杨幂电视剧电影 - 豆瓣
3. 三生三世十里桃花 - 豆瓣
```

## 使用

确保设置了 TAVILY_API_KEY：
```bash
export TAVILY_API_KEY="your_key_here"
```

然后正常搜索即可：
```bash
python skills/china-search/china_search.py "杨幂" --type tv
python skills/china-search/china_search.py "杨幂 三生三世" --type tv
```

## 技术细节

- 使用 Tavily HTTP API（`https://api.tavily.com/search`）
- 通过 `include_domains` 限制搜索中文网站
- 使用 httpx 发送 POST 请求
- 无需安装 tavily-python 包

## 优势

✅ 搜索结果准确相关  
✅ 无需额外 Python 依赖  
✅ 支持豆瓣、知乎、微博等中文网站  
✅ 自动降级到备用搜索源

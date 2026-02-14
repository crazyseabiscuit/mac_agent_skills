# 🔐 API Keys 和敏感信息安全指南

所有 API keys 和敏感信息已从代码中移除，现在统一管理在 `config.properties` 文件中。

## 🛡️ 安全措施

### 1. 配置文件管理

- **config.properties** - 本地配置文件（包含真实的 API keys）
  - ✅ 已添加到 .gitignore
  - ✅ 永远不会提交到版本控制
  - ✅ 包含所有实际的 API keys

- **config.properties.example** - 配置模板
  - ✅ 包含所有配置项说明
  - ✅ 使用占位符替代真实的 keys
  - ✅ 安全提交到版本控制
  - ✅ 用户参考模板

### 2. .gitignore 更新

以下文件已添加到 .gitignore，永远不会被提交：

```
config.properties          # 包含真实的 API keys
config.json               # 可能包含敏感信息
.env                      # 环境变量文件
.env.local               # 本地环境变量
*.key, *.pem, *.secret   # 证书和密钥文件
.memories/               # 可能包含敏感的对话记录
```

## 📝 如何使用

### 第一次设置项目

1. **查看模板配置**
   ```bash
   cat config.properties.example
   ```

2. **复制模板创建本地配置**
   ```bash
   cp config.properties.example config.properties
   ```

3. **编辑 config.properties，填入真实的 API keys**
   ```bash
   nano config.properties
   ```

4. **验证配置**
   ```bash
   cat config.properties  # 检查是否包含真实的 keys
   ```

### 运行代码和测试

代码会自动从 `config.properties` 读取 API keys：

```python
# 自动从 config.properties 加载
config = load_config()
api_key = config.get("tavily.api_key")
```

### 配置文件中的 API 密钥

#### ZhipuAI 密钥
```properties
zhipuai.api_key=YOUR_ZHIPUAI_API_KEY_HERE
```

获取方式: https://www.zhipuai.cn/

#### GNews API 密钥
```properties
gnews.api_key=YOUR_GNEWS_API_KEY_HERE
```

获取方式: https://gnews.io/

#### Tavily API 密钥
```properties
tavily.api_key=YOUR_TAVILY_API_KEY_HERE
```

获取方式: https://tavily.com/

#### DeepSeek API 密钥
```properties
deepseek.api_key=YOUR_DEEPSEEK_API_KEY_HERE
```

获取方式: https://www.deepseek.com/

#### NewsAPI 密钥（可选）
```properties
newsapi.api_key=YOUR_NEWSAPI_API_KEY_HERE
```

获取方式: https://newsapi.org/

## 🔍 验证安全性

### 1. 检查 config.properties 不在版本控制中

```bash
# 查看 git 中被跟踪的文件
git ls-files | grep config.properties
# 应该返回空（只有 config.properties.example）
```

### 2. 检查 .gitignore 配置

```bash
# 查看 .gitignore 中的配置
cat .gitignore | grep config.properties
# 应该包含 "config.properties"
```

### 3. 检查代码中没有硬编码的密钥

```bash
# 搜索硬编码的 API keys
grep -r "api_key.*=" *.py tests/*.py | grep -v "config.properties\|YOUR_"
# 应该返回空或只是配置加载的代码
```

## ⚠️ 重要提醒

### 如果误提交了密钥该怎么办

如果不小心把包含真实 API keys 的 config.properties 提交到了版本控制：

1. **立即更换所有 API keys**
   - 访问各个服务的仪表板
   - 重新生成新的 API keys
   - 更新本地 config.properties

2. **从 git 历史中删除**
   ```bash
   # 使用 git-filter-branch 或 BFG Repo-Cleaner
   git filter-branch --tree-filter 'rm -f config.properties' HEAD
   ```

3. **通知团队成员**
   - 告知他们已泄露的 keys 已被更换

### 开发时最佳实践

✅ **正确做法**
- 使用 config.properties.example 作为模板
- 在本地 config.properties 中填入真实的 keys
- 从不提交 config.properties
- 定期审查 .gitignore 配置

❌ **错误做法**
- 在代码中硬编码 API keys
- 提交包含真实 keys 的配置文件
- 在日志或注释中暴露密钥
- 在公开的 GitHub Gist 或 Pastebin 分享代码

## 📋 配置项说明

### 核心配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| glm.model | GLM 主模型 | glm-4.7 |
| glm.fallback_model | 备用模型 | glm-4.7 |
| glm.temperature | 采样温度 | 0.5 |
| glm.streaming | 是否启用流式 | false |

### API 密钥配置

| 配置项 | 说明 | 必需 |
|--------|------|------|
| zhipuai.api_key | ZhipuAI API 密钥 | ✅ 是 |
| gnews.api_key | GNews API 密钥 | ✅ 是 |
| tavily.api_key | Tavily API 密钥 | ✅ 是 |
| deepseek.api_key | DeepSeek API 密钥 | ❌ 可选 |
| newsapi.api_key | NewsAPI 密钥 | ❌ 可选 |

### 可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| langsmith.api_key | LangSmith API 密钥 | 无 |
| langsmith.project | LangSmith 项目名 | 无 |
| memory.dir | 内存存储目录 | .memories |
| memory.enabled | 是否启用记忆系统 | true |
| test.verbose | 测试是否详细输出 | false |

## 🔗 相关文件

- `.gitignore` - 版本控制忽略规则
- `config.properties` - 本地配置（不提交）
- `config.properties.example` - 配置模板（提交）
- `config.json` - JSON 格式配置（如果存在）

## 📞 故障排除

### "找不到 config.properties"

**原因**: 配置文件不存在

**解决方案**:
```bash
cp config.properties.example config.properties
# 然后编辑并填入真实的 API keys
```

### "API key 错误" 或 "认证失败"

**原因**: 
- config.properties 中的 API keys 未填入
- API keys 无效或已过期
- API keys 不匹配

**解决方案**:
1. 检查 config.properties 中的 keys 是否正确
2. 验证 API keys 是否仍有效（检查各服务仪表板）
3. 重新生成 API keys 并更新配置

### 配置加载失败

**原因**: config.properties 文件格式错误

**解决方案**:
1. 检查文件格式（key=value，每行一个）
2. 确保没有多余的空格或特殊字符
3. 参照 config.properties.example 重新创建文件

## ✅ 安全性检查清单

在提交代码前检查：

- [ ] config.properties 在 .gitignore 中
- [ ] config.properties 未被 git 跟踪
- [ ] 代码中没有硬编码的 API keys
- [ ] 使用了 config.properties.example 作为文档
- [ ] 所有敏感信息都从代码中移除
- [ ] 使用了环境变量或配置文件来管理 keys
- [ ] .gitignore 包含所有需要忽略的文件

## 🎓 推荐阅读

- [GitHub - 保护敏感数据](https://docs.github.com/en/code-security/secret-scanning)
- [12 Factor App - 配置管理](https://12factor.net/config)
- [OWASP - 敏感数据暴露](https://owasp.org/www-project-top-ten/)

---

**所有密钥现已安全管理！** 🔒

定期检查 .gitignore 配置和敏感文件状态，确保安全。

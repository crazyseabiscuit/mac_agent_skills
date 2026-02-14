# 📚 文档目录

所有项目文档已组织在此文件夹下。

## 📖 快速导航

### 🚀 快速开始
- **[MEMORY_QUICKSTART.md](MEMORY_QUICKSTART.md)** - 5分钟快速入门长期和短期记忆
  - 立即开始使用
  - 基础 API 示例
  - 常见问题

### 💾 长期和短期记忆系统
- **[MEMORY_USAGE.md](MEMORY_USAGE.md)** - 详细使用文档（推荐）
  - 完整 API 参考
  - 使用场景
  - 最佳实践
  - 故障排除
  
- **[MEMORY_IMPLEMENTATION_SUMMARY.md](MEMORY_IMPLEMENTATION_SUMMARY.md)** - 实现细节
  - 工作原理
  - 架构设计
  - 数据结构
  - 性能特点

- **[MEMORY_CHANGES.md](MEMORY_CHANGES.md)** - 长期记忆功能说明
  - 变更摘要
  - 新增特性
  - API 概览

### 🧪 测试文件整理
- **[TEST_REORGANIZATION.md](TEST_REORGANIZATION.md)** - 测试文件夹整理详情
  - 项目结构变化
  - 代码修改内容
  - 验证结果
  - 运行测试的方法

### ✅ 完成检查清单
- **[COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md)** - 功能完成清单
  - 功能实现状态
  - 测试覆盖
  - 质量指标
  - 部署检查

## 🗂️ 文件组织

```
docs/
├── README.md                              (本文件)
├── INDEX.md                               (详细索引)
├── 
├── 📘 长期记忆系统文档
│   ├── MEMORY_QUICKSTART.md              (快速开始) ⭐
│   ├── MEMORY_USAGE.md                   (详细指南)
│   ├── MEMORY_IMPLEMENTATION_SUMMARY.md  (实现原理)
│   └── MEMORY_CHANGES.md                 (变更说明)
│
└── 📗 项目管理文档
    ├── TEST_REORGANIZATION.md             (测试整理)
    └── COMPLETION_CHECKLIST.md            (完成清单)
```

## 🎯 按用途选择文档

### 如果你想...

**快速开始使用长期记忆**
→ 查看 [MEMORY_QUICKSTART.md](MEMORY_QUICKSTART.md)

**深入了解 API 和用法**
→ 查看 [MEMORY_USAGE.md](MEMORY_USAGE.md)

**理解系统实现原理**
→ 查看 [MEMORY_IMPLEMENTATION_SUMMARY.md](MEMORY_IMPLEMENTATION_SUMMARY.md)

**了解功能变更**
→ 查看 [MEMORY_CHANGES.md](MEMORY_CHANGES.md)

**了解测试整理**
→ 查看 [TEST_REORGANIZATION.md](TEST_REORGANIZATION.md)

**查看完成状态**
→ 查看 [COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md)

## 📊 文档统计

| 文档 | 大小 | 内容 | 推荐度 |
|------|------|------|--------|
| MEMORY_QUICKSTART.md | 4.9K | 快速入门 | ⭐⭐⭐⭐⭐ |
| MEMORY_USAGE.md | 5.4K | 详细指南 | ⭐⭐⭐⭐⭐ |
| MEMORY_IMPLEMENTATION_SUMMARY.md | 6.7K | 实现原理 | ⭐⭐⭐⭐ |
| MEMORY_CHANGES.md | 6.4K | 变更说明 | ⭐⭐⭐ |
| TEST_REORGANIZATION.md | 8.2K | 测试整理 | ⭐⭐⭐⭐ |
| COMPLETION_CHECKLIST.md | 5.3K | 完成清单 | ⭐⭐⭐ |
| **总计** | **36.9K** | **6 份文档** | |

## 🚀 常用命令

```bash
# 查看文档列表
ls -lh docs/

# 快速查看某个文档
cat docs/MEMORY_QUICKSTART.md

# 使用 less 分页查看
less docs/MEMORY_USAGE.md

# 搜索文档中的内容
grep -r "导入" docs/
grep -r "API" docs/
```

## 🔗 相关链接

### 项目根目录结构
```
mac_agent_skills/
├── docs/                    (📁 所有文档在这里)
├── tests/                   (📁 所有测试在这里)
├── skills/                  (📁 技能文件)
├── memory_manager.py        (💾 记忆管理模块)
├── glm_langchain_client.py  (🤖 GLM 客户端)
├── glm_terminal.py          (💻 终端交互)
└── example_memory_usage.py  (🎓 使用示例)
```

### 主要功能
- ✅ 长期和短期记忆系统
- ✅ GLM 模型集成
- ✅ 自动技能加载
- ✅ 新闻搜索功能
- ✅ 完整的测试套件

## 📚 推荐阅读顺序

1. **[MEMORY_QUICKSTART.md](MEMORY_QUICKSTART.md)** (5 分钟)
   - 快速了解基础概念
   
2. **[MEMORY_USAGE.md](MEMORY_USAGE.md)** (10 分钟)
   - 学习详细的 API 使用
   
3. **[MEMORY_IMPLEMENTATION_SUMMARY.md](MEMORY_IMPLEMENTATION_SUMMARY.md)** (10 分钟)
   - 理解内部工作原理
   
4. **[TEST_REORGANIZATION.md](TEST_REORGANIZATION.md)** (可选)
   - 了解测试文件组织

## ✨ 文档特点

✅ **全面覆盖** - 从快速入门到深入原理
✅ **实用指南** - 包含大量代码示例
✅ **最佳实践** - 专业建议和技巧
✅ **故障排除** - 常见问题解决方案
✅ **组织清晰** - 易于查找和导航

## 🎓 学习路径

### 新用户
1. 阅读 MEMORY_QUICKSTART.md
2. 运行 example_memory_usage.py
3. 查看 MEMORY_USAGE.md 中的特定部分

### 开发者
1. 阅读 MEMORY_IMPLEMENTATION_SUMMARY.md
2. 研究 memory_manager.py 源代码
3. 查看 COMPLETION_CHECKLIST.md 了解现有功能

### 维护者
1. 查看 COMPLETION_CHECKLIST.md
2. 查看 TEST_REORGANIZATION.md
3. 查看 MEMORY_CHANGES.md 了解所有变更

## 💡 提示

- 所有文档都支持搜索 (Ctrl+F)
- 使用目录导航快速跳转
- 文档中的代码示例都已验证
- 遇到问题时先查看故障排除部分

## 🔄 文档更新

这些文档记录了项目的最新状态：

- ✅ 长期记忆系统已完全实现
- ✅ 测试文件已整理到 tests/ 文件夹
- ✅ 所有代码已验证通过
- ✅ 文档已整理到 docs/ 文件夹

## 📞 快速参考

**长期记忆 API:**
```python
client.memory.save_preference(key, value)
client.memory.get_preference(key)
client.memory.save_context(key, value)
client.memory.get_context(key)
client.memory.get_memory_summary()
```

**运行测试:**
```bash
python tests/verify_imports.py
python tests/test_memory.py
pytest tests/
```

**查看文档:**
```bash
cat docs/MEMORY_QUICKSTART.md
cat docs/MEMORY_USAGE.md
```

---

**最后更新**: 2024-02-14  
**文档总数**: 6 份  
**总内容**: 36.9 KB

开始阅读: [MEMORY_QUICKSTART.md](MEMORY_QUICKSTART.md) ⭐

# Tests Directory

所有测试文件已组织到 `tests/` 目录下。

## 📁 文件结构

```
tests/
├── __init__.py                  # Python 包初始化
├── conftest.py                  # pytest 配置（导入路径设置）
├── run_all_tests.py            # 运行所有测试的脚本
├── test_memory.py              # 长期和短期记忆功能测试
├── test_glm.py                 # GLM 客户端基础测试
├── test_auto_skills.py         # 自动技能加载测试
├── test_agent_skill.py         # 代理技能测试
├── test_full_search.py         # 完整搜索功能测试
├── test_gnews_dates.py         # GNews 日期验证测试
├── test_news_debug.py          # 新闻搜索调试测试
├── test_search_detailed.py     # 详细搜索测试
└── test_tavily.py              # Tavily API 测试
```

## 🚀 运行测试

### 1. 运行所有测试
```bash
python tests/run_all_tests.py
```

### 2. 运行单个测试
```bash
cd mac_agent_skills
python tests/test_memory.py
python tests/test_glm.py
python tests/test_agent_skill.py
```

### 3. 使用 pytest（如果安装了）
```bash
pytest tests/
pytest tests/test_memory.py -v
```

## ✨ 测试说明

### Memory Tests
- **test_memory.py** - 演示长期记忆系统功能
  - 保存/读取偏好
  - 保存/读取上下文
  - 历史记录管理
  - 导入导出备份

### GLM Client Tests
- **test_glm.py** - 基础 GLM 客户端测试
- **test_auto_skills.py** - 技能自动加载测试
- **test_agent_skill.py** - 具体技能测试

### News Search Tests
- **test_full_search.py** - 完整搜索结果测试
- **test_gnews_dates.py** - GNews 日期范围测试
- **test_news_debug.py** - 多数据源搜索测试
- **test_search_detailed.py** - 详细搜索统计
- **test_tavily.py** - Tavily API 直接测试

## 🔧 导入路径配置

所有测试都已配置为从父目录导入主模块：

```python
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from glm_langchain_client import GLMClient
from memory_manager import MemoryManager
```

这样可以在任何位置运行测试，无需设置 PYTHONPATH。

## 🧪 conftest.py

`conftest.py` 文件为 pytest 自动提供路径配置：

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
```

## 📝 添加新测试

1. 在 `tests/` 目录下创建 `test_*.py` 文件
2. 在文件开头添加导入路径配置：
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
```
3. 编写测试代码
4. 运行测试验证

## ✅ 验证

所有测试文件已验证：
- ✓ Python 编译通过
- ✓ 导入路径正确
- ✓ 可从任何位置运行
- ✓ 支持 pytest 框架

## 🔍 常见问题

**Q: 从项目根目录运行测试？**
```bash
python -m pytest tests/
# 或
cd mac_agent_skills && python tests/run_all_tests.py
```

**Q: 导入找不到模块？**
检查 `sys.path.insert(0, str(Path(__file__).parent.parent))` 是否在所有测试开头

**Q: 相对路径问题？**
所有相对路径已改为使用 `Path(__file__).parent.parent` + 相对路径

## 📚 相关文档

- 主文档: `../MEMORY_USAGE.md`
- 快速指南: `../MEMORY_QUICKSTART.md`
- 实现细节: `../MEMORY_IMPLEMENTATION_SUMMARY.md`

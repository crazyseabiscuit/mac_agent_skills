#!/usr/bin/env python3
"""Test readline support for better input editing."""
import readline

print("=== 测试 readline 输入编辑 ===\n")
print("说明：")
print("- 现在可以使用退格键删除任何字符（包括第一个字）")
print("- 可以使用左右箭头键移动光标")
print("- 可以使用 Ctrl+A 跳到行首，Ctrl+E 跳到行尾")
print("- 可以使用 Ctrl+K 删除光标后的所有内容")
print("- 可以使用上下箭头键查看历史命令\n")

print("试试输入一些文字，然后用退格键删除第一个字：")
print("例如：输入 '棒查找新闻'，然后删除 '棒' 字\n")

try:
    user_input = input("测试输入: ").strip()
    print(f"\n你输入的是: {user_input}")
    print("\n✅ 如果你成功删除了第一个字，说明 readline 工作正常！")
except KeyboardInterrupt:
    print("\n\n测试结束")

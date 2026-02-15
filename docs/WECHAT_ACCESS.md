# 在微信中访问 GLM Terminal

## 🎯 方案概述

通过创建 Web 界面，让你可以在微信浏览器中使用 GLM Terminal。

## 📋 准备工作

### 1. 安装 Flask
```bash
pip install flask
```

### 2. 确保环境变量已设置
```bash
export ZHIPUAI_API_KEY="your-api-key"
```

## 🚀 启动 Web 服务

### 本地测试
```bash
python glm_web.py
```

你会看到：
```
🚀 GLM Web Assistant starting...
📱 Access from WeChat: http://your-ip:5000
💻 Local access: http://localhost:5000
```

### 在浏览器中测试
打开 http://localhost:5000

## 📱 在微信中访问

### 方案 1：局域网访问（最简单）

**适用场景**：手机和电脑在同一 WiFi

1. **获取电脑 IP 地址**：
   ```bash
   # macOS
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # 或者
   ipconfig getifaddr en0
   ```
   
   假设得到：`192.168.1.100`

2. **启动服务**：
   ```bash
   python glm_web.py
   ```

3. **在微信中访问**：
   - 打开微信
   - 在任意聊天窗口发送：`http://192.168.1.100:5000`
   - 点击链接即可打开

### 方案 2：使用 ngrok（推荐，可外网访问）

**适用场景**：需要从任何地方访问

1. **安装 ngrok**：
   ```bash
   # macOS
   brew install ngrok
   
   # 或下载：https://ngrok.com/download
   ```

2. **注册并获取 token**：
   - 访问 https://ngrok.com
   - 注册账号
   - 复制 authtoken

3. **配置 ngrok**：
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

4. **启动 GLM Web**：
   ```bash
   python glm_web.py
   ```

5. **在另一个终端启动 ngrok**：
   ```bash
   ngrok http 5000
   ```
   
   你会看到：
   ```
   Forwarding  https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:5000
   ```

6. **在微信中访问**：
   - 复制 ngrok 提供的 https 链接
   - 在微信中发送并点击
   - 即可使用！

### 方案 3：部署到云服务器（长期使用）

**适用场景**：需要 24/7 可用

1. **购买云服务器**（阿里云、腾讯云等）

2. **上传代码**：
   ```bash
   scp -r mac_agent_skills user@your-server:/path/
   ```

3. **在服务器上运行**：
   ```bash
   ssh user@your-server
   cd /path/mac_agent_skills
   export ZHIPUAI_API_KEY="your-key"
   nohup python glm_web.py &
   ```

4. **配置域名**（可选）：
   - 购买域名
   - 配置 DNS 指向服务器 IP
   - 配置 Nginx 反向代理

5. **在微信中访问**：
   - `http://your-domain.com:5000`
   - 或配置 Nginx 后：`https://your-domain.com`

## 🎨 功能特性

### Web 界面包含：
- ✅ 微信风格的聊天界面
- ✅ 自动执行搜索命令
- ✅ 中文总结搜索结果
- ✅ 会话历史记录
- ✅ 移动端适配

### 支持的功能：
- ✅ 新闻搜索
- ✅ 中国内容搜索（电影、电视剧）
- ✅ 任务管理
- ✅ 对话记忆

## 🔒 安全建议

### 1. 添加密码保护
在 `glm_web.py` 中添加：
```python
from functools import wraps

PASSWORD = "your-password"

def check_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth != PASSWORD:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/chat', methods=['POST'])
@check_auth
def chat():
    # ...
```

### 2. 使用 HTTPS
- 使用 ngrok（自动提供 HTTPS）
- 或在服务器上配置 SSL 证书

### 3. 限制访问
```python
# 只允许特定 IP 访问
ALLOWED_IPS = ['192.168.1.100', '10.0.0.1']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

## 📊 使用示例

### 在微信中：

**你**：今天有什么足球新闻

**助手**：
```
[正在搜索...]

搜索新闻: 足球

1. Manchester City make quick work of Fulham...
2. Harry Maguire likely to sign new contract...
3. Arne Slot: It won't be acceptable...

根据搜索结果，今天值得关注的足球新闻包括：
1. 曼城轻松击败富勒姆，但哈兰德因小伤提前下场
2. 曼联后卫马奎尔可能签署新合同
3. 利物浦主帅斯洛特表示如果无法获得欧冠资格将不可接受
```

## 🐛 故障排除

### 问题 1：无法访问
- 检查防火墙是否允许 5000 端口
- 确认电脑和手机在同一网络
- 尝试使用 `0.0.0.0` 而不是 `localhost`

### 问题 2：命令执行失败
- 确认 `ZHIPUAI_API_KEY` 已设置
- 检查 skills 文件夹路径是否正确
- 查看终端错误日志

### 问题 3：微信无法打开链接
- 使用 HTTPS（ngrok 自动提供）
- 或在微信中选择"在浏览器中打开"

## 💡 进阶功能

### 添加语音输入
```html
<button onclick="startVoice()">🎤</button>
<script>
function startVoice() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'zh-CN';
    recognition.onresult = (e) => {
        document.getElementById('input').value = e.results[0][0].transcript;
    };
    recognition.start();
}
</script>
```

### 添加图片上传
```python
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    # 处理图片...
    return jsonify({'result': 'success'})
```

## 📝 总结

**推荐方案**：
- 🏠 **在家使用**：方案 1（局域网）
- 🌍 **外出使用**：方案 2（ngrok）
- 🏢 **长期使用**：方案 3（云服务器）

**最快开始**：
```bash
pip install flask
python glm_web.py
# 在微信中访问 http://your-ip:5000
```

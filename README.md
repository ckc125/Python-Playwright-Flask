# 🌐 网页截图和录屏工具

一个基于 Python + Playwright + Flask 的网页截图和录屏工具，支持对任意网页进行截图和视频录制。

## ✨ 功能特性

- 📸 **网页截图**：支持完整页面截图（滚动截图）
- 🎥 **视频录制**：可录制网页操作视频（最长60秒）
- 📏 **自定义宽度**：支持800-3840像素自定义宽度
- 🖼️ **多种格式**：支持PNG、JPG、PDF、GIF四种格式
- 🎨 **美观界面**：现代化的Web界面，响应式设计
- ⚡ **高性能**：基于Playwright的无头浏览器
- 📱 **移动友好**：支持移动端访问
- 🔒 **安全可靠**：输入验证和错误处理

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Windows/Linux/macOS

### 安装步骤

1. **克隆或下载项目**

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **安装Playwright浏览器**
```bash
python -m playwright install chromium
```

4. **启动服务**
```bash
python run.py
```

5. **访问应用**
打开浏览器访问：http://localhost:5000

### 一键启动（推荐）

直接运行 `run.py` 脚本，它会自动检查依赖并启动服务：

```bash
python run.py
```

## 📖 使用方法

### 网页截图

1. 在输入框中输入网页URL
2. 选择是否截取完整页面
3. 设置自定义宽度（800-3840像素）
4. 选择截图格式（PNG、JPG、PDF、GIF）
5. 点击"📸 截图网页"按钮
6. 等待处理完成，下载截图文件

### 视频录制

1. 在输入框中输入网页URL
2. 选择录制时长（5-60秒）
3. 点击"🎥 录制视频"按钮
4. 等待录制完成，下载视频文件

## 🏗️ 项目结构

```
web-screenshot-recorder/
├── app.py                 # Flask主应用
├── screenshot_service.py  # 截图服务
├── video_service.py       # 视频录制服务
├── run.py                 # 启动脚本
├── requirements.txt       # 依赖列表
├── templates/
│   └── index.html         # Web界面
├── output/
│   ├── screenshots/       # 截图保存目录
│   └── videos/           # 视频保存目录
└── README.md             # 说明文档
```

## 🔧 API接口

### 截图接口

```http
POST /screenshot
Content-Type: application/json

{
    "url": "https://example.com",
    "full_page": true,
    "width": 1920,
    "format": "png"
}
```

### 录制接口

```http
POST /record
Content-Type: application/json

{
    "url": "https://example.com",
    "duration": 10
}
```

### 下载接口

```http
GET /download/screenshots/{filename}
GET /download/videos/{filename}
```

## ⚙️ 配置选项

### 截图选项

- `full_page`: 是否截取完整页面（默认：true）
- `width`: 自定义宽度，800-3840像素（默认：1920）
- `format`: 截图格式，支持PNG、JPG、PDF、GIF（默认：PNG）

### 录制选项

- `duration`: 录制时长，单位秒（默认：10，最大：60）
- 视频格式：WebM
- 分辨率：1920x1080

## 🐛 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **浏览器安装失败**
   ```bash
   # 手动安装浏览器
   python -m playwright install --with-deps chromium
   ```

3. **端口被占用**
   ```bash
   # 修改端口
   python app.py --port 8080
   ```

### 错误代码

- `400`: 请求参数错误
- `404`: 文件不存在
- `500`: 服务器内部错误

## 🔒 安全注意事项

- 仅用于合法用途
- 不要录制敏感信息
- 注意版权问题
- 建议在内网环境使用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Playwright](https://playwright.dev/) - 强大的浏览器自动化工具
- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架
- 所有贡献者和用户
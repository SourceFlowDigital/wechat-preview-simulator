# 微信图文预览模拟器 · WeChat Preview Simulator

在 PC 浏览器中模拟微信公众号文章的**真实手机渲染效果**。

375px 宽度锁定，完全仿照微信公众号内置浏览器样式。

## 功能

- 📱 **iPhone 外框模拟** — 真实手机比例，含状态栏和地址栏装饰
- 📂 **文件列表扫描** — 自动扫描指定目录下的 HTML 图文文件
- 🎨 **微信样式注入** — 自动注入微信公众号正文样式（字体/行高/图片宽度）
- ⚡ **即时预览** — 选择文件即可在手机框中渲染

## 技术栈

| 层 | 技术 |
|---|------|
| 后端 | Python FastAPI |
| 前端 | 纯 HTML/CSS/JS，零框架 |
| 运行时 | Uvicorn |

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置扫描目录（可选，默认值见下方）
export WECHAT_PREVIEW_SCAN_DIR=/path/to/your/html/files

# 3. 启动服务
uvicorn main:app --host 0.0.0.0 --port 8007

# 4. 访问
# http://localhost:8007
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 模拟器页面 |
| GET | `/files` | 返回扫描目录下的 HTML 文件列表 |
| GET | `/content?file=xxx` | 返回指定文件内容（已注入微信样式） |

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `WECHAT_PREVIEW_SCAN_DIR` | `/root/new-energy-policy-platform/wechat_push/output/` | HTML 文件扫描目录 |

## 作者

宁夏源流数字服务有限公司 · SourceFlow Digital

## License

MIT

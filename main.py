"""
微信公众图文手机预览模拟器 · FastAPI 后端
端口 8007，独立运行
"""
import os
import re
from datetime import datetime

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

# ── 配置 ──────────────────────────────────────────────
SCAN_DIR = os.getenv(
    "WECHAT_PREVIEW_SCAN_DIR",
    "/root/new-energy-policy-platform/wechat_push/output/",
)

app = FastAPI(title="微信预览模拟器", version="1.0.0")

# ── 微信正文基础样式（注入到 iframe 内容中）────────────
WECHAT_BASE_STYLES = """
<style>
    body {
        background: #ffffff;
        max-width: 375px;
        margin: 0 auto;
        padding: 0 0 20px 0;
        font-family: -apple-system, "PingFang SC", "Helvetica Neue", sans-serif;
        font-size: 15px;
        line-height: 1.8;
        color: #333333;
        word-break: break-word;
    }
    img { max-width: 100% !important; height: auto !important; display: block; margin: 0 auto; }
    p { margin: 0 0 1em 0; }
    h1, h2, h3, h4 { font-weight: 600; margin: 1.2em 0 0.6em 0; }
    h1 { font-size: 22px; }
    h2 { font-size: 18px; }
    h3 { font-size: 16px; }
    blockquote {
        margin: 0; padding: 0 0 0 10px;
        border-left: 3px solid #d9d9d9;
        color: #888888;
    }
    a { color: #576b95; text-decoration: none; }
    table { width: 100%; border-collapse: collapse; margin: 10px 0; }
    td, th { border: 1px solid #e0e0e0; padding: 6px 10px; font-size: 14px; }
    ul, ol { padding-left: 1.5em; }
    li { margin-bottom: 0.3em; }
</style>
"""


# ── API 接口 ──────────────────────────────────────────

@app.get("/files")
async def list_files():
    """扫描 output 目录，返回 .html 文件列表（按修改时间倒序）"""
    if not os.path.exists(SCAN_DIR):
        return {
            "files": [],
            "error": f"扫描目录不存在: {SCAN_DIR}",
            "scan_dir": SCAN_DIR,
        }

    entries = []
    for f in os.listdir(SCAN_DIR):
        if f.lower().endswith((".html", ".htm")):
            fp = os.path.join(SCAN_DIR, f)
            try:
                stat = os.stat(fp)
                entries.append({
                    "name": f,
                    "size": stat.st_size,
                    "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "mtime_ts": stat.st_mtime,
                })
            except OSError:
                continue

    entries.sort(key=lambda x: x["mtime_ts"], reverse=True)

    return {"files": entries, "scan_dir": SCAN_DIR, "count": len(entries)}


@app.get("/content", response_class=HTMLResponse)
async def get_content(file: str = Query(..., description="文件名")):
    """返回指定 HTML 文件内容（已注入微信正文样式）"""
    # 防路径穿越
    filename = os.path.basename(file)
    filepath = os.path.join(SCAN_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"文件不存在: {filename}")

    with open(filepath, "r", encoding="utf-8") as fh:
        content = fh.read()

    # 注入微信样式
    if "</head>" in content:
        content = content.replace("</head>", WECHAT_BASE_STYLES + "</head>")
    elif re.search(r"<body[^>]*>", content):
        content = re.sub(r"(<body[^>]*>)", r"\1" + WECHAT_BASE_STYLES, content)
    else:
        content = (
            '<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=375">'
            + WECHAT_BASE_STYLES +
            '</head><body>' + content + '</body></html>'
        )

    return HTMLResponse(content=content)


@app.get("/")
async def root():
    """返回前端模拟器页面"""
    return FileResponse("index.html")

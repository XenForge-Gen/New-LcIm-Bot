# LCIM Bot
> 基于 Flask 的 LCIM 开放接口机器人
> A LCIM OpenAPI Bot powered by Flask

## 📖 介绍｜Introduction
这是一个轻量机器人后端，对接 LCIM 开放平台 Webhook。可以接收消息、自动回复，监听撤回与已读事件，部署在 Render 云端，自带 HTTPS，不需要本地长期开机。
This is a lightweight bot backend connecting to the LCIM OpenAPI Webhook. It can receive messages, auto-reply, listen for recall and read events. Deployed on Render with native HTTPS, no need to keep your local computer online.

## ✨ 功能｜Features
- 接收 LCIM 推送的各类事件
  Receive all kinds of events pushed by LCIM
- 根据指令自动回复文本
  Auto reply text according to commands
- 支持 `/ping`、`/help` 指令
  Support commands: `/ping`, `/help`
- 捕获消息撤回、消息已读事件
  Capture message recall and message-read events

## 📦 项目文件｜Project Files
- `main.py`：主程序入口
  `main.py`: Main entry
- `requirements.txt`：Python 依赖
  `requirements.txt`: Python dependencies
- `render.yaml`：Render 部署配置
  `render.yaml`: Render deployment config

## 🚀 部署教程｜Deployment Guide
### 前置准备｜Prerequisites
1. 准备好 LCIM 的 `APP_ID` 和 `APP_SECRET`
   Get your `APP_ID` and `APP_SECRET` from LCIM
2. GitHub 账号，新建公开仓库
   A GitHub account, create a public repository
3. Render 账号，使用 GitHub 登录
   A Render account, sign in with GitHub

### 步骤 1：上传代码｜Step 1: Upload code
把下面三个文件上传到仓库根目录：
Upload these three files to the root of your repository:
- `main.py`
- `requirements.txt`
- `render.yaml`

同时上传本文件 `README.md`。
Also upload this `README.md`.

### 步骤 2：在 Render 创建服务｜Step 2: Create service on Render
1. 进入 Render 控制台 → `New` → `Web Service`
   Go to Render Dashboard → `New` → `Web Service`
2. 选中刚刚建好的 GitHub 仓库
   Select your GitHub repository
3. 配置项保持默认，确认部署
   Keep default settings and confirm deployment

### 步骤 3：环境变量配置｜Step 3: Environment variables
在 Render 的环境变量页面填入：
Add these environment variables in Render:

| 变量名 Name | 说明 Description |
| ---- | ---- |
| `APP_ID` | LCIM 应用 ID \| LCIM App ID |
| `APP_SECRET` | LCIM 应用密钥 \| LCIM App Secret |
| `REAL_SEND` | `False`（调试） / `True`（正式发消息） \| `False` for test / `True` to send real messages |

> 不要把密钥写到代码里上传到 GitHub！
> Never write secrets into your code and push to GitHub.

### 步骤 4：配置 Webhook｜Step 4: Set Webhook
部署成功后，复制 Render 给出的域名，拼接得到 Webhook 地址：
After deployment, copy your Render domain to get the Webhook URL:

把这条完整链接填入 LCIM 后台的 Webhook 设置。
Paste this full URL into the Webhook field on LCIM admin panel.

### 步骤 5：测试｜Step 5: Test
先保持 `REAL_SEND=False`，发送消息测试，查看 Render 日志确认收到事件；调试无误后，改为 `True` 开启真实回复。
Keep `REAL_SEND=False` at first. Send a message and check Render logs. Switch to `True` to enable real replies once everything works.

## ⚠️ 注意事项｜Notes
- Render 免费实例闲置 15 分钟后休眠，第一条消息冷启动较慢
  Free Render instance sleeps after 15 minutes idle. The first message may be slow.
- 如果想要减少休眠，可以使用定时访问保活
  You can use periodic ping service to reduce sleeping
- 所有密钥仅存放于 Render 后台环境变量
  All secrets are stored only in Render environment variables



https://www.lcim.site/bot/

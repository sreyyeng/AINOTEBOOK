# Telegram Bot 部署完整教程

## 🎯 部署概览

我们将使用：
- **Telegram Bot**: 作为用户界面
- **Railway.app**: 免费服务器托管
- **DeepSeek API**: AI分析（便宜）
- **JSON文件**: 数据存储（简单）

**总耗时**: 15-20分钟
**月度成本**: ¥1-2元（仅API费用）

---

## 📋 准备工作清单

在开始之前，准备好：
- [ ] Telegram账号
- [ ] Github账号
- [ ] DeepSeek API Key
- [ ] 电脑或手机浏览器

---

## 第一步：创建Telegram Bot（3分钟）⭐

### 1.1 找到BotFather
在Telegram搜索框输入：`@BotFather`

点击进入对话

### 1.2 创建新Bot
发送命令：`/newbot`

BotFather会问两个问题：

**问题1**: Bot的显示名称
```
例如：我的AI记事本
或者：My AI Notebook
```

**问题2**: Bot的用户名（必须以bot结尾）
```
例如：my_ai_notebook_bot
或者：john_notebook_bot
```

### 1.3 保存Token
创建成功后，会收到类似这样的消息：
```
Done! Congratulations on your new bot...
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure...
```

**⚠️ 重要：复制这个Token，马上要用！**

---

## 第二步：获取DeepSeek API Key（3分钟）⭐

### 2.1 注册DeepSeek账号
访问：https://platform.deepseek.com/

点击右上角"注册"，可以用：
- 手机号
- 邮箱

### 2.2 创建API Key
1. 登录后，点击左侧 "API Keys"
2. 点击 "创建新的API Key"
3. 给Key起个名字（比如：notebook_bot）
4. 点击"创建"

### 2.3 保存API Key
创建后会显示：`sk-xxxxxxxxxxxxxxxxxx`

**⚠️ 重要：复制并保存，只显示一次！**

---

## 第三步：选择免费服务器 ⭐⭐⭐

### 推荐方案对比

| 服务商 | 免费额度 | 优势 | 劣势 | 推荐指数 |
|--------|---------|------|------|---------|
| Railway | 500小时/月 | 最简单，自动部署 | 需要Github | ⭐⭐⭐⭐⭐ |
| Render | 750小时/月 | 完全免费 | 15分钟无活动会休眠 | ⭐⭐⭐⭐ |
| Fly.io | 3个实例 | 性能好 | 需信用卡验证 | ⭐⭐⭐ |

**我推荐Railway** - 最简单，最适合新手！

---

## 第四步：部署到Railway（最推荐）⭐⭐⭐⭐⭐

### 4.1 准备代码

#### 方案A：用Github（推荐）

1. 去Github创建新仓库
2. 把这些文件上传：
   - `telegram_bot.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`

#### 方案B：直接上传（简单）
Railway也支持直接上传文件夹

### 4.2 注册Railway
1. 访问：https://railway.app/
2. 点击右上角 "Login"
3. 选择 "Login with GitHub"（用Github登录）

### 4.3 创建新项目
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你刚才创建的仓库
4. 点击 "Deploy Now"

### 4.4 设置环境变量
部署后，需要设置两个环境变量：

1. 在项目页面点击 "Variables"
2. 添加变量：

```
变量名: TELEGRAM_BOT_TOKEN
变量值: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
(你的Telegram Bot Token)
```

3. 点击 "Add"

### 4.5 重新部署
添加变量后，点击 "Deploy" → "Redeploy"

### 4.6 检查状态
在 "Deployments" 页面，看到 "Success" 就成功了！

---

## 第五步：配置Bot（2分钟）⭐

### 5.1 找到你的Bot
在Telegram搜索你创建的Bot用户名（例如：`@my_ai_notebook_bot`）

### 5.2 启动Bot
点击 "Start" 或发送 `/start`

Bot会回复欢迎消息

### 5.3 设置API Key
发送命令：
```
/setkey sk-xxxxxxxxxxxxxxxxxx
```
（换成你的DeepSeek API Key）

看到 "✅ API Key已设置成功！" 就完成了！

---

## 第六步：开始使用！🎉

### 试试这些命令：

```
今天上午10点开会讨论新项目，开了2小时
```
Bot会自动记录并分类

```
/recent
```
查看最近记录

```
/categories
```
查看分类统计

```
/search 开会
```
搜索包含"开会"的记录

```
/summary
```
AI生成总结报告

---

## 🔧 故障排除

### 问题1：Bot没反应
**原因**：服务器可能没启动
**解决**：
1. 去Railway检查部署状态
2. 查看 "Logs" 是否有错误
3. 确认环境变量是否设置正确

### 问题2：提示"请先设置API Key"
**原因**：DeepSeek API Key未设置
**解决**：发送 `/setkey sk-你的key`

### 问题3：API调用失败
**原因**：API Key无效或余额不足
**解决**：
1. 去 https://platform.deepseek.com/ 检查余额
2. 重新创建API Key

### 问题4：Railway显示错误
**原因**：代码文件缺失或配置错误
**解决**：
1. 确认所有文件都上传了
2. 检查 `requirements.txt` 内容
3. 查看错误日志

---

## 📊 Railway免费额度说明

Railway免费套餐：
- **500小时/月**的运行时间
- 每月500小时 ÷ 24小时 = **约20天**
- 轻度使用完全够用

**省流量技巧**：
- Bot会自动休眠，收到消息才唤醒
- 一般能用满30天

如果不够用：
- 可以换到Render（完全免费，但会休眠）
- 或者付费升级（$5/月无限制）

---

## 🎁 进阶功能

### 添加定时任务（每晚提醒记录）

在Railway添加一个定时任务，每晚9点发消息提醒你记录。

需要修改代码添加：
```python
# 每天21:00提醒
from telegram.ext import JobQueue

async def daily_reminder(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text="📝 今天做了什么呢？记得记录一下哦~"
    )

# 设置定时任务
job_queue.run_daily(daily_reminder, time=datetime.time(hour=21))
```

### 添加语音输入支持

```python
from telegram import Voice

async def handle_voice(update, context):
    # 下载语音文件
    voice = await update.message.voice.get_file()
    # 使用语音转文字API（比如百度API）
    # 然后记录
```

---

## 🌟 其他免费服务器部署方案

### 方案B：Render.com

**优势**：完全免费，无时间限制
**劣势**：15分钟无活动会休眠

#### 部署步骤：
1. 访问 https://render.com/
2. 用Github登录
3. New → Web Service
4. 选择你的Github仓库
5. 设置：
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python telegram_bot.py`
6. 添加环境变量 `TELEGRAM_BOT_TOKEN`
7. Deploy

### 方案C：Fly.io

**优势**：性能好，稳定
**劣势**：需要信用卡验证（不扣费）

#### 部署步骤：
1. 安装 Fly CLI
2. `flyctl auth signup`
3. `flyctl launch`
4. 设置环境变量：`flyctl secrets set TELEGRAM_BOT_TOKEN=xxx`
5. `flyctl deploy`

---

## 💾 数据备份

### 自动备份到Github

可以定期把 `notebook_data.json` 备份到Github：

```python
import subprocess

def backup_data():
    subprocess.run(["git", "add", "notebook_data.json"])
    subprocess.run(["git", "commit", "-m", "Auto backup"])
    subprocess.run(["git", "push"])

# 每天备份一次
job_queue.run_daily(backup_data, time=datetime.time(hour=3))
```

### 手动导出

发送命令 `/export` 可以接收JSON文件

---

## 📱 使用技巧

### 1. 快速记录
直接发消息，无需任何命令：
```
早上7点起床跑步5公里
```

### 2. 模糊时间也行
```
昨天晚上看了电影
上周二去体检
今天下午开会
```

### 3. 批量记录
```
今天上午9点晨会半小时，10点开始写代码写到12点，
下午2点需求评审1小时，晚上7点健身1小时
```

AI会自动拆分成4条记录

### 4. 搜索技巧
```
/search 会议
/search 运动
/search 电影
```

---

## ⚙️ 成本优化

### DeepSeek费用估算
- 每次记录：~500 tokens
- 价格：¥0.001/千tokens
- 每天10条记录：10 × 500 × 0.001/1000 = ¥0.005
- **一个月才¥0.15！**

### Railway费用
- 免费500小时/月
- 实际使用：~300小时/月（够用）
- **免费！**

### 总成本：¥0.15-2元/月

---

## 🎉 完成！

恭喜！你的AI记事簿Bot已经上线了！

**快捷链接：**
- Railway控制台：https://railway.app/dashboard
- DeepSeek控制台：https://platform.deepseek.com/
- Bot使用说明：发送 `/help` 给Bot

**有问题随时问我！**

---

## 📞 常见问题

**Q: 数据存在哪里？**
A: 存在Railway服务器的 `notebook_data.json` 文件中

**Q: 会不会丢失数据？**
A: Railway会持久化存储，但建议定期备份

**Q: 可以多人使用吗？**
A: 可以，但所有人共享一个数据库（建议每人一个Bot）

**Q: 可以换成其他AI吗？**
A: 可以，改代码里的API地址和格式即可

**Q: 能加语音输入吗？**
A: 可以，需要接入语音转文字API（如百度、阿里云）

**Q: 将来能转到微信小程序吗？**
A: 完全可以，核心逻辑一样

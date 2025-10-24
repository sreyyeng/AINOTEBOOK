# 免费服务器详细选择指南

## 🎯 三大免费服务器对比

### 对比表格

| 特性 | Railway ⭐⭐⭐⭐⭐ | Render ⭐⭐⭐⭐ | Fly.io ⭐⭐⭐ |
|------|---------|--------|---------|
| **免费额度** | 500小时/月 | 750小时/月 | 3个实例 |
| **部署难度** | ⭐ 极简单 | ⭐⭐ 简单 | ⭐⭐⭐ 中等 |
| **需要信用卡** | ❌ 不需要 | ❌ 不需要 | ✅ 需要 |
| **自动休眠** | ❌ 不休眠 | ✅ 15分钟休眠 | ❌ 不休眠 |
| **唤醒速度** | N/A | ~30秒 | N/A |
| **稳定性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **数据持久化** | ✅ 支持 | ✅ 支持 | ✅ 支持 |
| **日志查看** | ✅ 实时 | ✅ 实时 | ✅ 实时 |
| **国内访问** | ✅ 正常 | ⚠️ 偶尔慢 | ✅ 正常 |
| **适合场景** | 个人Bot | 低频Bot | 商业项目 |

---

## 方案一：Railway（最推荐）⭐⭐⭐⭐⭐

### 为什么选Railway？
1. ✅ **最简单** - 连接Github就能自动部署
2. ✅ **不休眠** - Bot一直在线，随时响应
3. ✅ **无需信用卡** - 注册就能用
4. ✅ **500小时够用** - 轻度使用约20天
5. ✅ **实时日志** - 方便调试

### Railway详细部署步骤

#### 1. 准备Github仓库

**选项A：使用我的代码（推荐）**
1. 去Github创建新仓库（名字随意，比如：`ai-notebook-bot`）
2. 上传以下文件：
   ```
   telegram_bot.py
   requirements.txt
   Procfile
   railway.json
   ```

**选项B：Fork我的仓库**
如果我把代码放到Github，你可以直接Fork

#### 2. 注册Railway
1. 打开：https://railway.app/
2. 点击 "Login"
3. 选择 "Login with GitHub"
4. 授权Railway访问你的Github

#### 3. 创建项目
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 在列表中找到你的仓库
4. 点击仓库名称
5. Railway会自动开始部署

#### 4. 等待首次部署
- 大约需要2-3分钟
- 可以点击 "View Logs" 查看进度
- 看到 "Bot启动成功！" 表示成功

#### 5. 设置环境变量
1. 点击项目卡片
2. 点击 "Variables" 标签
3. 点击 "New Variable"
4. 添加：
   ```
   Name: TELEGRAM_BOT_TOKEN
   Value: 你的Bot Token（从BotFather获取）
   ```
5. 点击 "Add"

#### 6. 重新部署
- Railway会自动检测到变量变化并重新部署
- 或者手动点击 "Deploy" → "Redeploy"

#### 7. 验证部署
1. 在Telegram找到你的Bot
2. 发送 `/start`
3. 看到欢迎消息表示成功！

### Railway界面说明

**主界面**：
- 📊 Deployments - 部署历史
- 📝 Logs - 实时日志
- ⚙️ Settings - 设置
- 💾 Variables - 环境变量
- 📈 Metrics - 使用统计

**查看使用情况**：
Settings → Usage
可以看到已用小时数

**查看日志**：
点击 "Logs" 可以看到：
```
Bot启动成功！
处理用户消息: 今天...
记录成功
```

### Railway费用说明

**免费套餐**：
- 500小时/月
- 512MB RAM
- 1GB磁盘
- 无限流量

**超额怎么办？**
- 月底会重置
- 或者升级到 $5/月（无限制）

**实际使用**：
- Bot很轻量，500小时能用20-30天
- 如果24小时运行：500÷24≈21天

**省流量技巧**：
- 代码已优化，空闲时自动降低资源占用
- 一般能用满一个月

---

## 方案二：Render（完全免费）⭐⭐⭐⭐

### 为什么选Render？
1. ✅ **完全免费** - 无时间限制
2. ✅ **750小时** - 比Railway更多
3. ⚠️ **会休眠** - 15分钟无活动自动休眠
4. ⚠️ **唤醒慢** - 第一次响应需30秒

### 适合场景
- 低频使用（每小时才发几条消息）
- 不介意首次响应慢一点
- 想完全免费

### Render详细部署步骤

#### 1. 注册Render
1. 访问：https://render.com/
2. 点击 "Get Started"
3. 用Github登录

#### 2. 创建Web Service
1. 点击 "New +"
2. 选择 "Web Service"
3. 选择你的Github仓库

#### 3. 配置服务
```
Name: ai-notebook-bot（随意）
Region: Oregon (US West)（选最近的）
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python telegram_bot.py
```

#### 4. 选择免费套餐
- 在 "Instance Type" 选择 "Free"

#### 5. 添加环境变量
在 "Environment Variables" 部分：
```
Key: TELEGRAM_BOT_TOKEN
Value: 你的Token
```

#### 6. 部署
点击 "Create Web Service"

等待3-5分钟完成部署

### Render休眠机制

**什么时候休眠？**
- 15分钟内没有收到任何请求

**如何唤醒？**
- 用户发送消息时自动唤醒
- 第一条消息响应慢（30秒）
- 之后正常速度

**如何避免休眠？**
方案A：每10分钟ping一次（不推荐，浪费资源）
方案B：付费升级（$7/月不休眠）
方案C：接受休眠（免费）

---

## 方案三：Fly.io（高级用户）⭐⭐⭐

### 为什么选Fly.io？
1. ✅ **性能最好** - 全球边缘节点
2. ✅ **非常稳定** - 企业级可靠性
3. ⚠️ **需要信用卡** - 验证身份（不扣费）
4. ⚠️ **稍复杂** - 需要命令行操作

### 适合场景
- 有一定技术基础
- 追求性能和稳定性
- 不介意绑定信用卡

### Fly.io部署步骤

#### 1. 安装Fly CLI

**Mac/Linux**:
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows**:
下载：https://fly.io/docs/hands-on/install-flyctl/

#### 2. 注册并登录
```bash
flyctl auth signup
# 或者
flyctl auth login
```

#### 3. 创建应用
在项目目录运行：
```bash
flyctl launch
```

选择：
- App name: 自动生成或自定义
- Region: Hong Kong（离中国最近）
- Database: No
- Redis: No

#### 4. 设置环境变量
```bash
flyctl secrets set TELEGRAM_BOT_TOKEN=你的Token
```

#### 5. 部署
```bash
flyctl deploy
```

#### 6. 查看状态
```bash
flyctl status
flyctl logs
```

---

## 🎯 选择建议

### 给新手的建议：

**如果你是第一次部署，选Railway**
- 最简单，点几下就完成
- 界面友好
- 不会休眠

**如果想完全免费，选Render**
- 无限制免费
- 低频使用完全够
- 接受30秒唤醒延迟

**如果你是技术大佬，选Fly.io**
- 性能最好
- 最稳定
- 需要命令行操作

### 我的推荐：

**第一步**：Railway（测试功能）
**第二步**：如果不够用，迁移到Render
**第三步**：如果要商业化，付费升级

---

## 📊 成本对比

### 免费方案
| 服务 | 月成本 | 年成本 |
|------|--------|--------|
| Railway免费 | ¥0 | ¥0 |
| Render免费 | ¥0 | ¥0 |
| Fly.io免费 | ¥0 | ¥0 |
| DeepSeek API | ¥1-2 | ¥12-24 |
| **总计** | **¥1-2** | **¥12-24** |

### 付费方案（如果需要）
| 服务 | 月成本 | 年成本 |
|------|--------|--------|
| Railway付费 | $5 (¥35) | ¥420 |
| Render付费 | $7 (¥50) | ¥600 |
| Fly.io付费 | $5 (¥35) | ¥420 |
| DeepSeek API | ¥1-2 | ¥12-24 |
| **总计** | **¥36-52** | **¥432-624** |

---

## 🔧 迁移指南

### 从Railway迁移到Render

1. 在Render创建新服务
2. 连接同一个Github仓库
3. 设置相同的环境变量
4. 停止Railway服务

### 数据迁移

Railway和Render都用JSON存储，数据在仓库里：

**方法1**：Github自动同步
- 如果数据提交到Github，会自动同步

**方法2**：手动下载上传
- Railway下载 `notebook_data.json`
- 上传到新服务器

---

## 💡 性能优化建议

### 减少API调用
```python
# 缓存分类列表，减少重复分析
cache_categories = {}
```

### 定期备份
```python
# 每天自动备份到Github
def auto_backup():
    # 提交数据文件
    os.system('git add notebook_data.json')
    os.system('git commit -m "Auto backup"')
    os.system('git push')
```

### 监控使用情况
- Railway: Settings → Usage
- Render: Dashboard → Metrics  
- Fly.io: `flyctl status`

---

## ❓ 常见问题

**Q: Railway 500小时用完怎么办？**
A: 月底重置，或升级到$5/月无限制

**Q: Render休眠后数据会丢吗？**
A: 不会，数据持久化存储

**Q: 可以同时用多个服务器吗？**
A: 可以，但数据不会自动同步（需要共享数据库）

**Q: 哪个服务器最稳定？**
A: Fly.io > Railway > Render

**Q: 哪个最省钱？**
A: 都是免费的，成本只有API费用

**Q: 国内访问速度？**
A: Railway ≈ Fly.io > Render

---

## 🎉 开始部署吧！

选好了吗？我推荐：

**第一选择：Railway**
- 简单快速
- 不会休眠
- 新手友好

点击这里开始：https://railway.app/

需要帮助随时问我！

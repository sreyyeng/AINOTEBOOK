#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import logging
from datetime import datetime
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 配置文件
DB_FILE = "notebook_data.json"
CONFIG_FILE = "bot_config.json"

# API配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


class NotebookBot:
    def __init__(self):
        self.config = self.load_config()
        self.data = self.load_data()
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """保存配置"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"categories": [], "events": []}
    
    def save_data(self):
        """保存数据"""
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def analyze_input(self, user_input):
        """调用DeepSeek API分析用户输入"""
        categories_list = [cat["name"] for cat in self.data["categories"]]
        
        prompt = f"""分析用户的记录，完成以下任务：

现有分类：{', '.join(categories_list) if categories_list else '暂无'}

用户说：{user_input}

请以JSON格式返回：
{{
  "category": "选择现有分类或新建一个分类名（尽量复用现有分类）",
  "summary": "用一句话（15字内）总结这件事",
  "timestamp": "事件发生的时间点(格式：YYYY-MM-DD HH:MM)",
  "duration": "持续时长描述（如果有的话，比如'2小时'），没有就填null"
}}

注意：
1. 从用户描述中提取事件实际发生的时间，而不是现在的时间
2. 如果用户提到时长，记录到duration中
3. summary必须简短精炼，一句话概括
4. 如果用户没说具体时间，使用当前时间

当前时间是：{datetime.now().strftime('%Y-%m-%d %H:%M')}

只返回JSON，不要其他解释。"""

        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config.get('deepseek_api_key', '')}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30
            )
            
            result = response.json()
            
            if "error" in result:
                logger.error(f"API错误: {result['error']}")
                return None
            
            content = result['choices'][0]['message']['content']
            content = content.strip()
            if content.startswith('```'):
                content = re.sub(r'^```json\s*|\s*```$', '', content, flags=re.MULTILINE)
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            return None
    
    def add_event(self, user_input):
        """添加事件"""
        analysis = self.analyze_input(user_input)
        
        if not analysis:
            return None, "分析失败，请重试"
        
        # 检查或创建分类
        category_name = analysis["category"]
        category_id = None
        is_new_category = False
        
        for cat in self.data["categories"]:
            if cat["name"] == category_name:
                category_id = cat["id"]
                break
        
        if category_id is None:
            category_id = len(self.data["categories"]) + 1
            self.data["categories"].append({
                "id": category_id,
                "name": category_name,
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            is_new_category = True
        
        # 添加事件
        event = {
            "id": len(self.data["events"]) + 1,
            "category_id": category_id,
            "summary": analysis["summary"],
            "timestamp": analysis["timestamp"],
            "duration": analysis.get("duration"),
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.data["events"].append(event)
        self.save_data()
        
        return event, category_name, is_new_category
    
    def search_events(self, keyword, limit=10):
        """搜索事件"""
        matched = [
            e for e in self.data["events"]
            if keyword.lower() in e["summary"].lower()
        ]
        matched.sort(key=lambda x: x["timestamp"], reverse=True)
        return matched[:limit]
    
    def get_recent_events(self, limit=10):
        """获取最近事件"""
        events = sorted(self.data["events"], key=lambda x: x["timestamp"], reverse=True)
        return events[:limit]
    
    def get_categories_stats(self):
        """获取分类统计"""
        stats = []
        for cat in self.data["categories"]:
            count = sum(1 for e in self.data["events"] if e["category_id"] == cat["id"])
            stats.append({
                "id": cat["id"],
                "name": cat["name"],
                "count": count
            })
        return sorted(stats, key=lambda x: x["count"], reverse=True)
    
    def get_summary(self):
        """生成AI总结"""
        if not self.data["events"]:
            return "暂无记录，无法生成总结"
        
        categories_info = {cat["id"]: cat["name"] for cat in self.data["categories"]}
        recent_events = sorted(self.data["events"], key=lambda x: x["timestamp"], reverse=True)[:30]
        
        events_text = "\n".join([
            f"- [{categories_info.get(e['category_id'], '未知')}] {e['timestamp']}: {e['summary']}" +
            (f" (耗时: {e['duration']})" if e.get('duration') else "")
            for e in recent_events
        ])
        
        prompt = f"""基于以下用户的最近记录，生成一份简要的生活/工作总结：

{events_text}

请从以下角度分析（150字内）：
1. 主要活动分布
2. 时间投入特点
3. 简单建议

用简洁友好的语气回复。"""

        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config.get('deepseek_api_key', '')}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30
            )
            
            result = response.json()
            if "error" in result:
                return "生成总结失败"
            
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"生成总结失败: {e}")
            return "生成总结失败"


# 全局Bot实例
notebook = NotebookBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    
    welcome_text = f"""👋 你好 {user.first_name}！

我是你的AI记事簿，可以帮你：
📝 记录日常事件（自动分类）
🔍 搜索历史记录
📊 生成活动总结
⏰ 智能识别时间

💡 **使用方法：**
直接发消息给我，告诉我你做了什么，我会自动记录。

例如：
• "今天上午10点开会，讨论了2小时"
• "昨天晚上8点跑步半小时"
• "刚吃完午饭"

📱 **快捷命令：**
/recent - 查看最近记录
/categories - 查看分类统计
/search - 搜索记录
/summary - AI总结
/help - 查看帮助

现在就试试吧！告诉我你做了什么 👇"""
    
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助命令"""
    help_text = """📖 **命令列表**

🎯 **记录事件**
直接发送消息，无需命令
例：今天上午10点开会2小时

📋 **查看记录**
/recent - 最近10条记录
/categories - 分类统计
/search 关键词 - 搜索记录

📊 **分析总结**
/summary - AI生成总结报告

⚙️ **设置**
/setkey - 设置DeepSeek API Key

💡 **技巧**
• 说清楚具体时间，AI会更准确
• 可以一次记录多件事
• 支持自然语言时间（昨天、上周二等）"""
    
    await update.message.reply_text(help_text)


async def set_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """设置API Key"""
    if not context.args:
        await update.message.reply_text(
            "请提供DeepSeek API Key\n"
            "用法: /setkey sk-xxxxxxxx\n\n"
            "获取API Key: https://platform.deepseek.com/"
        )
        return
    
    api_key = context.args[0]
    notebook.config['deepseek_api_key'] = api_key
    notebook.save_config()
    
    await update.message.reply_text("✅ API Key已设置成功！")


async def recent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查看最近记录"""
    events = notebook.get_recent_events(10)
    
    if not events:
        await update.message.reply_text("暂无记录")
        return
    
    categories_info = {cat["id"]: cat["name"] for cat in notebook.data["categories"]}
    
    text = "📋 **最近记录**\n\n"
    for event in events:
        cat_name = categories_info.get(event["category_id"], "未知")
        duration = f" `[{event['duration']}]`" if event.get("duration") else ""
        text += f"📁 {cat_name}\n"
        text += f"🕐 {event['timestamp']}{duration}\n"
        text += f"📝 {event['summary']}\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查看分类统计"""
    stats = notebook.get_categories_stats()
    
    if not stats:
        await update.message.reply_text("暂无分类")
        return
    
    text = "📊 **分类统计**\n\n"
    total = sum(s["count"] for s in stats)
    
    for stat in stats:
        percentage = (stat["count"] / total * 100) if total > 0 else 0
        text += f"📁 {stat['name']}: {stat['count']}条 ({percentage:.1f}%)\n"
    
    text += f"\n总计: {total}条记录"
    
    await update.message.reply_text(text)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """搜索记录"""
    if not context.args:
        await update.message.reply_text(
            "请提供搜索关键词\n"
            "用法: /search 开会"
        )
        return
    
    keyword = ' '.join(context.args)
    events = notebook.search_events(keyword)
    
    if not events:
        await update.message.reply_text(f"未找到包含 '{keyword}' 的记录")
        return
    
    categories_info = {cat["id"]: cat["name"] for cat in notebook.data["categories"]}
    
    text = f"🔍 搜索 '{keyword}' 找到 {len(events)} 条：\n\n"
    for event in events:
        cat_name = categories_info.get(event["category_id"], "未知")
        duration = f" `[{event['duration']}]`" if event.get("duration") else ""
        text += f"📁 {cat_name}\n"
        text += f"🕐 {event['timestamp']}{duration}\n"
        text += f"📝 {event['summary']}\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """生成AI总结"""
    await update.message.reply_text("⏳ AI正在分析你的记录...")
    
    summary = notebook.get_summary()
    
    text = f"📊 **AI分析报告**\n\n{summary}"
    await update.message.reply_text(text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理普通消息 - 记录事件"""
    user_input = update.message.text
    
    # 检查API Key
    if not notebook.config.get('deepseek_api_key'):
        await update.message.reply_text(
            "⚠️ 请先设置DeepSeek API Key\n"
            "用法: /setkey sk-xxxxxxxx\n\n"
            "获取API Key: https://platform.deepseek.com/"
        )
        return
    
    # 显示处理中
    processing_msg = await update.message.reply_text("⏳ 正在分析...")
    
    try:
        result = notebook.add_event(user_input)
        
        if result is None:
            await processing_msg.edit_text("❌ 记录失败，请重试")
            return
        
        event, category_name, is_new = result
        
        # 构建回复消息
        status = "🆕 创建新分类" if is_new else "✅ 已记录"
        duration_text = f"\n⏱️ {event['duration']}" if event.get('duration') else ""
        
        reply_text = f"""{status}
📁 {category_name}
🕐 {event['timestamp']}{duration_text}
📝 {event['summary']}"""
        
        await processing_msg.edit_text(reply_text)
        
    except Exception as e:
        logger.error(f"处理消息失败: {e}")
        await processing_msg.edit_text("❌ 处理失败，请重试")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """错误处理"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """主函数"""
    # 从环境变量获取Token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("错误: 请设置环境变量 TELEGRAM_BOT_TOKEN")
        print("或者直接在这里输入Token:")
        token = input("Token: ").strip()
        if not token:
            print("Token不能为空！")
            return
    
    # 创建Application
    application = Application.builder().token(token).build()
    
    # 注册命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setkey", set_api_key))
    application.add_handler(CommandHandler("recent", recent_command))
    application.add_handler(CommandHandler("categories", categories_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("summary", summary_command))
    
    # 注册消息处理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 注册错误处理器
    application.add_error_handler(error_handler)
    
    # 启动Bot
    print("Bot启动成功！")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

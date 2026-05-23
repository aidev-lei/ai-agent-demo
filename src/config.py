"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI配置
OPENAI_API_KEY = "sk-acfb8b76305543c8a9976cbf9057aa72"
OPENAI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-turbo"

# 向量数据库配置
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K = int(os.getenv("TOP_K", "3"))

# 数据目录
DATA_DIR = "./data"

# 提示词模板
SYSTEM_PROMPT = """你是专业的AI客服助手，基于以下知识库为用户解答问题。

【回答规则】
1. 只基于提供的知识库内容回答，不要编造信息
2. 如果知识库中没有答案，诚实告知用户
3. 回答时标注信息来源（如"[来源于: xxx.txt]"）
4. 保持友好、专业的语气
5. 复杂问题分点说明，便于阅读

【工具使用】
当需要查询实时信息（如订单状态、库存等）时，使用提供的工具函数。
"""

RAG_PROMPT_TEMPLATE = """基于以下知识库内容回答用户问题：

【知识库内容】
{context}

【用户问题】
{question}

请根据知识库内容提供准确的回答。如果知识库中没有相关信息，请明确告知。"""

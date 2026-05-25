"""
Agent核心逻辑
"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import (
    OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME, EMBEDDING_MODEL,
    CHROMA_DB_PATH, TOP_K, SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE
)
from src.tools import ToolManager


class CustomerServiceAgent:
    """智能客服Agent"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            temperature=0.7
        )
        
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        
        # 加载向量数据库
        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )
        
        # 工具管理器
        self.tool_manager = ToolManager()
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
    
    def format_docs(self, docs) -> str:
        """格式化检索到的文档"""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', '未知来源')
            content = doc.page_content
            formatted.append(f"[{i}] 来源: {source}\n内容: {content}\n")
        return "\n".join(formatted)
    
    def retrieve(self, query: str) -> List[Any]:
        """检索相关知识"""
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": TOP_K}
        )
        return retriever.invoke(query)
    
    def generate_response(self, question: str, context: str) -> str:
        """生成回答"""
        # 构建消息
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]
        
        # 添加历史对话（保持最近5轮）
        for msg in self.conversation_history[-10:]:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(AIMessage(content=msg['content']))
        
        # 构建当前问题（包含检索到的上下文）
        prompt = RAG_PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )
        messages.append(HumanMessage(content=prompt))
        
        # 调用LLM
        response = self.llm.invoke(messages)
        return response.content
    
    def chat(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入，返回回答
        
        Returns:
            {
                'answer': str,  # AI回答
                'sources': List[str],  # 来源文档
                'used_tools': List[str]  # 使用的工具
            }
        """
        # 1. 检索相关知识
        retrieved_docs = self.retrieve(user_input)
        context = self.format_docs(retrieved_docs)
        
        # 2. 检查是否需要调用工具
        tool_calls = self.tool_manager.detect_tool_need(user_input)
        tool_results = []
        for tool_name in tool_calls:
            result = self.tool_manager.execute_tool(tool_name, user_input)
            tool_results.append(f"[{tool_name}] {result}")
        
        if tool_results:
            context += "\n\n【工具查询结果】\n" + "\n".join(tool_results)
        
        # 3. 生成回答
        answer = self.generate_response(user_input, context)
        
        # 4. 更新对话历史
        self.conversation_history.append({'role': 'user', 'content': user_input})
        self.conversation_history.append({'role': 'assistant', 'content': answer})
        
        # 5. 提取来源
        sources = [doc.metadata.get('source', '未知') for doc in retrieved_docs]
        
        return {
            'answer': answer,
            'sources': list(set(sources)),
            'used_tools': tool_calls
        }
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("✅ 对话历史已清空")

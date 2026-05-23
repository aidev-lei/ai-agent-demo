"""
Streamlit Web界面 - 用于在线演示
"""
import streamlit as st
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent import CustomerServiceAgent
from config import OPENAI_API_KEY

# 页面配置
st.set_page_config(
    page_title="AI智能客服系统",
    page_icon="🤖",
    layout="centered"
)

# 初始化session state
if 'agent' not in st.session_state:
    if OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here":
        try:
            st.session_state.agent = CustomerServiceAgent()
            st.session_state.messages = []
        except Exception as e:
            st.error(f"初始化失败: {e}")
            st.session_state.agent = None
    else:
        st.session_state.agent = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

# 页面标题
st.title("🤖 AI智能客服系统")
st.markdown("基于RAG技术的智能问答助手")

# 检查配置
if not st.session_state.agent:
    st.warning("⚠️ 请先配置 OpenAI API Key")
    api_key = st.text_input("输入你的 OpenAI API Key", type="password")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.rerun()
    st.stop()

# 侧边栏
with st.sidebar:
    st.header("设置")
    
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.session_state.agent.clear_history()
        st.rerun()
    
    st.divider()
    st.markdown("### 📚 知识库")
    st.markdown("系统已加载以下文档：")
    st.markdown("- 退款政策")
    st.markdown("- 配送政策")
    st.markdown("- 会员政策")
    st.markdown("- 常见问题")
    
    st.divider()
    st.markdown("### 🔧 支持功能")
    st.markdown("✅ 智能问答")
    st.markdown("✅ 订单查询")
    st.markdown("✅ 价格计算")
    st.markdown("✅ 物流追踪")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("输入你的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 获取AI回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = st.session_state.agent.chat(prompt)
            answer = response['answer']
            
            # 显示回答
            st.markdown(answer)
            
            # 显示来源
            if response['sources']:
                with st.expander("📚 查看来源"):
                    for source in response['sources']:
                        st.markdown(f"- {source}")
            
            # 显示工具使用
            if response['used_tools']:
                with st.expander("🔧 使用工具"):
                    for tool in response['used_tools']:
                        st.markdown(f"- {tool}")
    
    # 保存AI消息
    st.session_state.messages.append({"role": "assistant", "content": answer})

# 页脚
st.divider()
st.caption("🚀 基于 LangChain + OpenAI + RAG 技术构建")

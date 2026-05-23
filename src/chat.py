"""
对话主程序 - 命令行交互界面
"""
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

# 添加src目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import CustomerServiceAgent
from config import OPENAI_API_KEY

console = Console()


def print_welcome():
    """打印欢迎信息"""
    welcome_text = """
🤖 欢迎使用 AI智能客服系统

命令：
- 直接输入问题进行对话
- 输入 /clear 清空历史
- 输入 /exit 退出程序
"""
    console.print(Panel(welcome_text, title="AI Agent Demo", border_style="blue"))


def print_response(response: dict):
    """格式化打印回答"""
    # AI回答
    console.print("\n[bold cyan]🤖 AI客服:[/bold cyan]")
    console.print(Markdown(response['answer']))
    
    # 来源信息
    if response['sources']:
        sources_str = ", ".join(response['sources'])
        console.print(f"\n[dim]📚 参考来源: {sources_str}[/dim]")
    
    # 工具使用
    if response['used_tools']:
        tools_str = ", ".join(response['used_tools'])
        console.print(f"[dim]🔧 使用工具: {tools_str}[/dim]")
    
    console.print("-" * 50)


def check_api_key():
    """检查API Key"""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        console.print("[red]❌ 错误: 请先配置 OpenAI API Key[/red]")
        console.print("\n1. 复制 .env.example 为 .env")
        console.print("2. 编辑 .env 文件，填入你的 API Key")
        console.print("\n获取 API Key: https://platform.openai.com/api-keys")
        return False
    return True


def main():
    """主函数"""
    print_welcome()
    
    # 检查配置
    if not check_api_key():
        return
    
    # 检查向量库是否存在
    if not os.path.exists("./chroma_db"):
        console.print("[yellow]⚠️ 向量数据库不存在，请先运行: python src/build_index.py[/yellow]")
        console.print("是否现在构建？(y/n)")
        choice = input("> ").strip().lower()
        if choice == 'y':
            os.system("python src/build_index.py")
        else:
            return
    
    # 初始化Agent
    try:
        console.print("\n[green]🚀 正在启动 AI 客服...[/green]")
        agent = CustomerServiceAgent()
        console.print("[green]✅ 启动成功！\n[/green]")
    except Exception as e:
        console.print(f"[red]❌ 启动失败: {e}[/red]")
        return
    
    # 对话循环
    while True:
        try:
            # 获取用户输入
            user_input = Prompt.ask("\n[bold green]👤 用户[/bold green]").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() == '/exit':
                console.print("\n[blue]👋 再见！[/blue]")
                break
            
            if user_input.lower() == '/clear':
                agent.clear_history()
                continue
            
            # 处理用户问题
            with console.status("[bold yellow]🤔 思考中..."):
                response = agent.chat(user_input)
            
            print_response(response)
            
        except KeyboardInterrupt:
            console.print("\n\n[blue]👋 再见！[/blue]")
            break
        except Exception as e:
            console.print(f"\n[red]❌ 错误: {e}[/red]")


if __name__ == "__main__":
    main()

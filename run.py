import os
import sys

# 切换到项目目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*50)
print("🤖 AI Agent Demo - 启动器")
print("="*50)

print("\n请选择操作:")
print("1. 构建知识库索引 (首次运行)")
print("2. 启动对话系统")
print("3. 一键部署到Streamlit")
print("4. 退出")

choice = input("\n请输入选项 (1-4): ").strip()

if choice == '1':
    print("\n🔧 正在构建知识库...")
    os.system("python src/build_index.py")
    print("\n✅ 构建完成！现在可以启动对话系统了。")
    input("按回车键退出...")
    
elif choice == '2':
    print("\n🚀 启动对话系统...")
    os.system("python src/chat.py")
    
elif choice == '3':
    print("\n🌐 部署到Streamlit...")
    print("请先确保已安装 streamlit: pip install streamlit")
    print("然后运行: streamlit run src/app.py")
    input("按回车键退出...")
    
elif choice == '4':
    print("\n👋 再见！")
    
else:
    print("\n❌ 无效选项")

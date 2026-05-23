"""
构建向量索引 - 将知识库文档转换为向量存储
"""
import os
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader,
    DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import (
    OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL,
    CHROMA_DB_PATH, DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP
)


def load_documents(data_dir: str):
    """加载所有文档"""
    documents = []
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"⚠️ 数据目录不存在: {data_dir}")
        print("📁 创建示例数据...")
        create_sample_data(data_dir)
        return load_documents(data_dir)
    
    # 加载文本文件
    txt_files = list(data_path.glob("*.txt"))
    for file in txt_files:
        print(f"📄 加载: {file.name}")
        loader = TextLoader(str(file), encoding='utf-8')
        documents.extend(loader.load())
    
    # 加载Markdown文件
    md_files = list(data_path.glob("*.md"))
    for file in md_files:
        print(f"📝 加载: {file.name}")
        loader = TextLoader(str(file), encoding='utf-8')
        documents.extend(loader.load())
    
    # 加载PDF文件
    pdf_files = list(data_path.glob("*.pdf"))
    for file in pdf_files:
        print(f"📑 加载: {file.name}")
        loader = PyPDFLoader(str(file))
        documents.extend(loader.load())
    
    return documents


def create_sample_data(data_dir: str):
    """创建示例知识库数据"""
    os.makedirs(data_dir, exist_ok=True)
    
    # 退款政策
    refund_policy = """退款政策

1. 7天无理由退款
   - 自签收之日起7天内，商品未使用、包装完好，可申请无理由退款
   - 退款将在3-5个工作日内原路返回

2. 质量问题退款
   - 商品存在质量问题，提供照片/视频证明后可申请全额退款
   - 运费由我方承担

3. 超过7天退款
   - 根据商品使用时长按比例退款
   - 电子产品使用超过30天不支持退款

4. 不支持退款的情况
   - 已激活的软件/数字产品
   - 个性化定制商品
   - 使用过的一次性消耗品"""
    
    # 配送政策
    shipping_policy = """配送政策

1. 配送范围
   - 全国大陆地区（除偏远地区外）
   - 港澳台及海外请咨询客服

2. 配送时效
   - 标准快递：3-5个工作日
   - 顺丰速运：1-3个工作日
   - 偏远地区增加2-3天

3. 运费标准
   - 订单满299元包邮
   - 不满299元收取运费10元
   - 偏远地区（新疆、西藏等）额外收取20元

4. 发货时间
   - 工作日16:00前下单，当日发货
   - 16:00后下单，次日发货
   - 预售商品以页面标注时间为准"""
    
    # 会员政策
    vip_policy = """会员政策

1. 会员等级
   - 普通会员：注册即享
   - 银卡会员：累计消费满1000元
   - 金卡会员：累计消费满5000元
   - 黑卡会员：累计消费满20000元

2. 会员权益
   - 普通会员：9.8折，生日优惠券
   - 银卡会员：9.5折，优先发货，生日双倍积分
   - 金卡会员：9折，专属客服，免运费
   - 黑卡会员：8.5折，新品优先购，年度礼盒

3. 积分规则
   - 消费1元=1积分
   - 积分可抵扣现金（100积分=1元）
   - 积分有效期2年"""
    
    # 常见问题
    faq = """常见问题FAQ

Q: 如何修改订单地址？
A: 订单未发货前可联系客服修改，已发货无法修改。

Q: 收到的商品有破损怎么办？
A: 请当场拒收并拍照联系客服，我们会安排补发。

Q: 发票什么时候开具？
A: 默认电子发票，订单完成后自动发送至邮箱。

Q: 支持货到付款吗？
A: 目前仅支持在线支付（微信、支付宝、银行卡）。

Q: 如何联系客服？
A: 工作时间9:00-21:00，可通过在线客服、电话400-xxx-xxxx、或邮箱service@example.com联系。"""
    
    # 写入文件
    with open(os.path.join(data_dir, "退款政策.txt"), "w", encoding="utf-8") as f:
        f.write(refund_policy)
    
    with open(os.path.join(data_dir, "配送政策.txt"), "w", encoding="utf-8") as f:
        f.write(shipping_policy)
    
    with open(os.path.join(data_dir, "会员政策.txt"), "w", encoding="utf-8") as f:
        f.write(vip_policy)
    
    with open(os.path.join(data_dir, "常见问题.txt"), "w", encoding="utf-8") as f:
        f.write(faq)
    
    print(f"✅ 已创建示例数据到 {data_dir}")


def build_index():
    """构建向量索引"""
    print("🔧 开始构建知识库索引...")
    
    # 1. 加载文档
    print(f"\n📚 加载文档...")
    documents = load_documents(DATA_DIR)
    
    if not documents:
        print("❌ 没有找到任何文档")
        return
    
    print(f"✅ 共加载 {len(documents)} 个文档")
    
    # 2. 分割文本
    print(f"\n✂️ 分割文本...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "，", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ 共生成 {len(chunks)} 个文本块")
    
    # 3. 创建向量数据库
    print(f"\n🧠 生成向量嵌入...")
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )
    
    # 4. 存储到Chroma
    print(f"\n💾 保存到向量数据库...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    print(f"\n✅ 索引构建完成！")
    print(f"   - 文档数量: {len(documents)}")
    print(f"   - 文本块数量: {len(chunks)}")
    print(f"   - 存储路径: {CHROMA_DB_PATH}")


if __name__ == "__main__":
    build_index()

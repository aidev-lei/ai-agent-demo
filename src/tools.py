"""
工具函数 - 模拟查询订单、库存等实时信息
"""
import re
import random
from datetime import datetime, timedelta
from typing import List, Dict


class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools = {
            'query_order': self.query_order,
            'calculate_price': self.calculate_price,
            'check_inventory': self.check_inventory,
            'get_shipping_status': self.get_shipping_status
        }
    
    def detect_tool_need(self, user_input: str) -> List[str]:
        """检测用户输入是否需要调用工具"""
        input_lower = user_input.lower()
        needed_tools = []
        
        # 订单查询
        if any(kw in input_lower for kw in ['订单', 'order', '购买记录', '买的东西']):
            needed_tools.append('query_order')
        
        # 价格计算
        if any(kw in input_lower for kw in ['多少钱', '价格', '计算', '费用']):
            needed_tools.append('calculate_price')
        
        # 库存查询
        if any(kw in input_lower for kw in ['库存', '有货吗', '还有吗', '现货']):
            needed_tools.append('check_inventory')
        
        # 物流查询
        if any(kw in input_lower for kw in ['物流', '快递', '发货', '到哪里', 'tracking']):
            needed_tools.append('get_shipping_status')
        
        return needed_tools
    
    def execute_tool(self, tool_name: str, user_input: str) -> str:
        """执行工具"""
        if tool_name in self.tools:
            return self.tools[tool_name](user_input)
        return f"未知工具: {tool_name}"
    
    def query_order(self, user_input: str) -> str:
        """模拟查询订单"""
        # 尝试提取订单号
        order_pattern = r'(?:订单号|订单编号|order)[：:\s]*(\w+)'
        match = re.search(order_pattern, user_input, re.IGNORECASE)
        
        if match:
            order_id = match.group(1)
            # 模拟订单数据
            return f"订单号 {order_id}: 已付款，准备发货。商品：示例商品A x2，金额：¥199.00"
        else:
            # 返回最近的订单
            return "您最近的订单：\n- 订单号: ORD20240115001\n- 商品: 示例商品A\n- 状态: 已发货\n- 物流: 顺丰速运 SF1234567890"
    
    def calculate_price(self, user_input: str) -> str:
        """模拟价格计算"""
        # 简单示例：计算折扣后价格
        return """价格计算参考：
- 商品原价：¥299.00
- 会员折扣：9折 (-¥29.90)
- 优惠券：-¥20.00
- 最终价格：¥249.10
（满299包邮）"""
    
    def check_inventory(self, user_input: str) -> str:
        """模拟库存查询"""
        products = {
            '手机': 156,
            '耳机': 89,
            '充电器': 234,
            '保护壳': 567
        }
        
        for product, stock in products.items():
            if product in user_input:
                status = "库存充足" if stock > 50 else "库存紧张" if stock > 10 else "库存不足"
                return f"{product}: 当前库存 {stock} 件 ({status})"
        
        return "大部分商品库存充足，具体到货时间请咨询客服"
    
    def get_shipping_status(self, user_input: str) -> str:
        """模拟物流查询"""
        # 模拟物流状态
        today = datetime.now()
        events = [
            (today - timedelta(days=2), "【深圳市】已揽收"),
            (today - timedelta(days=2), "【深圳市】已发出，下一站上海"),
            (today - timedelta(days=1), "【上海市】已到达分拨中心"),
            (today - timedelta(hours=4), "【上海市】快递员正在派送中"),
        ]
        
        tracking_info = "\n".join([f"{date.strftime('%m-%d %H:%M')} {event}" for date, event in events])
        return f"物流单号: SF1234567890\n最新状态: 派送中\n\n物流详情:\n{tracking_info}"

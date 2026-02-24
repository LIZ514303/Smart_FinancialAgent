import csv
import random
from datetime import datetime, timedelta


def generate_mock_billing_csv(filename="mock_bills.csv", num_records=50):
    # 预设一些真实感的随机数据源
    merchants = {
        "餐饮": ["星巴克", "麦当劳", "海底捞", "本地居酒屋", "瑞幸咖啡"],
        "购物": ["淘宝", "亚马逊", "优衣库", "京东", "宜家"],
        "娱乐": ["Netflix", "Steam", "电影院", "Spotify", "健身房"],
        "交通": ["滴滴出行", "中石化", "特斯拉充电站", "中国铁路"],
        "生活": ["国家电网", "中国移动", "物业管理", "自来水公司"]
    }

    statuses = ["已付款", "待处理", "已退款"]
    categories = list(merchants.keys())

    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(["交易日期", "账单ID", "商户名称", "分类", "金额(元)", "状态"])

        start_date = datetime.now() - timedelta(days=90)  # 生成最近90天的数据

        for i in range(num_records):
            category = random.choice(categories)
            merchant = random.choice(merchants[category])

            # 随机生成日期
            random_days = random.randint(0, 90)
            date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M")

            # 随机生成账单 ID 和金额
            bill_id = f"TXN{random.randint(100000, 999999)}"
            amount = round(random.uniform(5.0, 2000.0), 2)
            status = random.choices(statuses, weights=[85, 10, 5])[0]  # 85% 是已付款

            writer.writerow([date, bill_id, merchant, category, amount, status])

    print(f"成功！已生成 {num_records} 条记录到文件: {filename}")


if __name__ == "__main__":
    generate_mock_billing_csv()
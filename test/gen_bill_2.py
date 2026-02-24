import pandas as pd
import random
from datetime import datetime, timedelta


def generate_finance_data(num_records=30):
    categories = {
        "餐饮": ["支出", (20, 150)],
        "交通": ["支出", (5, 50)],
        "购物": ["支出", (100, 1000)],
        "娱乐": ["支出", (30, 300)],
        "工资": ["收入", (15000, 15000)],
        "理财收益": ["收入", (50, 200)],
        "订阅服务": ["支出", (15, 60)]
    }

    data = []
    start_date = datetime(2026, 2, 1)

    for i in range(num_records):
        # 随机选择日期、分类
        current_date = (start_date + timedelta(days=random.randint(0, 27))).strftime("%Y-%m-%d")
        category = random.choice(list(categories.keys()))
        type_val, range_val = categories[category]

        # 模拟金额
        if category == "工资":
            # 工资只在月初发一次
            if any(d['分类'] == '工资' for d in data): continue
            amount = range_val[0]
        else:
            amount = round(random.uniform(range_val[0], range_val[1]), 2)

        data.append({
            "日期": current_date,
            "分类": category,
            "金额": amount,
            "收支类型": type_val,
            "备注": "测试数据"
        })

    # 转换为 DataFrame 并保存
    df = pd.DataFrame(data)
    # 按日期排序，让账单看起来更真实
    df = df.sort_values(by="日期")

    file_name = "test_bill_2026.csv"
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"✅ 测试账单已生成: {file_name}")
    print(df.head())


if __name__ == "__main__":
    generate_finance_data()
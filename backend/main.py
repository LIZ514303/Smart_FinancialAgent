import os
import json
import io
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from dotenv import load_dotenv
from hello_agents import SimpleAgent, HelloAgentsLLM
from plyer import notification

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 独立出来的通知函数
def send_desktop_notify(message):
    try:
        notification.notify(
            title="Auto-FinancialAssistance",
            message=message,
            timeout=5
        )
    except:
        pass

@app.get("/")
async def root():
    return {"status": "Service is active"}

@app.post("/analyze")
async def analyze_finance(file: UploadFile = File(...)):
    api_key = os.getenv("GEMINI_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # 极简统计数据
        income = df[df.iloc[:, 3].str.contains('入', na=False)].iloc[:, 2].sum()
        expense = df[df.iloc[:, 3].str.contains('支', na=False)].iloc[:, 2].sum()

        llm = HelloAgentsLLM(api_key=api_key, model="gemini-2.0-flash", base_url=base_url)
        
        # --- 核心修正：只传递框架确定支持的参数 ---
        agent = SimpleAgent(name="FinanceAgent", llm=llm)

        prompt = f"""
        你是理财专家。本月收入{income}，支出{expense}。
        请严格按 JSON 格式分析，包含以下三个 key：
        1. analysis_result: 收支盈亏总结。
        2. habit_report: 消费习惯深度分析。
        3. tasks: 包含7个具体理财任务的列表。
        输出示例：{{"analysis_result": "...", "habit_report": "...", "tasks": ["..."]}}
        """
        
        raw_res = agent.run(prompt)
        
        # 提取并解析 JSON
        start = raw_res.find("{")
        end = raw_res.rfind("}") + 1
        data = json.loads(raw_res[start:end])

        # 在分析成功后，手动触发通知（代替原本 Agent 内部的 Tool 调用）
        if data.get("tasks"):
            send_desktop_notify(f"今日建议：{data['tasks'][0]}")

        return data

    except Exception as e:
        return {"error": f"系统执行异常: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
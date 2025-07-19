import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
load_dotenv(".env")

# OpenAI APIキーの取得
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI APIキーが設定されていません。.env ファイルに OPENAI_API_KEY を記述してください。")
    st.stop()

# LLMモデルの初期化
llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7, model="gpt-3.5-turbo")

# 専門家ごとのシステムメッセージを返す関数
def get_system_message(expert_type: str) -> str:
    if expert_type == "心理学者":
        return (
            "あなたは経験豊富な心理学者です。"
            "ユーザーの感情や心理的な問題に寄り添い、優しく丁寧に助言をしてください。"
        )
    elif expert_type == "キャリアコンサルタント":
        return (
            "あなたは実績あるキャリアコンサルタントです。"
            "ユーザーの仕事・転職・将来設計の悩みに的確なアドバイスを提供してください。"
        )
    else:
        return "あなたは有能な専門家です。ユーザーに役立つアドバイスをしてください。"

# 入力と選択値を元にLLMから回答を得る関数
def get_expert_advice(user_input: str, expert_type: str) -> str:
    system_prompt = get_system_message(expert_type)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    response = llm(messages)
    return response.content

# --- Streamlit UI 定義 ---
st.set_page_config(page_title="専門家LLMアドバイザー", layout="centered")

st.title("🧑専門家LLMアドバイザー")
st.markdown("""
このアプリでは、以下の専門家の視点からLLMがあなたの質問に回答します：

1. **心理学者**：心の悩み、ストレス、対人関係の相談  
2. **キャリアコンサルタント**：就職・転職・キャリア設計に関する相談

ご相談内容を入力し、専門家を選択してください。
""")

# 専門家の選択
expert_choice = st.radio(
    "🔍 専門家の種類を選んでください：",
    ("心理学者", "キャリアコンサルタント")
)

# ユーザーの質問入力
user_input = st.text_area("💬 ご相談内容を入力してください：", height=150)

# 送信ボタン
if st.button("✅ 回答を得る"):
    if user_input.strip() == "":
        st.warning("ご相談内容を入力してください。")
    else:
        with st.spinner("専門家が回答中です..."):
            result = get_expert_advice(user_input, expert_choice)
            st.success("✅ 専門家からのアドバイス：")
            st.write(result)

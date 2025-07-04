import streamlit as st
from datetime import date

st.set_page_config(page_title="回転率マークツール", layout="centered")
st.title("📊 回転率マークツール（個人用）")

st.markdown("""
このツールでは、パチンコ台の回転率を記録・計算できます。

入力された情報から以下を表示：
- 総打ち込み玉数（現金投資から自動算出）
- 総回転数（手入力）
- 回転率（1kあたりの回転数）
""")

# --- 入力欄 ---
st.subheader("✏️ 入力欄")

col1, col2 = st.columns(2)
with col1:
    input_date = st.date_input("日付", value=date.today())
    shop_name = st.text_input("ホール名")
    machine_name = st.text_input("機種名")
    machine_number = st.text_input("台番号")

with col2:
    total_spins = st.number_input("総回転数（例：2300）", min_value=0, step=1)
    final_balls = st.number_input("最終出玉（発）", min_value=0, step=1)
    investment_yen = st.number_input("現金投資（円）", min_value=0, step=100)
    balls_per_1k = st.number_input("1kあたりの貸玉数（通常250）", min_value=1, value=250, step=10)

# --- 計算 ---
if total_spins > 0 and investment_yen > 0:
    invested_balls = investment_yen / 1000 * balls_per_1k
    rotation_rate = total_spins / (invested_balls / balls_per_1k)
    profit_balls = final_balls - invested_balls

    st.subheader("✅ 出力結果")
    st.write("### 記録内容：")
    st.markdown(f"""
    - **日付**：{input_date}
    - **ホール名**：{shop_name}
    - **機種名**：{machine_name}
    - **台番号**：{machine_number}
    - **総打ち込み玉数**：{int(invested_balls)} 発
    - **総回転数**：{total_spins} 回
    - **回転率（1kあたり）**：{rotation_rate:.2f} 回
    """)
else:
    st.info("総回転数と現金投資額を入力してください。")
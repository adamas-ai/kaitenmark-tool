import streamlit as st

st.set_page_config(page_title="回転率マークツール", layout="centered")
st.title("回転率マークツール")

st.markdown("""
### ✨ 台の効率チェックを行います
代金価値、ボーダー、電サポ増減などを基にした計算ツールです
""")

# --- 入力項目 ---
date = st.text_input("🗓️ 日付")
shop = st.text_input("🏪 店名")
machine = st.text_input("🎰 機種名")

spins = st.number_input("♻️ 総回転数（数字のみ）", min_value=1, step=1)
border = st.number_input("📊 ボーダー（例: 18.7）", value=18.7, step=0.1)
densa = st.number_input("⚡ 電サポ増減（例: -100玉）", value=-100, step=10)
kankin = st.number_input("💸 換金率（例: 3.57円 = 28玉交換）", value=3.57, step=0.01)

# --- 内部計算 ---
if spins and border and kankin:
    try:
        # 1回転するのに必要な玉数
        tama_per_spin = 250 / border

        # 理論打ち込み玉数
        total_tama = tama_per_spin * spins + densa

        # 逆算の回転率
        reverse_rotation = (spins / total_tama) * 250 if total_tama > 0 else 0

        # 判定
        diff = reverse_rotation - border
        if total_tama <= 0 or reverse_rotation <= 0 or reverse_rotation > 100:
            judge = "E"
        elif diff >= 3:
            judge = "○"
        elif diff >= 1.5:
            judge = "△"
        elif diff < 0:
            judge = "✗"
        else:
            judge = "○"

        # --- 表示 ---
        st.markdown("---")
        st.success(f"推定打ち込み玉数：{int(total_tama):,} 玉")
        st.success(f"算出された回転率：{reverse_rotation:.2f} 回転 / 250玉")
        st.info(f"評価：{judge}")

    except Exception as e:
        st.error(f"計算中にエラーが発生しました: {e}")
else:
    st.info("必要な項目をすべて入力してください。")

import streamlit as st

st.set_page_config(page_title="回転率マークツール", layout="centered")
st.title("回転率マークツール")

st.markdown("""
🔁 釘の効率チェックを行います  
ボーダー、換金率などを基にした計算ツールです
""")

# --- 入力欄 ---
date = st.text_input("📅 日付")
shop = st.text_input("🏪 店名")
machine = st.text_input("🎰 機種名")
dainumber = st.text_input("🔢 台番号")

spins = st.number_input("🔁 総回転数（数字のみ）", min_value=1, step=1)
border = st.number_input("📏 ボーダー（例: 18.7）", value=18.7, step=0.1)
kankin = st.number_input("💰 換金率（例: 28 = 28玉交換）", value=28, step=0.1)

# --- 内部計算 ---
if spins and border and kankin:
    try:
        # 1回転あたりに必要な玉数
        tama_per_spin = 250 / border

        # 推定打ち込み玉数
        total_tama = tama_per_spin * spins

        # 逆算回転率（1Kあたりの回転数）
        reverse_rotation = (spins / total_tama) * 250 if total_tama > 0 else 0

        # 評価
        diff = reverse_rotation - border
        if total_tama <= 0 or reverse_rotation <= 0 or abs(diff) >= 10:
            judge = "E"
        elif diff >= 2.5:
            judge = "○"
        elif diff >= 0:
            judge = "△"
        elif diff < 0:
            judge = "✗"
        else:
            judge = "E"

        # --- 出力 ---
        st.markdown("---")
        st.subheader("📊 結果")
        st.write(f"📅 日付：{date}")
        st.write(f"🏪 店名：{shop}")
        st.write(f"🎰 機種名：{machine}")
        st.write(f"🔢 台番号：{dainumber}")
        st.write(f"💥 総回転数：{spins} 回")
        st.write(f"🔢 推定打ち込み玉数：{int(total_tama):,} 玉")
        st.write(f"🔁 算出された回転率：{reverse_rotation:.2f} 回転 / 250玉")
        st.write(f"📈 評価：{judge}")

    except Exception as e:
        st.error(f"計算中にエラーが発生しました: {e}")
else:
    st.info("回転数、ボーダー、換金率を入力してください。")

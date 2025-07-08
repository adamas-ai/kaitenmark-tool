import streamlit as st
import pandas as pd

st.set_page_config(page_title="回転率マークツール", layout="centered")

st.title("🎯 回転率マークツール")
st.write("通常回転数と機種ボーダーから、推定打ち込み玉数と回転率を算出")

with st.form("input_form"):
    date = st.date_input("📅 日付")
    shop = st.text_input("🏪 店名")
    machine = st.text_input("🎰 機種名")
    number = st.text_input("🔢 台番号")
    spins = st.number_input("🔁 通常回転数", min_value=0)
    border = st.number_input("🎯 ボーダー（例: 18.7）", min_value=0.1)
    kankin = st.number_input("💰 換金率（例: 28 = 28玉交換）", value=28.0, min_value=1.0)

    submitted = st.form_submit_button("📊 計算する")

if submitted:
    try:
        # 補正係数
        correction_factor = 1.1

        # 計算
        tama_per_spin = 250 / border
        total_tama = spins * tama_per_spin * correction_factor
        reverse_rotation = (spins / total_tama) * 250

        # 評価ロジック
        gap = reverse_rotation - border
        if abs(gap) >= 10:
            judge = "E"
        elif gap >= 2.5:
            judge = "○"
        elif 2.0 <= gap < 2.5:
            judge = "△"
        else:
            judge = "✗"

        # 出力データ
        result = {
            "📅 日付": [date],
            "🏪 店名": [shop],
            "🎰 機種名": [machine],
            "🔢 台番号": [number],
            "🔁 通常回転数": [spins],
            "🔢 推定打ち込み玉数": [round(total_tama)],
            "🔁 回転率": [round(reverse_rotation, 2)],
            "📈 評価": [judge]
        }

        df = pd.DataFrame(result)

        st.success("✅ 結果")
        st.table(df)

        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 結果をCSVでダウンロード",
            data=csv,
            file_name="kaiten_result.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"計算中にエラーが発生しました: {e}")

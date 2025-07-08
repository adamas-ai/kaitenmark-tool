import streamlit as st
import pandas as pd

st.set_page_config(page_title="回転率マークツール", layout="centered")

st.title("🎯 回転率マークツール")
st.write("通常回転数から推定打ち込み玉数と回転率を計算します")

with st.form("input_form"):
    date = st.date_input("📅 日付")
    shop = st.text_input("🏪 店名")
    machine = st.text_input("🎰 機種名")
    number = st.text_input("🔢 台番号")

    # 通常回転数：初期値なし、+/- ボタンなし
    spins_raw = st.text_input("🔁 通常回転数（数字のみ）", value="")
    
    submitted = st.form_submit_button("📊 計算する")

if submitted:
    try:
        if not spins_raw.strip().isdigit():
            st.error("通常回転数は数字で入力してください。")
        else:
            spins = int(spins_raw)

            # パラメータ
            base_tama = 13.3
            correction = 1.1
            adjusted_tama_per_spin = base_tama * correction  # ≒14.63
            total_tama = spins * adjusted_tama_per_spin

            # 回転率計算
            reverse_rotation = (spins / total_tama) * 250

            # 評価基準（仮ボーダー18.7基準）
            border = 18.7
            gap = reverse_rotation - border
            if abs(gap) >= 10:
                judge = "E"
            elif gap >= 2.5:
                judge = "○"
            elif 2.0 <= gap < 2.5:
                judge = "△"
            else:
                judge = "✗"

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
            
            st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
            st.code(df.to_string(index=False), language="text")
            
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 結果をCSVでダウンロード",
                data=csv,
                file_name="kaiten_result.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"計算中にエラーが発生しました: {e}")
